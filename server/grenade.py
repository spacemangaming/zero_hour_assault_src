from rotation import get_3d_distance
from variable_management import string_contains
from map import get_tile_at
from file_directories import file_exists
from rotation import move
from vector import vector
from timer import timer
import globals as g
from random import randint as random
class grenade:
	def __init__(self,x,y,z,map,owner,dir):
		self.x=x
		self.y=y
		self.checktimer=timer()
		self.z=z
		self.hitwalls=[]
		self.hitmwalls=[]
		self.hitbarricades=[]
		self.hitladders=[]
		self.map=map
		self.owner=owner
		self.explodetimer=timer()
		self.explodetime=2000
		self.dir=dir
		self.speedtimer=timer()
		self.speedtime=30
		self.stopmoving=False
		self.range=10
		self.mindammage=40
		self.maxdammage=110
		self.distance=0
	def playsound(self, snd):
		g.play(snd,self.x,self.y,self.z,self.map)
	def distancecheck(self, xx, yy, zz):
		return get_3d_distance(self.x, self.y, self.z, xx, yy, zz)
def grenadeloop():
	for j in g.grenades:

		if j.checktimer.elapsed>1000:
			j.checktimer.restart()
			if not file_exists("maps/"+j.map+".map"):
				g.grenades.remove(j)
				return
		if j.speedtimer.elapsed>j.speedtime and not j.stopmoving:
			j.speedtimer.restart()
			wr=move(j.x, j.y, j.z, j.dir, 0, 0, 0)
			max=get_max_values(j.map)
			j.x=wr.x
			j.y=wr.y
			j.distance+=1
			if j.distance>=30: j.stopmoving=True; j.playsound("grenadedrop"+str(random(1,3))); return
			if j.x<0 or j.y<0: j.stopmoving=True; j.playsound("grenadedrop"+str(random(1,3))); return
			if j.x>=max.x and j.y>=max.y: j.stopmoving=True; j.playsound("grenadedrop"+str(random(1,3))); return
			if "wall" in get_tile_at(j.x, j.y, j.z, j.map): j.stopmoving=True; j.playsound("grenadedrop"+str(random(1,3))); return
			for wall in g.mwalls:
				if wall.destroyed or wall.map!=j.map: continue
				for wx in range(wall.minx,wall.maxx+1):
					for wy in range(wall.miny,wall.maxy+1):
						for wz in range(wall.minz,wall.maxz+1):
							if get_3d_distance(j.x,j.y,j.z,wx,wy,wz)<=3 and j.map==wall.map: j.playsound("grenadedrop"+str(random(1,3))); j.stopmoving=True; return
			for wall in g.barricades:
				if wall.destroyed or wall.map!=j.map: continue
				for wx in range(wall.minx,wall.maxx+1):
					for wy in range(wall.miny,wall.maxy+1):
						for wz in range(wall.minz,wall.maxz+1):
							if get_3d_distance(j.x,j.y,j.z,wx,wy,wz)<=3 and j.map==wall.map: j.playsound("grenadedrop"+str(random(1,3))); j.stopmoving=True; return
			for wall in g.ladders:
				if wall.destroyed or wall.map!=j.map: continue
				for wx in range(wall.minx,wall.maxx+1):
					for wy in range(wall.miny,wall.maxy+1):
						for wz in range(wall.minz,wall.maxz+1):
							if get_3d_distance(j.x,j.y,j.z,wx,wy,wz)<=3 and j.map==wall.map: j.playsound("grenadedrop"+str(random(1,3))); j.stopmoving=True; return


			for m in g.motors:
				if get_3d_distance(j.x,j.y,j.z,m.x,m.y,m.z)<=3 and j.map==m.map: j.playsound("grenadedrop"+str(random(1,3))); j.stopmoving=True; return
			for m in g.chests:
				if string_contains(j.map,"base",1)>-1: continue
				if get_3d_distance(j.x,j.y,j.z,m.x,m.y,m.z)<=1 and j.map==m.map: j.playsound("grenadedrop"+str(random(1,3))); j.stopmoving=True; return
			for m in g.electrics:
				if get_3d_distance(j.x,j.y,j.z,m.x,m.y,m.z)<=1 and j.map==m.map: j.playsound("grenadedrop"+str(random(1,3))); j.stopmoving=True; return

			for m in g.corpses:
				if get_3d_distance(j.x,j.y,j.z,m.x,m.y,m.z)<=1 and j.map==m.map: j.playsound("grenadedrop"+str(random(1,3))); j.stopmoving=True; return


			for m in g.npcs:
				if get_3d_distance(j.x,j.y,j.z,m.x,m.y,m.z)<=3 and j.map==m.map: j.playsound("grenadedrop"+str(random(1,3))); j.stopmoving=True; return
			for m in g.players:

				if j.map!="massacre_in_the_city" and m.joinedmatch==j.owner.joinedmatch and j.owner.joinedmatch!="" and m.matchteam==j.owner.matchteam and j.owner.matchmode!="teaml"  and j.owner.matchmode!="minecraft"  and j.owner.matchmode!="g" and j.owner.matchmode!="g2" and m.joinedmatch!="" and m.matchmode!="" and j.owner.matchmode!="": continue
				if m.vi==j.owner.vi and j.owner.vi!=-1 and m.vi!=-1: continue
				if m.matchmode=="teamz" and j.owner.joinedmatch==m.joinedmatch and g.get_tile_at(j.x, j.y, 0, j.map)!="hardwood": continue
				if(m.dead):
					continue
				if m.name!=j.owner.name and get_3d_distance(j.x,j.y,j.z,m.x,m.y,m.z)<=3 and j.map==m.map: j.playsound("grenadedrop"+str(random(1,3))); j.stopmoving=True; return
		if j.explodetimer.elapsed>j.explodetime:
			j.explodetimer.restart()
			j.playsound("grenadeexplode")
			for i in g.players:
				if i.dead: continue
				if(i.map==j.map or i.specmap==j.map):

					g.n.send_reliable(i.peer_id,"distsound grenadeexplodedist "+str(j.x)+" "+str(j.y)+" "+str(j.z)+" "+str(j.map),0)
			for i in range(len(g.motors)):
				if len(g.motors[i].players)!=0: continue
				oi=g.get_player_index_from(g.motors[i].owner)
				if oi>-1 and g.players[oi].matchteam!="" and g.players[oi].matchteam==j.owner.matchteam: continue
				if oi>-1 and g.players[oi].name==g.motors[i].owner: continue
				if not has_line_of_sight(j.x,j.y,j.z,g.motors[i].x,g.motors[i].y,g.motors[i].z,j.map): continue
				if g.motors[i].map==j.map and get_3d_distance(j.x, j.y, j.z, g.motors[i].x, g.motors[i].y, g.motors[i].z)<=j.range and g.motors[i].map==j.map and g.motors[i].health>0:
					inpact=random(j.mindammage, j.maxdammage)
					g.motors[i].health-=inpact
					g.play("bulletmotorhit"+str(random(1,8)), g.motors[i].x, g.motors[i].y, g.motors[i].z, g.motors[i].map)
					g.motors[i].hitby=j.owner.name
			for i in range(len(g.transits)):
				if g.transits[i].map!=j.map: continue
				if not has_line_of_sight(j.x,j.y,j.z,g.transits[i].x,g.transits[i].y,g.transits[i].z,j.map): continue
				dist_2d=get_3d_distance(j.x, j.y, 0, g.transits[i].x, g.transits[i].y, 0)
				if dist_2d<=j.range and 0<=j.z<=g.transits[i].z+5 and g.transits[i].health>0:
					inpact=random(j.mindammage, j.maxdammage)
					g.transits[i].take_damage(inpact, j.owner)
					g.play("bulletmotorhit"+str(random(1,8)), g.transits[i].x, g.transits[i].y, g.transits[i].z, g.transits[i].map)
			for i in range(len(g.chests)):
				if string_contains(j.map,"base",1)>-1: continue
				if not has_line_of_sight(j.x,j.y,j.z,g.chests[i].x,g.chests[i].y,g.chests[i].z,j.map): continue
				if g.chests[i].map==j.map and get_3d_distance(j.x, j.y, j.z, g.chests[i].x, g.chests[i].y, g.chests[i].z)<=j.range and g.chests[i].map==j.map and g.chests[i].health>0:
					inpact=random(j.mindammage, j.maxdammage)
					g.chests[i].health-=inpact
					g.play("bulletmotorhit"+str(random(1,8)), g.chests[i].x, g.chests[i].y, g.chests[i].z, g.chests[i].map)
					if g.chests[i].health<=0 and g.task==3 and j.owner.task_data[3]<15:
						j.owner.eventpoint+=10; j.owner.currenteventpoint+=10; g.n.send_reliable(j.owner.peer_id,"you got 10 event points",2); j.owner.task_data[3]+=1
					if g.chests[i].health<=0 and g.task==3 and j.owner.task_data[3]>=15:
						j.owner.currenteventpoint+=10

			for i in range(len(g.electrics)):
				if not has_line_of_sight(j.x,j.y,j.z,g.electrics[i].x,g.electrics[i].y,g.electrics[i].z,j.map): continue
				if g.electrics[i].map==j.map and get_3d_distance(j.x, j.y, j.z, g.electrics[i].x, g.electrics[i].y, g.electrics[i].z)<=j.range and g.electrics[i].map==j.map and g.electrics[i].health>0:
					inpact=random(j.mindammage, j.maxdammage)
					g.electrics[i].health-=inpact
					g.play("h"+str(random(1,6)), g.electrics[i].x, g.electrics[i].y, g.electrics[i].z, g.electrics[i].map)

			for i in range(len(g.npcs)):
				if g.npcs[i].matchmode=="teamz" and j.owner.joinedmatch==g.npcs[i].joinedmatch and g.get_tile_at(j.x, j.y, 0, j.map)!="hardwood": continue
				if g.npcs[i].fulldied or g.npcs[i].name==j.owner.name: continue
				if g.npcs[i].joinedmatch==j.owner.joinedmatch and j.owner.joinedmatch!="" and g.npcs[i].matchteam==j.owner.matchteam and j.owner.matchmode!="g" and j.owner.matchmode!="g2" and j.owner.matchmode!="teaml" and j.owner.matchmode!="minecraft":
					continue
				if not has_line_of_sight(j.x,j.y,j.z,g.npcs[i].x,g.npcs[i].y,g.npcs[i].z,j.map): continue
				if g.npcs[i].map==j.map and get_3d_distance(j.x, j.y, j.z, g.npcs[i].x, g.npcs[i].y, g.npcs[i].z)<=j.range and g.npcs[i].map==j.map and g.npcs[i].health>0:
					inpact=random(j.mindammage, j.maxdammage)
					g.npcs[i].health-=inpact
					g.npcs[i].trackwho=1 if not j.owner.isbot else 2
					if g.npcs[i].hitattack==True:
						g.npcs[i].attack=True
					if g.npcs[i].painsoundamount>0:
						g.play(g.npcs[i].painsound+str(random(1,g.npcs[i].painsoundamount)), g.npcs[i].x, g.npcs[i].y, g.npcs[i].z, g.npcs[i].map)
					else:
						g.play(g.npcs[i].painsound, g.npcs[i].x, g.npcs[i].y, g.npcs[i].z, g.npcs[i].map)
					g.play("bullet_impact_body"+str(random(1,16)),g.npcs[i].x,g.npcs[i].y,g.npcs[i].z,g.npcs[i].map,g.npcs[i])
					if g.npcs[i].hitby!=j.owner.name:
						g.npcs[i].hitby=j.owner.name
						if not j.owner.isbot: 						g.npcs[i].hitby2=j.owner.name
					# g.npcs[i].playsound2("hit")
			for i in range(len(g.zombies)):
				if not has_line_of_sight(j.x,j.y,j.z,g.zombies[i].x,g.zombies[i].y,g.zombies[i].z,j.map): continue
				if g.zombies[i].map==j.map and get_3d_distance(j.x, j.y, j.z, g.zombies[i].x, g.zombies[i].y, g.zombies[i].z)<=j.range and g.zombies[i].map==j.map and g.zombies[i].health>0:
					inpact=random(j.mindammage, j.maxdammage)
					g.zombies[i].health-=inpact
					g.play("zombiehurt", g.zombies[i].x, g.zombies[i].y, g.zombies[i].z, g.zombies[i].map)
					if j.owner.isbot: g.zombies[i].mode=2
					if not j.owner.isbot: g.zombies[i].mode=1
					g.play("bullet_impact_body"+str(random(1,16)),g.zombies[i].x,g.zombies[i].y,g.zombies[i].z,g.zombies[i].map,g.zombies[i])
			for wall in g.maps[g.get_map_index(j.map)].mapwalls:
				if wall.health<=0: continue
				for wx in range(wall.minx,wall.maxx+1):
					for wy in range(wall.miny,wall.maxy+1):
						for wz in range(wall.minz,wall.maxz+1):
							if wall not in j.hitwalls and get_3d_distance(j.x, j.y, j.z, wx, wy, wz)<=j.range:
				
								inpact=random(j.mindammage,j.maxdammage)
								wall.destroyed=False
								wall.health-=inpact
								j.hitwalls.append(wall)
								if wall.health>0: g.play("walldoor",j.x,j.y,j.z,j.map)
								if wall.health<=0: g.play("walldestroy",wx,wy,wz,j.map)
			for mwall in g.mwalls:
				if mwall.map!=j.map: continue
				if mwall.health<=0: continue
				for wx in range(mwall.minx,mwall.maxx+1):
					for wy in range(mwall.miny,mwall.maxy+1):
						for wz in range(mwall.minz,mwall.maxz+1):
							if mwall not in j.hitmwalls and get_3d_distance(j.x, j.y, j.z, wx, wy, wz)<=j.range:
				
								inpact=random(j.mindammage,j.maxdammage)
								mwall.health-=inpact
								j.hitmwalls.append(mwall)
								if mwall.health>0: g.play("walldoor",j.x,j.y,j.z,j.map)
								if mwall.health<=0: g.play("walldestroy",j.x,j.y,j.z,j.map)
			for barricade in g.barricades:
				if barricade.map!=j.map: continue
				if barricade.health<=0: continue
				for wx in range(barricade.minx,barricade.maxx+1):
					for wy in range(barricade.miny,barricade.maxy+1):
						for wz in range(barricade.minz,barricade.maxz+1):
							if barricade not in j.hitbarricades and get_3d_distance(j.x, j.y, j.z, wx, wy, wz)<=j.range:
				
								inpact=random(j.mindammage,j.maxdammage)
								barricade.health-=inpact
								j.hitbarricades.append(barricade)
								if barricade.health>0: g.play("wallhit"+str(random(3,9)),j.x,j.y,j.z,j.map)
								if barricade.health<=0: g.play("walldestroy5",j.x,j.y,j.z,j.map); barricade.remove_platform(); g.barricades.remove(barricade)
			for ladder in g.ladders:
				if ladder.map!=j.map: continue
				if ladder.health<=0: continue
				for wx in range(ladder.minx,ladder.maxx+1):
					for wy in range(ladder.miny,ladder.maxy+1):
						for wz in range(ladder.minz,ladder.maxz+1):
							if ladder not in j.hitladders and get_3d_distance(j.x, j.y, j.z, wx, wy, wz)<=j.range:
				
								inpact=random(j.mindammage,j.maxdammage)
								ladder.health-=inpact
								j.hitladders.append(ladder)
								if ladder.health<=0: g.play("ladder_collapse",j.x,j.y,j.z,j.map); ladder.remove_platform(); g.ladders.remove(ladder)


			for x in range(len(g.players)):
				#if x>len(g.players)-1: break
				if g.players[x].hidden: continue
				if g.players[x].vi==j.owner.vi and j.owner.vi!=-1 and g.players[x].vi!=-1: continue
				if g.players[x].matchmode=="teamz" and j.owner.joinedmatch==g.players[x].joinedmatch and g.get_tile_at(j.x, j.y, 0, j.map)!="hardwood": continue
				if(g.players[x].dead):
					continue
				if not has_line_of_sight(j.x,j.y,j.z,g.players[x].x,g.players[x].y,g.players[x].z,j.map): continue
				if(g.players[x].map==j.map and get_3d_distance(j.x, j.y, j.z, g.players[x].x, g.players[x].y, g.players[x].z)<=j.range and g.players[x].map==j.map):
				
					if j.map!="massacre_in_the_city" and g.players[x].joinedmatch==j.owner.joinedmatch and j.owner.joinedmatch!="" and g.players[x].matchteam==j.owner.matchteam and j.owner.matchmode!="teaml"  and j.owner.matchmode!="minecraft"  and j.owner.matchmode!="g" and j.owner.matchmode!="g2" and g.players[x].joinedmatch!="" and g.players[x].matchmode!="" and j.owner.matchmode!="": continue
					inpact=random(j.mindammage,j.maxdammage)
					if g.players[x].vi!=-1:
						r=random(1,4)
						if r!=1:
							g.play("bulletmotorhit"+str(random(1,8)),j.x,j.y,j.z,j.map)						
							g.motors[g.players[x].vi].health-=inpact
							break
						else:
							r2=random(0,len(g.motors[g.players[x].vi].players)-1)
							x=g.get_player_index_from(g.motors[g.players[x].vi].players[r2])
					if not g.players[x].shielded:
						g.players[x].hitby=j.owner.name+"'s grenade"
						if not j.owner.isbot: 						g.players[x].hitby2=j.owner.name
					if g.players[x].shielded==True:
						g.players[x].shieldhitchance=0
					else:
						g.players[x].health-=inpact
						g.play("swordbighit",g.players[x].x,g.players[x].y,g.players[x].z,g.players[x].map,g.players[x])
						g.players[x].play_hit_sound()
			g.grenades.remove(j)
def launch_grenade(x,y,z,map,owner,dir):
	if map=="lobby": return
	gr=grenade(x,y,z,map,owner,dir)
	g.grenades.append(gr)
def get_max_values(mapname):
	ind=g.get_map_index(mapname)
	temp=vector()
	if ind<0:
		return temp
	temp.x=g.maps[ind].max.x
	temp.y=g.maps[ind].max.y
	temp.z=g.maps[ind].max.z
	return temp
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