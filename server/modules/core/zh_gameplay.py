import globals as g
import os
import time
import pickle
import json
import datetime
import urllib.parse
import requests
from threading import Thread
from timer import timer
import data_loader

def climb_bus_ladder(player, bus):
	player.climbing = True
	g.n.send_reliable(player.peer_id, "stopmoving", 0)
	
	def func():
		try:
			# Play a realistic step-by-step ladder climb instead of a sudden snap upward.
			step_sounds = ["misc77.ogg", "misc78.ogg", "misc79.ogg", "misc77.ogg", "misc78.ogg"]
			time.sleep(0.18)
			for i, snd in enumerate(step_sounds):
				if not player.dead and player.map == bus.map and bus.running and bus.is_stopped:
					player.z += 1  # +1 Z per step = total +5 after 5 steps
					g.n.send_reliable(player.peer_id, f"move {player.x} {player.y} {player.z}", 0)
					# Play step sound directly to player (3D positioned)
					g.n.send_reliable(player.peer_id, f"play_s {snd}", 0)
					# Also play to nearby players as 3D sound
					g.play("bulletmotorhit" + str(random(1, 3)), player.x, player.y, player.z, player.map)
				time.sleep(0.28)
			
			if not player.dead and player.map == bus.map and bus.running and bus.is_stopped:
				# Landing sound
				g.n.send_reliable(player.peer_id, "play_s misc79.ogg", 0)
				# Place player at the bus entrance — outside the door, on top of the bus body
				# player.y is still bus.y - 1 (front of bus), z is now +5 higher
				# Close the bus door so player must open it before entering
				bus.doors_open = False
				g.play("bus_doors_sound_effect", bus.x, bus.y, bus.z, bus.map)
				# Now add as passenger: lands at local_y=0 (entrance, just outside cabin door)
				bus.add_passenger(player)
				# Override: place player at doorway threshold (local_y=1) facing inward
				player.local_y = 0
				player.y = bus.y + player.local_y
				g.n.send_reliable(player.peer_id, f"move {player.x} {player.y} {player.z}", 0)
				# Notify player about the door
				g.n.send_reliable(player.peer_id, "The bus door is closed. Press Enter to open it, then step inside.", 0)
		except Exception as ex:
			pass
		finally:
			player.climbing = False
			g.n.send_reliable(player.peer_id, "startmoving", 0)
	
	Thread(target=func).start()


def play(sound, x, y, z, map, index=None, reliable=True, channel=3,pitch=100):
	if index is not None and hasattr(index,'hidden') and index.hidden: return
	x=round(x)
	y=round(y)
	z=round(z)
	onlynear=True
	x=round(x)
	y=round(y)
	z=round(z)
	if(onlynear==True):
	
		if(index is not None):
		
			if(reliable):
				for p in g.players:
					if "bullet_to_wall" not in sound and p.specmap!=map and g.get_hidden_area_at(p.x,p.y,p.z,p.map)!=g.get_hidden_area_at(x,y,z,map): continue
					if "bullet_to_wall" not in sound and p.specmap==map and g.get_hidden_area_at(p.wx,p.wy,p.wz,p.specmap)!=g.get_hidden_area_at(x,y,z,map): continue
					if p.dead: continue
					if (p.map==map or p.specmap==map) and get_3d_distance(p.wx,p.wy,p.wz,x,y,z)<=40: g.n.send_reliable(p.peer_id,sound+" "+str(x)+" "+str(y)+" "+str(z)+" "+map+" "+str(pitch), channel)
			else:
				for p in g.players:
					if "bullet_to_wall" not in sound and p.specmap!=map and g.get_hidden_area_at(p.x,p.y,p.z,p.map)!=g.get_hidden_area_at(x,y,z,map): continue
					if "bullet_to_wall" not in sound and p.specmap==map and g.get_hidden_area_at(p.wx,p.wy,p.wz,p.specmap)!=g.get_hidden_area_at(x,y,z,map): continue

					if p.dead: continue
					if (p.map==map or p.specmap==map) and get_3d_distance(p.wx,p.wy,p.wz,x,y,z)<=40: g.n.send_reliable(p.peer_id,sound+" "+str(x)+" "+str(y)+" "+str(z)+" "+map+" "+str(pitch), channel)

			
		else:
		
			if(reliable):
				for p in g.players:
					if sound=="itembeep2" and p.itembeep==0: continue
					if "bullet_to_wall" not in sound and p.specmap!=map and g.get_hidden_area_at(p.x,p.y,p.z,p.map)!=g.get_hidden_area_at(x,y,z,map): continue
					if "bullet_to_wall" not in sound and p.specmap==map and g.get_hidden_area_at(p.wx,p.wy,p.wz,p.specmap)!=g.get_hidden_area_at(x,y,z,map): continue

					if p.dead: continue
					if (p.map==map or p.specmap==map) and get_3d_distance(p.wx,p.wy,p.wz,x,y,z)<=40: g.n.send_reliable(p.peer_id,sound+" "+str(x)+" "+str(y)+" "+str(z)+" "+map+" "+str(pitch), channel)
			else:
				for p in g.players:
					if sound=="itembeep2" and p.itembeep==0: continue
					if "bullet_to_wall" not in sound and p.specmap!=map and g.get_hidden_area_at(p.x,p.y,p.z,p.map)!=g.get_hidden_area_at(x,y,z,map): continue
					if "bullet_to_wall" not in sound and p.specmap==map and g.get_hidden_area_at(p.wx,p.wy,p.wz,p.specmap)!=g.get_hidden_area_at(x,y,z,map): continue

					if p.dead: continue
					if (p.map==map or p.specmap==map) and get_3d_distance(p.wx,p.wy,p.wz,x,y,z)<=40: g.n.send_reliable(p.peer_id,sound+" "+str(x)+" "+str(y)+" "+str(z)+" "+map+" "+str(pitch), channel)

			
		
	else:
		for p in g.players:
			if "bullet_to_wall" not in sound and p.specmap!=map and g.get_hidden_area_at(p.x,p.y,p.z,p.map)!=g.get_hidden_area_at(x,y,z,map): continue
			if "bullet_to_wall" not in sound and p.specmap==map and g.get_hidden_area_at(p.wx,p.wy,p.wz,p.specmap)!=g.get_hidden_area_at(x,y,z,map): continue

			if p.dead: continue
			if (p.map==map or p.specmap==map) and get_3d_distance(p.wx,p.wy,p.wz,x,y,z)<=40: g.n.send_reliable(p.peer_id,sound+" "+str(x)+" "+str(y)+" "+str(z)+" "+map+" "+str(pitch), channel)


def move_player(index, x, y, z, map, sound=False):
	try:
		f=open("maps/"+map+".map","r")
		f.close()
	except: return
	
	if(index>-1):
	
		g.players[index].items_got=0
		if map=="lobby": g.players[index].invites.clear()
		if "flag" in g.players[index].map and map=="lobby":
			if 1:
				if 1:
					j=g.players[index]
					item_map={}
					for item in g.dontlose:
						if j is not None and j.get_item_count(item)>0: item_map[item]=j.get_item_count(item)
					try: j.inv=dict()
					except: pass
					for item in item_map.keys():
						if j is not None: j.give(item,item_map[item])

		if g.players[index].faint and map=="lobby":
			g.players[index].faint=False
			g.players[index].fainted=False
			g.n.send_reliable(g.players[index].peer_id,"startmoving",0)
		if map=="lobby":
			g.players[index].weapon="punch"
			g.players[index].weapon2="feet"
			g.players[index].hitby=""
			g.players[index].hitby2=""

			g.n.send_reliable(g.players[index].peer_id,"drawsilent punch",0)
			g.n.send_reliable(g.players[index].peer_id,"draw2silent feet",0)
			g.players[index].get_char_properties()
		if g.players[index].dead: return
		if 1:
			if not g.players[index].hidden:
				for p in g.players:
					if p.name==g.players[index].name: continue
					if p.map==g.players[index].map:
						if p.mapsound==1: g.n.send_reliable(p.peer_id,"play_s misc290.ogg",0)
					if p.map==map:
						if p.mapsound==1: g.n.send_reliable(p.peer_id,"play_s misc280.ogg",0)

		g.players[index].x=string_to_number(x)
		g.players[index].y=string_to_number(y)
		g.players[index].z=string_to_number(z)
		g.players[index].map=map
		if g.players[index].map=="massacre_in_the_city": g.players[index].matchmode=""
		if not g.players[index].hidden:
			send_plus2(g.players[index].name,"update_player "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z)+" "+g.players[index].map+" "+g.players[index].name+" "+str(g.players[index].facing),20,True)
		f=open("maps/"+g.players[index].map+".map","r",encoding="utf-8")
		g.n.send_reliable(g.players[index].peer_id,"move "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z)+"",0)
		data=f.read()
		g.n.send_reliable(g.players[index].peer_id,"mapdata "+data,0)
		for p in g.players:
			if p.specplayer==g.players[index].name:
				g.n.send_reliable(p.peer_id,"mapdata "+data,0)
		f.close()
		for mwall in g.mwalls:
			if not mwall.destroyed and mwall.map==map:
				send_platform(g.players[index], mwall.minx, mwall.maxx, mwall.miny, mwall.maxy, mwall.minz, mwall.maxz, mwall.tile)
		for ladder in g.ladders:
			if not ladder.destroyed and ladder.map==map:
				send_platform(g.players[index], ladder.minx, ladder.maxx, ladder.miny, ladder.maxy, ladder.minz, ladder.maxz, ladder.tile)

		for base in g.group_bases:
			if base.map==map: base.send_platform_to(g.players[index])
		for b in g.bikes:
			if b.map==map: b.send_platform_to(g.players[index])

		for chest in g.chests:
			if chest.map==map:
				send_platform(g.players[index], chest.x, chest.x, chest.y, chest.y, chest.z, chest.z+4, "wallmedal4")
				send_platform(g.players[index], chest.x, chest.x, chest.y, chest.y, chest.z+5, chest.z+5, "metal5")
		if 1:
			if 1:
				if 1:
					for electric in g.electrics:
						if electric.map==g.players[index].map:
							send_platform(g.players[index], electric.x, electric.x, electric.y, electric.y, electric.z, electric.z+4, "wallfence6")
							send_platform(g.players[index], electric.x, electric.x, electric.y, electric.y, electric.z+5, electric.z+5, "metal7")

		for motor in g.motors:
			if motor.map==map:
				send_platform(g.players[index], motor.x, motor.x, motor.y, motor.y, motor.z, motor.z+4, "wallspaceship")
				send_platform(g.players[index], motor.x, motor.x, motor.y, motor.y, motor.z+5, motor.z+5, "cloth")

		#if map=="lobby": g.players[index].weapon=""
		if(sound):
			play("move",g.players[index].x,g.players[index].y,g.players[index].z,g.players[index].map,g.players[index])


def move_player2(index, x, y, z, map, sound=False):

	if(index>-1):
	
		#if g.players[index].dead: return
		g.players[index].x=string_to_number(x)
		g.players[index].y=string_to_number(y)
		g.players[index].z=string_to_number(z)
		g.players[index].map=map
		if not g.players[index].hidden:
			send_plus2(g.players[index].name,"update_player "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z)+" "+g.players[index].map+" "+g.players[index].name+" "+str(g.players[index].facing),20,True)
		f=open("maps/"+g.players[index].map+".map","r")
		g.n.send_reliable(g.players[index].peer_id,"mapdata "+f.read(),0)
		f.close()
		g.n.send_reliable(g.players[index].peer_id,"move "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z)+"",0)
		for mwall in g.mwalls:
				if not mwall.destroyed and mwall.map==map:
					send_platform(g.players[index], mwall.minx, mwall.maxx, mwall.miny, mwall.maxy, mwall.minz, mwall.maxz, mwall.tile)
		for ladder in g.ladders:
				if not ladder.destroyed and ladder.map==map:
					send_platform(g.players[index], ladder.minx, ladder.maxx, ladder.miny, ladder.maxy, ladder.minz, ladder.maxz, ladder.tile)

		for barricade in g.barricades:
				if not barricade.destroyed and barricade.map==map:
					send_platform(g.players[index], barricade.minx, barricade.maxx, barricade.miny, barricade.maxy, barricade.minz, barricade.maxz, barricade.tile)

					send_platform(g.players[index], barricade.minx, barricade.maxx, barricade.miny, barricade.maxy, barricade.minz+1, barricade.maxz+1, "dirt3")
		if 1:
			if 1:
				if 1:
					for electric in g.electrics:
						if electric.map==g.players[index].map:
							send_platform(g.players[index], electric.x, electric.x, electric.y, electric.y, electric.z, electric.z+4, "wallfence6")
							send_platform(g.players[index], electric.x, electric.x, electric.y, electric.y, electric.z+5, electric.z+5, "metal7")

		if 1:
			if 1:
				if 1:
					for electric in g.electrics:
						if electric.map==g.players[index].map:
							send_platform(g.players[index], electric.x, electric.x, electric.y, electric.y, electric.z, electric.z+4, "wallfence6")
							send_platform(g.players[index], electric.x, electric.x, electric.y, electric.y, electric.z+5, electric.z+5, "metal7")
		if 1:
			if 1:
				if 1:
					for electric in g.electrics:
						if electric.map==g.players[index].map:
							send_platform(g.players[index], electric.x, electric.x, electric.y, electric.y, electric.z, electric.z+4, "wallfence6")
							send_platform(g.players[index], electric.x, electric.x, electric.y, electric.y, electric.z+5, electric.z+5, "metal7")

		for base in g.group_bases:
			if base.map==map: base.send_platform_to(g.players[index])
		for b in g.bikes:
			if b.map==map: b.send_platform_to(g.players[index])

		for chest in g.chests:
			if chest.map==map:
				send_platform(g.players[index], chest.x, chest.x, chest.y, chest.y, chest.z, chest.z+4, "wallmedal4")
				send_platform(g.players[index], chest.x, chest.x, chest.y, chest.y, chest.z+5, chest.z+5, "metal5")
		for motor in g.motors:
			if motor.map==map:
				send_platform(g.players[index], motor.x, motor.x, motor.y, motor.y, motor.z, motor.z+4, "wallspaceship")
				send_platform(g.players[index], motor.x, motor.x, motor.y, motor.y, motor.z+5, motor.z+5, "cloth")


		#if map=="lobby": g.players[index].weapon=""
		if(sound):
			play("move",g.players[index].x,g.players[index].y,g.players[index].z,g.players[index].map,g.players[index])


def update_map(mapname):
	init_mapsystem()
	f=open("maps/"+mapname+".map","r")
	mdata=f.read()
	f.close()
	for i in range(len(g.players)):
	
		if(g.players[i].map==mapname):
		
			g.n.send_reliable(g.players[i].peer_id,"mapdata "+mdata,0)
			for mwall in g.mwalls:
				if not mwall.destroyed and mwall.map==map:
					send_platform(g.players[i], mwall.minx, mwall.maxx, mwall.miny, mwall.maxy, mwall.minz, mwall.maxz, mwall.tile)
			for ladder in g.ladders:
				if not ladder.destroyed and ladder.map==map:
					send_platform(g.players[i], ladder.minx, ladder.maxx, ladder.miny, ladder.maxy, ladder.minz, ladder.maxz, ladder.tile)

			for barricade in g.barricades:
				if not barricade.destroyed and barricade.map==map:
					send_platform(g.players[i], barricade.minx, barricade.maxx, barricade.miny, barricade.maxy, barricade.minz, barricade.maxz, barricade.tile)

					send_platform(g.players[i], barricade.minx, barricade.maxx, barricade.miny, barricade.maxy, barricade.minz+1, barricade.maxz+1, "dirt3")
			if 1:
				if 1:
					for electric in g.electrics:
						if electric.map==g.players[i].map:
							send_platform(g.players[i], electric.x, electric.x, electric.y, electric.y, electric.z, electric.z+4, "wallfence6")
							send_platform(g.players[i], electric.x, electric.x, electric.y, electric.y, electric.z+5, electric.z+5, "metal7")


			for chest in g.chests:
				if chest.map==map:
					send_platform(g.players[i], chest.x, chest.x, chest.y, chest.y, chest.z, chest.z+4, "wallmedal4")
					send_platform(g.players[i], chest.x, chest.x, chest.y, chest.y, chest.z+5, chest.z+5, "metal5")
			for motor in g.motors:
				if motor.map==map:
					send_platform(g.players[i], motor.x, motor.x, motor.y, motor.y, motor.z, motor.z+4, "wallspaceship")
					send_platform(g.players[i], motor.x, motor.x, motor.y, motor.y, motor.z+5, motor.z+5, "cloth")


def get_map_data(mapname):
	if(not file_exists("maps/"+mapname+".map")):
	
		return "That map does not exist."
		
	f=open("maps/"+mapname+".map","r")
	ret=f.read()
	f.close()
	if(ret=="" or ret=="\n"):
	
		return "Empty map."
		
	return ret


def get_nearest_player(px,py,pz,pmap,pindex=-1,maxdist=300000):
	current_distance=-1
	final_index=-1
	for i in range(len(g.players)):
		if g.players[i].faint: continue
		if(g.players[i].map!=pmap or i==pindex or g.players[i].dead):
		
			continue
			
		if pindex!=-1 and pindex.matchteam==g.players[i].matchteam and (pindex.matchmode=="teamd" or pindex.matchmode=="teamsnow" or pindex.matchmode=="teamsniper" or pindex.matchmode=="teamsword" or pindex.matchmode=="teamcollect" or pindex.matchmode=="teamk" or pindex.matchmode=="teamf" or pindex.matchmode=="teamg2" or pindex.matchmode=="teamminecraft" or pindex.matchmode=="teamg" or pindex.matchmode=="teamz2"): continue
		dist=get_3d_distance(px, py, pz, g.players[i].x, g.players[i].y, g.players[i].z)
		if dist>maxdist: continue
		if(current_distance==-1):
		
			current_distance=dist
			final_index=i
			
		else:
		
			if(dist<current_distance):
			
				current_distance=dist
				final_index=i
				
			
		
	return final_index


def get_nearest_zombie(px,py,pz,pmap,pindex=-1):
	current_distance=-1
	final_index=-1
	for i in range(len(g.zombies)):
		if(g.zombies[i].map!=pmap or i==pindex):
		
			continue
			
		dist=get_3d_distance(px, py, pz, g.zombies[i].x, g.zombies[i].y, g.zombies[i].z)
		if(current_distance==-1):
		
			current_distance=dist
			final_index=i
			
		else:
		
			if(dist<current_distance):
			
				current_distance=dist
				final_index=i
				
			
		
	return final_index


def get_nearest_npc(px,py,pz,pmap,pindex=-1,maxdist=3000000):
	current_distance=-1
	final_index=-1
	for i in range(len(g.npcs)):
		if g.npcs[i].faint: continue
		if(g.npcs[i].map!=pmap or g.npcs[i].name==pindex.name or g.npcs[i].fulldied):
		
			continue
			
		if (pindex.matchmode=="teamg2" or pindex.matchmode=="teamsnow" or pindex.matchmode=="teamsniper" or pindex.matchmode=="teamg" or pindex.matchmode=="teamk" or pindex.matchmode=="teamf" or pindex.matchmode=="teamsword" or pindex.matchmode=="teamcollect" or pindex.matchmode=="teamminecraft" or pindex.matchmode=="teamd" or pindex.matchmode=="teamz2") and g.npcs[i].matchteam==pindex.matchteam: continue
		dist=get_3d_distance(px, py, pz, g.npcs[i].x, g.npcs[i].y, g.npcs[i].z)
		if dist>maxdist: continue
		if(current_distance==-1):
		
			current_distance=dist
			final_index=i
			
		else:
		
			if(dist<current_distance):
			
				current_distance=dist
				final_index=i
				
			
		
	return final_index


def get_nearest_npc2(px,py,pz,pmap):
	current_distance=-1
	final_index=-1
	for i in range(len(g.npcs)):
		if g.npcs[i].faint: continue
		if(g.npcs[i].map!=pmap or g.npcs[i].fulldied):
		
			continue
			
		dist=get_3d_distance(px, py, pz, g.npcs[i].x, g.npcs[i].y, g.npcs[i].z)
		if(current_distance==-1):
		
			current_distance=dist
			final_index=i
			
		else:
		
			if(dist<current_distance):
			
				current_distance=dist
				final_index=i
				
			
		
	return final_index


def setupserver():
	"""Populate g.wdata from weapon JSON configs."""
	g.wdata.update(data_loader.build_wdata_dict())


def requires_ammo(w):
	w_data = data_loader.get_weapon(w)
	return bool(w_data and w_data.get("ammo_type") is not None)


def get_max_ammo(w):
	w_data = data_loader.get_weapon(w)
	val = w_data.get("mag_size", -1) if w_data else -1
	return val if val is not None else -1


def get_ammotype(w):
	w_data = data_loader.get_weapon(w)
	val = w_data.get("ammo_type", -1) if w_data else -1
	return val if val is not None else -1


def get_reloadtime(weapon):
	w_data = data_loader.get_weapon(weapon)
	val = w_data.get("reload_time", -1) if w_data else -1
	return val if val is not None else -1


def playmoving(x,y,z,map,snd,obj):
	msoundid=spawn_moving_sound(snd+".ogg",x,y,z,map,obj.name,playmoving=True)
	obj.msounds.append(msoundid)
	obj.msoundtimers.append(timer())


def playmoving2(x,y,z,map,snd,obj):
	msoundid=spawn_moving_sound(snd+".ogg",x,y,z,map,obj.name,sendowner=False,playmoving=True)
	obj.msounds.append(msoundid)
	obj.msoundtimers.append(timer())


def get_chest_at_player(p):
	for c in g.chests:
		if c.map==p.map and get_3d_distance(c.x,c.y,c.z,p.x,p.y,p.z)<=1: return c


def chestadd(p,c,m,play=False):
	if c is None: return
	p.chest=c
	for i, item in enumerate(c.items):
		if item=="zero_token": continue
		m.add(item+", "+str(c.itemamounts[i]),i)
	if "basement" in p.map: m.add("Put all your inventory to chest","put")
	#if "basement" in p.map: m.add("Get all items from chest","get")
	if len(m.menuids)==0:
		if play: p.playsound("chest7")
		pass


def get_corpse_at_player(p):
	for c in g.corpses:
		if c.map==p.map and get_3d_distance(c.x,c.y,c.z,p.x,p.y,p.z)<=0: return c


def get_corpse_at_player_length(p):
	r=0
	for c in g.corpses:
		if c.map==p.map and get_3d_distance(c.x,c.y,c.z,p.x,p.y,p.z)<=0: r+=1
	return r


def corpseadd(p,c,m,play=False):
	p.corpse=c
	if c is None: return
	for i, item in enumerate(c.items):
		if str(item)=="-1": continue
		m.add(str(item)+", "+str(c.itemamounts[i]),i)


def get_match_name(mode):
	if 1:
		if mode=="teamd": return "team dead match"
		if mode=="teamg": return "Explosive battle teamed"
		if mode=="g": return "Explosive battle not teamed"
		if mode=="teamg2": return "Abyss Clash teamed"
		if mode=="g2": return "Abyss Clash not teamed"

		if mode=="teamc": return "capture the flag"
		if mode=="teamf": return "hand to hand combat teamed"
		if mode=="teamf2": return "hand to hand combat not teamed"

		if mode=="teamk": return "knife fight match teamed"
		if mode=="teamk2": return "knife fight match not teamed"
		if mode=="snow": return "Snowflake survival not teamed"
		if mode=="teamsnow": return "Snowflake survival teamed"
		if mode=="sniper": return "Sniper duel not teamed"
		if mode=="teamsniper": return "Sniper duel teamed"

		if mode=="teamz": return "zombie survival"
		if mode=="teamz2": return "Zombie vs player"
		if mode=="teaml": return "last man standing"
		if mode=="teamminecraft": return "Medieval combat teamed"
		if mode=="minecraft": return "Medieval combat not teamed"
		if mode=="teamsword": return "Sword duel teamed"
		if mode=="sword": return "Sword duel not teamed"
		if mode=="teamcollect": return "collector's arena teamed"
		if mode=="collect": return "collector's arena not teamed"


def get_max_values(mapname):
	ind=g.get_map_index(mapname)
	temp=vector()
	if ind<0:
		return temp
	temp.x=g.maps[ind].max.x
	temp.y=g.maps[ind].max.y
	temp.z=g.maps[ind].max.z
	return temp


def get_zero_token_amount(pack):
	"""Data-driven token pack lookup."""
	return data_loader.get_token_pack_amount(pack)


def match_exists(owner):
	for m in g.matches:
		if m.owner==owner: return True
	return False


def chest_at(x,y,z,map):
	for chest in g.chests:
		if chest.x==x and chest.y==y and chest.z==z and chest.map==map: return True
	return False


def ladder_at(x,y,z,map):
	for ladder in g.ladders:
		if ladder.minx==x and ladder.miny==y and ladder.minz==z and ladder.map==map: return True
	return False


def barricade_at(x,y,z,map):
	for barricade in g.barricades:
		if barricade.minx==x and barricade.miny==y and barricade.minz==z and barricade.map==map: return True
	return False


def mine_at(x,y,z,map):
	for mine in g.mines:
		if mine.x==round(x) and mine.y==round(y) and mine.z==z and mine.map==map: return True
	return False


def get_chest_at(x,y,z,map):
	for chest in g.chests:
		if chest.x==x and chest.y==y and chest.z==z and chest.map==map: return chest
	return None


def corpse_at(x,y,z,map):
	for corpse in g.corpses:
		if corpse.x==x and corpse.y==y and corpse.z==z and corpse.map==map: return True
	return False


def get_corpse_at(x,y,z,map):
	for corpse in g.corpses:
		if corpse.x==x and corpse.y==y and corpse.z==z and corpse.map==map: return corpse
	return None


def get_player_count_in_freedom():
	ret=0
	for p in g.players:
		if p.hidden: continue
		if p.map=="helicopter" or p.map=="massacre_in_the_city": ret+=1
	return ret


def get_current_base(p):
	for base in g.group_bases:
		if p.map=="basement"+base.name+base.mapappend: return base


def get_base_count(grp):
	a=0
	for base in g.group_bases:
		if base.name==grp: a+=1
	return a


def update_char_counter(file):
	chars=os.listdir("chars")
	for char in chars:
		charfolder=os.path.join("chars",char)
		if get_player_index_from(char)!=-1: continue
		if os.path.isfile(charfolder+"/"+file+".usr"):
			num=int(file_get_contents(charfolder+"/"+file+".usr"))
			num+=1
		else:
			num=1
		file_put_contents(charfolder+"/"+file+".usr",str(num))


def play2(sound,minx,maxx,miny,maxy,minz,maxz,map):
	for p in g.players:
		if p.map==map:
			g.n.send_reliable(p.peer_id,"playrange "+sound+".ogg "+str(minx)+" "+str(maxx)+" "+str(miny)+" "+str(maxy)+" "+str(minz)+" "+str(maxz),0)


def get_match_info():
	if len(g.matches)==0: return "There are no matches right now"
	pubmatches=0
	privmatches=0
	for m in g.matches:
		if m.password=="": pubmatches+=1
		if m.password!="": privmatches+=1
	return "There are "+str(pubmatches)+" public matches and "+str(privmatches)+" private matches right now"


def get_drawtime(w):
	if w=="knife": return 2000
	if w=="mkek_jng90": return 850
	if w=="dragunov_psl": return 1650
	if w=="mkek_mpt76k": return 1140
	if w=="m4": return 1060
	if w=="mkek_yavuz16": return 1044
	if w=="gsg5": return 1127
	if w=="KelTecP318": return 1127

	if w=="colt1911": return 628
	if w=="IthicaM37": return 648
	if w=="wooden_sword": return 974
	if w=="stone_sword": return 1000
	if w=="diamond_sword": return 1100
	if w=="fnhfnp40": return 919
	if w=="S&WModel66": return 519

	if w=="fnhfnp45": return 919
	if w=="berettaM9": return 1500

	if w=="MosinNagant": return 1350
	if w=="maverick88": return 587


class vote:
	def __init__(self,owner,title,message):
		self.title=title
		self.owner=owner
		self.message=message
		self.id=randomstring()
		self.yesvoters=[]
		self.novoters=[]
		self.ended=False
		self.timer=timer()
		self.stick=False
		self.comments=[] # NEW: List to store comments for this poll


def votecheck():
	for v in g.votes:
		if not hasattr(v,"stick"): v.stick=False
		if not v.ended and v.timer.elapsed>86400000 and not v.stick:
			v.ended=True
			for p in g.players:
				if p.votenotify==1:
					g.n.send_reliable(p.peer_id,v.owner+"'s vote has been ended",2)
					g.n.send_reliable(p.peer_id,"play_s misc162.ogg",0)


def play_delay(snd,x,y,z,map,time_wait):
	time_wait=500
	temptimer=timer()
	def func():
		while 1:
			time.sleep(0.001)
			if temptimer.elapsed>time_wait: play(snd,x,y,z,map); return
	Thread(target=func).start()


def get_task_name():
	if g.task==0: return "survive for 10 minutes"
	if g.task==1: return "eliminate 20 enemies"
	if g.task==2: return "make 50 headshots"
	if g.task==3: return "destroy 15 chests"


def get_task_description():
	if g.task==0: return "the game chooses a random player in the freedom fight map, which is announced. If the player exits the freedom fight map or game, a new player is selected. This player should survive for 10 minutes. If they get killed, killer gets 10 event points and another player is selected. If nobody can kill them, they get 10 event points and another player is selected. Each 1 minute info about the player is given. After getting 5 event points on this event (whether by successfully surviving or killing the player which is selected to survive), your event point won't increase, but your score on this event scoreboard will increase."
	if g.task==1: return "you get 10 event points for each thing you kill untill 20. After 20 kills, your event point won't increase, but your score on this event scoreboard will increase."
	if g.task==2: return "you get 10 event points for each 10 headshots you make untill 50 headshots. After 50 headshots, you won't get event points, but your score on this event scoreboard will increase"
	if g.task==3: return "you get 10 event points for each chest you destroy untill 15 chests. After 15 chests, you won't get event points, but your score in the event scoreboard will increase"


def select_random_player_from_freedom_fight_map():
	fplayers=[]
	for p in g.players:
		if p.hidden: continue
		if p.map=="massacre_in_the_city": fplayers.append(p.name)
	if len(fplayers)<=1: return ""
	return fplayers[random(0,len(fplayers))-1]


def get_task_end_time():
	time_end=86400000
	time_left=time_end-tasktimer.elapsed
	return ms_to_readable_time(time_left)


def get_task_max_point():
	if g.task==1: return 20*10
	if g.task==2: return 50*1
	if g.task==3: return 50*15


def get_task_complete_need():
	if g.task==0: return 5
	if g.task==1: return 20
	if g.task==2: return 50
	if g.task==3: return 15


def get_corpse_amount_in_map(map):
	ret=0
	for corpse in g.corpses:
		if corpse.map==map: ret+=1
	return ret

