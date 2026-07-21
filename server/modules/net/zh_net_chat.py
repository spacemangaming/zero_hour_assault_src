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

def handle_channel_1(e):
	global languages
	index = g.get_player_index(e.peer_id)
	if index > -1:
	
		parsed=string_split(e.message, " ",True)
		index=g.get_player_index(e.peer_id)
		if (index>-1):
		
			message=e.message
			if not g.players[index].disable_all_chat_check(): return
			if "/pm" not in e.message and not g.players[index].disable_public_chat_check(): return
			if (string_left(e.message,1)!="/"):
			
				if g.players[index].chattimer.elapsed<1000:
					g.n.send_reliable(g.players[index].peer_id,"wait one second!",0)
					return
				if(len(e.message)>2000):
				
					return
					
				if g.players[index].langchan=="disable":
					g.n.send_reliable(g.players[index].peer_id,"You cannot send messages because you have disabled chat. Please select a channel by pressing F11",0)
					return
				chatmessage=e.message
				chatmess=""
				if not g.players[index].paid: chatmess+=""+g.players[index].title+" "+g.players[index].scorerank+" "+g.players[index].name+" says: "+chatmessage
				if g.players[index].paid: chatmess+="* "+g.players[index].title+" "+g.players[index].scorerank+" "+g.players[index].name+" says: "+chatmessage
				g.players[index].chat(chatmess)
				g.players[index].chattimer.restart()
				return
				
			index=g.get_player_index(e.peer_id)
			if (index>-1):
			
				if parsed[0]!="/pm" and g.players[index].is_builder()==False and g.players[index].moderator==False and not g.players[index].dev and g.players[index].is_admin()==False: return
				if parsed[0]=="/accounts" and len(parsed)>1:
					if parsed[1]=="sado":
						adminsend(""+g.players[index].name+" checked "+parsed[1]+"'s all accounts")
						g.n.send_reliable(g.players[index].peer_id,"sado has the following accounts.\nsado\nthis player has total of 1accounts.",2)
						return
					if parsed[1]=="masterkiller":
						adminsend(""+g.players[index].name+" checked "+parsed[1]+"'s all accounts")

						g.n.send_reliable(g.players[index].peer_id,"masterkiller has the following accounts.\nmasterkiller\nthis player has total of 1accounts.",2)
						return

					if directory_exists("chars/"+parsed[1]+"")==False: g.n.send_reliable(g.players[index].peer_id,"no such account exists",2); return
					final=""+parsed[1]+" has the following accounts.\n"
					accounts=0
					mainid=file_get_contents("chars/"+parsed[1]+"/compid.usr")
					c=find_directories("chars")
					for i in c:
						if file_get_contents("chars/"+i+"/compid.usr")==mainid:
							accounts+=1
							final+=""+i+"\n"
					final+="this player has total of "+str(accounts)+"accounts."
					g.n.send_reliable(e.peer_id, final, 2)
					adminsend(""+g.players[index].name+" checked "+parsed[1]+"'s all accounts")
				if parsed[0]=="/banned":
					compbanloop()
					if g.players[index].is_admin() or g.players[index].moderator==True:
						g.n.send_reliable(g.players[index].peer_id, get_comp_bans(), 0)
						adminsend(""+g.players[index].name+" checked banned list")
					else:
						g.n.send_reliable(g.players[index].peer_id, "you are not authorized to do this", 0)
				if parsed[0]=="/jails":
					s=""
					chars=find_directories("chars")
					for char in chars:
						if file_exists("chars/"+char+"/jailtime.usr"):
							try: time_elapsed=(tm.time()-int(file_get_contents("chars/"+char+"/jailtimestamp.usr")))*1000
							except: continue
							try: time_jailed=int(file_get_contents("chars/"+char+"/jailtime.usr"))
							except: continue
							time_left=time_jailed-time_elapsed
							if time_left>0:
								time_str=ms_to_readable_time(time_left)
								s+=char+" was jailed for "+file_get_contents("chars/"+char+"/jailreason.usr")+". They will be unjailed after "+time_str
					if s=="": s="no jailed player found"
					g.n.send_reliable(e.peer_id,s,2)
					adminsend(""+g.players[index].name+" checked jailed players list")
				if parsed[0]=="/jail" and len(parsed)>3:
					user=parsed[1]
					time=int(parsed[2])
					if time==0: time=100000000
					reason=e.message.replace(parsed[0]+" "+parsed[1]+" "+parsed[2]+" ","")
					ind=get_player_index_from(user)
					if ind>-1:
						g.players[ind].jailed=True
						g.players[ind].jailtimer.restart()
						g.players[ind].jailreason=reason
						g.players[ind].jailtime=time*60000
					file_put_contents("chars/"+user+"/jailtime.usr",str(time*60000))
					file_put_contents("chars/"+user+"/jailtimestamp.usr",str(round(tm.time())))
					file_put_contents("chars/"+user+"/jailreason.usr",reason)
					chars=find_directories("chars")
					for char in chars:
						if file_get_contents("chars/"+char+"/compid.usr")==file_get_contents("chars/"+user+"/compid.usr") and user!=char:
							file_put_contents("chars/"+char+"/jailtime.usr",str(time*60000))
							file_put_contents("chars/"+char+"/jailreason.usr",reason)
					if time!=100000000: adminsend(user+" has been jailed by "+g.players[index].name+" for the following reason: "+reason+". The time will end in "+str(time)+" minutes.")
					if time==100000000: adminsend(user+" has been jailed by "+g.players[index].name+" for the following reason: "+reason+".")
					g.n.send_reliable(e.peer_id,"done",0)
				if parsed[0]=="/unjail" and len(parsed)>1:
					user=parsed[1]
					if not file_exists("chars/"+user+"/jailtime.usr"): g.n.send_reliable(e.peer_id,"this player not jailed",0); return
					ind=get_player_index_from(user)
					if ind>-1:
						g.players[ind].jailed=False
						g.players[ind].jailtimer.restart()
						g.players[ind].jailreason=""
						g.players[ind].jailtime=0
					file_delete("chars/"+user+"/jailtime.usr")
					file_delete("chars/"+user+"/jailtimestamp.usr")
					file_delete("chars/"+user+"/jailreason.usr")
					chars=find_directories("chars")
					for char in chars:
						if file_get_contents("chars/"+char+"/compid.usr")==file_get_contents("chars/"+user+"/compid.usr") and user!=char:
							file_delete("chars/"+char+"/jailtime.usr")
							file_delete("chars/"+char+"/jailreason.usr")
							file_delete("chars/"+char+"/jailtimestamp.usr")
					adminsend(user+" has been unjailed by "+g.players[index].name+".")
					g.n.send_reliable(e.peer_id,"done",0)

				if parsed[0]=="/ban" and len(parsed)>3:
					if g.players[index].is_admin():
						if directory_exists("chars/"+parsed[1]+"")==False: g.n.send_reliable(g.players[index].peer_id,"no such account found",2); return

						ind2=get_player_index_from(parsed[1])
						if ind2>-1:
							success=comp_ban(ind2)
							if success==False:
								g.n.send_reliable(g.players[index].peer_id, "That player can not be banned.", 0)
							else:
								if int(parsed[2])!=0: adminsend(""+parsed[1]+" has been banned by "+g.players[index].name+": Reason: "+e.message.replace(parsed[0]+" "+parsed[1]+" "+parsed[2]+" ","")+": The time will end in "+str(convert_minutes_to_datetime_object(int(parsed[2])))+"")
								if int(parsed[2])==0: adminsend(""+parsed[1]+" has been permanently banned by "+g.players[index].name+": Reason: "+e.message.replace(parsed[0]+" "+parsed[1]+" "+parsed[2]+" ",""))
								if parsed[2]!="0": end_datetime=convert_minutes_to_datetime_object(int(parsed[2]))
								if parsed[2]=="0": end_datetime=convert_minutes_to_datetime_object(900000000); file_put_contents("chars/"+g.players[ind2].name+"/permaban.usr","")
								chars=find_directories("chars")
								for char in chars:
									if file_get_contents("chars/"+char+"/compid.usr")==file_get_contents("chars/"+g.players[ind2].name+"/compid.usr") and g.players[ind2].name!=char:
										file_put_contents("chars/"+char+"/banreason.usr",e.message.replace(parsed[0]+" "+parsed[1]+" "+parsed[2]+" ",""))
										file_put_contents("chars/"+char+"/banenddate.usr",pickle.dumps(end_datetime),"wb")
										if parsed[2]=="0": file_put_contents("chars/"+char+"/permaban.usr","")
								file_put_contents("chars/"+g.players[ind2].name+"/banreason.usr",e.message.replace(parsed[0]+" "+parsed[1]+" "+parsed[2]+" ",""))
								file_put_contents("chars/"+g.players[ind2].name+"/banenddate.usr",pickle.dumps(end_datetime),"wb")
								ban_mail(file_get_contents("chars/"+g.players[ind2].name+"/mail.usr"))
								compid=g.players[ind2].compid
								remove_from_server(ind2)
								g.n.send_reliable(e.peer_id,"done",0)
								for i in range(len(g.players)):
									if g.players[i].compid==compid: remove_from_server(i)

						else:
							if int(parsed[2])!=0: adminsend(""+parsed[1]+" has been banned by "+g.players[index].name+": Reason: "+e.message.replace(parsed[0]+" "+parsed[1]+" "+parsed[2]+" ","")+": The time will end in "+str(convert_minutes_to_datetime_object(int(parsed[2])))+"")
							if int(parsed[2])==0: adminsend(""+parsed[1]+" has been permanently banned by "+g.players[index].name+": Reason: "+e.message.replace(parsed[0]+" "+parsed[1]+" "+parsed[2]+" ",""))
							g.compbans[parsed[1]]=get_compid_from_player(parsed[1])
							save_bans()
							if 1:
								if parsed[2]!="0": end_datetime=convert_minutes_to_datetime_object(int(parsed[2]))
								if parsed[2]=="0": end_datetime=convert_minutes_to_datetime_object(900000000); file_put_contents("chars/"+parsed[1]+"/permaban.usr","")
								chars=find_directories("chars")
								for char in chars:
									if file_get_contents("chars/"+char+"/compid.usr")==file_get_contents("chars/"+parsed[1]+"/compid.usr") and g.players[ind2].name!=char:
										file_put_contents("chars/"+char+"/banreason.usr",e.message.replace(parsed[0]+" "+parsed[1]+" "+parsed[2]+" ",""))
										file_put_contents("chars/"+char+"/banenddate.usr",pickle.dumps(end_datetime),"wb")
										if parsed[2]=="0": file_put_contents("chars/"+char+"/permaban.usr","")
								file_put_contents("chars/"+parsed[1]+"/banreason.usr",e.message.replace(parsed[0]+" "+parsed[1]+" "+parsed[2]+" ",""))
								file_put_contents("chars/"+parsed[1]+"/banenddate.usr",pickle.dumps(end_datetime),"wb")
								ban_mail(file_get_contents("chars/"+parsed[1]+"/mail.usr"))
								g.n.send_reliable(e.peer_id,"done",0)
								compid=get_compid_from_player(parsed[1])
								for i in range(len(g.players)):
									if g.players[i].compid==compid: remove_from_server(i)
				elif parsed[0]=="/hideme":
					if g.players[index].is_admin() or g.players[index].moderator==True or g.players[index].dev==True:
						g.players[index].hidden = not g.players[index].hidden
						if g.players[index].hidden:
							g.n.send_reliable(g.players[index].peer_id,"Hidden mode ON. Other players cannot see, hear, or detect you.",0)
							g.n.send_reliable(g.players[index].peer_id,"play_s invisibility_start.ogg",0)
							for i in g.players:
								if i.friendonlinemessage==1 and g.players[index].name in i.friendlist: g.n.send_reliable(i.peer_id,"offline "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z)+" "+g.players[index].name+" "+g.players[index].map, 0)
						else:
							g.n.send_reliable(g.players[index].peer_id,"Hidden mode OFF. Other players can now see and hear you.",0)
							g.n.send_reliable(g.players[index].peer_id,"play_s invisibility_stop.ogg",0)
							for i in g.players:
								if i.friendonlinemessage==1 and g.players[index].name in i.friendlist: g.n.send_reliable(i.peer_id,"online "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z)+" "+g.players[index].name+" "+g.players[index].map+" "+str(g.players[index].samplerate), 0)
						save_char(index)
					else:
						g.n.send_reliable(g.players[index].peer_id,"You do not have permission to use this command.",0)

				elif parsed[0]=="/eventpointlist":
					if g.players[index].is_admin():
						chars=find_directories("chars")
						adminsend(""+g.players[index].name+" checked everyone's event points")
						m=server_menu()
						m.initial_packet="tokenlist_menu"
						m.intro="event point Balances"
						token_data=[]
						for char in chars:
							charfolder=os.path.join("chars", char)
							token_file=os.path.join(charfolder, "eventpoint.usr")
							if os.path.isfile(token_file):
								try:
									with open(token_file, "r") as f:
										token_str=f.read().strip()
										token=int(token_str)
										token_data.append((char, token))
								except (ValueError, FileNotFoundError):
									token_data.append((char, "Error Reading Token"))
							else:
								token_data.append((char, "No Token File"))
						token_data.sort(key=lambda item: item[1] if isinstance(item[1],int) else -999999999999, reverse=True)
						for char, token in token_data:
							if isinstance(token, int): m.add(f"{char}, event point: {token}", char, False)
							else: m.add(f"{char}, event point: {token}", char, False)
						m.send(e.peer_id)
					else:
						g.n.send_reliable(e.peer_id, "You do not have permission to use this command.", 0)

				elif parsed[0]=="/tokenlist":
					if g.players[index].is_admin():
						chars=find_directories("chars")
						adminsend(""+g.players[index].name+" checked everyone's tokens")
						m=server_menu()
						m.initial_packet="tokenlist_menu"
						m.intro="Zero Token Balances"
						token_data=[]
						for char in chars:
							charfolder=os.path.join("chars", char)
							token_file=os.path.join(charfolder, "zhtoken.usr")
							if os.path.isfile(token_file):
								try:
									with open(token_file, "r") as f:
										token_str=f.read().strip()
										token=int(token_str)
										token_data.append((char, token))
								except (ValueError, FileNotFoundError):
									token_data.append((char, "Error Reading Token"))
							else:
								token_data.append((char, "No Token File"))
						token_data.sort(key=lambda item: item[1] if isinstance(item[1],int) else -999999999999, reverse=True)
						for char, token in token_data:
							if isinstance(token, int): m.add(f"{char}, Zero Token: {token}", char, False)
							else: m.add(f"{char}, Zero Token: {token}", char, False)
						m.send(e.peer_id)
					else:
						g.n.send_reliable(e.peer_id, "You do not have permission to use this command.", 0)

				# --- /seemail command ---
				elif parsed[0] == "/seemail" and len(parsed) > 1:
					if g.players[index].is_admin():
						target_player_name = parsed[1]
						target_index = get_player_index_from(target_player_name)

						if target_index == -1:
							g.n.send_reliable(e.peer_id, "Player not found.", 0)
						else:
							try:
								email = file_get_contents(f"chars/{target_player_name}/mail.usr")
								g.n.send_reliable(e.peer_id, f"{target_player_name}'s email: {email}", 0)
							except: g.n.send_reliable(e.peer_id, f"Email not found", 0)
					else:
						g.n.send_reliable(e.peer_id, "You do not have permission to use this command.", 0)
					
				# --- /additemstore command ---
				elif parsed[0] == "/additemstore" and len(parsed) > 3:
					if g.players[index].is_admin():
						category=parsed[1]
						item_name=parsed[2]
						item_price=parsed[3]

						item = {"name":item_name, "price":item_price, "category":category, "description":"no description"}

						store_data.append(item)
						file_put_contents("store.txt", ""+item_name+":"+item_price+":"+category+":no description\n", "a")
						
						g.n.send_reliable(e.peer_id, f"Item '{item_name}' added to store.", 0)
					else:
						g.n.send_reliable(e.peer_id, "You do not have permission to use this command.", 0)
				# --- /removeitemstore command ---
				elif parsed[0] == "/removeitemstore" and len(parsed) > 2:
					if g.players[index].is_admin():

						category=parsed[1]
						item_name = parsed[2]
						found_and_removed = False
						for ind, item in enumerate(store_data):
							if item["category"]==category and item["name"] == item_name:
								del store_data[ind]
								found_and_removed = True
								break
						
						if found_and_removed:
							file_put_contents("store.txt", "".join(f"{item['name']}:{item['price']}:{item['category']}:{item['description']}\n" for item in store_data))

							g.n.send_reliable(e.peer_id, f"Item '{item_name}' removed from store.", 0)
						else:
							g.n.send_reliable(e.peer_id, "Item not found in store.", 0)
					else:
						g.n.send_reliable(e.peer_id, "You do not have permission to use this command.", 0)
				# --- /additemeventstore command ---
				elif parsed[0] == "/additemeventstore" and len(parsed) > 2:
					if g.players[index].is_admin():

						item_name=parsed[1]
						item_price=parsed[2]
						item = {"name":item_name, "price":item_price, "description":"no description"}

						event_store_data.append(item)

						file_put_contents("event_store.txt", ""+item_name+":"+item_price+":no description\n", "a")
						g.n.send_reliable(e.peer_id, f"Item '{item_name}' added to event store.", 0)
					else:
						g.n.send_reliable(e.peer_id, "You do not have permission to use this command.", 0)

				# --- /removeitemeventstore command ---
				elif parsed[0] == "/removeitemeventstore" and len(parsed) > 1:
					if g.players[index].is_admin():

						item_name = parsed[1]
						found_and_removed = False
						for ind, item in enumerate(event_store_data):
							if item["name"] == item_name:
								del event_store_data[ind]
								found_and_removed = True
								break
						

						if found_and_removed:
							file_put_contents("event_store.txt", "".join(f"{item['name']}:{item['price']}:{item['description']}\n" for item in event_store_data))

							g.n.send_reliable(e.peer_id, f"Item '{item_name}' removed from event store.", 0)
						else:
							g.n.send_reliable(e.peer_id, "Item not found in event store.", 0)
					else:
						g.n.send_reliable(e.peer_id, "You do not have permission to use this command.", 0)
				elif parsed[0] == "/scriptreload":
					if g.players[index].dev:
						try:
							importlib.reload(guns)
							importlib.reload(guns2)
							importlib.reload(npc)
							importlib.reload(zombie)
							importlib.reload(internet)
							importlib.reload(file_directories)
							importlib.reload(compban)
							importlib.reload(rotation)
							importlib.reload(match)
							importlib.reload(moving_sound_serverside_handler)
							importlib.reload(player)
							importlib.reload(compid_handler)
							importlib.reload(map)
							importlib.reload(item)
							importlib.reload(zhaserver) #addded


							g.n.send_reliable(e.peer_id, "Scripts reloaded successfully.", 0)
						except Exception as ex:
							g.n.send_reliable(e.peer_id, f"Error reloading scripts: {ex}", 0)
							developersend(f"Error reloading scripts by "+g.players[index].name+": "+str(ex))
					else:
						g.n.send_reliable(e.peer_id, "You do not have permission to use this command.", 0)
				elif parsed[0]=="/listip":
					if g.players[index].is_admin():
						chars = find_directories("chars")
						ip_character_data = []  # List of tuples (ip, char_names)

						for char in chars:
							charfolder = os.path.join("chars", char)
							compid_file = os.path.join(charfolder, "compid.usr")
							if os.path.isfile(compid_file):
								compid=file_get_contents(charfolder+"/compid.usr")
								for pl in g.players:
									if file_get_contents("chars/"+pl.name+"/compid.usr")==compid:
										ip_address = str(g.n.get_peer_address(pl.peer_id))

										ip_character_data.append((ip_address, char))
										break
						adminsend(""+g.players[index].name+" checked everyone's IP address")
						m = server_menu()
						m.initial_packet = "compid_menu"
						m.intro = "Accounts Linked to Specific IPs"

						# Add menu items - showing the IP and all related accounts:
						for ip, char in ip_character_data:
							m.add(f"{char}, IP: {ip}", char, False)

						if len(m.menuids) == 0:
							m.add("No accounts found.", "none", False)

						m.send(e.peer_id)
					else:
						g.n.send_reliable(e.peer_id, "You do not have permission to use this command.", 0)
				elif parsed[0] == "/weather":
					if g.players[index].is_admin():
						if parsed[1] == "0":
							g.rain=False
							g.rainstarttimer.restart()
							g.raintimer.restart()
							g.rainfinish=True
							g.rainfinishtimer.restart()

#									g.n.broadcast("remove_rain", 0)
							g.n.send_reliable(e.peer_id, "weather change to clear", 0)

						elif parsed[1] == "1":
							g.raintimer.restart()
							g.rainstarttimer.restart()
							g.rain=True
#									g.n.broadcast("start_rain",0)
							g.n.send_reliable(e.peer_id, "weather change to rain", 0)
						else:
							g.n.send_reliable(e.peer_id, "Invalid weather type. Use 'rain' or 'clear'.", 0)

					else:
						g.n.send_reliable(e.peer_id, "You do not have permission to use this command.", 0)

				elif parsed[0] == "/itemlist" and len(parsed) > 1:
					if g.players[index].is_admin() or g.players[index].moderator==True:
						target_player_name = parsed[1]
						target_index = get_player_index_from(target_player_name)

						if target_index == -1:
							g.n.send_reliable(e.peer_id, "Player not found.", 0)
						else:
							m = server_menu()
							m.initial_packet = "itemlist_menu"
							m.intro = f"Inventory of {target_player_name}"

							if g.players[target_index].inv:
								for item, amount in g.players[target_index].inv.items():
									m.add(f"{item}: {amount}", item, False)
							else:
								m.add("Inventory is empty", "empty", False)
#									g.n.send_reliable(g.players[target_index].peer_id, "You inventory is checking by staff",0)
							m.send(e.peer_id)
					else:
						g.n.send_reliable(e.peer_id, "You do not have permission to use this command.", 0)

				# --- /clearinventory command ---
				elif parsed[0] == "/clearinventory" and len(parsed) > 1:
					if g.players[index].is_admin() or g.players[index].moderator==True:
						target_player_name = parsed[1]
						target_index = get_player_index_from(target_player_name)

						if target_index == -1:
							g.n.send_reliable(e.peer_id, "Player not found.", 0)
						else:
							g.players[target_index].inv.clear()
							g.n.send_reliable(e.peer_id, f"Inventory of {target_player_name} cleared.", 0)
							g.n.send_reliable(g.players[target_index].peer_id,"All your items have been removed by staff. Please do not use hack",0)
							g.players[target_index].weapon="punch"
							g.players[target_index].weapon2="feet"
							save_char(target_index)
					else:
						g.n.send_reliable(e.peer_id, "You do not have permission to use this command.", 0)
				# --- /viewplayer command ---
				# --- /viewplayer command ---
				elif parsed[0] == "/viewplayer" and len(parsed) > 1:
					if g.players[index].is_admin() or g.players[index].moderator==True:
						target_player_name = parsed[1]
						player_dir = os.path.join("chars", target_player_name)

						if not directory_exists(player_dir):
							g.n.send_reliable(e.peer_id, "Player not found.", 0)
						else:
							m = server_menu()
							m.initial_packet = "viewplayer_info"
							m.intro = f"Information for {target_player_name}"

							# --- Basic Account Information ---
							try:
								comp_id = file_get_contents(os.path.join(player_dir, "compid.usr"))
								m.add(f"Computer ID: {comp_id}", "compid", False)
							except FileNotFoundError:
								m.add("Computer ID: Not available", "compid", False)

							try:
								email = file_get_contents(os.path.join(player_dir, "mail.usr"))
								m.add(f"Email: {email}", "email", False)
							except FileNotFoundError:
								m.add("Email: Not available", "email", False)

							try:
								created_date = file_get_contents(os.path.join(player_dir, "createdate.usr"))
								m.add(f"Account Created: {created_date}", "createdate", False)
							except FileNotFoundError:
								m.add("Account Created: Not available", "createdate", False)

							try:
								last_active = file_get_contents(os.path.join(player_dir, "lastactive.usr"))
								m.add(f"Last Active: {last_active}", "lastactive", False)
							except FileNotFoundError:
								m.add("Last Active: Not available", "lastactive", False)

							# --- Character Information ---
							try:
								current_char = pickle.loads(file_get_contents(os.path.join(player_dir, "current_char.usr"), "rb"))
								m.add(f"Current Character: {current_char}", "currentchar", False)
							except FileNotFoundError:
								m.add("Current Character: Not available", "currentchar", False)
							
							try: 
								scorepoint=file_get_contents(os.path.join(player_dir, "scorepoint.usr"))
								m.add(f"score point: {scorepoint}", "test", False)
							except: pass

							try: 
								scorepointrank=file_get_contents(os.path.join(player_dir, "scorerank.usr"))
								m.add(f"score rank: {scorepointrank}", "test", False)
							except: pass
							try: 
								scorepointban=file_get_contents(os.path.join(player_dir, "permaban.usr"))
								m.add(f"Perm ban: Yes", "test", False)
							except: 
								m.add(f"Perm ban: No", "test", False)

							# --- Moderation Information ---
							try:
								ban_reason = file_get_contents(os.path.join(player_dir, "banreason.usr"))
								ban_end_date_content = file_get_contents(os.path.join(player_dir, "banenddate.usr"), "rb")
								if ban_end_date_content:  # Check if the file content is not empty
									ban_end_date = pickle.loads(ban_end_date_content)
									m.add(f"Ban Reason: {ban_reason}, Time end: {ban_end_date}", "baninfo", False)
								else:
									m.add("Ban Reason: " + ban_reason + ", Time end: no time ", "baninfo", False)

							except FileNotFoundError:
								m.add("Ban Information: Not banned", "baninfo", False)
							except Exception as e: 
								m.add(f"Ban Information: Error reading ban info ({e})", "baninfo", False)

							#--- If player is admin
							if(file_exists(dir+"/admin.usr")):
								m.add(f"Admin: True", "admin", False)
							else: m.add(f"Admin: False", "admin", False)

							#--- If player is beta
							if(file_exists(dir+"/beta.usr")):
								m.add(f"Beta Member: True", "admin", False)
							else: m.add(f"Beta Member: False", "admin", False)


							#--- If player is beta
							if(file_exists(dir+"/moderator.usr")):
								m.add(f"Moderator: True", "moderator", False)
							else: m.add(f"Moderator: False", "moderator", False)

							# Add more information here (e.g., IP address, last login time, etc.)
							m.send(e.peer_id)
					else:
						g.n.send_reliable(e.peer_id, "You do not have permission to use this command.", 0)

				elif parsed[0]=="/unban" and len(parsed)>1:
					if g.players[index].is_admin():
						success=comp_unban(parsed[1])
						if success==False:
							g.n.send_reliable(g.players[index].peer_id, "That player can not be unbanned.", 0)
						else:
							g.n.send_reliable(e.peer_id,"done",0)

							adminsend(""+parsed[1]+"'s ban has been removed by "+g.players[index].name+"")
						file_delete("chars/"+parsed[1]+"/permaban.usr")
				elif parsed[0]=="/getchanges":
					if g.players[index].is_admin()==True:
						g.n.send_reliable(g.players[index].peer_id, ""+file_get_contents("changes.txt","rb").decode("utf-8",errors="ignore"), 2)
						adminsend(""+g.players[index].name+" copied the changes")
				elif parsed[0]=="/reboot" and len(parsed)>2:

					if g.players[index].is_admin() or g.players[index].dev==True or g.players[index].moderator==True:
						g.rebootreason=string_replace(e.message,parsed[0]+" "+parsed[1]+" ","",False)
						g.rebootputtime=string_to_number(parsed[1])
						g.n.broadcast("The server will be restarted within "+str(g.rebootputtime)+" seconds for "+g.rebootreason+"",2)
						g.n.broadcast("play_s wrong-answer-129254.ogg",0)
						adminsend("The server will be restarted within "+str(g.rebootputtime)+" seconds for "+g.rebootreason+" by "+g.players[index].name+"")

						for i in range(len(g.players)):
							save_char(i)
						update_char_counter("rebootcount")
						g.rebooting=True
						g.reboottimer.restart()
				elif(parsed[0]=="/exit"):
				
					if(g.players[index].dev): exit()
					
				elif(parsed[0]=="/where"):
				
					if(g.players[index].dev or g.players[index].is_admin()==True or g.players[index].moderator==True):
						index2=get_player_index_from(parsed[1])
						if index2>-1:
							g.n.send_reliable(e.peer_id,""+str(round(g.players[index2].x))+", "+str(round(g.players[index2].y))+", "+str(round(g.players[index2].z))+", "+g.players[index2].map+"",2)
							adminsend(""+g.players[index].name+" checked where "+g.players[index2].name+"'s location")
				elif(parsed[0]=="/newmap" and len(parsed)>5):
				
					if(g.players[index].is_builder()):
					
						mapname=parsed[1]
						maxx=parsed[2]
						maxy=parsed[3]
						maxz=parsed[4]
						defsurface=parsed[5]
						if(file_exists("maps/"+mapname+".map")):
						
							g.n.send_reliable(g.players[index].peer_id,"this map is already exists",0)
							return
							
						adminsend(""+parsed[1]+" map has been created by "+g.players[index].name+"")
						f=open("maps/"+mapname+".map","w")
						f.write("mapname:"+mapname+"\nmaxx:"+str(maxx)+"\nmaxy:"+str(maxy)+"\nmaxz:"+str(maxz)+"\nplatform:0:"+str(maxx)+":0:"+str(maxy)+":0:0:"+defsurface+"\n")
						f.close()
						init_mapsystem()
						move_player(index, 0, 0, 0, mapname)
						
					
				elif(parsed[0]=="/changemap" and len(parsed)>2):
				
					if(g.players[index].is_admin() or g.players[index].moderator==True):
					
						ind2=g.get_player_index_from(parsed[1])
						if(ind2<0):
							g.n.send_reliable(g.players[index].peer_id,"player not found",0)
						else:
							if not file_exists("maps/"+parsed[2]+".map"): g.n.send_reliable(e.peer_id,"No such map found.",0); return
							move_player(ind2,0,0,0,parsed[2],False)
							adminsend(""+g.players[ind2].name+"'s map changed to "+parsed[2]+" by "+g.players[index].name+"")
							g.n.send_reliable(g.players[index].peer_id,"Done, moved",0)
							
						
					
				elif(parsed[0]=="/changemymap" and len(parsed)>1):
				
					if(g.players[index].is_builder() or g.players[index].moderator==True):
					
#								if file_exists("maps/"+parsed[1]+".map")==False:
#									send_reliable(g.players[index].peer_id,"map does not exists, "+parsed[1]+"",0)
#									return
						adminsend(""+g.players[index].name+" changed their map to "+parsed[1]+"")
						move_player(index, 0, 0, 0, parsed[1], False)
						
					
				elif(parsed[0]=="/sendstaffmessage" and len(parsed)>1):
					ind2=g.get_player_index_from(parsed[1])
					if(ind2<0):
						message=string_replace(e.message,parsed[0]+" "+parsed[1]+" ","",False)
						try: offlinestaff(parsed[1],""+message)
						except: g.n.send_reliable(e.peer_id,"Player not found",0); return
						adminsend(""+g.players[index].name+" send a staff message to "+parsed[1]+": "+message)
						adminsendsound("misc214")
					else:
					
						message=string_replace(e.message,parsed[0]+" "+parsed[1]+" ","",False)
						g.n.send_reliable(g.players[ind2].peer_id,"adminmessage the staff sent you a message! "+message,0)
						g.n.send_reliable(g.players[ind2].peer_id,"play_s misc214.ogg",0)
						g.n.send_reliable(g.players[ind2].peer_id,"play_s misc305.ogg",0)
						adminsend(""+g.players[index].name+" send a staff message to "+g.players[ind2].name+": "+message)
						adminsendsound("misc214")
				elif(parsed[0]=="/pm" and len(parsed)>1):
					if not g.players[index].disable_all_chat_check(): return
					if not g.players[index].disable_pm_chat_check(): return
					if parsed[1] not in g.players[index].friendlist: g.n.send_reliable(e.peer_id,"This player not on your friend list",0); return
					try: blocks=pickle.loads(file_get_contents("chars/"+parsed[1]+"/blocks.usr","rb"))
					except: blocks=[]
					if g.players[index].name in blocks: g.n.send_reliable(e.peer_id,"Error, this player has blocked you.",0); return
					ind2=g.get_player_index_from(parsed[1])
					if(ind2<0):
						message=string_replace(e.message,parsed[0]+" "+parsed[1]+" ","",False)

						try: offlinepm(parsed[1],g.players[index].name,message)
						except: g.n.send_reliable(e.peer_id,"Player not found",0); return
						g.n.send_reliable(g.players[index].peer_id,"pm pm to offline "+parsed[1]+": "+message,0)
					else:
					
						message=string_replace(e.message,parsed[0]+" "+parsed[1]+" ","",False)
						if g.players[ind2].pmmessage==0: g.n.send_reliable(e.peer_id,"Error, this player disabled receiving private message from friends.",0); return
						g.n.send_reliable(g.players[ind2].peer_id,"pm Pm from "+g.players[index].name+": "+message,0)
						g.players[ind2].replyname=g.players[index].name
						if not g.players[ind2].hidden: g.n.send_reliable(g.players[index].peer_id,"pm pm to "+g.players[ind2].name+": "+message,0)
						if g.players[ind2].hidden: g.n.send_reliable(g.players[index].peer_id,"pm pm to offline "+g.players[ind2].name+": "+message,0)
						
					
				elif(parsed[0]=="/rawmap" and len(parsed)>1):
				
					if(g.players[index].is_builder()==True):
					
						g.n.send_reliable(g.players[index].peer_id,get_map_data(parsed[1]),2)
						adminsend(""+parsed[1]+" datas has been copied by "+g.players[index].name+"")
						
					
				elif(parsed[0]=="/rawdata" and len(parsed)>2):
				
					if(g.players[index].is_builder()==True):
					
						maptext=string_replace(e.message,"/rawdata "+parsed[1]+" ","",False)

						f=open("maps/"+parsed[1]+".map","w")
						f.write(maptext)
						f.close()
						update_map(parsed[1])
						g.n.send_reliable(g.players[index].peer_id,"Done",0)
						adminsend(""+g.players[index].name+" updated to "+parsed[1]+" map")
						
					
				elif(parsed[0]=="/setmoderator" and len(parsed)>2):
				
					if(g.players[index].is_admin()==True):
					
						ind2=g.get_player_index_from(parsed[1])
						if(ind2<0):
							if directory_exists("chars/"+parsed[1]+"")==False: g.n.send_reliable(g.players[index].peer_id,"char does not exists",2); return
							numm=string_to_number(parsed[2])
							if numm==0: file_delete("chars/"+parsed[1]+"/moderator.usr"); adminsend(""+parsed[1]+"'s moderator rank has been demoted by "+g.players[index].name+""); return
							if numm==1: file_put_contents("chars/"+parsed[1]+"/moderator.usr","1"); adminsend(""+parsed[1]+" is now moderator by "+g.players[index].name+""); return

						else:
						
							num=string_to_number(parsed[2])
							if(num==1):
							
								adminsend(""+g.players[ind2].name+" is now moderator of the game by "+g.players[index].name+"")
								g.players[ind2].moderator=True
#										g.players[ind2].title="Moderator"
#										g.players[ind2].title2="Moderator"

#										g.n.broadcast(""+g.players[ind2].name+" is now moderator of zero_hour_assault!",2)
#										g.n.broadcast("play_s error-2-126514.ogg",0)
								file_put_contents("chars/"+g.players[ind2].name+"/moderator.usr","1")
								
							elif(num==0):
							
								adminsend(""+g.players[ind2].name+"'s moderator rank has been removed by "+g.players[index].name+"")
								g.players[ind2].moderator=False
								g.players[ind2].title=""
								g.players[ind2].title2="Player"

#										g.n.broadcast(""+g.players[ind2].name+" moderator rank has been demoted",2)
#										g.n.broadcast("play_s error-2-126514.ogg",0)

								file_delete("chars/"+g.players[ind2].name+"/moderator.usr")
								
							
						
					


				elif parsed[0]=="/addbeta" and len(parsed)>1:
					if directory_exists("chars/"+parsed[1]+"")==False: g.n.send_reliable(g.players[index].peer_id,"invalid char",2); return
					if file_exists("chars/"+parsed[1]+"/beta.usr")==True: g.n.send_reliable(g.players[index].peer_id,"this player is already a betatester",2); return
					file_put_contents("chars/"+parsed[1]+"/beta.usr","1")
					adminsend(""+parsed[1]+" is now beta member of the game by "+g.players[index].name+"")
				elif parsed[0]=="/removebeta" and len(parsed)>1:
					if directory_exists("chars/"+parsed[1]+"")==False: g.n.send_reliable(g.players[index].peer_id,"invalid char",2); return
					if file_exists("chars/"+parsed[1]+"/beta.usr")==False: g.n.send_reliable(g.players[index].peer_id,"this player is already not a betatester",2); return

					file_delete("chars/"+parsed[1]+"/beta.usr")
					adminsend(""+parsed[1]+" is being removed from beta by "+g.players[index].name+"")
					x=get_player_index_from(parsed[1])
					if x>-1: g.n.send_reliable(g.players[x].peer_id,"you are removed from beta",0); remove_from_server(x);

				elif(parsed[0]=="/setadmin" and len(parsed)>2):
				
					if(g.players[index].is_admin()==True):
					
						ind2=g.get_player_index_from(parsed[1])
						if(ind2<0):
							if directory_exists("chars/"+parsed[1]+"")==False: g.n.send_reliable(g.players[index].peer_id,"char does not exists",2); return
							numm=string_to_number(parsed[2])
							if numm==0: file_delete("chars/"+parsed[1]+"/admin.usr"); adminsend(""+parsed[1]+"'s adminship has been demoted by "+g.players[index].name+""); return
							if numm==1: file_put_contents("chars/"+parsed[1]+"/admin.usr","1"); adminsend(""+parsed[1]+" is now admin by "+g.players[index].name+""); return


						else:
						
							num=string_to_number(parsed[2])
							if(num==1):
							
								adminsend(""+g.players[ind2].name+" is now admin of the game by "+g.players[index].name+"")
								g.players[ind2].admin=True
#										g.players[ind2].title="Administrator"
#										g.players[ind2].title2="Administrator"

#										g.n.broadcast(""+g.players[ind2].name+" is now admin of zero_hour_assault!",2)
#										g.n.broadcast("play_s error-2-126514.ogg",0)
								file_put_contents("chars/"+g.players[ind2].name+"/admin.usr","1")
								
							elif(num==0):
							
								adminsend(""+g.players[ind2].name+"'s admin rank has been removed by "+g.players[index].name+"")
								g.players[ind2].admin=False
								g.players[ind2].title=""
								g.players[ind2].title2="Player"

#										g.n.broadcast(""+g.players[ind2].name+" admin rank has been demoted",2)
#										g.n.broadcast("play_s error-2-126514.ogg",0)

								file_delete("chars/"+g.players[ind2].name+"/admin.usr")
								
							
						
					

				elif parsed[0]=="/clearmatchs" and g.players[index].is_admin():
					g.n.broadcast("play_s important.ogg",0)
					g.n.broadcast("all matches ended by staff",2)
					adminsend("all matchs have been ended by "+g.players[index].name+"")
					for i in range(len(g.players)):
						if g.players[i].map!="lobby": move_player(i,5,0,0,"lobby")
					for m in g.matches: m.cancel()
					g.npcs=[]
					g.matches=[]
					g.items=[]
					g.flags=[]
					g.zombies=[]
				elif parsed[0]=="/sethealth" and len(parsed)>2:
					if g.players[index].is_admin()==True or g.players[index].moderator==True:
						x=get_player_index_from(parsed[1])
						if x>-1:

							g.n.send_reliable(g.players[index].peer_id,"set to "+str(parsed[2])+"",0)
							adminsend(""+g.players[index].name+" updated "+g.players[x].name+" health to "+str(parsed[2])+"")

							g.players[x].health=stn(parsed[2])
				elif parsed[0]=="/settoken" and len(parsed)>2:
					if g.players[index].is_admin()==True:
						x=get_player_index_from(parsed[1])
						if x>-1:

							g.n.send_reliable(g.players[index].peer_id,"set to "+str(parsed[2])+"",0)
							adminsend(""+g.players[index].name+" updated "+g.players[x].name+" zero token to "+str(parsed[2])+"")

							g.players[x].zhtoken=stn(parsed[2])
				elif parsed[0]=="/seteventpoint" and len(parsed)>2:
					if g.players[index].is_admin()==True:
						x=get_player_index_from(parsed[1])
						if x>-1:

							g.n.send_reliable(g.players[index].peer_id,"set to "+str(parsed[2])+"",0)
							adminsend(""+g.players[index].name+" updated "+g.players[x].name+" event point to "+str(parsed[2])+"")

							g.players[x].eventpoint=stn(parsed[2])

				elif parsed[0]=="/givepack":
					adminsend(""+g.players[index].name+" gived "+parsed[1]+" to "+parsed[2]+" "+str(parsed[3])+"")
					file_put_contents("zitemdata.txt", parsed[2]+"="+parsed[1]+"="+parsed[3])
				elif parsed[0]=="/givepack2":
					adminsend(""+g.players[index].name+" gived "+parsed[1]+" to "+parsed[2]+" "+str(parsed[3])+"")
					file_put_contents("ioszitemdata.txt", parsed[2]+"="+parsed[1]+"="+parsed[3])

				elif parsed[0]=="/givetoken" and len(parsed)>2:
					if g.players[index].is_admin()==True or g.players[index].moderator==True:
						if directory_exists("chars/"+parsed[1]+"")==False: g.n.send_reliable(g.players[index].peer_id,"account not found",2); return
#								current_token=file_get_contents("chars/"+parsed[1]+"/zhtoken.usr")
						x=get_player_index_from(parsed[1])
						if x>-1:
							g.players[x].zhtoken+=stn(parsed[2])
							adminsend(""+g.players[index].name+" gaved "+str(parsed[2])+" zero token to "+g.players[x].name+"")
						else:
							current_token = int(file_get_contents("chars/" + parsed[1] + "/zhtoken.usr").strip())
							newtoken=int(parsed[2])
							finaly=current_token + newtoken

							file_put_contents("chars/"+parsed[1]+"/zhtoken.usr",str(finaly))
							adminsend(""+g.players[index].name+" gaved "+str(parsed[2])+" zero token to "+parsed[1]+": Before value was "+str(current_token)+", now he has "+str(finaly)+" tokens")

				elif parsed[0]=="/givetokenall" and len(parsed)>1:
					if g.players[index].is_admin()==True or g.players[index].moderator==True:
						adminsend(""+g.players[index].name+" gived everyone "+str(parsed[1])+" zero tokens")
						for p in range(len(g.players)):
							if g.players[p].map=="jail": continue
							g.n.send_reliable(g.players[p].peer_id,"play_s getpoints.ogg",0)
							g.n.send_reliable(g.players[p].peer_id,"you got "+str(parsed[1])+" zero tokens from the staff team!",2)
							g.players[p].zhtoken+=stn(parsed[1])
				elif(parsed[0]=="/setbuilder" and len(parsed)>2):
				
					if(g.players[index].dev==True):
					
						ind2=g.get_player_index_from(parsed[1])
						if(ind2<0):
#									g.n.send_reliable(g.players[index].peer_id,"Player not found.",0)
							if directory_exists("chars/"+parsed[1]+"")==False: g.n.send_reliable(g.players[index].peer_id,"char does not exists",2); return
							numm=string_to_number(parsed[2])
							if numm==0: file_delete("chars/"+parsed[1]+"/builder.usr"); adminsend(""+parsed[1]+"'s builder rank has been demoted by "+g.players[index].name+""); return
							if numm==1: file_put_contents("chars/"+parsed[1]+"/builder.usr","1"); adminsend(""+parsed[1]+" is now builder by "+g.players[index].name+""); return

						else:
						
							num=string_to_number(parsed[2])
							if(num==1):
							
								adminsend(""+g.players[ind2].name+" is now builder of the game by "+g.players[index].name+"")
								g.players[ind2].builder=True
#										g.players[ind2].title="Builder"
#										g.players[ind2].title2="Builder"

#										g.n.broadcast(""+g.players[ind2].name+" is now builder of zero_hour_assault!",2)
#										g.n.broadcast("play_s error-2-126514.ogg",0)
								file_put_contents("chars/"+g.players[ind2].name+"/builder.usr","1")
								
							elif(num==0):
							
								adminsend(""+g.players[ind2].name+"'s builder rank has been removed by "+g.players[index].name+"")
								g.players[ind2].builder=False
								g.players[ind2].title=""
								g.players[ind2].title2="Player"

#										g.n.broadcast(""+g.players[ind2].name+" builder rank has been demoted",2)
#										g.n.broadcast("play_s error-2-126514.ogg",0)

								file_delete("chars/"+g.players[ind2].name+"/builder.usr")
								
							
						
					
				if parsed[0]=="/newmotd" and len(parsed)>1:
					if g.players[index].is_admin()==True:
						mess=string_replace(e.message,"/newmotd ","",False)
						phpresponse=url_post("https://nbmstudios.com/zero_hour_assault/sendmotd.php", {"id":"nbmcantsend","motd":string_replace(e.message, "/newmotd ", "", True)})
						if phpresponse=="failed" or phpresponse!="success":
							g.n.send_reliable(g.players[index].peer_id,"the motd could not be updated online. php response: "+phpresponse, 2)

						import db as _db
						_db.sv_write_text("motd.txt", mess)
						adminsend("server message has been changed by "+g.players[index].name+": "+mess+"")
						g.n.broadcast("play_s misc200.ogg",0)
						g.n.broadcast("attention. Server message has been updated. Please press f1 for see more details",2)
						update_char_counter("motdcount")
				elif(parsed[0]=="/notify"):
				
					if(g.players[index].is_admin() or g.players[index].moderator==True):
					
						mess=string_replace(e.message,"/notify ","",False)
						adminsend(""+g.players[index].name+" gaved notification to everyone: "+mess+"")
						g.n.broadcast("notify "+mess,0)
						
					
				elif(parsed[0]=="/give" and len(parsed)>3):
				
					if(g.players[index].is_admin()):
					
						ind2=g.get_player_index_from(parsed[1])
						if(ind2<0):
							g.n.send_reliable(g.players[index].peer_id,"not found",0)
						else:
						
							what=parsed[2]
							amount=string_to_number(parsed[3])
							adminsend(""+g.players[index].name+" gived item to "+g.players[ind2].name+": "+str(amount)+" "+what+"")
							notify_admins("Zero hour assault, "+g.players[index].name+" gived item to "+g.players[ind2].name+": "+str(amount)+" "+what+"")
							g.players[ind2].give(what, amount)
							g.n.send_reliable(g.players[index].peer_id,"Done",0)
							
						
					
				elif parsed[0]=="/facing":
					g.n.send_reliable(g.players[index].peer_id,""+str(g.players[index].facing)+"",0)
				elif parsed[0]=="/scorepoint" and g.players[index].dev==True:
					g.players[index].scorepoint+=5
				elif parsed[0]=="/updatechanges" and len(parsed)>1:
					if g.players[index].is_admin()==True or g.players[index].dev==True:
						file_put_contents("changes.txt", string_replace(e.message, "/updatechanges ", "", False), "w")
						adminsend(""+g.players[index].name+" updated to changes")
						g.n.send_reliable(g.players[index].peer_id, "done", 0)
						g.n.broadcast("play_s misc153.ogg",0)
						g.n.broadcast("The last changes section has been updated, please take a look.",2)
						update_char_counter("changelogcount")

				elif parsed[0]=="/chars":
					if g.players[index].is_admin()==True:
						chars=find_directories("chars")
						adminsend(""+g.players[index].name+" checked chars")
						m=server_menu()
						m.initial_packet="charsmenu"
						m.intro="Chars list. There are currently "+str(len(chars))+" chars available."
						for i in range(len(chars)):
							m.add(chars[i], chars[i],False)
						m.send(g.players[index].peer_id)
				elif parsed[0]=="/maps":
					m=server_menu()
					ftotal=0
					msg=""
					f=find_files("maps")
					msg+=str(len(f))+" maps available."
					m.intro=""+str(len(f))+" maps available."
					m.initial_packet="move_map"

					for i in range(len(f)):
						if string_contains(f[i],"base",1)>-1: continue
						m.add(f[i],f[i])
					m.send(g.players[index].peer_id)
				elif parsed[0]=="/gamestop":
					if g.players[index].is_admin()==True or g.players[index].moderator==True:
						adminsend(""+g.players[index].name+" stopped to game")
						g.gamestop=1
						if not file_exists("frozen.txt"): file_put_contents("frozen.txt", "")

						g.n.broadcast("stopmoving",0)
						g.n.broadcast("Attention. The game has now been frozen by a staff member. Please be patiently.",2)
						g.n.broadcast("play_s important.ogg",0)
						g.n.broadcast("play_s misc136.ogg",0)
				elif parsed[0]=="/gamestart":
					if g.players[index].is_admin()==True or g.players[index].moderator==True:
						adminsend(""+g.players[index].name+" open the game")
						g.gamestop=0
						if file_exists("frozen.txt")==True:
							file_delete("frozen.txt")
						g.n.broadcast("startmoving",0)
						g.n.broadcast("Attention. The game has now been unfrozen!",2)
						g.n.broadcast("play_s misc163.ogg",0)

				elif(parsed[0]=="/block_voice" and len(parsed)>1):
				
					if(g.players[index].is_admin() or g.players[index].moderator==True):
					
						ind2=g.get_player_index_from(parsed[1])
						if(ind2>-1):
							g.n.send_reliable(g.players[ind2].peer_id,"disablevoicechat",0)
							g.players[ind2].blockvoice3=1
							adminsend(""+g.players[index].name+" disabled "+g.players[ind2].name+"s voice chat")
							g.n.send_reliable(g.players[ind2].peer_id,"Your voice chat feature has been blocked by staff",2)
				elif(parsed[0]=="/unblock_voice" and len(parsed)>1):
				
					if(g.players[index].is_admin() or g.players[index].moderator==True):
					
						ind2=g.get_player_index_from(parsed[1])
						if(ind2>-1):
							g.n.send_reliable(g.players[ind2].peer_id,"enablevoicechat",0)
							g.players[ind2].blockvoice3=0
							adminsend(""+g.players[index].name+" enabled "+g.players[ind2].name+"s voice chat")
							g.n.send_reliable(g.players[ind2].peer_id,"Your voice chat feature has been unblocked by staff",2)

				elif parsed[0]=="/npcs":
					s=""
					for i in g.npcs:
						s+="there are "+str(len(g.npcs))+" npcs: "+str(i.x)+", "+str(i.y)+", "+str(i.z)+", "+i.map+"\n"
					for i in g.matches:
						s+="there are "+str(len(g.matches))+" matches.\n"

					for i in g.motors:
						s+="there are "+str(len(g.motors))+" motors: "+str(i.x)+", "+str(i.y)+", "+str(i.z)+", "+i.map+"\n"
					for i in g.items:
						s+="there are "+str(len(g.items))+" items: "+str(i.x)+", "+str(i.y)+", "+str(i.z)+", "+i.map+"\n"
					for i in g.flags:
						s+="there are "+str(len(g.flags))+" flags: "+str(i.x)+", "+str(i.y)+", "+str(i.z)+", "+i.map+"\n"
					g.n.send_reliable(g.players[index].peer_id,s,2)
				elif parsed[0]=="/weapons": g.n.send_reliable(g.players[index].peer_id,str(len(g.weapons)),0)
				elif parsed[0]=="/disablepublicchat":
					reason=e.message.replace(parsed[0]+" "+parsed[1]+" "+parsed[2]+" ","")
					adminsend(""+parsed[1]+"'s general chat feature have been blocked by "+g.players[index].name+" for "+str(parsed[2])+" minutes: reason: "+reason+"")

					ind=g.get_player_index_from(parsed[1])
					if ind>-1: g.players[ind].disable_public_chat(stn(parsed[2]),reason); g.n.send_reliable(e.peer_id,"done",0)
					else:
						file_put_contents("chars/"+parsed[1]+"/disablepublicchattime.usr",str(minutes_to_timestamp(stn(parsed[2]))))
						file_put_contents("chars/"+parsed[1]+"/disablepublicchatreason.usr",reason)
						g.n.send_reliable(e.peer_id,"done",0)
				elif parsed[0]=="/enablepublicchat":
					ind=g.get_player_index_from(parsed[1])
					if ind>-1:
						adminsend(""+g.players[ind].name+"'s public chat feature have been unblocked by "+g.players[index].name+"")
						file_delete("chars/"+parsed[1]+"/disablepublicchattime.usr")
						file_delete("chars/"+parsed[1]+"/disablepublicchatreason.usr")
						g.n.send_reliable(g.players[ind].peer_id,"Your public  chat feature is enabled",2)
						g.n.send_reliable(e.peer_id,"done",0)
				elif parsed[0]=="/enableteamchat":
					ind=g.get_player_index_from(parsed[1])
					if ind>-1:
						adminsend(""+g.players[ind].name+"'s team chat feature have been unblocked by "+g.players[index].name+"")

						file_delete("chars/"+parsed[1]+"/disableteamchattime.usr")
						file_delete("chars/"+parsed[1]+"/disableteamchatreason.usr")
						g.n.send_reliable(g.players[ind].peer_id,"Your team  chat feature is enabled",2)
						g.n.send_reliable(e.peer_id,"done",0)
				elif parsed[0]=="/enableallchat":
					ind=g.get_player_index_from(parsed[1])
					if ind>-1:
						adminsend(""+g.players[ind].name+"'s all chats feature have been unblocked by "+g.players[index].name+"")

						file_delete("chars/"+parsed[1]+"/disableallchattime.usr")
						file_delete("chars/"+parsed[1]+"/disableallchatreason.usr")
						g.n.send_reliable(g.players[ind].peer_id,"Your all  chat feature is enabled",2)
						g.n.send_reliable(e.peer_id,"done",0)

				elif parsed[0]=="/enablepm":
					ind=g.get_player_index_from(parsed[1])
					if ind>-1:
						adminsend(""+g.players[ind].name+"'s private message feature have been unblocked by "+g.players[index].name+"")

						file_delete("chars/"+parsed[1]+"/disablepmchattime.usr")
						file_delete("chars/"+parsed[1]+"/disablepmchatreason.usr")
						g.n.send_reliable(g.players[ind].peer_id,"Your pm  feature is enabled",2)
						g.n.send_reliable(e.peer_id,"done",0)
				elif parsed[0]=="/enablevote":
					ind=g.get_player_index_from(parsed[1])
					if ind>-1:
						adminsend(""+g.players[ind].name+"'s vote feature have been unblocked by "+g.players[index].name+"")

						file_delete("chars/"+parsed[1]+"/disablevotetime.usr")
						file_delete("chars/"+parsed[1]+"/disablevotereason.usr")
						g.n.send_reliable(g.players[ind].peer_id,"Your vote  and poll feature is enabled",2)
						g.n.send_reliable(e.peer_id,"done",0)

				elif parsed[0]=="/enablemapchat":
					ind=g.get_player_index_from(parsed[1])
					if ind>-1:
						adminsend(""+g.players[ind].name+"'s map chat feature have been unblocked by "+g.players[index].name+"")

						file_delete("chars/"+parsed[1]+"/disablemapchattime.usr")
						file_delete("chars/"+parsed[1]+"/disablemapchatreason.usr")
						g.n.send_reliable(g.players[ind].peer_id,"Your map  chat feature is enabled",2)
						g.n.send_reliable(e.peer_id,"done",0)
				elif parsed[0]=="/enablegroupchat":
					ind=g.get_player_index_from(parsed[1])
					if ind>-1:
						adminsend(""+g.players[ind].name+"'s group chat feature have been unblocked by "+g.players[index].name+"")

						file_delete("chars/"+parsed[1]+"/disablegroupchattime.usr")
						file_delete("chars/"+parsed[1]+"/disablegroupchatreason.usr")
						g.n.send_reliable(g.players[ind].peer_id,"Your group  chat feature is enabled",2)
						g.n.send_reliable(e.peer_id,"done",0)

				elif parsed[0]=="/disablepm":
					reason=e.message.replace(parsed[0]+" "+parsed[1]+" "+parsed[2]+" ","")
					adminsend(""+parsed[1]+"'s private message feature have been blocked by "+g.players[index].name+" for "+str(parsed[2])+" minutes: reason: "+reason+"")

					ind=g.get_player_index_from(parsed[1])
					if ind>-1: g.players[ind].disable_pm_chat(stn(parsed[2]),reason); g.n.send_reliable(e.peer_id,"done",0)
					else:
						file_put_contents("chars/"+parsed[1]+"/disablepmchattime.usr",str(minutes_to_timestamp(stn(parsed[2]))))
						file_put_contents("chars/"+parsed[1]+"/disablepmchatreason.usr",reason)
						g.n.send_reliable(e.peer_id,"done",0)

				elif parsed[0]=="/disablevote":
					reason=e.message.replace(parsed[0]+" "+parsed[1]+" "+parsed[2]+" ","")
					adminsend(""+parsed[1]+"'s vote and poll feature have been blocked by "+g.players[index].name+" for "+str(parsed[2])+" minutes: reason: "+reason+"")

					ind=g.get_player_index_from(parsed[1])
					if ind>-1: g.players[ind].disable_vote(stn(parsed[2]),reason); g.n.send_reliable(e.peer_id,"done",0)
					else:
						file_put_contents("chars/"+parsed[1]+"/disablevotetime.usr",str(minutes_to_timestamp(stn(parsed[2]))))
						file_put_contents("chars/"+parsed[1]+"/disablevotereason.usr",reason)
						g.n.send_reliable(e.peer_id,"done",0)


				elif parsed[0]=="/disableteamchat":
					reason=e.message.replace(parsed[0]+" "+parsed[1]+" "+parsed[2]+" ","")
					adminsend(""+parsed[1]+"'s team chat feature have been blocked by "+g.players[index].name+" for "+str(parsed[2])+" minutes: reason: "+reason+"")

					ind=g.get_player_index_from(parsed[1])
					if ind>-1: g.players[ind].disable_team_chat(stn(parsed[2]),reason); g.n.send_reliable(e.peer_id,"done",0)
					else:
						file_put_contents("chars/"+parsed[1]+"/disableteamchattime.usr",str(minutes_to_timestamp(stn(parsed[2]))))
						file_put_contents("chars/"+parsed[1]+"/disableteamchatreason.usr",reason)
						g.n.send_reliable(e.peer_id,"done",0)

				elif parsed[0]=="/disablemapchat":
					reason=e.message.replace(parsed[0]+" "+parsed[1]+" "+parsed[2]+" ","")
					adminsend(""+parsed[1]+"'s map chat feature have been blocked by "+g.players[index].name+" for "+str(parsed[2])+" minutes: reason: "+reason+"")

					ind=g.get_player_index_from(parsed[1])
					if ind>-1: g.players[ind].disable_map_chat(stn(parsed[2]),reason); g.n.send_reliable(e.peer_id,"done",0)
					else:
						file_put_contents("chars/"+parsed[1]+"/disablemapchattime.usr",str(minutes_to_timestamp(stn(parsed[2]))))
						file_put_contents("chars/"+parsed[1]+"/disablemapchatreason.usr",reason)
						g.n.send_reliable(e.peer_id,"done",0)

				elif parsed[0]=="/disablegroupchat":
					reason=e.message.replace(parsed[0]+" "+parsed[1]+" "+parsed[2]+" ","")
					adminsend(""+parsed[1]+"'s group chat feature have been blocked by "+g.players[index].name+" for "+str(parsed[2])+" minutes: reason: "+reason+"")

					ind=g.get_player_index_from(parsed[1])
					if ind>-1: g.players[ind].disable_group_chat(stn(parsed[2]),reason); g.n.send_reliable(e.peer_id,"done",0)
					else:
						file_put_contents("chars/"+parsed[1]+"/disablegroupchattime.usr",str(minutes_to_timestamp(stn(parsed[2]))))
						file_put_contents("chars/"+parsed[1]+"/disablegroupchatreason.usr",reason)
						g.n.send_reliable(e.peer_id,"done",0)

				elif parsed[0]=="/disableallchat":
					reason=e.message.replace(parsed[0]+" "+parsed[1]+" "+parsed[2]+" ","")
					adminsend(""+parsed[1]+"'s all chats feature have been blocked by "+g.players[index].name+" for "+str(parsed[2])+" minutes: reason: "+reason+"")

					ind=g.get_player_index_from(parsed[1])
					if ind>-1: g.players[ind].disable_all_chat(stn(parsed[2]),reason); g.n.send_reliable(e.peer_id,"done",0)
					else:
						file_put_contents("chars/"+parsed[1]+"/disableallchattime.usr",str(minutes_to_timestamp(stn(parsed[2]))))
						file_put_contents("chars/"+parsed[1]+"/disableallchatreason.usr",reason)
						g.n.send_reliable(e.peer_id,"done",0)

				elif parsed[0]=="/bulletspawn":
					amount=stn(parsed[1])
					for _ in range(amount): spawn_weapon(0, 0, 0, 45, "test", g.players[index].map, g.players[index])
					g.n.send_reliable(e.peer_id,"done",0)
				elif parsed[0]=="/whotalking":
					s=""
					for p in g.players:
						if p.voiceon==1 and not p.hidden: s+=p.name+", "
					g.n.send_reliable(e.peer_id,s,2)
				elif parsed[0]=="/namefind":
					mails=[]
					chars=find_directories("chars")
					for char in chars:
						charfolder=os.path.join("chars",char)
						if file_get_contents(charfolder+"/mail.usr")==parsed[1]: mails.append(char)
					if len(mails)==0: g.n.send_reliable(e.peer_id,"no account with this mail found",0)
					else: g.n.send_reliable(e.peer_id,", ".join(mails),0)

				elif parsed[0]=="/garbage_collect":
					if g.players[index].is_admin()==True or g.players[index].dev==True or g.players[index].moderator==True:
						adminsend(""+g.players[index].name+" started a garbage cleaner to fix lags")
						garbage_collect()
#								g.n.broadcast("notify attention: The staff  initiated a cleanup to fix server lags. This process may take a few seconds",0)
						for i in g.weapons: g.weapons.remove(i)
						delay(500)
						for i in g.items:
							if i.dropped: continue
							g.items.remove(i)
						delay(500)

						for i in g.loots: g.loots.remove(i)
						delay(500)

						for i in g.zombies: g.zombies.remove(i)
						delay(500)

						for i in g.npcs: g.npcs.remove(i)
						delay(500)

						for i in g.bodyfalls: g.bodyfalls.remove(i)
						delay(500)

						garbage_collect()
						g.n.broadcast("notify The garbage clearing is completed. Enjoyable games",0)
				elif parsed[0]=="/deletemap" and len(parsed)>1:
					if g.players[index].builder==True or g.players[index].is_admin()==True or g.players[index].moderator==True or g.players[index].dev==True:
						if file_exists("maps/"+parsed[1]+".map")==False: g.n.send_reliable(g.players[index].peer_id,"map "+parsed[1]+" does not exists",2); return
						adminsend(""+parsed[1]+" map has been deleted by "+g.players[index].name+"")
						g.n.send_reliable(g.players[index].peer_id,"map "+parsed[1]+" has been deleted",2)
						file_delete("maps/"+parsed[1]+".map")
						init_mapsystem()
						for p in g.players:
							if p.map==parsed[1]: move_player(p,5,0,0,parsed[1])
				elif parsed[0]=="/enableverify":
					if g.players[index].moderator==True or g.players[index].dev==True or g.players[index].is_admin()==True:
						if directory_exists("chars/"+parsed[1]+"")==False: g.n.send_reliable(g.players[index].peer_id,"that char "+parsed[1]+" does not exists",2); return
						if file_exists("chars/"+parsed[1]+"/lastverify.usr")==False: g.n.send_reliable(g.players[index].peer_id,"that person can already verify the mail.",2); return
						file_delete("chars/"+parsed[1]+"/lastverify.usr")
						g.n.send_reliable(g.players[index].peer_id,"Done",2)
						adminsend(""+parsed[1]+" can now verify the e-mail by "+g.players[index].name+"")

				elif parsed[0]=="/ip" and len(parsed)>1:
					x=get_player_index_from(parsed[1])
					if x>-1:
						g.n.send_reliable(g.players[index].peer_id,""+str(g.n.get_peer_address(g.players[x].peer_id))+"",2)


				elif parsed[0]=="/watch" and len(parsed)>1:
					x=get_player_index_from(parsed[1])
					if x>-1:
						g.n.send_reliable(e.peer_id,"echo matchwatch "+g.players[x].name,0)

				elif parsed[0]=="/groupowner" and len(parsed)>1:
					if g.players[index].dev==True:
						x=get_player_index_from(parsed[1])
						if x>-1:
#									grp=get_group(g.players[x].groupinfoselect)
							get_group(g.players[x].group).owner=g.players[x].name
				elif parsed[0]=="/items":
					itemamount=0
					for i in range(len(g.items)):
						if g.items[i].map==g.players[index].map:
							itemamount+=1
					g.n.send_reliable(g.players[index].peer_id,"There are "+str(itemamount)+" items on this map.",0)
				elif parsed[0]=="/group_bases":
					if g.players[index].dev:
						adminsend(""+g.players[index].name+" checked all group bases locations")
						m = server_menu()
						m.initial_packet = "group_bases_menu"
						m.intro = "Group Bases List"
						if len(g.group_bases) == 0:
							m.add("No group bases found.", "none", False)
						else:
							for base_obj in g.group_bases:
								m.add(f"Name: {base_obj.name}{base_obj.mapappend}, Map: {base_obj.map}, password: {base_obj.password}. Coords: {base_obj.x}, {base_obj.y}, {base_obj.z}", base_obj.name, False)
						m.send(e.peer_id)
					else:
						g.n.send_reliable(e.peer_id, "You do not have permission to use this command.", 0)
				elif parsed[0]=="/groupbasemove" and len(parsed) > 4:
					if g.players[index].dev:
						base_name = parsed[1]
						try:
							new_x = int(parsed[2])
							new_y = int(parsed[3])
							new_z = int(parsed[4])
						except ValueError:
							g.n.send_reliable(e.peer_id, "Invalid coordinates. X, Y, Z must be numbers.", 0)
							return

						target_base = None
						for base_obj in g.group_bases:
							if base_obj.name+base_obj.mapappend == base_name:
								target_base = base_obj
								break

						if target_base is None:
							g.n.send_reliable(e.peer_id, f"Group base '{base_name}' not found.", 0)
							return

						# Store old coordinates before updating the object
						old_x = target_base.x
						old_y = target_base.y
						old_z = target_base.z
						base_map = target_base.map

						# Update the base object's coordinates
						target_base.x = new_x
						target_base.y = new_y
						target_base.z = new_z


						# Move players out of the old base map if they are inside
						for p in g.players:
							if p.map == f"basement{base_name}{target_base.mapappend}":
								# Move them to the new base entrance on the main map
								move_player(g.get_player_index_from(p.name), new_x, new_y, new_z, base_map)
								g.n.send_reliable(p.peer_id, f"Your group base was moved to {new_x}, {new_y}, {new_z}. You have been relocated.", 2)

#								adminsend(f"{g.players[index].name} moved group base '{base_name}' from ({old_x},{old_y},{old_z}) to ({new_x},{new_y},{new_z}) on map '{base_map}'.")
						g.n.send_reliable(e.peer_id, f"Successfully moved group base '{base_name}' to {new_x}, {new_y}, {new_z}.", 0)
					else:
						g.n.send_reliable(e.peer_id, "You do not have permission to use this command.", 0)

				elif parsed[0] == "/androids":
					if g.players[index].is_admin():
						android_count = 0
						char_dirs = find_directories("chars")  # Use your directory listing function

						for char_dir in char_dirs:
							char_path = os.path.join("chars", char_dir)
							android_file = os.path.join(char_path, "android.usr")
							if file_exists(android_file):
								android_count += 1


						message = f"There are {android_count} players using Android"
						g.n.send_reliable(e.peer_id, message, 0)
					else:
						g.n.send_reliable(e.peer_id, "You don't have permission for this command.", 0)
				elif parsed[0]=="/pingplayer" and len(parsed)>1:
					index2=get_player_index_from(parsed[1])
					if not directory_exists("chars/"+parsed[1]):
						g.n.send_reliable(g.players[index].peer_id, "player "+parsed[1]+" can not found on our data base not found", 2)
						return
					if index2<0:
						g.n.send_reliable(g.players[index].peer_id, "the player "+parsed[1]+" not found", 2)
						return
					if index2>-1:
						rtt=g.n.get_peer_average_round_trip_time(g.players[index2].peer_id)
						g.n.send_reliable(g.players[index].peer_id, "play_s misc128.ogg", 0)
						g.n.send_reliable(g.players[index].peer_id, g.players[index2].name+"'s ping is "+str(rtt)+" ms", 2)
				elif parsed[0] == "/backupchar":
					index = g.get_player_index(e.peer_id)
					if index > -1 and (g.players[index].is_admin() or g.players[index].dev):
						def send_backup_menu(player_index, path):
							m = server_menu()
							m.intro = "Select Backup:"
							m.initial_packet = "backup_selected"
							g.players[player_index].current_menu = "backup_select"

							backup_folders = find_directories(path)
							backup_folders.sort(reverse=True)

							if backup_folders:
								for folder in backup_folders:
									# URL kodlama kullanılarak boşluklar güvenli hale getirilir
									encoded_folder = urllib.parse.quote_plus(folder)
									m.add(folder, encoded_folder) # Görünen ad hala orjinal kalır, fakat gönderilen kimlik kodlanmış olur
							else:
								m.add("No Backups Found", "no_backups", False)
								adminsend(f"[{g.players[player_index].name}] attempted to access backups, but no backup folder was found!")

							g.n.send_reliable(g.players[player_index].peer_id, "play_s menuopen.ogg", 0)
							m.send(g.players[player_index].peer_id)

						backups_directory = "backups"

						if not os.path.exists(backups_directory):
							adminsend(f"[{g.players[index].name}] attempted to access backups, but the 'backups' directory does not exist!")
							g.n.send_reliable(e.peer_id, "Backup directory not found!", 0)
							return

						send_backup_menu(index, backups_directory)
					else:
						g.n.send_reliable(e.peer_id, "You do not have permission to use this command.", 0)
						return
				elif parsed[0] == "/timeditemlist":
					if g.players[index].is_admin():
						adminsend("" + g.players[index].name + " checked all timed items")
						m = server_menu()
						m.initial_packet = "timeditemlist_menu"
						m.intro = "Active Timed Items List"
						
						if len(g.timeditems) == 0:
							m.add("No active timed items found.", "none", False)
						else:
							sorted_items = reversed(sorted(g.timeditems, key=lambda x: (x.duration - x.timer.elapsed)))
							
							for i in sorted_items:
								time_left = i.duration - i.timer.elapsed
								if time_left > 0:
									readable_time = ms_to_readable_time(time_left)
									info_str = f"Item: {i.itemname}, Owner: {i.owner}, Expires in: {readable_time}"
									# Using a unique ID combination for the menu ID to ensure uniqueness if needed
									menu_id = f"{i.owner}_{i.itemname}"
									m.add(info_str, menu_id, False)
						
						m.send(e.peer_id)
					else:
						g.n.send_reliable(e.peer_id, "You do not have permission to use this command.", 0)
				elif parsed[0]=="/paid_list":
					if not g.players[index].is_admin():
						g.n.send_reliable(peer_id, "You do not have permission to use this command.", 0)
						return
					peer_id=g.players[index].peer_id
					SECONDS_IN_ONE_MONTH = 2592000
					now = int(tm.time())
					paid_accounts = []
					char_dir = "chars"

					if not directory_exists(char_dir):
						g.n.send_reliable(peer_id, "Error: 'chars' directory not found.", 0)
						return

					for char_name in os.listdir(char_dir):
						char_path = os.path.join(char_dir, char_name)
						if not os.path.isdir(char_path):
							continue

						paid_flag_file = os.path.join(char_path, "paid.usr")
						paid_time_file = os.path.join(char_path, "paidtime.usr")
						paid_months_file = os.path.join(char_path, "paidmonths.usr")

						if file_exists(paid_flag_file) and file_exists(paid_time_file) and file_exists(paid_months_file):
							try:
								paid_time = int(file_get_contents(paid_time_file))
								paid_months = float(file_get_contents(paid_months_file))
								time_left = paid_time + paid_months - now

								if time_left > 0:
									days = int(time_left / (60 * 60 * 24))
									hours = int((time_left % (60 * 60 * 24)) / (60 * 60))
									minutes = int((time_left % (60 * 60)) / 60)
									paid_accounts.append((char_name, days, hours, minutes, time_left))
								else:
									paid_accounts.append((char_name, 0, 0, 0, 0))  # Süresi dolmuş
							except ValueError:
								g.n.send_reliable(peer_id, f"Error reading paid info for {char_name}.", 0)

					# Süreye göre sırala (en uzun süreden en kısaya)
					paid_accounts.sort(key=lambda x: x[4], reverse=True)

					m=server_menu()
					m.intro="list of paid accounts"
					m.initial_packet="paidlist"
					for char_name, days, hours, minutes, time_left in paid_accounts:
						if time_left > 0:
							m.add(f"{char_name}: {days} days, {hours} hours, {minutes} minutes remaining.\n",char_name,False)
						else:
							m.add(f"{char_name}: Subscription expired.\n",char_name,False)

					m.send(peer_id)
					adminsend(f"{g.players[index].name} used the /paid_list command.")
				elif(parsed[0]=="/kick" and len(parsed)>1):
				
					if(g.players[index].is_admin() or g.players[index].moderator==True):
					
						ind2=g.get_player_index_from(parsed[1])
						if(ind2>-1):
						
							adminsend(""+g.players[ind2].name+" has been kicked from the game by "+g.players[index].name+"")
							remove_from_server(ind2)
							
						
					
				elif parsed[0]=="/moveall":
					for i in range(len(g.players)):
						if g.players[i].map=="massacre_in_the_city": g.players[i].parachuted=True; g.n.send_reliable(g.players[i].peer_id, "parachute_start", 0); move_player(i,5,0,0,"massacre_in_the_city"); g.players[i].parachuted=False; g.n.send_reliable(g.players[i].peer_id, "parachute_stop", 0)
					g.n.send_reliable(g.players[index].peer_id,"done",2)
				elif(parsed[0]=="/move" and len(parsed)>4):
				
					if(g.players[index].is_admin() or g.players[index].moderator==True or g.players[index].builder==True):
					
						ind2=g.get_player_index_from(parsed[1])
						if(ind2>-1):
						
							try:
								x=string_to_number(parsed[2])
								y=string_to_number(parsed[3])
								z=string_to_number(parsed[4])
								map=g.players[ind2].map
								move_player(ind2, x, y, z, map)
								adminsend(""+g.players[index].name+" moved "+g.players[ind2].name+" to "+str(x)+" "+str(y)+" "+str(z)+"")
								g.n.send_reliable(g.players[index].peer_id,"done",0)
							except:
								g.n.send_reliable(g.players[index].peer_id,"Invalid Syntax For This Command.",0)
							
						
					
				
			
		
	


