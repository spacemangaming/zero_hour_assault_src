import socket
import threading
import queue
import websocket
import nacl.utils
import nacl.public
import nacl.encoding
import traceback
import sys

event_none = 0
event_connect = 1     # Map to ENet EVENT_TYPE_CONNECT
event_disconnect = 2  # Map to ENet EVENT_TYPE_DISCONNECT
event_receive = 3     # Map to ENet EVENT_TYPE_RECEIVE

SERVER_PUBLIC_KEY_B64 = "svNwUAv3H3FdcaFeqZi/ZgbEWg4Y4e5qsP1yyS3/Llo="
HANDSHAKE_CHANNEL = 30

class SecurePeer:
    def __init__(self, ws):
        self.ws = ws
        self.box = None
        self.secure = False
        self.handshake_complete = False

class network:
    def __init__(self):
        self.ws = None
        self.secure_peer = None
        self.peer = None
        self.client_private_key = None
        self.event_queue = queue.Queue()
        self.thread = None
        self.connected = False
        self.channelLimit = 100

    def setup_server(self, port, maxchans, maxpeers):
        # Client network class doesn't setup server, but keep API compatibility
        pass

    def setup_client(self, maxchans, maxpeers):
        self.client_private_key = nacl.public.PrivateKey.generate()
        self.event_queue = queue.Queue()
        self.connected = False
        return self

    def connect(self, address, port):
        if isinstance(address, bytes):
            address = address.decode("utf-8")
        # Force IPv4 for localhost — Windows tries ::1 first, times out, then falls back (~2s delay)
        if address == "localhost":
            address = "127.0.0.1"

        # Use ws:// for local/dev connections, wss:// for production domain names
        is_local = (
            "localhost" in address
            or "127.0.0.1" in address
            or address.startswith("192.168.")
            or address.startswith("10.")
            or address.startswith("100.")  # Tailscale IP range
            or not ("." in address)        # bare hostnames / test names like "0user"
        )
        protocol = "ws" if is_local else "wss"

        if "://" in address:
            url = address
        else:
            url = f"{protocol}://{address}:{port}"

        self.connected = False

        # Capture the queue by value so this thread always fires events into
        # *this* connection's queue, even if setup_client() later replaces
        # self.event_queue for a new connection attempt.
        _queue = self.event_queue

        def ws_thread_target():
            try:
                ws = websocket.WebSocket()
                # ── Critical latency fix ───────────────────────────────────────
                # TCP_NODELAY disables Nagle's Algorithm so each game packet is
                # flushed to the wire immediately without waiting to coalesce with
                # others. This eliminates the 40-80ms buffering spikes.
                # SO_KEEPALIVE keeps the Tailscale / NAT session alive without
                # requiring application-level pings.
                ws.connect(
                    url,
                    timeout=10,
                    sockopt=(
                        (socket.IPPROTO_TCP, socket.TCP_NODELAY, 1),
                        (socket.SOL_SOCKET,  socket.SO_KEEPALIVE, 1),
                    ),
                )
                # ───────────────────────────────────────────────────────────────
                self.ws = ws
                self.secure_peer = SecurePeer(ws)

                # Step 1: Send our ephemeral public key on handshake channel 30
                client_public_key_bytes = self.client_private_key.public_key.encode()
                handshake_packet = bytes([HANDSHAKE_CHANNEL]) + client_public_key_bytes
                ws.send_binary(handshake_packet)

                # Wait for handshake confirmation [channel_byte(30)] + b"OK"
                response = ws.recv()
                # recv() may return str or bytes depending on how server sent it
                if isinstance(response, str):
                    response = response.encode("utf-8")

                if not response or len(response) < 2 or response[0] != HANDSHAKE_CHANNEL:
                    raise RuntimeError(f"Failed secure handshake: unexpected response: {response!r}")

                # Build the shared PyNaCl Box for encryption
                server_public_key = nacl.public.PublicKey(SERVER_PUBLIC_KEY_B64, encoder=nacl.encoding.Base64Encoder)
                self.secure_peer.box = nacl.public.Box(self.client_private_key, server_public_key)
                self.secure_peer.secure = True
                self.secure_peer.handshake_complete = True
                self.peer = self.secure_peer

                self.connected = True

                # Fire event_connect into the game loop queue
                evt = network_event()
                evt.type = event_connect
                evt.peer_id = self.secure_peer
                _queue.put(evt)

                # The timeout=10 we passed to ws.connect() applies to ALL socket
                # operations including recv(). Now that the handshake is done we
                # reset it to None (blocking, no timeout) so the receive loop
                # waits indefinitely for the next game packet without timing out
                # during idle periods (e.g. standing still, in a menu, etc.).
                ws.sock.settimeout(None)

                # Main receive loop
                while self.connected:
                    message = ws.recv()
                    if message is None:
                        break

                    if isinstance(message, str):
                        message = message.encode("utf-8")

                    if len(message) == 0:
                        continue

                    channel = message[0]
                    payload = message[1:]

                    if channel != 5 and channel != 6:
                        try:
                            decrypted_data = self.secure_peer.box.decrypt(payload)
                        except Exception:
                            continue
                    else:
                        decrypted_data = payload

                    evt = network_event()
                    evt.type = event_receive
                    evt.peer_id = self.secure_peer
                    evt.channel = channel

                    if channel != 5:
                        try:
                            evt.message = decrypted_data.decode("utf-8")
                        except UnicodeDecodeError:
                            evt.message = decrypted_data
                    else:
                        evt.message = decrypted_data

                    _queue.put(evt)

            except Exception as e:
                import traceback
                print(f"[WS Client] Connection error: {e}")
                traceback.print_exc()
            finally:
                self.connected = False
                self.peer = None
                evt = network_event()
                evt.type = event_disconnect
                evt.peer_id = self.secure_peer
                _queue.put(evt)

        self.thread = threading.Thread(target=ws_thread_target, daemon=True, name="ws-client")
        self.thread.start()
        return self.ws

    def destroy(self):
        self.connected = False
        if self.ws:
            try:
                self.ws.close()
            except:
                pass
            self.ws = None
        self.peer = None
        return True

    def broadcast(self, message, channel):
        # Client does not broadcast
        pass

    def is_active(self):
        return self.ws is not None and self.connected

    def get_peer_list(self):
        return [self.secure_peer] if self.secure_peer else []

    def get_peer_count(self):
        return 1 if self.connected else 0

    def get_total_received_data(self):
        return 0

    def get_total_received_packets(self):
        return 0

    def get_total_sent_data(self):
        return 0

    def get_total_sent_packets(self):
        return 0

    def request(self, timeout=0):
        # Non-blocking poll of thread-safe message queue
        try:
            if timeout > 0:
                evt = self.event_queue.get(timeout=timeout / 1000.0)
            else:
                evt = self.event_queue.get_nowait()
            return evt
        except queue.Empty:
            evt = network_event()
            evt.type = event_none
            return evt

    def get_peer_address(self, peer):
        if self.ws and self.ws.connected:
            return self.ws.sock.getpeername() if self.ws.sock else ("0.0.0.0", 0)
        return ("0.0.0.0", 0)

    def get_peer_average_round_trip_time(self, peer):
        # Return mock low-latency ping for TCP stream
        return 15

    def disconnect_peer(self, peer):
        self.destroy()
        return True

    def disconnect_peer_softly(self, peer):
        self.destroy()
        return True

    def disconnect_peer_forcefully(self, peer):
        self.destroy()
        return True

    def _prepare_packet_data(self, message):
        if isinstance(message, str):
            return message.encode("utf-8")
        return message

    def send_reliable(self, peer, message, channel):
        if not self.connected or not self.secure_peer or not self.secure_peer.secure:
            return False

        raw_message = self._prepare_packet_data(message)
        if channel != 5 and channel != 6:
            encrypted_message = self.secure_peer.box.encrypt(raw_message)
        else:
            encrypted_message = raw_message

        # Packet format: [1-byte channel] + [encrypted payload]
        packet = bytes([channel]) + encrypted_message
        try:
            self.ws.send_binary(packet)
            return True
        except:
            return False

    def send_unreliable(self, peer, message, channel):
        # Since TCP natively guarantees transport delivery, standard ws.send is fully secure & reliable
        return self.send_reliable(peer, message, channel)

class network_event:
    def __init__(self):
        self.type = event_none
        self.peer_id = None
        self.message = ""
        self.channel = -1
