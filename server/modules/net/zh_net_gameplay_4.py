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

def handle_gameplay_4(e, parsed, index):
	global languages
	cmds = {"deleteline", "weaponinfo", "drawsilent", "unload", "cheat", "basecomp", "corpse", "baseopen", "weaponinfo2", "corpseselect", "communitymessage", "draw", "vdown", "pingr", "reload", "vup", "draw2silent", "playsnd", "checkaround", "addline", "matchmodepublicbot", "motorengine", "basepasswordchange", "sendverify", "draw2", "verifycode", "matchmodeprivatebot", "buildobj", "chest2", "mapmessage", "editlinemenu", "addinmap", "pr", "motorhorn", "chest", "playonmap", "build", "outmotor", "matchmodeprivate", "groupmessage", "login", "baseupgrade", "base_wall_upgrade", "base_generator", "base_deposit_ammo", "base_turret_manage", "base_buy_turret", "base_select_turret", "base_select_weapon", "base_deconstruct_turret"}
	subs = {"editlineSPLITS_THE_PARTS_OF_EDITLINE"}
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

	if parsed[0]=="matchmodeprivate" and len(parsed)>1:
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="" or parsed[1]=="back":
				return

			if g.players[index].matchpassword=="" or g.players[index ].matchtypeamount=="0" or g.players[index].matchtypeamount=="":
				g.n.send_reliable(g.players[index].peer_id,"Canceled",0)
				return
#				newmatch(g.players[index].name,g.players[index].matchtypeamount,parsed[1],g.players[index].matchpassword)
			g.players[index].matchtypeamount=parsed[1]
			if g.players[index].mmode=="teamc":
				for m in g.matches:
					if m.owner==g.players[index].name: send_reliable(e.peer_id,"The match you created before didn't end yet, please wait for it to end before you can create a new match.",0); return

				newmatch(g.players[index].name,g.players[index].matchtypeamount,g.players[index].mmode,g.players[index].matchpassword,0)
				return

			m=server_menu()
			m.initial_packet="matchmodeprivatebot"
			m.intro="Would you like to add bot in this match"
			m.add("yes, i want to add bot in this match","1")
			m.add("no, i dont want to add bot in this match","0")
			m.send(e.peer_id)

			return
	elif(parsed[0]=="mapmessage"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if g.players[index].chattimer.elapsed<1000:
				g.n.send_reliable(g.players[index].peer_id,"wait one second!",0)
				return
			if(len(e.message)>2000):
				return

			if not g.players[index].disable_all_chat_check(): return
			if not g.players[index].disable_map_chat_check(): return
			if g.players[index].mapmessage==0:
				send_reliable(g.players[index].peer_id,"You turned off receiving map messages. So you can not send also",0)
				return
			saymessage=string_replace(e.message,""+parsed[0]+" ","",False)
			g.players[index].chattimer.restart()
			sentme=False
			for i in g.players:
				if i.mapmessage==0: continue
				if g.players[index].name in i.blocks or i.name in g.players[index].blocks: continue
				if i.map=="lobby" and g.players[index].map=="lobby" and g.players[index].specplayer!="": continue
				if i.map==g.players[index].map or i.specmap==g.players[index].map:
					if not g.players[index].paid: g.n.send_reliable(i.peer_id,"mapmessage "+g.players[index].name+" says to the map: "+saymessage+"",0)
					if g.players[index].paid: g.n.send_reliable(i.peer_id,"mapmessage * "+g.players[index].name+" says to the map: "+saymessage+"",0)
					g.n.send_reliable(i.peer_id,"play_s chat2.ogg",0)
				if i.map==g.players[index].specmap:
					if not g.players[index].paid: g.n.send_reliable(i.peer_id,"mapmessage spectator "+g.players[index].name+" says to the map: "+saymessage+"",0)
					if g.players[index].paid: g.n.send_reliable(i.peer_id,"mapmessage  spectator * "+g.players[index].name+" says to the map: "+saymessage+"",0)
					g.n.send_reliable(i.peer_id,"play_s chat2.ogg",0)
					if not sentme:
						if not g.players[index].paid: g.n.send_reliable(e.peer_id,"mapmessage spectator "+g.players[index].name+" says to the map: "+saymessage+"",0)
						if g.players[index].paid: g.n.send_reliable(e.peer_id,"mapmessage spectator * "+g.players[index].name+" says to the map: "+saymessage+"",0)
						g.n.send_reliable(e.peer_id,"play_s chat2.ogg",0)
						sentme=True

	elif(parsed[0]=="groupmessage"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if not g.players[index].disable_all_chat_check(): return
			if not g.players[index].disable_group_chat_check(): return
			if g.players[index].group=="": g.n.send_reliable(e.peer_id,"You're not on a group.",0); return
			if g.players[index].groupmessage==0:
				send_reliable(g.players[index].peer_id,"You turned off receiving group messages. So you can not send also",0)
				return
			saymessage=string_replace(e.message,""+parsed[0]+" ","",False)
			for i in g.players:
				if i.groupmessage==0: continue
				if i.group!=g.players[index].group: continue
				if not g.players[index].paid: g.n.send_reliable(i.peer_id,"groupmessage "+g.players[index].name+" says to the group: "+saymessage+"",0)
				if g.players[index].paid: g.n.send_reliable(i.peer_id,"groupmessage * "+g.players[index].name+" says to the group: "+saymessage+"",0)
				g.n.send_reliable(i.peer_id,"play_s misc157.ogg",0)

	elif(parsed[0]=="communitymessage"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if not g.players[index].disable_all_chat_check(): return
			if g.players[index].community=="": g.n.send_reliable(e.peer_id,"You're not on a community.",0); return
			if g.players[index].communitymessage==0:
				send_reliable(g.players[index].peer_id,"You turned off receiving community messages. So you can not send also",0)
				return
			saymessage=string_replace(e.message,""+parsed[0]+" ","",False)
			for i in g.players:
				if i.communitymessage==0: continue
				if i.community!=g.players[index].community: continue
				if not g.players[index].paid: g.n.send_reliable(i.peer_id,"communitymessage "+g.players[index].name+" says to the community: "+saymessage+"",0)
				if g.players[index].paid: g.n.send_reliable(i.peer_id,"communitymessage * "+g.players[index].name+" says to the community: "+saymessage+"",0)

				test=random(1,2)
				if test==1: g.n.send_reliable(i.peer_id,"play_s misc235.ogg",0)
				if test==2: g.n.send_reliable(i.peer_id,"play_s misc239.ogg",0)



	elif(parsed[0]=="checkaround"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):

			index=g.players[index]
			if index.specplayer!="":
				g.n.send_reliable(index.peer_id,"you can not look while you watching someone",0)
				return

			if index.specplayer!="": index=getpc(index.specplayer)
			if index is None: return
			m=""
			menu=server_menu()
			menu.intro="Select an object to track"
			menu.initial_packet="trackobj"
			if index.matchmode=="teamz":
				for ma in g.matches:
					if index.name in ma.players:
						if ma.redhousex!=-50: menu.add("Red team house",f"{ma.redhousex},{ma.redhousey},0")
						if ma.bluehousex!=-50: menu.add("Blue team house",f"{ma.bluehousex},{ma.bluehousey},0")
			for i in range(len(g.flags)):
				if (get_3d_distance(index.x, index.y, index.z, string_to_number(g.flags[i].x), string_to_number(g.flags[i].y), string_to_number(g.flags[i].z))
				   <=30
					and g.flags[i].map==index.map
				):
					level=1
					if g.flags[i].z>index.z:
						level=2
					elif g.flags[i].z<index.z:
						level=0
					else:
						level=1
					m+="a flag from "+g.flags[i].team+" team "
					m+=" is "
					if level==2:
						m+="above, "
					elif level==0:
						m+="below, "
					m+=(calculate_x_y_string(calculate_x_y_angle(index.x, index.y, g.flags[i].x, g.flags[i].y, index.facing)
						)
					   +", "
					   +str(round(index.distancecheck(g.flags[i].x, g.flags[i].y, g.flags[i].z))
						)
					   +" feet away. "
					)
					menu.add(m,str(g.flags[i].x)+","+str(g.flags[i].y)+","+str(g.flags[i].z))
					m=""
			for i in range(len(g.group_bases)):
				if (get_3d_distance(index.x, index.y, index.z, string_to_number(g.group_bases[i].x), string_to_number(g.group_bases[i].y), string_to_number(g.group_bases[i].z))
				   <=30
					and g.group_bases[i].map==index.map
				):
					level=1
					if g.group_bases[i].z>index.z:
						level=2
					elif g.group_bases[i].z<index.z:
						level=0
					else:
						level=1
					s=""
					if g.group_bases[i].dooron==True: s="unlocked"
					elif g.group_bases[i].dooron==False: s="locked"

					m+="The base of "+g.group_bases[i].name+" "+s+" with "+str(g.group_bases[i].health)+" base health "
					m+=" is "
					if level==2:
						m+="above, "
					elif level==0:
						m+="below, "
					m+=(calculate_x_y_string(calculate_x_y_angle(index.x, index.y, g.group_bases[i].x, g.group_bases[i].y, index.facing)
						)
					   +", "
					   +str(round(index.distancecheck(g.group_bases[i].x, g.group_bases[i].y, g.group_bases[i].z))
						)
					   +" feet away. "
					)
					menu.add(m,str(g.group_bases[i].x)+","+str(g.group_bases[i].y)+","+str(g.group_bases[i].z))
					m=""

			for i in range(len(g.motors)):
				if (get_3d_distance(index.x, index.y, index.z, string_to_number(g.motors[i].x), string_to_number(g.motors[i].y), string_to_number(g.motors[i].z))
				   <=30
					and g.motors[i].map==index.map
				):
					level=1
					if g.motors[i].z>index.z:
						level=2
					elif g.motors[i].z<index.z:
						level=0
					else:
						level=1
					m+="a motor of "+g.motors[i].owner+""
					m+=" "+str(g.motors[i].health)+" health "

					m+=" is "
					if level==2:
						m+="above, "
					elif level==0:
						m+="below, "
					m+=(calculate_x_y_string(calculate_x_y_angle(index.x, index.y, g.motors[i].x, g.motors[i].y, index.facing)
						)
					   +", "
					   +str(round(index.distancecheck(g.motors[i].x, g.motors[i].y, g.motors[i].z))
						)
					   +" feet away. "
					)
					menu.add(m,str(g.motors[i].x)+","+str(g.motors[i].y)+","+str(g.motors[i].z))
					m=""
			for i in range(len(g.bikes)):
				if (get_3d_distance(index.x, index.y, index.z, string_to_number(g.bikes[i].x), string_to_number(g.bikes[i].y), string_to_number(g.bikes[i].z))
				   <=30
					and g.bikes[i].map==index.map
				):
					level=1
					if g.bikes[i].z>index.z:
						level=2
					elif g.bikes[i].z<index.z:
						level=0
					else:
						level=1
					m+="a bike of "+g.bikes[i].owner+" "

					m+=" is "
					if level==2:
						m+="above, "
					elif level==0:
						m+="below, "
					m+=(calculate_x_y_string(calculate_x_y_angle(index.x, index.y, g.bikes[i].x, g.bikes[i].y, index.facing)
						)
					   +", "
					   +str(round(index.distancecheck(g.bikes[i].x, g.bikes[i].y, g.bikes[i].z))
						)
					   +" feet away. "
					)
					menu.add(m,str(g.bikes[i].x)+","+str(g.bikes[i].y)+","+str(g.bikes[i].z))
					m=""

			for i in range(len(g.ladders)):
				if (get_3d_distance(index.x, index.y, index.z, string_to_number(g.ladders[i].minx), string_to_number(g.ladders[i].miny), string_to_number(g.ladders[i].minz))
				   <=30
					and g.ladders[i].map==index.map
				):
					level=1
					if g.ladders[i].minz>index.z:
						level=2
					elif g.ladders[i].minz<index.z:
						level=0
					else:
						level=1
					m+="a ladder of "+g.ladders[i].owner+""

					m+=" is "
					if level==2:
						m+="above, "
					elif level==0:
						m+="below, "
					m+=(calculate_x_y_string(calculate_x_y_angle(index.x, index.y, g.ladders[i].minx, g.ladders[i].miny, index.facing)
						)
					   +", "
					   +str(round(index.distancecheck(g.ladders[i].minx, g.ladders[i].miny, g.ladders[i].minz))
						)
					   +" feet away. "
					)
					menu.add(m,str(g.ladders[i].minx)+","+str(g.ladders[i].miny)+","+str(g.ladders[i].minz))
					m=""

			for i in range(len(g.barricades)):
				if (get_3d_distance(index.x, index.y, index.z, string_to_number(g.barricades[i].minx), string_to_number(g.barricades[i].miny), string_to_number(g.barricades[i].minz))
				   <=30
					and g.barricades[i].map==index.map
				):
					level=1
					if g.barricades[i].minz>index.z:
						level=2
					elif g.barricades[i].minz<index.z:
						level=0
					else:
						level=1
					m+="a barricade of "+g.barricades[i].owner+" with "+str(g.barricades[i].health)+" health"

					m+=" is "
					if level==2:
						m+="above, "
					elif level==0:
						m+="below, "
					m+=(calculate_x_y_string(calculate_x_y_angle(index.x, index.y, g.barricades[i].minx, g.barricades[i].miny, index.facing)
						)
					   +", "
					   +str(round(index.distancecheck(g.barricades[i].minx, g.barricades[i].miny, g.barricades[i].minz))
						)
					   +" feet away. "
					)
					menu.add(m,str(g.barricades[i].minx)+","+str(g.barricades[i].miny)+","+str(g.barricades[i].minz))
					m=""


			for i in range(len(g.timebombs)):
				if (get_3d_distance(index.x, index.y, index.z, string_to_number(g.timebombs[i].x), string_to_number(g.timebombs[i].y), string_to_number(g.timebombs[i].z))
				   <=50
					and g.timebombs[i].map==index.map
				):
					level=1
					if g.timebombs[i].z>index.z:
						level=2
					elif g.timebombs[i].z<index.z:
						level=0
					else:
						level=1
					m+="a timebomb of "+g.timebombs[i].owner+", "+ms_to_readable_time(g.timebombs[i].explodetime-g.timebombs[i].explodetimer.elapsed)+" left before explode "
#						m+=" "+str(g.timebombs[i].health)+" health "

					m+=" is "
					if level==2:
						m+="above, "
					elif level==0:
						m+="below, "
					m+=(calculate_x_y_string(calculate_x_y_angle(index.x, index.y, g.timebombs[i].x, g.timebombs[i].y, index.facing)
						)
					   +", "
					   +str(round(index.distancecheck(g.timebombs[i].x, g.timebombs[i].y, g.timebombs[i].z))
						)
					   +" feet away. "
					)
					menu.add(m,str(g.timebombs[i].x)+","+str(g.timebombs[i].y)+","+str(g.timebombs[i].z))
					m=""


			for i in range(len(g.chests)):
				if (get_3d_distance(index.x, index.y, index.z, string_to_number(g.chests[i].x), string_to_number(g.chests[i].y), string_to_number(g.chests[i].z))
				   <=30
					and g.chests[i].map==index.map
				):
					level=1
					if g.chests[i].z>index.z:
						level=2
					elif g.chests[i].z<index.z:
						level=0
					else:
						level=1
					m+="a chest with "+str(len(g.chests[i].items))+"items "

					m+=" is "
					if level==2:
						m+="above, "
					elif level==0:
						m+="below, "
					m+=(calculate_x_y_string(calculate_x_y_angle(index.x, index.y, g.chests[i].x, g.chests[i].y, index.facing)
						)
					   +", "
					   +str(round(index.distancecheck(g.chests[i].x, g.chests[i].y, g.chests[i].z))
						)
					   +" feet away. "
					)

					menu.add(m,str(g.chests[i].x)+","+str(g.chests[i].y)+","+str(g.chests[i].z))
					m=""
			for i in range(len(g.electrics)):
				if (get_3d_distance(index.x, index.y, index.z, string_to_number(g.electrics[i].x), string_to_number(g.electrics[i].y), string_to_number(g.electrics[i].z))
				   <=30
					and g.electrics[i].map==index.map
				):
					level=1
					if g.electrics[i].z>index.z:
						level=2
					elif g.electrics[i].z<index.z:
						level=0
					else:
						level=1
					m+="a electric with "+str(g.electrics[i].health)+"health "

					m+=" is "
					if level==2:
						m+="above, "
					elif level==0:
						m+="below, "
					m+=(calculate_x_y_string(calculate_x_y_angle(index.x, index.y, g.electrics[i].x, g.electrics[i].y, index.facing)
						)
					   +", "
					   +str(round(index.distancecheck(g.electrics[i].x, g.electrics[i].y, g.electrics[i].z))
						)
					   +" feet away. "
					)

					menu.add(m,str(g.electrics[i].x)+","+str(g.electrics[i].y)+","+str(g.electrics[i].z))
					m=""

			for i in range(len(g.corpses)):
				if (get_3d_distance(index.x, index.y, index.z, string_to_number(g.corpses[i].x), string_to_number(g.corpses[i].y), string_to_number(g.corpses[i].z))
				   <=30
					and g.corpses[i].map==index.map
				):
					level=1
					if g.corpses[i].z>index.z:
						level=2
					elif g.corpses[i].z<index.z:
						level=0
					else:
						level=1
					m+="corpse of "+g.corpses[i].owner+" with "+str(len(g.corpses[i].items))+"items will disappear after "+ms_to_readable_time(600000-g.corpses[i].gotimer.elapsed)

					m+=" is "
					if level==2:
						m+="above, "
					elif level==0:
						m+="below, "
					m+=(calculate_x_y_string(calculate_x_y_angle(index.x, index.y, g.corpses[i].x, g.corpses[i].y, index.facing)
						)
					   +", "
					   +str(round(index.distancecheck(g.corpses[i].x, g.corpses[i].y, g.corpses[i].z))
						)
					   +" feet away. "
					)

					menu.add(m,str(g.corpses[i].x)+","+str(g.corpses[i].y)+","+str(g.corpses[i].z))
					m=""


			for i in range(len(g.items)):
				if (get_3d_distance(index.x, index.y, index.z, string_to_number(g.items[i].x), string_to_number(g.items[i].y), string_to_number(g.items[i].z))
				   <=30
					and g.items[i].map==index.map
				):
					level=1
					if g.items[i].z>index.z:
						level=2
					elif g.items[i].z<index.z:
						level=0
					else:
						level=1
					m+=""+str(g.items[i].itemamount)+" "+g.items[i].itemname+" "
					m+=" is "
					if level==2:
						m+="above, "
					elif level==0:
						m+="below, "
					m+=(calculate_x_y_string(calculate_x_y_angle(index.x, index.y, g.items[i].x, g.items[i].y, index.facing)
						)
					   +", "
					   +str(round(index.distancecheck(g.items[i].x, g.items[i].y, g.items[i].z))
						)
					   +" feet away. "
					)
					menu.add(m,str(g.items[i].x)+","+str(g.items[i].y)+","+str(g.items[i].z))
					m=""

			if len(menu.menuids)==0: menu.add("There is nothing around","nothing",False)
			menu.add("Stop tracking","stop")
			menu.send(e.peer_id)

	elif(parsed[0]=="matchmodepublicbot" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="" or parsed[1]=="back":
				return
			if parsed[1]=="0":
				for m in g.matches:
					if m.owner==g.players[index].name: send_reliable(e.peer_id,"The match you created before didn't end yet, please wait for it to end before you can create a new match.",0); return

				newmatch(g.players[index].name,g.players[index].matchtypeamount,g.players[index].mmode,"",0)
				return
			else:
				for m in g.matches:
					if m.owner==g.players[index].name: send_reliable(e.peer_id,"The match you created before didn't end yet, please wait for it to end before you can create a new match.",0); return

				newmatch(g.players[index].name,g.players[index].matchtypeamount,g.players[index].mmode,"",-1)
				return
	elif(parsed[0]=="matchmodeprivatebot" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="" or parsed[1]=="back":
				return
			if parsed[1]=="0":
				for m in g.matches:
					if m.owner==g.players[index].name: send_reliable(e.peer_id,"The match you created before didn't end yet, please wait for it to end before you can create a new match.",0); return

				newmatch(g.players[index].name,g.players[index].matchtypeamount,g.players[index].mmode,g.players[index].matchpassword,0)
				return
			else:
				for m in g.matches:
					if m.owner==g.players[index].name: send_reliable(e.peer_id,"The match you created before didn't end yet, please wait for it to end before you can create a new match.",0); return

				newmatch(g.players[index].name,g.players[index].matchtypeamount,g.players[index].mmode,g.players[index].matchpassword,-1)
				return
	elif parsed[0]=="unload":
		if parsed[0]=="unload":
			index=get_player_index(e.peer_id)
			if index>-1:
				if g.players[index].weapon!="punch" and g.players[index].weapon2!="feet" and g.players[index].weapon!="" and g.players[index].weapon2!="": g.n.send_reliable(e.peer_id,"You cannot unload the weapon when you have weapons on both of your hands",0); return
				if 1:
					if g.players[index].weapon!="punch":
						if g.players[index].weapon=="punch" or g.players[index].weapon=="feet" or g.players[index].weapon=="stick" or g.players[index].weapon=="knife" or g.players[index].weapon=="wooden_sword" or g.players[index].weapon=="stone_sword" or g.players[index].weapon=="diamond_sword":
							if not g.players[index].android and not g.players[index].ios: g.n.send_reliable(g.players[index].peer_id, "this weapon doesn't take ammo", 0)
							return
						elif g.players[index].weapon=="":
							g.n.send_reliable(g.players[index].peer_id, "You have not equipped a weapon right now.", 0)
							return
						elif g.players[index].get_ammo_count_from(g.players[index].weapon)<1:
							return
						g.players[index].playsound("draw1")
						c=g.players[index].get_ammo_count(g.players[index].weapon)
						g.players[index].give(get_ammotype(g.players[index].weapon), c)
						g.players[index].ammogive(g.players[index].weapon, -g.players[index].get_ammo_count_from(g.players[index].weapon))
					elif g.players[index].weapon2!="feet":
						if g.players[index].weapon2=="punch" or g.players[index].weapon2=="feet" or g.players[index].weapon2=="stick" or g.players[index].weapon2=="knife" or g.players[index].weapon2=="wooden_sword" or g.players[index].weapon2=="stone_sword" or g.players[index].weapon2=="diamond_sword":
							g.n.send_reliable(g.players[index].peer_id, "this weapon doesn't take ammo", 0)
							return
						elif g.players[index].weapon2=="":
							g.n.send_reliable(g.players[index].peer_id, "You have not equipped a weapon right now.", 0)
							return
						elif g.players[index].get_ammo_count_from(g.players[index].weapon2)<1:
							return
						g.players[index].playsound("draw1")
						c=g.players[index].get_ammo_count(g.players[index].weapon2)
						g.players[index].give(get_ammotype(g.players[index].weapon2), c)
						g.players[index].ammogive(g.players[index].weapon2, -g.players[index].get_ammo_count_from(g.players[index].weapon2))

	elif parsed[0]=="weaponinfo":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if g.players[index].weapon=="": g.n.send_reliable(e.peer_id,"You have no weapon equipped.",0); return
			if g.players[index].weapon in guns:
				if g.players[index].weapon not in g.players[index].silenced:
					if not g.players[index].adrenaline: g.n.send_reliable(e.peer_id,"The weapon "+g.players[index].weapon+" requires "+get_ammotype(g.players[index].weapon)+" ammo and can hold up to "+str(get_max_ammo(g.players[index].weapon))+" ammo. It has no silencer inserted .It can be fired every "+str(g.wdata[g.players[index].weapon].split()[0])+" ms. It has a range of "+str(get_weapon_range(g.players[index].weapon,[],index))+", and a spread of "+str(get_weapon_spread(g.players[index].weapon))+". Its damage is between "+str(g.players[index].get_plus_damage()+get_mindamage(g.players[index].weapon))+" and "+str(g.players[index].get_plus_damage()+get_maxdamage(g.players[index].weapon))+".",0)
					if g.players[index].adrenaline: g.n.send_reliable(e.peer_id,"The weapon "+g.players[index].weapon+" requires "+get_ammotype(g.players[index].weapon)+" ammo and can hold up to "+str(get_max_ammo(g.players[index].weapon))+" ammo. It has no silencer inserted .It can be fired every "+str(int(g.wdata[g.players[index].weapon].split()[0])-(int(g.wdata[g.players[index].weapon].split()[0])*25//100))+" ms. It has a range of "+str(get_weapon_range(g.players[index].weapon,[],index))+", and a spread of "+str(get_weapon_spread(g.players[index].weapon))+". Its damage is between "+str(g.players[index].get_plus_damage()+get_mindamage(g.players[index].weapon))+" and "+str(g.players[index].get_plus_damage()+get_maxdamage(g.players[index].weapon))+".",0)
				if g.players[index].weapon in g.players[index].silenced:
					if not g.players[index].adrenaline: g.n.send_reliable(e.peer_id,"The weapon "+g.players[index].weapon+" requires "+get_ammotype(g.players[index].weapon)+" ammo and can hold up to "+str(get_max_ammo(g.players[index].weapon))+" ammo. It has silencer inserted .It can be fired every "+str(g.wdata[g.players[index].weapon].split()[0])+" ms. It has a range of "+str(get_weapon_range(g.players[index].weapon,[],index)//2)+" due to silencer, and a spread of "+str(get_weapon_spread(g.players[index].weapon))+". Its damage is between "+str(g.players[index].get_plus_damage()+get_mindamage(g.players[index].weapon))+" and "+str(g.players[index].get_plus_damage()+get_maxdamage(g.players[index].weapon))+".",0)
					if g.players[index].adrenaline: g.n.send_reliable(e.peer_id,"The weapon "+g.players[index].weapon+" requires "+get_ammotype(g.players[index].weapon)+" ammo and can hold up to "+str(get_max_ammo(g.players[index].weapon))+" ammo. It has silencer inserted .It can be fired every "+str(int(g.wdata[g.players[index].weapon].split()[0])-(int(g.wdata[g.players[index].weapon].split()[0])*25//100))+" ms. It has a range of "+str(get_weapon_range(g.players[index].weapon,[],index)//2)+" due to silencer, and a spread of "+str(get_weapon_spread(g.players[index].weapon))+". Its damage is between "+str(g.players[index].get_plus_damage()+get_mindamage(g.players[index].weapon))+" and "+str(g.players[index].get_plus_damage()+get_maxdamage(g.players[index].weapon))+".",0)
			if g.players[index].weapon not in guns:
				if not g.players[index].adrenaline: g.n.send_reliable(e.peer_id,"The weapon "+g.players[index].weapon+" does not require ammo. It has a range of "+str(get_weapon_range(g.players[index].weapon,[],index))+", and a spread of "+str(get_weapon_spread(g.players[index].weapon))+". It can be fired every "+str(g.wdata[g.players[index].weapon].split()[0])+" ms. Its damage is between "+str(g.players[index].get_plus_damage()+get_mindamage(g.players[index].weapon))+" and "+str(g.players[index].get_plus_damage()+get_maxdamage(g.players[index].weapon))+".",0)
				if g.players[index].adrenaline: g.n.send_reliable(e.peer_id,"The weapon "+g.players[index].weapon+" does not require ammo. It has a range of "+str(get_weapon_range(g.players[index].weapon,[],index))+", and a spread of "+str(get_weapon_spread(g.players[index].weapon))+". It can be fired every "+str(int(g.wdata[g.players[index].weapon].split()[0])-(int(g.wdata[g.players[index].weapon].split()[0])*25//100))+" ms. Its damage is between "+str(g.players[index].get_plus_damage()+get_mindamage(g.players[index].weapon))+" and "+str(g.players[index].get_plus_damage()+get_maxdamage(g.players[index].weapon))+".",0)
	elif parsed[0]=="weaponinfo2":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if g.players[index].weapon2=="": g.n.send_reliable(e.peer_id,"You have no weapon equipped.",0); return
			if g.players[index].weapon2 in guns:
				if g.players[index].weapon2 not in g.players[index].silenced:
					if not g.players[index].adrenaline: g.n.send_reliable(e.peer_id,"The weapon "+g.players[index].weapon2+" requires "+get_ammotype(g.players[index].weapon2)+" ammo and can hold up to "+str(get_max_ammo(g.players[index].weapon2))+" ammo. It has no silencer inserted .It can be fired every "+str(g.wdata[g.players[index].weapon2].split()[0])+" ms. It has a range of "+str(get_weapon_range(g.players[index].weapon2,[],index))+", and a spread of "+str(get_weapon_spread(g.players[index].weapon2))+". Its damage is between "+str(g.players[index].get_plus_damage()+get_mindamage(g.players[index].weapon2))+" and "+str(g.players[index].get_plus_damage()+get_maxdamage(g.players[index].weapon2))+".",0)
					if g.players[index].adrenaline: g.n.send_reliable(e.peer_id,"The weapon "+g.players[index].weapon2+" requires "+get_ammotype(g.players[index].weapon2)+" ammo and can hold up to "+str(get_max_ammo(g.players[index].weapon2))+" ammo. It has no silencer inserted .It can be fired every "+str(int(g.wdata[g.players[index].weapon2].split()[0])-(int(g.wdata[g.players[index].weapon2].split()[0])*25//100))+" ms. It has a range of "+str(get_weapon_range(g.players[index].weapon2,[],index))+", and a spread of "+str(get_weapon_spread(g.players[index].weapon2))+". Its damage is between "+str(g.players[index].get_plus_damage()+get_mindamage(g.players[index].weapon2))+" and "+str(g.players[index].get_plus_damage()+get_maxdamage(g.players[index].weapon2))+".",0)
				if g.players[index].weapon2 in g.players[index].silenced:
					if not g.players[index].adrenaline: g.n.send_reliable(e.peer_id,"The weapon "+g.players[index].weapon2+" requires "+get_ammotype(g.players[index].weapon2)+" ammo and can hold up to "+str(get_max_ammo(g.players[index].weapon2))+" ammo. It has silencer inserted. It can be fired every "+str(g.wdata[g.players[index].weapon2].split()[0])+" ms. It has a range of "+str(get_weapon_range(g.players[index].weapon2,[],index)//2)+" due to silencer, and a spread of "+str(get_weapon_spread(g.players[index].weapon2))+". Its damage is between "+str(g.players[index].get_plus_damage()+get_mindamage(g.players[index].weapon2))+" and "+str(g.players[index].get_plus_damage()+get_maxdamage(g.players[index].weapon2))+".",0)
					if g.players[index].adrenaline: g.n.send_reliable(e.peer_id,"The weapon "+g.players[index].weapon2+" requires "+get_ammotype(g.players[index].weapon2)+" ammo and can hold up to "+str(get_max_ammo(g.players[index].weapon2))+" ammo. It has silencer inserted. It can be fired every "+str(int(g.wdata[g.players[index].weapon2].split()[0])-(int(g.wdata[g.players[index].weapon2].split()[0])*25//100))+" ms. It has a range of "+str(get_weapon_range(g.players[index].weapon2,[],index)//2)+" due to silencer, and a spread of "+str(get_weapon_spread(g.players[index].weapon2))+". Its damage is between "+str(g.players[index].get_plus_damage()+get_mindamage(g.players[index].weapon2))+" and "+str(g.players[index].get_plus_damage()+get_maxdamage(g.players[index].weapon2))+".",0)

			if g.players[index].weapon2 not in guns:
				if not g.players[index].adrenaline: g.n.send_reliable(e.peer_id,"The weapon "+g.players[index].weapon2+" does not require ammo. It has a range of "+str(get_weapon_range(g.players[index].weapon2,[],index))+", and a spread of "+str(get_weapon_spread(g.players[index].weapon2))+". It can be fired every "+str(g.wdata[g.players[index].weapon2].split()[0])+" ms. Its damage is between "+str(g.players[index].get_plus_damage()+get_mindamage(g.players[index].weapon2))+" and "+str(get_maxdamage(g.players[index].weapon2))+".",0)
				if g.players[index].adrenaline: g.n.send_reliable(e.peer_id,"The weapon "+g.players[index].weapon2+" does not require ammo. It has a range of "+str(get_weapon_range(g.players[index].weapon2,[],index))+", and a spread of "+str(get_weapon_spread(g.players[index].weapon2))+". It can be fired every "+str(int(g.wdata[g.players[index].weapon2].split()[0])-(int(g.wdata[g.players[index].weapon2].split()[0])*25//100))+" ms. Its damage is between "+str(g.players[index].get_plus_damage()+get_mindamage(g.players[index].weapon2))+" and "+str(get_maxdamage(g.players[index].weapon2))+".",0)


	elif(parsed[0]=="reload"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
		
			if g.players[index].weapon!="punch" and g.players[index].weapon2!="feet" and g.players[index].weapon!="" and g.players[index].weapon2!="": g.n.send_reliable(e.peer_id,"You cannot reload the weapon when you have weapons on both of your hands",0); return
			if(g.players[index].firing==False and g.players[index].reloading==False):
			
				if(g.players[index].weapon2=="" and g.players[index].weapon==""):
				
					g.n.send_reliable(g.players[index].peer_id, "You haven't selected any weapons yet.", 0)
					return
					
				if(g.players[index].weapon!="punch" and requires_ammo(g.players[index].weapon)==False):
				
					g.n.send_reliable(g.players[index].peer_id,"This weapon "+g.players[index].weapon+" does not take ammo",0)
					return
					
				if(g.players[index].weapon2!="feet" and requires_ammo(g.players[index].weapon2)==False):
				
					g.n.send_reliable(g.players[index].peer_id,"This weapon "+g.players[index].weapon2+" does not take ammo",0)
					return
					

				if g.players[index].weapon!="punch":
					if(g.players[index].get_ammo_count_from(g.players[index].weapon)==get_max_ammo(g.players[index].weapon)):
				
						return
					
					if(g.players[index].get_item_count(get_ammotype(g.players[index].weapon))<=0):
				
						g.n.send_reliable(g.players[index].peer_id,"you dont have "+get_ammotype(g.players[index].weapon)+" ammo!",0)
						return
					
				if g.players[index].weapon2!="feet":
					if(g.players[index].get_ammo_count_from(g.players[index].weapon2)==get_max_ammo(g.players[index].weapon2)):
				
						return
					
					if(g.players[index].get_item_count(get_ammotype(g.players[index].weapon2))<=0):
				
						g.n.send_reliable(g.players[index].peer_id,"you dont have "+get_ammotype(g.players[index].weapon2)+" ammo!",0)
						return
					

				if 1:
				
					if g.players[index].weapon!="punch" or g.players[index].weapon2!="feet": g.n.send_reliable(g.players[index].peer_id,"reloading",0)
					if g.players[index].weapon!="punch": ammoamount=g.players[index].ammocheck(g.players[index].weapon)
					if g.players[index].weapon2!="feet": ammoamount=g.players[index].ammocheck(g.players[index].weapon2)
					if g.players[index].weapon=="berettaM9":
						g.players[index].playsoundmoving("ak47reload")

					if g.players[index].weapon!="punch" or g.players[index].weapon!="berettaM9":
						g.players[index].playsoundmoving(g.players[index].weapon+"reload")
					if g.players[index].weapon2=="berettaM9":
						g.players[index].playsoundmoving("ak47reload")

					if g.players[index].weapon2!="feet" or g.players[index].weapon2!="berettaM9":
						g.players[index].playsoundmoving(g.players[index].weapon2+"reload")
					if g.players[index].weapon!="punch": g.players[index].reloadtime=get_reloadtime(g.players[index].weapon)
					if g.players[index].weapon2!="feet": g.players[index].reloadtime=get_reloadtime(g.players[index].weapon2)
					g.players[index].reloadtimer.restart()
					g.players[index].reloading=True
					
				
	elif parsed[0]=="deleteline":				
		if parsed[0]=="deleteline":
			index=get_player_index(e.peer_id)
			if index>-1:
				o=get_map_index(g.players[index].map)
				if o<0:
					g.n.send_reliable(g.players[index].peer_id, "There's have some problems with this map. Please contact with developers", 0)
					return
				if (g.players[index].builder==True or g.players[index].dev==True or g.players[index].is_admin()==True):
					emessage=e.message
					name=g.players[index].name
					if  send_yesno_question(g.players[index].peer_id,"Are you sure you want to delete this line?")=="yes":
						index=get_player_index_from(name)
						rawdata=file_get_contents("maps/"+g.players[index].map+".map")
						lines=string_split(rawdata, "\n", True)
						ld=string_split(string_replace(emessage, "deleteline ", "", False), ":", False)
						for i in range(len(lines)):
							if lines[i]==string_replace(emessage, "deleteline ", "", False):
								g.n.send_reliable(g.players[index].peer_id, ""+lines[i]+" deleted", 0)
								lines.remove(lines[i])
								break
						file_put_contents("maps/"+g.players[index].map+".map", linear(lines))
						update_map(g.players[index].map)

	elif parsed[0]=="addline":
		if parsed[0]=="addline":
			index=get_player_index(e.peer_id)
			if index>-1:
				map=open("maps/"+g.players[index].map+".map", "a")
				map.write("\n"+e.message.replace("addline ",""))
				map.close()
				update_map(g.players[index].map)
	elif parsed[0]=="editlinemenu":
		g.n.send_reliable(e.peer_id, "editline "+string_replace(e.message, "editlinemenu ", "", False), 0)
	elif string_contains(e.message, "editlineSPLITS_THE_PARTS_OF_EDITLINE", 1)>-1:
		if string_contains(e.message, "editlineSPLITS_THE_PARTS_OF_EDITLINE", 1)>-1:
			index=get_player_index(e.peer_id)
			if index>-1:
				p=string_split(e.message, "SPLITS_THE_PARTS_OF_EDITLINE", True)
				old=p[1]
				new=p[2]
				ld=string_split(new, ":", False)
				if not g.players[index].is_admin():
					if g.players[index].is_admin()==False or g.players[index].builder==False:
						g.n.send_reliable(e.peer_id, "error, only admins can do this", 0)
						return
				rawdata=file_get_contents("maps/"+g.players[index].map+".map")
				lines=string_split(rawdata, "\n", True)
				for i in range(len(lines)):
					if lines[i]==old:
						lines[i]=new
				file_put_contents("maps/"+g.players[index].map+".map", linear(lines), "w")
				update_map(g.players[index].map)

	elif parsed[0]=="buildobj" and len(parsed)>1:
		if parsed[0]=="buildobj" and len(parsed)>1:
			index=get_player_index(e.peer_id)
			if index>-1:
				o=get_map_index(g.players[index].map)
				if o<0:
					g.n.send_reliable(g.players[index].peer_id, "There's have some problems with this map.", 0)
					return
				if g.players[index].builder or g.players[index].is_admin()==True or g.players[index].dev==True:
					what=parsed[1]
					if what=="delete":
						rawdata=file_get_contents("maps/"+g.players[index].map+".map")
						send_reliable(e.peer_id, "menudeleteline "+rawdata, 0)
					if what=="edit":
						rawdata=file_get_contents("maps/"+g.players[index].map+".map")
						g.n.send_reliable(e.peer_id, "menueditline "+rawdata, 0)
					if what=="edit2":
						rawdata=file_get_contents("maps/"+g.players[index].map+".map")
						g.n.send_reliable(e.peer_id, "editmap "+rawdata, 0)


					if what=="add":
						g.n.send_reliable(e.peer_id, "addline", 0)
					if what=="reverb":
						g.n.send_reliable(g.players[index].peer_id, "buildreverb", 0)
					if what=="chest":
						g.n.send_reliable(g.players[index].peer_id, "buildchest", 0)

					if what=="door":
						g.n.send_reliable(g.players[index].peer_id, "builddoor", 0)
					if what=="eaxreverb":
						g.n.send_reliable(g.players[index].peer_id, "buildeaxreverb", 0)
					if what=="echo":
						g.n.send_reliable(g.players[index].peer_id, "buildecho", 0)
					if what=="staircase":
						g.n.send_reliable(g.players[index].peer_id, "buildstairs", 0)

					if what=="tile":
						g.n.send_reliable(g.players[index].peer_id, "buildtile", 0)
					if what=="hidden_area":
						g.n.send_reliable(g.players[index].peer_id, "buildhidden_area", 0)

					elif what=="wall":
						g.n.send_reliable(g.players[index].peer_id, "buildwall", 0)
					elif what=="wall2":
						g.n.send_reliable(g.players[index].peer_id, "buildwall2", 0)


					elif what=="src":
						g.n.send_reliable(g.players[index].peer_id, "buildsrc", 0)
					elif what=="src2":
						g.n.send_reliable(g.players[index].peer_id, "buildsrc2", 0)
					elif what=="amb":
						g.n.send_reliable(g.players[index].peer_id, "buildamb", 0)
					elif what=="electric":
						g.n.send_reliable(g.players[index].peer_id, "buildelectric", 0)

					elif what=="zone":
						g.n.send_reliable(g.players[index].peer_id, "buildzone", 0)
					elif what=="sign":
						g.n.send_reliable(g.players[index].peer_id, "buildsign", 0)

	elif parsed[0]=="outmotor":
		if parsed[0]=="outmotor":
			index=get_player_index(e.peer_id)
			if index>-1:
				if g.players[index].inve==True and g.motors[g.players[index].vi].pitch!=100:
					g.players[index].z+=10
					g.n.send_reliable(e.peer_id,"motorvolume -50",0)
					g.n.send_reliable(e.peer_id,"move "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z),0)
				if g.players[index].vi>-1:
					g.players[index].playsound("motorescape")
					v=g.players[index].vi

					g.players[index].inve=False
					send_reliable(g.players[index].peer_id, "motorunspawn", 0)
					pv=g.motors[g.players[index].vi].players.find(g.players[index].name)
					if pv>-1:
						g.motors[g.players[index].vi].players.remove(g.motors[g.players[index].vi].players[pv])
					g.players[index].vi=-1
					g.players[index].z+=5
					g.n.send_reliable(e.peer_id,"move "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z),0)
	elif parsed[0]=="motorengine":
		if parsed[0]=="motorengine":
			index=get_player_index(e.peer_id)
			if index>-1:
				v=g.players[index].vi
				if v<0:
					return
				if len(g.motors[g.players[index].vi].players)==0 or g.motors[g.players[index].vi].players[0]!=g.players[index].name: return
				if g.motors[v].pitch!=100:
					send_reliable(g.players[index].peer_id, "it would be very strange to turn off the engine of a moving motor", 0)
					return
				if g.motors[g.players[index].vi].running==True:
					g.motors[g.players[index].vi].speed=-1
					destroy_moving_sound(g.motors[g.players[index].vi].mid)
					g.motors[g.players[index].vi].running=False
					g.players[index].playsound("motorstop")

					return
				if g.motors[g.players[index].vi].running==False:
					g.motors[g.players[index].vi].running=True
					g.players[index].playsound("motorstart")

					g.motors[g.players[index].vi].mid=spawn_moving_sound("motorengine.ogg", g.motors[g.players[index].vi].x, g.motors[g.players[index].vi].y, g.motors[g.players[index].vi].z, g.motors[g.players[index].vi].map+"", "", 100)
					g.motors[g.players[index].vi].pitch=100
					return
			else:
				return
	elif parsed[0]=="motorhorn":
		if parsed[0]=="motorhorn":
			index=get_player_index(e.peer_id)
			if index>-1:
				v=g.players[index].vi
				if v<0:
					return
				if len(g.motors[g.players[index].vi].players)==0 or g.motors[g.players[index].vi].players[0]!=g.players[index].name: return
				if g.players[index].vi<0:
					return
				if g.motors[g.players[index].vi].running==False:
					send_reliable(g.players[index].peer_id, "the horn is not active because the motor is not running", 0)
					return
				if g.players[index].motorhorntimer.elapsed>=200:
					g.players[index].motorhorntimer.restart()
					g.players[index].playsound("motorhorn")
			else:
				return
	elif parsed[0]=="vup":
		if parsed[0]=="vup":
			index=get_player_index(e.peer_id)
			if index>-1:
				v=g.players[index].vi
				if v<0:
					return
				if len(g.motors[g.players[index].vi].players)==0 or g.motors[g.players[index].vi].players[0]!=g.players[index].name: return
				if g.motors[g.players[index].vi].running==True:
					if g.motors[v].pitch==100: g.n.send_reliable(e.peer_id,"restartmotor",0)
					g.motors[v].pitch+=1

					if g.motors[v].pitch>g.motors[v].maxpitch:
						g.motors[v].pitch=g.motors[v].maxpitch
					update_moving_sound(g.motors[v].mid, g.motors[v].x, g.motors[v].y, g.motors[v].z, g.motors[v].pitch)
			else:
				return
	elif parsed[0]=="vdown":
		if parsed[0]=="vdown":
			index=get_player_index(e.peer_id)
			if index>-1:
				v=g.players[index].vi
				if v<0:
					return
				if len(g.motors[g.players[index].vi].players)==0 or g.motors[g.players[index].vi].players[0]!=g.players[index].name: return
				if g.motors[g.players[index].vi].running==False:
					return
				if g.motors[g.players[index].vi].breaktimer.elapsed>=g.motors[g.players[index].vi].breaktime:
					g.motors[g.players[index].vi].breaktimer.restart()
					if g.motors[v].pitch<100:
						g.motors[v].pitch=100
					if g.motors[v].pitch>100:
						g.motors[v].pitch-=2
					update_moving_sound(g.motors[v].mid, g.motors[v].x, g.motors[v].y, g.motors[v].z, g.motors[v].pitch)

	elif parsed[0]=="addinmap":
		if parsed[0]=="addinmap":
			index=get_player_index(e.peer_id)
			if index>-1:
				o=get_map_index(g.players[index].map)
				if o<0:
					g.n.send_reliable(g.players[index].peer_id, "There's have some problems with this map.", 0)
					return
				if g.players[index].builder==True or g.players[index].dev==True or g.players[index].is_admin()==True:
					maptext=string_replace(e.message, "addinmap ", "", False)
					f=open("maps/"+g.players[index].map+".map", "r")
					mapdata=f.read()
					f.close()
					mapdata+="\n"+maptext
					f=open("maps/"+g.players[index].map+".map", "w")
					f.write(mapdata)
					f.close()
					g.n.send_reliable(g.players[index].peer_id, "Map updated", 0)
					update_map(g.players[index].map)
	elif parsed[0]=="build":
		if parsed[0]=="build":
			index=get_player_index(e.peer_id)
			if index>-1:
				o=get_map_index(g.players[index].map)
				if o<0:
					g.n.send_reliable(g.players[index].peer_id, "There's have some problems with this map.", 0)
					return
				if g.players[index].is_builder() or g.players[index].dev==True or g.players[index].is_admin()==True:
					o=get_map_index(g.players[index].map)
					if o<0:
						g.n.send_reliable(g.players[index].peer_id, "There's have some problems with this map.", 0)
						return
					m=server_menu()
					m.initial_packet="buildobj"
					m.store=False
					m.intro="Select an option you want to build."
					if o<0:
						g.n.send_reliable(g.players[index].peer_id, "There's have some problems with this map.", 0)
						return

					m.add("Platform", "tile")
					m.add("Chest", "chest")
					m.add("Hidden area", "hidden_area")
					m.add("Staircase", "staircase")
					m.add("wall", "wall")
					m.add("breakable wall", "wall2")
					m.add("sound source", "src")
					m.add("Ignore ambience", "src2")
					m.add("electric pole", "electric")
					m.add("ambience", "amb")
					m.add("zone", "zone")
					m.add("sign", "sign")

					m.add("reverb", "reverb")
					m.add("eaxreverb", "eaxreverb")
					m.add("echo", "echo")
					m.add("door","door")
					m.add("add line","add")
					m.add("edit line","edit")
					m.add("delete line","delete")
					m.add("edit map","edit2")
					m.send(e.peer_id)
	elif parsed[0]=="pr" and len(parsed)>2:
		if parsed[0]=="pr" and len(parsed)>2:
			s=""
			un=parsed[1]
			if directory_exists("chars/"+un)==False:
				send_reliable(e.peer_id,"errored no such account found",0)
				return
			compbanned=is_compbanned(parsed[3])
			if compbanned==True:
				if not file_exists("chars/"+un+"/permaban.usr"): send_reliable(e.peer_id, "errored Error. You have been temporary banned. Reason: "+get_compban_reason(parsed[3])+". The ban will end after "+get_compban_end_time(parsed[3]), 0)
				if file_exists("chars/"+un+"/permaban.usr"): send_reliable(e.peer_id, "errored Error. You have been permanently banned. Reason: "+get_compban_reason(parsed[3]),0)
				return

			getmail=file_get_contents("chars/"+un+"/mail.usr")

			if getmail!=parsed[2]:
				send_reliable(e.peer_id,"errored The Email is not correct.",0)
				return

			if file_exists("chars/"+un+"/mailsent.usr")==True:
				try: now=datetime.datetime.now()
				except: now=datetime.now()
				try: target_time = datetime.datetime(now.year, now.month, now.day, 23, 0, 0)
				except: target_time = datetime(now.year, now.month, now.day, 23, 0, 0)
				time_difference = target_time - now
				hours = time_difference.seconds // 3600
				minutes = (time_difference.seconds % 3600) // 60
				seconds = time_difference.seconds % 60

				send_reliable(e.peer_id,"errored You can not recover your password right now. Please try in "+str(hours)+" hours, "+str(minutes)+" minutes, "+str(seconds)+" seconds. If you want to get your password faster, please contact us at contact@nbmstudios.com",0)
				return

			if not file_exists("chars/"+un+"/pass.usr") or not file_exists("chars/"+un+"/mail.usr"):
				send_reliable(e.peer_id,"errored invalid account data",0)
				return
			eml=file_get_contents("chars/"+un+"/mail.usr")
			f=open("chars/"+un+"/mailsent.usr","w")
			f.close()
			f=open("chars/"+parsed[1]+"/pass.usr", "r")
			p=f.read()
			f.close()
			s+="Hello<br><br>You Have Requested The Password For The "+un+" Account<br>If You Did Not Make This Request, Ignore This Message<br>The Password Is: "+p+"<br>"
			s+="Please Do Not Reply To This Message<br>"
			s+="Copyright 2025 NBM DIGITAL LTD, all rights reserved<br>"
			s+="website<br>"
			s+="https://nbmstudios.com"
			res=send_mail(eml, "Zero Hour Assault Game Account Password Recovery.", ""+s+"")
			send_reliable(e.peer_id, "checkeml", 0)
	elif parsed[0]=="verifycode":
		user=parsed[1]
		code=parsed[2]
		if file_get_contents("chars/"+user+"/verifycode.usr")!=code:
			g.n.send_reliable(e.peer_id,"verifyincorrect",0)
		else:
			file_delete("chars/"+user+"/pending_email_verify.usr")
			auth_computers=file_get_contents("chars/"+user+"/authorized_compids.usr").split("\n")
			if parsed[3] not in auth_computers:
				auth_computers.append(parsed[3])
			file_put_contents("chars/"+user+"/authorized_compids.usr","\n".join(auth_computers))
			file_put_contents("chars/"+user+"/lastverify.usr",pickle.dumps(datetime.now()),"wb")
			g.n.send_reliable(e.peer_id,"verifycorrect",0)
	elif parsed[0]=="cheat":
		index=get_player_index(e.peer_id)
		if index>-1:
			adminsend(""+g.players[index].name+" is using cheat tools!")
			notify_admins("zero hour assault, "+g.players[index].name+" is using cheat tools!")
			g.n.broadcast(g.players[index].name+" was kicked out of the game due to using cheat tools!",2)
			g.n.broadcast("play_s misc181.ogg",0)
			g.n.send_reliable(g.players[index].peer_id,"cheat",0)
			remove_from_server(index)
	elif parsed[0]=="sendverify":
		user=parsed[1]
		verifycode=randomstring()
		file_put_contents("chars/"+user+"/verifycode.usr",verifycode)
		file_put_contents("chars/"+user+"/lastverify.usr",pickle.dumps(datetime.now()),"wb")
		if file_exists("chars/"+user+"/pending_email_verify.usr"):
			send_mail(file_get_contents("chars/"+user+"/mail.usr"),"Zero Hour Assault: Account Verification",'Hello,<br>You have registered a Zero Hour Assault account with the username <strong>'+user+'</strong>.<br>To verify your email and activate your account, please enter the following code in the game:<br><strong>'+verifycode+'</strong><br>If you did not register, please ignore this email.<br>Best regards,<br>NBM Studios<br><a href="https://nbmstudios.com">https://nbmstudios.com</a><br>© 2025 NBM Studios. All rights reserved.')
		else:
			send_mail(file_get_contents("chars/"+user+"/mail.usr"),"Zero Hour Assault: Computer Authorization", 'Hello dear '+user+',<br>You have attempted to log into your account from a device different from the one you originally used to create it<br>To proceed and authorize this device, please use the following code:<br><strong>' + verifycode + '</strong><br>If you did not initiate this login attempt, it may indicate that someone has gained access to your password and tried to log into your account. We strongly recommend changing your password immediately<br>To change your password, go to the "Account Security" section in the game menu<br>Best regards,<br>NBM Studios<br>Visit our website: <a href="https://nbmstudios.com">https://nbmstudios.com</a><br>This is an automated message. Please do not reply to this email. For any inquiries, please contact us at <a href="mailto:contact@nbmstudios.com">contact@nbmstudios.com</a><br>© 2025 NBM Studios. All rights reserved.')

	elif(parsed[0]=="login" and len(parsed) > 4):
	
		login(parsed[1], parsed[2], parsed[3], parsed[4], e.peer_id)
		
	elif parsed[0]=="pingr" and len(parsed)>1:
		index=get_player_index(e.peer_id)
		if index>-1:
			index2=get_player_index_from(parsed[1])
			if index2>-1:
				if not g.players[index2].pinging:
					return
				g.n.send_reliable(g.players[index2].peer_id, "play_s misc128.ogg", 0)
				g.n.send_reliable(g.players[index2].peer_id, g.players[index].name+"'s ping Approximately  took "+str(g.players[index2].pingtimer.elapsed)+" milliseconds", 2)
				g.players[index2].pinging=False
				g.players[index2].pingtimer.restart()

	elif(parsed[0]=="draw" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
		
#				if g.players[index].matchmode=="g2" or g.players[index].matchmode=="teamg2" or g.players[index].matchmode=="g" or g.players[index].matchmode=="teamg"or g.players[index].matchmode=="sword" or g.players[index].matchmode=="teamsword": return
#				if g.players[index].matchmode=="teamk" and parsed[1]!="knife": return
			if "combo" in g.players[index].map:
				if parsed[1]!="punch" and parsed[1]!="feet": return
			if g.players[index].map=="jail":
				return
#				play(parsed[1]+"draw", g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].map,g.players[index])
			if parsed[1]=="berettaM9":
				g.players[index].playsound("ks123shotgundraw")

			if not g.players[index].dead or parsed[1]!="berettaM9":
				g.players[index].playsound(""+parsed[1]+"draw")
			try:
				if not g.players[index].adrenaline: g.n.send_reliable(g.players[index].peer_id,"weapondata "+g.wdata[parsed[1]],0)
				if g.players[index].adrenaline: g.n.send_reliable(g.players[index].peer_id,"weapondatafast "+g.wdata[parsed[1]],0)
				g.n.send_reliable(e.peer_id,"cannotdraw",0)
			except:
				return
			g.players[index].weapon=parsed[1]
			g.players[index].get_weapon_properties(g.players[index].weapon)
			g.players[index].firing=False
			g.players[index].set_drawtime(get_drawtime(parsed[1]))

		
	elif(parsed[0]=="draw2" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
		
#				if g.players[index].matchmode=="g2" or g.players[index].matchmode=="teamg2" or g.players[index].matchmode=="g" or g.players[index].matchmode=="teamg"or g.players[index].matchmode=="sword" or g.players[index].matchmode=="teamsword": return
#				if g.players[index].matchmode=="teamk" and parsed[1]!="knife": return
			if "combo" in g.players[index].map:
				if parsed[1]!="punch" and parsed[1]!="feet": return

			if(g.players[index].dead or g.players[index].map=="jail"):
				return
#				play(parsed[1]+"draw", g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].map,g.players[index])
			if parsed[1]=="berettaM9":
				g.players[index].playsound("ks123shotgundraw")

			if parsed[1]!="berettaM9":
				g.players[index].playsound(""+parsed[1]+"draw")
			try:
				if not g.players[index].adrenaline: g.n.send_reliable(g.players[index].peer_id,"weapondata2 "+g.wdata[parsed[1]],0)
				if g.players[index].adrenaline: g.n.send_reliable(g.players[index].peer_id,"weapondata2fast "+g.wdata[parsed[1]],0)
			except:
				return
			g.players[index].weapon2=parsed[1]
			g.players[index].get_weapon_properties(g.players[index].weapon2)
			g.players[index].firing=False
			g.players[index].set_drawtime(get_drawtime(parsed[1]))
		
	elif(parsed[0]=="drawsilent" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
		
#				if g.players[index].matchmode=="g2" or g.players[index].matchmode=="teamg2" or g.players[index].matchmode=="g" or g.players[index].matchmode=="teamg"or g.players[index].matchmode=="sword" or g.players[index].matchmode=="teamsword": return
#				if g.players[index].matchmode=="teamk" and parsed[1]!="knife": return
			if g.players[index].map=="jail":
				return
#				play(parsed[1]+"draw", g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].map,g.players[index])
			try:
				if not g.players[index].adrenaline: g.n.send_reliable(g.players[index].peer_id,"weapondata "+g.wdata[parsed[1]],0)
				if g.players[index].adrenaline: g.n.send_reliable(g.players[index].peer_id,"weapondatafast "+g.wdata[parsed[1]],0)
				g.n.send_reliable(e.peer_id,"cannotdraw",0)
			except:
				return
			g.players[index].weapon=parsed[1]
			g.players[index].get_weapon_properties(g.players[index].weapon)
			g.players[index].firing=False

		
	elif(parsed[0]=="draw2silent" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
		
#				if g.players[index].matchmode=="g2" or g.players[index].matchmode=="teamg2" or g.players[index].matchmode=="g" or g.players[index].matchmode=="teamg"or g.players[index].matchmode=="sword" or g.players[index].matchmode=="teamsword": return
#				if g.players[index].matchmode=="teamk" and parsed[1]!="knife": return
			if g.players[index].map=="jail":
				return
#				play(parsed[1]+"draw", g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].map,g.players[index])
			try:
				if not g.players[index].adrenaline: g.n.send_reliable(g.players[index].peer_id,"weapondata2 "+g.wdata[parsed[1]],0)
				if g.players[index].adrenaline: g.n.send_reliable(g.players[index].peer_id,"weapondata2fast "+g.wdata[parsed[1]],0)
			except:
				return
			g.players[index].weapon2=parsed[1]
			g.players[index].get_weapon_properties(g.players[index].weapon2)
			g.players[index].firing=False

		


	elif(parsed[0]=="playonmap" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
		
			x=g.players[index].x
			y=g.players[index].y
			z=g.players[index].z
			map=g.players[index].map
			for i in range(len(g.players)):
			
				if(g.players[i].name!=g.players[index].name):
				
					g.n.send_reliable(g.players[i].peer_id,string_replace(parsed[1],".ogg","",True)+" "+str(x)+" "+str(y)+" "+str(z)+" "+str(map),3)
					
				
			
		
	elif(parsed[0]=="playsnd" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
		
			soundstring=string_replace(parsed[1], ".ogg","",True)
			play(soundstring, g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].map, g.players[index])
			
	elif parsed[0]=="chest" and len(parsed)>1:
		index=g.get_player_index(e.peer_id)
		if index>-1:
			if parsed[1]=="back":
				g.players[index].playsound("chest7")
				g.players[index].chest=None
				return
			p=g.players[index]
			if parsed[1]=="put":
				if p.chest is None: return
				if len(list(g.players[index].inv.keys()))<=0: g.n.send_reliable(e.peer_id,"Your inventory is empty",0); g.players[index].prevmenu(); return
				for item in list(g.players[index].inv.keys()):
					if item in g.dontlose: continue
					amount=g.players[index].inv[item]
					if p.chest is not None and item in p.chest.items: p.chest.itemamounts[p.chest.items.index(item)]+=amount
					if p.chest is not None and item not in p.chest.items:
						p.chest.items.append(item)
						p.chest.itemamounts.append(amount)						
					for base in g.group_bases:
						if p.map=="basement"+base.name+base.mapappend: 
							base.chestlog+=p.name+" put "+str(amount)+" "+item+" at "+get_current_date()+"\n"
							
					p.give(item,-amount)
				p.weapon="punch"
				p.weapon2="feet"
				g.n.send_reliable(p.peer_id,"drawsilent punch",0)
				g.n.send_reliable(p.peer_id,"draw2silent feet",0)
				g.players[index].playsound("chest1"); return
			if parsed[1]=="get":
				if p.chest is None: return
				if len(p.chest.items)==0: g.n.send_reliable(e.peer_id,"This chest is empty",0); g.players[index].prevmenu(); return
				while len(p.chest.items)>0:
					amount=p.chest.itemamounts[p.chest.items.index(p.chest.items[0])]
					p.give(p.chest.items[0],amount)
					p.chest.items.remove(p.chest.items[0])
					p.chest.itemamounts.remove(amount)

				g.players[index].playsound("chest2"); return

			try: i=int(parsed[1])
			except: return
			if 1:
				if p.chest is None: return
				if p.chest.taketimer.elapsed<1000 and g.players[index].paid==False: g.players[index].prevmenu(); return
				p.chest.taketimer.restart()
				if "basement" in p.chest.map:
					p.chestitemindex=i
					send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "chest2", "Enter amount")
					return
				try:
					p.chest.items[i]
					p.chest.itemamounts[i]
				except: return
				if p.chest.items[i] in g.invlimits and p.chest.itemamounts[i]+p.get_item_count(p.chest.items[i])>p.get_backpack_level_amount(g.invlimits[p.chest.items[i]]):
					amount=p.get_backpack_level_amount(g.invlimits[p.chest.items[i]])-p.get_item_count(p.chest.items[i])
					if amount<=0: g.n.send_reliable(e.peer_id,"Your inventory cannot hold more of this item",0); g.players[index].prevmenu(); return
					try: g.players[index].itemplay(""+p.chest.items[i]+"")
					except: return
					g.play("chest5",g.players[index].x,g.players[index].y,g.players[index].z,g.players[index].map)
					p.chest.fill=True
					if p.chestpickupnotify==1: g.n.send_reliable(p.peer_id,""+str(amount)+" "+p.chest.items[i]+"",2)
					p.give(p.chest.items[i],amount)
					p.chest.itemamounts[i]-=amount
				else:
					try: g.players[index].itemplay(""+p.chest.items[i]+"")
					except: return
					g.play("chest5",g.players[index].x,g.players[index].y,g.players[index].z,g.players[index].map)
					p.chest.fill=True

					if p.chest.items[i]!="zero_token": p.give(p.chest.items[i],p.chest.itemamounts[i]); p.chestpickupnotify==1 and g.n.send_reliable(p.peer_id,""+str(p.chest.itemamounts[i])+" "+p.chest.items[i]+"",2)

					else:
						if g.players[index].chesttoken>=300: g.n.send_reliable(e.peer_id,"you cannot get more tokens",0); g.players[index].prevmenu(); return
						g.players[index].zhtoken+=p.chest.itemamounts[i]
						if not g.players[index].hidden: g.n.broadcast("congratulations! "+g.players[index].name+" found "+str(p.chest.itemamounts[i])+" zero tokens from the chest!",2)
						g.players[index].chesttoken+=p.chest.itemamounts[i]
						g.n.broadcast("play_s getpoints.ogg",0)
					p.chest.items.pop(i)
					p.chest.itemamounts.pop(i)
				g.players[index].prevmenu()
	elif parsed[0]=="chest2" and len(parsed)>1:
		index=g.get_player_index(e.peer_id)
		if index>-1:
			if parsed[1]=="[cncel]":
				g.players[index].prevmenu()
				return
			p=g.players[index]
			try:
				p.chest
			except:
				 return
			if p.chest is None:  return
			try: i=g.players[index].chestitemindex
			except:  return
			try:
				amount=int(parsed[1])
			except: g.n.send_reliable(e.peer_id,"A number is required",0); g.players[index].prevmenu(); return
			if amount<=0: g.n.send_reliable(e.peer_id,"Amount cannot be less than or equal to 0",0); g.players[index].prevmenu(); return
			try:

				if amount>p.chest.itemamounts[i]: g.n.send_reliable(e.peer_id,"Amount cannot be higher than the item amount in the chest",0); g.players[index].prevmenu(); return
				newamount=g.players[index].get_item_count(p.chest.items[i])+int(parsed[1])
				if p.chest.items[i] in g.invlimits and newamount>p.get_backpack_level_amount(g.invlimits[p.chest.items[i]]): 

					g.n.send_reliable(e.peer_id,"Amount cannot be higher than the amount your inventory can hold of this item",0); g.players[index].prevmenu(); return
			except: return
			try:
				g.players[index].itemplay(""+p.chest.items[i]+"")
				g.play("chest5",g.players[index].x,g.players[index].y,g.players[index].z,g.players[index].map)
				p.chest.fill=True
				p.give(p.chest.items[i],amount)
				for base in g.group_bases:
					if g.players[index].map=="basement"+base.name+base.mapappend: base.chestlog+=g.players[index].name+" got "+str(amount)+" "+p.chest.items[i]+" at "+get_current_date()+"\n"
				p.chest.itemamounts[i]-=amount
				if p.chest.itemamounts[i]<=0:
					p.chest.items.pop(i)
					p.chest.itemamounts.pop(i)
				g.players[index].prevmenu()
			except:  return
	elif parsed[0]=="corpse" and len(parsed)>1:
		index=g.get_player_index(e.peer_id)
		if index>-1:
			if parsed[1]=="back":
				g.players[index].corpse=None
				return
			p=g.players[index]
			try: i=int(parsed[1])
			except: return
			if 1:
				if p.corpse is None: return
#					g.play("corpseitemtake",g.players[index].x,g.players[index].y,g.players[index].z,g.players[index].map)
				try: g.players[index].itemplay(p.corpse.items[i])
				except: return
				if p.corpse.items[i] in g.invlimits and p.corpse.itemamounts[i]+p.get_item_count(p.corpse.items[i])>p.get_backpack_level_amount(g.invlimits[p.corpse.items[i]]):
					amount=p.get_backpack_level_amount(g.invlimits[p.corpse.items[i]])-p.get_item_count(p.corpse.items[i])
					if amount<=0: g.n.send_reliable(e.peer_id,"Your inventory cannot hold more of this item",0); g.players[index].prevmenu(); return
					p.give(p.corpse.items[i],amount)
					p.corpse.itemamounts[i]-=amount
				else:
					p.give(p.corpse.items[i],p.corpse.itemamounts[i])
					p.corpse.items.pop(i)
					p.corpse.itemamounts.pop(i)
				g.players[index].prevmenu()

	elif parsed[0]=="baseopen":
		index=g.get_player_index(e.peer_id)
		if index>-1:
			if parsed[1]=="[cncel]": g.n.send_reliable(e.peer_id,"canceled",0)
			for base in g.group_bases:
				if base.mapappend==g.players[index].basemapappend and base.name==g.players[index].baseact:
					if g.players[index].baseentertimer.elapsed<g.players[index].baseentertime: g.n.send_reliable(e.peer_id,"wait "+str(ms_to_readable_time(g.players[index].baseentertime-g.players[index].baseentertimer.elapsed)),0); return
					g.players[index].baseentertimer.restart()
					g.players[index].baseentertime=0
					if base.password!=parsed[1]:
						g.n.send_reliable(e.peer_id,"wrong password",0)
						grp=get_group(base.name)
						if grp is None: g.players[index].baseentertime=60000; return
						if grp is not None and g.players[index].name not in grp.members: g.players[index].baseentertime=60000
						if grp is not None and g.players[index].name in grp.members: g.players[index].baseentertime=20000
						return
					else:
						g.n.send_reliable(e.peer_id,"stopmoving",0)
						g.players[index].playsound("misc147")
						base.dooropening=True
						name=g.players[index].name
						delay(1000)
						index=get_player_index_from(name)
						g.players[index].playsound("misc18")
						g.players[index].playsound("dooropen4")
						g.play("dooropen4",0,0,0,"basement"+base.name+base.mapappend)
						base.dooron=True
						grp=get_group(base.name)
						if grp is not None: grp.actions+=g.players[index].name+" opened the base door at "+get_current_date()+"\n"
						base.dooropening=False
						base.doorontimer.restart()
						g.n.send_reliable(g.players[index].peer_id,"startmoving",0)
	elif parsed[0]=="basepasswordchange":
		index=g.get_player_index(e.peer_id)
		if index>-1:
			base=get_current_base(g.players[index])
			grp=get_group(base.name)
			if grp is None: return
			if g.players[index].name!=grp.owner and g.players[index].name not in grp.admins: g.n.send_reliable(e.peer_id,"only owner and admins can do this",0); g.players[index].prevmenu(); return
			if len(parsed[1])<6: g.n.send_reliable(e.peer_id,"base password must be higher than or equal to 6 characters",0); g.players[index].prevmenu(); return

			base.password=parsed[1]
			if grp is not None: grp.actions+=g.players[index].name+" changed the base password to "+parsed[1]+" at "+get_current_date()+"\n"
			g.n.send_reliable(e.peer_id,"done",0)
			g.players[index].prevmenu()
	elif parsed[0]=="basecomp":
		index=g.get_player_index(e.peer_id)
		if index>-1:
			base=get_current_base(g.players[index])
			if base is None: return
			if base is not None and parsed[1]=="ammo":
				g.n.send_reliable(e.peer_id,"base gun has "+str(base.ammo)+" ammo",0); g.players[index].prevmenu(); return
			if g.gamestop==0 and base is not None and parsed[1]=="gun":
				if base.ammo<=0: g.n.send_reliable(e.peer_id,"no ammo",0); g.players[index].prevmenu(); return
				if base.firetimer.elapsed>=1000:
					base.firetimer.restart()
					base.ammo-=1
					spawn_weapon(base.x, base.y, base.z, 0, "base_gun", base.map, g.players[index])
					snd="m1garantbattleriflefire"+str(random(1,3))
					g.play(snd,base.x,base.y,base.z,base.map)
					g.n.broadcast("distsound m1garantbattlerifledist "+str(base.x)+" "+str(base.y)+" "+str(base.z)+" "+base.map,0)
					if not g.players[index].hidden: g.n.broadcast("distsound m1garantbattlerifledist "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z)+" "+g.players[index].map,0)
				g.players[index].prevmenu()
			if parsed[1]=="door":
				if 1:
					if base is not None:
						if base.dooropening: g.n.send_reliable(e.peer_id,"door is opening",0); g.players[index].prevmenu(); return
						if base.dooron: g.n.send_reliable(e.peer_id,"door is on",0); g.players[index].prevmenu(); return
						g.players[index].prevmenu()
						name=g.players[index].name
						g.play("misc147",0,0,0,"basement"+base.name+base.mapappend)
						base.dooropening=True

						delay(1000)
						index=get_player_index_from(name)
						g.play("misc18",0,0,0,"basement"+base.name+base.mapappend)
						g.play("dooropen4",0,0,0,"basement"+base.name+base.mapappend)
						g.play("dooropen4",base.x,base.y,base.z,base.map)
						base.dooron=True
						base.dooropening=False
						grp=get_group(g.players[index].group)
						if grp is not None: grp.actions+=g.players[index].name+" opened the base door at "+get_current_date()+"\n"

						base.doorontimer.restart()
			if parsed[1]=="password":
				send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "basepasswordchange", "enter new password")
			if parsed[1]=="near":
				if not base.generator_on or base.generator_fuel <= 0:
					g.n.send_reliable(e.peer_id, "Scanner offline: generator requires fuel and power.", 0)
					g.players[index].prevmenu()
					return
				m=server_menu()
				m.intro="near players"
				m.initial_packet="basenear"
				for p in g.players:
					if not p.invisible and not p.hidden and p.distancecheck(base.x,base.y,base.z)<=100 and p.map==base.map:
						if p.shielded and p.vi==-1: m.add(p.name+", shielded",p.name,False)
						if not p.shielded and p.vi!=-1: m.add(p.name+", in motor",p.name,False)
						if p.shielded and p.vi!=-1: m.add(p.name+", shielded, in motor",p.name,False)
						if not p.shielded and p.vi==-1: m.add(p.name,p.name,False)
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"no near players within 100 steps",0); g.players[index].prevmenu(); return
				m.send(e.peer_id)
			if parsed[1]=="upgrades":
				grp=get_group(base.name)
				if grp is None: return
				if g.players[index].name!=grp.owner and g.players[index].name not in grp.admins:
					g.n.send_reliable(e.peer_id,"only owner and admins can access upgrades",0)
					g.players[index].prevmenu()
					return
				m=server_menu()
				m.intro="Base Upgrades Menu"
				m.initial_packet="baseupgrade"
				wall_names={1:"Wood", 2:"Iron", 3:"Titanium"}
				curr_wall=wall_names.get(base.wall_level, "Unknown")
				m.add("Wall Reinforcement (Current: "+curr_wall+")", "wall")
				gen_status="On" if base.generator_on else "Off"
				m.add("Generator Options (Generator: "+gen_status+", Fuel: "+str(round(base.generator_fuel))+"s)", "generator")
				m.add("Deposit Ammo (Current: "+str(base.ammo)+" rounds)", "ammo")
				m.add("Manage Turrets (Turrets built: "+str(len(base.turrets))+"/3)", "turrets")
				m.send(e.peer_id)
	elif parsed[0]=="baseupgrade":
		index=g.get_player_index(e.peer_id)
		if index>-1:
			base=get_current_base(g.players[index])
			if base is None: return
			grp=get_group(base.name)
			if grp is None: return
			if g.players[index].name!=grp.owner and g.players[index].name not in grp.admins:
				g.n.send_reliable(e.peer_id,"only owner and admins can manage base upgrades",0)
				g.players[index].prevmenu()
				return
			if parsed[1]=="wall":
				m=server_menu()
				m.intro="Wall Upgrades"
				m.initial_packet="base_wall_upgrade"
				if base.wall_level==1:
					m.add("Upgrade to Iron Walls (Costs 1,000 zero tokens) (reduces dmg taken to 70%)", "2")
				elif base.wall_level==2:
					m.add("Upgrade to Titanium Walls (Costs 2,500 zero tokens) (reduces dmg taken to 40%)", "3")
				else:
					m.add("Walls are fully upgraded (Titanium)", "max", False)
				m.send(e.peer_id)
			elif parsed[1]=="generator":
				m=server_menu()
				m.intro="Generator Options (Fuel: "+str(round(base.generator_fuel))+" seconds)"
				m.initial_packet="base_generator"
				gen_action="Turn Off" if base.generator_on else "Turn On"
				m.add(gen_action+" Generator", "toggle")
				m.add("Deposit Fuel (Costs 100 zero tokens for 30 min of fuel)", "deposit")
				m.send(e.peer_id)
			elif parsed[1]=="ammo":
				m=server_menu()
				m.intro="Deposit Ammo (Base Ammo: "+str(base.ammo)+" rounds)"
				m.initial_packet="base_deposit_ammo"
				m.add("Buy 50 rounds of base ammo (Costs 50 zero tokens)", "buy_50")
				m.add("Buy 100 rounds of base ammo (Costs 90 zero tokens)", "buy_100")
				has_any=False
				for a_type in ["5.56x45mm", "7.62x51mm", "7.62x39mm", "12gauge"]:
					amt=g.players[index].get_ammo_count(a_type)
					if amt>0:
						m.add("Deposit "+str(amt)+" rounds of "+a_type, "dep_"+a_type)
						has_any=True
				if not has_any:
					m.add("No physical ammo in your inventory to deposit", "no_phys", False)
				m.send(e.peer_id)
			elif parsed[1]=="turrets":
				m=server_menu()
				m.intro="Turret Management"
				m.initial_packet="base_turret_manage"
				m.add("Buy/Build Turret (Costs 500 zero tokens, Max 3)", "buy")
				if len(base.turrets)>0:
					m.add("Upgrade Turret Weapon", "upgrade")
					m.add("Deconstruct Turret (Get 200 zero tokens back)", "deconstruct")
				else:
					m.add("No turrets built yet", "none", False)
				m.send(e.peer_id)

	elif parsed[0]=="base_wall_upgrade":
		index=g.get_player_index(e.peer_id)
		if index>-1:
			base=get_current_base(g.players[index])
			if base is None: return
			if parsed[1]=="2":
				if g.players[index].zhtoken<1000:
					g.n.send_reliable(e.peer_id,"You do not have enough zero tokens.",0)
				else:
					g.players[index].zhtoken-=1000
					base.wall_level=2
					g.n.send_reliable(e.peer_id,"Walls upgraded to Iron! Platforms refreshed.",0)
					g.play("misc147", base.x, base.y, base.z, base.map)
					for p in g.players:
						if p.map==base.map:
							base.remove_platform_to(p)
							base.send_platform_to(p)
			elif parsed[1]=="3":
				if g.players[index].zhtoken<2500:
					g.n.send_reliable(e.peer_id,"You do not have enough zero tokens.",0)
				else:
					g.players[index].zhtoken-=2500
					base.wall_level=3
					g.n.send_reliable(e.peer_id,"Walls upgraded to Titanium! Platforms refreshed.",0)
					g.play("misc147", base.x, base.y, base.z, base.map)
					for p in g.players:
						if p.map==base.map:
							base.remove_platform_to(p)
							base.send_platform_to(p)
			g.players[index].prevmenu()

	elif parsed[0]=="base_generator":
		index=g.get_player_index(e.peer_id)
		if index>-1:
			base=get_current_base(g.players[index])
			if base is None: return
			if parsed[1]=="toggle":
				if base.generator_on:
					base.generator_on=False
					g.play("motorstop", base.x, base.y, base.z, base.map)
					g.play("motorstop", 30, 30, 0, "basement"+base.name+base.mapappend)
					g.n.send_reliable(e.peer_id,"Generator turned off.",0)
				else:
					if base.generator_fuel<=0:
						g.n.send_reliable(e.peer_id,"Cannot turn on generator: out of fuel.",0)
					else:
						base.generator_on=True
						base.generator_timer.restart()
						g.play("motorstart", base.x, base.y, base.z, base.map)
						g.play("motorstart", 30, 30, 0, "basement"+base.name+base.mapappend)
						g.n.send_reliable(e.peer_id,"Generator turned on.",0)
			elif parsed[1]=="deposit":
				if g.players[index].zhtoken<100:
					g.n.send_reliable(e.peer_id,"You do not have enough zero tokens.",0)
				else:
					g.players[index].zhtoken-=100
					base.generator_fuel+=1800.0
					g.n.send_reliable(e.peer_id,"Deposited 30 minutes of fuel.",0)
					g.play("getcola2", 30, 30, 0, "basement"+base.name+base.mapappend)
			g.players[index].prevmenu()

	elif parsed[0]=="base_deposit_ammo":
		index=g.get_player_index(e.peer_id)
		if index>-1:
			base=get_current_base(g.players[index])
			if base is None: return
			if parsed[1]=="buy_50":
				if g.players[index].zhtoken<50:
					g.n.send_reliable(e.peer_id,"You do not have enough zero tokens.",0)
				else:
					g.players[index].zhtoken-=50
					base.ammo+=50
					g.n.send_reliable(e.peer_id,"Purchased 50 base ammo rounds.",0)
					g.play("ammo_crate", 30, 30, 0, "basement"+base.name+base.mapappend)
			elif parsed[1]=="buy_100":
				if g.players[index].zhtoken<90:
					g.n.send_reliable(e.peer_id,"You do not have enough zero tokens.",0)
				else:
					g.players[index].zhtoken-=90
					base.ammo+=100
					g.n.send_reliable(e.peer_id,"Purchased 100 base ammo rounds.",0)
					g.play("ammo_crate", 30, 30, 0, "basement"+base.name+base.mapappend)
			elif parsed[1].startswith("dep_"):
				ammo_type=parsed[1].replace("dep_", "")
				amt=g.players[index].get_ammo_count(ammo_type)
				if amt>0:
					g.players[index].ammogive(ammo_type, -amt)
					base.ammo+=amt
					g.n.send_reliable(e.peer_id,"Deposited "+str(amt)+" rounds of "+ammo_type+".",0)
					g.play("ammo_crate", 30, 30, 0, "basement"+base.name+base.mapappend)
				else:
					g.n.send_reliable(e.peer_id,"You do not have that ammo.",0)
			g.players[index].prevmenu()

	elif parsed[0]=="base_turret_manage":
		index=g.get_player_index(e.peer_id)
		if index>-1:
			base=get_current_base(g.players[index])
			if base is None: return
			if parsed[1]=="buy":
				if len(base.turrets)>=3:
					g.n.send_reliable(e.peer_id,"You have reached the limit of 3 turrets.",0)
					g.players[index].prevmenu()
					return
				if g.players[index].zhtoken<500:
					g.n.send_reliable(e.peer_id,"You do not have enough zero tokens (500 needed).",0)
					g.players[index].prevmenu()
					return
				send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "base_buy_turret", "Enter placement coordinates on outer map near base ("+str(round(base.x))+", "+str(round(base.y))+"). Format: x,y")
			elif parsed[1]=="upgrade":
				m=server_menu()
				m.intro="Select Turret to Upgrade"
				m.initial_packet="base_select_turret"
				for i, t in enumerate(base.turrets):
					w_names={"base_gun":"Rifle Sentry", "m4":"Machine Gun", "dragunov_psl":"Sniper", "maverick88":"Shotgun"}
					curr_w=w_names.get(t.weapon_type, t.weapon_type)
					m.add("Turret #"+str(i+1)+" at ("+str(round(t.x))+", "+str(round(t.y))+") - Weapon: "+curr_w, str(i))
				m.send(e.peer_id)
			elif parsed[1]=="deconstruct":
				m=server_menu()
				m.intro="Select Turret to Deconstruct"
				m.initial_packet="base_deconstruct_turret"
				for i, t in enumerate(base.turrets):
					w_names={"base_gun":"Rifle Sentry", "m4":"Machine Gun", "dragunov_psl":"Sniper", "maverick88":"Shotgun"}
					curr_w=w_names.get(t.weapon_type, t.weapon_type)
					m.add("Deconstruct Turret #"+str(i+1)+" at ("+str(round(t.x))+", "+str(round(t.y))+") - Weapon: "+curr_w, str(i))
				m.send(e.peer_id)

	elif parsed[0]=="base_buy_turret":
		index=g.get_player_index(e.peer_id)
		if index>-1:
			base=get_current_base(g.players[index])
			if base is None: return
			try:
				parts=parsed[1].split(",")
				tx=float(parts[0])
				ty=float(parts[1])
			except Exception:
				g.n.send_reliable(e.peer_id,"Invalid coordinate format. Use x,y (e.g. 500,450).",0)
				g.players[index].prevmenu()
				return
			if abs(tx - base.x)>30 or abs(ty - base.y)>30:
				g.n.send_reliable(e.peer_id,"Placement is too far from base entrance. Must be within 30 steps.",0)
				g.players[index].prevmenu()
				return
			if g.players[index].zhtoken<500:
				g.n.send_reliable(e.peer_id,"You do not have enough zero tokens.",0)
				g.players[index].prevmenu()
				return
			g.players[index].zhtoken-=500
			from base import base_turret
			new_t=base_turret(tx, ty, base.z, base.map, base.name)
			base.turrets.append(new_t)
			g.play("misc147", base.x, base.y, base.z, base.map)
			for p in g.players:
				if p.map==base.map:
					base.remove_turrets_from(p)
					base.send_turrets_to(p)
			g.n.send_reliable(e.peer_id,"Turret built successfully at "+str(round(tx))+", "+str(round(ty))+"!",0)
			g.players[index].prevmenu()

	elif parsed[0]=="base_select_turret":
		index=g.get_player_index(e.peer_id)
		if index>-1:
			base=get_current_base(g.players[index])
			if base is None: return
			try: idx=int(parsed[1])
			except: return
			g.players[index].selected_turret_idx=idx
			m=server_menu()
			m.intro="Select Weapon Upgrade"
			m.initial_packet="base_select_weapon"
			m.add("Rifle Sentry (base_gun, free)", "base_gun")
			m.add("Machine Gun (m4, Costs 800 zero tokens)", "m4")
			m.add("Sniper Turret (dragunov_psl, Costs 1,200 zero tokens)", "dragunov_psl")
			m.add("Shotgun Turret (maverick88, Costs 1,000 zero tokens)", "maverick88")
			m.send(e.peer_id)

	elif parsed[0]=="base_select_weapon":
		index=g.get_player_index(e.peer_id)
		if index>-1:
			base=get_current_base(g.players[index])
			if base is None: return
			t_idx=getattr(g.players[index], "selected_turret_idx", None)
			if t_idx is None or t_idx>=len(base.turrets):
				g.n.send_reliable(e.peer_id,"No turret selected.",0)
				g.players[index].prevmenu()
				return
			turret=base.turrets[t_idx]
			weapon_type=parsed[1]
			weapon_costs={"base_gun":0, "m4":800, "dragunov_psl":1200, "maverick88":1000}
			cost=weapon_costs.get(weapon_type, 0)
			if g.players[index].zhtoken<cost:
				g.n.send_reliable(e.peer_id,"You do not have enough zero tokens ("+str(cost)+" needed).",0)
			else:
				g.players[index].zhtoken-=cost
				turret.weapon_type=weapon_type
				g.n.send_reliable(e.peer_id,"Turret #"+str(t_idx+1)+" weapon upgraded to "+weapon_type+"!",0)
				g.play("misc147", base.x, base.y, base.z, base.map)
			g.players[index].prevmenu()

	elif parsed[0]=="base_deconstruct_turret":
		index=g.get_player_index(e.peer_id)
		if index>-1:
			base=get_current_base(g.players[index])
			if base is None: return
			try: t_idx=int(parsed[1])
			except: return
			if t_idx>=len(base.turrets):
				g.n.send_reliable(e.peer_id,"Invalid turret choice.",0)
				g.players[index].prevmenu()
				return
			t=base.turrets[t_idx]
			if t.operator is not None:
				from base import dismount_turret
				dismount_turret(t.operator)
			for p in g.players:
				if p.map==base.map:
					remove_platform(p, t.x, t.x, t.y, t.y, t.z, t.z, "metal")
					remove_zone(p, t.x, t.x, t.y, t.y, t.z, t.z, "turret_of_group_base_"+base.name)
			base.turrets.pop(t_idx)
			g.players[index].zhtoken+=200
			g.n.send_reliable(e.peer_id,"Turret deconstructed. 200 zero tokens refunded.",0)
			g.play("misc18", base.x, base.y, base.z, base.map)
			g.players[index].prevmenu()
	elif parsed[0]=="corpseselect":
		index=g.get_player_index(e.peer_id)
		if index>-1:
			if parsed[1]=="back": return
			try: ch=g.corpses[int(parsed[1])]
			except: return
			if 1:
				if 1:
					m=server_menu()
					m.initial_packet="corpse"
					m.intro="corpse with "+str(len(ch.items))+" items. Use up and down keys to move between items, enter key to pick it up, escape key to close the corpse."
					corpseadd(g.players[index],ch,m)
					g.players[index].playsound("corpsemisc1")
					if len(m.menuids)<=0:
						m.add("No items","no",False)
					if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"no items",0); return
					else: m.send(e.peer_id); return



	return True
