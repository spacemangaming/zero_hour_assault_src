import globals as g
from timer import timer
from random import randint as random
from file_directories import file_get_contents, file_put_contents
from moving_sound_serverside_handler import destroy_moving_sound, update_moving_sound
from pathfinder import pathfind
from rotation import get_3d_distance
from variable_management import string_replace
class zombie:
	def __init__(self, x, y, z, map, m):
		self.health=100
		self.damage=5
		self.name="zombie"
		self.path=None
		self.x=x
		self.y=y
		self.z=z
		self.m=m
		self.mode=random(1,2)
		self.msounds=[]
		self.msoundtimers=[]
		self.oldx=0
		self.oldy=0
		self.oldz=0
		self.map=map
		self.targetx=-1
		self.targety=-1
		self.targetz=-1
		self.targetplayer=None
		self.targethouse=""
		self.walktimer=timer()
		self.voicetimer=timer()
		self.attacktimer=timer()
		self.range=3
		self.housechecktimer=timer()
		self.housechecktimer2=timer()
		self.playerchecktimer=timer()
	def msoundloop(self):
		for i in range(len(self.msoundtimers)):
			if self.msoundtimers[i].elapsed>=15000:
				self.msoundtimers[i].restart()
				destroy_moving_sound(self.msounds[i])
				self.msoundtimers.remove(self.msoundtimers[i])
				self.msounds.remove(self.msounds[i])
				return
		if self.x!=self.oldx or self.y!=self.oldy or self.z!=self.oldz:
			for i in range(len(self.msounds)):
				update_moving_sound(self.msounds[i],self.x,self.y,self.z,self.map)
			self.oldx=self.x
			self.oldy=self.y
			self.oldz=self.z

def zombieloop():
	for z in g.zombies:
		z.msoundloop()
		m=None
		for ma in g.matches:
			if ma.owner==z.m: m=ma
		if m is None: z.health=0
		if z.health<=0:
			g.play("zombiedie",z.x,z.y,z.z,z.map)
			g.zombies.remove(z)
			return
		if z.targethouse=="red" and m.reddoorhealth<=0: z.targethouse=""
		if z.targethouse=="blue" and m.bluedoorhealth<=0: z.targethouse=""
		if z.housechecktimer.elapsed>0:
			z.housechecktimer.restart()
			if z.targethouse=="red" and m.reddoorhealth>0 and get_3d_distance(z.x,z.y,z.z,m.redhousex,m.redhousey,0)>25:
				z.targethouse=""
				z.targetx=-1
				z.targety=-1
				z.path=None
				z.targetplayer=None
			if z.targethouse=="blue" and m.bluedoorhealth>0 and get_3d_distance(z.x,z.y,z.z,m.bluehousex,m.bluehousey,0)>25:
				z.targethouse=""
				z.targetx=-1
				z.targety=-1
				z.path=None
				z.targetplayer=None
		if z.voicetimer.elapsed>=6500:
			z.voicetimer.restart()
			g.play("zombievoice"+str(random(1,5)),z.x,z.y,z.z,z.map)
		if z.housechecktimer2.elapsed>500 and z.targethouse=="":
			z.housechecktimer2.restart()
			if m.reddoorhealth>0 and get_3d_distance(z.x,z.y,z.z,m.redhousex,m.redhousey,0)<=25:
				z.targethouse="red"
				z.targetx=m.redhousex
				z.targety=m.redhousey
				z.path=pathfind(z.x, z.y, z.targetx, z.targety, z.map)
				z.targetplayer=None
			if m.bluedoorhealth>0 and get_3d_distance(z.x,z.y,z.z,m.bluehousex,m.bluehousey,0)<=25:
				z.targethouse="blue"
				z.targetx=m.bluehousex
				z.targety=m.bluehousey
				z.path=pathfind(z.x, z.y, z.targetx, z.targety, z.map)
				z.targetplayer=None
		if z.playerchecktimer.elapsed>0 and z.targethouse=="":
			z.playerchecktimer.restart()
			if z.mode==1: p=g.get_nearest_player(z.x,z.y,z.z,z.map)
			if z.mode==2: p=g.get_nearest_npc2(z.x,z.y,z.z,z.map)
			if p==-1 and z.mode==2:
				z.mode=1
				z.targetx=-1; z.targety=-1
				return
			if p==-1 and z.mode==1:
				z.mode=2
				z.targetx=-1; z.targety=-1
				return

			if p>-1:
				if z.mode==1: p=g.players[p]
				if z.mode==2: p=g.npcs[p]
				z.targetx=p.x
				z.targety=p.y
				z.targetz=p.z
				z.targetplayer=p.name
				#z.path=pathfind(z.x, z.y, z.targetx, z.targety, z.map)
		if z.walktimer.elapsed>=400 and z.targetx!=-1 and z.targety!=-1:
			z.walktimer.restart()
			if z.path is None or len(z.path)==0:
				if z.x<z.targetx: z.x+=1; g.play(g.get_tile_at(z.x,z.y,z.z,z.map)+"step"+str(random(1,5)),z.x,z.y,z.z,z.map,80)
				elif z.x>z.targetx: z.x-=1; g.play(g.get_tile_at(z.x,z.y,z.z,z.map)+"step"+str(random(1,5)),z.x,z.y,z.z,z.map,80)
				if z.y<z.targety: z.y+=1; g.play(g.get_tile_at(z.x,z.y,z.z,z.map)+"step"+str(random(1,5)),z.x,z.y,z.z,z.map,80)
				elif z.y>z.targety: z.y-=1; g.play(g.get_tile_at(z.x,z.y,z.z,z.map)+"step"+str(random(1,5)),z.x,z.y,z.z,z.map,80)
			else:
				next_x, next_y = z.path.pop()
				z.x=next_x
				z.y=next_y
				g.play(g.get_tile_at(z.x,z.y,z.z,z.map)+"step"+str(random(1,5)),z.x,z.y,z.z,z.map,80)
			if z.targetx!=-1 and z.targety!=-1 and z.attacktimer.elapsed>=800:
				z.attacktimer.restart()
				if z.targetplayer is not None:
					targetplayer=g.getpc(z.targetplayer)
					if targetplayer is not None:
						if get_3d_distance(z.x,z.y,z.z,targetplayer.x,targetplayer.y,targetplayer.z)<=z.range:
							targetplayer.play_hit_sound()
							targetplayer.health-=z.damage
							targetplayer.hitby="zombie"
							g.play("zombiehit",z.x,z.y,z.z,z.map)
				if m.reddoorhealth>0 and z.targethouse=="red" and get_3d_distance(z.x,z.y,z.z,m.redhousex,m.redhousey,0)<=z.range:
					m.reddoorhealth-=z.damage
					g.play("doorhit",z.x,z.y,z.z,z.map)
					g.n.broadcast("distsound doorhitdist "+str(z.x)+" "+str(z.y)+" "+str(z.z)+" "+z.map,0)
					if m.reddoorhealth<=0:
						g.play("doorbreak",z.x,z.y,z.z,z.map)
						for z2 in g.zombies:
							z2.damage+=5
							z2.range+=2
						matchmap=string_replace(file_get_contents("maps/zombie.map"),"mapname:zombie","mapname:zombie"+m.owner,False)

						matchmap+=f"""
platform:{m.redhousex-1}:{m.redhousex-1}:{m.redhousey+2}:{m.redhousey+20}:0:10:walldoor
platform:{m.redhousex}:{m.redhousex+19}:{m.redhousey+2}:{m.redhousey+19}:0:0:hardwood
platform:{m.redhousex+20}:{m.redhousex+20}:{m.redhousey}:{m.redhousey+20}:0:10:walldoor
platform:{m.redhousex}:{m.redhousex+20}:{m.redhousey+20}:{m.redhousey+20}:0:10:walldoor
door:{m.bluehousex}:{m.bluehousey}:0:{m.bluehousex}:{m.bluehousey+2}:0:5000:houseenter.ogg:houseexit.ogg
door:{m.bluehousex}:{m.bluehousey+2}:0:{m.bluehousex}:{m.bluehousey}:0:5000:houseenter.ogg:houseexit.ogg
platform:{m.bluehousex-1}:{m.bluehousex-1}:{m.bluehousey+2}:{m.bluehousey+20}:0:10:walldoor
platform:{m.bluehousex}:{m.bluehousex+20}:{m.bluehousey+1}:{m.bluehousey+1}:0:10:walldoor
platform:{m.bluehousex}:{m.bluehousex+19}:{m.bluehousey+2}:{m.bluehousey+19}:0:0:hardwood

platform:{m.bluehousex+20}:{m.bluehousex+20}:{m.bluehousey}:{m.bluehousey+20}:0:10:walldoor
platform:{m.bluehousex}:{m.bluehousex+20}:{m.bluehousey+20}:{m.bluehousey+20}:0:10:walldoor
"""
						file_put_contents("maps/zombie"+m.owner+".map",matchmap)
						m.redhousex=-50
						m.redhousey=-50

						for p in m.players:
							if g.get_player_index_from(p)>-1: g.move_player(g.get_player_index_from(p),g.players[g.get_player_index_from(p)].x,g.players[g.get_player_index_from(p)].y,g.players[g.get_player_index_from(p)].z,g.players[g.get_player_index_from(p)].map)
						for p in m.spectators:
							try: g.n.send_reliable(g.players[g.get_player_index_from(p)].peer_id,"mapdata "+file_get_contents("maps/"+m.get_cwmap()+".map"),0)
							except: pass
						z.targethouse=""
						z.targetx=-1
						z.targety=-1
				if m.bluedoorhealth>0 and z.targethouse=="blue" and get_3d_distance(z.x,z.y,z.z,m.bluehousex,m.bluehousey,0)<=z.range:
					m.bluedoorhealth-=z.damage
					g.play("doorhit",z.x,z.y,z.z,z.map)
					g.n.broadcast("distsound doorhitdist "+str(z.x)+" "+str(z.y)+" "+str(z.z)+" "+z.map,0)
					if m.bluedoorhealth<=0:
						g.play("doorbreak",z.x,z.y,z.z,z.map)

						for z2 in g.zombies:
							z2.damage+=5
							z2.range+=2
						matchmap=string_replace(file_get_contents("maps/zombie.map"),"mapname:zombie","mapname:zombie"+m.owner,False)
						matchmap+=f"""
platform:{m.bluehousex-1}:{m.bluehousex-1}:{m.bluehousey+2}:{m.bluehousey+20}:0:10:walldoor
platform:{m.bluehousex}:{m.bluehousex+19}:{m.bluehousey+2}:{m.bluehousey+19}:0:0:hardwood
platform:{m.bluehousex+20}:{m.bluehousex+20}:{m.bluehousey}:{m.bluehousey+20}:0:10:walldoor
platform:{m.bluehousex}:{m.bluehousex+20}:{m.bluehousey+20}:{m.bluehousey+20}:0:10:walldoor
door:{m.redhousex}:{m.redhousey}:0:{m.redhousex}:{m.redhousey+2}:0:5000:houseenter.ogg:houseexit.ogg
door:{m.redhousex}:{m.redhousey+2}:0:{m.redhousex}:{m.redhousey}:0:5000:houseenter.ogg:houseexit.ogg
platform:{m.redhousex-1}:{m.redhousex-1}:{m.redhousey+2}:{m.redhousey+20}:0:10:walldoor
platform:{m.redhousex}:{m.redhousex+20}:{m.redhousey+1}:{m.redhousey+1}:0:10:walldoor
platform:{m.redhousex}:{m.redhousex+19}:{m.redhousey+2}:{m.redhousey+19}:0:0:hardwood
platform:{m.redhousex+20}:{m.redhousex+20}:{m.redhousey}:{m.redhousey+20}:0:10:walldoor
platform:{m.redhousex}:{m.redhousex+20}:{m.redhousey+20}:{m.redhousey+20}:0:10:walldoor
"""
						file_put_contents("maps/zombie"+m.owner+".map",matchmap)
						m.bluehousex=-50
						m.bluehousey=-50

						for p in m.players:
							if g.get_player_index_from(p)>-1: g.move_player(g.get_player_index_from(p),g.players[g.get_player_index_from(p)].x,g.players[g.get_player_index_from(p)].y,g.players[g.get_player_index_from(p)].z,g.players[g.get_player_index_from(p)].map)
						for p in m.spectators:
							try: g.n.send_reliable(g.players[g.get_player_index_from(p)].peer_id,"mapdata "+file_get_contents("maps/"+m.get_cwmap()+".map"),0)
							except: pass
						z.targethouse=""
						z.targetx=-1
						z.targety=-1
def spawn_zombie(x,y,z,map,m):
	g.zombies.append(zombie(x,y,z,map,m))