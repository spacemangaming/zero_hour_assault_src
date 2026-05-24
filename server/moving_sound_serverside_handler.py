import globals as g
from random import randint as random
class msound:
	id=""
	soundloop=""
	map=""
	owner=""
	x=0
	y=0
	z=0
	pitch=0
	def __init__(self, i, l, c1, c2, c3, cm, own="", p=100):
		self.id=i
		self.playmoving=False
		self.soundloop=l
		self.x=c1
		self.y=c2
		self.z=c3
		self.map=cm
		self.owner=own
		self.pitch=p
	def updateme(self, c1, c2, c3, p=-1):
		self.x=c1
		self.y=c2
		self.z=c3
		if p!=-1:
			self.pitch=p
def spawn_moving_sound(loop, x, y, z, map, owner="", pitch=100,sendowner=True,playmoving=False):
	id=""
	breakit=False
	while True:
		id=randomstring()
		breakit=True
		for i in range(len(g.msounds)):
			if g.msounds[i].id==id:
				breakit=False
		if breakit:
			break
	m1=msound(id, loop, x, y, z, map, owner, pitch)
	m1.playmoving=playmoving
	g.msounds.append(m1)
	owner_player=g.getpc(owner) if owner!="" else None
	owner_hidden = owner_player is not None and owner_player.hidden
	if owner=="":
		for i in range(len(g.players)):
			if g.players[i].specmap==map or g.players[i].map==map:
				g.n.send_reliable(g.players[i].peer_id, "createmsound "+id+" "+loop+" "+str(x)+" "+str(y)+" "+str(z)+" "+map+" "+str(pitch), 0)
	else:
		for i in range(len(g.players)):
			if g.players[i].name!=owner:
				if owner_hidden: continue
				if g.players[i].specmap==map or g.players[i].map==map: g.n.send_reliable(g.players[i].peer_id, "createmsound "+id+" "+loop+" "+str(x)+" "+str(y)+" "+str(z)+" "+map+" "+str(pitch), 0)
			else:
				try:
					if loop.startswith("zombievoice"):
						g.n.send_reliable(g.players[i].peer_id,"play_s2 "+loop,0)
					else:
						if sendowner: g.n.send_reliable(g.players[i].peer_id,"play_s "+loop,0)
				except: pass
	return id
def update_moving_sound(id, x, y, z, pitch=-1):
	x=round(x)
	y=round(y)
	z=round(z)
	if isinstance(pitch,str): pitch=100
	for i in range(len(g.msounds)):
		if g.msounds[i].id==id:
			g.msounds[i].updateme(x, y, z, pitch)
			if g.msounds[i].owner=="":
				for j in range(len(g.players)):
					if g.players[j].specmap==g.msounds[i].map or g.players[j].map==g.msounds[i].map:
						g.n.send_unreliable(g.players[j].peer_id, "updatemsound "+id+" "+str(x)+" "+str(y)+" "+str(z)+" "+str(g.msounds[i].pitch), 0)
			else:
				owner_player=g.getpc(g.msounds[i].owner)
				if owner_player is not None and owner_player.hidden: continue
				for j in range(len(g.players)):
					if g.players[j].name!=g.msounds[i].owner:
						if g.players[j].specmap==g.msounds[i].map or g.players[j].map==g.msounds[i].map: g.n.send_unreliable(g.players[j].peer_id, "updatemsound "+id+" "+str(x)+" "+str(y)+" "+str(z)+" "+str(g.msounds[i].pitch), 0)
def destroy_moving_sound(id):
	for i in range(len(g.msounds)):
		if g.msounds[i].id==id:
			owner_player=g.getpc(g.msounds[i].owner) if g.msounds[i].owner!="" else None
			owner_hidden = owner_player is not None and owner_player.hidden
			for pl in g.players:
				if owner_hidden: break
				if pl.specmap==g.msounds[i].map or pl.map==g.msounds[i].map: g.n.send_reliable(pl.peer_id,"destroymsound "+id, 0)
			g.msounds.remove(g.msounds[i])
			break
def randomstring(length=10):
	temp="abcdefghijklmnopqrstuvwxyz1234567890"
	ret=""
	for i in range(length):
		ret=ret+temp[random(0, (len(temp)-1))]
	return ret
