import enet
import nacl.utils
import nacl.public
import nacl.encoding

event_none = 0
event_connect = enet.EVENT_TYPE_CONNECT
event_disconnect = enet.EVENT_TYPE_DISCONNECT
event_receive = enet.EVENT_TYPE_RECEIVE

SERVER_PUBLIC_KEY_B64 = "svNwUAv3H3FdcaFeqZi/ZgbEWg4Y4e5qsP1yyS3/Llo="
HANDSHAKE_CHANNEL = 30

class SecurePeer:
    def __init__(self, peer):
        self.enet_peer = peer
        self.box = None
        self.secure = False
        self.handshake_complete = False

class network:
    def __init__(self):
        self.host = None
        self.peer = None
        self.secure_peer = None
        self.client_private_key = None

    def setup_server(self, port, maxchans, maxpeers):
        self.host = enet.Host(enet.Address(b"0.0.0.0", port), maxchans, maxpeers, 0, 0)
        return self.host

    def destroy(self):
        if self.host is None:
            return False
        self.host.flush()
        del self.host
        self.host = None
        return self.host is None

    def broadcast(self, message, channel):
        if not self.secure_peer or not self.secure_peer.secure:
            return
        
        if isinstance(message, str):
            raw_message = message.encode("utf-8")
        else:
            raw_message = message
            
        encrypted_message = self.secure_peer.box.encrypt(raw_message)
        packet = enet.Packet(encrypted_message, enet.PACKET_FLAG_RELIABLE)
        self.host.broadcast(channel, packet)

    def is_active(self):
        return self.host is not None

    def setup_client(self, maxchans, maxpeers):
        self.host = enet.Host(None, maxchans, maxpeers, 0, 0)
        self.client_private_key = nacl.public.PrivateKey.generate()
        return self.host

    def connect(self, address, port):
        if isinstance(address, str):
            raw_address = address.encode("utf-8")
        else:
            raw_address = address
            
        enet_peer = self.host.connect(enet.Address(raw_address, port), self.host.channelLimit)
        if not enet_peer:
            return None
        self.peer = enet_peer
        self.secure_peer = SecurePeer(enet_peer)
        return self.peer

    def get_peer_list(self):
        return self.host.peers

    def get_peer_count(self):
        try:
            return self.host.peerCount
        except:
            return -1

    def get_total_received_data(self):
        return self.host.totalReceivedData

    def get_total_received_packets(self):
        return self.host.totalReceivedPackets

    def get_total_sent_data(self):
        return self.host.totalSentData

    def get_total_sent_packets(self):
        return self.host.totalSentPackets

    def request(self, timeout=0):
        while True:
            event = self.host.service(timeout)
            ret = network_event()
            ret.peer_id = event.peer

            if self.secure_peer and self.secure_peer.handshake_complete:
                ret.type = event.type
                if event.type == event_receive:
                    try:
                        if event.channelID!=5 and event.channelID!=6: decrypted_data = self.secure_peer.box.decrypt(event.packet.data)
                        else: decrypted_data=event.packet.data
                        if event.channelID != 5:
                            try: ret.message = decrypted_data.decode("utf-8")
                            except UnicodeDecodeError: ret.message = decrypted_data
                        else:
                            ret.message = decrypted_data
                        ret.channel = event.channelID
                        return ret
                    except nacl.exceptions.CryptoError:
                        timeout = 0
                        continue
                return ret

            if event.type == event_connect:
                client_public_key_bytes = self.client_private_key.public_key.encode()
                packet = enet.Packet(client_public_key_bytes, enet.PACKET_FLAG_RELIABLE)
                event.peer.send(HANDSHAKE_CHANNEL, packet)
                timeout = 0
                continue

            elif event.type == event_receive and event.channelID == HANDSHAKE_CHANNEL:
                try:
                    server_public_key = nacl.public.PublicKey(SERVER_PUBLIC_KEY_B64, encoder=nacl.encoding.Base64Encoder)
                    self.secure_peer.box = nacl.public.Box(self.client_private_key, server_public_key)
                    self.secure_peer.secure = True
                    self.secure_peer.handshake_complete = True
                    ret.type = event_connect
                    ret.peer = event.peer
                    return ret
                except:
                    timeout=0
                    continue
                
            elif event.type == event_disconnect:
                ret.type = event_disconnect
                return ret

            ret.type = event_none
            return ret
            
    def get_peer_address(self, peer):
        return peer.address

    def get_peer_average_round_trip_time(self, peer):
        return peer.roundTripTime

    def disconnect_peer(self, peer):
        try:
            return peer.disconnect()
        except:
            return False

    def disconnect_peer_softly(self, peer):
        try:
            return peer.disconnect_later()
        except:
            return False

    def disconnect_peer_forcefully(self, peer):
        try:
            return peer.disconnect_now()
        except:
            return False

    def _prepare_packet_data(self, message):
        if isinstance(message, str):
            return message.encode("utf-8")
        return message

    def send_reliable(self, peer, message, channel):
        if not self.secure_peer or not self.secure_peer.secure:
            return

        raw_message = self._prepare_packet_data(message)
        if channel!=5 and channel!=6: encrypted_message = self.secure_peer.box.encrypt(raw_message)
        else: encrypted_message=raw_message

        packet = enet.Packet(encrypted_message, enet.PACKET_FLAG_RELIABLE)
        p = self.peer if self.peer is not None else peer
        if p:
            return p.send(channel, packet)

    def send_unreliable(self, peer, message, channel):
        if not self.secure_peer or not self.secure_peer.secure:
            return

        raw_message = self._prepare_packet_data(message)
        if channel!=5 and channel!=6: encrypted_message = self.secure_peer.box.encrypt(raw_message)
        else: encrypted_message=raw_message


        if channel != 5:
            packet = enet.Packet(encrypted_message, enet.PACKET_FLAG_UNSEQUENCED)
        else:
            packet = enet.Packet(encrypted_message, enet.PACKET_FLAG_RELIABLE)

        p = self.peer if self.peer is not None else peer
        if p:
            return p.send(channel, packet)

class network_event:
    def __init__(self):
        self.type = event_none
        self.peer_id = None
        self.message = ""
        self.channel = -1