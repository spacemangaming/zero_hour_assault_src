import globals as g
from timer import timer
from variable_management import string_split

from vector import vector
from variable_management import string_replace
from file_directories import find_files
import copy

class mapdata:
	def __init__(self, loadname):
		if 1:
			self.tile_cache={}
			self.nwall_cache={}
			self.name=""
			self.maptiles=[]
			self.mapnwalls=[]
			self.mapstaircases=[]
			self.maphidden_areas=[]
			self.mapignore_ambiences=[]
			self.mapchests=[]
			self.mapwalls=[]
			self.rawdata=""
			self.max=vector()
			try: self.internal_load(loadname)
			except: pass
	def return_tile(self,  x,  y,  z):
	
		if (x, y, z) in self.tile_cache: return self.tile_cache[(x, y, z)]
		outval=""
		for i in range(len(self.maptiles)):
		
			if(self.maptiles[i].is_on_tile(x, y, z)):
			
				outval=self.maptiles[i].type
#				break
				
			
		self.tile_cache[(x, y, z)]=outval
		return outval
		
	def return_nwall(self,  x,  y,  z):
	
		if (x, y, z) in self.nwall_cache: return self.nwall_cache[(x, y, z)]
		outval=""
		for i in range(len(self.mapnwalls)):
		
			if(self.mapnwalls[i].is_on_nwall(x, y, z)):
			
				outval=self.mapnwalls[i].type
				break
				
			
		self.nwall_cache[(x, y, z)]=outval
		return outval
		

	def return_staircase(self,  x,  y,  z):
	
		outval=""
		for i in range(len(self.mapstaircases)):
		
			if(self.mapstaircases[i].is_on_staircase(x, y, z)):
			
				outval=self.mapstaircases[i].dir
				
			
		return outval
		

	def return_hidden_area(self,  x,  y,  z):
	
		outval=""
		for i in range(len(self.maphidden_areas)):
		
			if(self.maphidden_areas[i].is_on_hidden_area(x, y, z)):
			
				outval=self.maphidden_areas[i].type
				
			
		return outval
		

	def return_ignore_ambience(self,  x,  y,  z):
	
		outval=""
		for i in range(len(self.mapignore_ambiences)):
		
			if(self.mapignore_ambiences[i].is_on_ignore_ambience(x, y, z)):
			
				outval=self.mapignore_ambiences[i].type
				
			
		return outval
		



	def return_wall(self,  x,  y,  z):
	
		outval=""
		for i in range(len(self.mapwalls)):
		
			if(self.mapwalls[i].is_on_wall(x, y, z)):
			
				outval=self.mapwalls[i].type
				
			
		return outval
		

	def internal_load(self,loadname):
	
		self.tile_cache={}
		self.nwall_cache={}
		f=open("maps/"+loadname+".map", "r")
		self.rawdata=f.read()
		map=delinear(self.rawdata)
		f.close()
		for i in range(len(map)):
		
			parsed=string_split(map[i], ":", False)
			if(parsed[0]=="mapname"):
			
				self.name=parsed[1]
				

			elif(parsed[0]=="maxx"):
				self.max.x=int(parsed[1])
			elif(parsed[0]=="maxy"):
				self.max.y=int(parsed[1])
			elif(parsed[0]=="maxz"):
				self.max.z=int(parsed[1])
			elif parsed[0]=="chest" and len(parsed)>3:
				ch=mapchest()
				ch.x=int(parsed[1])
				ch.y=int(parsed[2])
				ch.z=int(parsed[3])
				self.mapchests.append(ch)
			elif(parsed[0]=="platform" or parsed[0]=="staircase" and len(parsed)>6):
			
				minx=int(parsed[1])
				maxx=int(parsed[2])
				miny=int(parsed[3])
				maxy=int(parsed[4])
				try: z=int(parsed[5])
				except: z=int(float(parsed[5]))
				try:
					maxz=int(parsed[6])
					type=parsed[7]
				except:
					maxz=z
					type=parsed[6]
				if "wall" in type:
					temp=mapnwall()
					temp.minx=minx
					temp.maxx=maxx
					temp.miny=miny
					temp.maxy=maxy
					temp.minz=z
					temp.maxz=maxz
					temp.type=type
					self.mapnwalls.append(temp)

				temp=maptile()
				temp.minx=minx
				temp.maxx=maxx
				temp.miny=miny
				temp.maxy=maxy
				temp.minz=z
				temp.maxz=maxz
				temp.type=type
				self.maptiles.append(temp)
				
			
		
	
			if parsed[0]=="staircase" and len(parsed)>6:
			
				minx=int(parsed[1])
				maxx=int(parsed[2])
				miny=int(parsed[3])
				maxy=int(parsed[4])
				z=int(parsed[5])
				try:
					maxz=int(parsed[6])
					type=parsed[7]
					dir=parsed[8]
				except:
					maxz=z
					type=parsed[6]
					dir=parsed[7]
				temp=mapstaircase()
				temp.minx=minx
				temp.maxx=maxx
				temp.miny=miny
				temp.maxy=maxy
				temp.minz=z
				temp.maxz=maxz
				temp.type=type
				temp.dir=dir
				self.mapstaircases.append(temp)
				
			
		
	

			elif(parsed[0]=="hidden_area" and len(parsed)>5):
			
				minx=int(parsed[1])
				maxx=int(parsed[2])
				miny=int(parsed[3])
				maxy=int(parsed[4])
				z=int(parsed[5])
				try:
					maxz=int(parsed[6])
				except:
					maxz=z
				temp=maphidden_area()
				temp.minx=minx
				temp.maxx=maxx
				temp.miny=miny
				temp.maxy=maxy
				temp.minz=z
				temp.maxz=maxz
				self.maphidden_areas.append(temp)
				
			
		
	
			elif(parsed[0]=="ignore_amb" and len(parsed)>5):
			
				minx=int(parsed[1])
				maxx=int(parsed[2])
				miny=int(parsed[3])
				maxy=int(parsed[4])
				z=int(parsed[5])
				try:
					maxz=int(parsed[6])
				except:
					maxz=z
				temp=mapignore_ambience()
				temp.minx=minx
				temp.maxx=maxx
				temp.miny=miny
				temp.maxy=maxy
				temp.minz=z
				temp.maxz=maxz
				self.mapignore_ambiences.append(temp)
				
			
		
	


			elif(parsed[0]=="wall" and len(parsed)>6):
			
				minx=int(parsed[1])
				maxx=int(parsed[2])
				miny=int(parsed[3])
				maxy=int(parsed[4])
				z=int(parsed[5])
				try:
					maxz=int(parsed[6])
					type=parsed[7]
				except:
					maxz=z
					type=parsed[6]
				temp=mapwall()
				temp.minx=minx
				temp.maxx=maxx
				temp.miny=miny
				temp.maxy=maxy
				temp.minz=z
				temp.maxz=maxz
				temp.type=type
				self.mapwalls.append(temp)
				
			
		
	
			elif parsed[0]=="electric_pole":
				x=int(parsed[1])
				y=int(parsed[2])
				z=int(parsed[3])
				found=False
				for e in g.electrics:
					if e.x==x and e.y==y and e.z==z and e.map==self.name: found=True
				if not found:
					e=g.electric(x,y,z,self.name)
					g.electrics.append(e)
			elif(parsed[0]=="mwall"):
			
				minx=int(parsed[1])
				maxx=int(parsed[2])
				miny=int(parsed[3])
				maxy=int(parsed[4])
				z=int(parsed[5])
				try:
					maxz=int(parsed[6])
					type=parsed[7]
				except:
					maxz=z
					type=parsed[6]
				temp=mwall(minx,maxx,miny,maxy,z,maxz,self.name,type)
				g.mwalls.append(temp)
				
			elif parsed[0] == "waypoint" and len(parsed) >= 6:
				path_id = parsed[1]
				idx = int(parsed[2])
				x = int(parsed[3])
				y = int(parsed[4])
				z = int(parsed[5])
				is_stop = False
				stop_duration = 0
				if len(parsed) >= 8:
					is_stop = (parsed[6].lower() == "true" or parsed[6] == "1")
					stop_duration = int(parsed[7])
				w = {
					"path_id": path_id,
					"index": idx,
					"x": x,
					"y": y,
					"z": z,
					"is_stop": is_stop,
					"stop_duration": stop_duration
				}
				g.waypoints.append(w)
				
			elif parsed[0] == "transit" and len(parsed) >= 6:
				vtype = parsed[1]
				start_x = int(parsed[2])
				start_y = int(parsed[3])
				z = int(parsed[4])
				config_str = parsed[5]
				
				# Parse semicolon-separated key-value configurations
				config = {}
				for pair in config_str.split(";"):
					if "=" in pair:
						k, v = pair.split("=", 1)
						config[k.strip()] = v.strip()
				
				path_id = config.get("path", "")
				interior_map = config.get("interior_map", "")
				max_health = int(config.get("health", "500"))
				speed = int(config.get("speed", "30"))
				engine_sound = config.get("sound", "motorengine.ogg")
				door_mode = config.get("door_mode", "always_open")
				
				from transit import OpenDoorBus
				if door_mode == "always_open":
					v = OpenDoorBus(vtype, start_x, start_y, z, self.name, path_id, interior_map, max_health, speed, engine_sound, door_mode)
					g.transits.append(v)
				
			
		
	

class mapchest:
	def __init__(self):
		self.x=0
		self.y=0
		self.z=0
class maptile:
	def __init__(self):
		self.minx=0
		self.maxx=0
		self.miny=0
		self.maxy=0
		self.minz=0
		self.maxz=0
		self.type=""
	def is_on_tile(self,  x, y, z):
	
		if(self.minx>x):
		
			return False
			
		if(self.minx<=x and self.maxx>=x and self.miny<=y and self.maxy>=y and self.minz<=z and self.maxz>=z):
		
			return True
			
		return False
		
	
def get_tile_at(x, y, z, mapname, includeglobal=True):
	outval=""
	x=round(x)
	y=round(y)
	z=round(z)
	if(includeglobal==True):
	
		index=get_map_index(mapname)
		if(index<0):
		
			return ""
			
		else:
		
			outval=g.maps[index].return_tile(x, y, z)
			
		
	if (g.rain or g.rainfinish) and "wall" not in outval and outval!="" and outval!="air" and outval in g.nomudtiles:
		if get_ignore_ambience_at(x,y,z,map)=="": outval="mud"
	return outval
	
g.get_tile_at=get_tile_at
class mapnwall:
	def __init__(self):
		self.minx=0
		self.maxx=0
		self.miny=0
		self.maxy=0
		self.minz=0
		self.maxz=0
		self.type=""
	def is_on_nwall(self,  x, y, z):
	
		if(self.minx>x):
		
			return False
			
		if(self.minx<=x and self.maxx>=x and self.miny<=y and self.maxy>=y and self.minz<=z and self.maxz>=z):
		
			return True
			
		return False
		
	
def get_nwall_at(x, y, z, mapname, includeglobal=True):
	outval=""
	x=round(x)
	y=round(y)
	z=round(z)
	if(includeglobal==True):
	
		index=get_map_index(mapname)
		if(index<0):
		
			return ""
			
		else:
		
			outval=g.maps[index].return_nwall(x, y, z)
			
		
	if (g.rain or g.rainfinish) and "wall" not in outval and outval!="" and outval!="air" and outval in g.nomudnwalls:
		if get_ignore_ambience_at(x,y,z,map)=="": outval="mud"
	return outval
	
g.get_nwall_at=get_nwall_at

class mapstaircase:
	def __init__(self):
		self.minx=0
		self.maxx=0
		self.miny=0
		self.maxy=0
		self.minz=0
		self.maxz=0
		self.type=""
		self.dir=""
	def is_on_staircase(self,  x, y, z):
	
		if(self.minx>x):
		
			return False
			
		if(self.minx<=x and self.maxx>=x and self.miny<=y and self.maxy>=y and self.minz<=z and self.maxz>=z):
		
			return True
			
		return False
		
	
def get_staircase_at(x, y, z, mapname, includeglobal=True):
	outval=""
	x=round(x)
	y=round(y)
	z=round(z)
	if(includeglobal==True):
	
		index=get_map_index(mapname)
		if(index<0):
		
			return ""
			
		else:
		
			outval=g.maps[index].return_staircase(x, y, z)
			
		
	return outval
	
g.get_staircase_at=get_staircase_at

class maphidden_area:
	def __init__(self):
		self.minx=0
		self.maxx=0
		self.miny=0
		self.maxy=0
		self.minz=0
		self.maxz=0
		self.type="hidden_area"
	def is_on_hidden_area(self,  x, y, z):
	
		if(self.minx>x):
		
			return False
			
		if(self.minx<=x and self.maxx>=x and self.miny<=y and self.maxy>=y and self.minz<=z and self.maxz>=z):
		
			return True
			
		return False
		
	
def get_hidden_area_at(x, y, z, mapname, includeglobal=True):
	outval=""
	x=round(x)
	y=round(y)
	z=round(z)
	if(includeglobal==True):
	
		index=get_map_index(mapname)
		if(index<0):
		
			return ""
			
		else:
		
			outval=g.maps[index].return_hidden_area(x, y, z)
			
		
	return outval
	
g.get_hidden_area_at=get_hidden_area_at
class mapignore_ambience:
	def __init__(self):
		self.minx=0
		self.maxx=0
		self.miny=0
		self.maxy=0
		self.minz=0
		self.maxz=0
		self.type="ignore_ambience"
	def is_on_ignore_ambience(self,  x, y, z):
	
		if(self.minx>x):
		
			return False
			
		if(self.minx<=x and self.maxx>=x and self.miny<=y and self.maxy>=y and self.minz<=z and self.maxz>=z):
		
			return True
			
		return False
		
	
def get_ignore_ambience_at(x, y, z, mapname, includeglobal=True):
	outval=""
	x=round(x)
	y=round(y)
	z=round(z)
	if(includeglobal==True):
	
		index=get_map_index(mapname)
		if(index<0):
		
			return ""
			
		else:
		
			outval=g.maps[index].return_ignore_ambience(x, y, z)
			
		
	return outval
	
g.get_ignore_ambience_at=get_ignore_ambience_at


class mapwall:
	def __init__(self):
		self.minx=0
		self.maxx=0
		self.miny=0
		self.maxy=0
		self.minz=0
		self.maxz=0
		self.type=""
		self.health=50
		self.destroyed=True
	def is_on_wall(self,  x, y, z):
	
		if(self.minx>x):
		
			return False
			
		if(self.minx<=x and self.maxx>=x and self.miny<=y and self.maxy>=y and self.minz<=z and self.maxz>=z):
		
			return True
			
		return False
		
	
def get_wall_at(x, y, z, mapname, includeglobal=True):
	outval=""
	x=round(x)
	y=round(y)
	z=round(z)
	if(includeglobal==True):
	
		index=get_map_index(mapname)
		if(index<0):
		
			return ""
			
		else:
		
			outval=g.maps[index].return_wall(x, y, z)
			
		
	return outval
	
g.get_wall_at=get_wall_at

def linear( a):
	final=""
	for i in range(len(a)):
	
		final+=(a[i]+"\n")
		
	return final
	
def delinear(a):
	return string_split(a, "\n", False)
	
def init_mapsystem():
	walld={}
	for m in g.maps:
		for w in m.mapwalls:
			try:
				walld[m.name].append(copy.deepcopy(w))
			except:
				walld[m.name]=[]
				walld[m.name].append(copy.deepcopy(w))
	g.maps.clear()
	g.mwalls.clear()
	
	# Clean up transit moving sounds and decouple passengers before clearing
	for bus in g.transits:
		if hasattr(bus, "engine_sound_id") and bus.engine_sound_id:
			from moving_sound_serverside_handler import destroy_moving_sound
			destroy_moving_sound(bus.engine_sound_id)
			bus.engine_sound_id = None
		for name in list(bus.players):
			p = g.getpc(name)
			if p is not None:
				p.in_bus = False
				p.bus_instance = None
				
	g.transits.clear()
	g.waypoints.clear()
	mapfiles=find_files("maps")
	for i in range(len(mapfiles)):
	
		workingname=string_replace(mapfiles[i], ".map", "", True)
		temp=mapdata(workingname)
		try: temp.mapwalls=copy.deepcopy(walld[temp.name])
		except: pass
		g.maps.append(temp)
		
	
g.init_mapsystem=init_mapsystem
def get_map_index(mn) :
	for i in range(len(g.maps)):
		if g.maps[i].name==mn:
			return i
	return -1
g.get_map_index=get_map_index
class mwall:
	def __init__(self,minx,maxx,miny,maxy,minz,maxz,map,tile):
		self.destroyed=False
		self.health=100
		self.respawntimer=timer()
		self.minx=minx
		self.maxx=maxx
		self.miny=miny
		self.maxy=maxy
		self.minz=minz
		self.maxz=maxz
		self.map=map
		self.tile=tile
		for p in g.players:
			if p.map==self.map:
				send_platform(p, self.minx, self.maxx, self.miny, self.maxy, self.minz, self.maxz, self.tile)
def mwallloop():
	for mwall in g.mwalls:
		if mwall.destroyed and mwall.respawntimer.elapsed>=120000:
			mwall.destroyed=False
			mwall.respawntimer.restart()
			for index in range(len(g.players)):
				if 1:
					if 1:
						if not mwall.destroyed and mwall.map==g.players[index].map:
							send_platform(g.players[index], mwall.minx, mwall.maxx, mwall.miny, mwall.maxy, mwall.minz, mwall.maxz, mwall.tile)
		if mwall.health<=0 and not mwall.destroyed:
			mwall.destroyed=True
			mwall.respawntimer.restart()
			for index in range(len(g.players)):
				if 1:
					if 1:
						if mwall.destroyed and mwall.map==g.players[index].map:
							remove_platform(g.players[index], mwall.minx, mwall.maxx, mwall.miny, mwall.maxy, mwall.minz, mwall.maxz, mwall.tile)
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

class barricade:
	def __init__(self,minx,maxx,miny,maxy,minz,maxz,map,tile,owner):
		self.owner=owner
		self.destroyed=False
		self.health=200
		self.respawntimer=timer()
		self.minx=minx
		self.maxx=maxx
		self.miny=miny
		self.maxy=maxy
		self.minz=minz
		self.maxz=maxz
		self.map=map
		self.tile=tile
		for p in g.players:
			if p.map==self.map:
				send_platform(p, self.minx, self.maxx, self.miny, self.maxy, self.minz, self.maxz, self.tile)
				send_platform(p, self.minx, self.maxx, self.miny, self.maxy, self.maxz+1, self.maxz+1, "dirt3")
	def remove_platform(self):
		for p in g.players:
			if p.map==self.map:
				remove_platform(p, self.minx, self.maxx, self.miny, self.maxy, self.minz, self.maxz, self.tile)
				remove_platform(p, self.minx, self.maxx, self.miny, self.maxy, self.maxz+1, self.maxz+1, "dirt3")

class ladder:
	def __init__(self,minx,maxx,miny,maxy,minz,maxz,map,tile,owner):
		self.owner=owner
		self.destroyed=False
		self.health=10
		self.respawntimer=timer()
		self.minx=minx
		self.maxx=maxx
		self.miny=miny
		self.maxy=maxy
		self.minz=minz
		self.maxz=maxz
		self.map=map
		self.tile=tile
		for p in g.players:
			if p.map==self.map:
				send_platform(p, self.minx, self.maxx, self.miny, self.maxy, self.minz, self.maxz, self.tile)
	def remove_platform(self):
		for p in g.players:
			if p.map==self.map:
				remove_platform(p, self.minx, self.maxx, self.miny, self.maxy, self.minz, self.maxz, self.tile)