from cytolk import tolk
tolk.load()
print("enet ping atıcı")
print("Bu program, enet kütüphanesini kullanan oyunlara ping atmanızı sağlar")
print("Sunucunun, ping paketine pong cevabı vermesi gerekir")
import enet,time
host = enet.Host(None, 20, 500, 0, 0)


class timer:
    """A timer class, to track time mesured in millis"""

    def __init__(self):
        self.inittime = time.time()
        self.paused = 0

    @property
    def elapsed(self):
        """Returns the exact elapsed time since this timer was created or last restarted."""
        if self.paused != 0:
            return self.paused
        else:
            return self._ms(time.time() - self.inittime)

    def force(self, amount):
        """Forces the timer to a specific time.

        Args:
                amount (int): The time elapsed (in millis)
        """
        if self.paused == 0:
            self.inittime = time.time() - (amount / 1000)
        else:
            self.paused = amount

    def restart(self):
        """Restarts the timer, and set it's elapsed time to 0."""
        self.__init__()

    def pause(self):
        """Pauses the timer at a certain position."""
        self.paused = self._ms(time.time() - self.inittime)

    def resume(self):
        """Resumes the timer after being paused."""
        self.inittime = time.time() - (self.paused / 1000)
        self.paused = 0

    def _ms(self, t):
        return int(t * 1000)

while True:
	sunucu=input("ping atılacak oyun ip adresi ya da domain girin")
	if sunucu=="": print("sunucu boş olamaz"); continue
	port=input("portu girin")
	try: port=int(port)
	except: print("yanlış port"); continue
	print("bağlanıyor")
	host.connect(enet.Address(sunucu.encode(), port), host.channelLimit)
	while True:
		time.sleep(0.001)
		baglandi=False
		olay=host.service(0)
		if olay.type==enet.EVENT_TYPE_DISCONNECT: print("bağlantı başarısız"); break
		if olay.type==enet.EVENT_TYPE_CONNECT: print("bağlantı başarılı, şimdi ping atılacak!"); baglandi=True
		if not baglandi: continue
		print("ping atılıyor... Ctrl c ile durdurabilirsiniz.")
		while True:
			time.sleep(0.001)
			paket = enet.Packet("ping".encode("utf-8"), enet.PACKET_FLAG_RELIABLE)
			host.broadcast(0, paket)
			pingtimer=timer()
			while True:
				time.sleep(0.001)
				olay=host.service(0)
				if olay.type==enet.EVENT_TYPE_RECEIVE and olay.packet.data==b"pong":
					tolk.speak(str(pingtimer.elapsed),True)
					break