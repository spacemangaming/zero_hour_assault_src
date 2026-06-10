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
from zh_net_data_editor import handle_data_editor

def handle_gameplay_2(e, parsed, index):
	global languages

	# --- Data editor (admin/dev only) ---
	if len(parsed) > 0 and parsed[0].startswith("de_"):
		if handle_data_editor(e, parsed, index):
			return True

	cmds = {"ammocheck", "communityrequest2", "changestatus", "eml", "rename2", "addfriend", "friendstats", "createvote2", "communityrequest", "staffmenu", "communityinfoselect", "removefriend", "addfriendchoose", "groupmakeadmin", "serverstatus", "tokentransfer", "groupinvite", "groupremoveadmin", "confirmdelete", "confirmpasswdcode", "vote2", "cinvitation2", "createvote", "communitymakeowner", "ticketviewchoose", "groupdonate2", "addfriend3", "ticket_create_department", "bus_board", "addfriendchoose2", "groupinfoselect", "communitykick", "eml2", "serverviewchoose", "invitation", "handselect", "lchannelset", "addfriendchoose3", "grouprequest", "groupmakeowner", "cinvitation", "group2", "editmap", "grouprename", "communityinfoselect2", "communityremoveadmin", "compid", "serverviewcategory", "langoption", "groupinfoselect2", "groupannounce", "sitstop", "invitation2", "adminlog", "communityinvite", "addfriend2", "communityannounce", "eventschoose", "eml3", "sitstart", "grouprequest2", "groupinvite2", "ticket2", "ammocheck2", "friend2", "addfriend4", "communityrename", "changepasswd", "communitycreate", "securitychoose", "gamemenuopt", "groupcreate", "char", "communitymakeadmin", "groupkick", "groupdonate", "communityinvite2", "notifys", "community2"}
	subs = {}
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

	if parsed[0]=="ticket_create_department": # Department chosen, finalize ticket (NEW FLOW)
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": g.players[index].prevmenu(); return
			
			title = g.players[index].ticket_selected_id
			message = g.players[index].ticket_selected_department # This is actually the message
			department = " ".join(parsed[1:])

			if file_exists("chars/"+g.players[index].name+"/rateneeded.usr"): g.n.send_reliable(e.peer_id,"you cannot create a new ticket without rating your last closed ticket",0); g.players[index].prevmenu(); return
			found_tickets=0
			for ticket_obj in g.tickets:
				if not ticket_obj["closed"] and ticket_obj["owner"]==g.players[index].name:
					found_tickets+=1
			if found_tickets>=5: g.n.send_reliable(e.peer_id,"You can't have more than 5 open tickets",0); g.players[index].prevmenu(); return
			
			full_title = f"#{len(g.tickets)+1} {title}"
			g.tickets.append({"title": full_title, "closetimer": timer(), 
							  "messages": f"{full_title}\ndepartment\n{department}\n{g.players[index].name}, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{message}",
							  "department": department, "closed": False, "pending": False, 
							  "owner": g.players[index].name, "id": f"#{len(g.tickets)+1}",
							  "lastupdate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
							  "createdate": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
			g.n.send_reliable(g.players[index].peer_id,"play_s misc216.ogg",0)
			g.n.send_reliable(e.peer_id,f"Done, ticket has been created with id: #{len(g.tickets)}",0)
			adminsend(f"The {full_title} ticket was created by {g.players[index].name}: "+message+"")
			notify_admins(f"zero hour assault, The {full_title} ticket was created by {g.players[index].name}: "+message+"")
			save_tickets()
			g.players[index].ticket_selected_id = "" # Clear temporary storage
			g.players[index].ticket_selected_department = ""


	if parsed[0]=="ticketviewchoose":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
		ticket=find_ticket_by_id(parsed[1])
		if ticket is None:
			g.n.send_reliable(e.peer_id,"Error, ticket not found!",0); return
		if not g.players[index].android and not g.players[index].ios: g.n.send_reliable(e.peer_id,"viewticket{}[]"+ticket["title"]+"{}[]"+ticket["messages"]+"{}[]"+str(ticket["closed"])+"{}[]"+str(ticket["pending"]),4)
		else: g.n.send_reliable(e.peer_id,"echo ticketview_select_action "+ticket["id"],0)
	if parsed[0]=="serverviewchoose":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
		ticket=find_ticket_by_id(parsed[1])
		if ticket is None:
			g.n.send_reliable(e.peer_id,"Error, ticket not found!",0); return
		if not g.players[index].android and not g.players[index].ios: g.n.send_reliable(e.peer_id,"viewticket2{}[]"+ticket["title"]+"{}[]"+ticket["messages"]+"{}[]"+str(ticket["closed"])+"{}[]"+str(ticket["pending"]),4)
		else: g.n.send_reliable(e.peer_id,"echo admin_ticket_action_menu "+ticket["id"],0)
	if parsed[0]=="invitation2":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			if parsed[1]=="decline":
				g.n.send_reliable(e.peer_id,"You declined the invitation",0)
				try: g.players[index].groupinvitations.remove(g.players[index].groupact)
				except: pass
			if parsed[1]=="accept":
				if g.players[index].group!="": g.n.send_reliable(e.peer_id,"You are in already a group",0); g.players[index].prevmenu(); return
				grp=get_group(g.players[index].groupact)
				if grp is None: return
				if grp.name not in g.players[index].groupinvitations: g.n.send_reliable(e.peer_id,"invitation not found",0); g.players[index].prevmenu(); return
				if grp is None:
					g.n.send_reliable(e.peer_id,"Group not found",0); return
				if len(grp.members)>=15: g.n.send_reliable(e.peer_id,"More than 15 members cannot join to group.",0); return

				else: 					g.n.send_reliable(e.peer_id,"You accepted the invitation",0)
				for m in grp.members:
					ind=get_player_index_from(m)
					if ind>-1:
						g.n.send_reliable(g.players[ind].peer_id,"groupnotification "+g.players[index].name+" joined to this group!",0)
						g.n.send_reliable(g.players[ind].peer_id,"play_s misc219.ogg",0)
				grp.members.append(g.players[index].name)
				grp.actions+=g.players[index].name+" joined at "+get_current_date()+"\n"
				try: g.players[index].groupinvitations.remove(grp.name)
				except: pass
	if parsed[0]=="invitation":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			m=server_menu()
			g.players[index].groupact=parsed[1]
			m.initial_packet="invitation2"
			m.intro="Select what would you like to do."
			m.add("accept","accept")
			m.add("decline","decline")
			m.send(e.peer_id)
	if parsed[0]=="grouprequest2":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			grp=get_group(g.players[index].group)
			if parsed[1]=="decline":
				g.n.send_reliable(e.peer_id,"You declined the request",0)
				ind=get_player_index_from(g.players[index].grouprequest)
				if ind>-1:
					g.n.send_reliable(g.players[ind].peer_id,"groupnotification "+g.players[index].name+" declined your group join request!",0)
					g.n.send_reliable(g.players[ind].peer_id,"play_s misc218.ogg",0)
				try: grp.join_requests.remove(g.players[index].grouprequest)
				except: pass
			if parsed[1]=="accept":
				ind=get_player_index_from(g.players[index].grouprequest)
				if ind>-1 and g.players[ind].group!="": g.n.send_reliable(e.peer_id,"This player is already in a group",0); g.players[index].prevmenu(); return
				for group in g.groups:
					for member in group.members:
						if member==g.players[index].grouprequest: g.n.send_reliable(e.peer_id,"This player is already in a group",0); g.players[index].prevmenu(); return
				if len(grp.members)>=15: g.n.send_reliable(e.peer_id,"More than 15 members cannot join to group.",0); return

				g.n.send_reliable(e.peer_id,"You accepted the request",0)
				for m in grp.members:
					ind=get_player_index_from(m)
					if ind>-1:
						g.n.send_reliable(g.players[ind].peer_id,"groupnotification "+g.players[index].grouprequest+" joined to this group!",0)
						g.n.send_reliable(g.players[ind].peer_id,"play_s misc219.ogg",0)
				grp.members.append(g.players[index].grouprequest)
				grp.actions+=g.players[index].grouprequest+" joined at "+get_current_date()+"\n"
				try: grp.join_requests.remove(g.players[index].grouprequest)
				except: pass
				ind=get_player_index_from(g.players[index].grouprequest)
				if ind>-1:
					g.n.send_reliable(g.players[ind].peer_id,"groupnotification "+g.players[index].name+" accepted your group join request!",0)
					g.n.send_reliable(g.players[ind].peer_id,"play_s misc222.ogg",0)

	if parsed[0]=="grouprequest":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			m=server_menu()
			m.initial_packet="grouprequest2"
			m.intro="Select what would you like to do."
			g.players[index].grouprequest=parsed[1]
			m.add("accept","accept")
			m.add("decline","decline")
			m.send(e.peer_id)

	if parsed[0]=="groupcreate":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			if " " in parsed[1] or not parsed[1].isascii(): g.n.send_reliable(e.peer_id,"invalid input",0); return
			if g.players[index].zhtoken<1000:
				g.n.send_reliable(g.players[index].peer_id,"You need 1000 tokens to create a group.",0)
				return
			if g.players[index].map!="massacre_in_the_city":
				g.n.send_reliable(g.players[index].peer_id,"You need to be on the free fight mode map to create a group.",0)
				return
			if get_group(parsed[1]) is not None: g.n.send_reliable(e.peer_id,"A group with this name already exists.",0); return
			if 1:
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
			gpt2=get_tile_at(mx+1,my,g.players[index].z,g.players[index].map)
			gpt3=get_tile_at(mx-1,my,g.players[index].z,g.players[index].map)
			gpt4=get_tile_at(mx+1,my+1,g.players[index].z,g.players[index].map)
			gpt5=get_tile_at(mx-1,my+1,g.players[index].z,g.players[index].map)
			gpt6=get_tile_at(mx+1,my-1,g.players[index].z,g.players[index].map)
			gpt7=get_tile_at(mx-1,my-1,g.players[index].z,g.players[index].map)

			if g.players[index].map!="massacre_in_the_city": g.n.send_reliable(e.peer_id,"You can only create group in freedom fight map",0); return
			max=get_max_values(g.players[index].map)
			mx=round(mx)
			my=round(my)
			if "wall" in gpt6 or "wall" in gpt7 or "wall" in gpt2 or "wall" in gpt3 or "wall" in gpt4 or "wall" in gpt5 or chest_at(mx,my,g.players[index].z,g.players[index].map) or corpse_at(mx,my,g.players[index].z,g.players[index].map) or mx>max.x or my>max.y or mx<0 or my<0 or gpt=="" or gpt=="air" or gpt.startswith("wall"): g.n.send_reliable(e.peer_id,"You can't create group here",0); return
			for base in g.group_bases:
				if base.map==g.players[index].map and g.players[index].distancecheck(base.x,base.y,base.z)<=20: g.n.send_reliable(e.peer_id,"you can't create group base here",0); g.players[index].prevmenu(); return
			g.players[index].zhtoken-=1000
			create_group(parsed[1],g.players[index].name)
			create_group_base(mx,my,mz,g.players[index].map,parsed[1],g.players[index].name)
			if not g.players[index].hidden: g.n.broadcast("groupnotification the "+parsed[1]+" group was created by "+g.players[index].name+"!",0)
			g.n.broadcast("play_s misc234.ogg",0)
			data=file_get_contents("maps/basement.map")
			data=data.replace("mapname:basement","mapname:basement"+parsed[1])
			file_put_contents("maps/basement"+parsed[1]+".map",data)

			group_baseloop()
			base=g.group_bases[len(g.group_bases)-1]
			for pl in g.players:
				if pl.map==base.map: base.send_platform_to(pl)
			g.n.send_reliable(e.peer_id,"your base password is: "+base.password,2)
			spawn_chest(20,25,0,"basement"+parsed[1]+base.mapappend)
	if parsed[0]=="cinvitation2":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			if parsed[1]=="decline":
				g.n.send_reliable(e.peer_id,"You declined the invitation",0)
				try: g.players[index].communityinvitations.remove(g.players[index].communityact)
				except: pass
			if parsed[1]=="accept":
				if g.players[index].community!="": g.n.send_reliable(e.peer_id,"You are in already a community",0); g.players[index].prevmenu(); return
				grp=get_community(g.players[index].communityact)
				if grp is None: return
				if grp.name not in g.players[index].communityinvitations: g.n.send_reliable(e.peer_id,"invitation not found",0); g.players[index].prevmenu(); return
				if grp is None:
					g.n.send_reliable(e.peer_id,"community not found",0); return
				if len(grp.members)>=50: g.n.send_reliable(e.peer_id,"More than 15 members cannot join to community.",0); return

				else: 					g.n.send_reliable(e.peer_id,"You accepted the invitation",0)
				for m in grp.members:
					ind=get_player_index_from(m)
					if ind>-1:
						g.n.send_reliable(g.players[ind].peer_id,"communitynotification "+g.players[index].name+" joined to this community!",0)
						g.n.send_reliable(g.players[ind].peer_id,"play_s misc219.ogg",0)
				grp.members.append(g.players[index].name)
				grp.actions+=g.players[index].name+" joined at "+get_current_date()+"\n"
				try: g.players[index].communityinvitations.remove(grp.name)
				except: pass
	if parsed[0]=="cinvitation":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			m=server_menu()
			g.players[index].communityact=parsed[1]
			m.initial_packet="cinvitation2"
			m.intro="Select what would you like to do."
			m.add("accept","accept")
			m.add("decline","decline")
			m.send(e.peer_id)
	if parsed[0]=="communityrequest2":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			grp=get_community(g.players[index].community)
			if parsed[1]=="decline":
				g.n.send_reliable(e.peer_id,"You declined the request",0)
				ind=get_player_index_from(g.players[index].communityrequest)
				if ind>-1:
					g.n.send_reliable(g.players[ind].peer_id,"communitynotification "+g.players[index].name+" declined your community join request!",0)
					g.n.send_reliable(g.players[ind].peer_id,"play_s misc218.ogg",0)
				try: grp.join_requests.remove(g.players[index].communityrequest)
				except: pass
			if parsed[1]=="accept":
				ind=get_player_index_from(g.players[index].communityrequest)
				if ind>-1 and g.players[ind].community!="": g.n.send_reliable(e.peer_id,"This player is already in a community",0); g.players[index].prevmenu(); return
				for community in g.communitys:
					for member in community.members:
						if member==g.players[index].communityrequest: g.n.send_reliable(e.peer_id,"This player is already in a community",0); g.players[index].prevmenu(); return
				if len(grp.members)>=50: g.n.send_reliable(e.peer_id,"More than 15 members cannot join to community.",0); return

				g.n.send_reliable(e.peer_id,"You accepted the request",0)
				for m in grp.members:
					ind=get_player_index_from(m)
					if ind>-1:
						g.n.send_reliable(g.players[ind].peer_id,"communitynotification "+g.players[index].communityrequest+" joined to this community!",0)
						g.n.send_reliable(g.players[ind].peer_id,"play_s misc219.ogg",0)
				grp.members.append(g.players[index].communityrequest)
				grp.actions+=g.players[index].communityrequest+" joined at "+get_current_date()+"\n"
				try: grp.join_requests.remove(g.players[index].communityrequest)
				except: pass
				ind=get_player_index_from(g.players[index].communityrequest)
				if ind>-1:
					g.n.send_reliable(g.players[ind].peer_id,"communitynotification "+g.players[index].name+" accepted your community join request!",0)
					g.n.send_reliable(g.players[ind].peer_id,"play_s misc222.ogg",0)

	if parsed[0]=="communityrequest":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			m=server_menu()
			m.initial_packet="communityrequest2"
			m.intro="Select what would you like to do."
			g.players[index].communityrequest=parsed[1]
			m.add("accept","accept")
			m.add("decline","decline")
			m.send(e.peer_id)

	if parsed[0]=="communitycreate":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			if " " in parsed[1] or not parsed[1].isascii(): g.n.send_reliable(e.peer_id,"invalid input",0); return
			if not parsed[1].isascii(): g.n.send_reliable(e.peer_id,"invalid input",0); return
			if not g.players[index].paid and g.players[index].zhtoken<1000:
				g.n.send_reliable(g.players[index].peer_id,"Free accounts need 1000 tokens to create a community.",0)
				return
			if get_community(parsed[1]) is not None: g.n.send_reliable(e.peer_id,"A community with this name already exists.",0); return
			if not g.players[index].paid: g.players[index].zhtoken-=100
			create_community(parsed[1],g.players[index].name)
			if not g.players[index].hidden: g.n.broadcast("communitynotification the "+parsed[1]+" community was created by "+g.players[index].name+"!",0)
			g.n.broadcast("play_s misc234.ogg",0)

	if parsed[0]=="tokentransfer":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="[cncel]": return
			try:
				amount=int(parsed[1])
			except: g.n.send_reliable(e.peer_id,"You need to enter a valid number",0); return
			if amount<=0: g.n.send_reliable(e.peer_id,"You need to enter a number larger than 0",0); g.players[index].prevmenu(); return
			if g.players[index].zhtoken<amount: g.n.send_reliable(e.peer_id,"You don't have this many tokens!",0); g.players[index].prevmenu(); return
			ind=get_player_index_from(g.players[index].playeract)
			if ind==-1: g.n.send_reliable(e.peer_id,"Player not found",0); return
			if g.players[index].name==g.players[ind].name:
				g.n.send_reliable(g.players[index].peer_id,"you can not transfer token to yourself",2)
				g.players[index].prevmenu()
				return
			if g.players[ind].tokentransfer==0: g.n.send_reliable(e.peer_id,"this player disabled receiving token transfers",0); g.players[index].prevmenu(); return
			g.n.send_reliable(e.peer_id,"You transfered "+str(amount)+" zero tokens to "+g.players[index].playeract,2)
			g.players[index].playsound("getpoint")
			g.players[ind].playsound("getpoint")
			g.n.send_reliable(g.players[ind].peer_id,g.players[index].name+" has transfered you "+str(amount)+" zero tokens.",2)
			g.players[ind].zhtoken+=amount
			g.players[index].zhtoken-=amount
			g.players[index].prevmenu()
	if parsed[0]=="grouprename":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			if g.players[index].zhtoken<200: g.n.send_reliable(e.peer_id,"you need 200 zero tokens for doing this",0); return
			
			# Capture old group name before processing
			old_group_name = g.players[index].group
			new_group_name = parsed[1]

			g.players[index].zhtoken-=200
			for grp in g.groups:
				if grp.name==parsed[1]: g.n.send_reliable(e.peer_id,"This group exists",0); g.players[index].prevmenu(); return
			
			rename_group(g.players[index].group,parsed[1])
			
			for base in g.group_bases:
				if base.name==old_group_name: # Changed to check against old_group_name variable for safety
					if file_exists("maps/basement"+old_group_name+base.mapappend+".map"):
						try: os.rename("maps/basement"+old_group_name+base.mapappend+".map","maps/basement"+parsed[1]+base.mapappend+".map")
						except: pass
					for chest in g.chests:
						if chest.map=="basement"+old_group_name+base.mapappend: chest.map="basement"+parsed[1]+base.mapappend
			
			for base in g.group_bases:
				if base.name==old_group_name:
					data=file_get_contents("maps/basement"+parsed[1]+base.mapappend+".map")
					data=data.replace("mapname:basement"+old_group_name+base.mapappend,"mapname:basement"+parsed[1]+base.mapappend)
					file_put_contents("maps/basement"+parsed[1]+base.mapappend+".map",data)
					init_mapsystem()
					base.name=parsed[1]

			# --- START OF NEW CODE ---
			# Move players and update offline files
			grp = get_group(parsed[1])
			if grp:
				for member in grp.members:
					member_index = get_player_index_from(member)
					
					# Check all bases associated with this group to handle map names correctly
					for base in g.group_bases:
						if base.name == parsed[1]:
							old_map_name = "basement" + old_group_name + base.mapappend
							new_map_name = "basement" + parsed[1] + base.mapappend

							# 1. Handle Online Players
							if member_index > -1:
								p_obj = g.players[member_index]
								if p_obj.map == old_map_name:
									move_player(member_index, p_obj.x, p_obj.y, p_obj.z, new_map_name)
									g.n.send_reliable(p_obj.peer_id, "The group base has been renamed. You have been moved to the new map.", 2)
							
							# 2. Handle Offline Players
							else:
								member_map_file = "chars/" + member + "/map.usr"
								if file_exists(member_map_file):
									saved_map = file_get_contents(member_map_file)
									# If the offline player was saved in the old map, update it
									if saved_map == old_map_name:
										file_put_contents(member_map_file, new_map_name)
			# --- END OF NEW CODE ---

			grp=get_group(parsed[1])
			grp.actions+=g.players[index].name+" renamed the group to "+parsed[1]+" at "+get_current_date()+"\n"
			grp.send("groupnotification the group name was changed to "+parsed[1]+" by "+g.players[index].name+"!",0)
			g.n.broadcast("play_s misc231.ogg",0)
			g.players[index].prevmenu()
	if parsed[0]=="groupmakeowner":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			try: get_group(g.players[index].group).owner=parsed[1]
			except: pass
			grp=get_group(g.players[index].group)
			try: grp.send("groupnotification the group owner was changed to "+parsed[1]+" by "+g.players[index].name+"!",0)
			except: pass
			try: grp.actions+=g.players[index].name+" changed the owner to "+parsed[1]+" at "+get_current_date()+"\n"
			except: pass
			try: grp.send("play_s misc228.ogg",0)
			except: pass
#				g.n.broadcast("play_s misc232.ogg",0)
			g.players[index].prevmenu()

	if parsed[0]=="groupkick":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			grp=get_group(g.players[index].group)
			grp.send("play_s misc228.ogg",0)
			grp.send("groupnotification "+parsed[1]+" has been kicked from this group by "+g.players[index].name+"!",0)
			grp.actions+=g.players[index].name+" kicked "+parsed[1]+" at "+get_current_date()+"\n"
			try: grp.members.remove(parsed[1])
			except: g.n.send_reliable(e.peer_id,"This player is not in the group",0); g.players[index].prevmenu(); return
			g.n.send_reliable(e.peer_id,"Success",0)
			g.players[index].prevmenu()
	if parsed[0]=="groupmakeadmin":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			grp=get_group(g.players[index].group)
			grp.send("play_s misc226.ogg",0)
			grp.send("groupnotification "+parsed[1]+" is now an admin of this group!",0)
			grp.actions+=g.players[index].name+" made "+parsed[1]+" an admin at "+get_current_date()+"\n"
			grp.admins.append(parsed[1])
			g.n.send_reliable(e.peer_id,"Success",0)
			g.players[index].prevmenu()
	if parsed[0]=="groupremoveadmin":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			grp=get_group(g.players[index].group)
			grp.send("play_s misc227.ogg",0)
			grp.send("groupnotification "+parsed[1]+" is no longer an admin of this group!",0)
			grp.actions+=g.players[index].name+" removed "+parsed[1]+"'s admin role at "+get_current_date()+"\n"
			try: grp.admins.remove(parsed[1])
			except: pass
			g.n.send_reliable(e.peer_id,"Success",0)
			g.players[index].prevmenu()
	if parsed[0]=="communityrename":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			if g.players[index].zhtoken<200: g.n.send_reliable(e.peer_id,"you need 200 zero tokens for doing this",0); return
			g.players[index].zhtoken-=200
			for grp in g.communitys:
				if grp.name==parsed[1]: g.n.send_reliable(e.peer_id,"This community exists",0); g.players[index].prevmenu(); return
			rename_community(g.players[index].community,parsed[1])
			grp=get_community(parsed[1])
			grp.actions+=g.players[index].name+" renamed the community to "+parsed[1]+" at "+get_current_date()+"\n"
			grp.send("communitynotification the community name was changed to "+parsed[1]+" by "+g.players[index].name+"!",0)
			g.n.broadcast("play_s misc231.ogg",0)
			g.players[index].prevmenu()
	if parsed[0]=="communitymakeowner":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			get_community(g.players[index].community).owner=parsed[1]
			grp=get_community(g.players[index].community)
			grp.send("communitynotification the community owner was changed to "+parsed[1]+" by "+g.players[index].name+"!",0)
			grp.actions+=g.players[index].name+" changed the owner to "+parsed[1]+" at "+get_current_date()+"\n"
			grp.send("play_s misc232.ogg",0)
			g.players[index].prevmenu()

	if parsed[0]=="communitykick":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			grp=get_community(g.players[index].community)
			grp.send("play_s misc228.ogg",0)
			grp.send("communitynotification "+parsed[1]+" has been kicked from this community by "+g.players[index].name+"!",0)
			grp.actions+=g.players[index].name+" kicked "+parsed[1]+" at "+get_current_date()+"\n"
			try: grp.members.remove(parsed[1])
			except: g.n.send_reliable(e.peer_id,"This player is not in the community",0); g.players[index].prevmenu(); return
			g.n.send_reliable(e.peer_id,"Success",0)
			g.players[index].prevmenu()
	if parsed[0]=="communitymakeadmin":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			grp=get_community(g.players[index].community)
			grp.send("play_s misc226.ogg",0)
			grp.send("communitynotification "+parsed[1]+" is now an admin of this community!",0)
			grp.actions+=g.players[index].name+" made "+parsed[1]+" an admin at "+get_current_date()+"\n"
			grp.admins.append(parsed[1])
			g.n.send_reliable(e.peer_id,"Success",0)
			g.players[index].prevmenu()
	if parsed[0]=="communityremoveadmin":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			grp=get_community(g.players[index].community)
			grp.send("play_s misc227.ogg",0)
			grp.send("communitynotification "+parsed[1]+" is no longer an admin of this community!",0)
			grp.actions+=g.players[index].name+" removed "+parsed[1]+"'s admin role at "+get_current_date()+"\n"
			try: grp.admins.remove(parsed[1])
			except: pass
			g.n.send_reliable(e.peer_id,"Success",0)
			g.players[index].prevmenu()

	if parsed[0]=="sitstart":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			#g.players[index].playsound("sitstart",False)
			g.players[index].sitting=True
	if parsed[0]=="sitstop":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].playsound("sitstop",False)
			g.players[index].sitting=False
	if parsed[0] == "bus_board":
		index = g.get_player_index(e.peer_id)
		if index > -1:
			player = g.players[index]
			if getattr(player, "climbing", False): return
			boarded = False
			for bus in g.transits:
				if bus.map == player.map and bus.running:
					# Narrow ladder contact zone at the front of the bus.
					is_ladder = (bus.x <= player.x <= bus.x + 9) and (player.y == bus.y - 1) and abs(player.z - bus.z) <= 2
					if is_ladder:
						g.play("misc263", player.x, player.y, player.z, player.map)
						g.play("misc77", player.x, player.y, player.z, player.map)
						if bus.is_stopped:
							climb_bus_ladder(player, bus)
							boarded = True
							break
						else:
							g.n.send_reliable(player.peer_id, "The bus is moving, wait for it to stop.", 0)
							break


	if parsed[0]=="groupinvite2":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			char=parsed[1]
			grp=get_group(g.players[index].group)
			ind=get_player_index_from(char)
			if ind>-1:
				try: g.players[ind].groupinvitations.remove(grp.name)
				except: pass
				g.n.send_reliable(g.players[ind].peer_id,"groupnotification "+g.players[index].name+" removed your invitation to "+grp.name,0)
				g.n.send_reliable(g.players[ind].peer_id,"play_s misc202.ogg",0)
			else:
					flist=pickle.loads(file_get_contents("chars/"+g.players[ind].name+"/groupinvitations.usr","rb"))
					try: flist.remove(grp.name)
					except: pass
					file_put_contents("chars/"+g.players[ind].name+"/groupinvitations.usr",pickle.dumps(flist),"wb")
			g.n.send_reliable(e.peer_id,"done",0)
	if parsed[0]=="groupinvite":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			grp=get_group(g.players[index].group)
			ind=get_player_index_from(parsed[1])
			if ind==-1: g.n.send_reliable(e.peer_id,"Player not found",0); return
			if g.players[ind].hidden: g.n.send_reliable(e.peer_id,"Player not found",0); return
			if grp.name in g.players[ind].groupinvitations: g.n.send_reliable(e.peer_id,"This player is already invited to this group",0); g.players[index].prevmenu(); return
			if g.players[ind].groupinvitation==0: g.n.send_reliable(e.peer_id,"This player has disabled receiving group invitations",0); g.players[index].prevmenu(); return
			if g.players[ind].group!="": g.n.send_reliable(e.peer_id,"This player is already joined to a group",0); g.players[index].prevmenu(); return
			g.n.send_reliable(g.players[ind].peer_id,"play_s misc214.ogg",0)
			g.n.send_reliable(g.players[ind].peer_id,"groupnotification "+g.players[index].name+" is inviting you to the "+grp.name+" group! Please use the group menu in the game menu to accept or decline their invitation.",0)
			g.players[ind].groupinvitations.append(grp.name)
			g.n.send_reliable(e.peer_id,"invitation sent",0)
			grp.actions+=g.players[index].name+" invited "+parsed[1]+" at "+get_current_date()+"\n"
			g.players[index].prevmenu()
	if parsed[0]=="communityinvite2":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			char=parsed[1]
			grp=get_community(g.players[index].community)
			ind=get_player_index_from(char)
			if ind>-1:
				try: g.players[ind].communityinvitations.remove(grp.name)
				except: pass
				g.n.send_reliable(g.players[ind].peer_id,"communitynotification "+g.players[index].name+" removed your invitation to "+grp.name,0)
				g.n.send_reliable(g.players[ind].peer_id,"play_s misc202.ogg",0)
			else:
					flist=pickle.loads(file_get_contents("chars/"+g.players[ind].name+"/communityinvitations.usr","rb"))
					try: flist.remove(grp.name)
					except: pass
					file_put_contents("chars/"+g.players[ind].name+"/communityinvitations.usr",pickle.dumps(flist),"wb")
			g.n.send_reliable(e.peer_id,"done",0)
	if parsed[0]=="communityinvite":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			grp=get_community(g.players[index].community)
			ind=get_player_index_from(parsed[1])
			if ind==-1: g.n.send_reliable(e.peer_id,"Player not found",0); return
			if g.players[ind].hidden: g.n.send_reliable(e.peer_id,"Player not found",0); return
			if grp.name in g.players[ind].communityinvitations: g.n.send_reliable(e.peer_id,"This player is already invited to this community",0); g.players[index].prevmenu(); return
			if g.players[ind].communityinvitation==0: g.n.send_reliable(e.peer_id,"This player has disabled receiving community invitations",0); g.players[index].prevmenu(); return
			if g.players[ind].community!="": g.n.send_reliable(e.peer_id,"This player is already joined to a community",0); g.players[index].prevmenu(); return
			g.n.send_reliable(g.players[ind].peer_id,"play_s misc214.ogg",0)
			g.n.send_reliable(g.players[ind].peer_id,"communitynotification "+g.players[index].name+" is inviting you to the "+grp.name+" community! Please use the community menu in the game menu to accept or decline their invitation.",0)
			g.players[ind].communityinvitations.append(grp.name)
			g.n.send_reliable(e.peer_id,"invitation sent",0)
			grp.actions+=g.players[index].name+" invited "+parsed[1]+" at "+get_current_date()+"\n"
			g.players[index].prevmenu()

	if parsed[0]=="lchannelset":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			if parsed[1]=="disable":
				g.n.send_reliable(g.players[index].peer_id,"chatdisable",0)
				g.n.send_reliable(g.players[index].peer_id,"chat disabled",0)
				g.players[index].langchan="disable"
				return
			if g.players[index].langchan==parsed[1]:
				g.n.send_reliable(g.players[index].peer_id,"you're already in this channel",2)
				return
			g.players[index].langchan=parsed[1]
			g.n.send_reliable(g.players[index].peer_id,"channel set to "+parsed[1]+"",0)
			g.n.send_reliable(g.players[index].peer_id,"chatenable",0)
			if parsed[1]=="back": return

	if parsed[0]=="groupinfoselect2":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			try: grp=get_group(g.players[index].groupinfoselect)
			except: return
			if grp is not None and parsed[1]=="members":
				g.n.send_reliable(e.peer_id,"group members: "+convert_to_list(copy.deepcopy(grp.members)),0); g.players[index].prevmenu()
			if parsed[1]=="request":
				if g.players[index].name in grp.join_requests: g.n.send_reliable(e.peer_id,"You already sent join request to this group",0); g.players[index].prevmenu(); return
				grp.join_requests.append(g.players[index].name)
				g.n.send_reliable(e.peer_id,"Join request sent.",0)
				grp.actions+=g.players[index].name+" sent a join request at "+get_current_date()+"\n"
				for m in grp.members:
					if m in grp.admins or grp.owner==m:
						ind=get_player_index_from(m)
						if ind>-1:
							g.n.send_reliable(g.players[ind].peer_id,"groupnotification "+g.players[index].name+" wants to join this group!",0)
							g.n.send_reliable(g.players[ind].peer_id,"play_s misc207.ogg",0)
			if parsed[1]=="request2":
				if g.players[index].name not in grp.join_requests: g.n.send_reliable(e.peer_id,"You didn't sent join request to this group",0); g.players[index].prevmenu(); return
				grp.join_requests.remove(g.players[index].name)
				g.n.send_reliable(e.peer_id,"Join request removed.",0)
				grp.actions+=g.players[index].name+" removed their join request at "+get_current_date()+"\n"
				for m in grp.members:
					if m in grp.admins or grp.owner==m:
						ind=get_player_index_from(m)
						if ind>-1:
							g.n.send_reliable(g.players[ind].peer_id,"groupnotification "+g.players[index].name+" no longer wants to join this group!",0)
							g.n.send_reliable(g.players[ind].peer_id,"play_s misc207.ogg",0)

	if parsed[0]=="groupinfoselect":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			m=server_menu()
			m.intro="Select an option"
			m.initial_packet="groupinfoselect2"
			g.players[index].groupinfoselect=parsed[1]
			m.add("See members","members")
			grp=get_group(parsed[1])
			if grp is None: return
			if g.players[index].group=="" and g.players[index].name not in grp.join_requests: m.add("Send joining request","request")
			if g.players[index].group=="" and g.players[index].name in grp.join_requests: m.add("Remove joining request","request2")
			m.send(e.peer_id)
	if parsed[0]=="communityinfoselect2":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			grp=get_community(g.players[index].communityinfoselect)
			if parsed[1]=="members":
				g.n.send_reliable(e.peer_id,"community members: "+convert_to_list(copy.deepcopy(grp.members)),0); g.players[index].prevmenu()
			if parsed[1]=="request":
				if g.players[index].name in grp.join_requests: g.n.send_reliable(e.peer_id,"You already sent join request to this community",0); g.players[index].prevmenu(); return
				grp.join_requests.append(g.players[index].name)
				g.n.send_reliable(e.peer_id,"Join request sent.",0)
				grp.actions+=g.players[index].name+" sent a join request at "+get_current_date()+"\n"
				for m in grp.members:
					if m in grp.admins or grp.owner==m:
						ind=get_player_index_from(m)
						if ind>-1:
							g.n.send_reliable(g.players[ind].peer_id,"communitynotification "+g.players[index].name+" wants to join this community!",0)
							g.n.send_reliable(g.players[ind].peer_id,"play_s misc207.ogg",0)
			if parsed[1]=="request2":
				if g.players[index].name not in grp.join_requests: g.n.send_reliable(e.peer_id,"You didn't sent join request to this community",0); g.players[index].prevmenu(); return
				grp.join_requests.remove(g.players[index].name)
				g.n.send_reliable(e.peer_id,"Join request removed.",0)
				grp.actions+=g.players[index].name+" removed their join request at "+get_current_date()+"\n"
				for m in grp.members:
					if m in grp.admins or grp.owner==m:
						ind=get_player_index_from(m)
						if ind>-1:
							g.n.send_reliable(g.players[ind].peer_id,"communitynotification "+g.players[index].name+" no longer wants to join this community!",0)
							g.n.send_reliable(g.players[ind].peer_id,"play_s misc207.ogg",0)

	if parsed[0]=="communityinfoselect":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			m=server_menu()
			m.intro="Select an option"
			m.initial_packet="communityinfoselect2"
			g.players[index].communityinfoselect=parsed[1]
			m.add("See members","members")
			grp=get_community(parsed[1])
			if grp is None: return
			if g.players[index].community=="" and g.players[index].name not in grp.join_requests: m.add("Send joining request","request")
			if g.players[index].community=="" and g.players[index].name in grp.join_requests: m.add("Remove joining request","request2")
			m.send(e.peer_id)

	if parsed[0]=="serverstatus":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": g.players[index].prevmenu(); return
			if parsed[1]=="viewp":
				m=server_menu()
				m.initial_packet="pview"
				m.intro="Here you can view the players who were penalized in the game."
				compbanloop()
				m.add(get_comp_bans(),"a",False)
				chars=os.listdir("chars")
				for char in chars:
					charfolder=os.path.join("chars",char)
					if os.path.isfile(charfolder+"/disableallchattime.usr"):
						timestamp=int(file_get_contents("chars/"+char+"/disableallchattime.usr"))
						if int(tm.time())<timestamp:
							m.add(char+"'s all chat feature is disabled due to following reason: "+file_get_contents("chars/"+char+"/disableallchatreason.usr")+". It will be re-enabled after "+ms_to_readable_time2(timestamp-int(tm.time()))+".",char,False)
					if os.path.isfile(charfolder+"/disablepmchattime.usr"):
						timestamp=int(file_get_contents("chars/"+char+"/disablepmchattime.usr"))
						if int(tm.time())<timestamp:
							m.add(char+"'s pm feature is disabled due to following reason: "+file_get_contents("chars/"+char+"/disablepmchatreason.usr")+". It will be re-enabled after "+ms_to_readable_time2(timestamp-int(tm.time()))+".",char)

					if os.path.isfile(charfolder+"/disablevotetime.usr"):
						timestamp=int(file_get_contents("chars/"+char+"/disablevotetime.usr"))
						if int(tm.time())<timestamp:
							m.add(char+"'s vote feature is disabled due to following reason: "+file_get_contents("chars/"+char+"/disablevotereason.usr")+". It will be re-enabled after "+ms_to_readable_time2(timestamp-int(tm.time()))+".",char)

					if os.path.isfile(charfolder+"/disablegroupchattime.usr"):
						timestamp=int(file_get_contents("chars/"+char+"/disablegroupchattime.usr"))
						if int(tm.time())<timestamp:
							m.add(char+"'s group chat feature is disabled due to following reason: "+file_get_contents("chars/"+char+"/disablegroupchatreason.usr")+". It will be re-enabled after "+ms_to_readable_time2(timestamp-int(tm.time()))+".",char)

					if os.path.isfile(charfolder+"/disableteamchattime.usr"):
						timestamp=int(file_get_contents("chars/"+char+"/disableteamchattime.usr"))
						if int(tm.time())<timestamp:
							m.add(char+"'s team chat feature is disabled due to following reason: "+file_get_contents("chars/"+char+"/disableteamchatreason.usr")+". It will be re-enabled after "+ms_to_readable_time2(timestamp-int(tm.time()))+".",char)

					if os.path.isfile(charfolder+"/disablemapchattime.usr"):
						timestamp=int(file_get_contents("chars/"+char+"/disablemapchattime.usr"))
						if int(tm.time())<timestamp:
							m.add(char+"'s map chat feature is disabled due to following reason: "+file_get_contents("chars/"+char+"/disablemapchatreason.usr")+". It will be re-enabled after "+ms_to_readable_time2(timestamp-int(tm.time()))+".",char)

					if os.path.isfile(charfolder+"/disablepublicchattime.usr"):
						timestamp=int(file_get_contents("chars/"+char+"/disablepublicchattime.usr"))
						if int(tm.time())<timestamp:
							m.add(char+"'s public chat feature is disabled due to following reason: "+file_get_contents("chars/"+char+"/disablepublicchatreason.usr")+". It will be re-enabled after "+ms_to_readable_time2(timestamp-int(tm.time()))+".",char)


				m.add("go back","back")
				m.send(g.players[index].peer_id)

	if parsed[0]=="groupdonate":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="[cncel]": g.players[index].prevmenu(); return
			grp=get_group(g.players[index].group)
			try: amount=int(parsed[1])
			except: g.n.send_reliable(e.peer_id,"you need to enter a number",0); g.players[index].prevmenu(); return
			if g.players[index].zhtoken<amount: g.n.send_reliable(e.peer_id,"You do not have that many tokens",0); g.players[index].prevmenu(); return
			if amount<=0: g.n.send_reliable(e.peer_id,"Amount must be greater than zero",0); g.players[index].prevmenu(); return
			grp.donations+=g.players[index].name+" donated "+str(amount)+" zero tokens at "+get_current_date()+"\n"
			grp.zhtoken+=amount
			g.players[index].zhtoken-=amount
			grp.send("play_s misc297.ogg",0)
			grp.send("groupnotification "+g.players[index].name+" donated "+str(amount)+" zero tokens to this group!",0)
			g.players[index].prevmenu()
	if parsed[0]=="groupannounce":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="[cncel]": g.players[index].prevmenu(); return
			grp=get_group(g.players[index].group)
			text=e.message.replace("groupannounce ","")
			grp.announcement=text
			grp.send("play_s misc264.ogg",0)
			grp.send("groupnotification New group announcement! "+text,0)
			for member in grp.members:
				if get_player_index_from(member)==-1:
					file_put_contents("chars/"+member+"/groupinform.usr","New announcement to the group! "+text)
	if parsed[0]=="communityannounce":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="[cncel]": g.players[index].prevmenu(); return
			grp=get_community(g.players[index].community)
			text=e.message.replace("communityannounce ","")
			grp.announcement=text
			grp.send("play_s misc264.ogg",0)
			grp.send("communitynotification New community announcement! "+text,0)
			for member in grp.members:
				if get_player_index_from(member)==-1:
					file_put_contents("chars/"+member+"/communityinform.usr","New announcement to the community! "+text)

	if parsed[0]=="groupdonate2":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="[cncel]": g.players[index].prevmenu(); return
			grp=get_group(g.players[index].group)
			try: amount=int(parsed[1])
			except: g.n.send_reliable(e.peer_id,"you need to enter a number",0); g.players[index].prevmenu(); return
			if grp.zhtoken<amount: g.n.send_reliable(e.peer_id,"group do not have that many tokens",0); g.players[index].prevmenu(); return
			if amount<=0: g.n.send_reliable(e.peer_id,"Amount must be greater than zero",0); g.players[index].prevmenu(); return
			grp.zhtoken-=amount
			g.players[index].zhtoken+=amount
			grp.send("play_s misc275.ogg",0)
			grp.send("groupnotification "+g.players[index].name+" get "+str(amount)+" zero tokens from this group!",0)
			grp.donations+=g.players[index].name+" withdrawn "+str(amount)+" zero tokens at "+get_current_date()+"\n"
			g.players[index].prevmenu()
	if parsed[0]=="group2":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			grp=get_group(g.players[index].group)
			if grp is not None and parsed[1]=="donate2":
				if grp.donations=="": g.n.send_reliable(e.peer_id,"no donations",0); g.players[index].prevmenu(); return
				m=server_menu()
				m.intro="donations"
				m.initial_packet="groupdonatemenu"
				for donation in grp.donations.split("\n"):
					m.add(donation,donation,False)
				m.send(e.peer_id)
			if parsed[1]=="action2":
				grp.actions=""
				g.n.send_reliable(e.peer_id,"done",0); g.players[index].prevmenu()
			if parsed[1]=="log2":
				if grp.owner!=g.players[index].name: g.n.send_reliable(e.peer_id,"only group owner can do this",0); g.players[index].prevmenu(); return
				for base in g.group_bases:
					if base.name==grp.name: base.chestlog=""
				g.n.send_reliable(e.peer_id,"chest log cleared",0); g.players[index].prevmenu()
			if parsed[1]=="log":
				m=server_menu()
				m.intro="base chest log"
				m.initial_packet="chestlog"
				for base in g.group_bases:
					if base.name==grp.name:
						entries=base.chestlog.split("\n")
						for entry in entries:
							m.add(entry,"entry",False)
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"log is empty",0); g.players[index].prevmenu(); return
				m.send(e.peer_id)
			if parsed[1]=="action":
				if grp.actions=="": g.n.send_reliable(e.peer_id,"no actions",0); g.players[index].prevmenu(); return
				m=server_menu()
				m.intro="actions"
				m.initial_packet="groupactionmenu"
				for action in grp.actions.split("\n"):
					m.add(action,action,False)
				m.send(e.peer_id)

			if parsed[1]=="donate3":
				send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "groupdonate2", "how many zero tokens you want to get? group has "+str(grp.zhtoken)+" zero tokens")
			if grp is not None and parsed[1]=="viewannouncement":
				if grp.announcement=="": g.n.send_reliable(e.peer_id,"no announcement",0)
				else: g.n.send_reliable(e.peer_id,grp.announcement,0)
				g.players[index].prevmenu()
			if parsed[1]=="announce":
				send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "groupannounce", "write announcement text")

			if parsed[1]=="donatetoken":
				g.n.send_reliable(e.peer_id,str(grp.zhtoken),0); g.players[index].prevmenu(); return
			if parsed[1]=="donate":
				send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "groupdonate", "how many zero tokens you want to donate?")
			if grp is not None and parsed[1]=="freedom":
				if grp.freedomhit==0: grp.freedomhit=1; g.n.send_reliable(e.peer_id,"enabled",0); g.players[index].prevmenu(); grp.send("play_s misc289.ogg",0); grp.send("groupnotification Now group members can hit the group members in freedom fight map!",0); grp.actions+=g.players[index].name+" enabled members to hit other members in freedom fight map at "+get_current_date()+"\n"; return
				if grp.freedomhit==1: grp.freedomhit=0; g.n.send_reliable(e.peer_id,"disabled",0); g.players[index].prevmenu(); grp.send("play_s misc289.ogg",0); grp.send("groupnotification Now group members can no longer hit the group members in freedom fight map!",0); grp.actions+=g.players[index].name+" disabled members to hit other members in freedom fight map at "+get_current_date()+"\n"; return
			if parsed[1]=="base":
				m=server_menu()
				m.intro="Base information"
				m.initial_packet="baseinfo"

				for i in g.group_bases:
					if i.name==g.players[index].group:
						m.add("base at "+str(i.x)+", "+str(i.y)+", "+str(round(i.z))+" with "+str(i.health)+" health, password is "+i.password,"base")
				m.send(e.peer_id)
			if parsed[1]=="base2":
				for i in g.group_bases:
					if i.name==g.players[index].group:
						g.n.send_reliable(e.peer_id,str(round(i.health)),0); g.players[index].prevmenu()

			name=g.players[index].name
			if grp is not None and parsed[1]=="delete" and send_yesno_question(g.players[index].peer_id,"Are you sure you want to delete this group?")=="yes":
				index=get_player_index_from(name)
				grp.send("play_s misc199.ogg",0)
				grp.send("groupnotification "+g.players[index].name+" deleted this group!",0)
				for base in g.group_bases[:]:
					if base.name==grp.name:
						for pl in g.players:
							if pl.map=="basement"+base.name+base.mapappend: g.move_player(g.get_player_index_from(pl),base.x,base.y,base.z,base.map)
							if pl.map==base.map: base.remove_platform_to(pl)

						file_delete("maps/basement"+base.name+base.mapappend+".map")
						g.group_bases.remove(base)
				try: g.groups.remove(grp)
				except: pass
			if parsed[1]=="rename":
				send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "grouprename", "Enter new name")

			if parsed[1]=="owner":
				m=server_menu()
				m.intro="Select a member to make owner."
				m.initial_packet="groupmakeowner"
				for member in grp.members:
					if member!=grp.owner and member!=g.players[index].name: m.add(member,member)
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"No players found that you can make owner.",0); g.players[index].prevmenu()
				m.send(e.peer_id)

			if parsed[1]=="putbase":
				cnt=0
				for base in g.group_bases:
					if base.name==grp.name: cnt+=1
				if cnt>=5: g.n.send_reliable(e.peer_id,"a group cannot have more than 5 bases",0); g.players[index].prevmenu(); return
				if g.players[index].zhtoken<2000: g.n.send_reliable(e.peer_id,"you need 2000 zero tokens for this",0); g.players[index].prevmenu(); return
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
				if g.players[index].map!="massacre_in_the_city": g.n.send_reliable(e.peer_id,"You can only put  base in freedom fight map",0); return
				max=get_max_values(g.players[index].map)
				mx=round(mx)
				my=round(my)
				if chest_at(mx,my,g.players[index].z,g.players[index].map) or corpse_at(mx,my,g.players[index].z,g.players[index].map) or mx>max.x or my>max.y or mx<0 or my<0 or gpt=="" or gpt=="air" or gpt.startswith("wall"): g.n.send_reliable(e.peer_id,"You can't put base here",0); return
				for base in g.group_bases:
					if base.map==g.players[index].map and g.players[index].distancecheck(base.x,base.y,base.z)<=20: g.n.send_reliable(e.peer_id,"you can't create group base here",0); g.players[index].prevmenu(); return
				create_group_base(mx,my,mz,g.players[index].map,grp.name,g.players[index].name,randomstring())
				grp.actions+=g.players[index].name+" added a new base at "+get_current_date()+"\n"
				grp.send("groupnotification "+g.players[index].name+" added a new base to this group!",0)
				grp.send("play_s misc234.ogg",0)
				bmap="basement"+grp.name+g.group_bases[len(g.group_bases)-1].mapappend
				data=file_get_contents("maps/basement.map")
				data=data.replace("mapname:basement","mapname:"+bmap)
				file_put_contents("maps/"+bmap+".map",data)
				group_baseloop()
				base=g.group_bases[len(g.group_bases)-1]
				for pl in g.players:
					if pl.map==base.map: base.send_platform_to(pl)

				g.n.send_reliable(e.peer_id,"your base password is: "+base.password,2)

				spawn_chest(20,25,0,bmap)
				g.players[index].zhtoken-=2000
			if parsed[1]=="kick":
				m=server_menu()
				m.intro="Select a member to kick."
				m.initial_packet="groupkick"
				for member in grp.members:
					if member!=grp.owner and member!=g.players[index].name and member not in grp.admins: m.add(member,member)
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"No players found that you can kick.",0); g.players[index].prevmenu()
				m.send(e.peer_id)
			if parsed[1]=="makeadmin":
				m=server_menu()
				m.intro="Select a member to make admin."
				m.initial_packet="groupmakeadmin"
				for member in grp.members:
					if member!=grp.owner and member!=g.players[index].name and member not in grp.admins: m.add(member,member)
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"No players found that you can make admin.",0); g.players[index].prevmenu()
				m.send(e.peer_id)
			if parsed[1]=="removeadmin":
				m=server_menu()
				m.intro="Select a member to remove admin."
				m.initial_packet="groupremoveadmin"
				for member in grp.members:
					if member!=grp.owner and member!=g.players[index].name and member in grp.admins: m.add(member,member)
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"No players found that you can remove admin.",0); g.players[index].prevmenu()
				m.send(e.peer_id)
			if parsed[1]=="request":
				m=server_menu()
				m.intro="Select a request."
				m.initial_packet="grouprequest"
				for r in grp.join_requests:
					m.add(r,r)
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"No requests found.",0); g.players[index].prevmenu()
				m.send(e.peer_id)
			if parsed[1]=="invite2":
				m=server_menu()
				m.intro="Select a member to remove invitation."
				m.initial_packet="groupinvite2"
				chars=os.listdir("chars")
				for char in chars:
					charfolder=os.path.join("chars",char)
					try: invitations=pickle.loads(file_get_contents("chars/"+char+"/groupinvitations.usr","rb"))
					except: invitations=[]
					if grp.name in invitations: m.add(char,char)
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"no invitations",0); g.players[index].prevmenu(); return
				m.send(e.peer_id)
			if parsed[1]=="invite":
				m=server_menu()
				m.intro="Select a member to invite."
				m.initial_packet="groupinvite"
				for p in g.players:
					if p.name!=grp.owner and p.name!=g.players[index].name and p.name not in grp.admins and p.name not in grp.members and not p.hidden: m.add(p.name,p.name)
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"No players found that you can invite.",0); g.players[index].prevmenu()
				m.send(e.peer_id)

			if parsed[1]=="admins":
				g.n.send_reliable(e.peer_id,"group admins: "+convert_to_list(copy.deepcopy(grp.admins)),0); g.players[index].prevmenu()
			if grp is not None and parsed[1]=="members":
				g.n.send_reliable(e.peer_id,"group members: "+convert_to_list(copy.deepcopy(grp.members)),0); g.players[index].prevmenu()


			if grp is not None and parsed[1]=="leave":

				try: grp.members.remove(g.players[index].name)
				except: pass
				g.n.send_reliable(e.peer_id,"you left the group",0)
				grp.send("groupnotification "+g.players[index].name+" left this group!",0)
				grp.actions+=g.players[index].name+" left at "+get_current_date()+"\n"
				grp.send("play_s misc190.ogg",0)
			if grp is not None and parsed[1]=="resign":

				try: grp.admins.remove(g.players[index].name)
				except: pass
				g.n.send_reliable(e.peer_id,"you resigned from administrating the group",0)
				grp.send("groupnotification "+g.players[index].name+" resigned from administrating this group!",0)
				grp.actions+=g.players[index].name+" resigned from administrating this group at "+get_current_date()+"\n"
				grp.send("play_s misc227.ogg",0)

			if parsed[1]=="create":
				send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "groupcreate", "Please enter a group name")
			if parsed[1]=="invitation":
				m=server_menu()
				m.intro="Select an invitation."
				m.initial_packet="invitation"
				for i in g.players[index].groupinvitations: m.add(i,i)
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"No group invitations",0); g.players[index].prevmenu(); return
				else: m.send(e.peer_id)

	if parsed[0]=="community2":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			grp=get_community(g.players[index].community)
			if parsed[1]=="action2":
				grp.actions=""
				g.n.send_reliable(e.peer_id,"done",0); g.players[index].prevmenu()
			if parsed[1]=="action":
				if grp.actions=="": g.n.send_reliable(e.peer_id,"no actions",0); g.players[index].prevmenu(); return
				m=server_menu()
				m.intro="actions"
				m.initial_packet="communityactionmenu"
				for action in grp.actions.split("\n"):
					m.add(action,action,False)
				m.send(e.peer_id)

			if grp is not None and parsed[1]=="viewannouncement":
				if grp.announcement=="": g.n.send_reliable(e.peer_id,"no announcement",0)
				else: g.n.send_reliable(e.peer_id,grp.announcement,0)
				g.players[index].prevmenu()
			if parsed[1]=="announce":
				send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "communityannounce", "write announcement text")

			name=g.players[index].name
			if parsed[1]=="delete" and send_yesno_question(g.players[index].peer_id,"Are you sure you want to delete this community?")=="yes":
				index=get_player_index_from(name)
				grp.send("play_s misc199.ogg",0)
				grp.send("communitynotification "+g.players[index].name+" deleted this community!",0)
				g.communitys.remove(grp)
			if parsed[1]=="rename":
				send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "communityrename", "Enter new name")

			if parsed[1]=="owner":
				m=server_menu()
				m.intro="Select a member to make owner."
				m.initial_packet="communitymakeowner"
				for member in grp.members:
					if member!=grp.owner and member!=g.players[index].name: m.add(member,member)
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"No players found that you can make owner.",0); g.players[index].prevmenu()
				m.send(e.peer_id)

			if parsed[1]=="kick":
				m=server_menu()
				m.intro="Select a member to kick."
				m.initial_packet="communitykick"
				for member in grp.members:
					if member!=grp.owner and member!=g.players[index].name and member not in grp.admins: m.add(member,member)
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"No players found that you can kick.",0); g.players[index].prevmenu()
				m.send(e.peer_id)
			if parsed[1]=="makeadmin":
				m=server_menu()
				m.intro="Select a member to make admin."
				m.initial_packet="communitymakeadmin"
				for member in grp.members:
					if member!=grp.owner and member!=g.players[index].name and member not in grp.admins: m.add(member,member)
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"No players found that you can make admin.",0); g.players[index].prevmenu()
				m.send(e.peer_id)
			if parsed[1]=="removeadmin":
				m=server_menu()
				m.intro="Select a member to remove admin."
				m.initial_packet="communityremoveadmin"
				for member in grp.members:
					if member!=grp.owner and member!=g.players[index].name and member in grp.admins: m.add(member,member)
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"No players found that you can remove admin.",0); g.players[index].prevmenu()
				m.send(e.peer_id)
			if parsed[1]=="request":
				m=server_menu()
				m.intro="Select a request."
				m.initial_packet="communityrequest"
				for r in grp.join_requests:
					m.add(r,r)
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"No requests found.",0); g.players[index].prevmenu()
				m.send(e.peer_id)
			if parsed[1]=="invite2":
				m=server_menu()
				m.intro="Select a member to remove invitation."
				m.initial_packet="communityinvite2"
				chars=os.listdir("chars")
				for char in chars:
					charfolder=os.path.join("chars",char)
					try:
						invitations=pickle.loads(file_get_contents("chars/"+char+"/communityinvitations.usr","rb"))
						if grp.name in invitations: m.add(char,char)
					except: pass
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"no invitations",0); g.players[index].prevmenu(); return
				m.send(e.peer_id)
			if parsed[1]=="invite":
				m=server_menu()
				m.intro="Select a member to invite."
				m.initial_packet="communityinvite"
				for p in g.players:
					if p.name!=grp.owner and p.name!=g.players[index].name and p.name not in grp.admins and p.name not in grp.members and not p.hidden: m.add(p.name,p.name)
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"No players found that you can invite.",0); g.players[index].prevmenu()
				m.send(e.peer_id)

			if parsed[1]=="admins":
				g.n.send_reliable(e.peer_id,"community admins: "+convert_to_list(copy.deepcopy(grp.admins)),0); g.players[index].prevmenu()
			if parsed[1]=="members":
				g.n.send_reliable(e.peer_id,"community members: "+convert_to_list(copy.deepcopy(grp.members)),0); g.players[index].prevmenu()


			if grp is not None and parsed[1]=="leave":

				try: grp.members.remove(g.players[index].name)
				except: pass
				g.n.send_reliable(e.peer_id,"you left the community",0)
				grp.send("communitynotification "+g.players[index].name+" left this community!",0)
				grp.actions+=g.players[index].name+" left at "+get_current_date()+"\n"
				grp.send("play_s misc190.ogg",0)
			if grp is not None and parsed[1]=="resign":

				try: grp.admins.remove(g.players[index].name)
				except: pass
				g.n.send_reliable(e.peer_id,"you resigned from administrating the community",0)
				grp.send("communitynotification "+g.players[index].name+" resigned from administrating this community!",0)
				grp.actions+=g.players[index].name+" resigned from administrating this community at "+get_current_date()+"\n"
				grp.send("play_s misc227.ogg",0)

			if parsed[1]=="create":
				send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "communitycreate", "Please enter a community name")
			if parsed[1]=="invitation":
				m=server_menu()
				m.intro="Select an invitation."
				m.initial_packet="cinvitation"
				for i in g.players[index].communityinvitations: m.add(i,i)
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"No community invitations",0); g.players[index].prevmenu(); return
				else: m.send(e.peer_id)


	if parsed[0]=="friend2":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return

			if parsed[1]=="friendrequests":
				m=server_menu()
				m.intro="Select player to refuse or accept"
				m.initial_packet="addfriendchoose"
				for pl in g.players[index].pendingfriendlist:
					if pl!=g.players[index].name: m.add(pl,pl)
				if len(m.menuids)==0:
					g.n.send_reliable(e.peer_id,"No friend requests found.",0)
					g.players[index].prevmenu()
				m.send(e.peer_id)
			if parsed[1]=="friendrequests2":
				m=server_menu()
				m.intro="Select player to remove your request"
				m.initial_packet="addfriendchoose3"
				for p in g.players:
					if g.players[index].name==p.name: continue
					if p.hidden: continue
					for pl in p.pendingfriendlist:
						if pl==g.players[index].name: m.add(p.name,p.name); break
				if len(m.menuids)==0:
					g.n.send_reliable(e.peer_id,"No friend requests found.",0)
					g.players[index].prevmenu()
				m.send(e.peer_id)

			if parsed[1]=="friendadd":
				m=server_menu()
				m.intro="Select player to add as friend"
				m.initial_packet="addfriend"
				for pl in g.players:
					if not pl.hidden and pl.name not in g.players[index].friendlist and pl.name not in g.players[index].pendingfriendlist and pl.name!=g.players[index].name: m.add(pl.name,pl.name)
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"No players found that you can add as friend.",0); g.players[index].prevmenu(); return
				m.send(e.peer_id)
			name=g.players[index].name
			if parsed[1]=="friendclean" and send_yesno_question(g.players[index].peer_id,"are you sure you want to clear your friend list?")=="yes":
				index=get_player_index_from(name)
				g.players[index].friendlist.clear()
				g.n.send_reliable(e.peer_id,"done",0); g.players[index].prevmenu(); return
			if parsed[1]=="friendremove":
				m=server_menu()
				m.initial_packet="removefriend"
				removefriendadd(m,index)
				if len(m.menuids)==0:
					g.n.send_reliable(e.peer_id,"no friends found.",0)
					g.players[index].prevmenu()
				m.send(e.peer_id)

	if parsed[0]=="staffmenu":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": g.players[index].prevmenu()

	if parsed[0]=="notifys":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back":
				g.players[index].prevmenu()
				return
			if parsed[1]=="mapmessage":
				if g.players[index].mapmessage==0:
					g.players[index].mapmessage=1
					send_reliable(g.players[index].peer_id,"enabled",0)
				elif g.players[index].mapmessage==1:
					g.players[index].mapmessage=0
					send_reliable(g.players[index].peer_id,"disabled",0)
			if parsed[1]=="groupmessage":
				if g.players[index].groupmessage==0:
					g.players[index].groupmessage=1
					send_reliable(g.players[index].peer_id,"enabled",0)
				elif g.players[index].groupmessage==1:
					g.players[index].groupmessage=0
					send_reliable(g.players[index].peer_id,"disabled",0)
			if parsed[1]=="groupinvitation":
				if g.players[index].groupinvitation==0:
					g.players[index].groupinvitation=1
					send_reliable(g.players[index].peer_id,"enabled",0)
				elif g.players[index].groupinvitation==1:
					g.players[index].groupinvitation=0
					send_reliable(g.players[index].peer_id,"disabled",0)


			if parsed[1]=="pmmessage":
				if g.players[index].pmmessage==0:
					g.players[index].pmmessage=1
					send_reliable(g.players[index].peer_id,"enabled",0)
				elif g.players[index].pmmessage==1:
					g.players[index].pmmessage=0
					send_reliable(g.players[index].peer_id,"disabled",0)
			if parsed[1]=="voicemessage":
				if g.players[index].voicemessage==0:
					if g.players[index].blockvoice3==1:
						g.n.send_reliable(g.players[index].peer_id,"your voice chat feature have been blocked by staff",0)
						g.n.send_reliable(g.players[index].peer_id,"disablevoicechat",0)
						return
					g.players[index].voicemessage=1
					send_reliable(g.players[index].peer_id,"enabled",0)
					send_reliable(g.players[index].peer_id,"enablevoicechat",0)
				elif g.players[index].voicemessage==1:
					if g.players[index].blockvoice3==1:
						g.n.send_reliable(g.players[index].peer_id,"your voice chat feature have been blocked by staff",0)
						g.n.send_reliable(g.players[index].peer_id,"disablevoicechat",0)
						return

					g.players[index].voicemessage=0
					send_reliable(g.players[index].peer_id,"disabled",0)
					send_reliable(g.players[index].peer_id,"disablevoicechat",0)
			if parsed[1]=="voicemessage2":
				if g.players[index].voicemessage2==0:
					if g.players[index].blockvoice3==1:
						g.n.send_reliable(g.players[index].peer_id,"your voice chat feature have been blocked by staff",0)
						g.n.send_reliable(g.players[index].peer_id,"disablevoicechat2",0)
						return
					g.players[index].voicemessage2=1
					send_reliable(g.players[index].peer_id,"enabled",0)
					send_reliable(g.players[index].peer_id,"enablevoicechat2",0)
				elif g.players[index].voicemessage2==1:
					if g.players[index].blockvoice3==1:
						g.n.send_reliable(g.players[index].peer_id,"your voice chat feature have been blocked by staff",0)
						g.n.send_reliable(g.players[index].peer_id,"disablevoicechat2",0)
						return

					g.players[index].voicemessage2=0
					send_reliable(g.players[index].peer_id,"disabled",0)
					send_reliable(g.players[index].peer_id,"disablevoicechat2",0)

			if parsed[1]=="friendmessage":
				if g.players[index].friendmessage==0:
					g.players[index].friendmessage=1
					send_reliable(g.players[index].peer_id,"enabled",0)
				elif g.players[index].friendmessage==1:
					g.players[index].friendmessage=0
					send_reliable(g.players[index].peer_id,"disabled",0)
			if parsed[1]=="matchmessage":
				if g.players[index].matchmessage==0:
					g.players[index].matchmessage=1
					send_reliable(g.players[index].peer_id,"enabled",0)
				elif g.players[index].matchmessage==1:
					g.players[index].matchmessage=0
					send_reliable(g.players[index].peer_id,"disabled",0)
			if parsed[1]=="teammessage":
				if g.players[index].teammessage==0:
					g.players[index].teammessage=1
					send_reliable(g.players[index].peer_id,"enabled",0)
				elif g.players[index].teammessage==1:
					g.players[index].teammessage=0
					send_reliable(g.players[index].peer_id,"disabled",0)
			if parsed[1]=="friendonlinemessage":
				if g.players[index].friendonlinemessage==0:
					g.players[index].friendonlinemessage=1
					send_reliable(g.players[index].peer_id,"enabled",0)
				elif g.players[index].friendonlinemessage==1:
					g.players[index].friendonlinemessage=0
					send_reliable(g.players[index].peer_id,"disabled",0)

			if parsed[1]=="ticketmail":
				if g.players[index].ticketmail==0:
					g.players[index].ticketmail=1
					send_reliable(g.players[index].peer_id,"enabled",0)
				elif g.players[index].ticketmail==1:
					g.players[index].ticketmail=0
					send_reliable(g.players[index].peer_id,"disabled",0)
			if parsed[1]=="communitymessage":
				if g.players[index].communitymessage==0:
					g.players[index].communitymessage=1
					send_reliable(g.players[index].peer_id,"enabled",0)
				elif g.players[index].communitymessage==1:
					g.players[index].communitymessage=0
					send_reliable(g.players[index].peer_id,"disabled",0)
			if parsed[1]=="matchinvite":
				if g.players[index].matchinvite==0:
					g.players[index].matchinvite=1
					send_reliable(g.players[index].peer_id,"enabled",0)
				elif g.players[index].matchinvite==1:
					g.players[index].matchinvite=0
					send_reliable(g.players[index].peer_id,"disabled",0)

			if parsed[1]=="eventalerts":
				if g.players[index].eventalerts==0:
					g.players[index].eventalerts=1
					send_reliable(g.players[index].peer_id,"enabled",0)
				elif g.players[index].eventalerts==1:
					g.players[index].eventalerts=0
					send_reliable(g.players[index].peer_id,"disabled",0)

			if parsed[1]=="mapsound":
				if g.players[index].mapsound==0:
					g.players[index].mapsound=1
					send_reliable(g.players[index].peer_id,"enabled",0)
				elif g.players[index].mapsound==1:
					g.players[index].mapsound=0
					send_reliable(g.players[index].peer_id,"disabled",0)


			if parsed[1]=="authreq":
				if g.players[index].authreq==0:
					g.players[index].authreq=1
					send_reliable(g.players[index].peer_id,"enabled",0)
				elif g.players[index].authreq==1:
					g.players[index].authreq=0
					send_reliable(g.players[index].peer_id,"disabled",0)

			if parsed[1]=="votenotify":
				if g.players[index].votenotify==0:
					g.players[index].votenotify=1
					send_reliable(g.players[index].peer_id,"enabled",0)
				elif g.players[index].votenotify==1:
					g.players[index].votenotify=0
					send_reliable(g.players[index].peer_id,"disabled",0)



			if parsed[1]=="istyping":
				if g.players[index].istyping==0:
					g.players[index].istyping=1
					send_reliable(g.players[index].peer_id,"enabled",0)
				elif g.players[index].istyping==1:
					g.players[index].istyping=0
					send_reliable(g.players[index].peer_id,"disabled",0)

			if parsed[1]=="chestpickupnotify":
				if g.players[index].chestpickupnotify==0:
					g.players[index].chestpickupnotify=1
					send_reliable(g.players[index].peer_id,"enabled",0)
				elif g.players[index].chestpickupnotify==1:
					g.players[index].chestpickupnotify=0
					send_reliable(g.players[index].peer_id,"disabled",0)



			if parsed[1]=="tokentransfer":
				if g.players[index].tokentransfer==0:
					g.players[index].tokentransfer=1
					send_reliable(g.players[index].peer_id,"enabled",0)
				elif g.players[index].tokentransfer==1:
					g.players[index].tokentransfer=0
					send_reliable(g.players[index].peer_id,"disabled",0)


	if parsed[0]=="createvote2":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if not g.players[index].disable_vote_check(): return

			if parsed[1]=="[cncel]": return
			v=vote(g.players[index].name,g.players[index].votetitle,e.message.replace("createvote2 ",""))
			g.votes.append(v)
			g.n.send_reliable(e.peer_id,"poll successfully created",0)
			for i in range(len(g.players)):
				if g.players[i].votenotify==1: g.n.send_reliable(g.players[i].peer_id,"a new poll has been created by "+g.players[index].name+". Title: "+g.players[index].votetitle+". Message: "+v.message,2)
				if g.players[i].votenotify==1: g.n.send_reliable(g.players[i].peer_id,"play_s misc304.ogg",0)
			update_char_counter("votecount")
	if parsed[0]=="createvote":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if not g.players[index].disable_vote_check(): return

			if parsed[1]=="[cncel]": return
			g.players[index].votetitle=e.message.replace("createvote ","")
			send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "createvote2", "Enter poll message")
	if parsed[0]=="vote2":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			if parsed[1]=="create":
				if not g.players[index].disable_vote_check(): return

				for v in g.votes:
					if not v.stick and not v.ended and v.owner==g.players[index].name: g.n.send_reliable(e.peer_id,"you already have a unended poll",0); g.players[index].prevmenu(); return
				send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "createvote", "Enter poll title")
			if parsed[1]=="view":
				if not g.votes: g.n.send_reliable(g.players[index].peer_id,"no polls",2); g.players[index].prevmenu(); return

				m=server_menu()
				m.intro="Select poll to view"
				m.initial_packet="voteview"
				for v in list(reversed(g.votes)):
					if not v.stick: continue
					if not v.ended and not v.stick: m.add("in progress, poll of "+v.owner+". Title: "+v.title+", message: "+v.message+", will end in "+ms_to_readable_time(86400000 - v.timer.elapsed),v.owner+"{}[]"+v.title+"{}[]"+v.message+"{}[]"+v.id)
					if v.stick: m.add("sticky, poll of "+v.owner+". Title: "+v.title+", message: "+v.message,v.owner+"{}[]"+v.title+"{}[]"+v.message+"{}[]"+v.id)
					if v.ended and not v.stick: m.add("ended, poll of "+v.owner+". Title: "+v.title+", message: "+v.message,v.owner+"{}[]"+v.title+"{}[]"+v.message+"{}[]"+v.id)


				for v in list(reversed(g.votes)):
					if v.stick: continue
					if not v.ended and not v.stick: m.add("in progress, poll of "+v.owner+". Title: "+v.title+", message: "+v.message+", will end in "+ms_to_readable_time(86400000 - v.timer.elapsed),v.owner+"{}[]"+v.title+"{}[]"+v.message+"{}[]"+v.id)
					if v.stick: m.add("sticky, poll of "+v.owner+". Title: "+v.title+", message: "+v.message+", will end in "+ms_to_readable_time(86400000 - v.timer.elapsed),v.owner+"{}[]"+v.title+"{}[]"+v.message+"{}[]"+v.id)
					if v.ended and not v.stick: m.add("ended, poll of "+v.owner+". Title: "+v.title+", message: "+v.message,v.owner+"{}[]"+v.title+"{}[]"+v.message+"{}[]"+v.id)

				m.send(e.peer_id)
	if parsed[0]=="ticket2":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return

			if parsed[1]=="ticketview":
				m=server_menu()
				m.intro="Select ticket to view"
				m.initial_packet="ticketviewchoose"
				for ticket in g.tickets:
					if ticket["owner"]==g.players[index].name: m.add((("pending, " if ticket["pending"] else "Open, ") if not ticket["closed"] else "closed, ")+ticket["title"]+", department "+ticket["department"]+", Last updated "+get_datetime_difference(ticket["lastupdate"])+" ago.",ticket["id"])
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"You have no tickets",0); g.players[index].prevmenu(); return
				m.send(e.peer_id)

			if parsed[1]=="ticketcreate":
				if not g.players[index].android and not g.players[index].ios: g.n.send_reliable(e.peer_id,"ticketcreate",0)
				else: 				send_serverbox(g.players[index].peer_id, 0, 1000, 0, -1, "ticket_create_title", "Enter Ticket Title:")
			if parsed[1]=="serverview":
				m=server_menu()
				m.intro="Select ticket category to view"
				m.initial_packet="serverviewcategory"
				m.add("open tickets, "+str(get_open_ticket_count()),"open")
				m.add("closed tickets, "+str(get_closed_ticket_count()),"closed")
				m.add("pending tickets, "+str(get_pending_ticket_count()),"pending")
				m.send(e.peer_id)

	if parsed[0]=="serverviewcategory":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return

			if parsed[1]=="open":
				m=server_menu()
				m.intro="Select ticket to view"
				m.initial_packet="serverviewchoose"
				for ticket in g.tickets:
					if ticket["closed"] or ticket["pending"]: continue
					m.add((("pending, " if ticket["pending"] else "Open, ") if not ticket["closed"] else "closed, ")+ticket["title"]+", department "+ticket["department"]+", created at "+ticket["createdate"]+" by "+ticket["owner"]+", last updated "+get_datetime_difference(ticket["lastupdate"])+" ago.",ticket["id"])
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"list empty",0); g.players[index].prevmenu(); return
				m.send(e.peer_id)

			if parsed[1]=="closed":
				m=server_menu()
				m.intro="Select ticket to view"
				m.initial_packet="serverviewchoose"
				for ticket in g.tickets:
					if not ticket["closed"] or ticket["pending"]: continue
					m.add((("pending, " if ticket["pending"] else "Open, ") if not ticket["closed"] else "closed, ")+ticket["title"]+", department "+ticket["department"]+", created at "+ticket["createdate"]+" by "+ticket["owner"]+", last updated "+get_datetime_difference(ticket["lastupdate"])+" ago.",ticket["id"])
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"list empty",0); g.players[index].prevmenu(); return
				m.send(e.peer_id)


			if parsed[1]=="pending":
				m=server_menu()
				m.intro="Select ticket to view"
				m.initial_packet="serverviewchoose"
				for ticket in g.tickets:
					if not ticket["pending"]: continue
					m.add((("pending, " if ticket["pending"] else "Open, ") if not ticket["closed"] else "closed, ")+ticket["title"]+", department "+ticket["department"]+", created at "+ticket["createdate"]+" by "+ticket["owner"]+", last updated "+get_datetime_difference(ticket["lastupdate"])+" ago.",ticket["id"])
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"list empty",0); g.players[index].prevmenu(); return
				m.send(e.peer_id)



	if parsed[0]=="changepasswd":
		index=g.get_player_index(e.peer_id)
		if(index>-1 and parsed[1]!="[cncel]"):
			file_put_contents("chars/"+g.players[index].name+"/pass.usr",parsed[1])
			g.n.send_reliable(e.peer_id,"done",0)
	if parsed[0]=="eml":
		index=g.get_player_index(e.peer_id)
		if(index>-1 and parsed[1]!="[cncel]"):
			# Cooldown kontrolü (Eger daha once degistirdiyse)
			if file_exists("chars/"+g.players[index].name+"/lastmail.usr"):
				maildate=pickle.loads(file_get_contents("chars/"+g.players[index].name+"/lastmail.usr","rb"))
				if not time_difference_exceeds_24_hours(datetime.now(),maildate):
					g.n.send_reliable(e.peer_id,"You can only change your email 1 time each day",0); return

			# Yeni mail adresini kaydet
			g.players[index].neweml=parsed[1]
			mailcode=randomstring()
			file_put_contents("chars/"+g.players[index].name+"/mailcode.usr",mailcode)
			
			# BURADA ZAMAN DAMGASI KAYDETMİYORUZ (Cooldown baslamamasi icin)

			send_mail(file_get_contents("chars/"+g.players[index].name+"/mail.usr"),"Code for changing email for zero hour assault","Hello "+g.players[index].name+",<br>You have requested to change your email address. To continue, please use this code<br>"+mailcode+"<br>Copyright 2025 NBM studios, all rights reserved")
			send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "eml2", "Enter code sent to your old email")
	if parsed[0]=="eml2":
		index=g.get_player_index(e.peer_id)
		if(index>-1 and parsed[1]!="[cncel]"):
			if parsed[1]!=file_get_contents("chars/"+g.players[index].name+"/mailcode.usr"): g.n.send_reliable(e.peer_id,"invalid code",0); return
			mailcode=randomstring()
			file_put_contents("chars/"+g.players[index].name+"/mailcode.usr",mailcode)
			send_mail(g.players[index].neweml,"Code for changing email for zero hour assault","Hello "+g.players[index].name+",<br>You have requested to change your email address. To continue, please use this code<br>"+mailcode+"<br>Copyright 2025 NBM studios, all rights reserved")
			send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "eml3", "Enter code sent to your new email")
	if parsed[0]=="changestatus":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="[cncel]": g.n.send_reliable(g.players[index].peer_id,"canceled",0); g.players[index].prevmenu(); return
			if parsed[1]=="": g.players[index].status=""; g.n.send_reliable(g.players[index].peer_id,"you removed your status message by leaving the text blank",0); g.players[index].prevmenu(); return
			g.players[index].status=string_replace(e.message,parsed[0]+" ","",False)
			g.n.send_reliable(g.players[index].peer_id,"Status set!",0)
			g.players[index].prevmenu()
	if parsed[0]=="rename2":
		index=g.get_player_index(e.peer_id)
		if(index>-1 and parsed[1]!="[cncel]"):
			if " " in parsed[1] or "/" in parsed[1] or not parsed[1].isascii(): g.n.send_reliable(e.peer_id,"invalid input",0); return
			if g.players[index].zhtoken<150: g.n.send_reliable(g.players[index].peer_id,"you don't have 150 tokens",2); g.players[index].prevmenu(); return

			if directory_exists2("chars/"+parsed[1].lower()) or directory_exists2("chars/"+parsed[1]): g.n.send_reliable(e.peer_id,"this account exists",0); g.players[index].prevmenu(); return
			for ticket in g.tickets:
				if ticket["owner"]==g.players[index].name: ticket["owner"]=parsed[1]
			for grp in g.groups:
				if grp.owner==g.players[index].name: grp.owner=parsed[1]
				if g.players[index].name in grp.members:
					for m in range(len(grp.members)):
						if grp.members[m]==g.players[index].name: grp.members[m]=parsed[1]
				if g.players[index].name in grp.admins:
					for m in range(len(grp.admins)):
						if grp.admins[m]==g.players[index].name: grp.admins[m]=parsed[1]

			for grp in g.communitys:
				if grp.owner==g.players[index].name: grp.owner=parsed[1]
				if g.players[index].name in grp.members:
					for m in range(len(grp.members)):
						if grp.members[m]==g.players[index].name: grp.members[m]=parsed[1]
				if g.players[index].name in grp.admins:
					for m in range(len(grp.admins)):
						if grp.admins[m]==g.players[index].name: grp.admins[m]=parsed[1]


			for friend in g.players[index].friendlist:
				ind=get_player_index_from(friend)
				if ind>-1:
					try:
						f=g.players[ind].friendlist.index(g.players[index].name)
						g.players[ind].friendlist[f]=parsed[1]
					except: pass
				else:
					try:
						flist=pickle.loads(file_get_contents("chars/"+friend+"/friendlist.usr","rb"))
						f=flist.index(g.players[index].name)
						flist[f]=parsed[1]
						file_put_contents("chars/"+friend+"/friendlist.usr",pickle.dumps(flist),"wb")

					except: pass
			# --- FIX BAŞLANGICI ---
			# Timed itemlerin sahibini yeni isme taşı
			for t_item in g.timeditems:
				if t_item.owner == g.players[index].name:
					t_item.owner = parsed[1]
			# --- FIX BİTİŞİ ---

			g.players[index].zhtoken-=150
			try:
				f=open("chars/"+g.players[index].name+"/renamehistory.usr","a")
				f.write("You changed your name from "+g.players[index].name+" to "+parsed[1]+" in "+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"\n")
				f.close()
			except: pass
			save_char(index)
			notify_admins("zero hour assault, "+g.players[index].name+" changed their name to "+parsed[1]+"")
			adminsend(""+g.players[index].name+" changed their name to "+parsed[1]+"")
			g.n.send_reliable(e.peer_id,"Done",0)
			oldname=g.players[index].name
			remove_from_server(index)

			try: os.rename("chars/"+oldname, "chars/"+parsed[1])
			except: pass
	if parsed[0]=="eml3":
		index=g.get_player_index(e.peer_id)
		if(index>-1 and parsed[1]!="[cncel]"):
			if parsed[1]!=file_get_contents("chars/"+g.players[index].name+"/mailcode.usr"): g.n.send_reliable(e.peer_id,"invalid code",0); return

			# Kod dogru ise maili degistir
			file_put_contents("chars/"+g.players[index].name+"/mail.usr",g.players[index].neweml)
			
			# ZAMAN DAMGASINI SADECE BASARILI OLUNCA KAYDET (YENI EKLENEN KISIM)
			file_put_contents("chars/"+g.players[index].name+"/lastmail.usr",pickle.dumps(datetime.now()),"wb")
			
			g.n.send_reliable(e.peer_id,"done",0)
			remove_from_server(index)
	if parsed[0]=="compid":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			name=g.players[index].name



			if send_yesno_question(g.players[index].peer_id,"Are you sure you want to block this computer from logging into your account? to remove the block, you will have to verify your email access.") == "yes":
				index=get_player_index_from(name)
				compids=file_get_contents("chars/"+g.players[index].name+"/authorized_compids.usr").split("\n")
				if parsed[1] not in compids: g.n.send_reliable(e.peer_id,"This computer is not authorized to log into your account",0); return
				compids.remove(parsed[1])
				file_put_contents("chars/"+g.players[index].name+"/authorized_compids.usr","\n".join(compids))
				g.n.send_reliable(e.peer_id,"Done",0)
				if g.players[index].compid==parsed[1]: remove_from_server(index)
	if parsed[0]=="adminlog":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if(parsed[1]=="log2"):
				g.n.send_reliable(e.peer_id,"copyed",0)
				g.n.send_reliable(e.peer_id,"clip "+file_get_contents("adminlog.txt"),0)
				g.players[index].prevmenu()

			if parsed[1]=="log":
				if not file_exists("adminlog.txt") or file_get_contents("adminlog.txt")=="":
					send_reliable(e.peer_id, "no logs", 0)
					g.players[index].prevmenu()
					return
				r=open("adminlog.txt", "r")
				changes=string_split(r.read(), "\n", True)
				r.close()
				if len(changes)<=0:
					send_reliable(e.peer_id, "no logs", 0)
					g.players[index].prevmenu()
					return
				m=server_menu()
				m.intro="Command logs."
				m.initial_packet="latest"
				for i in range(len(changes)):
					m.add(string_replace(changes[i], ":", ".", True), string_replace(changes[i], ":", ".", True),False)
				m.send(e.peer_id)
			if parsed[1]=="adminhelp":
				if not file_exists("adminhelp.txt") or file_get_contents("adminhelp.txt")=="":
					send_reliable(e.peer_id, "no help", 0)
					g.players[index].prevmenu()
					return
				r=open("adminhelp.txt", "rb")
				changes=string_split(r.read().decode("utf-8",errors="ignore"), "\n", True)
				r.close()
				if len(changes)<=0:
					send_reliable(e.peer_id, "no help", 0)
					g.players[index].prevmenu()
					return
				m=server_menu()
				m.intro="Admin help menu. Here you can view commands for admins."
				m.initial_packet="latest"
				for i in range(len(changes)):
					m.add(string_replace(changes[i], ":", ".", True), string_replace(changes[i], ":", ".", True),False)
				m.send(e.peer_id)
			if parsed[1]=="moderatorhelp":
				if not file_exists("moderatorhelp.txt") or file_get_contents("moderatorhelp.txt")=="":
					send_reliable(e.peer_id, "no help", 0)
					g.players[index].prevmenu()
					return
				r=open("moderatorhelp.txt", "r")
				changes=string_split(r.read(), "\n", True)
				r.close()
				if len(changes)<=0:
					send_reliable(e.peer_id, "no help", 0)
					g.players[index].prevmenu()
					return
				m=server_menu()
				m.intro="moderator help menu. Here you can view commands for moderators."
				m.initial_packet="latest"
				for i in range(len(changes)):
					m.add(string_replace(changes[i], ":", ".", True), string_replace(changes[i], ":", ".", True),False)
				m.send(e.peer_id)

			if parsed[1]=="builderhelp":
				if not file_exists("builderhelp.txt") or file_get_contents("builderhelp.txt")=="":
					send_reliable(e.peer_id, "no help", 0)
					g.players[index].prevmenu()
					return
				r=open("builderhelp.txt", "r")
				changes=string_split(r.read(), "\n", True)
				r.close()
				if len(changes)<=0:
					send_reliable(e.peer_id, "no help", 0)
					g.players[index].prevmenu()
					return
				m=server_menu()
				m.intro="Builder help menu. Here you can view commands for builders."
				m.initial_packet="latest"
				for i in range(len(changes)):
					m.add(string_replace(changes[i], ":", ".", True), string_replace(changes[i], ":", ".", True),False)
				m.send(e.peer_id)


			if parsed[1]=="suggestion":
				if not file_exists("suggest.txt") or file_get_contents("suggest.txt")=="":
					send_reliable(e.peer_id, "no suggestions", 0)
					g.players[index].prevmenu()
					return
				r=open("suggest.txt", "r")
				changes=string_split(r.read(), "\n", True)
				r.close()
				if len(changes)<=0:
					send_reliable(e.peer_id, "no suggestions", 0)
					g.players[index].prevmenu()
					return
				m=server_menu()
				m.intro="Suggestions."
				m.initial_packet="latest"
				for i in range(len(changes)):
					m.add(string_replace(changes[i], ":", ".", True), string_replace(changes[i], ":", ".", True),False)
				m.send(e.peer_id)

			if parsed[1]=="dataeditor":
				if not (g.players[index].is_admin() or g.players[index].dev):
					g.n.send_reliable(e.peer_id,"You don't have permission to use the data editor.",0)
					g.players[index].prevmenu()
					return
				handle_data_editor(e, ["de_main"], index)
	if parsed[0]=="confirmdelete":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="[cncel]": 
				g.n.send_reliable(e.peer_id, "Deletion canceled.", 0)
				return
			
			name = g.players[index].name
			# Kaydedilen kodu oku
			real_code = file_get_contents("chars/"+name+"/delcode.usr")
			
			# Girilen kod dogru mu?
			if parsed[1] == real_code and real_code != "":
				file_delete("chars/"+name+"/delcode.usr") # Kodu sil
				g.n.send_reliable(e.peer_id, "Account deleted successfully.", 0)
				
				# Oyuncuyu sunucudan at ve klasoru sil
				remove_from_server(index)
				directory_delete("chars/"+name)
				
				# Adminlere log dus
				adminsend(name + " has verified their email and deleted their account.")
			else:
				g.n.send_reliable(e.peer_id, "Incorrect verification code. Process canceled.", 0)
	if parsed[0]=="confirmpasswdcode":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="[cncel]": 
				g.n.send_reliable(e.peer_id, "Password change canceled.", 0)
				return
			
			name = g.players[index].name
			real_code = file_get_contents("chars/"+name+"/passcode.usr")
			
			if parsed[1] == real_code and real_code != "":
				file_delete("chars/"+name+"/passcode.usr") # Kodu sil
				g.n.send_reliable(e.peer_id, "Code verified.", 0)
				
				# Kod dogruysa asil sifre degistirme kutusunu ac
				send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "changepasswd", "Enter new password")
			else:
				g.n.send_reliable(e.peer_id, "Incorrect verification code.", 0)
	if parsed[0]=="securitychoose":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			name=g.players[index].name
			if parsed[1]=="rhist":
				m=server_menu()
				m.intro="Rename history"
				m.initial_packet="renamehistory"
				data=file_get_contents("chars/"+g.players[index].name+"/renamehistory.usr").split("\n")
				for i in data:
					m.add(i,i,False)
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"You never renamed your account",0); g.players[index].prevmenu(); return
				m.send(e.peer_id)
			if parsed[1]=="rename":
				if g.players[index].zhtoken<150: g.n.send_reliable(e.peer_id,"You need 150 zero tokens to rename your character",0); g.players[index].prevmenu(); return

				send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "rename2", "enter new name, warning, you need 150 tokens for proceed")
			if parsed[1]=="clearstatus":
				if g.players[index].status=="": g.n.send_reliable(g.players[index].peer_id,"you did not set a status message",0); g.players[index].prevmenu(); return
				g.players[index].status=""
				g.n.send_reliable(g.players[index].peer_id,"Status cleared!",0)
				g.players[index].prevmenu()
			if parsed[1]=="setstatus":

				send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "changestatus", "Type your text here. A maximum of 1000 characters is allowed.")
			if parsed[1]=="delete":
				createdate=file_get_contents("chars/"+g.players[index].name+"/createdate.usr","r")
				if not time_difference_exceeds_1_week(datetime.now(),datetime.strptime(createdate,"%Y-%m-%d %H:%M:%S")): g.n.send_reliable(e.peer_id,"Your account must be created at least one week ago before you can delete it",0); g.players[index].prevmenu(); return
				name=g.players[index].name
				
				# Ilk soru: Emin misin?
				if send_yesno_question(g.players[index].peer_id,"Are you sure you want to delete your account? You cannot get it back if you delete it.")=="yes":
					index=get_player_index_from(name)
					# Kod olustur
					delverifycode = randomstring(6)
					# Kodu dosyaya kaydet
					file_put_contents("chars/"+name+"/delcode.usr", delverifycode)
					# Mail adresini al
					mailaddr = file_get_contents("chars/"+name+"/mail.usr")
					# Mail gonder
					send_mail(mailaddr, "Account Deletion Verification", "Hello " + name + ",<br>Use this code to confirm deletion of your zero hour assault account: " + delverifycode)
					
					# Server box acip kodu iste
					send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "confirmdelete", "Enter the code sent to your email to confirm deletion")
			if parsed[1]=="compid":
				m=server_menu()
				m.intro="Select a computer"
				m.initial_packet="compid"
				compids=file_get_contents("chars/"+g.players[index].name+"/authorized_compids.usr").split("\n")
				m.add("current computer with id "+g.players[index].compid,g.players[index].compid)
				for compid in compids:
					if compid!=g.players[index].compid: m.add("computer with id "+compid,compid)
				m.send(e.peer_id)
			if parsed[1]=="passwd": 
				if g.players[index].authreq == 1:
					# Authreq acik (1) ise direkt sifre degistirme kutusunu ac
					send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "changepasswd", "Enter new password")
				else:
					# Authreq kapali (0) ise mail gonderip kod iste (Eski mantik)
					passverifycode = randomstring(6)
					file_put_contents("chars/"+g.players[index].name+"/passcode.usr", passverifycode)
					mailaddr = file_get_contents("chars/"+g.players[index].name+"/mail.usr")
					send_mail(mailaddr, "Password Change Verification", "Hello " + g.players[index].name + ",<br>Use this code to verify your identity before changing your zero hour assault account password: " + passverifycode)
					send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "confirmpasswdcode", "Enter the code sent to your email")
			if parsed[1]=="eml" and send_yesno_question(g.players[index].peer_id,"Warning. You can only change your email address 1 time each day. Do you want to continue?")=="yes":
				index=get_player_index_from(name)
				send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "eml", "Enter new email")
	if parsed[0]=="eventschoose":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			if parsed[1]=="current":
				m=server_menu()
				m.intro="event info"
				m.initial_packet="eventinfo"
				m.add("event name: "+get_task_name(),"name",False)
				m.add("event description: "+get_task_description(),"description",False)
				m.add("Amount of event points you got from this event: "+str(g.players[index].currenteventpoint),"point",False)
				m.add("Amount of times you got event points from this event: "+str(g.players[index].task_data[g.task]),"point2",False)
				m.add("amount of times you need to get event points to complete this event, "+str(get_task_complete_need()),"complete",False)
				if not g.players[index].is_completed_task(): m.add("You have not completed this event","complete",False)
				if g.players[index].is_completed_task(): m.add("You have completed this event","complete",False)
				if g.task==0 and g.freedomsurvivor!="":
					m.add("player selected which should survive for 10 minutes: "+g.freedomsurvivor,"survivor",False)
					m.add("time left for this player: "+str((10-survivestage))+" minutes","stage",False)
				
				m.send(e.peer_id)
			if parsed[1]=="viewscoreboard2":
				m = server_menu()
				m.intro = "scores menu"
				m.initial_packet = "scrsend"

				chars = find_directories("chars")
				scores_dict = {}

				for char in chars:
							score = file_get_contents(f"chars/{char}/currenteventpoint.usr")
							try: scores_dict[char] = int(score)
							except: pass

				sorted_scores = sorted(scores_dict.items(), key=lambda x: x[1], reverse=True)

				pos = 1
				playerse = my_list()


				for char, score in sorted_scores:
							if char not in playerse:
										playerse.append(char)
										if int(score)<=0: continue
										m.add(f"{pos}. {char}, event point {score}", char,False)
										pos += 1
				if len(m.menuids)==0: m.add("no scores available","noscore",False)
				m.send(e.peer_id)


			if parsed[1]=="event_store":
				g.n.send_reliable(e.peer_id,"echo event_store2",0)


			if parsed[1]=="eventpoint": g.n.send_reliable(e.peer_id,"you have "+str(g.players[index].eventpoint)+" event points",0); g.players[index].prevmenu(); return
			if parsed[1]=="token":
				if 1:
					if file_exists("chars/"+g.players[index].name+"/todaygift.usr")==True:
						now=datetime.now()
						target_time = datetime(now.year, now.month, now.day, 23, 0, 0)
						time_difference = target_time - now
						hours = time_difference.seconds // 3600
						minutes = (time_difference.seconds % 3600) // 60
						seconds = time_difference.seconds % 60
						g.n.send_reliable(e.peer_id,"You already got your daily zero tokens today, after "+str(hours)+" hours, "+str(minutes)+" minutes, "+str(seconds)+" seconds, try again.",0)
						g.players[index].prevmenu()
						return
					f=open("chars/"+g.players[index].name+"/todaygift.usr","w")
					f.close()
					amount=random(1,5)
					g.players[index].zhtoken+=amount
					g.n.send_reliable(e.peer_id,"You got "+str(amount)+" zero tokens",0)
					g.players[index].playsound("coin")
					g.players[index].prevmenu()
	if parsed[0]=="langoption" and len(parsed)>1:
		index=get_player_index(e.peer_id)
		if index>-1:
			if parsed[1]=="lang":
				send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "langcreate", "Please input language name")
			if parsed[1]=="help":
				m=server_menu()
				m.initial_packet="langhelp"
				m.intro="Use up and down arrows to read help, escape to go back"
				helptext='''use this syntax on the language
translate a static string
hello=merhaba
use substr keyword after the translation if you want to translate a string that is not static
example
came online=çevrimiçi oldu=substr
here, since the player name is before the string "came online", we added =substr so it translates came online even if it is not the whole text. If you do not add =substr, it would only work if the string is exactly "came online" without player name.'''
				parts=helptext.split("\n")
				for item in parts: m.add(item,"dummy",False)
				m.send(e.peer_id)
			if parsed[1]=="langmanage":
				m=server_menu()
				m.intro="Select language to manage"
				m.initial_packet="langmanageoption"
				for key in languages.keys():
					if g.players[index].dev or g.players[index].is_admin()==True or languages[key]["owner"]==g.players[index].name or g.players[index].name in languages[key]["contributors"]: m .add(key,key)
				m.send(e.peer_id)
			if parsed[1]=="switch":
				m=server_menu()
				m.intro="Select language to switch"
				m.initial_packet="langswitchoption"
				for key in languages.keys():
					if languages[key]["released"]==True:
						if languages[key]["official"]: m .add(key+", official, created by "+languages[key]["owner"]+", "+get_language_used_count(key)+" players are using it, has "+str(len(languages[key]["contributors"]))+" contributors, "+get_file_size("lang/"+key+".lng"),key)
				m.add("unofficial languages","unofficial")
				m.send(e.peer_id)

	if parsed[0]=="friendstats":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			pname=parsed[1]
			if 1:
				m=server_menu()
				m.intro="character stats menu."
				m.initial_packet="stats"
				try: m.add("current character, "+pickle.loads(file_get_contents("chars/"+pname+"/current_char.usr","rb"))+"","test123",False)
				except: pass
				m.add("Gender, "+file_get_contents("chars/"+pname+"/gender.usr")+"","test123",False)

				m.add("Score point, "+str(file_get_contents("chars/"+pname+"/scorepoint.usr"))+"","lolllll",False)
				m.add("Score Rank, "+file_get_contents("chars/"+pname+"/scorerank.usr")+"","lolasdlasdl",False)
				m.add("bot kills, "+str(file_get_contents("chars/"+pname+"/botkills.usr")),"kills",False)
				m.add("bot deaths, "+str(file_get_contents("chars/"+pname+"/botdeaths.usr")),"deaths",False)
				m.add("player kills, "+str(file_get_contents("chars/"+pname+"/playerkills.usr")),"kills2",False)
				m.add("player deaths, "+str(file_get_contents("chars/"+pname+"/playerdeaths.usr")),"deaths2",False)
				m.add("amount of headshots made, "+str(file_get_contents("chars/"+pname+"/headshots.usr")),"head")
				m.add("amount of headshots got, "+str(file_get_contents("chars/"+pname+"/headhits.usr")),"head")
				m.add("amount of legshots made, "+str(file_get_contents("chars/"+pname+"/legshots.usr")),"leg")
				m.add("amount of legshots got, "+str(file_get_contents("chars/"+pname+"/leghits.usr")),"leg")
				m.add("This player is using the language "+file_get_contents("chars/"+pname+"/lang.usr"),"lang",False)

#					m.add("zero token amount, "+str(g.players[ind].zhtoken)+"","test123",False)
				m.add("Time elapsed since this account is created: "+get_datetime_difference(file_get_contents("chars/"+pname+"/createdate.usr"))+".","elapsed",False)
				langchan=file_get_contents("chars/"+pname+"/langchan.usr")
				if langchan=="disable":
					m.add("Chat language, disabled.","a",False)

				else:
					m.add("Chat language, "+langchan+"","a",False)

				m.send(e.peer_id)
	if parsed[0]=="handselect":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			if parsed[1]=="left":
				parsed[1]=g.players[index].drawweapon
				if g.players[index].weapon==parsed[1]: return
				g.players[index].weapon=parsed[1]
				g.n.send_reliable(e.peer_id,"draw "+parsed[1],0)
				if g.players[index].weapon2==parsed[1]:
					g.players[index].weapon2="feet"
					g.players[index].get_weapon_properties(g.players[index].weapon2)
					g.n.send_reliable(e.peer_id,"draw2silent feet",0)

			if parsed[1]=="right":
				parsed[1]=g.players[index].drawweapon
				if g.players[index].weapon2==parsed[1]: return
				g.players[index].weapon2=parsed[1]
				g.n.send_reliable(e.peer_id,"draw2 "+parsed[1],0)
				if g.players[index].weapon==parsed[1]:
					g.players[index].weapon="punch"
					g.players[index].get_weapon_properties(g.players[index].weapon)
					g.n.send_reliable(e.peer_id,"drawsilent punch",0)

	if parsed[0]=="gamemenuopt":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			pname=g.players[index].name
			if parsed[1]=="viewscoreboard":
				m = server_menu()
				m.intro = "scores menu"
				m.initial_packet = "scrsend"

				chars = find_directories("chars")
				scores_dict = {}

				for char in chars:
							score = file_get_contents(f"chars/{char}/scorepoint.usr")
							scores_dict[char] = int(score)

				sorted_scores = sorted(scores_dict.items(), key=lambda x: x[1], reverse=True)

				pos = 1
				playerse = my_list()


				for char, score in sorted_scores:
							if char not in playerse:
										playerse.append(char)
										if int(score)<=0: continue
										rank=file_get_contents("chars/"+char+"/scorerank.usr")
										character=file_get_contents("chars/"+char+"/current_char.usr","rb")
										if character!=b"": character=pickle.loads(character)
										if character is None or character=="": character="tristan"
										if character is None or character=="default": character="tristan"

										if rank!="":
											m.add(f"{char}, {pos}, score point {score}, score rank {rank}, character {character}", char,False)
										else: m.add(f"{pos}. {char}, score point {score}, character {character}", char,False)
										pos += 1
				if len(m.menuids)==0: m.add("no scores available","noscore",False)
				m.send(e.peer_id)
			if parsed[1]=="free" and send_yesno_question(g.players[index].peer_id,"Are you sure you want to return to lobby? You will lose all the items you got in this map.")=="yes":
				index=g.get_player_index_from(pname)
				if g.players[index].cannotexit: g.n.send_reliable(g.players[index].peer_id,"You have to wait 1 minute after getting hit to exit the freedom fight map",0); return
				if g.players[index].near: g.n.send_reliable(g.players[index].peer_id,"You cannot exit the map because someone near you",0); return
				move_player(index,5,0,0,"lobby")
				g.players[index].freedomhelicopter=False
				j=g.players[index]
				item_map={}
				for item in g.dontlose:
					if j is not None and j.get_item_count(item)>0: item_map[item]=j.get_item_count(item)
				try: j.inv=dict()
				except: pass
				for item in item_map.keys():
					if j is not None: j.give(item,item_map[item])

				g.players[index].matchmode=""
			try: name=g.players[index].name
			except: pass
			if parsed[1]=="cancel" and send_yesno_question(g.players[index].peer_id,"Are you sure you want to cancel this match?")=="yes":
				index=get_player_index_from(name)
				for m in g.matches:
					if m.owner==g.players[index].name: 
						if m.starting:
							g.n.send_reliable(e.peer_id,"You cannot cancel a starting match",0); return
						m.send("play_s misc220.ogg",0)
						m.send("Match canceled by "+g.players[index].name+"!",2)
						m.cancel()
						g.players[index].joinedmatch=""
						g.players[index].matchteam=""
			if parsed[1]=="suggest":
				if g.players[index].suggesttimer.elapsed>=60000:
					g.players[index].suggesttimer.restart()
					send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "suggestsomething", "write your text here.")
				else:
					g.n.send_reliable(g.players[index].peer_id,"You can do this every 1 minute.",0)
					g.players[index].prevmenu()
					return

			if parsed[1]=="adminmenu":
				if g.players[index].is_admin()==True or g.players[index].dev==True or g.players[index].moderator==True:
					m=server_menu()
					m.intro="Select an option"
					m.initial_packet="adminlog"
					m.add("Copy what commands used, system notification, reports, etc","log2")
					m.add("check what commands used, system notification, reports, etc","log")
					m.add("view suggestions","suggestion")
					if g.players[index].is_admin()==True or g.players[index].dev==True:
						m.add("View Admin Help","adminhelp")
					m.add("View moderator Help","moderatorhelp")

					if g.players[index].is_admin()==True or g.players[index].builder==True or g.players[index].dev==True:
						m.add("View builder Help","builderhelp")

					if g.players[index].is_admin()==True or g.players[index].dev==True:
						m.add("Data Editor - edit game balance configs live","dataeditor")

					m.send(e.peer_id)
			if parsed[1]=="security":
				if g.players[index].map=="jail": g.n.send_reliable(g.players[index].peer_id,"you  are jailed, so you can not perform this process",0); return
				m=server_menu()
				m.intro="Select an option"
				m.initial_packet="securitychoose"
				m.add("Change password","passwd")
				m.add("Change email address","eml")
				m.add("rename your character, requires 150 zero tokens","rename")
				if g.players[index].status=="":
					m.add("Set a status message","setstatus")
				if g.players[index].status!="":
					m.add("change your status message","setstatus")
					m.add("clear your status","clearstatus")
				m.add("Rename history","rhist")
				m.add("View computers you logged into the game from, and block their accesses","compid")
				m.add("Delete your account","delete")
				m.send(e.peer_id)
			if parsed[1]=="motor":
				m=server_menu()
				m.intro="Your motors: "
				m.initial_packet="motor"
				for motor in g.motors:
					if motor.map==g.players[index].map and motor.owner==g.players[index].name:
						m.add("Your motor at "+str(round(motor.x))+", "+str(round(motor.y))+", "+str(round(motor.z)),"motor",False)
				for item in g.players[index].motorhistory.split("\n"): m.add(item,item,False)
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"You have no motors in this map and you have no motors destroyed before",0); g.players[index].prevmenu(); return
				m.send(e.peer_id)
			if parsed[1]=="bike":
				m=server_menu()
				m.intro="Your bikes: "
				m.initial_packet="bike"
				for b in g.bikes:
					if b.map==g.players[index].map and b.owner==g.players[index].name:
						m.add("Your bike at "+str(round(b.x))+", "+str(round(b.y))+", "+str(round(b.z)),"bike",False)
				m.send(e.peer_id)

			if parsed[1]=="events":
				m=server_menu()
				m.intro="events"
				m.initial_packet="eventschoose"
				m.add("current event is "+get_task_name()+", will end after "+get_task_end_time(),"current")
				m.add("view event point","eventpoint")
				m.add("Event store, Spend the event points you have.","event_store")

				m.add("view current event scoreboard","viewscoreboard2")

				m.send(e.peer_id)
			if parsed[1]=="latest":
				if not file_exists("changes.txt") or file_get_contents("changes.txt")=="":
					send_reliable(e.peer_id, "no Latest Additions", 0)
					return
				r=open("changes.txt", "r")
				changes=string_split(r.read(), "\n", True)
				r.close()
				if len(changes)<=0:
					send_reliable(e.peer_id, "no Latest Additions", 0)
					return
				m=server_menu()
				m.intro="Latest Additions."
				m.initial_packet="latest"
				for i in range(len(changes)):
					m.add(string_replace(changes[i], ":", ".", True), string_replace(changes[i], ":", ".", True),False)
				m.send(e.peer_id)
			if parsed[1]=="rules":
				if not file_exists("rules.txt"):
					send_reliable(e.peer_id, "no rules.", 0)
					return
				r=open("rules.txt", "rb")
				changes=string_split(r.read().decode("utf-8",errors="ignore"), "\n", True)
				r.close()
				if len(changes)<=0:
					send_reliable(e.peer_id, "no rules.", 0)
					return
				m=server_menu()
				m.intro="Rules."
				m.initial_packet="latest"
				for i in range(len(changes)):
					m.add(string_replace(changes[i], ":", ".", True), string_replace(changes[i], ":", ".", True),False)
				m.send(e.peer_id)

			if parsed[1]=="readme":
				if not file_exists("readme.txt") or file_get_contents("readme.txt")=="":
					send_reliable(e.peer_id, "The file could be not found.", 0)
					return
				r=open("readme.txt", "r")
				changes=string_split(r.read(), "\n", True)
				r.close()
				if len(changes)<=0:
					send_reliable(e.peer_id, "The file could be not found.", 0)
					return
				m=server_menu()
				m.intro="readme"
				m.initial_packet="latest"
				for i in range(len(changes)):
					m.add(string_replace(changes[i], ":", ".", True), string_replace(changes[i], ":", ".", True),False)
				m.send(e.peer_id)

			if parsed[1]=="timed":
				m=server_menu()
				m.intro="Timed item information menu"
				m.initial_packet="timed"
				for i in g.timeditems:
					if i.owner==g.players[index].name:
						m.add("The item "+i.itemname+" will expire after "+str(ms_to_readable_time(i.duration-i.timer.elapsed))+".",i)
				if g.players[index].backpacks_level!=0:
					m.add("backpacks level "+str(g.players[index].backpacks_level)+", it will expire after "+ms_to_readable_time(604800000-g.players[index].backpacktimer.elapsed),"backpack",False)
				if len(m.menuids)==0:
					g.n.send_reliable(e.peer_id,"You have no timed items.",0)
					g.players[index].prevmenu()
				else: m.send(e.peer_id)
			if parsed[1]=="communityinfo":
				m=server_menu()
				m.intro="community information. There are "+str(len(g.communitys))+" communitys."
				m.initial_packet="communityinfoselect"
				for grp in g.communitys: m.add("Name: "+grp.name+", owner: "+grp.owner+", member count: "+str(len(grp.members))+"",grp.name)
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"No communitys",0); g.players[index].prevmenu(); return
				else: m.send(e.peer_id)
			if parsed[1]=="community":
				m=server_menu()
				m.intro="Select an option"
				m.initial_packet="community2"
				if g.players[index].community=="":
					m.add("create community","create")
					m.add("View community invitations","invitation")
				else:
					grp=get_community(g.players[index].community)
					m.add("community members","members")
					m.add("community admins","admins")
					m.add("view announcement","viewannouncement")
					if grp.owner==g.players[index].name or g.players[index].name in grp.admins:

						m.add("view community action history","action")
						m.add("clear community action history","action2")
						m.add("kick a member","kick")
						m.add("invite a player to this community","invite")
						m.add("remove invitation of a player to this community","invite2")
						m.add("View community join requests","request")
					if grp.owner==g.players[index].name:
						m.add("make a member the community administrator","makeadmin")
						m.add("remove a member's community administrator role","removeadmin")
						m.add("change community owner","owner")
						m.add("rename this community","rename")
						m.add("publish announcement","announce")
						m.add("delete this community","delete")
					if grp.owner!=g.players[index].name and g.players[index].name not in grp.admins: m.add("leave this community","leave")
					if grp.owner!=g.players[index].name and g.players[index].name in grp.admins: m.add("resign from administrating this community","resign")
				m.send(e.peer_id)

			if parsed[1]=="groupinfo2":
				m=server_menu()
				m.intro="Group base destroy history"
				m.initial_packet="groupinfoselect2"
				lines=file_get_contents("grouphistory.txt").split("\n")[::-1]
				if len(lines)==0: g.n.send_reliable(e.peer_id,"history empty",0); g.players[index].prevmenu(); return
				for line in lines: m.add(line,line,False)
				m.send(e.peer_id)
			if parsed[1]=="groupinfo":
				m=server_menu()
				m.intro="Group information. There are "+str(len(g.groups))+" groups."
				m.initial_packet="groupinfoselect"
				sorted_groups = sorted(g.groups, key=lambda grp: grp.kills, reverse=True)
				for grp in sorted_groups: m.add("Name: "+grp.name+", base count: "+str(get_base_count(grp.name))+", owner: "+grp.owner+", member count: "+str(len(grp.members))+", kills: "+str(grp.kills)+", deaths: "+str(grp.deaths),grp.name)
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"No groups",0); g.players[index].prevmenu(); return
				else: m.send(e.peer_id)
			if parsed[1]=="group":
				m=server_menu()
				m.intro="Select an option"
				m.initial_packet="group2"
				if g.players[index].group=="":
					m.add("create group","create")
					m.add("View group invitations","invitation")
				else:
					grp=get_group(g.players[index].group)
					m.add("group members","members")
					m.add("group admins","admins")
					m.add("donate to this group","donate")
					m.add("view announcement","viewannouncement")
					m.add("view donation history","donate2")
					if grp.owner==g.players[index].name or g.players[index].name in grp.admins:

						m.add("view group action history","action")
						m.add("view group base chest log","log")
						m.add("kick a member","kick")
						m.add("put a base here","putbase")
						m.add("invite a player to this group","invite")
						m.add("remove invitation of a player to this group","invite2")
						m.add("View group join requests","request")
						if grp.freedomhit==1: m.add("Disable members' hitting each other in freedom fight map","freedom")
						if grp.freedomhit==0: m.add("Enable members' hitting each other in freedom fight map","freedom")
						m.add("view zero token amount donated to this group","donatetoken")
					if grp.owner==g.players[index].name:
						m.add("make a member the group administrator","makeadmin")
						m.add("remove a member's group administrator role","removeadmin")
						m.add("change group owner","owner")
						m.add("rename this group","rename")
						m.add("publish announcement","announce")
						m.add("get zero tokens from donated tokens","donate3")
						m.add("delete this group","delete")
						m.add("clear group action history","action2")
						m.add("clear group base chest log","log2")
					if grp.owner!=g.players[index].name and g.players[index].name not in grp.admins: m.add("leave this group","leave")
					if grp.owner!=g.players[index].name and g.players[index].name in grp.admins: m.add("resign from administrating this group","resign")
					if grp.owner==g.players[index].name or g.players[index].name in grp.admins:
						m.add("View group base info","base")
				m.send(e.peer_id)

			if parsed[1]=="friend":
				m=server_menu()
				m.intro="Select an option"
				m.initial_packet="friend2"
				m.add("add friend","friendadd")
				m.add("Pending friend requests sent to you","friendrequests")
				m.add("Pending friend requests you sent","friendrequests2")
				m.add("Remove friend","friendremove")
				m.add("clear friend list","friendclean")
				m.send(e.peer_id)
			if parsed[1]=="vote":
				m=server_menu()
				m.intro="Select an option"
				m.initial_packet="vote2"
				m.add("create poll","create")
				m.add("view polls","view")
				m.send(e.peer_id)
			if parsed[1]=="ticket":
				m=server_menu()
				m.intro="Select an option"
				m.initial_packet="ticket2"
				m.add("create ticket","ticketcreate")
				m.add("View tickets you've created","ticketview")
				if g.players[index].is_admin() or g.players[index].moderator==True:
					m.add("View tickets on server","serverview")
				m.send(e.peer_id)
			if parsed[1]=="status":
				m=server_menu()
				m.initial_packet="serverstatus"
				m.intro="server status"
				m.add("The server has been up for "+ms_to_readable_time(g.servertime.elapsed)+" without any shutdown","a",False)
				m.add("View penalyzed players","viewp")

				m.add("go back","back")
				m.send(e.peer_id)
			if parsed[1]=="staff":
				builders=my_list()
				admins=my_list()
				moderators=my_list()

				developers=my_list()
				chars=find_directories("chars")
				for i in range(len(chars)):
					cf="chars/"+chars[i]+"/"
					rs=chars[i]
					if file_exists(cf+"builder.usr"):
						builders.append(rs)
					if file_exists(cf+"admin.usr"):
						admins.append(rs)
					if file_exists(cf+"moderator.usr"):
						moderators.append(rs)

					if file_exists(cf+"developer.usr"):
						developers.append(rs)
				ret=""
				m=server_menu()
				m.initial_packet="staffmenu"
				m.intro="Staff list."
				if len(developers)>0:
					m.add("Developers: Has the ability to view or edit the game's code.", "test",False)
					m.add("\n"+convert_to_list(developers)+":", "test",False)
				elif len(developers)<=0:
					m.add("\nzero developers found:", "test",False)
					m.add("\n", "test",False)
				if len(admins)>0:
					m.add("\nAdministrators: resolving player issues, crafting maps, and other duties.", "test",False)
					m.add("\n"+convert_to_list(admins)+":", "test",False)
				elif len(admins)<=0:
					m.add("\nzero administrators found:", "test",False)
					m.add("", "test",False)
				if len(moderators)>0:
					m.add("\nModerators: Responsible for players, tickets, assisting administrators, and helping people in the game.", "test",False)
					m.add("\n"+convert_to_list(moderators)+":", "test",False)
				elif len(moderators)<=0:
					m.add("\nno zero moderator found:", "test",False)
					m.add("", "test",False)


				if len(builders)>0:
					m.add("\nBuilders: Capable of constructing maps and integrating them into the game.", "test",False)
					m.add("\n"+convert_to_list(builders)+".", "test",False)
				elif len(builders)<=0:
					m.add("\nzero builders found", "test",False)
				m.add("Go Back", "back")
				m.send(e.peer_id)

			if parsed[1]=="langg":
				m=server_menu()
				m.intro="languages menu"
				m.initial_packet="langoption"

				m.add("Create language","lang")
				for key in languages.keys():
					if g.players[index].dev or g.players[index].is_admin()==True or languages[key]["owner"]==g.players[index].name or g.players[index].name in languages[key]["contributors"]:
						m.add("Manage languages","langmanage"); break
				m.add("switch to a language","switch")
				m.add("View language syntax help","help")
				m.add("go back","back")
				m.send(e.peer_id)

			if parsed[1]=="nsetting":
				m=server_menu()
				m.intro="select an option"
				m.initial_packet="notifys"
				if g.players[index].mapmessage==0: m.add("enable receiving map messages","mapmessage")
				elif g.players[index].mapmessage==1: m.add("disable receiving map messages","mapmessage")
				if g.players[index].groupmessage==0: m.add("enable receiving group messages","groupmessage")
				elif g.players[index].groupmessage==1: m.add("disable receiving group messages","groupmessage")
				if g.players[index].groupinvitation==0: m.add("enable receiving group invitations","groupinvitation")
				elif g.players[index].groupinvitation==1: m.add("disable receiving group invitations","groupinvitation")

				if g.players[index].pmmessage==0: m.add("enable receiving private messages","pmmessage")
				elif g.players[index].pmmessage==1: m.add("disable receiving private messages","pmmessage")
				if g.players[index].voicemessage==0 and g.players[index].blockvoice3==0: m.add("enable hearing voice chat","voicemessage")
				elif g.players[index].voicemessage==1 and g.players[index].blockvoice3==0: m.add("disable hearing voice chat","voicemessage")
				if g.players[index].voicemessage2==0 and g.players[index].blockvoice3==0: m.add("enable hearing community voice chat","voicemessage2")
				elif g.players[index].voicemessage2==1 and g.players[index].blockvoice3==0: m.add("disable hearing community voice chat","voicemessage2")

				if g.players[index].friendmessage==0: m.add("enable receiving friend request from players","friendmessage")
				elif g.players[index].friendmessage==1: m.add("disable receiving friend request from players","friendmessage")
				if g.players[index].matchmessage==0: m.add("enable receiving new match notification","matchmessage")
				elif g.players[index].matchmessage==1: m.add("disable receiving new match notification","matchmessage")
				if g.players[index].teammessage==0: m.add("enable receiving team messages in matches","teammessage")
				elif g.players[index].teammessage==1: m.add("disable receiving team messages in matches","teammessage")
				if g.players[index].friendonlinemessage==0: m.add("enable online/offline messages when your friends enter/exit to the game","friendonlinemessage")
				elif g.players[index].friendonlinemessage==1: m.add("disable online/offline messages when your friends enter/exit to the game","friendonlinemessage")
				if g.players[index].ticketmail==0: m.add("enable ticket update mails","ticketmail")
				elif g.players[index].ticketmail==1: m.add("disable ticket update mails","ticketmail")
				if g.players[index].matchinvite==0: m.add("enable receiving match invitations","matchinvite")
				elif g.players[index].matchinvite==1: m.add("disable receiving match invitations","matchinvite")

				if g.players[index].communitymessage==0: m.add("enable receiving community messages","communitymessage")
				elif g.players[index].communitymessage==1: m.add("disable receiving community messages","communitymessage")

				if g.players[index].mapsound==0: m.add("enable sound when someone enters and exits your map","mapsound")
				elif g.players[index].mapsound==1: m.add("disable sound when someone enters and exits your map","mapsound")
				if g.players[index].eventalerts==0: m.add("enable event notifications","eventalerts")
				elif g.players[index].eventalerts==1: m.add("disable event notifications","eventalerts")

				if g.players[index].tokentransfer==0: m.add("enable receiving zero token transfers","tokentransfer")
				if g.players[index].tokentransfer==1: m.add("disable receiving zero token transfers","tokentransfer")
				if g.players[index].authreq==0: m.add("enable authorization requirement when logging in from different computers","authreq")
				elif g.players[index].authreq==1: m.add("disable authorization requirement when logging in from different computers","authreq")
				if g.players[index].votenotify==0: m.add("enable poll notifications","votenotify")
				elif g.players[index].votenotify==1: m.add("disable poll notifications","votenotify")

				if g.players[index].istyping==0: m.add("enable typing notifications","istyping")
				elif g.players[index].istyping==1: m.add("disable typing notifications","istyping")

				if g.players[index].chestpickupnotify==0: m.add("enable chest pickup item announcements","chestpickupnotify")
				elif g.players[index].chestpickupnotify==1: m.add("disable chest pickup item announcements","chestpickupnotify")

				m.send(e.peer_id)




			if parsed[1]=="char":
				m=server_menu()
				m.intro="Select character to switch"
				m.initial_packet="char"
				for char in g.players[index].bought_chars: m.add(char,char)
				m.send(e.peer_id)
			if parsed[1]=="stats":
				m=server_menu()
				m.intro="character stats menu."
				m.initial_packet="stats"
				m.add("current character, "+g.players[index].current_char+"","test123",False)
				m.add("Your gender, "+g.players[index].gender+"","test123",False)
				if g.players[index].paid: m.add("you are paid account","paid",False)
				if not g.players[index].paid: m.add("you are free account","paid",False)
				if g.players[index].corpse_bomb==1: m.add("corpse bomb on","corpse",False)
				if g.players[index].corpse_bomb==0: m.add("corpse bomb off","corpse",False)
				if g.players[index].paid: m.add("Time left for paid account expiry: "+ms_to_readable_time2(int(file_get_contents("chars/"+g.players[index].name+"/paidtime.usr")) + g.players[index].paidmonths - tm.time())+".","elapsed",False)

				if g.players[index].backpacks_level!=0:
					m.add("this player has backpacks level "+str(g.players[index].backpacks_level)+"","backpacks",False)

				m.add("Score point, "+str(g.players[index].scorepoint)+"","lolllll",False)
				m.add("Score Rank, "+g.players[index].scorerank+"","lolasdlasdl",False)
				m.add("bot kills, "+str(g.players[index].botkills),"kills",False)
				m.add("bot deaths, "+str(g.players[index].botdeaths),"deaths",False)
				m.add("player kills, "+str(g.players[index].playerkills),"kills2",False)
				m.add("player deaths, "+str(g.players[index].playerdeaths),"deaths2",False)
				m.add("amount of headshots made, "+str(g.players[index].headshots),"head")
				m.add("amount of headshots got, "+str(g.players[index].headhits),"head")
				m.add("amount of legshots made, "+str(g.players[index].legshots),"leg")
				m.add("amount of legshots got, "+str(g.players[index].leghits),"leg")

				m.add("zero token amount, "+str(g.players[index].zhtoken)+"","test123",False)
				if g.players[index].adrenaline:
					m.add("adrenaline shot on, will expire after "+ms_to_readable_time(120000-g.players[index].adrenalinetimer.elapsed),"adr",False)
				if g.players[index].jammer:
					m.add("jammer on, will expire after "+ms_to_readable_time(120000-g.players[index].jammertimer.elapsed),"adr",False)

				m.send(e.peer_id)

			elif parsed[1]=="setting": g.n.send_reliable(e.peer_id,"opensettings",0)
			elif parsed[1]=="store":
				m=server_menu()
				m.intro="Select category"
				g.players[index].playsound("storeenter")
				m.initial_packet="store2"
				cat=[]
				for item in store_data:
					if item["category"] not in cat: cat.append(item["category"])
				for elem in cat: m.add(elem,elem)
				m.add("View packs you bought from the shop and open them","storeview")
				if not g.players[index].ios: m.add("Go to online store website to buy zero token packs, paid account, event points, etc","onlinestore")
				if not g.players[index].ios: m.add("Copy the link of the online store web page to buy zero token packs, paid account, event points, etc","copyonlinestore")
				m.send(e.peer_id)
	if(parsed[0]=="addfriendchoose"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			m=server_menu()
			m.intro="Select what you would like to do."
			m.initial_packet="addfriendchoose2"
			g.players[index].friendmanage=parsed[1]
			m.add("accept","a")
			m.add("refuse","r")
			m.send(e.peer_id)
	if(parsed[0]=="editmap"):
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if 1:
				if 1:
					if 1:
						if(g.players[index].is_builder()):
						
							maptext=string_replace(e.message,"editmap ","",False)

							f=open("maps/"+g.players[index].map+".map","w")
							f.write(maptext)
							f.close()
							update_map(g.players[index].map)
							g.n.send_reliable(g.players[index].peer_id,"Done",0)
							
						

	if(parsed[0]=="addfriendchoose2"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			if parsed[1]=="a": g.n.send_reliable(e.peer_id,"echo addfriend2 "+g.players[index].friendmanage,0)
			if parsed[1]=="r": g.n.send_reliable(e.peer_id,"echo addfriend3 "+g.players[index].friendmanage,0)
	if(parsed[0]=="addfriendchoose3"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			g.n.send_reliable(e.peer_id,"echo addfriend4 "+parsed[1],0)
	if(parsed[0]=="addfriend"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			i=get_player_index_from(parsed[1])
			if i==-1: g.n.send_reliable(e.peer_id,"Error, player not found.",0); g.players[index].prevmenu(); return
			if g.players[index].friendtimer.elapsed<20000:
				g.n.send_reliable(e.peer_id,"Error, you can send friend request every 20 seconds.",0)
				g.players[index].prevmenu(); return
			friendcount=0
			for p in g.players:
				if g.players[index].name in p.pendingfriendlist and p.name != g.players[index].name: friendcount+=1
			if friendcount>=3:
				g.n.send_reliable(e.peer_id,"Error, you already sent friend request to 3 players which are pending, please wait for them to be accepted or refused before you can send more requests.",0); return
			g.players[index].friendtimer.restart()
			if g.players[index].friendmessage==0: g.n.send_reliable(e.peer_id,"Error, you can't send friend requests to people because you turned of receiving friend requests.",0); g.players[index].prevmenu(); return
			if g.players[i].friendmessage==0: g.n.send_reliable(e.peer_id,"Error, you can't send friend request to this player because they turned of receiving friend requests.",0); g.players[index].prevmenu(); return
			if g.players[index].name in g.players[i].pendingfriendlist:
				g.n.send_reliable(e.peer_id,"You've already sent friend request to this player.",0)
				g.players[index].prevmenu() 
				return
			if g.players[index].name in g.players[i].friendlist:
				g.n.send_reliable(e.peer_id,"You've already added this player as friend.",0)
				g.players[index].prevmenu() 
				return
			if g.players[i].name in g.players[index].pendingfriendlist:
				g.n.send_reliable(e.peer_id,"This player already sent friend request to you",0)
				g.players[index].prevmenu() 
				return

			g.players[i].pendingfriendlist.append(g.players[index].name)

			g.n.send_reliable(e.peer_id,"Done, friend request sent successfully.",0)
			g.players[index].prevmenu()
			g.n.send_reliable(g.players[i].peer_id,"play_s misc10.ogg",0)
			g.n.send_reliable(g.players[i].peer_id,"friend "+g.players[index].name+" wants to add you as friend!",0)
	if(parsed[0]=="removefriend"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			i=get_player_index_from(parsed[1])
			name=g.players[index].name
			name2=parsed[1]
			if  send_yesno_question(g.players[index].peer_id,"Are you sure you want to remove this friend?")!="yes": return
			index=get_player_index_from(name)
			i=get_player_index_from(name2)
			try:
				g.players[index].friendlist.remove(parsed[1])
				if i>-1: g.players[i].friendlist.remove(g.players[index].name)
				else:
					flist=pickle.loads(file_get_contents("chars/"+parsed[1]+"/friendlist.usr","rb"))
					flist.remove(g.players[index].name)
					file_put_contents("chars/"+parsed[1]+"/friendlist.usr",pickle.dumps(flist),"wb")

			except: pass
			g.n.send_reliable(g.players[index].peer_id,"Done, friend removed successfully.",0)
			g.players[index].prevmenu()
			if i>-1: g.n.send_reliable(g.players[i].peer_id,"play_s misc10.ogg",0)
			if i>-1: g.n.send_reliable(g.players[i].peer_id,"friend "+g.players[index].name+" removed you from their friend list!",0)

	if(parsed[0]=="addfriend2"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			i=get_player_index_from(parsed[1])
			try: g.players[index].pendingfriendlist.remove(parsed[1])
			except: pass
			if i>-1: g.players[i].friendlist.append(g.players[index].name)
			else:
				try:
					flist=pickle.loads(file_get_contents("chars/"+parsed[1]+"/friendlist.usr","rb"))
					flist.append(g.players[index].name)
					file_put_contents("chars/"+parsed[1]+"/friendlist.usr",pickle.dumps(flist),"wb")
				except: return
			g.players[index].friendlist.append(parsed[1])
			g.n.send_reliable(e.peer_id,"Done, friend request accepted successfully.",0)
			if i>-1: g.n.send_reliable(g.players[i].peer_id,"friend "+g.players[index].name+" accepted your friend request!",0)
			if i>-1: g.n.send_reliable(g.players[i].peer_id,"play_s misc10.ogg",0)
	if(parsed[0]=="addfriend4"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			i=get_player_index_from(parsed[1])
			if i>-1:
				try: g.players[i].pendingfriendlist.remove(g.players[index].name)
				except: pass
			else:
				flist=pickle.loads(file_get_contents("chars/"+parsed[1]+"/pendingfriendlist.usr","rb"))
				flist.remove(g.players[index].name)
				file_put_contents("chars/"+parsed[1]+"/pendingfriendlist.usr",pickle.dumps(flist),"wb")
			g.n.send_reliable(e.peer_id,"Done, friend request removed successfully.",0)
			if i>-1: g.n.send_reliable(g.players[i].peer_id,""+g.players[index].name+"removed their friend request to you!",0)
			if i>-1: g.n.send_reliable(g.players[i].peer_id,"play_s misc10.ogg",0)

	if(parsed[0]=="addfriend3"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			i=get_player_index_from(parsed[1])
			try:
				g.players[index].pendingfriendlist.remove(parsed[1])
			except: pass
			g.n.send_reliable(e.peer_id,"Done, friend request refused successfully.",0)
			if i>-1: g.n.send_reliable(g.players[i].peer_id,"friend "+g.players[index].name+" refused your friend request!",0)
			if i>-1: g.n.send_reliable(g.players[i].peer_id,"play_s misc10.ogg",0)

	if(parsed[0]=="char"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			if g.players[index].map!="lobby" and not g.players[index].map.startswith("match"):
				g.n.send_reliable(e.peer_id,"You can only change characters in lobby or in the waiting area of a match!",0)
				g.players[index].prevmenu(); return
			if g.players[index].current_char==parsed[1]:
				g.n.send_reliable(g.players[index].peer_id,"you are already using the "+parsed[1]+" character",0)
				g.players[index].prevmenu()
				return
			if parsed[1] not in g.players[index].bought_chars:
				f=open("razeon.txt","a")
				f.write(g.players[index].name+", "+parsed[1])
				f.close()
			g.players[index].current_char=parsed[1]
			g.players[index].get_char_properties()
			send_reliable(g.players[index].peer_id,"play_s misc11.ogg",0)
			g.n.send_reliable(e.peer_id,"Done, switched to the "+parsed[1]+" character.",0)
			g.players[index].prevmenu()
	if(parsed[0]=="ammocheck"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			index=g.players[index]
			if index.specplayer!="": index=getpc(index.specplayer)
			if index is None: return
			try:
				gp=guns.index(index.weapon)
			except:
			
				g.n.send_reliable(e.peer_id,"this weapon "+index.weapon+" does not take ammo",0)
				return
				

			ammoamount=index.ammocheck(index.weapon)
			ra=index.get_item_count(get_ammotype(index.weapon)+"")
			g.n.send_reliable(e.peer_id,("no ammo loaded for " + index.weapon + ". and also you have " + str(ra) + " " + get_ammotype(index.weapon) + " ammo" if ammoamount <= 0 else str(ammoamount) + " ammo for " + index.weapon + " loaded, and also you have " + str(ra) + " " + get_ammotype(index.weapon) + " ammo"),0)
				
			
	if(parsed[0]=="ammocheck2"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			index=g.players[index]
			if index.specplayer!="": index=getpc(index.specplayer)
			if index is None: return
			try:
				gp=guns.index(index.weapon2)
			except:
			
				g.n.send_reliable(e.peer_id,"this weapon "+index.weapon2+" does not take ammo",0)
				return
				

			ammoamount=index.ammocheck(index.weapon2)
			ra=index.get_item_count(get_ammotype(index.weapon2)+"")
			g.n.send_reliable(e.peer_id,("no ammo loaded for " + index.weapon2 + ". and also you have " + str(ra) + " " + get_ammotype(index.weapon2) + " ammo" if ammoamount <= 0 else str(ammoamount) + " ammo for " + index.weapon2 + " loaded, and also you have " + str(ra) + " " + get_ammotype(index.weapon2) + " ammo"),0)