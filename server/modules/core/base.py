import globals as g
from random import randint as random
from timer import timer
from datetime import datetime
import pickle
from file_directories import file_delete, file_exists
from file_directories import file_get_contents, file_put_contents
from variable_management import string_replace, string_contains, string_split
import time
import copy
from motor import remove_platform, send_platform
class base_turret:
	def __init__(self, x, y, z, map, base_name):
		self.x = x
		self.y = y
		self.z = z
		self.map = map
		self.base_name = base_name
		self.weapon_type = "base_gun"
		self.operator = None
		self.fire_timer = timer()

	def __getstate__(self):
		state = self.__dict__.copy()
		state["operator"] = None
		return state

	def __setstate__(self, state):
		self.__dict__.update(state)
		self.operator = None

	def get_firetime(self):
		import data_loader
		w = data_loader.get_weapon(self.weapon_type)
		return w.get("fire_time", 300) if w else 300

def dismount_turret(player):
	if hasattr(player, "controlled_turret") and player.controlled_turret is not None:
		turret = player.controlled_turret
		turret.operator = None
		player.controlled_turret = None
		g.n.send_reliable(player.peer_id, "You stepped off the turret.", 0)
		player.playsound("sitstop", True)

class group_base:
	def __init__(self,bx,by,bz,bmap,bname,bowner,bmapappend=""):
		self.mapappend=""
		self.chestlog=""
		self.ammo=10
		self.firetimer=timer()
		self.dooropening=False
		self.password=""
		self.mapappend=bmapappend
		self.x=bx
		self.alarmtimer=timer()
		self.y=by
		self.z=bz
		self.map=bmap
		self.alarm=False
		self.notifytimer=timer()
		self.name=bname
		self.owner=bowner
		self.health=20000000
		self.max_health=20000000
		self.wall_level=1
		self.turrets=[]
		self.generator_on=False
		self.generator_fuel=0.0
		self.generator_timer=timer()
		self.siren_timer=timer()
		self.dooron=False
		self.doorontimer=timer()
	def get_door_tile(self):
		if self.wall_level == 1:
			return "wallglass6"
		elif self.wall_level == 2:
			return "wallmetal"
		elif self.wall_level == 3:
			return "wallstone2"
		return "wallglass6"
	def send_turrets_to(self,p):
		for t in self.turrets:
			send_platform(p,t.x,t.x,t.y,t.y,t.z,t.z,"metal")
			send_zone(p,t.x,t.x,t.y,t.y,t.z,t.z,"turret_of_group_base_"+self.name)
	def remove_turrets_from(self,p):
		for t in self.turrets:
			remove_platform(p,t.x,t.x,t.y,t.y,t.z,t.z,"metal")
			remove_zone(p,t.x,t.x,t.y,t.y,t.z,t.z,"turret_of_group_base_"+self.name)
	def send_platform_to(self,p):
		tile = self.get_door_tile()
		send_platform(p,self.x,self.x,self.y,self.y,self.z,self.z+8,tile)
		send_zone(p,self.x,self.x,self.y-1,self.y,self.z,self.z+8,"entrance_of_group_base_"+self.name)
		self.send_turrets_to(p)
	def remove_platform_to(self,p):
		tile = self.get_door_tile()
		remove_platform(p,self.x,self.x,self.y,self.y,self.z,self.z+8,tile)
		remove_zone(p,self.x,self.x,self.y-1,self.y,self.z,self.z+8,"entrance_of_group_base_"+self.name)
		self.remove_turrets_from(p)

def group_baseloop():
	for i in g.group_bases:
		if i.dooron and i.doorontimer.elapsed>2000:
			i.doorontimer.restart()
			i.dooron=False
			g.play("doorclose4",0,0,0,"basement"+i.name+i.mapappend)
			g.play("doorclose4",i.x,i.y,i.z,i.map)
		if i.password=="" or len(i.password)<6: i.password=randomstring()
		if i.alarm==True and i.alarmtimer.elapsed>=20000:
			i.alarmtimer.restart()
			i.alarm=False

		# Generator fuel logic
		if i.generator_on:
			elapsed_seconds = i.generator_timer.elapsed / 1000.0
			i.generator_timer.restart()
			if i.generator_fuel > 0:
				i.generator_fuel -= elapsed_seconds
				if i.generator_fuel <= 0:
					i.generator_fuel = 0.0
					i.generator_on = False
					g.play("motorstop", i.x, i.y, i.z, i.map)
					g.play("motorstop", 30, 30, 0, "basement" + i.name + i.mapappend)
					for p in g.players:
						if p.group == i.name:
							g.n.send_reliable(p.peer_id, "groupnotification Generator has run out of fuel!", 0)
			else:
				i.generator_on = False
		else:
			i.generator_timer.restart()

		# Siren Alarm logic
		if i.alarm:
			if i.siren_timer.elapsed >= 3000:
				i.siren_timer.restart()
				g.play("misc32", i.x, i.y, i.z, i.map)
				g.play("misc32", 30, 30, 0, "basement" + i.name + i.mapappend)

		if i.alarm==True and i.notifytimer.elapsed>=5000:
			i.notifytimer.restart()
			attacker_pc=g.getpc(i.hitby)
			if attacker_pc is None or not attacker_pc.hidden:
				for p in g.players:
					if p.group==i.name: g.n.send_reliable(p.peer_id,"play_s misc32.ogg",0); g.n.send_reliable(p.peer_id,"groupnotification "+i.hitby+" attacking your group base!",0)

		if i.health<=0:
			g.play("misc56",i.x,i.y,i.z,i.map)
			g.n.broadcast("distsound misc58 "+str(i.x)+" "+str(i.y)+" "+str(i.z)+" "+str(i.map),0)
			should_del=True
			for base in g.group_bases:
				if base.name==i.name and base.mapappend!=i.mapappend: should_del=False
			if should_del:
				for grp in g.groups:
					if i.name==grp.name:
						destroyer_pc=g.getpc(i.hitby)
						destroyer_name=i.hitby if (destroyer_pc is None or not destroyer_pc.hidden) else "unknown"
						grp.send("groupnotification group deleted because its base destroyed by "+destroyer_name+"!",0)
						g.groups.remove(grp)
			for pl in g.players:
				if pl.map==i.map: i.remove_platform_to(pl)
				if pl.map=="basement"+i.name+i.mapappend: g.move_player(g.get_player_index_from(pl),i.x,i.y,i.z,i.map)
			f=open("grouphistory.txt","a")
			f.write("group base "+i.name+" destroyed by "+i.hitby+" at "+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"\n")
			f.close()
			g.group_bases.remove(i)
			file_delete("maps/basement"+i.name+i.mapappend+".map")
			return
def create_group_base(x,y,z,map,name,owner,mapappend=""):
	g.group_bases.append(group_base(x,y,z,map,name,owner,mapappend))
def randomstring(length=6):
	temp="abcdefghijklmnopqrstuvwxyz1234567890"
	ret=""
	for i in range(length):
		ret=ret+temp[random(0, (len(temp)-1))]
	return ret

def send_platform(p, minx, maxx, miny, maxy, minz, maxz, tile):
	g.n.send_reliable(p.peer_id, "addplatform " + str(round(minx)) + " " + str(round(maxx)) + " " + str(round(miny)) + " " + str(round(maxy)) + " " + str(round(minz)) + " " + str(round(maxz)) + " " + tile, 4)

def update_platform(p, minx, maxx, miny, maxy, minz, maxz, tile, minx2, maxx2, miny2, maxy2, minz2, maxz2, tile2):
	g.n.send_reliable(p.peer_id, "updateplatform " + str(round(minx)) + " " + str(round(maxx)) + " " + str(round(miny)) + " " + str(round(maxy)) + " " + str(round(minz)) + " " + str(round(maxz)) + " " + tile + " " + str(round(minx2)) + " " + str(round(maxx2)) + " " + str(round(miny2)) + " " + str(round(maxy2)) + " " + str(round(minz2)) + " " + str(round(maxz2)) + " " + tile2, 4)

def remove_platform(p, minx, maxx, miny, maxy, minz, maxz, tile):
	g.n.send_reliable(p.peer_id, "removeplatform " + str(round(minx)) + " " + str(round(maxx)) + " " + str(round(miny)) + " " + str(round(maxy)) + " " + str(round(minz)) + " " + str(round(maxz)) + " " + tile, 4)
def send_zone(p, minx, maxx, miny, maxy, minz, maxz, tile):
	g.n.send_reliable(p.peer_id, "addzone " + str(round(minx)) + " " + str(round(maxx)) + " " + str(round(miny)) + " " + str(round(maxy)) + " " + str(round(minz)) + " " + str(round(maxz)) + " " + tile, 4)

def update_zone(p, minx, maxx, miny, maxy, minz, maxz, tile, minx2, maxx2, miny2, maxy2, minz2, maxz2, tile2):
	g.n.send_reliable(p.peer_id, "updatezone " + str(round(minx)) + " " + str(round(maxx)) + " " + str(round(miny)) + " " + str(round(maxy)) + " " + str(round(minz)) + " " + str(round(maxz)) + " " + tile + " " + str(round(minx2)) + " " + str(round(maxx2)) + " " + str(round(miny2)) + " " + str(round(maxy2)) + " " + str(round(minz2)) + " " + str(round(maxz2)) + " " + tile2, 4)

def remove_zone(p, minx, maxx, miny, maxy, minz, maxz, tile):
	g.n.send_reliable(p.peer_id, "removezone " + str(round(minx)) + " " + str(round(maxx)) + " " + str(round(miny)) + " " + str(round(maxy)) + " " + str(round(minz)) + " " + str(round(maxz)) + " " + tile, 4)

