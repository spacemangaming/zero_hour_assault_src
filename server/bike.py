import globals as g
from rotation import move
from timer import timer
from vector import vector
class bike:
	def __init__(self,x,y,z,map,owner):
		self.x=x
		self.y=y
		self.z=z
		self.map=map
		self.players=[]
		self.hornplaytimer=timer()
		self.owner=owner
		for p in g.players:
			if p.map==self.map: self.send_platform_to(p)
	def horn(self,index):
		if g.players[index].name!=self.players[0]: return
		g.players[index].playsoundmoving("bikehorn")
	def remove_all_players(self):
		for p in self.players: self.exit(g.get_player_index_from(p))
	def exit(self,index):
		if index==-1: return
		self.players.remove(g.players[index].name)
		g.n.send_reliable(g.players[index].peer_id,"notinbike",0)
		g.players[index].playsound("bikestop")
		g.players[index].bike=None
		self.hornplaytimer.restart()
	def add_player(self,index):
		if g.players[index].name in self.players: return
		self.players.append(g.players[index].name)
		g.n.send_reliable(g.players[index].peer_id,"inbike",0)
		g.players[index].playsound("bikestart")
		g.players[index].bike=self
	def move(self,index):
		if g.players[index].name!=self.players[0]: return
		dir=g.players[index].facing
		oldtile=g.get_tile_at(self.x,self.y,self.z,self.map)
		oldx=self.x
		oldy=self.y
		oldz=self.z
		max=get_max_values(self.map)
		v=vector(self.x,self.y,self.z)
		for _ in range(10):
			v=move(v.x,v.y,v.z,dir,0,0,0)
			tile=g.get_tile_at(v.x,v.y,v.z,self.map)
			if tile=="" or "water" in tile or "wall" in tile:
				g.play("bikecrash",self.x,self.y,self.z,self.map)
				for pl2 in self.players:
					try: self.remove_platform_to(g.getpc(pl2))
					except: pass
				self.remove_all_players()
				g.bikes.remove(self)
				return
		if v.x>max.x or v.y>max.y or v.z>max.z or v.x<0 or v.y<0: return
		self.x=v.x
		self.y=v.y
		self.z=v.z
		for pl in self.players:
			p=g.getpc(pl)
			if p is None: continue
			p.x=self.x
			p.y=self.y
			p.z=self.z
			g.n.send_reliable(p.peer_id,"move "+str(p.x)+" "+str(p.y)+" "+str(p.z),0)
			if not p.hidden: g.n.broadcast("update_player2 "+str(p.x)+" "+str(p.y)+" "+str(p.z)+" "+p.map+" "+p.name+" "+str(p.facing),20)
		try: g.players[index].playsoundmoving(self.get_tile_sound())
		except: pass
		self.radar(dir)
		tile=g.get_tile_at(self.x,self.y,self.z,self.map)
		if tile=="" or "water" in tile or "wall" in tile:
			g.play("bikecrash",self.x,self.y,self.z,self.map)
			for pl2 in self.players:
				try: self.remove_platform_to(g.getpc(pl2))
				except: pass
			self.remove_all_players()
			g.bikes.remove(self)
			return
		if tile!=oldtile: g.play("bikechangetile",self.x,self.y,self.z,self.map)
		for pl in self.players:
			p=g.getpc(pl)
			if p is not None and p.map==self.map:
				update_platform(p,oldx,oldx,oldy,oldy,oldz,oldz,"metal2",self.x,self.x,self.y,self.y,self.z,self.z,"metal2")
	def radar(self,dir):
		v=vector(self.x,self.y,self.z)
		max=get_max_values(self.map)
		for i in range(30):
			if 1:
				if v.x>max.x:
					v.x=max.x
				if v.x<0:
					v.x=0
				if v.y>max.y:
					v.y=max.y
				if v.y<0:
					v.y=0
				if v.z>max.z:
					v.z=max.z

			v=move(v.x,v.y,v.z,dir,0,0,0)
			tile=g.get_tile_at(v.x,v.y,v.z,self.map)
			if "wall" in tile or tile=="" or "water" in tile: g.getpc(self.players[0]).playsound("bikeradar"); return
	def send_platform_to(self,p):
		send_platform(p,self.x,self.x,self.y,self.y,self.z,self.z,"metal2")
	def remove_platform_to(self,p):
		remove_platform(p,self.x,self.x,self.y,self.y,self.z,self.z,"metal2")



	def get_tile_sound(self):
		tile=g.get_tile_at(self.x,self.y,self.z,self.map)
		if "grass" in tile: return "bikegrass"
		elif "gravel" in tile: return "bikegravel"
		elif "metal" in tile: return "bikemedal"
		elif "concrete" in tile or "carpet" in tile: return "bikemisc"
		elif "mud" in tile: return "bikemud"
		elif "stone" in tile or "rock" in tile: return "bikerock"
		elif "weed" in tile: return "bikeweed"
		elif "wood" in tile: return "bikewood"
		else: return "bikemisc"
def bikeloop():
	for b in g.bikes:
		for p in b.players:
			if g.get_player_index_from(p)<=-1: b.players.remove(p)
			if g.get_player_index_from(p)>-1 and g.getpc(p).map!=b.map: b.players.remove(p)
		if b.hornplaytimer.elapsed>4000 and len(b.players)<=0:
			b.hornplaytimer.restart()
			g.play("bikehorn",b.x,b.y,b.z,b.map)

def send_platform(p, minx, maxx, miny, maxy, minz, maxz, tile):
	g.n.send_reliable(p.peer_id, "addplatform " + str(round(minx)) + " " + str(round(maxx)) + " " + str(round(miny)) + " " + str(round(maxy)) + " " + str(round(minz)) + " " + str(round(maxz)) + " " + tile, 4)

def remove_platform(p, minx, maxx, miny, maxy, minz, maxz, tile):
	g.n.send_reliable(p.peer_id, "removeplatform " + str(round(minx)) + " " + str(round(maxx)) + " " + str(round(miny)) + " " + str(round(maxy)) + " " + str(round(minz)) + " " + str(round(maxz)) + " " + tile, 4)
def get_max_values(mapname):
	ind=g.get_map_index(mapname)
	temp=vector()
	if ind<0:
		return temp
	temp.x=g.maps[ind].max.x
	temp.y=g.maps[ind].max.y
	temp.z=g.maps[ind].max.z
	return temp
def update_platform(p, minx, maxx, miny, maxy, minz, maxz, tile, minx2, maxx2, miny2, maxy2, minz2, maxz2, tile2):
	g.n.send_reliable(p.peer_id, "updateplatform " + str(round(minx)) + " " + str(round(maxx)) + " " + str(round(miny)) + " " + str(round(maxy)) + " " + str(round(minz)) + " " + str(round(maxz)) + " " + tile + " " + str(round(minx2)) + " " + str(round(maxx2)) + " " + str(round(miny2)) + " " + str(round(maxy2)) + " " + str(round(minz2)) + " " + str(round(maxz2)) + " " + tile2, 4)

