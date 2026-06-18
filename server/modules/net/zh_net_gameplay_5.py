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

def handle_gameplay_5(e, parsed, index):
	global languages
	cmds = {"xplay", "zkusecode", "spatial_amplifier_remote", "itemdisable", "setversion", "character_selected", "throwweaponleft", "zkplacecode", "grouponline", "motd", "useitem", "weaponfire2", "aimmode", "bikehorn", "binoculars", "aim", "fire", "backup_selected", "duck", "android", "juharjksjkadjknjk12n3kjnkjn1j23kjnkjn12k3nknkn123kjnkn12k3nknk5nknkn32knkn1n1k1k", "unequip", "enter", "throwweaponright", "spatial_amplifier_choose", "regenerate2", "unduck", "silence", "fall", "create", "firestart", "bikeexit", "dropitem", "ping", "ios", "dropitemamount", "jump", "regenerate", "weaponfire", "fire2", "hardland", "land", "firestop", "unequip2", "facing", "communityonline", "travelpoint", "healthcheck"}
	subs = {"messagereport"}
	matched = False
	if len(parsed) > 0 and parsed[0] in cmds:
		matched = True
	else:
		for s in subs:
			if s in e.message:
				matched = True
				break
	if not matched:
		return False

	if parsed[0]=="enter":
		index=get_player_index(e.peer_id)
		if index>-1:
			if g.players[index].map=="helicopter" or string_contains(g.players[index].map,"helicopter",1)>-1:
				for m in g.matches:
					if m.owner==g.players[index].joinedmatch and g.players[index].map!="helicopter":
						if g.players[index].helijumptimer.elapsed<10000: g.n.send_reliable(e.peer_id,"Wait "+str(ms_to_readable_time(10000-g.players[index].helijumptimer.elapsed))+".",0); return
						g.move_player(index,g.players[index].x,g.players[index].y,119,m.get_cwmap())
						g.players[index].packet("distsound helicopterdist "+str(g.players[index].x)+" "+str(g.players[index].y+50)+" "+str(g.players[index].z)+" "+g.players[index].map, 0)
						if m.mode=="snow" or m.mode=="sniper" or m.mode=="teamk2" or m.mode=="collect" or m.mode=="teamf2" or m.mode=="sword" or m.mode=="g" or m.mode=="g2" or m.mode=="teaml" or m.mode=="minecraft":
							m.send(g.players[index].name+" jumped off the helicopter at coordinates "+str(round(g.players[index].x))+", "+str(round(g.players[index].y))+", "+str(round(g.players[index].z))+"!",2)
							m.send("play_s teammessage.ogg",0)
						else:
							m.teamsend(g.players[index].matchteam,"teammessage "+g.players[index].name+" jumped off the helicopter at coordinates "+str(g.players[index].x)+", "+str(g.players[index].y)+", "+str(g.players[index].z)+"!",0)
							m.teamsend(g.players[index].matchteam,"play_s teammessage.ogg",0)
						return
				if g.players[index].helijumptimer.elapsed<10000: g.n.send_reliable(e.peer_id,"Wait "+str(ms_to_readable_time(10000-g.players[index].helijumptimer.elapsed))+".",0); return
				g.move_player(index,g.players[index].x,g.players[index].y,70,"massacre_in_the_city")
				g.n.send_reliable(e.peer_id,"distsound helicopterdist "+str(g.players[index].x)+" "+str(g.players[index].y+50)+" "+str(g.players[index].z)+" massacre_in_the_city",0)


			if not g.players[index].can_move: return
			for ladder in g.ladders:
				if ladder.map==g.players[index].map and g.players[index].distancecheck(ladder.minx,ladder.miny,ladder.minz)<=0:
					for p in g.players:
						if p.map==ladder.map: remove_platform(p, ladder.minx, ladder.maxx, ladder.miny, ladder.maxy, ladder.minz, ladder.maxz, ladder.tile)
					g.play2("ladder_retract",ladder.minx,ladder.maxx,ladder.miny,ladder.maxy,ladder.minz,ladder.maxz,ladder.map)
					try: g.ladders.remove(ladder)
					except: pass
					g.n.send_reliable(g.players[index].peer_id,"stopmoving",0)

					name=g.players[index].name
					delay(5600)
					index=get_player_index_from(name)
					g.players[index].give("ladder",1)
					g.n.send_reliable(g.players[index].peer_id,"startmoving",0)
			if g.players[index].dead or g.players[index].stunned==True: return
			if round(g.players[index].x)==500 and round(g.players[index].y)==463 and round(g.players[index].z)==0 and g.players[index].map=="massacre_in_the_city":
				m=server_menu()
				m.intro="Select category"
				m.initial_packet="store2"
				cat=[]
				for item in store_data:
					if item["category"] not in cat: cat.append(item["category"])
				for elem in cat: m.add(elem,elem)
				m.add("View packs you bought from the shop and open them","storeview")
				if not g.players[index].ios: m.add("Go to online store website to buy zero token packs, paid account, event points, etc","onlinestore")
				if not g.players[index].ios: m.add("Copy the link of the online store web page to buy zero token packs, paid account, event points, etc","copyonlinestore")
				m.send(e.peer_id)
			if 1:
				ch=get_corpse_at_player(g.players[index])
				chl=get_corpse_at_player_length(g.players[index])
				if ch is not None :
					if chl>1:
						m=server_menu()
						m.initial_packet="corpseselect"
						m.intro="select a corpse"
						for i in range(len(g.corpses)):
							corpse=g.corpses[i]
							if corpse.map==g.players[index].map and g.players[index].distancecheck(corpse.x,corpse.y,corpse.z)==0: m.add("corpse with "+str(len(corpse.items))+" items",str(i))
						m.send(e.peer_id); return
					if ch.bomb==1:
						g.players[index].playsound("corpse_bombexplode")
						if not g.players[index].hidden: g.n.broadcast("distsound corpse_bombdist "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z)+" "+g.players[index].map+"",0)
						itemlist=""
						for i, item in enumerate(ch.items):
							if str(item)=="-1": continue
							itemlist+=str(item)+", "+str(ch.itemamounts[i])+"\n"
						g.n.send_reliable(e.peer_id,"corpse had the following items: "+itemlist,2)
						for p in g.players:
							if g.players[index].distancecheck(p.x,p.y,p.z)<=10 and p.map==g.players[index].map:
								p.health-=random(100,200)
								p.hitby=ch.owner+"'s corpse with bomb"
								p.playsoundmoving("corpse_bombhit")
						pl=g.getpc(ch.owner)
						if pl is not None and p.name!=pl.name:
							g.n.send_reliable(pl.peer_id,"you got 1 zero token because someone opened your corpse with bomb",2); pl.zhtoken+=1
						g.corpses.remove(ch); return
					m=server_menu()
					m.initial_packet="corpse"
					m.intro="corpse with "+str(len(ch.items))+" items. Use up and down keys to move between items, enter key to pick it up, escape key to close the corpse."
					corpseadd(g.players[index],ch,m)
					g.players[index].playsound("corpsemisc1")
					if len(m.menuids)<=0:
						m.add("No items","no",False)
					if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"no items",0); return
					else: m.send(e.peer_id); return



			if "basement" in g.players[index].map and round(g.players[index].x)==30 and round(g.players[index].y)==30 and round(g.players[index].z)==0:
				m=server_menu()
				m.intro="base computer"
				m.initial_packet="basecomp"
				m.add("see nearby players","near")
				m.add("change basse password","password")
				m.add("open the door","door")
				m.add("fire the gun","gun")
				m.add("see base gun ammo amount","ammo")
				m.add("base upgrades","upgrades")
				m.send(e.peer_id)
			if round(g.players[index].x)==1901 and round(g.players[index].y)==775 and round(g.players[index].z)==0 and g.players[index].map=="massacre_in_the_city":
				m=server_menu()
				m.intro="Select an item to buy"
				m.initial_packet="store3"
				for item in store_data:
					if item["category"]=="equipments": m.add(item["name"]+", requires "+item["price"]+" zero tokens, description: "+item["description"],item["name"])
				m.add("View packs you bought from the shop and open them","storeview")
				m.add("Go to online store website to buy zero token packs, paid account, event points, etc","onlinestore")
				m.add("Copy the link of the online store web page to buy zero token packs, paid account, event points, etc","copyonlinestore")
				m.send(e.peer_id)
			if round(g.players[index].x)==1450 and round(g.players[index].y)==774 and round(g.players[index].z)==0 and g.players[index].map=="massacre_in_the_city":
				m=server_menu()
				m.intro="Select an item to buy"
				m.initial_packet="store3"
				for item in store_data:
					if item["category"]=="weapons": m.add(item["name"]+", requires "+item["price"]+" zero tokens, description: "+item["description"],item["name"])
				m.add("View packs you bought from the shop and open them","storeview")
				m.add("Go to online store website to buy zero token packs, paid account, event points, etc","onlinestore")
				m.add("Copy the link of the online store web page to buy zero token packs, paid account, event points, etc","copyonlinestore")
				m.send(e.peer_id)
			if round(g.players[index].x)==111 and round(g.players[index].y)==775 and round(g.players[index].z)==0 and g.players[index].map=="massacre_in_the_city":
				m=server_menu()
				m.intro="Select an item to buy"
				m.initial_packet="store3"
				for item in store_data:
					if item["category"]=="explosives": m.add(item["name"]+", requires "+item["price"]+" zero tokens, description: "+item["description"],item["name"])
				m.add("View packs you bought from the shop and open them","storeview")
				m.add("Go to online store website to buy zero token packs, paid account, event points, etc","onlinestore")
				m.add("Copy the link of the online store web page to buy zero token packs, paid account, event points, etc","copyonlinestore")
				m.send(e.peer_id)
			if round(g.players[index].x)==300 and round(g.players[index].y)==775 and round(g.players[index].z)==0 and g.players[index].map=="massacre_in_the_city":
				m=server_menu()
				m.intro="Select an item to buy"
				m.initial_packet="store3"
				for item in store_data:
					if item["category"]=="potions": m.add(item["name"]+", requires "+item["price"]+" zero tokens, description: "+item["description"],item["name"])
				m.add("View packs you bought from the shop and open them","storeview")
				m.add("Go to online store website to buy zero token packs, paid account, event points, etc","onlinestore")
				m.add("Copy the link of the online store web page to buy zero token packs, paid account, event points, etc","copyonlinestore")
				m.send(e.peer_id)
			if round(g.players[index].x)==400 and round(g.players[index].y)==775 and round(g.players[index].z)==0 and g.players[index].map=="massacre_in_the_city":
				m=server_menu()
				m.intro="Select an item to buy"
				m.initial_packet="store3"
				for item in store_data:
					if item["category"]=="vehicles": m.add(item["name"]+", requires "+item["price"]+" zero tokens, description: "+item["description"],item["name"])
				m.add("View packs you bought from the shop and open them","storeview")
				m.add("Go to online store website to buy zero token packs, paid account, event points, etc","onlinestore")
				m.add("Copy the link of the online store web page to buy zero token packs, paid account, event points, etc","copyonlinestore")
				m.send(e.peer_id)
			if round(g.players[index].x)==1660 and round(g.players[index].y)==775 and round(g.players[index].z)==0 and g.players[index].map=="massacre_in_the_city":
				m=server_menu()
				m.intro="Select an item to buy"
				m.initial_packet="store3"
				for item in store_data:
					if item["category"]=="ammos": m.add(item["name"]+", requires "+item["price"]+" zero tokens, description: "+item["description"],item["name"])
				m.add("View packs you bought from the shop and open them","storeview")
				m.add("Go to online store website to buy zero token packs, paid account, event points, etc","onlinestore")
				m.add("Copy the link of the online store web page to buy zero token packs, paid account, event points, etc","copyonlinestore")
				m.send(e.peer_id)
			# Turret mounting check
			for base in g.group_bases:
				if base.map == g.players[index].map:
					for t in base.turrets:
						if round(g.players[index].x) == round(t.x) and round(g.players[index].y) == round(t.y) and round(g.players[index].z) == round(t.z):
							if t.operator is not None:
								g.n.send_reliable(e.peer_id, "This turret is already operated by " + t.operator.name, 0)
								return
							t.operator = g.players[index]
							g.players[index].controlled_turret = t
							g.n.send_reliable(g.players[index].peer_id, "You are now operating the turret. Use left/right arrow keys to swivel, and the fire key to shoot. Walk to step off.", 0)
							g.players[index].playsound("sitstart", True)
							return

			for base in g.group_bases:
				if g.players[index].distancecheck(base.x,base.y,base.z)<=1 and g.players[index].map==base.map:
					if base.health<2000:
						move_player(index, 0, 0, 0, "basement"+base.name+base.mapappend)
						grp=get_group(base.name)
						if grp is not None: grp.actions+=g.players[index].name+" entered the base at "+get_current_date()+"\n"
						if not g.players[index].hidden: g.n.broadcast("distsound misc38 "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z)+" "+g.players[index].map, 0)
						return
					if not base.dooron:
						g.players[index].baseact=base.name
						g.players[index].basemapappend=base.mapappend
						send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "baseopen", "Enter the password of this base")
					else:
						move_player(index, 0, 0, 0, "basement"+base.name+base.mapappend)
						g.players[index].motormove()
						grp=get_group(base.name)
						if grp is not None: grp.actions+=g.players[index].name+" entered the base at "+get_current_date()+"\n"

						if not g.players[index].hidden: g.n.broadcast("distsound misc38 "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z)+" "+g.players[index].map, 0)
						return
				if round(g.players[index].x)==0 and round(g.players[index].y)==0 and g.players[index].map=="basement"+base.name+base.mapappend:
					if base.health<2000:
						move_player(index, base.x, base.y-1, base.z, base.map); return

					if not base.dooron:
						name=g.players[index].name
						g.n.send_reliable(e.peer_id,"stopmoving",0)
						g.players[index].playsound("misc147")
						base.dooropening=True

						delay(1000)
						index=get_player_index_from(name)
						g.players[index].playsound("misc18")
						g.players[index].playsound("dooropen4")
						g.play("dooropen4",base.x,base.y,base.z,base.map)
						g.n.send_reliable(g.players[index].peer_id,"startmoving",0)
						base.dooron=True
						base.dooropening=False
						grp=get_group(g.players[index].group)
						if grp is not None: grp.actions+=g.players[index].name+" opened the base door at "+get_current_date()+"\n"

						base.doorontimer.restart()
					else:
						move_player(index, base.x, base.y-1, base.z, base.map)
						g.players[index].motormove()
						grp=get_group(base.name)
						if grp is not None: grp.actions+=g.players[index].name+" exited the base at "+get_current_date()+"\n"

			if 500 <= g.players[index].x <= 600 and 336 <= g.players[index].y <= 636 and g.players[index].z == 200 and g.players[index].map=="massacre_in_the_city":
				if g.players[index].snowcollecttimer.elapsed>=1000:
					g.players[index].snowcollecttimer.restart()
					if g.players[index].get_item_count("snowflake_shard")>=10:
						g.n.send_reliable(g.players[index].peer_id,"you can't collect more than 10 snowflake_shard",0)
						return
					g.players[index].playsound("snowhit3")
					g.players[index].give("snowflake_shard",1)

			if ("snow" in g.players[index].map or string_contains(g.players[index].map,"knife",1)>-1) and g.players[index].z==0 and not g.players[index].dead:
				if g.players[index].snowcollecttimer.elapsed>=1000:
					g.players[index].snowcollecttimer.restart()
					if g.players[index].get_item_count("snowflake_shard")>=5:
						g.n.send_reliable(g.players[index].peer_id,"you can't collect more than 5 snowflake_shard",0)
						return
					g.players[index].playsound("snowhit3")
					g.players[index].give("snowflake_shard",1)
			# --- Transit Bus Boarding (Enter key) ---
			if g.players[index].in_bus and g.players[index].bus_instance is not None:
				bus = g.players[index].bus_instance
				local_x = g.players[index].local_x
				local_y = g.players[index].local_y
				player = g.players[index]
				if player.map != bus.map:
					return
				if local_x in (1, 2, 5, 6) and 2 <= local_y <= 13:
					if not getattr(g.players[index], "sitting", False):
						g.players[index].sitting = True
						g.players[index].playsound("sitstart", True)
						g.n.send_reliable(g.players[index].peer_id, "sitstart", 0)
						g.n.send_reliable(g.players[index].peer_id, "You sat down on the seat.", 0)
					else:
						g.players[index].sitting = False
						g.players[index].playsound("sitstart", True)
						g.n.send_reliable(g.players[index].peer_id, "sitstop", 0)
						g.n.send_reliable(g.players[index].peer_id, "You stood up.", 0)
				else:
					# Door control only works while the player is at the bus threshold.
					at_front_door = player.local_x in (3, 4) and player.local_y == 1
					at_rear_door = player.local_x in (3, 4) and player.local_y == 14
					if at_front_door or at_rear_door:
						if not bus.doors_open:
							bus.doors_open = True
							g.play("bus_doors_sound_effect", bus.x, bus.y, bus.z, bus.map)
							g.n.send_reliable(g.players[index].peer_id, "Doors opened.", 0)
						else:
							bus.doors_open = False
							g.play("bus_closing_door", bus.x, bus.y, bus.z, bus.map)
							g.n.send_reliable(g.players[index].peer_id, "Doors closed.", 0)
					else:
						g.n.send_reliable(g.players[index].peer_id, "Move to the door threshold before pressing Enter.", 0)
				return
			# --- End Transit Boarding ---
			if g.players[index].vi>-1: g.n.send_reliable(e.peer_id,"echo motorengine",0); return
			if g.players[index].specplayer!="": return
			while True:
				if not g.pathfinding: gameloops()
				should_break=True
				for i in range(len(g.items)):
					if not g.players[index].zombie and get_3d_distance(g.players[index].x,g.players[index].y,g.players[index].z,g.items[i].x,g.items[i].y,g.items[i].z)<=4 and g.players[index].map==g.items[i].map:
						if g.items[i].fake:
							g.players[index].playsound("fakeitem")
							if not g.players[index].hidden: g.n.broadcast("distsound fakeitemdist "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z)+" "+g.players[index].map+"",0)
							for p in g.players:
								if g.players[index].distancecheck(p.x,p.y,p.z)<=5 and p.map==g.players[index].map:
									p.health-=random(60,90)
									p.hitby="boom box"
									p.playsoundmoving("planebombhit")
							pl=g.getpc(g.items[i].owner)
							if pl is not None:
								g.n.send_reliable(pl.peer_id,"you got 1 zero token because someone picked up your boom box",2); pl.zhtoken+=1
							g.items.remove(g.items[i]); return

						amount=g.items[i].itemamount
						if g.items[i].itemname in g.invlimits and g.players[index].get_item_count(g.items[i].itemname)+g.items[i].itemamount>g.players[index].get_backpack_level_amount(g.invlimits[g.items[i].itemname]): amount=g.players[index].get_backpack_level_amount(g.invlimits[g.items[i].itemname])-g.players[index].get_item_count(g.items[i].itemname)
						if amount<=0:
							g.n.send_reliable(g.players[index].peer_id,"Your inventory cannot hold more of this item",0)
							continue

						g.players[index].give(g.items[i].itemname,amount)
						g.players[index].items_got+=1
						if g.players[index].matchmode=="teamcollect":
							for match in g.matches:
								if match.owner==g.players[index].joinedmatch:
									if g.players[index].matchteam=="red": match.redgot+=1
									if g.players[index].matchteam=="blue": match.bluegot+=1
						for p2 in g.players:
							if p2.specplayer==g.players[index].name: g.n.send_reliable(p2.peer_id,""+str(amount)+" "+str(g.items[i].itemname)+"",2)

						should_break=False
						g.n.send_reliable(g.players[index].peer_id,"itemmessage "+str(g.items[i].itemamount)+" "+str(g.items[i].itemname)+"",0)
						if g.items[i].itemname=="small_potion" or g.items[i].itemname=="vitality_potion" or g.items[i].itemname=="revival_nectar":
							g.play("getcola2",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
						elif g.items[i].itemname=="5.56x45mm":
							g.play("getmachinegunammo",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
						elif g.items[i].itemname=="mkek_jng90":
							g.play("mkek_jng90draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
						elif g.items[i].itemname=="dragunov_psl":
							g.play("dragunov_psldraw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

						elif g.items[i].itemname=="mkek_mpt76k":
							g.play("mkek_mpt76kdraw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
						elif g.items[i].itemname=="m4":
							g.play("m4draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

						elif g.items[i].itemname=="mkek_yavuz16":
							g.play("mkek_yavuz16draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
						elif g.items[i].itemname=="gsg5":
							g.play("gsg5draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
						elif g.items[i].itemname=="KelTecP318":
							g.play("KelTecP318draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

						elif g.items[i].itemname=="fnhfnp40":
							g.play("fnhfnp40draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
						elif g.items[i].itemname=="fnhfnp45":
							g.play("fnhfnp45draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
						elif g.items[i].itemname=="berettaM9":
							g.play("ks123shotgundraw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

						elif g.items[i].itemname=="S&WModel66":
							g.play("S&WModel66draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

						elif g.items[i].itemname=="colt1911":
							g.play("colt1911draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

						elif g.items[i].itemname=="IthicaM37":
							g.play("IthicaM37draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
						elif g.items[i].itemname=="maverick88":
							g.play("maverick88draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

						elif g.items[i].itemname=="MosinNagant":
							g.play("MosinNagantdraw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

						elif g.items[i].itemname=="9mm":
							g.play("getpistolammo",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
						elif g.items[i].itemname=="12_gauge":
							g.play("getshotgunammo",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
						elif g.items[i].itemname=="7.62x51mm":
							g.play("getsniperammo",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
						elif g.items[i].itemname=="molotov_cocktail":
							g.play("getmoolotov",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
						elif g.items[i].itemname=="hand_grenade":
							g.play("getparachute",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
						elif g.items[i].itemname=="m4":
							g.play("m4draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

						elif g.items[i].itemname=="binoculars":
							g.play("binocularsclose",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
						elif g.items[i].itemname=="wooden_sword":
							g.play("getwooden_sword",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
						elif g.items[i].itemname=="stone_sword":
							g.play("getstone_sword",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
						elif g.items[i].itemname=="diamond_sword":
							g.play("getdiamond_sword",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

						else:
							g.play("itemget",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
						if amount==g.items[i].itemamount: g.items.pop(i)
						else: g.items[i].itemamount-=amount

						break
				if should_break: break
			if 1:
				ch=get_chest_at_player(g.players[index])
				if ch is not None :
					g.players[index].playsound("chest8")
					minefound=False
					for mine in g.mines:
						if ch.x==mine.x and ch.y==mine.y and ch.z==mine.z and ch.map==mine.map: mine.health=0; minefound=True
					if minefound: return
					m=server_menu()
					m.initial_packet="chest"
					m.intro="Chest with "+str(len(ch.items))+" items. Use up and down keys to move between items, enter key to pick it up, escape key to close the chest."
					chestadd(g.players[index],ch,m)
					if len(m.menuids)<=0:
						m.add("No items","no",False)
					if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"no items",0); return
					else: m.send(e.peer_id); return
				for transit in g.transits:
					if transit.map == g.players[index].map and get_3d_distance(g.players[index].x, g.players[index].y, g.players[index].z, transit.x, transit.y, transit.z) <= 5:
						transit.add_passenger(g.players[index])
						return
				for b in g.bikes:
					if round(g.players[index].x)==round(b.x) and round(g.players[index].y)==round(b.y) and round(g.players[index].z)==round(b.z) and g.players[index].map==b.map:
						b.add_player(index); return
				for i in range(len(g.motors)):
					if round(g.players[index].x)==round(g.motors[i].x) and round(g.players[index].y)==round(g.motors[i].y) and round(g.players[index].z)==round(g.motors[i].z)+5 and g.players[index].map==g.motors[i].map:
						if g.players[index].inve==False:
							if len(g.motors[i].players)==g.motors[i].maxplayers: g.n.send_reliable(e.peer_id,"Motor full",0); return
							g.players[index].playsound("motorenter")
							g.players[index].inve=True
							send_reliable(g.players[index].peer_id, "motorspawn", 0)
							g.players[index].vi=i
							g.motors[i].players.append(g.players[index].name)
							g.players[index].z-=5
							g.n.send_reliable(e.peer_id,"move "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z),0)
			for m in g.matches:
				if not m.started and not m.starting and g.players[index].name==m.owner:
					m2=server_menu()
					m2.intro="Select an option"
					m2.initial_packet="matchoption"
					m2.add("start match","start")
					if m.password!="": m2.add("invite player","invite")
					m2.add("kick player","kick")
					m2.add("ban player","ban")
					m2.add("unban player","unban")
					m2.add("cancel match","cancel")
					m2.add("back","back")
					m2.send(e.peer_id)
				if not m.started and g.players[index].name!=m.owner and g.players[index].joinedmatch==m.owner and g.players[index].map.startswith("match"):
					m2=server_menu()
					m2.intro="Select an option"
					m2.initial_packet="matchoption"
					m2.add("leave match","leave")
					m2.send(e.peer_id)
			for f in g.flags:
				if g.players[index].map==f.map and g.players[index].distancecheck(f.x,f.y,f.z)<=2:
					for match in g.matches:
						if g.players[index].joinedmatch==match.owner:
							if f.team=="red" and g.players[index].matchteam=="blue":
								g.players[index].playsound("flag"+str(random(1,1))+"")
								match.send(g.players[index].name+" got the red flag!",2)
								g.players[index].flag+=1
								try: g.flags.remove(f)
								except: pass



							elif f.team=="blue" and g.players[index].matchteam=="red":
								match.send(g.players[index].name+" got the blue flag!",2)
								g.players[index].playsound("flag1")
								g.players[index].flag+=1
								try: g.flags.remove(f)
								except: pass
							else: g.n.send_reliable(e.peer_id,"This flag is not opposing teams",0)
			if round(g.players[index].x)==0 and round(g.players[index].y)==0 and round(g.players[index].z)==0 and g.players[index].matchteam=="red" and g.players[index].flag>0 and g.players[index].joinedmatch!="":
				g.players[index].flag-=1
				for match in g.matches:
					if g.players[index].joinedmatch==match.owner:
						match.blueflagpoint+=1
						match.send(g.players[index].name+" put the blue flag! "+str(10-match.blueflagpoint)+" more flags needed",2)
						g.play("flag3",g.players[index].x,g.players[index].y,g.players[index].z,g.players[index].map)
						spawn_flag(random(0, 100), random(0, 100), 0, match.get_cwmap(), "blue")
						match.send("play_s misc160.ogg",0)

						if match.blueflagpoint>=10:
							match.send("Match ended. "+g.players[index].matchteam+" team won!",2)
							match.teamsend("blue","play_s misc171.ogg",0)
							match.teamsend("red","play_s win.ogg",0)
							#match.givezhtokenteam("blue")
							for i in range(len(match.players)): g.move_player(g.get_player_index_from(match.players[i]),5,0,0,"lobby")
							file_delete("maps/match"+match.owner+".map")
							file_delete("maps/flag"+match.owner+".map")
							g.init_mapsystem()
							g.matches.remove(match)
							return
						match.teamsend("red","play_s flag5.ogg",0)
			if round(g.players[index].x)==100 and round(g.players[index].y)==100 and round(g.players[index].z)==0 and g.players[index].matchteam=="blue" and g.players[index].flag>0 and g.players[index].joinedmatch!="":
				g.players[index].flag-=1
				for match in g.matches:
					if g.players[index].joinedmatch==match.owner:
						match.redflagpoint+=1
						match.send(g.players[index].name+" put the red flag! "+str(10-match.redflagpoint)+" more flags needed",2)
						g.play("flag3",g.players[index].x,g.players[index].y,g.players[index].z,g.players[index].map)
						spawn_flag(random(0, 100), random(0, 100), 0, match.get_cwmap(), "red")
						match.send("play_s misc160.ogg",0)

						if match.redflagpoint>=10:
							match.send("Match ended. "+g.players[index].matchteam+" team won!",2)
							#match.givezhtokenteam(g.players[index].matchteam)
							match.teamsend("red","play_s misc171.ogg",0)
							match.teamsend("blue","play_s win.ogg",0)

							for i in range(len(match.players)): g.move_player(g.get_player_index_from(match.players[i]),5,0,0,"lobby")

							file_delete("maps/match"+match.owner+".map")
							file_delete("maps/flag"+match.owner+".map")
							g.init_mapsystem()
							g.matches.remove(match)

						match.teamsend("blue","play_s flag5.ogg",0)
			if (g.players[index].map == "lobby" and 4 <= round(g.players[index].x) <= 6 and 0 <= round(g.players[index].y) <= 4 and round(g.players[index].z) == 0):
#					move_player(index,random(0,500),random(0,500),0,"main")
#					g.n.send_reliable(g.players[index].peer_id,"Joined to the battleground",2)
#					g.n.send_reliable(g.players[index].peer_id,"play_s voice23.ogg",0)
				if g.gamestop==1 or g.players[index].in_match_menu:
					return
				m=server_menu()
				m.intro="Please select an option."
				m.initial_packet="matchmenu"
				m.add("create a match","create")
				m.add("join or spectate a match, "+get_match_info(),"join")
				m.add("go to freedom fight map, there are "+str(get_player_count_in_freedom())+" players in the freedom fight map","free")
				m.add("Watch your friends in freedom fight map, there are "+str(get_player_count_in_freedom())+" players in the freedom fight map, and "+str(g.players[index].get_friend_count_in_freedom())+" of them are your friends.","watch")
				if g.players[index].is_admin() or g.players[index].moderator==True or g.players[index].dev==True:
					m.add("Watch anyone in freedom fight map (admin), watch any player currently in the freedom fight map.","watchadmin")
				m.send(e.peer_id)
				g.players[index].in_match_menu=True

			ind=get_map_index(g.players[index].map)
			if ind>-1:
				mdata=g.maps[ind].rawdata
				p1=delinear(mdata)
				for i in range(len(p1)):
					parsed=string_split(p1[i], ":", True)
					if parsed[0]=="travelpoint" and len(parsed)>11:
						minx=string_to_number(parsed[1])
						maxx=string_to_number(parsed[2])
						miny=string_to_number(parsed[3])
						maxy=string_to_number(parsed[4])
						minz=string_to_number(parsed[5])
						maxz=string_to_number(parsed[6])
						newmap=parsed[7]
						newx=string_to_number(parsed[8])
						newy=string_to_number(parsed[9])
						newz=string_to_number(parsed[10])
						text=parsed[11]
						if minx<=g.players[index].x and maxx>=g.players[index].x and miny<=g.players[index].y and maxy>=g.players[index].y and minz<=g.players[index].z and maxz>=g.players[index].z:
							move_player(index, newx, newy, newz, newmap, True)
							g.n.send_reliable(g.players[index].peer_id, text, 2)

	elif(parsed[0]=="ping"):
	
		g.n.send_reliable(e.peer_id,"pong",0)
		
	elif(parsed[0]=="dropitem" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index > -1):
		
			if "helicopter" in g.players[index].map or g.players[index].map=="jail": return
			item=parsed[1]
			if "collect" in g.players[index].map: return
			if g.players[index].weapon==item:
				if "minecraft" in g.players[index].map: g.n.send_reliable(e.peer_id,"draw stick",0); g.players[index].weapon="stick"
				if "minecraft" not in g.players[index].map: g.n.send_reliable(e.peer_id,"drawsilent punch",0); g.players[index].weapon="punch"
			if g.players[index].weapon2==item:
				if "minecraft" in g.players[index].map: g.n.send_reliable(e.peer_id,"draw stick",0); g.players[index].weapon="stick"
				if "minecraft" not in g.players[index].map: g.n.send_reliable(e.peer_id,"draw2silent feet",0); g.players[index].weapon2="feet"

			if item in g.dontlose: g.n.send_reliable(e.peer_id,"You can't drop persistent items!",0); return
			if(g.players[index].get_item_count(item)>=1):
				g.players[index].playsound("inventorydrop"+str(random(2,3))+"")
				g.players[index].give(item,-1)
				for it in g.items:
					if it.map==g.players[index].map and it.dropped and g.players[index].distancecheck(it.x,it.y,it.z)<=4 and it.itemname==item: it.itemamount+=1; return
				spawn_item(round(g.players[index].x),round(g.players[index].y),round(g.players[index].z),g.players[index].map,item,1,True,pindex=index)

	elif(parsed[0]=="dropitemamount" and len(parsed)>2):
	
		index=g.get_player_index(e.peer_id)
		if(index > -1):
		
			item=parsed[1]
			if "helicopter" in g.players[index].map or g.players[index].map=="jail": return
			if item in g.players[index].silenced: g.players[index].silenced.remove(item)
			amount=int(parsed[2])
			if amount<=0: g.n.send_reliable(e.peer_id,"amount must be higher than zero",0); return
			if g.players[index].weapon==item:
				if "minecraft" in g.players[index].map: g.n.send_reliable(e.peer_id,"draw stick",0); g.players[index].weapon="stick"
				if "minecraft" not in g.players[index].map: g.n.send_reliable(e.peer_id,"drawsilent punch",0); g.players[index].weapon="punch"
			if g.players[index].weapon2==item:
				if "minecraft" in g.players[index].map: g.n.send_reliable(e.peer_id,"draw stick",0); g.players[index].weapon="stick"
				if "minecraft" not in g.players[index].map: g.n.send_reliable(e.peer_id,"draw2silent feet",0); g.players[index].weapon2="feet"


			if item in g.dontlose: g.n.send_reliable(e.peer_id,"You can't drop persistent items!",0); return
			if(g.players[index].get_item_count(item)>=1):
				g.players[index].playsound("inventorydrop"+str(random(2,3))+"")
				g.players[index].give(item,-amount)
				for it in g.items:
					if it.map==g.players[index].map and it.dropped and g.players[index].distancecheck(it.x,it.y,it.z)<=4 and it.itemname==item: it.itemamount+=amount; return
				spawn_item(round(g.players[index].x),round(g.players[index].y),round(g.players[index].z),g.players[index].map,item,amount,True)



	elif(parsed[0]=="binoculars" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index > -1):
			g.players[index].playsound("binocularsclose")
			if parsed[1]!="back": g.players[index].binocularsplayer=parsed[1]
	elif parsed[0]=="grouponline":
	
		index=g.get_player_index(e.peer_id)
		if(index > -1):
			if g.players[index].group=="": g.n.send_reliable(g.players[index].peer_id,"you are not member of any group",2); return
			m=server_menu()
			m.intro="online players in your group"
			m.initial_packet="grouponlinee"
			for pl in g.players:
				if pl.hidden: continue
				if pl.group==g.players[index].group: m.add(pl.name,pl.name,False)
			m.send(e.peer_id)
	elif parsed[0]=="communityonline":
	
		index=g.get_player_index(e.peer_id)
		if(index > -1):
			if g.players[index].community=="": g.n.send_reliable(g.players[index].peer_id,"you are not member of any community",2); return
			m=server_menu()
			m.intro="online players in your community"
			m.initial_packet="communityonlinee"
			for pl in g.players:
				if pl.hidden: continue
				if pl.community==g.players[index].community: m.add(pl.name,pl.name,False)
			m.send(e.peer_id)

	elif(parsed[0]=="spatial_amplifier_choose" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index > -1):
			if parsed[1]=="back": return
			ind=get_player_index_from(g.players[index].spatialplayer)
			if parsed[1]=="destroy" and g.players[ind].spatialized_by!="":
				if g.players[ind].map=="lobby" or "match" in g.players[ind].map: g.n.send_reliable(e.peer_id,"action cannot be performed when player is in the lobby or match waiting area",0); g.players[index].prevmenu(); return
				g.players[ind].playsoundmoving("misc339")
				g.players[ind].playsound("minehit")
				g.players[ind].health-=random(90,140)
				g.players[ind].hitby=g.players[index].name+"'s spatial amplifier"
				for ind2 in range(len(g.players)):
					if g.players[ind2].distancecheck(g.players[ind].x,g.players[ind].y,g.players[ind].z)<=20 and g.players[ind].map==g.players[ind2].map and g.players[ind].name!=g.players[ind2].name:
						g.players[ind2].playsound("minehit")
						g.players[ind2].health-=random(90,140)
						g.players[ind2].hitby=g.players[index].name+"'s spatial amplifier"

				for p in g.players:
					if p.map==g.players[ind].map:
						g.n.send_reliable(p.peer_id,"distsound tayfundist3 "+str(g.players[ind].x)+" "+str(g.players[ind].y)+" "+str(g.players[ind].z)+" "+g.players[ind].map,0)
				g.players[ind].spatialized_by=""
			if parsed[1]=="map":
				if g.players[ind].map!=g.players[index].map: g.n.send_reliable(e.peer_id,"this action cannot be performed when player is in a different map",0); return
				g.n.send_reliable(e.peer_id,"Player Coordinates: "+str(round(g.players[ind].x))+", "+str(round(g.players[ind].y))+", "+str(round(g.players[ind].z))+". Health: "+str(g.players[ind].health),0); g.players[index].prevmenu(); return
	elif(parsed[0]=="spatial_amplifier_remote" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index > -1):
			if parsed[1]=="back": return
			m=server_menu()
			m.intro="select an action"
			m.initial_packet="spatial_amplifier_choose"
			g.players[index].spatialplayer=parsed[1]
			ind=get_player_index_from(g.players[index].spatialplayer)
			m.add("destroy the item","destroy")
			m.add("see player coordinates and health","map")
			m.add("the item will expire after "+str(ms_to_readable_time(600000-g.players[ind].spatializertimer.elapsed)),"time",False)
			m.send(e.peer_id)
	elif parsed[0]=="silence":
		index=g.get_player_index(e.peer_id)
		if(index > -1):
			if parsed[1]=="left":
				if 1:
					if g.players[index].weapon not in guns: g.n.send_reliable(e.peer_id,"silencer not usable for this weapon",0); 						g.players[index].weapon_rays=None; 						g.players[index].weapon_rays2=None; return
					if g.players[index].weapon not in snipers and g.players[index].weapon not in machineguns and g.players[index].weapon not in pistols: g.n.send_reliable(e.peer_id,"silencer not usable for this weapon",0); 						g.players[index].weapon_rays=None; 						g.players[index].weapon_rays2=None; return
					p=g.players[index]
					if g.players[index].weapon in g.players[index].silenced: g.players[index].silenced.remove(g.players[index].weapon); g.players[index].playsound("misc327"); g.n.send_reliable(p.peer_id,"stopmoving",0); name=g.players[index].name; delay(1500); index=get_player_index_from(name); p=g.players[index]; g.n.send_reliable(p.peer_id,"startmoving",0); g.n.send_reliable(p.peer_id,"silencer off for "+g.players[index].weapon,0); g.players[index].weapon_rays=None; g.players[index].weapon_rays2=None; return
					if g.players[index].weapon not in g.players[index].silenced:
						if len(g.players[index].silenced)>=g.players[index].get_item_count("silencer"): g.n.send_reliable(e.peer_id,"you do not have more silencer to insert to this weapon",0); return
						p=g.players[index]
						g.players[index].silenced.append(g.players[index].weapon); name=g.players[index].name; g.players[index].playsound("misc323"); g.n.send_reliable(p.peer_id,"stopmoving",0); delay(1500); index=get_player_index_from(name); p=g.players[index]; g.n.send_reliable(p.peer_id,"startmoving",0); g.n.send_reliable(p.peer_id,"silencer on for "+g.players[index].weapon,0); g.players[index].weapon_rays=None; g.players[index].weapon_rays2=None; return
			if parsed[1]=="right":
				if 1:
					if g.players[index].weapon2 not in guns: g.n.send_reliable(e.peer_id,"silencer not usable for this weapon",0); 						g.players[index].weapon_rays=None; 						g.players[index].weapon_rays2=None; return
					if g.players[index].weapon2 not in snipers and g.players[index].weapon2 not in machineguns and g.players[index].weapon2 not in pistols: g.n.send_reliable(e.peer_id,"silencer not usable for this weapon",0); 						g.players[index].weapon_rays=None; 						g.players[index].weapon_rays2=None; return
					p=g.players[index]
					if g.players[index].weapon2 in g.players[index].silenced: g.players[index].silenced.remove(g.players[index].weapon2); g.players[index].playsound("misc327"); g.n.send_reliable(p.peer_id,"stopmoving",0); name=g.players[index].name; delay(1500); index=get_player_index_from(name); p=g.players[index]; g.n.send_reliable(p.peer_id,"startmoving",0); g.n.send_reliable(p.peer_id,"silencer off for "+g.players[index].weapon2,0); g.players[index].weapon_rays=None; g.players[index].weapon_rays2=None; return
					if g.players[index].weapon2 not in g.players[index].silenced:
						if len(g.players[index].silenced)>=g.players[index].get_item_count("silencer"): g.n.send_reliable(e.peer_id,"you do not have more silencer to insert to this weapon",0); return
						p=g.players[index]
						g.players[index].silenced.append(g.players[index].weapon2); g.players[index].playsound("misc323"); g.n.send_reliable(p.peer_id,"stopmoving",0); name=g.players[index].name; delay(1500); index=get_player_index_from(name); p=g.players[index]; g.n.send_reliable(p.peer_id,"startmoving",0); g.n.send_reliable(p.peer_id,"silencer on for "+g.players[index].weapon2,0); g.players[index].weapon_rays=None; g.players[index].weapon_rays2=None; return



	elif(parsed[0]=="useitem" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index > -1):
		
			item=parsed[1]
			if "collect" in g.players[index].map or not g.players[index].can_move or g.players[index].faint or g.players[index].map.startswith("match") or g.players[index].stunned==True: return
			if "helicopter" in g.players[index].map: return
			if(g.players[index].get_item_count(item)>=1):
			
				takeobj=False
				if item=="corpse_scanner":
					takeobj=True
					pname=g.players[index].name
					g.players[index].playsound("corpse_scanner")
					g.n.send_reliable(e.peer_id,"stopmoving",0)
					delay(2000)
					index=get_player_index_from(pname)
					g.n.send_reliable(g.players[index].peer_id,"startmoving",0)
					sendtext="there are "+str(get_corpse_amount_in_map(g.players[index].map))+" corpses in this map. "
					for i in g.corpses:
						if i.map==g.players[index].map:
							sendtext+=i.owner+"'s corpse, at "+str(round(i.x))+" "+str(round(i.y))+" "+str(round(i.z))+", it has "+str(len(i.items))+" items, will be gone after "+str(ms_to_readable_time(600000-i.gotimer.elapsed))+"\n"
					g.n.send_reliable(g.players[index].peer_id,sendtext,2)
				if item=="boom_box":
					g.players[index].playsound("fakeitemplace")
					name=g.players[index].name
					g.n.send_reliable(e.peer_id,"stopmoving",0)
					delay(900)
					index=g.get_player_index_from(name)
					g.n.send_reliable(g.players[index].peer_id,"startmoving",0)
					itemlist={"silencer":1,"berettaM9":1,"357_magnum":10,"S&WModel66":1,"invisibility_shield":1,"fnhfnp45":1,"knife":1,"barricade":1,"ladder":1,"tm62":1,"7.62x54mmR":10,"metal_shield":1,"steel_helmet":1,"vitality_potion":1,"timebomb":1,"22_LR_Long_Rifle":30,"gsg5":1,"base_life_amplifier":9,"dragunov_psl":1,"fnhfnp40":1,"40S&W":40,"parachute":1,"mkek_jng90":1,"mkek_mpt76k":1,"m4":1,"mkek_yavuz16":1,"colt1911":1,"IthicaM37":1,"wooden_sword":1,"stone_sword":1,"diamond_sword":1,"molotov_cocktail":4,"7.62x51mm":20,"5.56x45mm":50,"9mm":20,"45_ACP":20,"12_gauge":15,"40S&W":50,"revival_nectar":1,"small_potion":2,"binoculars":1,"hand_grenade":3}
					item=choice(list(itemlist.keys()))
					amount=random(1,itemlist[item])
					spawn_item(round(g.players[index].x),round(g.players[index].y),round(g.players[index].z),g.players[index].map,item,amount,False)
					g.items[len(g.items)-1].fake=True
					g.items[len(g.items)-1].owner=g.players[index].name
					g.players[index].give("boom_box",-1); return
				if item=="corpse_bomb":
					takeobj=False
					if g.players[index].corpse_bomb==0:
						g.players[index].playsound("corpse_bombwear")
						name=g.players[index].name
						g.n.send_reliable(e.peer_id,"stopmoving",0)
						delay(4380)
						index=g.get_player_index_from(name)
						g.n.send_reliable(g.players[index].peer_id,"startmoving",0)
						g.n.send_reliable(g.players[index].peer_id,"corpse bomb on",0)
						g.players[index].corpse_bomb=1
					elif g.players[index].corpse_bomb==1:
						g.players[index].playsound("remove_corpse_bomb")
						name=g.players[index].name
						g.n.send_reliable(e.peer_id,"stopmoving",0)
						delay(5019)
						index=g.get_player_index_from(name)
						g.n.send_reliable(g.players[index].peer_id,"startmoving",0)
						g.n.send_reliable(g.players[index].peer_id,"corpse bomb off",0)
						g.players[index].corpse_bomb=0

				if item=="spatial_amplifier":
					takeobj=False
					for p in g.players:
						if p.map==g.players[index].map and get_3d_distance(p.x,p.y,p.z,g.players[index].x,g.players[index].y,g.players[index].z)<=5 and p.name!=g.players[index].name:
							if p.spatialized_by==g.players[index].name: g.n.send_reliable(e.peer_id,"you already used spatial amplifier on this player",0); return
							g.players[index].playsound("remote_place5")
							g.players[index].stunned=True
							g.players[index].stuntime=800
							g.players[index].stuntimer.restart()
							g.n.send_reliable(p.peer_id,"stopmoving",0)
							g.n.send_reliable(e.peer_id,"stopmoving",0)
							p.stunned=True
							p.stuntime=800
							p.stuntimer.restart()

							p.spatialized_by=g.players[index].name
							p.spatializertimer.restart(); takeobj=True; break
					if not takeobj: g.n.send_reliable(e.peer_id,"no player nearby 5 tiles",0)
				if item=="spatial_amplifier_controller":
					takeobj=False
					m=server_menu()
					m.intro="select a player"
					m.initial_packet="spatial_amplifier_remote"
					for p in g.players:
						if p.spatialized_by==g.players[index].name: m.add(p.name,p.name)
					if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"no one",0); return
					m.send(e.peer_id)
				if item=="adrenaline_shot":
					takeobj=False
					if g.players[index].adrenaline: g.n.send_reliable(e.peer_id,"adrenaline shot already on",0); return
					takeobj=True
					g.n.send_reliable(g.players[index].peer_id,"stopmoving",0)
					g.players[index].playsoundmoving("ultra_health_potion")
					name=g.players[index].name
					delay(5000)
					index=g.get_player_index_from(name)
					g.n.send_reliable(g.players[index].peer_id,"startmoving",0)
					g.players[index].adrenaline=True
					file_put_contents("chars/"+g.players[index].name+"/adrenaline.usr","")
					if g.players[index].weapon!="": 					g.n.send_reliable(g.players[index].peer_id,"weapondatafast "+g.wdata[g.players[index].weapon],0)
					if g.players[index].weapon2!="": 					g.n.send_reliable(g.players[index].peer_id,"weapondata2fast "+g.wdata[g.players[index].weapon2],0)
					g.players[index].adrenalinetimer.restart()
				if item=="jammer":
					takeobj=False
					jplayers=""
					for i in g.players:
						if i.name!=g.players[index].name and i.distancecheck(g.players[index].x,g.players[index].y,g.players[index].z)<=50 and i.map==g.players[index].map:
							if i.jammer: continue
							i.jammer=True
							file_put_contents("chars/"+i.name+"/jammer.usr","")
							g.n.send_reliable(i.peer_id,g.players[index].name+" used jammer, you cannot use binoculars and you cannot check near players with e/p for 2 minutes",2)
							takeobj=True
							jplayers+=i.name+", "
							i.playsound("jammerinuse")
							
							i.jammertimer.restart()
					if jplayers!="": 								g.players[index].playsound("jammerinuse")
					if jplayers=="": g.n.send_reliable(e.peer_id,"no one within 50 steps",0)
					else: g.n.send_reliable(e.peer_id,"players affected by jammer: "+jplayers,2)
				if item=="parachute":
					takeobj=False
					if g.players[index].parachuted==False:
						if g.players[index].usetimer.elapsed>=1000:
							g.players[index].usetimer.restart()
							g.players[index].parachuted=True
							g.n.send_reliable(g.players[index].peer_id,"stopmoving",0)
							g.players[index].playsound("parachuteopen")
							if not g.players[index].hidden: g.n.broadcast("distsound parachute_dist "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z)+" "+g.players[index].map, 0)
							g.n.send_reliable(g.players[index].peer_id, "parachute_start", 0)
							for i in g.players:
								if i.specplayer==g.players[index].name: g.n.send_reliable(i.peer_id,"parachute_start",0)
							g.players[index].get_char_properties()

							return
					if g.players[index].parachuted==True:
						if g.players		[index].usetimer.elapsed>=1000:
							g.players[index].usetimer.restart()
#								takeobj=True
							g.players[index].parachuted=False
							g.n.send_reliable(g.players[index].peer_id,"startmoving",0)
							g.players[index].playsound("parachuteclose")
							g.n.send_reliable(g.players[index].peer_id, "parachute_stop", 0)
							for i in g.players:
								if i.specplayer==g.players[index].name: g.n.send_reliable(i.peer_id,"parachute_stop",0)

							g.players[index].get_char_properties()
							g.players[index].get_weapon_properties(g.players[index].weapon)
				if item=="binoculars":
					takeobj=False
					index=g.players[index]
					m=server_menu()
					m.intro="Use up and down arrows to see players within 120 steps, escape to close the binoculars"
					m.initial_packet="binoculars"
					for i in range(len(g.players)):
					
						if g.get_hidden_area_at(g.players[i].x,g.players[i].y,g.players[i].z,g.players[i].map)!=g.get_hidden_area_at(index.x,index.y,index.z,index.map): continue
						if g.players[i].dead: continue
						if g.players[i].dead: continue
						if g.players[i].invisible: continue
						if g.players[i].hidden: continue
						if (g.players[i].x<index.x+120 and g.players[i].x>index.x-120 and g.players[i].y<index.y+120 and g.players[i].y>index.y-120 and g.players[i].z<index.z+120 and g.players[i].z>index.z-120 and g.players[i].map==index.map and g.players[i].name!=index.name):
							if index.jammer: m.add("Device cannot operate","operate",False); break
							if not g.players[i].ducking:
								if not g.players[i].zombie:
									if g.players[i].faint and g.players[i].fainted: m.add("faint "+g.players[i].name+" at "+str(round(g.players[i].x))+", "+str(round(g.players[i].y))+", "+str(round(g.players[i].z))+" with "+str(g.players[i].health)+" hp ("+str(round(get_3d_distance(g.players[i].x,g.players[i].y,g.players[i].z,index.x,index.y,index.z)))+" feet.\n",str(g.players[i].name))
									if not g.players[i].faint and not g.players[i].fainted: m.add(g.players[i].name+" at "+str(round(g.players[i].x))+", "+str(round(g.players[i].y))+", "+str(round(g.players[i].z))+" with "+str(g.players[i].health)+" hp ("+str(round(get_3d_distance(g.players[i].x,g.players[i].y,g.players[i].z,index.x,index.y,index.z)))+" feet.\n",str(g.players[i].name))
								if  g.players[i].zombie:
									if g.players[i].faint and g.players[i].fainted: m.add("zombie faint "+g.players[i].name+" at "+str(round(g.players[i].x))+", "+str(round(g.players[i].y))+", "+str(round(g.players[i].z))+" with "+str(g.players[i].health)+" hp ("+str(round(get_3d_distance(g.players[i].x,g.players[i].y,g.players[i].z,index.x,index.y,index.z)))+" feet.\n",str(g.players[i].name))
									if not g.players[i].faint and not g.players[i].fainted: m.add("zombie "+g.players[i].name+" at "+str(round(g.players[i].x))+", "+str(round(g.players[i].y))+", "+str(round(g.players[i].z))+" with "+str(g.players[i].health)+" hp ("+str(round(get_3d_distance(g.players[i].x,g.players[i].y,g.players[i].z,index.x,index.y,index.z)))+" feet.\n",str(g.players[i].name))

							elif g.players[i].ducking:
								if not g.players[i].zombie: m.add("Ducking "+g.players[i].name+"  at "+str(round(g.players[i].x))+", "+str(round(g.players[i].y))+", "+str(round(g.players[i].z))+" with "+str(g.players[i].health)+" hp ("+str(round(get_3d_distance(g.players[i].x,g.players[i].y,g.players[i].z,index.x,index.y,index.z)))+" feet.\n"+(calculate_x_y_string(calculate_x_y_angle(index.x, index.y, g.players[i].x, g.players[i].y, index.facing))),str(g.players[i].name))
								if  g.players[i].zombie: m.add("Ducking zombie "+g.players[i].name+"  at "+str(round(g.players[i].x))+", "+str(round(g.players[i].y))+", "+str(round(g.players[i].z))+" with "+str(g.players[i].health)+" hp ("+str(round(get_3d_distance(g.players[i].x,g.players[i].y,g.players[i].z,index.x,index.y,index.z)))+" feet.\n"+(calculate_x_y_string(calculate_x_y_angle(index.x, index.y, g.players[i].x, g.players[i].y, index.facing))),str(g.players[i].name))
					
					for i in range(len(g.npcs)):
					
						if (g.npcs[i].x<index.x+120 and g.npcs[i].x>index.x-120 and g.npcs[i].y<index.y+120 and g.npcs[i].y>index.y-120 and g.npcs[i].map==index.map and g.npcs[i].name!=index.name):
							if g.npcs[i].faint and g.npcs[i].fainted: m.add("faint "+g.npcs[i].name+"  at "+str(round(g.npcs[i].x))+", "+str(round(g.npcs[i].y))+", "+str(round(g.npcs[i].z))+" with "+str(g.npcs[i].health)+" hp ("+str(round(get_3d_distance(g.npcs[i].x,g.npcs[i].y,g.npcs[i].z,index.x,index.y,index.z)))+" feet.\n"+(calculate_x_y_string(calculate_x_y_angle(index.x, index.y, g.npcs[i].x, g.npcs[i].y, index.facing))),str(i),False)
							if not g.npcs[i].faint and not g.npcs[i].fainted: m.add("faint "+g.npcs[i].name+"  at "+str(round(g.npcs[i].x))+", "+str(round(g.npcs[i].y))+", "+str(round(g.npcs[i].z))+" with "+str(g.npcs[i].health)+" hp ("+str(round(get_3d_distance(g.npcs[i].x,g.npcs[i].y,g.npcs[i].z,index.x,index.y,index.z)))+" feet.\n"+(calculate_x_y_string(calculate_x_y_angle(index.x, index.y, g.npcs[i].x, g.npcs[i].y, index.facing))),str(i),False)
						
					if len(m.menuids)<=0:
						m.add("No one near you","noone",False)
					if len(m.menuids)>0:
						index.playsound("binocularsopen")
						m.send(e.peer_id)
					else: g.n.send_reliable(e.peer_id,"No one near you",0)
				if item=="mine_detector":
					takeobj=True
					final=""
					for mine in g.mines:
						if g.players[index].distancecheck(mine.x,mine.y,mine.z)>50 or mine.map!=g.players[index].map: continue
						final+=f"mine of {mine.owner} at {mine.x}, {mine.y}, {mine.z}\n"
					if final=="": g.n.send_reliable(e.peer_id,"no mines within 50 steps",0); return
					g.n.send_reliable(e.peer_id,final,2)
				if item=="tm62":
					facing=getdir(g.players[index].facing)
					mx=g.players[index].x; my=g.players[index].y; mz=g.players[index].z
					if facing==north: my+=1
					elif facing==northeast: my+=1; mx+=1
					elif facing==east: mx+=1
					elif facing==southeast: my-=1; mx+=1
					elif facing==south: my-=1
					elif facing==southwest: my-=1; mx-=1
					elif facing==west: mx-=1
					elif facing==northwest: my+=1; mx-=1
					gpt=get_tile_at(mx,my,g.players[index].z,g.players[index].map)
					max=get_max_values(g.players[index].map)
					mx=round(mx)
					my=round(my)
					if mine_at(mx,my,g.players[index].z,g.players[index].map) or corpse_at(mx,my,g.players[index].z,g.players[index].map) or mx>max.x or my>max.y or mx<0 or my<0 or gpt=="" or gpt=="air" or gpt.startswith("wall"): g.n.send_reliable(e.peer_id,"You can't place mine here",0); return
					takeobj=True
					g.players[index].stunned=True
					g.players[index].stuntime=3000
					g.players[index].stuntimer.restart()
					g.n.send_reliable(g.players[index].peer_id,"stopmoving",0)
					g.players[index].playsound("mineplace")
					g.players[index].placeminetimer.restart()
					g.players[index].placemine=True
					g.players[index].tx=mx
					g.players[index].ty=my
					g.players[index].tz=mz
				if item=="invisibility_shield":
					if g.players[index].invisible==True:
						g.n.send_reliable(e.peer_id,"you are already invisible",0)
						return
					g.players[index].invisible=True
					takeobj=True
					g.players[index].playsoundmoving("invisibility_start")
					g.players[index].invisibletimer.restart()
				if item=="metal_shield":
					if g.players[index].shielded==True or g.players[index].shieldhitchance>0: g.n.send_reliable(g.players[index].peer_id,"You already have a shield on",0); return
					g.players[index].shieldhitchance=100
					g.players[index].shielded=True
					g.n.send_reliable(g.players[index].peer_id,"stopmoving",0)
					g.players[index].stuntimer.restart()
					g.players[index].stuntime=1250
					g.players[index].stunned=True
					g.players[index].playsoundmoving("shieldon")
					takeobj=True
				if item=="silencer":
					if g.players[index].silencertimer.elapsed<2000: return
					g.players[index].silencertimer.restart()
					takeobj=False
					m=server_menu()
					m.intro="Select hand"
					m.initial_packet="silence"
					m.add("left","left")
					m.add("right","right")
					m.send(e.peer_id)
				if item=="steel_helmet":
					if g.players[index].helmeted==True or g.players[index].helmethitchance>0:
						name=g.players[index].name
						g.n.send_reliable(g.players[index].peer_id,"stopmoving",0)
						g.players[index].can_move=False
						g.players[index].playsoundmoving("removehelmet")
						delay(2800)
						index=get_player_index_from(name)
						g.n.send_reliable(g.players[index].peer_id,"startmoving",0)
						g.players[index].can_move=True
						g.players[index].lasthelmethitchance=g.players[index].helmethitchance
						g.players[index].helmethitchance=0
						g.players[index].helmeted=False
						takeobj=False
					else:
						name=g.players[index].name
						g.n.send_reliable(g.players[index].peer_id,"stopmoving",0)
						g.players[index].playsoundmoving("wearhelmet")
						delay(2550)
						index=get_player_index_from(name)
						if index>-1:
							g.n.send_reliable(g.players[index].peer_id,"startmoving",0)

							try: g.players[index].helmethitchance=g.players[index].lasthelmethitchance
							except: g.players[index].helmethitchance=100
							if g.players[index].helmethitchance<=0: g.players[index].helmethitchance=100
							g.players[index].helmeted=True

							takeobj=False
						else: return
				if item=="zk91" and g.players[index].map!="lobby":
					takeobj=False
					send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "zkplacecode", "Enter a 4 digit number for zk91")

				if item=="zk91_controller" and g.players[index].map!="lobby":
					takeobj=False
					if g.players[index].zkcontrollertimer.elapsed<2000:
						g.n.send_reliable(g.players[index].peer_id,"wait 2 seconds!",0)
						return
					send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "zkusecode", "Enter a 4 digit number")

				if item=="timebomb":
					takeobj=True
					g.players[index].stunned=True
					g.players[index].stuntime=4000
					g.players[index].stuntimer.restart()
					g.players[index].playsound("timebombplace")
					g.n.send_reliable(g.players[index].peer_id,"stopmoving",0)
					g.players[index].placetimebombtimer.restart()
					g.players[index].placetimebomb=True
				if item=="barricade":
					facing=getdir(g.players[index].facing)
					mx=g.players[index].x; my=g.players[index].y; mz=g.players[index].z
					if facing==north: my+=1
					elif facing==northeast: my+=1; mx+=1
					elif facing==east: mx+=1
					elif facing==southeast: my-=1; mx+=1
					elif facing==south: my-=1
					elif facing==southwest: my-=1; mx-=1
					elif facing==west: mx-=1
					elif facing==northwest: my+=1; mx-=1
					gpt=get_tile_at(mx,my,g.players[index].z,g.players[index].map)
					max=get_max_values(g.players[index].map)
					mx=round(mx)
					my=round(my)
					if g.players[index].map=="lobby" or barricade_at(mx,my,g.players[index].z,g.players[index].map) or ladder_at(mx,my,g.players[index].z,g.players[index].map) or chest_at(mx,my,g.players[index].z,g.players[index].map) or corpse_at(mx,my,g.players[index].z,g.players[index].map) or mx>max.x or my>max.y or mx<0 or my<0 or gpt=="" or gpt=="air" or gpt.startswith("wall"): g.n.send_reliable(e.peer_id,"You can't place barricade here",0); return

					takeobj=True
					g.players[index].stunned=True
					g.players[index].stuntime=3000
					g.players[index].stuntimer.restart()
					g.players[index].playsound("walldestroy")
					g.n.send_reliable(g.players[index].peer_id,"stopmoving",0)
					g.players[index].placebarricadetimer.restart()
					g.players[index].placebarricade=True
					g.players[index].px=g.players[index].x
					g.players[index].py=g.players[index].y
					g.players[index].pz=g.players[index].z

				if item=="ladder":
					facing=getdir(g.players[index].facing)
					mx=g.players[index].x; my=g.players[index].y; mz=g.players[index].z
					if facing==north: my+=1
					elif facing==northeast: my+=1; mx+=1
					elif facing==east: mx+=1
					elif facing==southeast: my-=1; mx+=1
					elif facing==south: my-=1
					elif facing==southwest: my-=1; mx-=1
					elif facing==west: mx-=1
					elif facing==northwest: my+=1; mx-=1
					gpt=get_tile_at(mx,my,g.players[index].z,g.players[index].map)
					max=get_max_values(g.players[index].map)
					mx=round(mx)
					my=round(my)
					if g.players[index].map=="lobby" or barricade_at(mx,my,g.players[index].z,g.players[index].map) or ladder_at(mx,my,g.players[index].z,g.players[index].map) or chest_at(mx,my,g.players[index].z,g.players[index].map) or corpse_at(mx,my,g.players[index].z,g.players[index].map) or mx>max.x or my>max.y or mx<0 or my<0 or gpt=="" or gpt=="air" or gpt.startswith("wall"): g.n.send_reliable(e.peer_id,"You can't place ladder here",0); return

					takeobj=True
					g.players[index].stunned=True
					g.players[index].stuntime=5000
					g.players[index].stuntimer.restart()
					g.players[index].playsound("ladder_place")
					g.n.send_reliable(g.players[index].peer_id,"stopmoving",0)
					g.players[index].placeladdertimer.restart()
					g.players[index].placeladder=True
					g.players[index].px=g.players[index].x
					g.players[index].py=g.players[index].y
					g.players[index].pz=g.players[index].z
				if item=="base_ammo_gun_pack":
					for i in g.group_bases:
						if g.players[index].distancecheck(round(i.x),round(i.y),round(i.z))<=2 and g.players[index].map==i.map:
							i.ammo+=10
							g.players[index].playsound("misc191")
							g.players[index].give(item,-1)
							return
						elif g.players[index].distancecheck(round(i.x),round(i.y),round(i.z))>2 and g.players[index].map==i.map: continue
						g.n.send_reliable(g.players[index].peer_id,"You can use this item while at the near of the base",0)
						takeobj=False
						return



				if item=="base_life_amplifier":
					for i in g.group_bases:
						if g.players[index].distancecheck(round(i.x),round(i.y),round(i.z))<=2 and g.players[index].map==i.map:
							if i.health>200000000:
								g.n.send_reliable(g.players[index].peer_id,"this base reached to max health.",0)
								takeobj=False
								return

							i.health+=random(3000,4000)
							g.players[index].playsound("misc191")
							g.players[index].give(item,-1)
							return
						elif g.players[index].distancecheck(round(i.x),round(i.y),round(i.z))>2 and g.players[index].map==i.map: continue
						g.n.send_reliable(g.players[index].peer_id,"You can use this item while at the near of the base",0)
						takeobj=False
						return


				if item=="snowflake_shard":
					if g.players[index].snowtimer.elapsed>=1000:
						g.players[index].snowtimer.restart()
						g.players[index].playsound("grenadethrow")
						takeobj=True
						spawn_weapon(g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].facing, "snowflake_shard", g.players[index].map, g.players[index])
				if item=="admin_grenade":
					g.players[index].playsound("grenadethrow")
					spawn_weapon(g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].facing, "admin_grenade", g.players[index].map, g.players[index])

				if item=="hand_grenade":
					map=g.players[index].map
					if "collect" in map or "combo" in map or "knife" in map or "one_shot_one_kill" in map or "sword" in map: return

					takeobj=False
					if g.players[index].grenadepin:
						if g.players[index].grenadeonetimer.elapsed>500:

							g.players[index].playsound("grenadethrow")
							g.players[index].grenadepin=False
							launch_grenade(g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].map, g.players[index], g.players[index].facing)
							try: g.grenades[len(g.grenades)-1].explodetimer.elapsed=g.players[index].grenadepintimer.elapsed
							except: pass
							g.players[index].grenadetwotimer.restart()
							takeobj=True
					else:
						if g.players[index].grenadetwotimer.elapsed>2000:
							g.players[index].grenadepin=True
							g.players[index].playsound("grenadepul"+str(random(1,2)))
							g.players[index].grenadeonetimer.restart()
							g.players[index].grenadepintimer.restart()
				if item=="fire_suppressant______":
					found_molotov=False
					g.players[index].playsound("misc336")
					g.n.send_reliable(e.peer_id,"stopmoving",0)
					name=g.players[index].name
					delay(14429)
					index=g.get_player_index_from(name)
					if index>-1: g.n.send_reliable(g.players[index].peer_id,"startmoving",0)
					for m in g.molotofs:
						if m.player_is_in_bounds(g.players[index]): g.molotofs.remove(m); found_molotov=True
					if found_molotov: takeobj=True
					else: g.n.send_reliable(e.peer_id,"no fire near",0)
				if item=="molotov_cocktail":
					if g.players[index].molotovthrowtimer.elapsed>=3000:
						g.players[index].molotovthrowtimer.restart()
						takeobj=True
						g.players[index].playsound("molotovthrow")
#							spawn_molotof(g.players[index].x+16, g.players[index].y+16, g.players[index].z, g.players[index].map, g.players[index])
						spawn_weapon(g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].facing, item, g.players[index].map, g.players[index])

				if item=="m4_ammo_cartrigges":
					if get_ammotype(item.replace("_ammo_cartrigges","")) in g.invlimits and get_max_ammo(item.replace("_ammo_cartrigges",""))>g.players[index].get_backpack_level_amount(g.invlimits[get_ammotype(item.replace("_ammo_cartrigges",""))]): g.n.send_reliable(e.peer_id,"Your inventory cannot hold more of this item",0); return
					g.players[index].playsound("misc"+str(random(223,225))+"")
					g.players[index].give("5.56x45mm", get_max_ammo("m4"))
					g.n.send_reliable(g.players[index].peer_id, "you got "+str(get_max_ammo("m4"))+" m4 5.56x45mm ammos from inside cartrigges", 0)
					takeobj=True


				if item=="colt1911_ammo_cartrigges":
					if get_ammotype(item.replace("_ammo_cartrigges","")) in g.invlimits and get_max_ammo(item.replace("_ammo_cartrigges",""))>g.players[index].get_backpack_level_amount(g.invlimits[get_ammotype(item.replace("_ammo_cartrigges",""))]): g.n.send_reliable(e.peer_id,"Your inventory cannot hold more of this item",0); return
					g.players[index].playsound("misc"+str(random(223,225))+"")
					g.players[index].give("45_ACP", get_max_ammo("colt1911"))
					g.n.send_reliable(g.players[index].peer_id, "you got "+str(get_max_ammo("colt1911"))+" colt1911 45_ACP ammos from inside cartrigges", 0)
					takeobj=True

				if item=="dragunov_psl_ammo_cartrigges":
					if get_ammotype(item.replace("_ammo_cartrigges","")) in g.invlimits and get_max_ammo(item.replace("_ammo_cartrigges",""))>g.players[index].get_backpack_level_amount(g.invlimits[get_ammotype(item.replace("_ammo_cartrigges",""))]): g.n.send_reliable(e.peer_id,"Your inventory cannot hold more of this item",0); return
					g.players[index].playsound("misc"+str(random(223,225))+"")
					g.players[index].give("7.62x51mm", get_max_ammo("dragunov_psl"))
					g.n.send_reliable(g.players[index].peer_id, "you got "+str(get_max_ammo("dragunov_psl"))+" dragunov_psl 7.62x51mm ammos from inside cartrigges", 0)
					takeobj=True


				if item=="gsg5_ammo_cartrigges":
					if get_ammotype(item.replace("_ammo_cartrigges","")) in g.invlimits and get_max_ammo(item.replace("_ammo_cartrigges",""))>g.players[index].get_backpack_level_amount(g.invlimits[get_ammotype(item.replace("_ammo_cartrigges",""))]): g.n.send_reliable(e.peer_id,"Your inventory cannot hold more of this item",0); return
					g.players[index].playsound("misc"+str(random(223,225))+"")
					g.players[index].give("22_LR_Long_Rifle", get_max_ammo("gsg5"))
					g.n.send_reliable(g.players[index].peer_id, "you got "+str(get_max_ammo("gsg5"))+" gsg5 22_LR_Long_Rifle ammos from inside cartrigges", 0)
					takeobj=True

				if item=="fnhfnp40_ammo_cartrigges":
					if get_ammotype(item.replace("_ammo_cartrigges","")) in g.invlimits and get_max_ammo(item.replace("_ammo_cartrigges",""))>g.players[index].get_backpack_level_amount(g.invlimits[get_ammotype(item.replace("_ammo_cartrigges",""))]): g.n.send_reliable(e.peer_id,"Your inventory cannot hold more of this item",0); return
					g.players[index].playsound("misc"+str(random(223,225))+"")
					g.players[index].give("40S&W", get_max_ammo("fnhfnp40"))
					g.n.send_reliable(g.players[index].peer_id, "you got "+str(get_max_ammo("fnhfnp40"))+" fnhfnp40 40S&W ammos from inside cartrigges", 0)
					takeobj=True

				if item in g.wdata or item in guns or item in guns2:
					if g.players[index].drawing or g.players[index].reloading: return
					g.players[index].drawweapon=item
					m=server_menu()
					m.intro="select hand"
					m.initial_packet="handselect"
					m.add("left","left")
					m.add("right","right")
					m.send(e.peer_id)
				if(item=="vitality_potion"):
				
					if(g.players[index].health>=g.players[index].maxhealth):
						g.n.send_reliable(g.players[index].peer_id,"Maximum health",0)
						return
					if g.players[index].drinktimer.elapsed>=5000:
						g.players[index].drinktimer.restart()
						g.players[index].health+=g.players[index].maxhealth/2
						g.players[index].playsound("cola2")
						takeobj=True
				if(item=="revival_nectar"):
				
					if(g.players[index].health>=g.players[index].maxhealth):
						g.n.send_reliable(g.players[index].peer_id,"Maximum health",0)
						return
					if g.players[index].drinktimer.elapsed>=5000:
						g.players[index].drinktimer.restart()
						g.players[index].health=g.players[index].maxhealth
						g.players[index].playsound("cola2")
						takeobj=True


				if(item=="small_potion"):
				
					if(g.players[index].health>=g.players[index].maxhealth):
						g.n.send_reliable(g.players[index].peer_id,"Maximum health",0)
						return
					if g.players[index].drinktimer.elapsed>=5000:
						g.players[index].drinktimer.restart()
						g.players[index].health+=g.players[index].maxhealth/5
						g.players[index].playsound("cola2")
						takeobj=True
				if(takeobj==True):
					g.players[index].give(item,-1)
				
			
		
	elif parsed[0]=="xplay":
		index=g.get_player_index(e.peer_id)
		if(index > -1):
			if g.players[index].map!="lobby":
				g.players[index].playsoundmoving(parsed[1],False)
	elif(parsed[0]=="jump"):
	
		index=g.get_player_index(e.peer_id)
		if(index > -1):
		
			g.players[index].playsoundnonlobby("jump"+str(random(1,4)),False)
			
		
	elif(parsed[0]=="fall"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			for p in g.players:
				if p.specplayer==g.players[index].name: g.n.send_reliable(p.peer_id,"fallstart",0)

	elif(parsed[0]=="hardland"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
		
			falld=string_to_number(parsed[1])
			if g.players[index].parachuted==False and g.players[index].map!="lobby":
				g.players[index].health-=falld*3
				g.players[index].hitby="hitting the ground"
			if not g.players[index].hidden: g.n.broadcast("hardland "+g.players[index].name+" "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z)+" "+g.players[index].map,0)
			g.n.send_reliable(e.peer_id,"sitstart",0)
			
		
	elif(parsed[0]=="land"):
	
		index=g.get_player_index(e.peer_id)
		if(index > -1):
		
			for p in g.players:
				if p.specplayer==g.players[index].name: g.n.send_reliable(p.peer_id,"fallstop",0)

			gpt=get_tile_at(g.players[index].x,g.players[index].y,g.players[index].z,g.players[index].map)
			for el in g.electrics:
				if el.z==round(g.players[index].z)-5 and el.x==round(g.players[index].x) and el.y==round(g.players[index].y) and el.map==g.players[index].map:
					g.players[index].playsound("electrictyhit")
					g.players[index].hitby="electric pole"
					g.players[index].health=0
					g.players[index].hitby2="electric pole"
			if gpt!="" or gpt!="air":
				g.players[index].playsoundnonlobby(get_tile_at(g.players[index].x,g.players[index].y, g.players[index].z, g.players[index].map)+"land",False)
			
		
	elif(parsed[0]=="regenerate"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
		
			g.n.send_reliable(g.players[index].peer_id,"sitstop",0)
			g.players[index].health=100
			g.players[index].dead=False
			if g.players[index].matchmode!="teamc":
				for m in g.matches:
					if m.owner==g.players[index].joinedmatch:
						g.players[index].specmatch=g.players[index].joinedmatch
						g.n.send_reliable(e.peer_id,"echo matchwatch "+m.players[0],0)
						g.players[index].map="lobby"
						g.players[index].x=5
						g.players[index].y=0
			else:
				move_player(index, random(0, 100), random(0, 100), 0, "flag"+g.players[index].joinedmatch)

			
		
	elif(parsed[0]=="regenerate2"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
		
			g.players[index].health=g.players[index].maxhealth
			g.n.send_reliable(g.players[index].peer_id,"sitstop",0)
			g.players[index].dead=False
			if "basement" not in g.players[index].map and g.players[index].matchmode!="teamc" and g.players[index].map!="massacre_in_the_city":
				for m in g.matches:
					if m.owner==g.players[index].joinedmatch:
						g.players[index].map="lobby"
						g.players[index].x=5
						g.players[index].y=0
						move_player(index, random(5, 5), random(0, 0), 0, "lobby")
			else:
				if "basement" in g.players[index].map:
					move_player(index,random(5,5),random(0,0),0,"lobby")
				elif g.players[index].map=="massacre_in_the_city":
					move_player2(index,random(0,500),random(0,500),1,"massacre_in_the_city")

				if "flag" in g.players[index].map: move_player(index, random(0, 100), random(0, 100), 0, "flag"+g.players[index].joinedmatch)

			g.n.send_reliable(e.peer_id,"startmoving",0)
		

	elif(parsed[0]=="healthcheck"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			ind=getpc(g.players[index].specplayer)
			if ind == None:
				if g.players[index].vi==-1:
					shieldinfo=""
					if g.players[index].shieldhitchance>0: shieldinfo=", with "+str(g.players[index].shieldhitchance)+"% shield damage resistance"
					if g.players[index].shieldhitchance<=0: shieldinfo="with not shielded"
					helmetinfo=""
					if g.players[index].helmethitchance>0: helmetinfo=", with "+str(round(g.players[index].helmethitchance))+"% helmet damage resistance"
					if g.players[index].helmethitchance<=0: helmetinfo="with not helmetted"


					if g.players[index].health>0: g.players[index].packet(""+str(round(g.players[index].health))+" HP "+shieldinfo+" "+helmetinfo+"",0)
					else: g.players[index].packet("you are died",0)
				else:
					shieldinfo=""
					if g.players[index].shieldhitchance>0: shieldinfo=", with "+str(g.players[index].shieldhitchance)+"% shield damage resistance"
					if g.players[index].shieldhitchance<=0: shieldinfo="with not shielded"
					helmetinfo=""
					if g.players[index].helmethitchance>0: helmetinfo=", with "+str(round(g.players[index].helmethitchance))+"% helmet damage resistance"
					if g.players[index].helmethitchance<=0: helmetinfo="with not helmetted"



					g.players[index].packet("You have "+str(round(g.players[index].health))+" HP, and the motor has "+str(g.motors[g.players[index].vi].health)+" hp "+shieldinfo+" "+helmetinfo+"",0)

			if ind != None:
				if ind.vi==-1:
					shieldinfo=""
					if ind.shieldhitchance>0: shieldinfo=", with "+str(ind.shieldhitchance)+"% shield damage resistance"
					if ind.shieldhitchance<=0: shieldinfo="with not shielded"
					helmetinfo=""
					if ind.helmethitchance>0: helmetinfo=", with "+str(round(ind.helmethitchance))+"% helmet damage resistance"
					if ind.helmethitchance<=0: helmetinfo="with not helmetted"


					if ind.health>0: g.players[index].packet(""+str(round(ind.health))+" HP "+shieldinfo+" "+helmetinfo+"",0)
					else: g.players[index].packet("this player is died",0)
				else:
					shieldinfo=""
					if ind.shieldhitchance>0: shieldinfo=", with "+str(ind.shieldhitchance)+"% shield damage resistance"
					if ind.shieldhitchance<=0: shieldinfo="with not shielded"
					helmetinfo=""
					if ind.helmethitchance>0: helmetinfo=", with "+str(round(ind.helmethitchance))+"% helmet damage resistance"
					if ind.helmethitchance<=0: helmetinfo="with not helmetted"



					g.players[index].packet(""+str(round(ind.health))+" HP, and the motor has "+str(g.motors[ind.vi].health)+" hp "+shieldinfo+" "+helmetinfo+"",0)


	elif(parsed[0]=="setversion" and len(parsed)>1):
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].version=parsed[1]
	elif(parsed[0]=="juharjksjkadjknjk12n3kjnkjn1j23kjnkjn12k3nknkn123kjnkn12k3nknk5nknkn32knkn1n1k1k"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
		
			if(file_exists("chars/"+g.players[index].name+"/developer.usr")==True):
			
				g.players[index].dev=True

				g.players[index].title="Developer"
				g.players[index].title2="Developer"

				g.n.send_reliable(g.players[index].peer_id,"isadmin",0)
#					g.n.broadcast(""+g.players[index].name+" is a Developer of Zero Hour Assault",2)
				
			
		
	elif(parsed[0]=="motd"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
		
			g.n.send_reliable(g.players[index].peer_id,"Server Message: "+file_get_contents("motd.txt")+"",0)
	elif parsed[0]=="throwweaponleft":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if g.players[index].map=="lobby" or "match" in g.players[index].map: return
			if "sword" in g.players[index].weapon or g.players[index].weapon=="knife":
				g.players[index].give(g.players[index].weapon,-1)
				wname=g.players[index].weapon
				g.players[index].weapon="punch"
				g.players[index].get_weapon_properties(g.players[index].weapon)
				g.n.send_reliable(e.peer_id,"drawsilent punch",0)
				spawn_weapon(g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].facing, "thrown_"+wname, g.players[index].map, g.players[index])
	elif parsed[0]=="throwweaponright":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if g.players[index].map=="lobby" or "match" in g.players[index].map: return
			if "sword" in g.players[index].weapon2 or g.players[index].weapon2=="knife":
				g.players[index].give(g.players[index].weapon2,-1)
				wname=g.players[index].weapon2
				g.players[index].weapon2="feet"
				g.players[index].get_weapon_properties(g.players[index].weapon2)
				g.n.send_reliable(e.peer_id,"draw2silent feet",0)
				spawn_weapon(g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].facing, "thrown_"+wname, g.players[index].map, g.players[index])

	elif(parsed[0]=="firestart" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
		
			if g.players[index].reloading==True:
				return
			if(g.players[index].dead):
				return

			if(g.players[index].dead):
				g.n.send_reliable(g.players[index].peer_id,"You are died!",0)
			if g.players[index].get_ammo_count_from(g.players[index].weapon)<=0:
				g.players[index].firing=False
				g.players[index].playsound(g.players[index].weapon+"empty")
				return



			wname=parsed[1]
			if wname in guns==False:
				g.n.send_reliable(g.players[index].peer_id,"Error while shooting",0)
			g.players[index].weapon=parsed[1]
			g.players[index].firing=True

			
		
	elif(parsed[0]=="firestop") :
		index=g.get_player_index(e.peer_id)
		if(index>-1): g.players[index].firing=False
		

	elif(parsed[0]=="unequip"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if g.players[index].weapon!="":
				g.players[index].weapon="punch"
				if not g.players[index].adrenaline: g.n.send_reliable(e.peer_id,"weapondata "+g.wdata["punch"],0)
				if g.players[index].adrenaline: g.n.send_reliable(e.peer_id,"weapondatafast "+g.wdata["punch"],0)
				if g.players[index].weapon=="" and g.players[index].weapon2=="": g.n.send_reliable(e.peer_id,"candraw",0)
				g.players[index].playsound("berettaM9draw")
	elif(parsed[0]=="unequip2"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if g.players[index].weapon2!="":
				g.players[index].weapon2="feet"
				if not g.players[index].adrenaline: g.n.send_reliable(e.peer_id,"weapondata2 "+g.wdata["feet"],0)
				if g.players[index].adrenaline: g.n.send_reliable(e.peer_id,"weapondata2fast "+g.wdata["feet"],0)
				if g.players[index].weapon=="" and g.players[index].weapon2=="": g.n.send_reliable(e.peer_id,"candraw",0)
				g.players[index].playsound("berettaM9draw")
	elif(parsed[0]=="weaponfire"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if g.players[index].sitting or "abyss_clash" in g.players[index].map or "grenade" in g.players[index].map: return
			if g.players[index].weapon!="knife" and g.players[index].weapon!="claw" and g.players[index].get_item_count(g.players[index].weapon)<=0: return
			if g.players[index].map=="lobby": return
			if "helicopter" in g.players[index].map: return
			if "match" in g.players[index].map: return
			if g.players[index].reloading==True:
				return
			if(g.players[index].dead):
				return
			if not requires_ammo(g.players[index].weapon): return
			wr=vector(g.players[index].x,g.players[index].y,g.players[index].z)
			g.players[index].playsound("weaponfire"+str(random(1,3)))
			for r in range(15):
				wr=move(wr.x,wr.y,wr.z,g.players[index].facing,0,0,0)
				if get_tile_at(wr.x,wr.y,wr.z,g.players[index].map).startswith("wall"): return
				for x in g.players:
					if x.map=="massacre_in_the_city" and g.get_group(x.group) is not None and x.group==g.players[index].group and g.get_group(x.group).freedomhit==0: continue
					if x.health<=0: continue
					if x.name!=g.players[index].name and x.distancecheck(wr.x,wr.y,wr.z)<=3 and g.players[index].map==x.map:
						x.playsound("weaponhit")
						x.health-=random(5,10)
						x.hitby=g.players[index].name+"'s "+g.players[index].weapon
						x.hitby2=g.players[index].name
						if not x.sitting:
							g.n.send_reliable(x.peer_id,"sitstart",0)
							x.playsound(g.get_tile_at(x.x,x.y,x.z,x.map)+"fall")
						g.n.send_reliable(x.peer_id,"drawsilent punch",0)
						g.n.send_reliable(x.peer_id,"draw2silent feet",0)
						return
	elif(parsed[0]=="weaponfire2"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if g.players[index].sitting or "abyss_clash" in g.players[index].map or "grenade" in g.players[index].map: return
			if g.players[index].weapon2!="knife" and g.players[index].weapon2!="claw" and g.players[index].get_item_count(g.players[index].weapon2)<=0: return
			if g.players[index].map=="lobby": return
			if "helicopter" in g.players[index].map: return
			if "match" in g.players[index].map: return
			if g.players[index].reloading==True:
				return
			if(g.players[index].dead):
				return
			if not requires_ammo(g.players[index].weapon2): return
			g.players[index].playsound("weaponfire"+str(random(1,3)))
			wr=vector(g.players[index].x,g.players[index].y,g.players[index].z)
			for r in range(15):
				wr=move(wr.x,wr.y,wr.z,g.players[index].facing,0,0,0)
				if get_tile_at(wr.x,wr.y,wr.z,g.players[index].map).startswith("wall"): return
				for x in g.players:
					if x.map=="massacre_in_the_city" and g.get_group(x.group) is not None and x.group==g.players[index].group and g.get_group(x.group).freedomhit==0: continue
					if x.health<=0: continue
					if x.name!=g.players[index].name and x.distancecheck(wr.x,wr.y,wr.z)<=3 and g.players[index].map==x.map:
						x.playsound("weaponhit")
						if not x.sitting:
							g.n.send_reliable(x.peer_id,"sitstart",0)
							x.playsound(g.get_tile_at(x.x,x.y,x.z,x.map)+"fall")
						x.health-=random(5,10)
						x.hitby=g.players[index].name+"'s "+g.players[index].weapon2
						x.hitby2=g.players[index].name

						g.n.send_reliable(x.peer_id,"drawsilent punch",0)
						g.n.send_reliable(x.peer_id,"draw2silent feet",0)
						return
	elif(parsed[0]=="fire"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if getattr(g.players[index], "controlled_turret", None) is not None:
				turret = g.players[index].controlled_turret
				base = None
				for b in g.group_bases:
					if b.name == turret.base_name:
						base = b
						break
				if base is None: return
				# Check generator
				if not base.generator_on or base.generator_fuel <= 0:
					g.n.send_reliable(g.players[index].peer_id, "The generator is off! Turret requires power.", 0)
					return
				# Check base ammo
				if base.ammo <= 0:
					g.players[index].playsound("punchempty")
					g.n.send_reliable(g.players[index].peer_id, "Turret has no ammo!", 0)
					return
				# Check turret cooldown
				if turret.fire_timer.elapsed < turret.get_firetime():
					return
				turret.fire_timer.restart()
				
				# Fire!
				base.ammo -= 1
				spawn_weapon(turret.x, turret.y, turret.z, g.players[index].facing, turret.weapon_type, turret.map, g.players[index])
				
				# Play weapon firing sound at turret
				g.play(turret.weapon_type + "fire" + str(random(1, 3)), turret.x, turret.y, turret.z, turret.map)
				
				# Play distant whiz/weapon sound to other players on map
				for p in g.players:
					if p.name != g.players[index].name and p.map == turret.map:
						g.n.send_reliable(p.peer_id, "distsound " + turret.weapon_type + "dist" + str(random(1, 3)) + " " + str(turret.x) + " " + str(turret.y) + " " + str(turret.z) + " " + turret.map, 0)
				return
		
			if "teamc" in g.players[index].map:
				if g.players[index].matchteam=="" or g.players[index].joinedmatch=="" or g.players[index].matchmode=="": return
			if "android" not in os.getcwd() and g.players[index].firetimer.elapsed<g.players[index].get_firetime(): return
			g.players[index].firetimer.restart()
			if g.players[index].map=="jail": return
			if "collect" in g.players[index].map: return
			if g.players[index].drawing or g.players[index].sitting or "abyss_clash" in g.players[index].map or "grenade" in g.players[index].map: return
			if g.players[index].weapon!="punch" and g.players[index].weapon!="claw" and g.players[index].get_item_count(g.players[index].weapon)<=0: return
			if g.players[index].map=="lobby": return
			if "helicopter" in g.players[index].map: return
			if "match" in g.players[index].map: return
			if g.players[index].reloading==True:
				return
			if(g.players[index].dead):
				return
			wname=g.players[index].weapon
#				if g.players[index].matchmode=="teamk" and wname!="knife": return
			if requires_ammo(g.players[index].weapon):
				if(g.players[index].get_ammo_count_from(g.players[index].weapon)<=0) and g.players[index].reloading==False:
					g.players[index].playsound(""+wname+"empty")
					return
				if(g.players[index].get_ammo_count_from(g.players[index].weapon)>0):					
					spawn_weapon(g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].facing, wname, g.players[index].map, g.players[index])
#						play(""+wname+"fire"+str(random(1,3))+"", g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].map,g.players[index])
					if wname=="diamond_sword" or wname=="stone_sword" or wname=="wooden_sword":
						g.players[index].playsound(""+wname+"fire")
					else:
						if wname in g.players[index].silenced:
							if wname in pistols: g.players[index].playsound("psilenced"+str(random(1,3)))
							if wname in machineguns: g.players[index].playsound("msilenced"+str(random(1,1)))
							if wname in snipers: g.players[index].playsound("sssilenced"+str(random(1,1)))
						else: g.players[index].playsound(""+wname+"fire"+str(random(1,3))+"")
					if wname!="punch" and wname!="kick" and wname!="stick" and wname!="knife" and wname!="claw" and wname!="wooden_sword" and wname!="stone_sword" and wname!="diamond_sword":
						for i in g.players:
							if g.players[index].hidden: continue
							if i.dead: continue
							if i.name!=g.players[index].name and (i.map==g.players[index].map or i.specmap==g.players[index].map):
								if wname in g.players[index].silenced: g.n.send_reliable(i.peer_id,"distpitchsound "+wname+"dist"+str(random(1,3))+" "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z)+" "+g.players[index].map+" 170",0)
								if wname not in g.players[index].silenced: g.n.send_reliable(i.peer_id,"distsound "+wname+"dist"+str(random(1,3))+" "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z)+" "+g.players[index].map,0)
#							g.n.broadcast("distsound "+wname+"dist"+str(random(1,3))+" "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z)+" "+g.players[index].map,0)

						for n in g.npcs:
							if n.randomwalking and n.map==g.players[index].map and "zombie" not in n.map:
								n.targetx=g.players[index].x
								n.targety=g.players[index].y
								n.targetz=g.players[index].z
					g.players[index].ammogive(g.players[index].weapon,-1)
			else:
				spawn_weapon(g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].facing, wname, g.players[index].map, g.players[index])
#					play(""+wname+"fire"+str(random(1,3))+"", g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].map,g.players[index])
				if wname=="diamond_sword" or wname=="stone_sword" or wname=="wooden_sword":
					g.players[index].playsound(""+wname+"fire")
				else:
					g.players[index].playsound(""+wname+"fire"+str(random(1,3))+"")
#					g.n.broadcast("distsound "+wname+"dist "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z)+" "+g.players[index].map,0)

			
		
	elif(parsed[0]=="fire2"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
		
			if "teamc" in g.players[index].map:
				if g.players[index].matchteam=="" or g.players[index].joinedmatch=="" or g.players[index].matchmode=="": return

			if "android" not in os.getcwd() and g.players[index].firetimer2.elapsed<g.players[index].get_firetime2(): return
			g.players[index].firetimer2.restart()

			if g.players[index].map=="jail": return
			if "collect" in g.players[index].map: return
			if g.players[index].drawing or g.players[index].sitting or "abyss_clash" in g.players[index].map or "grenade" in g.players[index].map: return
			if g.players[index].weapon2!="feet" and g.players[index].weapon2!="claw" and g.players[index].get_item_count(g.players[index].weapon2)<=0: return
			if g.players[index].map=="lobby": return
			if "match" in g.players[index].map: return
			if "helicopter" in g.players[index].map: return
			if g.players[index].reloading==True:
				return
			if(g.players[index].dead):
				return
			wname=g.players[index].weapon2
#				if g.players[index].matchmode=="teamk" and wname!="knife": return
			if requires_ammo(g.players[index].weapon2):
				if(g.players[index].get_ammo_count_from(g.players[index].weapon2)<=0) and g.players[index].reloading==False:
					g.players[index].playsound(""+wname+"empty")
					return
				if(g.players[index].get_ammo_count_from(g.players[index].weapon2)>0):					
					spawn_weapon(g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].facing, wname, g.players[index].map, g.players[index])
#						play(""+wname+"fire"+str(random(1,3))+"", g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].map,g.players[index])
					if wname=="diamond_sword" or wname=="stone_sword" or wname=="wooden_sword":
						g.players[index].playsound(""+wname+"fire")
					else:
						if wname in g.players[index].silenced:
							if wname in pistols: g.players[index].playsound("psilenced"+str(random(1,3)))
							if wname in machineguns: g.players[index].playsound("msilenced"+str(random(1,1)))
							if wname in snipers: g.players[index].playsound("sssilenced"+str(random(1,1)))
						else: g.players[index].playsound(""+wname+"fire"+str(random(1,3))+"")

					if wname!="punch" and wname!="feet" and wname!="stick" and wname!="knife" and wname!="claw" and wname!="wooden_sword" and wname!="stone_sword" and wname!="diamond_sword":
						for i in g.players:
							if g.players[index].hidden: continue
							if i.dead: continue
							if i.name!=g.players[index].name and (i.map==g.players[index].map or i.specmap==g.players[index].map):
								if wname in g.players[index].silenced: g.n.send_reliable(i.peer_id,"distpitchsound "+wname+"dist"+str(random(1,3))+" "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z)+" "+g.players[index].map+" 170",0)
								if wname not in g.players[index].silenced: g.n.send_reliable(i.peer_id,"distsound "+wname+"dist"+str(random(1,3))+" "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z)+" "+g.players[index].map,0)

#							g.n.broadcast("distsound "+wname+"dist"+str(random(1,3))+" "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z)+" "+g.players[index].map,0)

						for n in g.npcs:
							if n.randomwalking and n.map==g.players[index].map and "zombie" not in n.map:
								n.targetx=g.players[index].x
								n.targety=g.players[index].y
								n.targetz=g.players[index].z
					g.players[index].ammogive(g.players[index].weapon2,-1)
			else:
				spawn_weapon(g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].facing, wname, g.players[index].map, g.players[index])
#					play(""+wname+"fire"+str(random(1,3))+"", g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].map,g.players[index])
				if wname=="diamond_sword" or wname=="stone_sword" or wname=="wooden_sword":
					g.players[index].playsound(""+wname+"fire")
				else:
					g.players[index].playsound(""+wname+"fire"+str(random(1,3))+"")
#					g.n.broadcast("distsound "+wname+"dist "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z)+" "+g.players[index].map,0)

			
		

	elif(parsed[0]=="facing" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
		
			g.players[index].facing=string_to_number(parsed[1])
			if getattr(g.players[index], "controlled_turret", None) is not None:
				g.players[index].playsound("misc327", True)
			g.players[index].weapon_rays=None
			g.players[index].weapon_rays2=None
	
	elif(parsed[0]=="aim" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
		
			g.players[index].aim=string_to_number(parsed[1])
			g.players[index].weapon_rays=None
			g.players[index].weapon_rays2=None
			for p in g.players:
				if p.specplayer==g.players[index].name: g.n.send_reliable(p.peer_id,"setaim "+parsed[1],0)
			
		
		
	elif(parsed[0]=="aimmode" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
		
			g.players[index].aim_mode=string_to_number(parsed[1])
	elif(parsed[0]=="duck"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
		
			g.players[index].ducking=True
			g.players[index].playsound("duck",False)
			
		
		
	elif(parsed[0]=="unduck"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
		
			g.players[index].ducking=False
			g.players[index].playsound("unduck",False)				
		
		


	elif(parsed[0]=="create"):
		if len(parsed) > 5:
			create(parsed[1],parsed[2],parsed[3],parsed[4],parsed[5],e.peer_id)
		else:
			g.n.send_reliable(e.peer_id, "banned Invalid account creation request format.", 0)
	elif string_contains(e.message, "messagereport", 1)>-1:			
		if string_contains(e.message, "messagereport", 1)>-1:
			index=get_player_index(e.peer_id)
			if index>-1:
				parsed2=string_split(e.message, "{}[]", True)
				if parsed2[1]=="":
					return
				if parsed[2]=="":
					return
				g.n.send_reliable(g.players[index].peer_id,"Report message sent successfull",0)
				adminsend(g.players[index].name+" has reported a message! The message is: "+parsed2[1]+". The player's message is: "+parsed2[2]+".")
				notify_admins("zero hour assault, "+g.players[index].name+" has reported a message! The message is: "+parsed2[1]+". The player's message is: "+parsed2[2]+".")
	elif parsed[0]=="zkplacecode" and len(parsed)>1:
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			if len(parsed[1])!=4:
				g.n.send_reliable(g.players[index].peer_id,"The code must consist of at least 4 numbers",0)
				return
			if parsed[1].isdigit()==False:
				g.n.send_reliable(g.players[index].peer_id,"it should only contain numbers",0)
				return
			codeinput=int(parsed[1])
			name=g.players[index].name
			g.n.send_reliable(g.players[index].peer_id,"stopmoving",0)
			g.players[index].can_move=False
			g.play("flashbangput",g.players[index].x,g.players[index].y,g.players[index].z,g.players[index].map)
			delay(4000)
			index=get_player_index_from(name)
			g.n.send_reliable(g.players[index].peer_id,"startmoving",0)
			g.players[index].can_move=True

			g.players[index].give("zk91",-1)
			place_zk(g.players[index].x,g.players[index].y,g.players[index].z,g.players[index].map,g.players[index].name,codeinput)
			g.play("misc351",g.players[index].x,g.players[index].y,g.players[index].z,g.players[index].map)
			g.n.send_reliable(g.players[index].peer_id,"the bomb is now set! use the code "+str(codeinput)+" to explode your bomb",0)

	elif parsed[0]=="zkusecode" and len(parsed)>1:
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			if len(parsed[1])!=4:
				g.n.send_reliable(g.players[index].peer_id,"The code must consist of at least 4 numbers",0)
				return
			if parsed[1].isdigit()==False:
				g.n.send_reliable(g.players[index].peer_id,"it should only contain numbers",0)
				return

			codeinput=int(parsed[1])
			g.players[index].zkcontrollertimer.restart()
			bombfound=0
			for bomb in g.zks:
				if bomb.code==codeinput and bomb.map==g.players[index].map:
					bombfound+=1
					bomb.exploding=True
					bomb.codefound=True
					bomb.explodetimer.restart()
			if bombfound>0:

				g.play("remote_buttonbeep",g.players[index].x,g.players[index].y,g.players[index].z,g.players[index].map)
			g.n.send_reliable(g.players[index].peer_id,""+str(bombfound)+" zks are going to explode!",0)
	elif parsed[0] == "backup_selected":
		index = g.get_player_index(e.peer_id)
		if index > -1:
			# URL kodlamasını geri alarak orijinal klasör adını elde et
			encoded_selected_backup = parsed[1]
			selected_backup = urllib.parse.unquote_plus(encoded_selected_backup)

			def send_character_menu(player_index, backup_directory):
				m = server_menu()
				m.intro = "Select Character:"
				m.initial_packet = "character_selected"
				g.players[player_index].selected_backup = selected_backup
				
				chars_directory = os.path.join(backup_directory, "chars")

				if not os.path.exists(chars_directory):
					g.n.send_reliable(
						g.players[player_index].peer_id,
						"The 'chars' folder containing characters was not found!",
						0
					)
					adminsend(
						f"[{g.players[index].name}] attempted to access the 'chars' directory within {backup_directory} but the folder does not exist!"
					)
					return

				character_folders = find_directories(chars_directory)

				if character_folders:
					# alfabetik olarak sırala
					character_folders = sorted(character_folders, key=lambda x: x.lower())

					for folder in character_folders:
						encoded_folder = urllib.parse.quote_plus(folder)
						m.add(folder, encoded_folder)
				else:
					m.add("No Characters Found", "no_chars", False)

				g.n.send_reliable(g.players[player_index].peer_id, "play_s menuopen.ogg", 0)
				m.send(g.players[player_index].peer_id)
			
			backup_directory = os.path.join("backups", selected_backup)
			
			send_character_menu(index, backup_directory)

	elif parsed[0] == "character_selected":
		index = g.get_player_index(e.peer_id)
		if index > -1:
			# URL kodlamasını geri alarak orijinal klasör adını elde et
			encoded_selected_character = parsed[1]
			selected_character = urllib.parse.unquote_plus(encoded_selected_character)
			
			if not hasattr(g.players[index], 'selected_backup'):
				g.n.send_reliable(e.peer_id, "You must select a backup first.", 0)
				return

			def copy_character(player_index, selected_backup, selected_character):
				kaynak_dizin = os.path.join("backups", selected_backup, "chars", selected_character)
				hedef_dizin = os.path.join("chars", selected_character)

				if not os.path.exists(kaynak_dizin):
					g.n.send_reliable(g.players[player_index].peer_id, f"Source directory not found: {kaynak_dizin}", 0)
					adminsend(f"[{g.players[player_index].name}] attempted to copy a character but the source directory was not found: {kaynak_dizin}")
					return

				try:
					g.n.send_reliable(g.players[player_index].peer_id, f"Character {selected_character} successfully copied.", 0)
					adminsend(f"[{g.players[player_index].name}] successfully copied character {selected_character} from backup {selected_backup}.")
					notify_admins(f"zero hour assault, [{g.players[player_index].name}] successfully copied character {selected_character} from backup {selected_backup}.")
					target_index = get_player_index_from(selected_character)
					if target_index != -1:
						remove_from_server(target_index)

					if os.path.exists(hedef_dizin):
						shutil.rmtree(hedef_dizin)

					shutil.copytree(kaynak_dizin, hedef_dizin)
				except Exception as e:
					g.n.send_reliable(g.players[player_index].peer_id, f"An error occurred while copying the character: {e}", 0)
					adminsend(f"[{g.players[player_index].name}] encountered an error while copying the character: {e}")

			selected_backup = g.players[index].selected_backup
			
			# Copy the character
			copy_character(index, selected_backup, selected_character)
	elif parsed[0]=="android":
		index=get_player_index(e.peer_id)
		if index>-1:
			g.players[index].android=True
			f=open("chars/"+g.players[index].name+"/android.usr","w")
			f.close()
	elif parsed[0]=="ios":
		index=get_player_index(e.peer_id)
		if index>-1:
			g.players[index].ios=True
			f=open("chars/"+g.players[index].name+"/ios.usr","w")
			f.close()

	elif parsed[0]=="itemdisable":
		index=get_player_index(e.peer_id)
		if index>-1:
			g.players[index].itembeep=0
	elif parsed[0]=="bikehorn":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			try:
				g.players[index].bike.horn(index)
			except: pass
	elif parsed[0]=="bikeexit":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			try:
				g.players[index].bike.exit(index)
			except: pass

	return True
