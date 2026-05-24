from rotation import get_3d_distance
from vector import vector
from timer import timer
import globals as g
from random import randint as random
class molotof:
	def __init__(self,x,y,z,map,owner):
		self.x=x
		self.y=y
		self.z=z
		self.map=map
		self.owner=owner
		self.soundtimer=timer()
		self.soundtimer.restart()
		g.play2("molotofburnstart",self.x-15,self.x+15,self.y-15,self.y+15,self.z,self.z+15,self.map)

		g.play2("molotofburning",self.x-15,self.x+15,self.y-15,self.y+15,self.z,self.z+15,self.map)

		self.endburntimer=timer()
		self.endburntime=30000
		self.hittimer=timer()
		self.hittime=random(1000,2000)
		self.dammage=random(10,20)
	def player_is_in_bounds(self, player):
		in_x = (player.x >= self.x - 15) and (player.x <= self.x + 15)

		in_y = (player.y >= self.y - 15) and (player.y <= self.y + 15)

		in_z = (player.z >= self.z) and (player.z <= self.z + 15)

		return in_x and in_y and in_z
def molotofloop():
	for m in g.molotofs:
		if g.rain and m in g.molotofs: g.molotofs.remove(m); return
		if m.hittimer.elapsed>=m.hittime:
			m.hittimer.restart()
			for p in g.players:
				if p.hidden: continue
				if m.player_is_in_bounds(p) and m.map==p.map:
					p.health-=m.dammage
					p.play_hit_sound()
			for p in g.bikes:
				if m.player_is_in_bounds(p) and m.map==p.map:
					for pl2 in p.players:
						try: p.remove_platform_to(g.getpc(pl2))
						except: pass
					p.remove_all_players()
					g.bikes.remove(p)
			for p in g.timebombs:
				if m.player_is_in_bounds(p) and m.map==p.map:
					g.timebombs.remove(p)
			for p in g.items:
				if m.player_is_in_bounds(p) and m.map==p.map:
					g.items.remove(p)

			for p in g.chests:
				if "base" not in p.map and m.player_is_in_bounds(p) and m.map==p.map:
					g.chests.remove(p)

			for p in g.motors:
				if m.player_is_in_bounds(p) and m.map==p.map:
					g.motors.remove(p)


			for p in g.corpses:
				if m.player_is_in_bounds(p) and m.map==p.map:
					g.corpses.remove(p)


		if m.endburntimer.elapsed>=m.endburntime:
			m.endburntimer.restart()
			g.n.broadcast("destroymolotofburning",0)
			g.molotofs.remove(m)
			return
		if m.soundtimer.elapsed>=7500:
			m.soundtimer.restart()
			g.play2("molotofburning",m.x-15,m.x+15,m.y-15,m.y+15,m.z,m.z+15,m.map)


def spawn_molotof(x,y,z,map,owner):
	if map=="lobby": return
	ml=molotof(x,y,z,map,owner)
	g.molotofs.append(ml)
