import globals as g
from timer import timer
from random import randint as random
from item import spawn_item
from file_directories import file_exists
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

		if l.timer.elapsed>=10000:
			g.play("lootfinish",l.x,l.y,l.z,l.map)
			if 1:
				spawn_item(l.x,l.y,0,l.map,"9mm",random(25,45))
				spawn_item(l.x,l.y,0,l.map,"small_potion",random(1,5))
				spawn_item(l.x,l.y,0,l.map,"vitality_potion",random(1,3))
				spawn_item(l.x,l.y,0,l.map,"revival_nectar",random(1,2))

				spawn_item(l.x,l.y,0,l.map,"colt1911",random(1,1))
				spawn_item(l.x,l.y,0,l.map,"45_ACP",random(10,30))
				spawn_item(l.x,l.y,0,l.map,"fnhfnp40",random(1,1))
				spawn_item(l.x,l.y,0,l.map,"fnhfnp45",random(1,1))

				spawn_item(l.x,l.y,0,l.map,"40S&W",random(20,50))

				spawn_item(l.x,l.y,0,l.map,"mkek_jng90",random(1,1))
				spawn_item(l.x,l.y,0,l.map,"7.62x51mm",random(10,20))
				spawn_item(l.x,l.y,0,l.map,"mkek_mpt76k",random(1,1))
				spawn_item(l.x,l.y,0,l.map,"5.56x45mm",random(20,30))
				spawn_item(l.x,l.y,0,l.map,"IthicaM37",random(1,1))
				spawn_item(l.x,l.y,0,l.map,"12_gauge",random(1,10))
				spawn_item(l.x,l.y,0,l.map,"7.62x54mmR",random(10,15))

				spawn_item(l.x,l.y,0,l.map,"molotov_cocktail",random(1,10))
				spawn_item(l.x,l.y,0,l.map,"tm62",random(1,10))
				spawn_item(l.x,l.y,0,l.map,"timebomb",random(1,10))
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