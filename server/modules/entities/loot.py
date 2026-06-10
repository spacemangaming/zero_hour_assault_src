import globals as g
from timer import timer
from random import randint as random
from item import spawn_item
from file_directories import file_exists
import data_loader
class loot:
	def __init__(self,x,y,z,map,m):
		self.x=x
		self.m=m
		self.y=y
		self.z=z
		self.map=map
		self.timer=timer()
		for i in g.players:
			if i.dead: continue
			if(i.map==self.map or i.specmap==self.map):


				g.n.send_reliable(i.peer_id,"distsound loot"+str(random(1,2))+" "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" "+self.map,0)
def lootloop():
	for l in g.loots:
		if not file_exists("maps/"+l.map+".map"):
			g.loots.remove(l)
			return

		_loot_cfg = data_loader.get_loot_table()
		if l.timer.elapsed >= _loot_cfg.get("interval_ms", 10000):
			g.play("lootfinish",l.x,l.y,l.z,l.map)
			if 1:
				for _drop in _loot_cfg.get("drops", []):
					spawn_item(l.x, l.y, 0, l.map, _drop["item"], random(_drop["min"], _drop["max"]))
			l.m.send("Loot dropped at "+str(l.x)+", "+str(l.y)+", 0!",2)
			for n in g.npcs:
				if l.map==n.map and not n.inhouse:
					n.targetx=l.x
					n.targety=l.y
					n.targetz=l.z
					n.randomwalking=False; n.looting=True
			g.loots.remove(l)
def spawn_loot(x,y,z,map,m):
	g.loots.append(loot(x,y,z,map,m))