from rotation import get_3d_distance, find_appropriate_facing
from variable_management import string_contains
from moving_sound_serverside_handler import update_moving_sound, destroy_moving_sound
from rotation import move
from vector import vector
from timer import timer
from moving_sound_serverside_handler import update_moving_sound, destroy_moving_sound
import globals as g
from random import randint as random
from item import spawn_item
from molotof import spawn_molotof
import data_loader

class weapon:
	def __init__(self, bx, by, bz, bdir, btype, bmap,p):
		self.x=0;self.y=0;self.z=0
		self.netlooptimer=timer()
		self.dir=0
		self.msounds=[]
		self.msoundtimers=[]
		self.oldx=0
		self.oldy=0
		self.oldz=0

		self.whiztimer=timer()
		self.whiztimer.elapsed=1500
		self.type=""
		self.speedtimer=timer()
		self.name="just_a_bullet"
		self.speedtime=0
		self.oldx=0
		self.oldy=0
		self.oldz=0
		self.range=0
		self.distance=0
		self.mindammage=50
		self.maxdammage=1000
		self.map=""
		self.owner=None
		self.spread=0
		self.bullet=False
		self.x=bx
		self.y=by
		self.z=bz
		self.startz=bz
		self.dir=bdir
		self.type=btype
		self.owner=p
		if "thrown" not in self.type and p.aim_mode==0: self.z+=p.aim
		self.map=bmap

		# ── data-driven stat lookup ───────────────────────────────────────────
		base_type = self.type.replace("thrown_", "") if "thrown" in self.type else self.type
		wdata = data_loader.get_weapon(base_type)

		if wdata:
			self.bullet = wdata.get("bullet", False)
			self.range = wdata.get("range", 0)
			self.mindammage = wdata.get("min_damage", 0)
			self.maxdammage = wdata.get("max_damage", 0)
			self.spread = wdata.get("spread", 3)
			self.speedtime = 1  # default; overridden below for special cases

			# thrown-weapon overrides
			if "thrown" in self.type and wdata.get("thrown"):
				td = wdata["thrown"]
				self.bullet = False
				self.range = td.get("range", 20)
				self.mindammage = td.get("min_damage", 50)
				self.maxdammage = td.get("max_damage", 130)
				self.speedtime = td.get("speedtime", 37)
				self.spread = td.get("spread", 3)

			# snowflake shard: map-dependent damage
			if self.type == "snowflake_shard":
				if "snow" not in bmap:
					self.mindammage = 0
					self.maxdammage = 0
				self.speedtime = 4

			# feet / punch have speedtime=5 in original code
			if self.type in ("feet", "punch"):
				self.speedtime = 5

			# test weapon speedtime=5
			if self.type == "test":
				self.speedtime = 5
		else:
			# Unknown weapon — safe defaults
			self.bullet = False
			self.range = 0
			self.mindammage = 0
			self.maxdammage = 0
			self.spread = 3
			self.speedtime = 1

		self.mindammage += self.owner.plusdammage
		self.maxdammage += self.owner.plusdammage
		if "thrown" not in self.type and self.type in self.owner.silenced: self.range //= 2
		if "thrown" in self.type: g.playmoving(self.x, self.y, self.z, self.map, "misc299", self)
		if self.owner.aim_mode==1 and self.owner.aim==1 or self.owner.aim_mode==1 and self.owner.aim==-1: self.range //= 2; self.spread -= 1

	def msoundloop(self):
		for i in range(len(self.msoundtimers)):
			if self.msoundtimers[i].elapsed>=9000:
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

	def get_ground_z(self):
		ret=self.z
		while ret>-1000 and g.get_tile_at(self.x,self.y,ret,self.map)=="": ret-=1
		return ret
def _play_bulletfall(weapon_obj):
	"""Play the bullet-fall sound for weapon_obj based on its configured bulletfall range."""
	base_type = weapon_obj.type.replace("thrown_", "") if "thrown" in weapon_obj.type else weapon_obj.type
	wdata = data_loader.get_weapon(base_type)
	bf_min = wdata.get("bulletfall_min") if wdata else None
	bf_max = wdata.get("bulletfall_max") if wdata else None
	if bf_min is not None and bf_max is not None:
		g.play_delay(
			"bulletfall" + str(random(bf_min, bf_max)),
			weapon_obj.x, weapon_obj.y, weapon_obj.get_ground_z(),
			weapon_obj.map, 1000
		)


def weaponloop():
	for j in range(len(g.weapons)):
		g.weapons[j].msoundloop()
		if(g.weapons[j].speedtimer.elapsed>=g.weapons[j].speedtime):
		
			g.weapons[j].speedtimer.restart()

			wr=vector()
			wr=move(g.weapons[j].x, g.weapons[j].y, g.weapons[j].z, g.weapons[j].dir, 0, 0, 0)
			#if "thrown" not in g.weapons[j].type and g.weapons[j].owner.aim>=20: g.weapons[j].z+=1
			#elif "thrown" not in g.weapons[j].type and g.weapons[j].owner.aim<=-20: g.weapons[j].z-=1
			if g.weapons[j].owner.aim_mode==1:
				if g.weapons[j].owner.aim!=2 and g.weapons[j].owner.aim!=-2:
					g.weapons[j].x=wr.x
					g.weapons[j].y=wr.y
				if g.weapons[j].owner.aim==2 or g.weapons[j].owner.aim==1: g.weapons[j].z+=1
				if g.weapons[j].owner.aim==-2 or g.weapons[j].owner.aim==-1: g.weapons[j].z-=1
			else:
				g.weapons[j].x=wr.x
				g.weapons[j].y=wr.y

			rx=g.weapons[j].x
			ry=g.weapons[j].y

			g.weapons[j].distance+=1
			if g.weapons[j].type!="base_gun" and (string_contains(g.get_nwall_at(wr.x, wr.y, g.weapons[j].startz, g.weapons[j].map), "wall", 1)>-1 or string_contains(g.get_nwall_at(wr.x, wr.y, g.weapons[j].z, g.weapons[j].map), "wall", 1)>-1):
			
				if(g.weapons[j].bullet==True):
					g.play("bullet_to_wall"+str(random(1, 4)), wr.x, wr.y, g.weapons[j].z, g.weapons[j].map)
				else:
					g.play(g.weapons[j].type+"rico", wr.x, wr.y, g.weapons[j].z, g.weapons[j].map)
				_play_bulletfall(g.weapons[j])
				if "thrown" in g.weapons[j].type:
					if "sword" in g.weapons[j].type: g.play("sworddrop"+str(random(1,3)),g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
					if "knife" in g.weapons[j].type: g.play("knifedrop",g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
					spawn_item(g.weapons[j].x,g.weapons[j].y,g.weapons[j].get_ground_z(),g.weapons[j].map,g.weapons[j].type.replace("thrown_",""),1,False)
				if g.weapons[j].type=="molotov_cocktail":
					g.play("molotovexplode",g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
					g.n.broadcast("distsound molotovexplode "+str(g.weapons[j].x)+" "+str(g.weapons[j].y)+" "+str(g.weapons[j].z)+" "+g.weapons[j].map+"",0)
					spawn_molotof(g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map,g.weapons[j].owner.name)
				g.weapons.pop(j)
				return
				
			if g.weapons[j].distance > g.weapons[j].range:
			
				if g.weapons[j].x<0: g.weapons[j].x=0
				if g.weapons[j].y<0: g.weapons[j].y=0
				if g.weapons[j].type=="molotov_cocktail":
					g.play("molotovexplode",g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
					g.n.broadcast("distsound molotovexplode "+str(g.weapons[j].x)+" "+str(g.weapons[j].y)+" "+str(g.weapons[j].z)+" "+g.weapons[j].map+"",0)
					spawn_molotof(g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map,g.weapons[j].owner.name)
				_play_bulletfall(g.weapons[j])
				if "thrown" in g.weapons[j].type:
					if "sword" in g.weapons[j].type: g.play("sworddrop"+str(random(1,3)),g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
					if "knife" in g.weapons[j].type: g.play("knifedrop",g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
					spawn_item(g.weapons[j].x,g.weapons[j].y,g.weapons[j].get_ground_z(),g.weapons[j].map,g.weapons[j].type.replace("thrown_",""),1,False)
				g.weapons.pop(j)
				return
				
			hit=False
			for i in range(len(g.motors)):
				if g.motors[i].map!=g.weapons[j].map: continue
				if len(g.motors[i].players)!=0: continue
				oi=g.get_player_index_from(g.motors[i].owner)
				if oi>-1 and g.players[oi].matchteam!="" and g.players[oi].matchteam==g.weapons[j].owner.matchteam: continue
				#if oi>-1 and g.players[oi].name==g.motors[i].owner: continue
				dist=get_3d_distance(rx, ry, g.weapons[j].z, g.motors[i].x, g.motors[i].y, g.motors[i].z)
				if g.weapons[j].whiztimer.elapsed>=1500 and g.motors[i].map==g.weapons[j].map and g.weapons[j].bullet and dist>g.weapons[j].spread and dist<=15 and g.weapons[j].owner!=g.motors[i] :
					g.play("bulletwhiz"+str(random(1,8)),g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
					g.weapons[j].whiztimer.restart()



				if g.motors[i].map==g.weapons[j].map and dist<=g.weapons[j].spread and g.motors[i].map==g.weapons[j].map and g.motors[i].health>0:
					if hit==False:
						hit=True
					inpact=random(g.weapons[j].mindammage, g.weapons[j].maxdammage)
					g.motors[i].health-=inpact
					if(g.weapons[j].bullet):
						g.play("bulletmotorhit"+str(random(1,8)), g.motors[i].x, g.motors[i].y, g.motors[i].z, g.motors[i].map)
						try: g.n.send_reliable(g.weapons[j].owner.peer_id,"play_s bullethit"+str(random(1,4))+".ogg",0)
						except: pass
						for p in g.players:
							if p.specplayer==g.weapons[j].owner.name:
								g.n.send_reliable(p.peer_id,"play_s bullethit"+str(random(1,4))+".ogg",0)
						_play_bulletfall(g.weapons[j])

					if g.weapons[j].type=="molotov_cocktail":
						g.play("molotovexplode",g.motors[i].x,g.motors[i].y,g.motors[i].z,g.motors[i].map)
						g.n.broadcast("distsound molotovexplode "+str(g.motors[i].x)+" "+str(g.motors[i].y)+" "+str(g.motors[i].z)+" "+g.motors[i].map+"",0)
						_play_bulletfall(g.weapons[j])

#						g.play("bulletfall"+str(random(1,12))+"",g.motors[i].x,g.motors[i].y,g.motors[i].z,g.motors[i].map)
					else: 						g.play("bulletmotorhit"+str(random(1,8)), g.motors[i].x, g.motors[i].y, g.motors[i].z, g.motors[i].map)
					
				

					g.motors[i].hitby=g.weapons[j].owner.name
					break
			for i in range(len(g.transits)):
				if g.transits[i].map!=g.weapons[j].map: continue
				dist_2d=get_3d_distance(rx, ry, 0, g.transits[i].x, g.transits[i].y, 0)
				if dist_2d<=g.weapons[j].spread and 0<=g.weapons[j].z<=g.transits[i].z+5 and g.transits[i].health>0:
					if hit==False:
						hit=True
					inpact=random(g.weapons[j].mindammage, g.weapons[j].maxdammage)
					g.transits[i].take_damage(inpact, g.weapons[j].owner)
					if(g.weapons[j].bullet):
						g.play("bulletmotorhit"+str(random(1,8)), g.transits[i].x, g.transits[i].y, g.transits[i].z, g.transits[i].map)
						try: g.n.send_reliable(g.weapons[j].owner.peer_id,"play_s bullethit"+str(random(1,4))+".ogg",0)
						except: pass
					break
			for x in range(len(g.players)):
				if g.players[x].hidden: continue
				if (g.players[x].map=="massacre_in_the_city" or "basement" in g.players[x].map) and g.get_group(g.players[x].group) is not None and g.players[x].group==g.weapons[j].owner.group and g.get_group(g.players[x].group).freedomhit==0: continue
				if g.players[x].faint: continue
				if g.players[x].vi==g.weapons[j].owner.vi and g.weapons[j].owner.vi!=-1 and g.players[x].vi!=-1: continue
				if g.weapons[j].bullet and g.players[x].ducking and g.weapons[j].owner.aim>-g.weapons[j].spread and not g.weapons[j].owner.ducking:
					if g.weapons[j].whiztimer.elapsed>1500:
						g.play("bulletwhiz"+str(random(1,8)),g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
						g.weapons[j].whiztimer.restart()
					continue
				if g.players[x].matchmode=="teamz" and g.weapons[j].owner.joinedmatch==g.players[x].joinedmatch and g.get_tile_at(rx, ry, 0, g.weapons[j].map)!="hardwood": continue
				if(g.players[x].dead):
					continue
				if g.weapons[j].map==g.players[x].map: dist = get_3d_distance(rx, ry, g.weapons[j].z, g.players[x].x, g.players[x].y, g.players[x].z)
				if g.weapons[j].whiztimer.elapsed>=1500 and g.players[x].map==g.weapons[j].map and g.weapons[j].bullet and dist>g.weapons[j].spread and dist<=15 and g.weapons[j].owner!=g.players[x] and g.players[x].map==g.weapons[j].map :
					g.play("bulletwhiz"+str(random(1,8)),g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
					g.weapons[j].whiztimer.restart()
				if(g.players[x].map==g.weapons[j].map and dist<=g.weapons[j].spread and g.weapons[j].owner.name!=g.players[x].name and g.players[x].map==g.weapons[j].map):
				
					if g.weapons[j].map!="massacre_in_the_city" and g.players[x].joinedmatch==g.weapons[j].owner.joinedmatch and g.weapons[j].owner.joinedmatch!="" and g.players[x].matchteam==g.weapons[j].owner.matchteam and g.weapons[j].owner.matchmode!="teaml"  and g.weapons[j].owner.matchmode!="snow"  and g.weapons[j].owner.matchmode!="sniper"  and g.weapons[j].owner.matchmode!="sword"  and g.weapons[j].owner.matchmode!="teamk2"  and g.weapons[j].owner.matchmode!="teamf2"  and g.weapons[j].owner.matchmode!="minecraft"  and g.weapons[j].owner.matchmode!="g"  and g.weapons[j].owner.matchmode!="collect" and g.weapons[j].owner.matchmode!="g2"  and g.players[x].joinedmatch!="" and g.players[x].matchmode!="" and g.weapons[j].owner.matchmode!="": continue
					if g.weapons[j].type!="base_gun" and not has_line_of_sight(g.weapons[j].x, g.weapons[j].y, g.weapons[j].startz, g.players[x].x, g.players[x].y, g.players[x].z, g.players[x].map): continue

					#if g.weapons[j].map=="massacre_in_the_city" and g.weapons[j].owner.group==g.players[x].group: continue
					tx=g.weapons[j].x
					ty=g.weapons[j].y
					for _ in range(get_weapon_spread(g.weapons[j].type)):
						temp=move(tx, ty, g.weapons[j].z, g.weapons[j].dir, 0, 0, 0)
						tx=temp.x
						ty=temp.y



						if g.weapons[j].type!="base_gun" and string_contains(g.get_nwall_at(temp.x, temp.y, g.weapons[j].startz, g.weapons[j].map), "wall", 1)>-1 or g.weapons[j].type!="base_gun" and string_contains(g.get_nwall_at(temp.x, temp.y, g.weapons[j].z, g.weapons[j].map), "wall", 1)>-1:
			
							if(g.weapons[j].bullet==True):
								g.play("bullet_to_wall"+str(random(1, 4)), temp.x, temp.y, g.weapons[j].z, g.weapons[j].map)
							else:
								g.play(g.weapons[j].type+"rico", temp.x, temp.y, g.weapons[j].z, g.weapons[j].map)
							_play_bulletfall(g.weapons[j])
							if "thrown" in g.weapons[j].type:
								if "sword" in g.weapons[j].type: g.play("sworddrop"+str(random(1,3)),g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
								if "knife" in g.weapons[j].type: g.play("knifedrop",g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
								spawn_item(g.weapons[j].x,g.weapons[j].y,g.weapons[j].get_ground_z(),g.weapons[j].map,g.weapons[j].type.replace("thrown_",""),1,False)
							g.weapons.pop(j)
							return
					hit=True
					inpact=random(g.weapons[j].mindammage,g.weapons[j].maxdammage)
					if g.players[x].vi!=-1:
						r=random(1,4)
						if r!=1:
							g.play("bulletmotorhit"+str(random(1,8)),g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)						
							g.motors[g.players[x].vi].health-=inpact
							break
						else:
							r2=random(0,len(g.motors[g.players[x].vi].players)-1)
							x=g.get_player_index_from(g.motors[g.players[x].vi].players[r2])
					if g.weapons[j].name not in g.weapons[j].owner.silenced: g.players[x].hitby=g.weapons[j].owner.name+"'s "+g.weapons[j].type+""
					if g.weapons[j].name in g.weapons[j].owner.silenced: g.players[x].hitby=g.weapons[j].owner.name+"'s silenced "+g.weapons[j].type+""
					if not g.weapons[j].owner.isbot: 						g.players[x].hitby2=g.weapons[j].owner.name
					if g.weapons[j].type=="base_gun": g.n.send_reliable(g.weapons[j].owner.peer_id,"the base gun hit to the player "+g.players[x].name,0)
					headshot=False
					helmet=False
					if g.weapons[j].bullet:
						if not g.players[x].shielded or (g.players[x].shielded and (g.weapons[j].type=="punch" or g.weapons[j].type=="feet")) and g.weapons[j].owner.aim<=-get_weapon_spread(g.weapons[j].type):
							leg=random(1,15)
							if leg==1:
								if not g.players[x].sitting: g.n.send_reliable(g.players[x].peer_id,"sitstart",0)
								if not g.players[x].sitting: g.players[x].playsound(g.get_tile_at(g.players[x].x,g.players[x].y,g.players[x].z,g.players[x].map)+"fall")
								g.players[x].playsound("leg")
								g.players[x].leghits+=1
								g.weapons[j].owner.legshots+=1
						if g.weapons[j].type!="base_gun" and g.weapons[j].owner.z>=g.players[x].z+2:
							inpact*=2
							headshot=True
							if "flag" not in g.weapons[j].map and hasattr(g.weapons[j].owner,"task_data") and g.task==2 and g.weapons[j].owner.task_data[2]<50: g.weapons[j].owner.task_data[2]+=1; g.weapons[j].owner.eventpoint+=1; g.weapons[j].owner.playsound("misc294"); g.weapons[j].owner.currenteventpoint+=1; g.n.send_reliable(g.weapons[j].owner.peer_id,"you got 1 event point",0)
							if "flag" not in g.weapons[j].map and hasattr(g.weapons[j].owner,"task_data") and g.task==2 and g.weapons[j].owner.task_data[2]>=50: g.weapons[j].owner.currenteventpoint+=1

							if g.players[x].helmethitchance>0: helmet=True

							try:
								if not helmet:
									g.players[x].headhits+=1
									g.weapons[j].owner.headshots+=1
									g.weapons[j].owner.send_bulletbody()

								else: g.weapons[j].owner.playsound("bullethelmethit"+str(random(1,2)))
							except: pass
						else:
							try:
								if not g.players[x].shielded or (g.players[x].shielded and (g.weapons[j].type=="punch" or g.weapons[j].type=="feet")):
									g.weapons[j].owner.send_bulletbody2()
								if g.players[x].shielded and (g.weapons[j].type!="punch" and g.weapons[j].type!="feet"):
									try: g.n.send_reliable(g.weapons[j].owner.peer_id,"play_s metal_shield"+str(random(1,2))+".ogg",0)
									except: pass
							except: pass

					if not headshot and g.players[x].shielded and (g.weapons[j].type!="punch" and g.weapons[j].type!="feet"): g.players[x].shieldhitchance-=inpact
					else:
						if headshot and g.players[x].helmethitchance>0:
							g.players[x].helmethitchance-=inpact/2
						else:
							g.players[x].health-=inpact
							sit=random(1,20)
							if sit==1 and headshot and g.players[x].shielded==False:
								if not g.players[x].sitting: g.n.send_reliable(g.players[x].peer_id,"sitstart",0)
							if sit==1 and headshot and g.players[x].shielded==False:
								if not g.players[x].sitting: g.players[x].playsound(g.get_tile_at(g.players[x].x,g.players[x].y,g.players[x].z,g.players[x].map)+"fall")

					if not g.players[x].cannotexit:
						g.n.send_reliable(g.players[x].peer_id,"cannotexit",0)
						g.players[x].cannotexit=True
						g.players[x].cannotexittimer.restart()
					if g.weapons[j].map=="massacre_in_the_city" and g.weapons[j].owner.group==g.players[x].group: g.weapons[j].owner.playsound("beep3")
					if(g.weapons[j].bullet):
						if headshot or not g.players[x].shielded or (g.players[x].shielded and (g.weapons[j].type=="punch" or g.weapons[j].type=="feet")):
							if headshot and helmet: g.players[x].playsound("bullethelmethit"+str(random(1,2)))
							else:
								if not headshot: g.players[x].playsound("bullet_impact_body"+str(random(1,16)))
								if headshot: g.players[x].playsound("bullet_impact_body"+str(random(1,2)))
							if not helmet and (not g.players[x].shielded or (g.players[x].shielded and (g.weapons[j].type=="punch" or g.weapons[j].type=="feet"))): g.players[x].play_hit_sound()
						else:
							g.players[x].playsound("metal_shield"+str(random(1,2)))
						_play_bulletfall(g.weapons[j])
					if headshot or not g.players[x].shielded or (g.players[x].shielded and (g.weapons[j].type=="punch" or g.weapons[j].type=="feet")):
						if g.weapons[j].type=="snowflake_shard":
							g.players[x].playsound("snowhit"+str(random(1,2)))
							g.players[x].stunned=True
							g.players[x].stuntime=3000
							g.players[x].stuntimer.restart()
							g.n.send_reliable(g.players[x].peer_id,"stopmoving",0)
					if g.weapons[j].bullet:
						_play_bulletfall(g.weapons[j])


					if g.weapons[j].type=="molotov_cocktail":
						g.players[x].playsound("molotovexplode")
						g.n.broadcast("distsound molotovexplode "+str(g.players[x].x)+" "+str(g.players[x].y)+" "+str(g.players[x].z)+" "+g.players[x].map+"",0)
#						g.play("bulletfall"+str(random(1,12))+"",g.players[x].x,g.players[x].y,g.players[x].z,g.players[x].map)
					else:
						if "thrown" not in g.weapons[j].type: g.play(g.weapons[j].type+"hit"+str(random(1,3))+"",g.players[x].x,g.players[x].y,g.players[x].z,g.players[x].map,g.players[x])
						if "_knife" in g.weapons[j].type: g.play("misc346",g.players[x].x,g.players[x].y,g.players[x].z,g.players[x].map,g.players[x])
						if "thrown" in g.weapons[j].type and "_sword" in g.weapons[j].type: g.play("misc293",g.players[x].x,g.players[x].y,g.players[x].z,g.players[x].map,g.players[x])
						if not g.players[x].shielded or (g.players[x].shielded and (g.weapons[j].type=="punch" or g.weapons[j].type=="feet")): g.players[x].play_hit_sound()
			for i in range(len(g.items)):
				if g.weapons[j].map!=g.items[i].map: continue
				dist=get_3d_distance(rx, ry, g.weapons[j].z, g.items[i].x, g.items[i].y, g.items[i].z)
				if g.weapons[j].whiztimer.elapsed>=1500 and g.items[i].map==g.weapons[j].map and g.weapons[j].bullet and dist>g.weapons[j].spread and dist<=15:
					g.play("bulletwhiz"+str(random(1,8)),g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
					g.weapons[j].whiztimer.restart()


				if g.items[i].map==g.weapons[j].map and dist<=g.weapons[j].spread and g.items[i].map==g.weapons[j].map:
					g.play("itembreak",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
					try: g.n.send_reliable(g.weapons[j].owner.peer_id,"itemmessage you have destroyed "+str(g.items[i].itemamount)+" "+g.items[i].itemname,0)
					except: pass

					g.items.remove(g.items[i])
					hit=True
					break
			for i in range(len(g.chests)):
				if g.weapons[j].map!=g.chests[i].map: continue
				dist=get_3d_distance(rx, ry, g.weapons[j].z, g.chests[i].x, g.chests[i].y, g.chests[i].z)
				if g.weapons[j].whiztimer.elapsed>=1500 and g.chests[i].map==g.weapons[j].map and g.weapons[j].bullet and dist>g.weapons[j].spread and dist<=15:
					g.play("bulletwhiz"+str(random(1,8)),g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
					g.weapons[j].whiztimer.restart()


				if string_contains(g.chests[i].map,"base",1)>-1: continue
				if g.chests[i].map==g.weapons[j].map and dist<=g.weapons[j].spread and g.chests[i].map==g.weapons[j].map and g.chests[i].health>0:
					if g.weapons[j].type!="base_gun" and not has_line_of_sight(g.weapons[j].x, g.weapons[j].y, g.weapons[j].startz, g.chests[i].x, g.chests[i].y, g.chests[i].z, g.chests[i].map): continue

					tx=g.weapons[j].x
					ty=g.weapons[j].y
					for _ in range(get_weapon_spread(g.weapons[j].type)):
						temp=move(tx, ty, g.weapons[j].z, g.weapons[j].dir, 0, 0, 0)
						tx=temp.x
						ty=temp.y


						if g.weapons[j].type!="base_gun" and string_contains(g.get_nwall_at(temp.x, temp.y, g.weapons[j].startz, g.weapons[j].map), "wall", 1)>-1 or g.weapons[j].type!="base_gun" and string_contains(g.get_nwall_at(temp.x, temp.y, g.weapons[j].z, g.weapons[j].map), "wall", 1)>-1:
			
							if(g.weapons[j].bullet==True):
								g.play("bullet_to_wall"+str(random(1, 4)), temp.x, temp.y, g.weapons[j].z, g.weapons[j].map)
							else:
								g.play(g.weapons[j].type+"rico", temp.x, temp.y, g.weapons[j].z, g.weapons[j].map)
							_play_bulletfall(g.weapons[j])

							if "thrown" in g.weapons[j].type:
								if "sword" in g.weapons[j].type: g.play("sworddrop"+str(random(1,3)),g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
								if "knife" in g.weapons[j].type: g.play("knifedrop",g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
								spawn_item(g.weapons[j].x,g.weapons[j].y,g.weapons[j].get_ground_z(),g.weapons[j].map,g.weapons[j].type.replace("thrown_",""),1,False)
							g.weapons.pop(j)
							return

					if hit==False:
						hit=True
					inpact=random(g.weapons[j].mindammage, g.weapons[j].maxdammage)
					g.chests[i].health-=inpact
					if g.chests[i].health<=0 and g.task==3 and g.weapons[j].owner.task_data[3]<15:
						g.weapons[j].owner.eventpoint+=10;g.weapons[j].owner.playsound("misc294"); g.weapons[j].owner.currenteventpoint+=10; g.n.send_reliable(g.weapons[j].owner.peer_id,"you got 10 event points",2); g.weapons[j].owner.task_data[3]+=1
					if g.chests[i].health<=0 and g.task==3 and g.weapons[j].owner.task_data[3]>=15:
						g.weapons[j].owner.currenteventpoint+=10

					if(g.weapons[j].bullet):
						g.play("bulletmotorhit"+str(random(1,8)), g.chests[i].x, g.chests[i].y, g.chests[i].z, g.chests[i].map)
						_play_bulletfall(g.weapons[j])

					if g.weapons[j].type=="molotov_cocktail":
						g.play("molotovexplode",g.chests[i].x,g.chests[i].y,g.chests[i].z,g.chests[i].map)
						g.n.broadcast("distsound molotovexplode "+str(g.chests[i].x)+" "+str(g.chests[i].y)+" "+str(g.chests[i].z)+" "+g.chests[i].map+"",0)
						_play_bulletfall(g.weapons[j])

#						g.play("bulletfall"+str(random(1,12))+"",g.chests[i].x,g.chests[i].y,g.chests[i].z,g.chests[i].map)
					else: 						g.play("bulletmotorhit"+str(random(1,8)), g.chests[i].x, g.chests[i].y, g.chests[i].z, g.chests[i].map)
					
				

					break
			for i in range(len(g.electrics)):
				if g.weapons[j].map!=g.electrics[i].map: continue
				dist=get_3d_distance(rx, ry, g.weapons[j].z, g.electrics[i].x, g.electrics[i].y, g.electrics[i].z)
				if g.weapons[j].whiztimer.elapsed>=1500 and g.electrics[i].map==g.weapons[j].map and g.weapons[j].bullet and dist>g.weapons[j].spread and dist<=15:
					g.play("bulletwhiz"+str(random(1,8)),g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
					g.weapons[j].whiztimer.restart()


				if g.electrics[i].map==g.weapons[j].map and dist<=g.weapons[j].spread and g.electrics[i].map==g.weapons[j].map and g.electrics[i].health>0:
					#if not has_line_of_sight(g.weapons[j].x, g.weapons[j].y, g.weapons[j].startz, g.electrics[i].x, g.electrics[i].y, g.electrics[i].z, g.electrics[i].map): continue
					tx=g.weapons[j].x
					ty=g.weapons[j].y
					for _ in range(get_weapon_spread(g.weapons[j].type)):
						temp=move(tx, ty, g.weapons[j].z, g.weapons[j].dir, 0, 0, 0)
						tx=temp.x
						ty=temp.y
						if g.weapons[j].type!="base_gun" and string_contains(g.get_nwall_at(temp.x, temp.y, g.weapons[j].startz, g.weapons[j].map), "wall", 1)>-1 or g.weapons[j].type!="base_gun" and string_contains(g.get_nwall_at(temp.x, temp.y, g.weapons[j].z, g.weapons[j].map), "wall", 1)>-1:
			
							if(g.weapons[j].bullet==True):
								g.play("bullet_to_wall"+str(random(1, 4)), temp.x, temp.y, g.weapons[j].z, g.weapons[j].map)
							else:
								g.play(g.weapons[j].type+"rico", temp.x, temp.y, g.weapons[j].z, g.weapons[j].map)
							_play_bulletfall(g.weapons[j])

							if "thrown" in g.weapons[j].type:
								if "sword" in g.weapons[j].type: g.play("sworddrop"+str(random(1,3)),g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
								if "knife" in g.weapons[j].type: g.play("knifedrop",g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
								spawn_item(g.weapons[j].x,g.weapons[j].y,g.weapons[j].get_ground_z(),g.weapons[j].map,g.weapons[j].type.replace("thrown_",""),1,False)
							g.weapons.pop(j)
							return

					if hit==False:
						hit=True
					inpact=random(g.weapons[j].mindammage, g.weapons[j].maxdammage)
					g.electrics[i].health-=inpact
					if(g.weapons[j].bullet):
						g.play("h"+str(random(1,6)), g.electrics[i].x, g.electrics[i].y, g.electrics[i].z, g.electrics[i].map)
						_play_bulletfall(g.weapons[j])

					if g.weapons[j].type=="molotov_cocktail":
						g.play("molotovexplode",g.electrics[i].x,g.electrics[i].y,g.electrics[i].z,g.electrics[i].map)
						g.n.broadcast("distsound molotovexplode "+str(g.electrics[i].x)+" "+str(g.electrics[i].y)+" "+str(g.electrics[i].z)+" "+g.electrics[i].map+"",0)
						_play_bulletfall(g.weapons[j])

#						g.play("bulletfall"+str(random(1,12))+"",g.electrics[i].x,g.electrics[i].y,g.electrics[i].z,g.electrics[i].map)
					else: 						g.play("bulletmotorhit"+str(random(1,8)), g.electrics[i].x, g.electrics[i].y, g.electrics[i].z, g.electrics[i].map)
					
				

					break

			for i in range(len(g.group_bases)):
				if g.weapons[j].owner.group=="": continue
				if g.group_bases[i].map!=g.weapons[j].map: continue
				dist=get_3d_distance(rx, ry, g.weapons[j].z, g.group_bases[i].x, g.group_bases[i].y, g.group_bases[i].z)
				if g.weapons[j].whiztimer.elapsed>=1500 and g.group_bases[i].map==g.weapons[j].map and g.weapons[j].bullet and dist>g.weapons[j].spread and dist<=15:
					g.play("bulletwhiz"+str(random(1,8)),g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
					g.weapons[j].whiztimer.restart()


				if g.weapons[j].owner.group==g.group_bases[i].name: continue
				if g.group_bases[i].map==g.weapons[j].map and dist<=g.weapons[j].spread and g.group_bases[i].map==g.weapons[j].map and g.group_bases[i].health>0:
					if hit==False:
						hit=True
					inpact=random(g.weapons[j].mindammage, g.weapons[j].maxdammage)
					damage_mult = 1.0
					if hasattr(g.group_bases[i], "wall_level"):
						if g.group_bases[i].wall_level == 2:
							damage_mult = 0.7
						elif g.group_bases[i].wall_level == 3:
							damage_mult = 0.4
					g.group_bases[i].health-=int(inpact*35*damage_mult)
					if g.group_bases[i].health<=0:
						g.n.send_reliable(g.weapons[j].owner.peer_id,"you got 100 zero tokens for destroying a base",2)
						g.weapons[j].owner.zhtoken+=100
					if g.group_bases[i].alarm==False:
						g.group_bases[i].alarm=True
					g.group_bases[i].hitby=g.weapons[j].owner.name
					g.group_bases[i].hitby2=g.weapons[j].owner.name+"'s "+g.weapons[j].type
					hit_sound = "bulletmotorhit" + str(random(1,8))
					if hasattr(g.group_bases[i], "wall_level"):
						if g.group_bases[i].wall_level == 1:
							hit_sound = "wallhit" + str(random(1,3))
						elif g.group_bases[i].wall_level == 3:
							hit_sound = "wallhit" + str(random(4,6))
					if(g.weapons[j].bullet):
						g.play(hit_sound, g.group_bases[i].x, g.group_bases[i].y, g.group_bases[i].z, g.group_bases[i].map)
						_play_bulletfall(g.weapons[j])

					if g.weapons[j].type=="molotov_cocktail":
						g.play("molotovexplode",g.group_bases[i].x,g.group_bases[i].y,g.group_bases[i].z,g.group_bases[i].map)
						g.n.broadcast("distsound molotovexplode "+str(g.group_bases[i].x)+" "+str(g.group_bases[i].y)+" "+str(g.group_bases[i].z)+" "+g.group_bases[i].map+"",0)
						_play_bulletfall(g.weapons[j])

#						g.play("bulletfall"+str(random(1,12))+"",g.group_bases[i].x,g.group_bases[i].y,g.group_bases[i].z,g.group_bases[i].map)
					else: 						g.play(hit_sound, g.group_bases[i].x, g.group_bases[i].y, g.group_bases[i].z, g.group_bases[i].map)
					
				

					break

			for i in range(len(g.mines)):
				if g.weapons[j].map!=g.mines[i].map: continue
				dist=get_3d_distance(rx, ry, g.weapons[j].z, g.mines[i].x, g.mines[i].y, g.mines[i].z)
				if g.weapons[j].whiztimer.elapsed>=1500 and g.mines[i].map==g.weapons[j].map and g.weapons[j].bullet and dist>g.weapons[j].spread and dist<=15:
					g.play("bulletwhiz"+str(random(1,8)),g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
					g.weapons[j].whiztimer.restart()


				if g.mines[i].map==g.weapons[j].map and dist<=g.weapons[j].spread and g.mines[i].map==g.weapons[j].map and g.mines[i].health>0:
					if g.weapons[j].type!="base_gun" and not has_line_of_sight(g.weapons[j].x, g.weapons[j].y, g.weapons[j].startz, g.mines[i].x, g.mines[i].y, g.mines[i].z, g.mines[i].map): continue

					if hit==False:
						hit=True
					inpact=random(g.weapons[j].mindammage, g.weapons[j].maxdammage)
					g.mines[i].health-=inpact
					if(g.weapons[j].bullet):
						g.play("corpsehit"+str(random(1,3)), g.mines[i].x, g.mines[i].y, g.mines[i].z, g.mines[i].map)
						_play_bulletfall(g.weapons[j])

					if g.weapons[j].type=="molotov_cocktail":
						g.play("molotovexplode",g.mines[i].x,g.mines[i].y,g.mines[i].z,g.mines[i].map)
						g.n.broadcast("distsound molotovexplode "+str(g.mines[i].x)+" "+str(g.mines[i].y)+" "+str(g.mines[i].z)+" "+g.mines[i].map+"",0)
						_play_bulletfall(g.weapons[j])

#						g.play("bulletfall"+str(random(1,12))+"",g.mines[i].x,g.mines[i].y,g.mines[i].z,g.mines[i].map)
					else: 						g.play("corpsehit"+str(random(1,3)), g.mines[i].x, g.mines[i].y, g.mines[i].z, g.mines[i].map)
					break
				



			for i in range(len(g.npcs)):
				if g.npcs[i].faint: continue
				if g.weapons[j].map==g.npcs[i].map: dist = get_3d_distance(rx, ry, g.weapons[j].z, g.npcs[i].x, g.npcs[i].y, g.npcs[i].z)
				if g.weapons[j].whiztimer.elapsed>=1500 and g.npcs[i].map==g.weapons[j].map and g.weapons[j].bullet and dist>g.weapons[j].spread and dist<=15 and g.weapons[j].owner!=g.npcs[i] and g.npcs[i].map==g.weapons[j].map :
					g.play("bulletwhiz"+str(random(1,8)),g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
					g.weapons[j].whiztimer.restart()

				if g.npcs[i].matchmode=="teamz" and g.weapons[j].owner.joinedmatch==g.npcs[i].joinedmatch and g.get_tile_at(rx, ry, 0, g.weapons[j].map)!="hardwood": continue
				if g.npcs[i].fulldied or g.npcs[i].name==g.weapons[j].owner.name: continue
				if g.npcs[i].joinedmatch==g.weapons[j].owner.joinedmatch and g.weapons[j].owner.joinedmatch!="" and g.npcs[i].matchteam==g.weapons[j].owner.matchteam and g.weapons[j].owner.matchmode!="teaml" and g.weapons[j].owner.matchmode!="g" and g.weapons[j].owner.matchmode!="g2" and g.weapons[j].owner.matchmode!="sword" and g.weapons[j].owner.matchmode!="collect" and g.weapons[j].owner.matchmode!="teamk2" and g.weapons[j].owner.matchmode!="teamf2" and g.weapons[j].owner.matchmode!="snow" and g.weapons[j].owner.matchmode!="sniper" and g.weapons[j].owner.matchmode!="minecraft":
					continue

				if g.npcs[i].map==g.weapons[j].map and dist<=g.weapons[j].spread and g.npcs[i].map==g.weapons[j].map and g.npcs[i].health>0:
					if hit==False:
						hit=True
					inpact=random(g.weapons[j].mindammage, g.weapons[j].maxdammage)
					if g.weapons[j].bullet:
						if g.weapons[j].owner.z>=g.npcs[i].z+2:
							inpact*=2
							try: g.weapons[j].owner.send_bulletbody()
							except: pass
						else:
							try: g.weapons[j].owner.send_bulletbody2()
							except: pass


					g.npcs[i].health-=inpact
					g.npcs[i].trackwho=1 if not g.weapons[j].owner.isbot else 2
					if g.npcs[i].hitattack==True:
						g.npcs[i].attack=True
					if g.npcs[i].painsoundamount>0:
						g.play(g.npcs[i].painsound+str(random(1,g.npcs[i].painsoundamount)), g.npcs[i].x, g.npcs[i].y, g.npcs[i].z, g.npcs[i].map)
					else:
						g.play(g.npcs[i].painsound, g.npcs[i].x, g.npcs[i].y, g.npcs[i].z, g.npcs[i].map)
					if(g.weapons[j].bullet):
						g.play("bullet_impact_body"+str(random(1,16)),g.npcs[i].x,g.npcs[i].y,g.npcs[i].z,g.npcs[i].map,g.npcs[i])
						_play_bulletfall(g.weapons[j])

					if g.weapons[j].type=="snowflake_shard":
						g.play("snowhit"+str(random(1,2))+"",g.npcs[i].x,g.npcs[i].y,g.npcs[i].z,g.npcs[i].map)
						g.npcs[i].stunned=True
						g.npcs[i].stuntime=3000
						g.npcs[i].stuntimer.restart()
					if(g.weapons[j].bullet):
						_play_bulletfall(g.weapons[j])

					if g.weapons[j].type=="molotov_cocktail":
						g.play("molotovexplode",g.npcs[i].x,g.npcs[i].y,g.npcs[i].z,g.npcs[i].map)
						g.n.broadcast("distsound molotovexplode "+str(g.npcs[i].x)+" "+str(g.npcs[i].y)+" "+str(g.npcs[i].z)+" "+g.npcs[i].map+"",0)

#						g.play("bulletfall"+str(random(1,12))+"",g.npcs[i].x,g.npcs[i].y,g.npcs[i].z,g.npcs[i].map)
					else:
						if "thrown" not in g.weapons[j].type: g.play(g.weapons[j].type+"hit"+str(random(1,3))+"",g.npcs[i].x,g.npcs[i].y,g.npcs[i].z,g.npcs[i].map,g.npcs[i])
						if "_knife" in g.weapons[j].type: g.play("misc346",g.npcs[i].x,g.npcs[i].y,g.npcs[i].z,g.npcs[i].map,g.npcs[i])
						if "thrown" in g.weapons[j].type and "_sword" in g.weapons[j].type: g.play("misc293",g.npcs[i].x,g.npcs[i].y,g.npcs[i].z,g.npcs[i].map,g.npcs[i])

					
				

					if g.npcs[i].hitby!=g.weapons[j].owner.name:
						g.npcs[i].hitby=g.weapons[j].owner.name
						if not g.weapons[j].owner.isbot: 						g.npcs[i].hitby2=g.weapons[j].owner.name
						break
					# g.npcs[i].playsound2("hit")
			for i in range(len(g.zombies)):
				if hit: continue
				if g.weapons[j].map==g.zombies[i].map: dist = get_3d_distance(rx, ry, g.weapons[j].z, g.zombies[i].x, g.zombies[i].y, g.zombies[i].z)
				if g.weapons[j].whiztimer.elapsed>=1500 and g.zombies[i].map==g.weapons[j].map and g.weapons[j].bullet and dist>g.weapons[j].spread and dist<=15 and g.weapons[j].owner!=g.zombies[i] and g.zombies[i].map==g.weapons[j].map :
					g.play("bulletwhiz"+str(random(1,8)),g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
					g.weapons[j].whiztimer.restart()

				if g.zombies[i].map==g.weapons[j].map and dist<=g.weapons[j].spread and g.zombies[i].map==g.weapons[j].map and g.zombies[i].health>0:
					if hit==False:
						hit=True
					inpact=random(g.weapons[j].mindammage, g.weapons[j].maxdammage)
					if g.weapons[j].bullet:
						if g.weapons[j].owner.z>=g.zombies[i].z+2:
							inpact*=2
							try: g.weapons[j].owner.send_bulletbody()
							except: pass
						else:
							try: g.weapons[j].owner.send_bulletbody2()
							except: pass


					g.zombies[i].health-=inpact
					g.play("zombiehurt", g.zombies[i].x, g.zombies[i].y, g.zombies[i].z, g.zombies[i].map)
					if g.weapons[j].owner.isbot: g.zombies[i].mode=2
					if not g.weapons[j].owner.isbot: g.zombies[i].mode=1
					#g.weapons[j].owner.send_bulletbody2()
					if(g.weapons[j].bullet):
						g.play("bullet_impact_body"+str(random(1,16)),g.zombies[i].x,g.zombies[i].y,g.zombies[i].z,g.zombies[i].map,g.zombies[i])
						_play_bulletfall(g.weapons[j])

					if g.weapons[j].type=="molotov_cocktail":
						g.play("molotovexplode",g.zombies[i].x,g.zombies[i].y,g.zombies[i].z,g.zombies[i].map)
						g.n.broadcast("distsound molotovexplode "+str(g.zombies[i].x)+" "+str(g.zombies[i].y)+" "+str(g.zombies[i].z)+" "+g.zombies[i].map+"",0)
						_play_bulletfall(g.weapons[j])

#						g.play("bulletfall"+str(random(1,12))+"",g.zombies[i].x,g.zombies[i].y,g.zombies[i].z,g.zombies[i].map)
					else:
						if "thrown" not in g.weapons[j].type: g.play(g.weapons[j].type+"hit"+str(random(1,3))+"",g.zombies[i].x,g.zombies[i].y,g.zombies[i].z,g.zombies[i].map,g.zombies[i])
						if "_knife" in g.weapons[j].type: g.play("misc346",g.zombies[i].x,g.zombies[i].y,g.zombies[i].z,g.zombies[i].map,g.zombies[i])
						if "thrown" in g.weapons[j].type and "_sword" in g.weapons[j].type: g.play("misc293",g.zombies[i].x,g.zombies[i].y,g.zombies[i].z,g.zombies[i].map,g.zombies[i])

					
				
			for wall in g.maps[g.get_map_index(g.weapons[j].map)].mapwalls:
				if wall.health<=0: continue
				for wx in range(wall.minx,wall.maxx+1):
					for wy in range(wall.miny,wall.maxy+1):
						for wz in range(wall.minz,wall.maxz+1):
							if g.weapons[j].whiztimer.elapsed>=1500 and g.weapons[j].bullet and get_3d_distance(rx, ry, g.weapons[j].z, wx, wy, wz)>g.weapons[j].spread and get_3d_distance(rx, ry, g.weapons[j].z, wx, wy, wz)<=15 and g.weapons[j].owner!=wall and g.weapons[j].map==g.weapons[j].map :
								g.play("bulletwhiz"+str(random(1,8)),g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
								g.weapons[j].whiztimer.restart()
							if not hit and get_3d_distance(rx, ry, g.weapons[j].z, wx, wy, wz)<=g.weapons[j].spread:
				
								hit=True
								inpact=random(g.weapons[j].mindammage,g.weapons[j].maxdammage)
								wall.destroyed=False
								wall.health-=inpact
								if wall.health>0: g.play("walldoor",g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
								if wall.health<=0: g.play("walldestroy",g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
								if(g.weapons[j].bullet):

									_play_bulletfall(g.weapons[j])

								if g.weapons[j].type=="molotov_cocktail":
									g.play("molotovexplode",g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
									g.n.broadcast("distsound molotovexplode "+str(wx)+" "+str(wy)+" "+str(wz)+" "+g.weapons[j].map+"",0)
									_play_bulletfall(g.weapons[j])

#						g.play("bulletfall"+str(random(1,12))+"",g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
								else: g.play(g.weapons[j].type+"hit"+str(random(1,3))+"",wx,wy,wz,g.weapons[j].map,wall)
					
				
			for mwall in g.mwalls:
				if mwall.health<=0: continue
				if mwall.map!=g.weapons[j].map: continue
				for wx in range(mwall.minx,mwall.maxx+1):
					for wy in range(mwall.miny,mwall.maxy+1):
						for wz in range(mwall.minz,mwall.maxz+1):
							dist = get_3d_distance(rx, ry, g.weapons[j].z, wx, wy, wz)
							if g.weapons[j].whiztimer.elapsed>=1500 and g.weapons[j].bullet and dist>g.weapons[j].spread and dist<=15:
								g.play("bulletwhiz"+str(random(1,8)),g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
								g.weapons[j].whiztimer.restart()
							if not hit and dist<=g.weapons[j].spread:
				
								hit=True
								inpact=random(g.weapons[j].mindammage,g.weapons[j].maxdammage)
								mwall.health-=inpact
								if mwall.health>0: g.play2("walldoor",mwall.minx,mwall.maxx,mwall.miny,mwall.maxy,mwall.minz,mwall.maxz,mwall.map)
								if mwall.health<=0: g.play2("walldestroy",mwall.minx,mwall.maxx,mwall.miny,mwall.maxy,mwall.minz,mwall.maxz,mwall.map)
								if(g.weapons[j].bullet):

									_play_bulletfall(g.weapons[j])

								if g.weapons[j].type=="molotov_cocktail":
									g.play("molotovexplode",g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
									g.n.broadcast("distsound molotovexplode "+str(wx)+" "+str(wy)+" "+str(wz)+" "+g.weapons[j].map+"",0)
									_play_bulletfall(g.weapons[j])

								else: g.play(g.weapons[j].type+"hit"+str(random(1,3))+"",wx,wy,wz,g.weapons[j].map)
					
				

					
				if hit: break
			for barricade in g.barricades:
				if barricade.health<=0: continue
				if barricade.map!=g.weapons[j].map: continue
				for wx in range(barricade.minx,barricade.maxx+1):
					for wy in range(barricade.miny,barricade.maxy+1):
						for wz in range(barricade.minz,barricade.maxz+1):
							dist = get_3d_distance(rx, ry, g.weapons[j].z, wx, wy, wz)
							if g.weapons[j].whiztimer.elapsed>=1500 and g.weapons[j].bullet and dist>g.weapons[j].spread and dist<=15:
								g.play("bulletwhiz"+str(random(1,8)),g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
								g.weapons[j].whiztimer.restart()
							if not hit and dist<=g.weapons[j].spread:
				
								hit=True
								inpact=random(g.weapons[j].mindammage,g.weapons[j].maxdammage)
								barricade.health-=inpact
								if barricade.health>0: g.play("wallhit"+str(random(1,3)),barricade.minx,barricade.miny,barricade.minz,barricade.map)
								if barricade.health<=0: g.play2("walldestroy5",barricade.minx,barricade.maxx,barricade.miny,barricade.maxy,barricade.minz,barricade.maxz,barricade.map); barricade.remove_platform(); g.barricades.remove(barricade)
								if(g.weapons[j].bullet):

									_play_bulletfall(g.weapons[j])

								if g.weapons[j].type=="molotov_cocktail":
									g.play("molotovexplode",g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
									g.n.broadcast("distsound molotovexplode "+str(wx)+" "+str(wy)+" "+str(wz)+" "+g.weapons[j].map+"",0)
									_play_bulletfall(g.weapons[j])

								else: g.play(g.weapons[j].type+"hit"+str(random(1,3))+"",wx,wy,wz,g.weapons[j].map)
					
				if hit: break

					
			for ladder in g.ladders:
				if ladder.health<=0: continue
				if ladder.map!=g.weapons[j].map: continue
				for wx in range(ladder.minx,ladder.maxx+1):
					for wy in range(ladder.miny,ladder.maxy+1):
						for wz in range(ladder.minz,ladder.maxz+1):
							dist = get_3d_distance(rx, ry, g.weapons[j].z, wx, wy, wz)
							if g.weapons[j].whiztimer.elapsed>=1500 and g.weapons[j].bullet and dist>g.weapons[j].spread and dist<=15:
								g.play("bulletwhiz"+str(random(1,8)),g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
								g.weapons[j].whiztimer.restart()
							if not hit and dist<=g.weapons[j].spread:
				
								hit=True
								inpact=random(g.weapons[j].mindammage,g.weapons[j].maxdammage)
								ladder.health-=inpact
								if ladder.health<=0: g.play2("ladder_collapse",ladder.minx,ladder.maxx,ladder.miny,ladder.maxy,ladder.minz,ladder.maxz,ladder.map); ladder.remove_platform(); g.ladders.remove(ladder)
								if(g.weapons[j].bullet):

									_play_bulletfall(g.weapons[j])

								if g.weapons[j].type=="molotov_cocktail":
									g.play("molotovexplode",g.weapons[j].x,g.weapons[j].y,g.weapons[j].z,g.weapons[j].map)
									g.n.broadcast("distsound molotovexplode "+str(wx)+" "+str(wy)+" "+str(wz)+" "+g.weapons[j].map+"",0)
									_play_bulletfall(g.weapons[j])

								else: g.play(g.weapons[j].type+"hit"+str(random(1,3))+"",wx,wy,wz,g.weapons[j].map)
					
				if hit: break

					


			if(hit and g.weapons[j].map.startswith("zombie2")):
				if g.weapons[j].owner.matchteam=="blue": g.weapons[j].owner.health+=20
			if hit:
				g.weapons.pop(j)
				return
				
			

		
	
def spawn_weapon(x, y, z, dir, type, map, owner):
	w1=weapon(x, y, z, dir, type, map, owner)
	g.weapons.append(w1)
	
def get_weapon_range(gun, silenced=[], index=-1):
	"""Data-driven weapon range lookup."""
	w = data_loader.get_weapon(gun)
	if not w:
		return 0
	r = w.get("range", 0)
	if gun in silenced:
		return r // 2
	if index != -1 and g.players[index].aim_mode == 1 and (g.players[index].aim == 1 or g.players[index].aim == -1):
		return r // 2
	return r

def get_weapon_spread(gun):
	"""Data-driven weapon spread lookup."""
	w = data_loader.get_weapon(gun)
	return w.get("spread", 0) if w else 0

def get_mindamage(gun):
	"""Data-driven min damage lookup."""
	w = data_loader.get_weapon(gun)
	return w.get("min_damage", -1) if w else -1

def get_maxdamage(gun):
	"""Data-driven max damage lookup."""
	w = data_loader.get_weapon(gun)
	return w.get("max_damage", -1) if w else -1

def get_max_values(mapname):
	ind=g.get_map_index(mapname)
	temp=vector()
	if ind<0:
		return temp
	temp.x=g.maps[ind].max.x
	temp.y=g.maps[ind].max.y
	temp.z=g.maps[ind].max.z
	return temp
import math


def has_line_of_sight(start_x, start_y, start_z, end_x, end_y, end_z, map_name):
    dir_x = end_x - start_x
    dir_y = end_y - start_y
    dir_z = end_z - start_z

    distance = math.sqrt(dir_x**2 + dir_y**2 + dir_z**2)
    if distance < 0.1:
        return True

    norm_x = dir_x / distance
    norm_y = dir_y / distance
    norm_z = dir_z / distance

    step_size = 1
    num_steps = int(distance / step_size)

    current_x, current_y, current_z = start_x, start_y, start_z
    
    map_idx = g.get_map_index(map_name)

    for i in range(num_steps + 1): 
        if i > 0:
            current_x += norm_x * step_size
            current_y += norm_y * step_size
            current_z += norm_z * step_size

        check_tile_x = round(current_x)
        check_tile_y = round(current_y)
        check_tile_z = round(current_z)

        is_target_tile = (check_tile_x == round(end_x) and
                          check_tile_y == round(end_y) and
                          check_tile_z == round(end_z))
        
        if is_target_tile and i >= num_steps:
            continue

        nwall_type = g.get_nwall_at(check_tile_x, check_tile_y, check_tile_z, map_name)
        if "wall" in nwall_type:
            return False

    return True