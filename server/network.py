import asyncio
import websockets
import threading
import queue
import socket
import nacl.utils
import nacl.public
import nacl.encoding
import os
import traceback
import sys

event_none = 0
event_connect = 1     # ENet EVENT_TYPE_CONNECT
event_disconnect = 2  # ENet EVENT_TYPE_DISCONNECT
event_receive = 3     # ENet EVENT_TYPE_RECEIVE

HANDSHAKE_CHANNEL = 30

class SecurePeer:
    def __init__(self, ws):
        self.ws = ws
        self.box = None
        self.secure = False
        self.state = 1 # Mock PEER_STATE_CONNECTED
        self.roundTripTime = 15
        
    @property
    def address(self):
        # ws.remote_address contains (ip, port)
        if hasattr(self.ws, "remote_address") and self.ws.remote_address:
            return self.ws.remote_address
        return ("0.0.0.0", 0)

    def send(self, channel, packet):
        # Compatibility helper (optional)
        pass

class network:
    def __init__(self):
        self.host = None
        self.server_private_key = None
        self.secure_peers = {} # ws -> SecurePeer
        self.event_queue = queue.Queue()
        self.loop = None
        self.server_thread = None
        self.port = None

    def setup_server(self, port, maxchans, maxpeers):
        self.port = port
        
        # Load the asymmetric private key
        server_dir = os.path.dirname(os.path.abspath(__file__))
        key_path = os.path.join(server_dir, "server.private.key")
        try:
            with open(key_path, "r") as f:
                self.server_private_key = nacl.public.PrivateKey(f.read(), encoder=nacl.encoding.Base64Encoder)
        except FileNotFoundError:
            raise RuntimeError("Server private key (server.private.key) not found!")

        # Startup ready event — blocks setup_server() until the asyncio server is actually listening
        self._ready = threading.Event()

        # Spin up background event loop for websockets server
        self.loop = asyncio.new_event_loop()

        def run_async_server():
            asyncio.set_event_loop(self.loop)

            # websockets v12+ handler takes only one argument (websocket)
            async def ws_handler(websocket):
                # ── Critical latency fix ──────────────────────────────────────
                # Disable Nagle's Algorithm: forces OS to flush every packet
                # immediately instead of buffering small writes. This is what
                # eliminates the 40-80ms spikes caused by TCP coalescing.
                raw_sock = websocket.transport.get_extra_info("socket")
                if raw_sock:
                    raw_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    raw_sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                # ─────────────────────────────────────────────────────────────

                peer = SecurePeer(websocket)
                self.secure_peers[websocket] = peer

                try:
                    # Step 1: Handshake — client sends [channel_byte(30)] + [32-byte public key]
                    first_message = await websocket.recv()
                    # recv() returns bytes when client sends binary
                    if isinstance(first_message, str):
                        first_message = first_message.encode("utf-8")

                    if not first_message or len(first_message) < 2 or first_message[0] != HANDSHAKE_CHANNEL:
                        await websocket.close()
                        return

                    client_public_key_bytes = first_message[1:]
                    client_public_key = nacl.public.PublicKey(client_public_key_bytes)
                    peer.box = nacl.public.Box(self.server_private_key, client_public_key)
                    peer.secure = True

                    # Handshake OK response — must send as bytes
                    handshake_response = bytes([HANDSHAKE_CHANNEL]) + b"OK"
                    await websocket.send(handshake_response)

                    # Signal connection established to the main game loop
                    evt = network_event()
                    evt.type = event_connect
                    evt.peer_id = peer
                    self.event_queue.put(evt)

                    # Loop reading packets from this client
                    async for message in websocket:
                        if isinstance(message, str):
                            message = message.encode("utf-8")

                        if len(message) == 0:
                            continue

                        channel = message[0]
                        payload = message[1:]

                        if channel != 5 and channel != 6:
                            try:
                                decrypted_data = peer.box.decrypt(payload)
                            except Exception:
                                continue
                        else:
                            decrypted_data = payload

                        evt = network_event()
                        evt.type = event_receive
                        evt.peer_id = peer
                        evt.channel = channel

                        if channel != 5:
                            try:
                                evt.message = decrypted_data.decode("utf-8")
                            except UnicodeDecodeError:
                                evt.message = decrypted_data
                        else:
                            evt.message = decrypted_data

                        self.event_queue.put(evt)

                except Exception:
                    pass
                finally:
                    if websocket in self.secure_peers:
                        del self.secure_peers[websocket]

                    evt = network_event()
                    evt.type = event_disconnect
                    evt.peer_id = peer
                    self.event_queue.put(evt)

            async def main_async():
                # compression=None disables per-message WebSocket deflate compression.
                # Compression adds CPU overhead and unpredictable latency per frame —
                # unnecessary for a game server sending small binary payloads.
                async with websockets.serve(
                    ws_handler,
                    "0.0.0.0",
                    port,
                    compression=None,
                    ping_interval=20,    # Built-in WS keepalive every 20s
                    ping_timeout=10,     # Drop dead connections after 10s no-pong
                    max_size=2**20,      # 1 MB max message size
                ):
                    self._ready.set()  # Signal that the server is now actually listening
                    await asyncio.Future()  # run forever

            self.loop.run_until_complete(main_async())

        self.server_thread = threading.Thread(target=run_async_server, daemon=True, name="ws-server")
        self.server_thread.start()

        # Wait until the WebSocket server is actually bound and listening (up to 5 seconds)
        self._ready.wait(timeout=5)

        self.host = self  # For API checks
        return self

    def destroy(self):
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)
        self.host = None
        return True

    def is_active(self):
        return self.host is not None

    def get_peer_list(self):
        return list(self.secure_peers.values())

    def get_peer_count(self):
        return len(self.secure_peers)

    def get_total_received_data(self):
        return 0

    def get_total_received_packets(self):
        return 0

    def get_total_sent_data(self):
        return 0

    def get_total_sent_packets(self):
        return 0

    def request(self, timeout=0):
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
        # Returns host address IP string
        addr = peer.address
        return f"{addr[0]}:{addr[1]}"

    def get_peer_average_round_trip_time(self, peer):
        return peer.roundTripTime

    def disconnect_peer(self, peer):
        if peer and peer.ws:
            asyncio.run_coroutine_threadsafe(peer.ws.close(), self.loop)
        return True

    def disconnect_peer_softly(self, peer):
        return self.disconnect_peer(peer)

    def disconnect_peer_forcefully(self, peer):
        return self.disconnect_peer(peer)

    def _prepare_packet_data(self, message):
        if isinstance(message, str):
            return message.encode("utf-8")
        return message

    def send_reliable(self, peer, message, channel):
        if not peer or not peer.ws or peer.ws not in self.secure_peers:
            return False

        raw_message = self._prepare_packet_data(message)
        if channel != 5 and channel != 6:
            encrypted_message = peer.box.encrypt(raw_message)
        else:
            encrypted_message = raw_message

        packet = bytes([channel]) + encrypted_message
        try:
            # Safely schedule sending across threads
            asyncio.run_coroutine_threadsafe(peer.ws.send(packet), self.loop)
            return True
        except Exception as e:
            return False

    def send_unreliable(self, peer, message, channel):
        return self.send_reliable(peer, message, channel)

    def broadcast(self, message, channel):
        if message is None:
            return
        for peer in list(self.secure_peers.values()):
            self.send_reliable(peer, message, channel)

    def broadcast_unreliable(self, message, channel):
        self.broadcast(message, channel)

class network_event:
    def __init__(self):
        self.type = event_none
        self.peer_id = None
        self.message = ""
        self.channel = -1