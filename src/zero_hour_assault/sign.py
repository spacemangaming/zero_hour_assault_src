from sound import *
import globals as g
from rotation import *
from speech import speak

from timer import timer

class sign:
	def __init__(self, sx, sy, sz, stext):
		self.x=sx
		self.y=sy
		self.z=sz
		self.text=stext
		self.beeptime=2000
		self.beeptimer=timer()
		self.readtime=2000
		self.readtimer=timer()
def signcheck():
	for i in range(len(g.signs)):
		if g.signs[i].x == round(g.mr.x) and g.signs[i].y == round(g.mr.y) and g.signs[i].z == round(g.me.z):
			if g.signs[i].readtimer.elapsed>g.signs[i].readtime:
				g.signs[i].readtimer.restart()
				g.p.play_stationary("beep4.ogg", False)
				g.n.send_reliable(0, "playonmap beep4", 0)
				speak(g.signs[i].text)
def spawn_sign(sx, sy, sz, stext):
	s=sign(sx, sy, sz, stext)
	g.signs.append(s)
def signloop():
	for i in range(len(g.signs)):
		if g.signs[i].beeptimer.elapsed>g.signs[i].beeptime and g.signbeepsound==1:
			if g.inthegame == True:
				g.signs[i].beeptimer.restart()
				g.p.play_3d("beep3.ogg", g.me.x, g.me.y, g.me.z, g.signs[i].x, g.signs[i].y, g.signs[i].z, calculate_theta(g.facing), False)