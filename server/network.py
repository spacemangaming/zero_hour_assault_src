import enet,traceback
import nacl.utils
import nacl.public
import nacl.encoding
import weakref

event_none = 0
event_connect = enet.EVENT_TYPE_CONNECT
event_disconnect = enet.EVENT_TYPE_DISCONNECT
event_receive = enet.EVENT_TYPE_RECEIVE

HANDSHAKE_CHANNEL = 30

class SecurePeer:
    def __init__(self, peer):
        self.enet_peer = peer
        self.box = None
        self.secure = False

class network:
    def __init__(self):
        self.host = None
        self.peer = None
        self.server_private_key = None
        self.secure_peers = {}

    def setup_server(self, port, maxchans, maxpeers):
        self.host = enet.Host(enet.Address(b"0.0.0.0", port), maxchans, maxpeers, 0, 0)
        import os
        server_dir = os.path.dirname(os.path.abspath(__file__))
        key_path = os.path.join(server_dir, "server.private.key")
        try:
            with open(key_path, "r") as f:
                self.server_private_key = nacl.public.PrivateKey(f.read(), encoder=nacl.encoding.Base64Encoder)
        except FileNotFoundError:
            raise RuntimeError("Server private key (server.private.key) not found!")
        return self.host

    def destroy(self):
        if self.host is None:
            return False
        self.host.flush()
        del self.host
        self.host = None
        return self.host is None

    def _prepare_packet_data(self, message):
        if isinstance(message, str):
            return message.encode("utf-8")
        return message

    def broadcast(self, message, channel):
        if message is None:
            return

        raw_message = self._prepare_packet_data(message)
        for peer in self.host.peers:
            if peer.state == enet.PEER_STATE_CONNECTED and peer in self.secure_peers and self.secure_peers[peer].secure:
                secure_peer_info = self.secure_peers[peer]
                encrypted_message = secure_peer_info.box.encrypt(raw_message)
                packet = enet.Packet(encrypted_message, enet.PACKET_FLAG_RELIABLE)
                peer.send(channel, packet)
    
    def broadcast_unreliable(self, message, channel):
        if message is None:
            return

        raw_message = self._prepare_packet_data(message)
        for peer in self.host.peers:
            if peer.state == enet.PEER_STATE_CONNECTED and peer in self.secure_peers and self.secure_peers[peer].secure:
                secure_peer_info = self.secure_peers[peer]
                encrypted_message = secure_peer_info.box.encrypt(raw_message)
                packet = enet.Packet(encrypted_message, 0)
                peer.send(channel, packet)

    def is_active(self):
        return self.host is not None

    def setup_client(self, maxchans, maxpeers):
        self.host = enet.Host(None, maxchans, maxpeers, 0, 0)
        return self.host

    def connect(self, address, port):
        if isinstance(address, str):
            raw_address = address.encode("utf-8")
        else:
            raw_address = address
        self.peer = self.host.connect(enet.Address(raw_address, port), self.host.channelLimit)
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
            peer = event.peer
            ret.peer_id = peer

            if event.type == event_connect:
                self.secure_peers[peer] = SecurePeer(peer)
                timeout = 0
                continue

            elif event.type == event_disconnect:
                ret.type = event_disconnect
                return ret

            elif event.type == event_receive:
                if 1:
                    secure_peer_info = self.secure_peers[peer]
                    
                    if event.channelID == HANDSHAKE_CHANNEL:
                        if not secure_peer_info.secure:
                            try:
                                client_public_key = nacl.public.PublicKey(event.packet.data)
                                secure_peer_info.box = nacl.public.Box(self.server_private_key, client_public_key)
                                secure_peer_info.secure = True
                                response_packet = enet.Packet(b"OK", enet.PACKET_FLAG_RELIABLE)
                                peer.send(HANDSHAKE_CHANNEL, response_packet)
                                ret.type = event_connect

                                return ret

                            except:
                                traceback.print_exc(); peer.disconnect()
                        
                        timeout = 0
                        continue

                    elif secure_peer_info.secure:
                        try:
                            if event.channelID!=5 and event.channelID!=6: decrypted_data = secure_peer_info.box.decrypt(event.packet.data)
                            else: decrypted_data = event.packet.data
                            ret.type = event_receive
                            if event.channelID != 5:
                                try: ret.message = decrypted_data.decode("utf-8")
                                except UnicodeDecodeError: ret.message = decrypted_data
                            else:
                                ret.message = decrypted_data
                            ret.channel = event.channelID
                            return ret
                        except nacl.exceptions.CryptoError:
                            pass
                
                timeout = 0
                continue
            
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

    def send_reliable(self, peer, message, channel):
        if peer not in self.secure_peers or not self.secure_peers[peer].secure:
            return False

        secure_peer_info = self.secure_peers[peer]
        raw_message = self._prepare_packet_data(message)
        if channel!=5 and channel!=6: encrypted_message = secure_peer_info.box.encrypt(raw_message)
        else: encrypted_message=raw_message
        packet = enet.Packet(encrypted_message, enet.PACKET_FLAG_RELIABLE)
        try: return peer.send(channel, packet)
        except: return False

    def send_unreliable(self, peer, message, channel):
        if peer not in self.secure_peers or not self.secure_peers[peer].secure:
            return False

        secure_peer_info = self.secure_peers[peer]
        raw_message = self._prepare_packet_data(message)

        if channel!=5 and channel!=6: encrypted_message = secure_peer_info.box.encrypt(raw_message)
        else: encrypted_message=raw_message

        packet = enet.Packet(encrypted_message, enet.PACKET_FLAG_UNSEQUENCED)
        try: return peer.send(channel, packet)
        except: return False

class network_event:
    def __init__(self):
        self.type = event_none
        self.peer_id = None
        self.message = ""
        self.channel = -1