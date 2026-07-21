from file_directories import file_exists
from rotation import vector
import globals as g
from random import randint as random
from random import choice
from variable_management import string_contains, string_split
from rotation import get_3d_distance, calculate_x_y_angle
from timer import timer
from file_directories import file_delete
class zk:
	def __init__(self,x,y,z,map,owner,code):
		g.play("semtexactivate",x,y,z,map)
		self.codefound=False
		self.hitmwalls=[]
		self.hitbarricades=[]
		self.hitladders=[]
		self.beeptimer=timer()
		self.beeptime=200
		self.owner=owner
		self.mindammage=50
		self.maxdammage=50
		self.code=code
		self.checktimer=timer()
		self.x=x
		self.range=15
		self.y=y
		self.z=z
		self.map=map
		self.explodetimer=timer()
		self.exploding=False
		self.explodetime=3000
		self.hitwalls=[]
		self.matchteam=g.getpc(owner).matchteam
		self.joinedmatch=g.getpc(owner).joinedmatch
		self.matchmode=g.getpc(owner).matchmode

def zkloop():
	for t in g.zks:
		if t.beeptimer.elapsed>=t.beeptime and t.exploding==True:
			t.beeptimer.restart()
			g.play("semtexactivate",t.x,t.y,t.z,t.map)
#			for p in g.players:
#				if get_3d_distance(t.x,t.y,t.z,p.x,p.y,p.z)<=t.range and t.map==p.map:
#					g.n.send_reliable(p.peer_id,"distsound zkbeep "+str(t.x)+" "+str(t.y)+" "+str(t.z)+" "+str(t.map),0)

		if t.checktimer.elapsed>=1000:
			t.checktimer.restart()
			if not file_exists("maps/"+t.map+".map"):
				g.zks.remove(t)
				return
		if t.explodetimer.elapsed>=t.explodetime and t.codefound==True:
			t.codefound=False
			t.explodetimer.restart()
			t.exploding=False
			for i in g.players:
				if i.dead: continue
				if (i.map==t.map or i.specmap==t.map):
					g.n.send_reliable(i.peer_id,"distsound planebomblounchdist "+str(t.x)+" "+str(t.y)+" "+str(t.z)+" "+str(t.map),0)
					g.n.send_reliable(i.peer_id,"distsound grenadesomethingexplode "+str(t.x)+" "+str(t.y)+" "+str(t.z)+" "+str(t.map),0)

			_zk_boss = getattr(g, "mega_boss", None)
			for p in g.players:
				if p.hidden: continue
				if get_3d_distance(t.x,t.y,t.z,p.x,p.y,p.z)<=t.range and t.map==p.map:
					if (t.map == "megaboss" and t.owner != p.name
							and (_zk_boss is None or _zk_boss.health > 2500)):
						continue
					p.playsound("planebombhit")
					inpact=random(t.mindammage, t.maxdammage)
					p.health-=inpact
					p.hitby=""+t.owner+"'s zk"
			for i in range(len(g.npcs)):
				if g.npcs[i].matchmode=="teamz" and t.joinedmatch==g.npcs[i].joinedmatch and g.get_tile_at(t.x, t.y, 0, t.map)!="hardwood": continue
				if g.npcs[i].fulldied or g.npcs[i].name==t.owner: continue
				if g.npcs[i].joinedmatch==t.joinedmatch and t.joinedmatch!="" and g.npcs[i].matchteam==t.matchteam and t.matchmode!="g" and t.matchmode!="g2" and t.matchmode!="teaml" and t.matchmode!="minecraft":
					continue
				if not has_line_of_sight(t.x,t.y,t.z,g.npcs[i].x,g.npcs[i].y,g.npcs[i].z,t.map): continue
				if g.npcs[i].map==t.map and get_3d_distance(t.x, t.y, t.z, g.npcs[i].x, g.npcs[i].y, g.npcs[i].z)<=t.range and g.npcs[i].map==t.map and g.npcs[i].health>0:
					inpact=random(t.mindammage, t.maxdammage)
					g.npcs[i].health-=inpact
					g.npcs[i].trackwho=2
					if g.npcs[i].hitattack==True:
						g.npcs[i].attack=True
					if g.npcs[i].painsoundamount>0:
						g.play(g.npcs[i].painsound+str(random(1,g.npcs[i].painsoundamount)), g.npcs[i].x, g.npcs[i].y, g.npcs[i].z, g.npcs[i].map)
					else:
						g.play(g.npcs[i].painsound, g.npcs[i].x, g.npcs[i].y, g.npcs[i].z, g.npcs[i].map)
					g.play("planebombhit",g.npcs[i].x,g.npcs[i].y,g.npcs[i].z,g.npcs[i].map,g.npcs[i])
					if g.npcs[i].hitby!=t.owner:
						g.npcs[i].hitby=t.owner
						g.npcs[i].hitby2=t.owner
			for i in range(len(g.zombies)):
				if not has_line_of_sight(t.x,t.y,t.z,g.zombies[i].x,g.zombies[i].y,g.zombies[i].z,t.map): continue
				if g.zombies[i].map==t.map and get_3d_distance(t.x, t.y, t.z, g.zombies[i].x, g.zombies[i].y, g.zombies[i].z)<=t.range and g.zombies[i].map==t.map and g.zombies[i].health>0:
					inpact=random(t.mindammage, t.maxdammage)
					g.zombies[i].health-=inpact
					g.play("zombiehurt", g.zombies[i].x, g.zombies[i].y, g.zombies[i].z, g.zombies[i].map)
					g.zombies[i].mode=1
					g.play("planebombhit",g.zombies[i].x,g.zombies[i].y,g.zombies[i].z,g.zombies[i].map,g.zombies[i])
			for wall in g.maps[g.get_map_index(t.map)].mapwalls:
				if wall.health<=0: continue
				for wx in range(wall.minx,wall.maxx+1):
					for wy in range(wall.miny,wall.maxy+1):
						for wz in range(wall.minz,wall.maxz+1):
							if wall not in t.hitwalls and get_3d_distance(t.x, t.y, t.z, wx, wy, wz)<=t.range:
				
								inpact=random(t.mindammage,t.maxdammage)
								wall.destroyed=False
								wall.health-=inpact
								t.hitwalls.append(wall)
								if wall.health>0: g.play("walldoor",t.x,t.y,t.z,t.map)
								if wall.health<=0: g.play("walldestroy",wx,wy,wz,t.map)
			for mwall in g.mwalls:
				if mwall.map!=t.map: continue
				if mwall.health<=0: continue
				for wx in range(mwall.minx,mwall.maxx+1):
					for wy in range(mwall.miny,mwall.maxy+1):
						for wz in range(mwall.minz,mwall.maxz+1):
							if mwall not in t.hitmwalls and get_3d_distance(t.x, t.y, t.z, wx, wy, wz)<=t.range:
				
								inpact=random(t.mindammage,t.maxdammage)
								mwall.health-=inpact
								t.hitmwalls.append(mwall)
								if mwall.health>0: g.play("walldoor",t.x,t.y,t.z,t.map)
								if mwall.health<=0: g.play("walldestroy",t.x,t.y,t.z,t.map)
			for barricade in g.barricades:
				if barricade.map!=t.map: continue
				if barricade.health<=0: continue
				for wx in range(barricade.minx,barricade.maxx+1):
					for wy in range(barricade.miny,barricade.maxy+1):
						for wz in range(barricade.minz,barricade.maxz+1):
							if barricade not in t.hitbarricades and get_3d_distance(t.x, t.y, t.z, wx, wy, wz)<=t.range:
				
								inpact=random(t.mindammage,t.maxdammage)
								barricade.health-=inpact
								t.hitbarricades.append(barricade)
								if barricade.health>0: g.play("wallhit"+str(random(3,9)),t.x,t.y,t.z,t.map)
								if barricade.health<=0: g.play("walldestroy5",t.x,t.y,t.z,t.map); barricade.remove_platform(); g.barricades.remove(barricade)
			for ladder in g.ladders:
				if ladder.map!=t.map: continue
				if ladder.health<=0: continue
				for wx in range(ladder.minx,ladder.maxx+1):
					for wy in range(ladder.miny,ladder.maxy+1):
						for wz in range(ladder.minz,ladder.maxz+1):
							if ladder not in t.hitladders and get_3d_distance(t.x, t.y, t.z, wx, wy, wz)<=t.range:
				
								inpact=random(t.mindammage,t.maxdammage)
								ladder.health-=inpact
								t.hitladders.append(ladder)
								if ladder.health<=0: g.play("ladder_collapse",t.x,t.y,t.z,t.map); ladder.remove_platform(); g.ladders.remove(ladder)


			for m in g.chests:
				if string_contains(t.map,"base",1)>-1: continue
				if get_3d_distance(t.x,t.y,t.z,m.x,m.y,m.z)<=t.range and t.map==m.map:
					g.play("wallfence6",m.x,m.y,m.z,m.map)
					inpact=random(t.mindammage, t.maxdammage)
					m.health-=inpact
					if m.health<=0 and g.task==3 and g.getpc(t.owner) is not None and g.getpc(t.owner).task_data[3]<15:
						g.getpc(t.owner).eventpoint+=10; g.getpc(t.owner).currenteventpoint+=10; g.n.send_reliable(g.getpc(t.owner).peer_id,"you got 10 event points",2); g.getpc(t.owner).task_data[3]+=1
					if m.health<=0 and g.task==3 and g.getpc(t.owner).task_data[3]>=15:
						g.getpc(t.owner).currenteventpoint+=10


			for m in g.electrics:
				if get_3d_distance(t.x,t.y,t.z,m.x,m.y,m.z)<=t.range and t.map==m.map:
					g.play("h"+str(random(1,6)),m.x,m.y,m.z,m.map)
					inpact=random(t.mindammage, t.maxdammage)
					m.health-=inpact

			g.zks.remove(t)
			return
def place_zk(x,y,z,map,owner,code):
	place=zk(x,y,z,map,owner,code)
	g.zks.append(place)
def has_line_of_sight(start_x, start_y, start_z, end_x, end_y, end_z, map):
    return True
    # Implement a simple ray-casting algorithm
    steps = max(abs(end_x - start_x), abs(end_y - start_y), abs(end_z - start_z))
    if steps == 0:
        return True

    dx = (end_x - start_x) / steps
    dy = (end_y - start_y) / steps
    dz = (end_z - start_z) / steps

    x, y, z = start_x, start_y, start_z

    for _ in range(int(steps)):
        x += dx
        y += dy
        z += dz
        if "wall" in get_tile_at(int(x), int(y), int(z), map):
            return False
    return True