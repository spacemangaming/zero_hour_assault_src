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

def handle_gameplay_1(e, parsed, index):
	global languages
	cmds = {"talking", "talking2", "gamemenu", "playermenu", "admin_ticket_action_menu", "is_typing", "wakeup", "ticket_create_message", "suggestsomething", "friendpm", "selectchannel", "resetfriends", "playermenuchoose", "voiceoff2", "packopen", "pollcomment_submit", "ticketview_select_action", "voiceon", "voicechatvolume", "ticket_create_title", "admin_ticket_action_chosen", "friendpmsend", "ticket_add_message_submit", "voteview", "vote", "ticket_action_chosen", "voiceon2", "voiceoff", "is_not_typing", "playermenuchoose2", "getdate", "writeitemdata", "ticket_rate_submit", "trackobj"}
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

	if (e.channel==0):
	

		parsed=string_split(e.message, " ", True)
		if parsed[0]=="voicechatvolume" and parsed[1]=="back": return
		if parsed[0]=="voicechatvolume" or parsed[0]=="trackobj": g.n.send_reliable(e.peer_id,e.message,e.channel)
		if parsed[0]=="voiceon":
			index=get_player_index(e.peer_id)
			if index>-1:
				g.players[index].voiceon=1
		if parsed[0]=="voiceoff":
			index=get_player_index(e.peer_id)
			if index>-1:
				g.players[index].voiceon=0
		if parsed[0]=="voiceon2":
			index=get_player_index(e.peer_id)
			if index>-1:
				g.players[index].voiceon2=1
		if parsed[0]=="voiceoff2":
			index=get_player_index(e.peer_id)
			if index>-1:
				g.players[index].voiceon2=0

		if parsed[0]=="talking":
			index=get_player_index(e.peer_id)
			if index>-1:
				if g.players[index].voicemessage2==0: g.n.send_reliable(e.peer_id,"You disabled receiving voicechats",0); return
				m=server_menu()
				m.intro="talking players. Press enter on one player to adjust their voicechat volume."
				m.initial_packet="voicechatvolume"
				send_to=[]
				if 1:
					for i in g.players:
						if i.voiceon==0 or i.hidden or g.players[index].name in i.blocks or i.name in send_to or i.voicemessage==0: continue
						if i.name==g.players[index].name and g.players[index].listen==1: m.add(i.name,i.name); send_to.append(i.name); continue
						if i.name==g.players[index].name and g.players[index].listen==0: continue
						if i.map!=g.players[index].map: continue
						if i.name not in send_to: m.add(i.name,i.name); send_to.append(i.name)

				if g.players[index].voicechatmap==1:
					for i in g.players:
						if i.voiceon==0 or i.hidden or g.players[index].name in i.blocks or i.name in send_to or i.voicemessage==0: continue
						if i.name==g.players[index].name and g.players[index].listen==1: m.add(i.name,i.name); send_to.append(i.name); continue
						if i.name==g.players[index].name and g.players[index].listen==0: continue
						if i.map!=g.players[index].map: continue
						m.add(i.name,i.name); send_to.append(i.name)
				if g.players[index].voicechatgroup==1:
					for i in g.players:
						if i.voiceon==0 or i.hidden or g.players[index].name in i.blocks or i.name in send_to or i.voicemessage==0: continue
						if i.name==g.players[index].name and g.players[index].listen==1: m.add(i.name,i.name); send_to.append(i.name); continue
						if i.name==g.players[index].name and g.players[index].listen==0: continue
						if i.group!=g.players[index].group: continue
						m.add(i.name,i.name); send_to.append(i.name)

				if g.players[index].voicechatteam==1:
					for i in g.players:
						if i.voiceon==0 or i.hidden or g.players[index].name in i.blocks or i.name in send_to or i.voicemessage==0: continue
						if i.name==g.players[index].name and g.players[index].listen==1: m.add(i.name,i.name); send_to.append(i.name); continue
						if i.name==g.players[index].name and g.players[index].listen==0: continue
						if i.matchteam!=g.players[index].matchteam and i.matchteam!="" and g.players[index].matchteam!="": continue
						m.add(i.name,i.name); send_to.append(i.name)
				if g.players[index].voicechatfriend==1:
					for i in g.players:
						if i.voiceon==0 or i.hidden or g.players[index].name in i.blocks or i.name in send_to or i.voicemessage==0: continue
						if i.name==g.players[index].name and g.players[index].listen==1: m.add(i.name,i.name); send_to.append(i.name); continue
						if i.name==g.players[index].name and g.players[index].listen==0: continue
						if i.name not in g.players[index].friendlist: continue
						m.add(i.name,i.name); send_to.append(i.name)
				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"no one talking",0); return
				m.send(e.peer_id)
		if parsed[0]=="talking2":
			index=get_player_index(e.peer_id)
			if index>-1:
				if g.players[index].voicemessage2==0: g.n.send_reliable(e.peer_id,"You disabled receiving voicechats",0); return
				m=server_menu()
				m.intro="talking players. Press enter on one player to adjust their voicechat volume."
				m.initial_packet="voicechatvolume"

				send_to=[]
				if 1:
					for i in g.players:
						if i.voiceon2==0 or i.hidden or g.players[index].name in i.blocks or i.name in send_to or i.voicemessage2==0: continue
						if i.name==g.players[index].name and g.players[index].listen==1: m.add(i.name,i.name); send_to.append(i.name); continue
						if i.name==g.players[index].name and g.players[index].listen==0: continue
						if i.community!=g.players[index].community: continue
						if i.name not in send_to: m.add(i.name,i.name); send_to.append(i.name)

				if 1:
					for i in g.players:
						if i.voiceon2==0 or i.hidden or g.players[index].name in i.blocks or i.name in send_to or i.voicemessage2==0: continue
						if i.name==g.players[index].name and g.players[index].listen==1: m.add(i.name,i.name); send_to.append(i.name); continue
						if i.name==g.players[index].name and g.players[index].listen==0: continue
						if i.community!=g.players[index].community: continue
						m.add(i.name,i.name); send_to.append(i.name)

				if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"no one talking",0); return
				m.send(e.peer_id)

		if parsed[0]=="is_typing":
			index=get_player_index(e.peer_id)
			if index>-1:
				if g.players[index].hidden: return
				x=get_player_index_from(parsed[1])
				if x>-1:
					if not g.players[index].disable_pm_chat_check2(): return
					if not g.players[index].disable_all_chat_check2(): return
					if not g.players[x].disable_pm_chat_check2(): return
					if not g.players[x].disable_all_chat_check2(): return
				if x>-1 and g.players[x].istyping==1 and g.players[x].friendmessage==1:
					if 1:
						if 1:
							try: blocks=pickle.loads(file_get_contents("chars/"+parsed[1]+"/blocks.usr","rb"))
							except: blocks=[]
							if g.players[index].name in blocks: return
							try: blocks=pickle.loads(file_get_contents("chars/"+g.players[index].name+"/blocks.usr","rb"))
							except: blocks=[]
							if parsed[1] in blocks: return


					g.n.send_reliable(g.players[x].peer_id,"friend "+g.players[index].name+" is typing...",0)
					g.n.send_reliable(g.players[x].peer_id,"play_s keyenter"+str(random(2,3))+".ogg",0)
		if parsed[0]=="is_not_typing":
			index=get_player_index(e.peer_id)
			if index>-1:
				if g.players[index].hidden: return
				x=get_player_index_from(parsed[1])
				if x>-1 and g.players[x].istyping==1:
					if not g.players[index].disable_pm_chat_check2(): return
					if not g.players[index].disable_all_chat_check2(): return
					if not g.players[x].disable_pm_chat_check2(): return
					if not g.players[x].disable_all_chat_check2(): return
					if 1:
						if 1:
							try: blocks=pickle.loads(file_get_contents("chars/"+parsed[1]+"/blocks.usr","rb"))
							except: blocks=[]
							if g.players[index].name in blocks: return
							try: blocks=pickle.loads(file_get_contents("chars/"+g.players[index].name+"/blocks.usr","rb"))
							except: blocks=[]
							if parsed[1] in blocks: return



					g.n.send_reliable(g.players[x].peer_id,"friend "+g.players[index].name+" is not typing",0)
					g.n.send_reliable(g.players[x].peer_id,"play_s keyenter"+str(random(2,3))+".ogg",0)

		if parsed[0]=="getdate": g.n.send_reliable(e.peer_id,"dateis "+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),0)
		if parsed[0]=="wakeup":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				for p in g.players:
					if p.name==g.players[index].name: continue
					if g.players[index].distancecheck(p.x,p.y,p.z)<=3 and p.map==g.players[index].map and p.faint:
						p.faint=False
						p.fainted=False
						g.n.send_reliable(e.peer_id,"You waked up "+p.name,0)
						g.n.send_reliable(p.peer_id,"startmoving",0)
						g.n.send_reliable(p.peer_id,g.players[index].name+" waked you",0)
						g.play(p.get_current_char()+"voice32",p.x,p.y,p.z,p.map)
				for p in g.npcs:
					if g.players[index].distancecheck(p.x,p.y,p.z)<=3 and p.map==g.players[index].map and p.faint and p.matchteam==g.players[index].matchteam:
						p.faint=False
						p.fainted=False
						p.stunned=False
						g.n.send_reliable(e.peer_id,"You waked up "+p.name,0)
						g.play("voice32",p.x,p.y,p.z,p.map)
		if parsed[0]=="writeitemdata":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				if g.players[index].ios: file_put_contents("ioszitemdata.txt", e.message.replace("writeitemdata ","")+"\n", "a")
				elif not g.players[index].ios: file_put_contents("zitemdata.txt", e.message.replace("writeitemdata ","")+"\n", "a")
		if parsed[0]=="resetfriends":
			for p in g.players: p.friendcount=0
		if parsed[0]=="gamemenu":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				m=server_menu()
				m.intro="Game menu"
				m.initial_packet="gamemenuopt"
				if g.players[index].jailed:
					if g.players[index].jailtime!=100000000*60000: m.add("You are jailed for the following reason: "+g.players[index].jailreason+". You will be unjailed after "+ms_to_readable_time(g.players[index].jailtime-g.players[index].jailtimer.elapsed),"jail",False)
					if g.players[index].jailtime==100000000*60000: m.add("You are jailed for the following reason: "+g.players[index].jailreason+".","jail")
				if g.players[index].map=="helicopter" or g.players[index].map=="massacre_in_the_city":
					m.add("Leave from freedom fight map","free")
				if match_exists(g.players[index].joinedmatch) and g.players[index].name==g.players[index].joinedmatch: m.add("Cancel the match","cancel")

				m.add("Character Stats, Check the properties of your account, your score points, rank, amount of tokens, etc.","stats")
				m.add("Change character, View the characters you have and switch to those characters. Notes. You can only change your character in the lobby and waiting part of the match.","char")
				if (g.players[index].map!="massacre_in_the_city" and g.players[index].map!="helicopter") or string_contains(g.players[index].map,"base",1)>-1:
					m.add("Store, Spend the zero tokens you have, view the packages you have purchased, or buy tokens from the virtual store.","store")

				m.add("Account settings, Update your account password, rename your character, set a status message, see your rename history, Modify your registered email, delete your account, View Login History and See which devices have accessed your account and block unauthorized devices.","security")
				m.add("events, Upcoming Events.","events")
				m.add("See your motors","motor")
				m.add("See your bikes","bike")
				m.add("Game settings, Change your game settings.","setting")
				m.add("Friend menu, Send a friend request, View Pending Friend Requests, Remove Friend.","friend")
				m.add("Group menu, Start a new group for collaboration, View Group Invitations, Manage Group Members.","group")
				m.add("community menu, Create a new community for talk, View community Invitations, Manage community Members.","community")

				m.add("Poll menu, create polls, vote on existing polls","vote")

				m.add("Make suggestions, leave feedback, report bugs.","suggest")
				m.add("view scoreboard","viewscoreboard")
				m.add("View rules, View the game rules, read the rules to avoid making mistakes in the game.","rules")

				m.add("view all groups, View groups created in the game, view how many kills and how many deaths they have, send a request to join a group.","groupinfo")
				m.add("view all communitys, View communitys created in the game, send a request to join a community.","communityinfo")

				m.add("View destroyed groups history","groupinfo2")
				m.add("View timed item expiry times","timed")
				m.add("View Latest Additions","latest")
				m.add("View Announcements, See latest news and updates from admins.","announcements")
				#m.add("View game readme file, learn the game about.","readme")

				m.add("languages, Manage Languages, Switch to a Language, Get syntax and usage tips for creating languages, Create New Language.","langg")
				if g.players[index].moderator==True or g.players[index].is_admin()==True or g.players[index].dev==True:

					m.add("Staff List, View All Staff Members.","staff")
				m.add("Server Status.","status")
				m.add("notification settings, Customize Notification Alerts.","nsetting")
				m.add("ticket menu, Submit a new support request, View Your Previous Tickets.","ticket")
				if g.players[index].dev==True or g.players[index].is_admin()==True or g.players[index].moderator==True:
					m.add("staff menu, manage the game","adminmenu")
				m.send(e.peer_id)
		if parsed[0]=="suggestsomething":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				if parsed[1]=="[cncel]": g.players[index].prevmenu(); return
				message=e.message.replace("suggestsomething ","")
				file_put_contents("suggest.txt", ""+g.players[index].name+": "+message+", "+get_date()+", "+get_time(True, True)+"\n", "a")
				g.n.send_reliable(g.players[index].peer_id,"Your message has been delivered to the staff team.",0)
				g.players[index].suggesttimer.restart()
				adminsend(""+g.players[index].name+" suggested: "+message+"")
				notify_admins("zero hour assault, "+g.players[index].name+" suggested: "+message+"")
		if parsed[0]=="friendpmsend":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				if parsed[1]=="[cncel]": return
				message=e.message.replace("friendpmsend ","")
				if g.players[index].pmmessage==0: g.n.send_reliable(e.peer_id,"You can't send pm to someone while your pm notifications are disabled.",0); return
				x=get_player_index_from(g.players[index].friendmanage)
				if x>-1 and g.players[x].istyping==1:
					g.n.send_reliable(g.players[x].peer_id,"friend "+g.players[index].name+" is typing...",0)
					g.n.send_reliable(g.players[x].peer_id,"play_s keyenter"+str(random(2,3))+".ogg",0)
				g.n.send_reliable(e.peer_id,"echocommand /pm "+g.players[index].friendmanage+" "+message,0)
				g.players[index].prevmenu()
		if parsed[0]=="selectchannel":
			index=get_player_index(e.peer_id)
			if index>-1:
				menu=server_menu()
				menu.intro="Select a channel to switch."
				menu.initial_packet="lchannelset"
				lc=string_split(file_get_contents("languages.txt"), "\n", False)				
				for i in range(len(lc)):
#					if lc[i]==g.players[index].langchan:
#						continue
					menu.add(lc[i], lc[i])
				menu.add("Disable_chat", "disable")
				menu.send(e.peer_id)
		if parsed[0] == "friendpm":
			index = g.get_player_index(e.peer_id)
			if index > -1:
				if len(g.players[index].friendlist) <= 0:
					g.n.send_reliable(g.players[index].peer_id, "You don't have a friend you can send a private message to.", 0)
					return
				if len(g.players[index].friendlist) > 0:
					m = server_menu()
					m.intro = "Select player to send private message. Press shift enter on a player to copy their name to clipboard."
					m.initial_packet = "friendpmchoose"
					for pl in g.players[index].friendlist:
						if pl != g.players[index].name:
							if pl not in m.menuids and get_player_index_from(pl) > -1 and not g.players[get_player_index_from(pl)].hidden:
								m.add(pl + ", online", pl)
					
					offline_players = []
					for pl in g.players[index].friendlist:
						if pl != g.players[index].name:
							if pl not in m.menuids:
								last_active = file_get_contents("chars/" + pl + "/lastactive.usr")
								try:
									last_active_datetime = datetime.strptime(last_active, "%Y-%m-%d %H:%M:%S")
									offline_players.append((pl, last_active_datetime))
								except ValueError:
									pass
					offline_players.sort(key=lambda x: x[1], reverse=True)
					for pl, last_active_datetime in offline_players:
						time_difference = get_datetime_difference(last_active_datetime.strftime("%Y-%m-%d %H:%M:%S"))
						m.add(f"{pl}, offline, was last active {time_difference} ago.", pl)
					
					m.send(e.peer_id)
		if parsed[0]=="packopen":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				if parsed[1]=="back": return
				pack=parsed[1]
				if g.players[index].storeget_item_count(pack)<=0: g.n.send_reliable(e.peer_id,"You don't have any "+pack,0); g.players[index].prevmenu(); return
				g.players[index].storegive(pack,-1)
				try: g.players[index].zhtoken+=get_zero_token_amount(pack)
				except: pass
				g.n.send_reliable(e.peer_id,"play_s misc"+str(random(77,79))+".ogg",0)
				g.n.send_reliable(e.peer_id,"you received "+str(get_zero_token_amount(pack))+" zero tokens from the packs",0)
				if not g.players[index].hidden: g.n.broadcast(g.players[index].name+" opened a "+pack+" and received "+str(get_zero_token_amount(pack))+" zero tokens",2)
				g.players[index].prevmenu()
		if parsed[0]=="playermenuchoose2":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				ind=g.get_player_index_from(g.players[index].playeract)
				if ind==-1: g.n.send_reliable(e.peer_id,"Player not found",0); g.players[index].prevmenu(); return
				if parsed[1]=="status":
					if g.players[ind].status=="": g.n.send_reliable(g.players[index].peer_id,""+g.players[index].playeract+" did not set a status message",0); g.players[index].prevmenu(); return
					g.n.send_reliable(g.players[index].peer_id,"Status for "+g.players[index].playeract+": "+g.players[ind].status+"",0); g.players[index].prevmenu(); return

				if parsed[1]=="volume": g.n.send_reliable(e.peer_id,"voicechatvolume "+g.players[index].playeract,0)
				if parsed[1]=="pm":
					g.players[index].friendmanage=g.players[index].playeract
					send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "friendpmsend", "Enter the private message you want to send to "+g.players[index].playeract)
				if parsed[1]=="token":
					send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "tokentransfer", "Please enter the amount of zero tokens you want to transfer.")
				if parsed[1]=="block":
					if g.players[ind].name in g.players[index].blocks: g.n.send_reliable(e.peer_id,"Removed "+g.players[ind].name+"'s block",0); g.players[index].blocks.remove(g.players[ind].name); save_all_chars()
					elif g.players[ind].name not in g.players[index].blocks: g.n.send_reliable(e.peer_id,"Blocked "+g.players[ind].name,0); g.players[index].blocks.append(g.players[ind].name); save_all_chars()
				if parsed[1]=="friendaccept":
					i=get_player_index_from(g.players[index].playeract)
					try: g.players[index].pendingfriendlist.remove(g.players[index].playeract)
					except: pass
					if i>-1: g.players[i].friendlist.append(g.players[index].name)
					else:
						flist=pickle.loads(file_get_contents("chars/"+g.players[index].playeract+"/friendlist.usr","rb"))
						flist.append(g.players[index].name)
						file_put_contents("chars/"+g.players[index].playeract+"/friendlist.usr",pickle.dumps(flist),"wb")
					g.players[index].friendlist.append(g.players[index].playeract)
					g.n.send_reliable(e.peer_id,"Done, friend request accepted successfully.",0)
					if i>-1: g.n.send_reliable(g.players[i].peer_id,"friend "+g.players[index].name+" accepted your friend request!",0)
					if i>-1: g.n.send_reliable(g.players[i].peer_id,"play_s misc10.ogg",0)
				if parsed[1]=="frienddecline":
					i=get_player_index_from(g.players[index].playeract)
					try: g.players[index].pendingfriendlist.remove(g.players[index].playeract)
					except: pass
					g.n.send_reliable(e.peer_id,"Done, friend request declined successfully.",0)
					if i>-1: g.n.send_reliable(g.players[i].peer_id,"friend "+g.players[index].name+" declined your friend request!",0)
					if i>-1: g.n.send_reliable(g.players[i].peer_id,"play_s misc10.ogg",0)


				if parsed[1]=="friend" and g.players[ind].name not in g.players[index].friendlist:
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
					if g.players[ind].friendmessage==0: g.n.send_reliable(e.peer_id,"Error, you can't send friend request to this player because they turned of receiving friend requests.",0); g.players[index].prevmenu(); return
					if g.players[index].name in g.players[ind].pendingfriendlist:
						g.n.send_reliable(e.peer_id,"You've already sent friend request to this player.",0)
						g.players[index].prevmenu() 
						return
					if g.players[index].name in g.players[ind].friendlist:
						g.n.send_reliable(e.peer_id,"You've already added this player as friend.",0)
						g.players[index].prevmenu() 
						return
					if g.players[ind].name in g.players[index].pendingfriendlist:
						g.n.send_reliable(e.peer_id,"This player already sent friend request to you",0)
						g.players[index].prevmenu() 
						return
					if g.players[index].name in g.players[ind].blocks: g.n.send_reliable(e.peer_id,"this player has blocked you",0); 					g.players[index].prevmenu(); return
					g.players[ind].pendingfriendlist.append(g.players[index].name)
					g.players[index].prevmenu()
					g.n.send_reliable(e.peer_id,"Done, friend request sent successfully.",0)
					g.n.send_reliable(g.players[ind].peer_id,"play_s misc10.ogg",0)
					g.n.send_reliable(g.players[ind].peer_id,"friend "+g.players[index].name+" wants to add you as friend!",0)
				name=g.players[index].name
				name2=g.players[ind].name
				if parsed[1]=="friend" and g.players[ind].name in g.players[index].friendlist and send_yesno_question(g.players[index].peer_id,"Are you sure you want to remove this friend?")=="yes":
					index=get_player_index_from(name)
					ind=get_player_index_from(name2)
					try: g.players[index].friendlist.remove(g.players[ind].name)
					except: pass
					if ind>-1:
						try: g.players[ind].friendlist.remove(g.players[index].name)
						except: pass
					g.n.send_reliable(g.players[index].peer_id,"Done, friend removed successfully.",0)
					g.players[index].prevmenu()
					if ind>-1: g.n.send_reliable(g.players[ind].peer_id,"play_s misc10.ogg",0)
					if ind>-1: g.n.send_reliable(g.players[ind].peer_id,"friend "+g.players[index].name+" removed you from their friend list!",0)
				if parsed[1]=="stats":
					m=server_menu()
					m.intro="character stats menu."
					m.initial_packet="stats"
					m.add("current character, "+g.players[ind].current_char+"","test123",False)
					m.add("Gender, "+g.players[ind].gender+"","test123",False)
					if g.players[ind].paid: m.add("This player is paid account","paid",False)
					if not g.players[ind].paid: m.add("This player is free account","paid",False)
					if g.players[ind].backpacks_level!=0:
						m.add("this player has backpacks level "+str(g.players[ind].backpacks_level)+"","backpacks",False)
					m.add("Score point, "+str(g.players[ind].scorepoint)+"","lolllll",False)
					m.add("Score Rank, "+g.players[ind].scorerank+"","lolasdlasdl",False)
					if g.players[ind].group!="": m.add("group, "+g.players[ind].group,"group",False)
					if g.players[ind].community!="": m.add("community, "+g.players[ind].community,"group",False)
					if g.players[ind].adrenaline:
						m.add("adrenaline shot on, will expire after "+ms_to_readable_time(120000-g.players[ind].adrenalinetimer.elapsed),"adr",False)
					if g.players[ind].jammer:
						m.add("jammer on, will expire after "+ms_to_readable_time(120000-g.players[ind].jammertimer.elapsed),"adr",False)

					m.add("bot kills, "+str(g.players[ind].botkills),"kills",False)
					m.add("bot deaths, "+str(g.players[ind].botdeaths),"deaths",False)
					m.add("player kills, "+str(g.players[ind].playerkills),"kills2",False)
					m.add("player deaths, "+str(g.players[ind].playerdeaths),"deaths2",False)
					m.add("amount of headshots made, "+str(g.players[ind].headshots),"head")
					m.add("amount of headshots got, "+str(g.players[ind].headhits),"head")
					m.add("amount of legshots made, "+str(g.players[ind].legshots),"leg")
					m.add("amount of legshots got, "+str(g.players[ind].leghits),"leg")
					if g.players[ind].lang=="": m.add("This player is using the language english","lang",False)
					else: m.add("This player is using the language "+g.players[ind].lang,"lang",False)

#					m.add("zero token amount, "+str(g.players[ind].zhtoken)+"","test123",False)
					m.add("Time elapsed since this account is created: "+get_datetime_difference(file_get_contents("chars/"+g.players[index].playeract+"/createdate.usr"))+".","elapsed",False)
					if g.players[ind].langchan=="disable":
						m.add("Chat language, disabled.","a",False)

					if g.players[ind].langchan!="disable":
						m.add("Chat language, "+g.players[ind].langchan+"","a",False)
					if g.players[ind].android==True: m.add("Client platform: Android","askdjaskjdsakjadkjsa",False)
					if g.players[ind].ios==True: m.add("Client platform: iOS","askdjaskjdsakjadkjsa",False)

					if g.players[ind].android==False and g.players[ind].ios==False: m.add("Client platform: Windows","askdjaskjdsakjadkjsa",False)

					m.add("Client version: "+g.players[ind].version+"","asdsadas",False)
					m.add("Rank: "+g.players[ind].title2+"","asdsadas",False)

					m.send(e.peer_id)


		if parsed[0]=="playermenuchoose":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				if parsed[1]=="back": return
				if len(g.players)>0:
					m=server_menu()
					m.intro="Select an option"
					m.initial_packet="playermenuchoose2"
					g.players[index].playeract=parsed[1]
					m.add("View stats","stats")
					m.add("view status message","status")
					#if parsed[1] in g.players[index].friendlist: m.add("send pm","pm")
					if(parsed[1] not in g.players[index].blocks) and parsed[1]!=g.players[index].name: m.add("Block this player from sending you private messages","block")
					if(parsed[1] in g.players[index].blocks): m.add("Unblock this player from sending you private messages","block")
					m.add("change voicechat volume","volume")
					if parsed[1] in g.players[index].friendlist: m.add("Remove from friend list","friend")
					#if parsed[1] in g.players[index].friendlist: m.add("Send private message","pm")
					if g.players[index].name!=g.players[index].playeract and parsed[1] not in g.players[index].pendingfriendlist and parsed[1] not in g.players[index].friendlist: m.add("Send friend request","friend")
					if parsed[1] in g.players[index].pendingfriendlist and parsed[1] not in g.players[index].friendlist: m.add("Accept friend request from this player","friendaccept")
					if parsed[1] in g.players[index].pendingfriendlist and parsed[1] not in g.players[index].friendlist: m.add("Decline friend request from this player","frienddecline")

					if parsed[1]!=g.players[index].name: m.add("Transfer zero token","token")
					m.send(e.peer_id)
		"""
		if parsed[0]=="playermenu":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				if len(g.players)>0:
					m = server_menu()
					m.intro = "Players menu: There are " + str(len(g.players)) + " connected players."
					m.initial_packet = "playermenuchoose"

					for pl in g.players:
						if pl.hidden: continue
						if pl.name not in m.menuids:
							if pl.dev:
								role = "Developer"
#							elif pl.is_admin():
#								role = "Administrator"
#							elif pl.moderator==True:
#								role = "Moderator"

#							elif pl.builder:
#								role = "Builder"
							else:
								role = ""
							if pl.map == "jail" and pl.jailed:
								if pl.jailtime!=100000000*60000: m.add(f"{pl.name}, {role}, jailed for {pl.jailreason}, will be unjailed after {ms_to_readable_time(pl.jailtime-pl.jailtimer.elapsed)}", pl.name)
								else: m.add(f"{pl.name}, {role}, jailed for {pl.jailreason}", pl.name)
							elif pl.map == "massacre_in_the_city":
								m.add(f"{pl.name}, {role}, in the freedom fight map", pl.name)

							elif pl.map.startswith("basement"):
								for base in g.group_bases:
									if "basement"+base.name+base.mapappend==pl.map:
										m.add(f"{pl.name}, {role}, in the base of {base.name}", pl.name)
							elif pl.specplayer == "" and pl.map == "lobby":
								m.add(f"{pl.name}, {role}, in the lobby", pl.name)
							elif pl.specplayer != "" and pl.map == "lobby":
								added=False
								for ma in g.matches:
									if pl.specplayer in ma.players:
										m.add(f"{pl.name}, {role}, watching {pl.specplayer} in the match of {ma.owner}, match mode is {ma.get_mode()}", pl.name); added=True
								if not added: m.add(f"{pl.name}, {role}, watching {pl.specplayer} in the freedom fight map", pl.name); added=True
							elif pl.map.startswith("match") and pl.matchmode != "":
								m.add(f"{pl.name}, {role}, in the waiting area of the {get_match_name(pl.matchmode)}", pl.name)
							elif not pl.map.startswith("match") and pl.map != "lobby" and pl.matchmode != "":
								m.add(f"{pl.name}, {role}, playing {get_match_name(pl.matchmode)}", pl.name)
							elif pl.map!="helicopter" and pl.map.startswith("helicopter") and pl.matchmode != "":
								m.add(f"{pl.name}, {role}, in the helicopter of the {get_match_name(pl.matchmode)}", pl.name)
							elif pl.map=="helicopter":
								m.add(f"{pl.name}, {role}, in the helicopter of the freedom fight map", pl.name)

							else:
								m.add(f"{pl.name}, {role}", pl.name)

					m.send(e.peer_id)
"""
		if parsed[0]=="playermenu":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				if len(g.players)>0:
					m = server_menu()

					android_count = sum(1 for pl in g.players if pl.android and not pl.hidden)
					ios_count = sum(1 for pl in g.players if pl.ios and not pl.hidden)

					windows_count = sum(1 for pl in g.players if (not pl.android and not pl.ios and not pl.hidden))
					visible_count = sum(1 for pl in g.players if not pl.hidden)

					m.intro = f"Players menu: There are {str(visible_count)} connected players.  {android_count} are Android, {ios_count} are iOS, {windows_count} are Windows."
					m.initial_packet = "playermenuchoose"

					for pl in g.players:
						if pl.hidden: continue
						if pl.name not in m.menuids:
							if pl.dev:
								role = "Developer"
#							elif pl.is_admin():
#								role = "Administrator"
#							elif pl.moderator==True:
#								role = "Moderator"

#							elif pl.builder:
#								role = "Builder"
							else:
								role = ""
							if pl.map == "jail" and pl.jailed:
								if pl.jailtime!=100000000*60000: m.add(f"{pl.name}, {role}, jailed for {pl.jailreason}, will be unjailed after {ms_to_readable_time(pl.jailtime-pl.jailtimer.elapsed)}", pl.name)
								else: m.add(f"{pl.name}, {role}, jailed for {pl.jailreason}", pl.name)
							elif pl.map == "massacre_in_the_city":
								m.add(f"{pl.name}, {role}, in the freedom fight map", pl.name)

							elif pl.map.startswith("basement"):
								for base in g.group_bases:
									if "basement"+base.name+base.mapappend==pl.map:
										m.add(f"{pl.name}, {role}, in the base of {base.name}", pl.name)
							elif pl.specplayer == "" and pl.map == "lobby":
								m.add(f"{pl.name}, {role}, in the lobby", pl.name)
							elif pl.specplayer != "" and pl.map == "lobby":
								added=False
								for ma in g.matches:
									if pl.specplayer in ma.players:
										m.add(f"{pl.name}, {role}, watching {pl.specplayer} in the match of {ma.owner}, match mode is {ma.get_mode()}", pl.name); added=True
								if not added: m.add(f"{pl.name}, {role}, watching {pl.specplayer} in the freedom fight map", pl.name); added=True
							elif pl.map.startswith("match") and pl.matchmode != "":
								m.add(f"{pl.name}, {role}, in the waiting area of the {get_match_name(pl.matchmode)}", pl.name)
							elif not pl.map.startswith("match") and pl.map != "lobby" and pl.matchmode != "":
								m.add(f"{pl.name}, {role}, playing {get_match_name(pl.matchmode)}", pl.name)
							elif pl.map!="helicopter" and pl.map.startswith("helicopter") and pl.matchmode != "":
								m.add(f"{pl.name}, {role}, in the helicopter of the {get_match_name(pl.matchmode)}", pl.name)
							elif pl.map=="helicopter":
								m.add(f"{pl.name}, {role}, in the helicopter of the freedom fight map", pl.name)

							else:
								m.add(f"{pl.name}, {role}", pl.name)

					m.send(e.peer_id)
		if parsed[0]=="pollcomment_submit":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				if parsed[1]=="[cncel]": g.players[index].prevmenu(); return
				if not g.players[index].disable_vote_check(): return

				comment_text = e.message.replace("pollcomment_submit ", "")
				current_poll = getattr(g.players[index], 'votecurrentpoll', None)
				if current_poll and not current_poll.ended:
					comment_data = {
						"author": g.players[index].name,
						"text": comment_text,
						"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
					}
					current_poll.comments.append(comment_data)
					g.n.send_reliable(e.peer_id, "Comment added successfully.", 0)
					# Notify other players in the poll that a new comment was added (optional, but good for engagement)
					for p in g.players:
						if p.votenotify==1 and p.name != g.players[index].name:
							# Check if this player is viewing or involved with this specific poll
							# (more complex check might be needed depending on how closely polls are tracked client-side)
							g.n.send_reliable(p.peer_id, f"A new comment was added to the poll '{current_poll.title}' by {g.players[index].name}.", 2)
					g.players[index].prevmenu() # Go back to the poll view
				else:
					g.n.send_reliable(e.peer_id, "Error: Poll not found or is ended.", 0)
				g.players[index].votecurrentpoll = None # Clear the stored poll object

		if parsed[0]=="vote":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				if parsed[1]=="back": return
				for v in g.votes:
					if g.players[index].vote==v.owner and v.title==g.players[index].votename and v.message==g.players[index].votemessage and v.id==g.players[index].voteid:

						#if v.ended: g.n.send_reliable(e.peer_id,"This vote is ended",0); g.players[index].prevmenu(); return
						if parsed[1]=="voteyes":
							if 1:
								if g.players[index].vote==v.owner and v.title==g.players[index].votename and v.message==g.players[index].votemessage and v.id==g.players[index].voteid:
									if g.players[index].name in v.yesvoters or g.players[index].name in v.novoters: g.n.send_reliable(e.peer_id,"You already voted",0); g.players[index].prevmenu(); return

							if not g.players[index].disable_vote_check(): return

							if g.players[index].name==v.owner and g.players[index].votename==v.title and g.players[index].votemessage==v.message and g.players[index].voteid==v.id: g.n.send_reliable(e.peer_id,"You cannot vote your own poll",0); g.players[index].prevmenu(); return
							v.yesvoters.append(g.players[index].name)
							g.n.send_reliable(e.peer_id,"done",0)
							for p in g.players:
								if p.name!=g.players[index].name and p.votenotify==1:
									g.n.send_reliable(p.peer_id,g.players[index].name+" voted yes to the "+v.owner+"'s poll",2)
									g.n.send_reliable(p.peer_id,"play_s misc288.ogg",0)
							g.players[index].prevmenu()
						if parsed[1]=="end":
							if v.ended: g.n.send_reliable(e.peer_id,"this poll is already ended",0); g.players[index].prevmenu(); return
							v.ended=True
							adminsend(g.players[index].name+" ended "+v.owner+"'s poll")
							for p in g.players:
								if p.name!=g.players[index].name and p.votenotify==1:
									g.n.send_reliable(p.peer_id,v.owner+"'s poll has been ended by "+g.players[index].name,2)
									g.n.send_reliable(p.peer_id,"play_s misc162.ogg",0)
							g.n.send_reliable(e.peer_id,"done",0)
							g.players[index].prevmenu()

						if parsed[1]=="stick":
							v.stick=not v.stick; v.timer.restart(); v.ended=False
							if v.stick: g.n.send_reliable(e.peer_id,"sticked",0)
							if not v.stick: g.n.send_reliable(e.peer_id,"unsticked",0)
							g.players[index].prevmenu()
						if parsed[1]=="delete":
							g.n.send_reliable(e.peer_id,"done",0)
							g.votes.remove(v); return
						if 1:
							if 1:
								if parsed[1] == "leavecomment":
									if not g.players[index].disable_vote_check(): return

									g.players[index].votecurrentpoll = v # Store the poll object for later
									send_serverbox(g.players[index].peer_id, 0, 500, 0, -1, "pollcomment_submit", "Enter your comment:")
								elif parsed[1] == "seepollcomments":
									if len(v.comments) == 0:
										g.n.send_reliable(e.peer_id, "No comments yet for this poll.", 0)
										g.players[index].prevmenu()
									else:
										m = server_menu()
										m.intro = f"Comments for '{v.title}'"
										m.initial_packet = "dummy_poll_comments" # Dummy packet for displaying
										for comment_data in v.comments:
											comment_str = f"{comment_data['author']}: {comment_data['text']} at {comment_data['timestamp']}"
											m.add(comment_str, comment_data['author'], False) # Act is False as these are just for viewing
										m.send(e.peer_id)
								# --- NEW POLL COMMENT COMMANDS END ---
						if parsed[1]=="voteno":
							if 1:
								if g.players[index].vote==v.owner and g.players[index].votename==v.title and g.players[index].votemessage==v.message and g.players[index].voteid==v.id:
									if g.players[index].name in v.yesvoters or g.players[index].name in v.novoters: g.n.send_reliable(e.peer_id,"You already voted",0); g.players[index].prevmenu(); return

							if not g.players[index].disable_vote_check(): return

							if g.players[index].name==v.owner and g.players[index].votename==v.title and g.players[index].votemessage==v.message and g.players[index].voteid==v.id: g.n.send_reliable(e.peer_id,"You cannot vote your own poll",0); g.players[index].prevmenu(); return
							v.novoters.append(g.players[index].name)
							g.n.send_reliable(e.peer_id,"done",0)
							for p in g.players:
								if p.name!=g.players[index].name and p.votenotify==1:
									g.n.send_reliable(p.peer_id,g.players[index].name+" voted no to the "+v.owner+"'s poll",2)
									g.n.send_reliable(p.peer_id,"play_s misc288.ogg",0)
							g.players[index].prevmenu()

		if parsed[0]=="voteview":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				if parsed[1]=="back": return
				votedata=e.message.replace(parsed[0]+" ","")
				for v in g.votes:
					if v.owner==votedata.split("{}[]")[0] and v.title==votedata.split("{}[]")[1] and v.message==votedata.split("{}[]")[2] and v.id==votedata.split("{}[]")[3]:
						g.players[index].vote=votedata.split("{}[]")[0]
						g.players[index].votename=votedata.split("{}[]")[1]
						g.players[index].votemessage=votedata.split("{}[]")[2]
						g.players[index].voteid=votedata.split("{}[]")[3]
						m=server_menu()
						m.intro="poll of "+votedata.split("{}[]")[0]
						m.initial_packet="vote"
						m.add("title: "+v.title,"title",False)
						m.add("message: "+v.message,"message",False)
						m.add("Yes voters: "+str(len(v.yesvoters))+", they are: "+convert_to_list2(v.yesvoters),"yes",False)
						m.add("no voters: "+str(len(v.novoters))+", they are: "+convert_to_list2(v.novoters),"no",False)
						if not v.ended: m.add("vote yes","voteyes")
						if not v.ended: m.add("vote no","voteno")
						# --- NEW: Add comment options to poll menu ---
						m.add("Leave a comment", "leavecomment")
						m.add(f"See comments ({len(v.comments)})", "seepollcomments")
						# --- End NEW ---
						if g.players[index].is_admin() or g.players[index].dev:
							if not v.stick: m.add("stick","stick")
							if v.stick: m.add("unstick","stick")
						if not v.ended and (g.players[index].dev or g.players[index].is_admin()): m.add("end the poll","end")
						if (g.players[index].dev or g.players[index].is_admin()): m.add("delete the poll","delete")
						m.send(e.peer_id)
		elif parsed[0]=="admin_ticket_action_menu":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				if parsed[1]=="back": g.players[index].prevmenu(); return
				g.players[index].ticket_selected_id = parsed[1] # Store selected ticket ID

				ticket_obj = find_ticket_by_id(g.players[index].ticket_selected_id)
				if ticket_obj is None: g.n.send_reliable(e.peer_id,"Error, ticket not found!",0); g.players[index].prevmenu(); return

				m = server_menu()
				m.intro = f"Admin actions for Ticket: {ticket_obj['title']}"
				m.initial_packet = "admin_ticket_action_chosen"

				# Display messages
				m.add("View Messages", "view_messages")
				m.add("Add Message", "add_message") # Admins can always add messages

				# Admin-specific actions
				if ticket_obj["closed"]:
					m.add("Reopen Ticket", "reopen_ticket")
				else:
					m.add("Close Ticket", "close_ticket")
				
				if ticket_obj["pending"]:
					m.add("Mark as Not Pending", "mark_not_pending")
				else:
					m.add("Mark as Pending", "mark_pending")

				m.send(e.peer_id)

		elif parsed[0]=="admin_ticket_action_chosen":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				if parsed[1]=="back": g.players[index].prevmenu(); return
				
				ticket_obj = find_ticket_by_id(g.players[index].ticket_selected_id)
				if ticket_obj is None: g.n.send_reliable(e.peer_id,"Error, ticket not found!",0); g.players[index].prevmenu(); return

				if parsed[1]=="view_messages":
					m = server_menu()
					m.intro = f"Messages for '{ticket_obj['title']}'"
					m.initial_packet = "dummy_ticket_messages" # Dummy for display
					message_lines = ticket_obj["messages"].split("\n")
					for line in message_lines:
						m.add(line, line, False)
					m.send(e.peer_id)

				elif parsed[1]=="add_message":
					send_serverbox(g.players[index].peer_id, 0, 1000, 0, -1, "ticket_add_message_submit", "Enter your message:") # Same handler as user message

				elif parsed[1]=="reopen_ticket":
					# Reopen ticket logic (copied from original /openticket)
					if not ticket_obj["closed"]: g.n.send_reliable(e.peer_id,"This ticket is not closed!",0); g.players[index].prevmenu(); return
					ticket_obj["closed"]=False
					ticket_obj["closetimer"].restart()
					ticket_obj["messages"]+="\nThis ticket was reopened by "+g.players[index].name+" at "+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
					ticket_obj["lastupdate"]=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
					adminsend(g.players[index].name+" reopened the "+ticket_obj["title"]+" ticket.")
					notify_admins("zero hour assault, "+g.players[index].name+" reopened the "+ticket_obj["title"]+" ticket.")
					g.n.send_reliable(e.peer_id,"Done, ticket reopened successfully.",0)
					getmail=file_get_contents("chars/"+ticket_obj["owner"]+"/mail.usr")
					if is_enabled_ticket_mail(ticket_obj["owner"]): send_mail(getmail,"your ticket "+ticket_obj["title"]+" has been reopened","Hello "+ticket_obj["owner"]+"<br>your ticket "+ticket_obj["title"]+" has been reopened by "+g.players[index].name+"<br>We will answer you as soon as possible. We will resolve your issue soon.<br>regards,<br>Nbm studios team")
					if g.players[index].name!=ticket_obj["owner"]:
						ind=g.get_player_index_from(ticket_obj["owner"])
						if ind>-1: g.n.send_reliable(g.players[ind].peer_id,"Your ticket with id "+ticket_obj["id"]+" is reopened",0)
						else: file_put_contents("chars/"+ticket_obj["owner"]+"/ticketinform.usr","Your ticket with "+ticket_obj["id"]+" is reopened")
					g.players[index].prevmenu() # Refresh menu

				elif parsed[1]=="close_ticket":
					# Close ticket logic (copied from original /closeticket)
					if ticket_obj["closed"]: g.n.send_reliable(e.peer_id,"This ticket is already closed!",0); g.players[index].prevmenu(); return
					ticket_obj["closed"]=True
					ticket_obj["messages"]+="\nThis ticket was closed by "+g.players[index].name+" in "+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
					ticket_obj["lastupdate"]=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
					adminsend(g.players[index].name+" closed the "+ticket_obj["title"]+" ticket.")
					notify_admins("zero hour assault, "+g.players[index].name+" closed the "+ticket_obj["title"]+" ticket.")
					g.n.send_reliable(g.players[index].peer_id,"Done, ticket closed successfully.",0)
					getmail=file_get_contents("chars/"+ticket_obj["owner"]+"/mail.usr")
					if is_enabled_ticket_mail(ticket_obj["owner"]): send_mail(getmail,"your ticket "+ticket_obj["title"]+" has been resolved and closed","Hello "+ticket_obj["owner"]+"<br>your ticket "+ticket_obj["title"]+" has been closed by "+g.players[index].name+"<br>Below is all the ticket messages:<br>"+ticket_obj["messages"].replace("\n","<br>")+"<br>If you have more questions or need help, please create a support ticket again from the game or contact us at contact@nbmstudios.com<br>regards,<br>Nbm studios team")
					file_put_contents(f"chars/{ticket_obj['owner']}/rateneeded.usr","") # Mark as needing rating
					if g.players[index].name!=ticket_obj["owner"]:
						ind=g.get_player_index_from(ticket_obj["owner"])
						if ind>-1: g.n.send_reliable(g.players[ind].peer_id,"Your ticket with id "+ticket_obj["id"]+" is closed",2)
						else: file_put_contents(f"chars/{ticket_obj['owner']}/ticketinform.usr","Your ticket with "+ticket_obj["id"]+" is closed")
					g.players[index].prevmenu() # Refresh menu
				
				elif parsed[1]=="mark_pending":
					# Make ticket pending logic (copied from original /maketicketpending)
					if ticket_obj["pending"]: g.n.send_reliable(e.peer_id,"This ticket is already pending!",0); g.players[index].prevmenu(); return
					ticket_obj["pending"]=True
					ticket_obj["messages"]+="\nThis ticket was marked as pending by "+g.players[index].name+" at "+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
					ticket_obj["lastupdate"]=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
					adminsend(g.players[index].name+" made pending the "+ticket_obj["title"]+" ticket.")
					notify_admins("zero hour assault, "+g.players[index].name+" made pending the "+ticket_obj["title"]+" ticket.")
					g.n.send_reliable(e.peer_id,"Done, ticket made pending successfully.",0)
					if g.players[index].name!=ticket_obj["owner"]:
						ind=g.get_player_index_from(ticket_obj["owner"])
						if ind>-1: g.n.send_reliable(g.players[ind].peer_id,"Your ticket with id "+ticket_obj["id"]+" is marked as pending",0)
						else: file_put_contents(f"chars/{ticket_obj['owner']}/ticketinform.usr","Your ticket with "+ticket_obj["id"]+" is marked as pending")
					g.players[index].prevmenu() # Refresh menu

				elif parsed[1]=="mark_not_pending":
					# Make ticket not pending logic (copied from original /maketicketnotpending)
					if not ticket_obj["pending"]: g.n.send_reliable(e.peer_id,"This ticket is not pending!",0); g.players[index].prevmenu(); return
					ticket_obj["pending"]=False
					ticket_obj["messages"]+="\nThis ticket was marked as not pending by "+g.players[index].name+" at "+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
					ticket_obj["lastupdate"]=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
					ticket_obj["closetimer"].restart()
					ticket_obj["closetimer"].pause() # Ensure it doesn't auto-close immediately after becoming not pending
					adminsend(g.players[index].name+" made not pending the "+ticket_obj["title"]+" ticket.")
					notify_admins("zero hour assault, "+g.players[index].name+" made not pending the "+ticket_obj["title"]+" ticket.")
					g.n.send_reliable(e.peer_id,"Done, ticket made not pending successfully.",0)
					getmail=file_get_contents("chars/"+ticket_obj["owner"]+"/mail.usr")
					if is_enabled_ticket_mail(ticket_obj["owner"]): send_mail(getmail,"your ticket "+ticket_obj["title"]+" has been marked as not pending","Hello "+ticket_obj["owner"]+"<br>your ticket "+ticket_obj["title"]+" has been marked as not pending by "+g.players[index].name+"<br>We will answer you as soon as possible. We will resolve your issue soon.<br>regards,<br>Nbm studios team")
					if g.players[index].name!=ticket_obj["owner"]:
						ind=g.get_player_index_from(ticket_obj["owner"])
						if ind>-1: g.n.send_reliable(g.players[ind].peer_id,"Your ticket with id "+ticket_obj["id"]+" is marked as not pending",0)
						else: file_put_contents(f"chars/{ticket_obj['owner']}/ticketinform.usr","Your ticket with "+ticket_obj["id"]+" is marked as not pending")
					g.players[index].prevmenu() # Refresh menu
		elif parsed[0]=="ticketview_select_action":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				if parsed[1]=="back": g.players[index].prevmenu(); return
				g.players[index].ticket_selected_id = parsed[1] # Store selected ticket ID

				ticket_obj = find_ticket_by_id(g.players[index].ticket_selected_id)
				if ticket_obj is None: g.n.send_reliable(e.peer_id,"Error, ticket not found!",0); g.players[index].prevmenu(); return

				m = server_menu()
				m.intro = f"Ticket: {ticket_obj['title']}"
				m.initial_packet = "ticket_action_chosen"

				m.add("View Messages", "view_messages")
				if not ticket_obj["closed"] and not ticket_obj["pending"]: # Can only add message to open, not pending tickets
					m.add("Add Message", "add_message")
				
				if ticket_obj["closed"] and file_exists(f"chars/{g.players[index].name}/rateneeded.usr"): # Only rate if closed and rating needed
					m.add("Rate this Ticket", "rate_ticket")

				m.send(e.peer_id)

		elif parsed[0]=="ticket_action_chosen":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				if parsed[1]=="back": g.players[index].prevmenu(); return
				
				ticket_obj = find_ticket_by_id(g.players[index].ticket_selected_id)
				if ticket_obj is None: g.n.send_reliable(e.peer_id,"Error, ticket not found!",0); g.players[index].prevmenu(); return

				if parsed[1]=="view_messages":
					m = server_menu()
					m.intro = f"Messages for '{ticket_obj['title']}'"
					m.initial_packet = "dummy_ticket_messages" # Dummy for display
					message_lines = ticket_obj["messages"].split("\n")
					for line in message_lines:
						m.add(line, line, False) # Act is False as these are just for viewing
					m.send(e.peer_id)

				elif parsed[1]=="add_message":
					if ticket_obj["closed"] or ticket_obj["pending"]: 
						g.n.send_reliable(e.peer_id,"This ticket is closed or pending, you cannot add messages.",0); g.players[index].prevmenu(); return
					send_serverbox(g.players[index].peer_id, 0, 1000, 0, -1, "ticket_add_message_submit", "Enter your message:")

				elif parsed[1]=="rate_ticket":
					if not ticket_obj["closed"] or not file_exists(f"chars/{g.players[index].name}/rateneeded.usr"):
						g.n.send_reliable(e.peer_id,"You can only rate closed tickets that require rating.",0); g.players[index].prevmenu(); return
					m = server_menu()
					m.intro = "Rate the ticket from 0 to 10:"
					m.initial_packet = "ticket_rate_submit"
					for i in range(11): # 0 to 10
						m.add(str(i), str(i))
					m.send(e.peer_id)

		elif parsed[0]=="ticket_add_message_submit":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				if parsed[1]=="[cncel]": g.players[index].prevmenu(); return
				message_text = e.message.replace("ticket_add_message_submit ", "")
				ticket_obj = find_ticket_by_id(g.players[index].ticket_selected_id)
				if ticket_obj and not ticket_obj["closed"] and not ticket_obj["pending"]:
					prank = "" # Determine player rank for message, similar to original /answerticket
					if g.players[index].dev: prank = "Support Team"
					elif g.players[index].is_admin(): prank = "Support Team"
					elif g.players[index].moderator==True: prank = "Support Team"
					elif g.players[index].builder: prank = "Support Team"

					ticket_obj["messages"] += f"\n{g.players[index].name}, {prank}, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{message_text}"
					ticket_obj["lastupdate"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
					g.n.send_reliable(e.peer_id,"Message added successfully.",0)
					adminsend(f"{g.players[index].name} added a message to ticket {ticket_obj['title']}: {message_text}")
					notify_admins(f"zero hour assault, {g.players[index].name} added a message to ticket {ticket_obj['title']}: {message_text}")
					# Refresh menu to show new message count if applicable or just go back
					g.players[index].prevmenu() 
				else:
					g.n.send_reliable(e.peer_id, "Error: Ticket not found, closed, or pending.", 0)
				
		elif parsed[0]=="ticket_rate_submit":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				if parsed[1]=="back": g.players[index].prevmenu(); return
				try:
					rating = int(parsed[1])
					if not (0 <= rating <= 10): raise ValueError
				except ValueError:
					g.n.send_reliable(e.peer_id,"Invalid rating. Please choose a number from 0 to 10.",0); g.players[index].prevmenu(); return

				ticket_obj = find_ticket_by_id(g.players[index].ticket_selected_id)
				if ticket_obj and ticket_obj["closed"] and file_exists(f"chars/{g.players[index].name}/rateneeded.usr"):
					file_delete(f"chars/{g.players[index].name}/rateneeded.usr") # Mark as needing rating
					ticket_obj["messages"] += f"\n{g.players[index].name} rated this ticket {rating} points at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
					ticket_obj["lastupdate"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
					g.n.send_reliable(e.peer_id,"Ticket rated successfully. Thank you for your feedback!",0)
					adminsend(f"{g.players[index].name} rated ticket {ticket_obj['title']} with {rating} points.")
					notify_admins(f"zero hour assault, {g.players[index].name} rated ticket {ticket_obj['title']} with {rating} points.")
					g.players[index].prevmenu() # Return to previous menu
				else:
					g.n.send_reliable(e.peer_id,"Error: Cannot rate ticket. It might not be closed or already rated.",0)


		elif parsed[0]=="ticket_create_title": # Title entered, ask for message (NEW FLOW)
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				if parsed[1]=="[cncel]": g.players[index].prevmenu(); return
				g.players[index].ticket_selected_id = " ".join(parsed[1:])
				send_serverbox(g.players[index].peer_id, 0, 1000, 0, -1, "ticket_create_message", "Enter Ticket Message:")

		elif parsed[0]=="ticket_create_message": # Message entered, ask for department (NEW FLOW)
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				if parsed[1]=="[cncel]": g.players[index].prevmenu(); return
				g.players[index].ticket_selected_department = " ".join(parsed[1:])
				m=server_menu()
				m.intro="Select a department for your ticket:"
				m.initial_packet="ticket_create_department"
				m.add("Support", "support")
				m.add("Report a Bug", "report_a_bug")
				m.add("Report a Player", "report_a_player")
				m.add("Game Suggestion", "game_suggestion")
				m.add("Other", "other")
				m.send(e.peer_id)
		

	return True
