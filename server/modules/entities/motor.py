import globals as g
from timer import timer
from random import randint as random
from vector import vector
from rotation import get_3d_distance
from rotation import move
from moving_sound_serverside_handler import update_moving_sound, destroy_moving_sound
from file_directories import file_exists
from map import get_tile_at, get_staircase_at
from rotation import getdir, north, northeast, east, southeast, south, southwest, west, northwest
class motor:
	def __init__(self, vx, vy, vz, vmap, vhealth, vmaxspeed, vmaxplayers, vbreaktime, vowner):
		self.players=my_list()
		self.wind_volume=0
		self.owner=vowner
		self.running=False
		self.matchteam=""
		self.speed=0
		self.x=0
		self.y=0
		self.z=0
		self.map=""
		self.crashed=False
		self.crashedto=None
		self.breaktimer=timer()
		self.filechecktimer=timer()
		self.breaktime=700
		self.mid=0
		self.hitby="no one"
		self.health=0
		self.maxspeed=0
		self.maxpitch=0
		self.speedtimer=timer()
		self.walltimer=timer()
		self.slowdowntimer=timer()
		self.maxplayers=0
		self.pitch=100
		self.x=vx
		self.y=vy
		self.z=vz
		self.map=vmap
		self.health=vhealth
		self.maxspeed=vmaxspeed
		self.maxplayers=vmaxplayers
		self.maxpitch=300
		self.breaktime=vbreaktime
		self.facing=0
	def windvolume(self, volume):
		if self.wind_volume!=volume:
			self.wind_volume=volume
			for p in self.players:
				pl=g.getpc(p)
				if pl is not None: g.n.send_reliable(pl.peer_id,"motorvolume "+str(volume),0)
def motorloop():
	for i in range(len(g.motors)):
		for p in range(len(g.motors[i].players)):
			try: index=g.get_player_index_from(g.motors[i].players[p])
			except: index=-1
			if index==-1 or (index>-1 and g.players[index].map!=g.motors[i].map):
				try: g.motors[i].players.remove(g.motors[i].players[p])
				except: pass
				if index>-1:
					g.n.send_reliable(g.players[index].peer_id,"motorunspawn",0)
					g.players[index].vi=-1
					g.players[index].inve=False
			if index>-1 and p==0: g.motors[i].facing=g.players[index].facing
			if index>-1: g.motors[i].matchteam=g.players[index].matchteam
		if g.motors[i].matchteam=="": g.motors[i].matchteam="unknown"

		if g.motors[i].filechecktimer.elapsed>1000:
			g.motors[i].filechecktimer.restart()
			if not file_exists("maps/"+g.motors[i].map+".map"):
				if g.motors[i].running: destroy_moving_sound(g.motors[i].mid)
				for p in range(len(g.players)):
					pv=g.motors[i].players.find(g.players[p].name)
					if pv>-1:
						g.players[p].inve=False
						g.n.send_reliable(g.players[p].peer_id, "motorunspawn", 0)
						g.players[p].vi=-1
				for pl in g.players:
					if pl.map==g.motors[i].map: remove_platform(pl, g.motors[i].x, g.motors[i].x, g.motors[i].y, g.motors[i].y, g.motors[i].z, g.motors[i].z+4, "wallspaceship")
					if pl.map==g.motors[i].map: remove_platform(pl, g.motors[i].x, g.motors[i].x, g.motors[i].y, g.motors[i].y, g.motors[i].z+5, g.motors[i].z+5, "cloth")

				g.motors.remove(g.motors[i])
				return
		if g.motors[i].health<=0:
			if 1==1:
				for p in range(len(g.players)):
					pv=g.motors[i].players.find(g.players[p].name)
					if pv>-1:
						g.players[p].inve=False
						g.players[p].z+=10
						if get_tile_at(g.players[p].x,g.players[p].y,g.players[p].z,g.players[p].map).startswith("wall"): g.players[p].z-=1
						g.n.send_reliable(g.players[p].peer_id,"motorvolume -100",0)
						g.n.send_reliable(g.players[p].peer_id,"move "+str(g.players[p].x)+" "+str(g.players[p].y)+" "+str(g.players[p].z),0)

						g.n.send_reliable(g.players[p].peer_id, "motorunspawn", 0)
						g.players[p].vi=-1
						g.motors[i].players.remove(g.players[p].name)
			if g.motors[i].running==True:
				g.motors[i].running=False
				destroy_moving_sound(g.motors[i].mid)
			g.play("motorexplode", g.motors[i].x, g.motors[i].y, g.motors[i].z, g.motors[i].map)
			g.n.broadcast("distsound motorexplodedist "+str(g.motors[i].x)+" "+str(g.motors[i].y)+" "+str(g.motors[i].z)+" "+g.motors[i].map, 0)
			for pl in g.players:
				if pl.map==g.motors[i].map: remove_platform(pl, g.motors[i].x, g.motors[i].x, g.motors[i].y, g.motors[i].y, g.motors[i].z, g.motors[i].z+4, "wallspaceship")
				if pl.map==g.motors[i].map: remove_platform(pl, g.motors[i].x, g.motors[i].x, g.motors[i].y, g.motors[i].y, g.motors[i].z+5, g.motors[i].z+5, "cloth")

			g.n.broadcast("motor of "+g.motors[i].owner+" destroyed by "+g.motors[i].hitby,2)
			for p in g.players:
				if p.name==g.motors[i].owner: p.motorhistory+="your motor destroyed by "+g.motors[i].hitby+" at "+g.get_current_date()+"\n"
			g.motors.remove(g.motors[i])
			return
		if g.motors[i].walltimer.elapsed>=500 and g.motors[i].speed!=0 and g.motors[i].running==True and g.motors[i].pitch>100:
			g.motors[i].walltimer.restart()
			coords=vector(g.motors[i].x,g.motors[i].y,g.motors[i].z)
			max=get_max_values(g.motors[i].map)
			for counter in range(50):
				coords=move(coords.x, coords.y, coords.z, g.motors[i].facing, 0, 0, 0)
				if coords.x>max.x:
					coords.x=max.x
				if coords.x<0:
					coords.x=0
				if coords.y>max.y:
					coords.y=max.y
				if coords.y<0:
					coords.y=0
				if coords.z>max.z:
					coords.z=max.z
				tile=get_tile_at(coords.x, coords.y, coords.z, g.motors[i].map)
				if tile!="wallspaceship" and tile.startswith("wall"):
					g.play("misc55",g.motors[i].x,g.motors[i].y,g.motors[i].z,g.motors[i].map)
					break
				if tile=="":
					g.play("misc55",g.motors[i].x,g.motors[i].y,g.motors[i].z,g.motors[i].map)
					break


		if g.motors[i].speedtimer.elapsed>g.motors[i].speed and g.motors[i].speed!=0 and g.motors[i].running==True and g.motors[i].pitch>100:
			g.motors[i].speedtimer.restart()
			max=get_max_values(g.motors[i].map)
			coords=move(g.motors[i].x, g.motors[i].y, g.motors[i].z, g.motors[i].facing, 0, 0, 0)
			if coords.x>max.x:
				coords.x=max.x
			if coords.x<0:
				coords.x=0
			if coords.y>max.y:
				coords.y=max.y
			if coords.y<0:
				coords.y=0
			if coords.z>max.z:
				coords.z=max.z
			if get_staircase_at(coords.x, coords.y, coords.z, g.motors[i].map)=="x":
				if coords.x>g.motors[i].x and get_tile_at(coords.x,coords.y,coords.z+1,g.motors[i].map)!="": coords.z+=1
				if coords.x<g.motors[i].x and get_tile_at(coords.x,coords.y,coords.z-1,g.motors[i].map)!="": coords.z-=1
			if get_staircase_at(coords.x, coords.y, coords.z, g.motors[i].map)=="y":
				if coords.y>g.motors[i].y and get_tile_at(coords.x,coords.y,coords.z+1,g.motors[i].map)!="": coords.z+=1
				if coords.y<g.motors[i].y and get_tile_at(coords.x,coords.y,coords.z-1,g.motors[i].map)!="": coords.z-=1
			tile=get_tile_at(coords.x, coords.y, coords.z, g.motors[i].map)

			if (tile!="wallspaceship" and tile.startswith("wall")) or tile=="":
				g.play("wallhard",g.motors[i].x,g.motors[i].y,g.motors[i].z,g.motors[i].map)
				g.motors[i].health-=30
				g.motors[i].speed=-1
				g.motors[i].pitch=100
				destroy_moving_sound(g.motors[i].mid)
				g.motors[i].running=False
				g.play("motorstop",g.motors[i].x,g.motors[i].y,g.motors[i].z,g.motors[i].map)
				for p in range(len(g.players)):
					pv=g.motors[i].players.find(g.players[p].name)
					if pv>-1:
						g.players[p].inve=False
						g.players[p].z+=10
						if get_tile_at(g.players[p].x,g.players[p].y,g.players[p].z,g.players[p].map).startswith("wall"): g.players[p].z-=1

						g.n.send_reliable(g.players[p].peer_id,"motorvolume -100",0)
						facing=getdir(g.players[p].facing)
						if facing==north: g.players[p].y-=1
						if facing==south: g.players[p].y+=1
						if facing==west: g.players[p].x+=1
						if facing==east: g.players[p].x-=1
						if facing==northeast: g.players[p].x-=1; g.players[p].y-=1
						if facing==southeast: g.players[p].x-=1; g.players[p].y+=1
						if facing==southwest: g.players[p].x+=1; g.players[p].y+=1
						if facing==northwest: g.players[p].x+=1; g.players[p].y-=1
						g.n.send_reliable(g.players[p].peer_id,"move "+str(g.players[p].x)+" "+str(g.players[p].y)+" "+str(g.players[p].z),0)

						g.n.send_reliable(g.players[p].peer_id, "motorunspawn", 0)
						g.players[p].vi=-1
						g.motors[i].players.remove(g.players[p].name)


			for pl in g.players:
				if pl.map==g.motors[i].map:
					update_platform(pl, g.motors[i].x, g.motors[i].x, g.motors[i].y, g.motors[i].y, g.motors[i].z, g.motors[i].z+4, "wallspaceship", coords.x, coords.x, coords.y, coords.y, coords.z, coords.z+4, "wallspaceship")
					update_platform(pl, g.motors[i].x, g.motors[i].x, g.motors[i].y, g.motors[i].y, g.motors[i].z+5, g.motors[i].z+5, "cloth", coords.x, coords.x, coords.y, coords.y, coords.z+5, coords.z+5, "cloth")
			g.motors[i].x=coords.x
			g.motors[i].y=coords.y
			g.motors[i].z=coords.z
			update_moving_sound(g.motors[i].mid, g.motors[i].x, g.motors[i].y, g.motors[i].z, g.motors[i].pitch)
			if g.motors[i].crashedto!=None:
				p=g.getpc(g.motors[i].crashedto)
				if p is not None and get_3d_distance(p.x,p.y,p.z,coords.x,coords.y,coords.z)>3:
					g.motors[i].crashed=False
					g.motors[i].crashedto=None
			else:
				for p in g.npcs:
					if g.motors[i].matchteam!=p.matchteam and not g.motors[i].crashed and p.map==g.motors[i].map and get_3d_distance(coords.x,coords.y,coords.z,p.x,p.y,p.z)<=3:
						g.motors[i].crashed=True
						g.motors[i].crashedto=p.name
						g.motors[i].health-=30
						p.health-=random(1,40)
						p.play_hit_sound()
						p.hitby=g.motors[i].owner+"'s motor"
						g.play("woodfall",coords.x,coords.y,coords.z,g.motors[i].map)
				for p in g.players:
					if not p.dead and g.motors[i].matchteam!=p.matchteam and not g.motors[i].crashed and p.map==g.motors[i].map and p.name not in g.motors[i].players and get_3d_distance(coords.x,coords.y,coords.z,p.x,p.y,p.z)<=3:
						g.motors[i].crashed=True
						g.motors[i].crashedto=p.name
						g.motors[i].health-=30
						p.health-=random(1,40)
						p.play_hit_sound()
						g.play("woodfall",coords.x,coords.y,coords.z,g.motors[i].map)
						p.z+=10
						if get_tile_at(p.x,p.y,p.z,p.map).startswith("wall"): p.z-=1

						p.hitby=g.motors[i].owner+"'s motor"
						g.n.send_reliable(p.peer_id,"move "+str(p.x)+" "+str(p.y)+" "+str(p.z),0)
						if p.vi!=-1:
							g.n.send_reliable(p.peer_id,"motorvolume -100",0)
							p.inve=False
							g.n.send_reliable(p.peer_id, "motorunspawn", 0)
							p.vi=-1
							try: p=g.getpc(g.motors[i].owner)
							except: return
							if p is not None:
								p.z+=10
								if get_tile_at(p.x,p.y,p.z,p.map).startswith("wall"): p.z-=1

								g.n.send_reliable(p.peer_id,"motorvolume -100",0)
								g.n.send_reliable(p.peer_id,"move "+str(p.x)+" "+str(p.y)+" "+str(p.z),0)
								p.inve=False
								g.n.send_reliable(p.peer_id, "motorunspawn", 0)
								p.vi=-1
			for p in range(len(g.motors[i].players)):
				pi=g.get_player_index_from(g.motors[i].players[p])
				if pi>-1:
					g.players[pi].x=coords.x
					g.players[pi].y=coords.y
					g.players[pi].z=coords.z
					if g.players[pi].name!=g.motors[i].owner: g.players[pi].facing=g.motors[i].facing
					if g.players[pi].name!=g.motors[i].owner: g.n.send_reliable(g.players[pi].peer_id,"facing "+str(g.motors[i].facing),0)
					g.n.send_reliable(g.players[pi].peer_id, "move "+str(coords.x)+" "+str(coords.y)+" "+str(coords.z), 0)
					if not g.players[pi].hidden: g.n.broadcast("update_player2 "+str(coords.x)+" "+str(coords.y)+" "+str(coords.z)+" "+g.players[pi].map+" "+g.players[pi].name+" "+str(g.motors[i].facing), 20)
		if g.motors[i].slowdowntimer.elapsed>140:
			g.motors[i].slowdowntimer.restart()
			g.motors[i].pitch-=1
			if g.motors[i].pitch<100:
				g.motors[i].pitch=100
			update_moving_sound(g.motors[i].mid, g.motors[i].x, g.motors[i].y, g.motors[i].z, g.motors[i].pitch)
		if g.motors[i].pitch!=100:
			tspeed=0
			maxspeed=g.motors[i].maxspeed
			p=g.motors[i].pitch
			windvolume=-100
			if p>=110:
				tspeed=maxspeed*15
				windvolume=-45
			if p>=120:
				tspeed=maxspeed*14
				windvolume=-40
			if p>=130:
				tspeed=maxspeed*13
				windvolume=-35
			if p>=140:
				tspeed=maxspeed*12
				windvolume=-30
			if p>=150:
				tspeed=maxspeed*11
				windvolume=-25
			if p>=160:
				tspeed=maxspeed*10
				windvolume=-20
			if p>=170:
				tspeed=maxspeed*9
				windvolume=-15
			if p>=180:
				tspeed=maxspeed*8
				windvolume=-10
			if p>=190:
				tspeed=maxspeed*7
				windvolume=-8
			if p>=200:
				tspeed=maxspeed*6
				windvolume=-6
			if p>=210:
				tspeed=maxspeed*5
				windvolume=-4
			if p>=220:
				tspeed=maxspeed*4
				windvolume=-3
			if p>=230:
				tspeed=maxspeed*3
				windvolume=-2
			if p>=240:
				tspeed=maxspeed*2
				windvolume=-1
			if p>=250:
				tspeed=maxspeed
				windvolume=0
			g.motors[i].windvolume(windvolume)
			g.motors[i].speed=tspeed
		else:
			g.motors[i].speed=0
def add_motor(x, y, z, map, health, maxspeed, maxplayers, breaktime, owner):
	t=motor(x, y, z, map, health, maxspeed, maxplayers, breaktime, owner)
	g.motors.append(t)
	for p in g.players:
		if p.map==map: send_platform(p, x, x, y, y, z, z+4, "wallspaceship")
		if p.map==map: send_platform(p, x, x, y, y, z+5, z+5, "cloth")
def get_max_values(mapname):
	ind=g.get_map_index(mapname)
	temp=vector()
	if ind<0:
		return temp
	temp.x=g.maps[ind].max.x
	temp.y=g.maps[ind].max.y
	temp.z=g.maps[ind].max.z
	return temp
class my_list(list):
	def find(self, val):
		for i, x in enumerate(self):
			if x==val:
				return i
		return -1
def send_platform(p, minx, maxx, miny, maxy, minz, maxz, tile):
	g.n.send_reliable(p.peer_id, "addplatform " + str(round(minx)) + " " + str(round(maxx)) + " " + str(round(miny)) + " " + str(round(maxy)) + " " + str(round(minz)) + " " + str(round(maxz)) + " " + tile, 4)

def update_platform(p, minx, maxx, miny, maxy, minz, maxz, tile, minx2, maxx2, miny2, maxy2, minz2, maxz2, tile2):
	g.n.send_reliable(p.peer_id, "updateplatform " + str(round(minx)) + " " + str(round(maxx)) + " " + str(round(miny)) + " " + str(round(maxy)) + " " + str(round(minz)) + " " + str(round(maxz)) + " " + tile + " " + str(round(minx2)) + " " + str(round(maxx2)) + " " + str(round(miny2)) + " " + str(round(maxy2)) + " " + str(round(minz2)) + " " + str(round(maxz2)) + " " + tile2, 4)

def remove_platform(p, minx, maxx, miny, maxy, minz, maxz, tile):
	g.n.send_reliable(p.peer_id, "removeplatform " + str(round(minx)) + " " + str(round(maxx)) + " " + str(round(miny)) + " " + str(round(maxy)) + " " + str(round(minz)) + " " + str(round(maxz)) + " " + tile, 4)
