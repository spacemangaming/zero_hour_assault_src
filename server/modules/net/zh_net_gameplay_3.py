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

def handle_gameplay_3(e, parsed, index):
	global languages
	cmds = {"langcontribadd", "langline", "store4", "watchadmin_select", "event_store3", "beacontoggle", "store3", "differentgroupplayers", "matchmenu", "enablenear", "voicechatgroup", "event_store2", "matchteamselect", "mitems", "matchwatch", "scoreboard", "kickmatch", "matchpassword2", "matchoption", "admchat", "sound", "disablelisten", "enablelisten", "store2", "enablescope", "matchmodepublic", "sameteambots", "differentteamplayers", "matchv", "mpacket", "langcreate", "matchwatchstop", "unbanmatch", "move_map", "voicechatwho", "langswitchoption", "langswitchoptionunofficial", "voicechatteam", "exithouse", "disablescope", "invitematch", "joinmatch", "matchpublic", "charvoice", "event_store4", "enablekill", "matchteaminfo", "banmatch", "langcontribremove", "teammessage", "disablekill", "langmanageoption", "matchpassword", "sameteamplayers", "voicechatfriend", "voicechatmap", "langupdate", "langowneradd", "matchteamselect2", "differentteambots", "matchprivate", "disablenear", "samegroupplayers", "langmanageoption2"}
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

	if parsed[0]=="move_map":
		index=get_player_index(e.peer_id)
		if index>-1:
			if parsed[1]=="": return
			if parsed[1]=="back": g.n.send_reliable(g.players[index].peer_id,"canceled",2); return
			if string_contains(parsed[1],"base",1)>-1: g.n.send_reliable(g.players[index].peer_id,"you are unable to move yourself in a base",2); return

			notify_admins("zero hour assault, "+g.players[index].name+" changed their map to "+parsed[1]+" map")
			adminsend(""+g.players[index].name+" changed their map to "+parsed[1]+" map")
			g.n.send_reliable(g.players[index].peer_id,"your map changed to "+parsed[1]+"",0)
			if parsed[1].endswith(".map"):
				parsed[1]=parsed[1][:-4]
				move_player(index, 0, 0, 0, parsed[1], False)

	elif parsed[0]=="beacontoggle":
		index=get_player_index(e.peer_id)
		if index>-1:
			if g.players[index].beacon==1:
				g.players[index].beacon=0
				g.n.send_reliable(e.peer_id,"Beacons disabled.",0)
			elif g.players[index].beacon==0:
				g.players[index].beacon=1
				g.n.send_reliable(e.peer_id,"Beacons enabled.",0)
	elif parsed[0]=="admchat":
		index=get_player_index(e.peer_id)
		if index>-1:
			admchat=string_replace(e.message,"admchat ","",False)
			for pl in g.players:
				if pl.builder or pl.moderator==True or pl.is_admin() or pl.dev:
					g.n.send_reliable(pl.peer_id,"play_s chat_message.ogg",0)
					g.n.send_reliable(pl.peer_id,"adminmessage "+g.players[index].name+" says: "+admchat,0)
	elif parsed[0] == "scoreboard":
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
									m.add(f"{char}, {pos}, score point {score}, score rank {rank}, character {character}", char)
								else: m.add(f"{pos}. {char}, score point {score}, character {character}", char)
								pos += 1
		if len(m.menuids)==0: m.add("no scores available","noscore")
		m.send(e.peer_id)

	elif parsed[0]=="teammessage" and len(parsed)>0:
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if not g.players[index].disable_all_chat_check(): return
			if not g.players[index].disable_team_chat_check(): return
			if g.players[index].teammessage==0: g.n.send_reliable(e.peer_id,"Error, you can't send team messages because you turned off receiving team messages.",0); return
			if g.players[index].matchteam=="":
				g.n.send_reliable(g.players[index].peer_id,"You are not member of any team.",0)
				return
			mess=string_replace(e.message,parsed[0]+" ","",False)
			for i in g.players:
				if i.joinedmatch==g.players[index].joinedmatch and i.matchteam==g.players[index].matchteam and i.teammessage==1 and i.map==g.players[index].map:
					if g.players[index].paid: g.n.send_reliable(i.peer_id,"teammessage * "+g.players[index].name+" says to the team: "+mess,0)
					if not g.players[index].paid: g.n.send_reliable(i.peer_id,"teammessage "+g.players[index].name+" says to the team: "+mess,0)
					g.n.send_reliable(i.peer_id,"play_s teammessage.ogg",0)
					if mess.startswith("come"):
						parts=mess.split(" ")
						if len(parts)>1:
							for n in g.npcs:
								if n.faint or n.fainted: continue
								if (n.name==parts[1] or parts[1]=="all") and n.matchteam!="" and g.players[index].matchteam==n.matchteam:
									n.looting=True; n.comename=g.players[index].name; n.randomwalking=False
					if mess.startswith("go"):
						parts=mess.split(" ")
						if len(parts)>1:
							for n in g.npcs:
								if n.faint or n.fainted: continue
								if (n.name==parts[1] or parts[1]=="all") and n.matchteam!="" and g.players[index].matchteam==n.matchteam:
									n.looting=False; n.comename=""; n.randomwalking=False
	elif parsed[0]=="sameteambots":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].sameteambots=int(parsed[1])
	elif parsed[0]=="sound":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].sound=int(parsed[1])
	elif parsed[0]=="charvoice":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].charvoice=int(parsed[1])


	elif parsed[0]=="sameteamplayers":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].sameteamplayers=int(parsed[1])

	elif parsed[0]=="differentteamplayers":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].differentteamplayers=int(parsed[1])

	elif parsed[0]=="differentteambots":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].differentteambots=int(parsed[1])

	elif parsed[0]=="samegroupplayers":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].samegroupplayers=int(parsed[1])

	elif parsed[0]=="differentgroupplayers":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].differentgroupplayers=int(parsed[1])


	elif parsed[0]=="voicechatfriend":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].voicechatfriend=int(parsed[1])
	elif parsed[0]=="voicechatmap":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].voicechatmap=int(parsed[1])
	elif parsed[0]=="voicechatgroup":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].voicechatgroup=int(parsed[1])


	elif parsed[0]=="voicechatteam":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].voicechatteam=int(parsed[1])


	elif(parsed[0]=="disablekill"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].killn=0
	elif(parsed[0]=="enablekill"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].killn=1

	elif(parsed[0]=="voicechatwho"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1): g.players[index].voicechatwho=parsed[1]

	elif(parsed[0]=="disablenear"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].nearn=0
	elif(parsed[0]=="disablelisten"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].listen=0

	elif(parsed[0]=="disablescope"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].scope=0
	elif(parsed[0]=="enablenear"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].nearn=1
	elif(parsed[0]=="enablelisten"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].listen=1

	elif(parsed[0]=="enablescope"):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].scope=1


	elif parsed[0]=="exithouse":
		index=g.get_player_index(e.peer_id)
		if(index>-1): g.players[index].exithouse=True
	elif parsed[0]=="matchwatch":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].watchingfreedom=True
			g.n.send_reliable(e.peer_id,e.message,e.channel)
			g.n.send_reliable(e.peer_id,"stopmoving",0)
			for m in g.matches:
				if m.owner==g.players[index].specmatch:
					if g.players[index].name not in m.spectators:
						#m.send(g.players[index].name+" joined this match as spectator!",2)
						m.spectators.append(g.players[index].name)
						g.players[index].watchingfreedom=False
			p=g.getpc(parsed[1])
			if p is not None:
				g.n.send_reliable(e.peer_id,"mapdata "+file_get_contents("maps/"+p.map+".map"),0)
				g.players[index].specplayer=parsed[1]
				return

	elif parsed[0]=="matchwatchstop":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			move_player(index,5,0,0,"lobby")
			g.n.send_reliable(e.peer_id,"parachute_stop",0)
			g.players[index].specplayer=""
			g.players[index].specmap=""

			g.players[index].watchingfreedom=False
			g.n.send_reliable(e.peer_id,"startmoving",0)
			g.n.send_reliable(e.peer_id,"matchwatchstopnoserver",0)
			for m in g.matches:
				if m.owner==g.players[index].specmatch:
					#m.send(g.players[index].name+" stopped spectating this match!",2)
					if g.players[index].name in m.spectators: m.spectators.remove(g.players[index].name)
			g.players[index].specmatch=""
	elif parsed[0]=="matchteaminfo":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if "basement" in g.players[index].map or g.players[index].map=="massacre_in_the_city" or g.players[index].specmap=="massacre_in_the_city":
				fplayers=[]
				famount=0
				for p in g.players:
					if p.hidden: continue
					if p.map=="massacre_in_the_city": famount+=1; fplayers.append(p.name)
				s="There are "+str(famount)+" players in the freedom fight map: "
				for item in fplayers: s+=item+", "
				g.n.send_reliable(e.peer_id,s,0); return
			for m in g.matches:
				if (m.owner==g.players[index].joinedmatch or m.owner==g.players[index].specmatch) and m.mode=="teamc":
					rlen=0
					blen=0
					blist=[]
					rlist=[]
					for p in m.players:
						if getpc(p) is None: continue
						if getpc(p).matchteam=="red": rlen+=1; rlist.append(p)
						if getpc(p).matchteam=="blue": blen+=1; blist.append(p)
					g.n.send_reliable(e.peer_id,"You are in the "+g.players[index].matchteam+" team, red team has "+str(rlen)+" players and "+str(m.blueflagpoint)+" flags, players on red team are "+", ".join(rlist)+"), and blue team has "+str(blen)+" players and "+str(m.redflagpoint)+" flags, players on blue team are "+", ".join(blist)+".",0); return

				if (m.owner==g.players[index].joinedmatch or m.owner==g.players[index].specmatch) and m.mode=="teaml":
					vp=[n for n in m.players if not (g.getpc(n) is not None and g.getpc(n).hidden)]; liste=vp[0] if len(vp)==1 else ", ".join(vp)
					g.n.send_reliable(e.peer_id,str(len(vp))+" players in the match: "+liste,0); return
				if (m.owner==g.players[index].joinedmatch or m.owner==g.players[index].specmatch) and m.mode=="teamk2":
					vp=[n for n in m.players if not (g.getpc(n) is not None and g.getpc(n).hidden)]; liste=vp[0] if len(vp)==1 else ", ".join(vp)
					g.n.send_reliable(e.peer_id,str(len(vp))+" players in the match: "+liste,0); return
				if (m.owner==g.players[index].joinedmatch or m.owner==g.players[index].specmatch) and m.mode=="teamf2":
					vp=[n for n in m.players if not (g.getpc(n) is not None and g.getpc(n).hidden)]; liste=vp[0] if len(vp)==1 else ", ".join(vp)
					g.n.send_reliable(e.peer_id,str(len(vp))+" players in the match: "+liste,0); return

				if (m.owner==g.players[index].joinedmatch or m.owner==g.players[index].specmatch) and m.mode=="snow":
					vp=[n for n in m.players if not (g.getpc(n) is not None and g.getpc(n).hidden)]; liste=vp[0] if len(vp)==1 else ", ".join(vp)
					g.n.send_reliable(e.peer_id,str(len(vp))+" players in the match: "+liste,0); return

				if (m.owner==g.players[index].joinedmatch or m.owner==g.players[index].specmatch) and m.mode=="sniper":
					vp=[n for n in m.players if not (g.getpc(n) is not None and g.getpc(n).hidden)]; liste=vp[0] if len(vp)==1 else ", ".join(vp)
					g.n.send_reliable(e.peer_id,str(len(vp))+" players in the match: "+liste,0); return


				if (m.owner==g.players[index].joinedmatch or m.owner==g.players[index].specmatch) and m.mode=="g":
					vp=[n for n in m.players if not (g.getpc(n) is not None and g.getpc(n).hidden)]; liste=vp[0] if len(vp)==1 else ", ".join(vp)
					g.n.send_reliable(e.peer_id,str(len(vp))+" players in the match: "+liste,0); return
				if (m.owner==g.players[index].joinedmatch or m.owner==g.players[index].specmatch) and m.mode=="g2":
					vp=[n for n in m.players if not (g.getpc(n) is not None and g.getpc(n).hidden)]; liste=vp[0] if len(vp)==1 else ", ".join(vp)
					g.n.send_reliable(e.peer_id,str(len(vp))+" players in the match: "+liste,0); return


				if (m.owner==g.players[index].joinedmatch or m.owner==g.players[index].specmatch) and m.mode=="minecraft":
					vp=[n for n in m.players if not (g.getpc(n) is not None and g.getpc(n).hidden)]; liste=vp[0] if len(vp)==1 else ", ".join(vp)
					g.n.send_reliable(e.peer_id,str(len(vp))+" players in the match: "+liste,0); return
				if (m.owner==g.players[index].joinedmatch or m.owner==g.players[index].specmatch) and m.mode=="sword":
					vp=[n for n in m.players if not (g.getpc(n) is not None and g.getpc(n).hidden)]; liste=vp[0] if len(vp)==1 else ", ".join(vp)
					g.n.send_reliable(e.peer_id,str(len(vp))+" players in the match: "+liste,0); return

				if (m.owner==g.players[index].joinedmatch or m.owner==g.players[index].specmatch) and m.mode=="collect":
					s=""
					for p in m.players:
						pl=g.getpc(p)
						if pl is not None:
							if pl.hidden: continue
							s+=p+", collected "+str(pl.items_got)+" golds. "
					s+=" Match will end after "+ms_to_readable_time(600000-m.endtimer.elapsed)+"."
					g.n.send_reliable(e.peer_id,s,2); return



				if (m.owner==g.players[index].joinedmatch or m.owner==g.players[index].specmatch) and m.mode=="teamz":
					g.players[index].send_teaminfo_menu(); return
				if (m.owner==g.players[index].joinedmatch or m.owner==g.players[index].specmatch) and m.mode=="teamminecraft":
					g.players[index].send_teaminfo_menu(); return
				if (m.owner==g.players[index].joinedmatch or m.owner==g.players[index].specmatch) and m.mode=="teamsword":
					g.players[index].send_teaminfo_menu(); return
				if (m.owner==g.players[index].joinedmatch or m.owner==g.players[index].specmatch) and m.mode=="teamcollect":
					ma=m
					m=server_menu()
					m.intro="match info"
					m.initial_packet="dummy"
					m.add("you are in the "+g.players[index].matchteam+" team","team",False)
					m.add("match will end after "+ms_to_readable_time(600000-ma.endtimer.elapsed)+".","end",False)
					m.add("red team has "+str(ma.redgot)+" gold","red",False)
					m.add("blue team has "+str(ma.bluegot)+" gold","blue",False)
					m.send(e.peer_id); return

				if (m.owner==g.players[index].joinedmatch or m.owner==g.players[index].specmatch) and m.mode=="teamz2":
					g.players[index].send_teaminfo_menu(); return
				if (m.owner==g.players[index].joinedmatch or m.owner==g.players[index].specmatch) and m.mode=="teamd":
					g.players[index].send_teaminfo_menu(); return
				if (m.owner==g.players[index].joinedmatch or m.owner==g.players[index].specmatch) and m.mode=="teamg":
					g.players[index].send_teaminfo_menu(); return
				if (m.owner==g.players[index].joinedmatch or m.owner==g.players[index].specmatch) and m.mode=="teamg2":
					g.players[index].send_teaminfo_menu(); return

				if (m.owner==g.players[index].joinedmatch or m.owner==g.players[index].specmatch) and m.mode=="teamk":
					g.players[index].send_teaminfo_menu(); return
				if (m.owner==g.players[index].joinedmatch or m.owner==g.players[index].specmatch) and m.mode=="teamf":
					g.players[index].send_teaminfo_menu(); return

				if (m.owner==g.players[index].joinedmatch or m.owner==g.players[index].specmatch) and m.mode=="teamsnow":
					g.players[index].send_teaminfo_menu(); return
				if (m.owner==g.players[index].joinedmatch or m.owner==g.players[index].specmatch) and m.mode=="teamsniper":
					g.players[index].send_teaminfo_menu(); return

			g.n.send_reliable(e.peer_id,"You are not on any match.",0)
	elif(parsed[0]=="matchoption" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			if parsed[1]=="cancel":
				for m in g.matches:
					if m.owner==g.players[index].name:
						m.cancel()
			if parsed[1]=="leave":
				for m in g.matches:
					if m.owner==g.players[index].joinedmatch:
						if not m.inprogress and not m.started: m.leave(g.players[index])
						else: g.n.send_reliable(e.peer_id,"You cannot leave the match because it is started",0); return

			if parsed[1]=="start":
				for m in g.matches:
					if m.owner==g.players[index].name:
						if m.botcount!=-1 and len(m.players)<(m.playersinoneteam*2 if m.mode!="teaml" and m.mode!="snow" and m.mode!="sniper" and m.mode!="teamf2" and m.mode!="g2" and m.mode!="teamk2" and m.mode!="sword" and m.mode!="collect" and m.mode!="g" and m.mode!="minecraft" else m.playersinoneteam): g.n.send_reliable(e.peer_id,"not enough players",0); g.players[index].prevmenu()
						else:
							m.starting=True
							m.starttimer.elapsed=10000
							m.send("play_s countdown.ogg",0)
			if parsed[1]=="kick":
				for m in g.matches:
					if m.owner==g.players[index].name:
						m2=server_menu()
						m2.intro="select player to kick"
						m2.initial_packet="kickmatch"
						for p in m.players: m2.add(p,p)
						m2.send(e.peer_id)
			if parsed[1]=="invite":
				for m in g.matches:
					if m.owner==g.players[index].name:
						m2=server_menu()
						m2.intro="select player to invite"
						m2.initial_packet="invitematch"
						for p in g.players:
							if p.hidden or p.map!="lobby" or p.name==g.players[index].name: continue
							m2.add(p.name,p.name)
						m2.send(e.peer_id)

			if parsed[1]=="ban":
				for m in g.matches:
					if m.owner==g.players[index].name:
						m2=server_menu()
						m2.intro="select player to ban"
						m2.initial_packet="banmatch"
						for p in m.players: m2.add(p,p)
						m2.send(e.peer_id)
			if parsed[1]=="unban":
				for m in g.matches:
					if m.owner==g.players[index].name:
						m2=server_menu()
						m2.intro="select player to unban"
						m2.initial_packet="unbanmatch"
						for p in g.players[index].matchbanned:
							m2.add(p,p)
						if len(m2.menuids)==0:
							g.n.send_reliable(g.players[index].peer_id,"No banned player found",0)
							g.players[index].prevmenu()
						m2.send(e.peer_id)


	elif(parsed[0]=="kickmatch" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]==g.players[index].name: return
			if parsed[1]=="back": return
			for m in g.matches:
				if m.owner==g.players[index].joinedmatch:
					i=get_player_index_from(parsed[1])
					g.n.send_reliable(g.players[i].peer_id,g.players[index].name+" has kicked you from the match!",0)
					g.n.send_reliable(g.players[i].peer_id,"startmoving",0)
					move_player(i,5,0,0,"lobby")
					m.send(g.players[index].name+" kicked "+g.players[i].name+" from the match!",2)
					try: m.players.remove(g.players[i].name)
					except: pass
					g.players[i].joinedmatch=""
					g.players[i].matchteam=""
	elif(parsed[0]=="invitematch" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]==g.players[index].name: g.players[index].prevmenu(); return
			if parsed[1]=="back": return
			for m in g.matches:
				if m.owner==g.players[index].joinedmatch:
					i=get_player_index_from(parsed[1])
					if g.players[i].matchinvite==0: g.n.send_reliable(e.peer_id,"this player disabled receiving match invitations",0); g.players[index].prevmenu(); return
					if g.players[index].matchinvitetimer.elapsed<60000: g.n.send_reliable(e.peer_id,"you can only invite players to matches every 1 minute",0); g.players[index].prevmenu(); return
					g.players[index].matchinvitetimer.restart()
					g.n.send_reliable(g.players[i].peer_id,g.players[index].name+" is inviting you to the match! match mode is "+m.get_mode(),2)
					g.n.send_reliable(g.players[i].peer_id,"play_s alert4.ogg",0)
					g.players[i].invites.append(m.owner)
					g.n.send_reliable(e.peer_id,"done",0); g.players[index].prevmenu()

	elif(parsed[0]=="banmatch" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			for m in g.matches:
				if m.owner==g.players[index].joinedmatch:
					if parsed[1]==m.owner: return
					i=get_player_index_from(parsed[1])

					g.n.send_reliable(g.players[i].peer_id,g.players[index].name+" has banned you from the match!",0)
					g.n.send_reliable(g.players[i].peer_id,"startmoving",0)
					move_player(i,5,0,0,"lobby")
					m.send(g.players[index].name+" banned "+g.players[i].name+" from the match!",2)
					try: m.players.remove(g.players[i].name)
					except: pass
					g.players[index].matchbanned.append(g.players[i].name)
					g.players[i].joinedmatch=""
					g.players[i].matchteam=""

	elif(parsed[0]=="unbanmatch" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			for m in g.matches:
				if m.owner==g.players[index].joinedmatch:
					i=get_player_index_from(parsed[1])
					if i>-1: g.n.send_reliable(g.players[i].peer_id,g.players[index].name+" has unbanned you from the match!",0)
					m.send(g.players[index].name+" unbanned "+parsed[1]+" from the match!",2)
					try: g.players[index].matchbanned.remove(parsed[1])
					except: pass
	elif parsed[0]=="mitems": 
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			menuitems=e.message.replace("mitems ","")
			items=string_split(menuitems, "\t", False)
			if len(menuitems)<=1:
				return
			g.players[index].menuitems.clear()
			g.players[index].menuids.clear()
			g.players[index].menuacts.clear()
			for i in items:
				if i == "":
					continue
				parsed=string_split(i, "<", False)
				if len(parsed)>2:
					if 1 == 1:
						g.players[index].menuitems.append(parsed[0])
						g.players[index].menuids.append(parsed[1])
						g.players[index].menuacts.append(strtobool(parsed[2]))
	elif parsed[0]=="mpacket": 
		index=g.get_player_index(e.peer_id)
		if(index>-1): g.players[index].initial_packet=e.message.replace("mpacket ","")

	elif(parsed[0]=="langcontribadd" and len(parsed)>1):
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			pl=parsed[1]
			pi=get_player_index_from(pl)
			if pi>-1:
				g.n.send_reliable(e.peer_id,"done",0)
				g.n.send_reliable(g.players[pi].peer_id,"You are now a contributor of the language "+g.players[index].lngmanage+"!",2)
				g.players[index].prevmenu()
				languages[g.players[index].lngmanage]["contributors"].append(pl)
	elif(parsed[0]=="langowneradd" and len(parsed)>1):
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			pl=parsed[1]
			pi=get_player_index_from(pl)
			if pi>-1:
				g.n.send_reliable(e.peer_id,"done",0)
				g.players[index].prevmenu()
				g.n.send_reliable(g.players[pi].peer_id,"You are now the owner of the language "+g.players[index].lngmanage+"!",2)
				languages[g.players[index].lngmanage]["owner"]=pl

	elif(parsed[0]=="langcontribremove" and len(parsed)>1):
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			pl=parsed[1]
			if pl=="back": return
			pi=get_player_index_from(pl)
			if pi>-1:
				g.n.send_reliable(g.players[pi].peer_id,"You are no longer a contributor of the language "+g.players[index].lngmanage+"!",2)
			try:
				if pl in languages[g.players[index].lngmanage]["contributors"]: languages[g.players[index].lngmanage]["contributors"].remove(pl)
			except: pass
			g.n.send_reliable(e.peer_id,"done",0)
			g.players[index].prevmenu()
	elif(parsed[0]=="langmanageoption2" and len(parsed)>1):
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="copy":
				g.n.send_reliable(e.peer_id,"copyed",0)
				g.n.send_reliable(e.peer_id,"clip "+file_get_contents("lang/"+g.players[index].lngmanage+".lng"),0)
				g.players[index].prevmenu()
			if parsed[1]=="switch":
				g.n.send_reliable(e.peer_id,"switchlang "+g.players[index].lngmanage+" "+file_get_contents("lang/"+g.players[index].lngmanage+".lng"),0)
				g.n.send_reliable(e.peer_id,"Done",0)
				g.players[index].lang=g.players[index].lngmanage
				g.players[index].prevmenu()
			if parsed[1]=="release":
				languages[g.players[index].lngmanage]["released"]=True
				g.n.send_reliable(e.peer_id,"Language released",0)
				g.players[index].prevmenu()
			if parsed[1]=="official":
				languages[g.players[index].lngmanage]["official"]=True
				g.n.send_reliable(e.peer_id,"Language now official",0)
				g.players[index].prevmenu()
			if parsed[1]=="unofficial":
				languages[g.players[index].lngmanage]["official"]=False
				g.n.send_reliable(e.peer_id,"Language now unofficial",0)
				g.players[index].prevmenu()

			name=g.players[index].name
			if parsed[1]=="del" and send_yesno_question(g.players[index].peer_id,"Are you sure you want to delete this language?")=="yes":
				index=get_player_index_from(name)
				try: del languages[g.players[index].lngmanage]
				except: pass
				file_delete("lang/"+g.players[index].lngmanage+".lng")
				for p in g.players:
					if p.lang==g.players[index].lngmanage:
						p.lang="en"
						g.n.send_reliable(p.peer_id,"switchlang en english",0)
						file_put_contents("lang/en.lng","english")
				g.n.send_reliable(e.peer_id,"Language deleted",0)
			if parsed[1]=="update":
				send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "langupdate", "Please paste language data")
			if parsed[1]=="line":
				send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "langline", "Please input new line")

			if parsed[1]=="contrib":
				m=server_menu()
				m.intro="Select player to add as contributor"
				m.initial_packet="langcontribadd"
				for p in g.players:
					if not p.hidden and g.players[get_player_index_from(p.name)].name not in languages[g.players[index].lngmanage]["contributors"]: m.add(p.name,p.name)
				m.send(e.peer_id)
			if parsed[1]=="owner":
				m=server_menu()
				m.intro="Select player to make owner"
				m.initial_packet="langowneradd"
				for p in g.players:
					if not p.hidden: m.add(p.name,p.name)
				m.send(e.peer_id)

			if parsed[1]=="contrib2":
				m=server_menu()
				m.intro="Select player to remove from contributor list"
				m.initial_packet="langcontribremove"
				for p in languages[g.players[index].lngmanage]["contributors"]:
					m.add(p,p)
				m.send(e.peer_id)
			if parsed[1]=="contrib3":
				contriblist=[]
				for i in languages[g.players[index].lngmanage]["contributors"]:
					contriblist.append(i)
				if len(contriblist)==0: g.n.send_reliable(e.peer_id,"No contributors",0); g.players[index].prevmenu(); return
				else: s="There are "+str(len(contriblist))+" contributors. They are: "+str(contriblist)
				g.n.send_reliable(e.peer_id,s,0)
				g.players[index].prevmenu()
	elif((parsed[0]=="langswitchoption" or parsed[0]=="langswitchoptionunofficial") and len(parsed)>1):
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back":
				return
			if parsed[1]=="unofficial":
				m=server_menu()
				m.intro="Select language to switch"
				m.initial_packet="langswitchoptionunofficial"
				for key in languages.keys():
					if languages[key]["released"]==True:
						if not languages[key]["official"]: m .add(key+", unofficial, created by "+languages[key]["owner"]+", "+get_language_used_count(key)+" players are using it, has "+str(len(languages[key]["contributors"]))+" contributors, "+get_file_size("lang/"+key+".lng"),key)
				m.send(e.peer_id); return


			g.players[index].prevmenu()
			g.n.send_reliable(e.peer_id,"switchlang "+parsed[1]+" "+file_get_contents("lang/"+parsed[1]+".lng"),0)
			g.n.send_reliable(e.peer_id,"done",0)
			g.players[index].lang=parsed[1]
	elif(parsed[0]=="langmanageoption" and len(parsed)>1):
		if parsed[1]=="back": return
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].lngmanage=parsed[1]
			m=server_menu()
			m.intro="Select an option"
			m.initial_packet="langmanageoption2"
			m.add("copy data","copy")
			m.add("View contributors","contrib3")
			m.add("update data","update")
			m.add("add line","line")
			m.add("Switch to this language","switch")
			if parsed[1] not in languages: return
			if not languages[parsed[1]]["released"] and (g.players[index].is_admin() or languages[parsed[1]]["owner"]==g.players[index].name): m.add("release","release")
			if g.players[index].dev or g.players[index].moderator or g.players[index].is_admin():
				if not languages[parsed[1]]["official"]: m.add("set as official language","official")
				if languages[parsed[1]]["official"]: m.add("set as unofficial language","unofficial")
			if g.players[index].is_admin() or languages[parsed[1]]["owner"]==g.players[index].name: m.add("Change owner","owner")
			if g.players[index].is_admin() or languages[parsed[1]]["owner"]==g.players[index].name: m.add("Add contributor","contrib")
			if g.players[index].is_admin() or languages[parsed[1]]["owner"]==g.players[index].name: m.add("Remove contributor","contrib2")

			if g.players[index].is_admin() or languages[parsed[1]]["owner"]==g.players[index].name: m.add("delete language","del")
			m.send(e.peer_id)
	elif(parsed[0]=="langcreate" and len(parsed)>1):
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="[cncel]": return
			if " " in parsed[1] or not parsed[1].isascii(): g.n.send_reliable(e.peer_id,"invalid input",0); return
			if "\\" in parsed[1]: g.n.send_reliable(e.peer_id,"invalid name",0); g.players[index].prevmenu(); return
			if "/" in parsed[1]: g.n.send_reliable(e.peer_id,"invalid name",0); g.players[index].prevmenu(); return
			if any(k.lower() == parsed[1].lower() for k in languages.keys()):
				g.n.send_reliable(g.players[index].peer_id,"This language is exists",0)
				g.players[index].prevmenu()
				return
			languages[parsed[1]]={"owner":g.players[index].name,"official":False,"released":False,"contributors":[]}

			if not directory_exists("lang"): directory_create("lang")
			file_put_contents("lang/"+parsed[1]+".lng","")
			g.n.send_reliable(e.peer_id,"Language was created successfully.",0)
			g.players[index].prevmenu()
	elif(parsed[0]=="langupdate" and len(parsed)>1):
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="[cncel]": return
			if not directory_exists("lang"): directory_create("lang")
			file_put_contents("lang/"+g.players[index].lngmanage+".lng",e.message.replace(parsed[0]+" ",""))
			for p in g.players:
				g.n.send_reliable(p.peer_id,"updatelang "+g.players[index].lngmanage+" "+file_get_contents("lang/"+g.players[index].lngmanage+".lng"),0)
			g.n.send_reliable(e.peer_id,"Language was updated successfully.",0)
			g.players[index].prevmenu()
	elif(parsed[0]=="langline" and len(parsed)>1):
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="[cncel]": return
			if not directory_exists("lang"): directory_create("lang")
			data=e.message.replace(parsed[0]+" ","")
			olddata=file_get_contents("lang/"+g.players[index].lngmanage+".lng")
			newdata=olddata+"\n"+data
			file_put_contents("lang/"+g.players[index].lngmanage+".lng",newdata)
			for p in g.players:
				g.n.send_reliable(p.peer_id,"updatelang "+g.players[index].lngmanage+" "+file_get_contents("lang/"+g.players[index].lngmanage+".lng"),0)
			g.n.send_reliable(e.peer_id,"Language was updated successfully.",0)
			g.players[index].prevmenu()
	elif(parsed[0]=="store4" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			try:
				a=int(parsed[1])
			except: return
			if a==0: return
			if a<=0: g.n.send_reliable(e.peer_id,"You can't buy less than 1",0); g.players[index].prevmenu(); return
			for ind, elem in enumerate(store_data):
				if g.players[index].storeitem==elem["name"]: i=ind
			try:
				tokenreq=int(store_data[i]["price"])*abs(a)
			except:  return
			if a>0 and g.players[index].zhtoken<tokenreq: g.n.send_reliable(e.peer_id,"Not enough zero tokens",0); g.players[index].prevmenu(); return
			if a<0 and g.players[index].get_item_count(g.players[index].storeitem)<(-a): g.n.send_reliable(e.peer_id,"You don't have the amount you are trying to sell",0); g.players[index].prevmenu(); return
			for t in g.timeditems:
				if g.players[index].get_item_count(g.players[index].storeitem)>0 and t.itemname==g.players[index].storeitem and t.owner==g.players[index].name:
					g.n.send_reliable(e.peer_id,"You already got this item, please wait for the item's timer to expire to get another one.",0); g.players[index].prevmenu(); return

			if "backpack" not in g.players[index].storeitem and g.players[index].storeitem!="motor":
				if a>0:
					newamount=g.players[index].get_item_count(g.players[index].storeitem)+int(parsed[1])
					if g.players[index].storeitem in g.invlimits and newamount>g.players[index].get_backpack_level_amount(g.invlimits[g.players[index].storeitem]): g.n.send_reliable(e.peer_id,"Your inventory can hold up to "+str(g.players[index].get_backpack_level_amount(g.invlimits[g.players[index].storeitem]))+" of this item, but if you buy this amount, you'd have "+str(newamount)+" of this item, so purchase canceled.",0); g.players[index].prevmenu(); return
				g.players[index].give(g.players[index].storeitem,int(parsed[1]))
			else:
				if g.players[index].storeitem=="backpacks_level1":
					if g.players[index].paid: g.n.send_reliable(e.peer_id,"paid players cannot buy this, they already have unlimited item storage ability",0); g.players[index].prevmenu(); return
					g.players[index].backpacks_level=1; g.players[index].backpacktimer.restart()
				elif g.players[index].storeitem=="backpacks_level2":
					if g.players[index].paid: g.n.send_reliable(e.peer_id,"paid players cannot buy this, they already have unlimited item storage ability",0); g.players[index].prevmenu(); return
					g.players[index].backpacks_level=2; g.players[index].backpacktimer.restart()
				elif g.players[index].storeitem=="backpacks_level3":
					if g.players[index].paid: g.n.send_reliable(e.peer_id,"paid players cannot buy this, they already have unlimited item storage ability",0); g.players[index].prevmenu(); return
					g.players[index].backpacks_level=3; g.players[index].backpacktimer.restart()
				elif g.players[index].storeitem=="motor":
					g.n.send_reliable(g.players[index].peer_id,"motors are disabled at this moment",2); return
					if g.players[index].map=="lobby" or g.players[index].map.startswith("match") or g.players[index].map.startswith("helicopter"): g.n.send_reliable(e.peer_id,"Error, please join a match to be able to buy a motor.",0); g.players[index].prevmenu(); return
					if "minecraft" in g.players[index].map: g.n.send_reliable(e.peer_id,"Error, you can't buy motor in this match mode.",0); return
					gpt=get_tile_at(g.players[index].x,g.players[index].y,g.players[index].z,g.players[index].map)
					if gpt=="" or gpt=="air": g.n.send_reliable(e.peer_id,"Error, you can't buy the motor while in the air.",0); g.players[index].prevmenu(); return
					if "water" in gpt: g.n.send_reliable(e.peer_id,"Error, you can't buy the motor while in the air.",0); g.players[index].prevmenu(); return
					for m in g.motors:
						if round(m.x)==round(g.players[index].x) and round(m.y)==round(g.players[index].y) and round(m.z)==round(g.players[index].z) and m.map==g.players[index].map:
							g.n.send_reliable(e.peer_id,"Error, there's already a motor here.",0); g.players[index].prevmenu(); return
					maxvalues=get_max_values(g.players[index].map)
					if g.players[index].x==maxvalues.x or g.players[index].y==maxvalues.y:
						g.n.send_reliable(e.peer_id,"You cannot buy a motor in the map boundary",0); g.players[index].prevmenu(); return
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
					add_motor(mx, my, g.players[index].z, g.players[index].map, 500, 30, 3, 0, g.players[index].name)
			if a>0: g.players[index].zhtoken-=tokenreq
			if a<0: g.players[index].zhtoken+=tokenreq
			g.players[index].playsound("storepurchase")
			if a>0: g.n.send_reliable(e.peer_id,"Purchase success.",0)
			if a<0: g.n.send_reliable(e.peer_id,"Sell success.",0)
			g.players[index].prevmenu() 
	elif(parsed[0]=="store3" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			if parsed[1]=="storeview":
				if len(g.players[index].storeinv.keys())==0: g.n.send_reliable(e.peer_id,"You have no packs",0); g.players[index].prevmenu(); return
				m=server_menu()
				m.intro="Select an pack to open"
				m.initial_packet="packopen"
				keys=list(g.players[index].storeinv.keys())
				for pack in keys:
					m.add(pack+", "+str(g.players[index].storeinv[pack]),pack)
				m.send(e.peer_id); return
			if parsed[1]=="onlinestore":
				send_reliable(g.players[index].peer_id,"openlink https://nbmstudios.com/zhashop.php",0)
				g.players[index].prevmenu()
				return
			if parsed[1]=="copyonlinestore":
				send_reliable(g.players[index].peer_id,"copied",0)
				send_reliable(g.players[index].peer_id,"clip https://nbmstudios.com/zhashop.php",0)
				g.players[index].prevmenu()
				return


			g.players[index].storeitem=parsed[1]
			if parsed[1] in charlist:
				charname=parsed[1]
				if charname in g.players[index].bought_chars:
					g.n.send_reliable(e.peer_id,"You already bought this character before!",0); g.players[index].prevmenu(); return
				else:
					for ind, elem in enumerate(store_data):
						if g.players[index].storeitem==elem["name"]: i=ind
					tokenreq=int(store_data[i]["price"])
					if g.players[index].zhtoken<tokenreq: g.n.send_reliable(e.peer_id,"Not enough zero tokens",0); g.players[index].prevmenu(); return
					g.players[index].bought_chars.append(charname)
					g.players[index].zhtoken-=tokenreq
					g.players[index].playsound("storepurchase")
					g.n.send_reliable(e.peer_id,"Purchase success.",0); g.players[index].prevmenu(); return

			if "backpack" not in parsed[1] and parsed[1]!="motor": send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "store4", "How many "+parsed[1]+" would you like to buy?")
			else: g.n.send_reliable(e.peer_id,"echo store4 1",0)

	elif(parsed[0]=="store2" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			print(f"[debug_store] store2 packet received! store_data length: {len(store_data)}, list ID: {id(store_data)}, parsed[1]: {repr(parsed[1])}")
			if parsed[1]=="back":
				return
			if parsed[1]=="storeview":
				if len(g.players[index].storeinv.keys())==0: g.n.send_reliable(e.peer_id,"You have no packs",0); g.players[index].prevmenu()
				m=server_menu()
				m.intro="Select an pack to open"
				m.initial_packet="packopen"
				keys=list(g.players[index].storeinv.keys())
				for pack in keys:
					m.add(pack+", "+str(g.players[index].storeinv[pack]),pack)
				m.send(e.peer_id)
			if parsed[1]=="onlinestore":
				send_reliable(g.players[index].peer_id,"openlink https://nbmstudios.com/zhashop.php",0)
				g.players[index].prevmenu()
				return
			if parsed[1]=="copyonlinestore":
				send_reliable(g.players[index].peer_id,"copied",0)
				send_reliable(g.players[index].peer_id,"clip https://nbmstudios.com/zhashop.php",0)
				g.players[index].prevmenu()
				return

			m=server_menu()
			m.intro="Select an item to buy"
			m.initial_packet="store3"
			for item in store_data:
				if item["category"]==parsed[1]: m.add(item["name"]+", requires "+item["price"]+" zero tokens, description: "+item["description"],item["name"])
			m.send(e.peer_id)
	elif(parsed[0]=="event_store4" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			try:
				a=int(parsed[1])
			except: return
			if a<=0: g.n.send_reliable(e.peer_id,"You can't buy less than 1",0); g.players[index].prevmenu(); return
			for ind, elem in enumerate(event_store_data):
				if g.players[index].event_storeitem==elem["name"]: i=ind
			try:
				tokenreq=int(event_store_data[i]["price"])*a
			except:  return
			if g.players[index].eventpoint<tokenreq: g.n.send_reliable(e.peer_id,"Not enough event points",0); g.players[index].prevmenu(); return
			for t in g.timeditems:
				if t.itemname==g.players[index].event_storeitem and t.owner==g.players[index].name:
					g.n.send_reliable(e.peer_id,"You already got this item, please wait for the item's timer to expire to get another one.",0); g.players[index].prevmenu(); return
				if int(parsed[1])<=0:
					g.n.send_reliable(e.peer_id,"incorrect value.",0); g.players[index].prevmenu(); return
			if g.players[index].event_storeitem=="bike":
				if g.players[index].map=="helicopter" or "helicopter" in g.players[index].map or g.players[index].map=="lobby": g.n.send_reliable(e.peer_id,"you cannot buy bike here",0); return
				b=bike(g.players[index].x,g.players[index].y,g.players[index].z,g.players[index].map,g.players[index].name)
				g.bikes.append(b)
				g.players[index].eventpoint-=tokenreq
				g.players[index].playsound("storepurchase")
				g.n.send_reliable(e.peer_id,"Purchase success.",0)
				g.players[index].prevmenu() ; return

			if 1:
				newamount=g.players[index].get_item_count(g.players[index].event_storeitem)+int(parsed[1])
				if g.players[index].event_storeitem in g.invlimits and newamount>g.players[index].get_backpack_level_amount(g.invlimits[g.players[index].event_storeitem]): g.n.send_reliable(e.peer_id,"Your inventory can hold up to "+str(g.players[index].get_backpack_level_amount(g.invlimits[g.players[index].event_storeitem]))+" of this item, but if you buy this amount, you'd have "+str(newamount)+" of this item, so purchase canceled.",0); g.players[index].prevmenu(); return
				g.players[index].give(g.players[index].event_storeitem,int(parsed[1]))
			g.players[index].eventpoint-=tokenreq
			g.players[index].playsound("storepurchase")
			g.n.send_reliable(e.peer_id,"Purchase success.",0)
			g.players[index].prevmenu() 
	elif(parsed[0]=="event_store3" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back": return
			g.players[index].event_storeitem=parsed[1]
			if parsed[1]=="bike": g.n.send_reliable(e.peer_id,"echo event_store4 1",0); return
			send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "event_store4", "How many "+parsed[1]+" would you like to buy?")

	elif parsed[0]=="event_store2":
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].playsound("storeenter")
			m=server_menu()
			m.intro="Select an item to buy"
			m.initial_packet="event_store3"
			for item in event_store_data:
				m.add(item["name"]+", requires "+item["price"]+" event points, description: "+item["description"],item["name"])
			m.send(e.peer_id)

	elif(parsed[0]=="watchadmin_select" and len(parsed)>1):
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if not (g.players[index].is_admin() or g.players[index].moderator==True or g.players[index].dev==True):
				g.n.send_reliable(e.peer_id,"You do not have permission to use this option.",0); return
			if parsed[1]=="back": return
			target=get_player_index_from(parsed[1])
			if target>-1 and not g.players[target].hidden:
				g.n.send_reliable(e.peer_id,"echo matchwatch "+g.players[target].name,0)
			else:
				g.n.send_reliable(e.peer_id,"Player not found or no longer available.",0)

	elif(parsed[0]=="matchmenu" and len(parsed)>1):

		index=g.get_player_index(e.peer_id)
		if(index>-1):
			g.players[index].in_match_menu=False
			name=g.players[index].name
			if parsed[1]=="watch":
				if get_player_count_in_freedom()<=0:
					g.n.send_reliable(e.peer_id,"No one on freedom fight map",0); g.players[index].prevmenu(); return
				if g.players[index].get_friend_count_in_freedom()<=0:
					g.n.send_reliable(e.peer_id,"No friend on freedom fight map",0); g.players[index].prevmenu(); return

				for p in g.players:
					if p.hidden: continue
					if (p.map=="helicopter" or p.map=="massacre_in_the_city") and p.name in g.players[index].friendlist:
						g.n.send_reliable(e.peer_id,"echo matchwatch "+p.name,0)
						return
			if parsed[1]=="watchadmin":
				if not (g.players[index].is_admin() or g.players[index].moderator==True or g.players[index].dev==True):
					g.n.send_reliable(e.peer_id,"You do not have permission to use this option.",0); g.players[index].prevmenu(); return
				freedom_players=[p for p in g.players if (p.map=="helicopter" or p.map=="massacre_in_the_city") and not p.hidden]
				if len(freedom_players)==0:
					g.n.send_reliable(e.peer_id,"No one on freedom fight map",0); g.players[index].prevmenu(); return
				m2=server_menu()
				m2.intro="Select a player to watch in freedom fight map ("+str(len(freedom_players))+" players)"
				m2.initial_packet="watchadmin_select"
				for p in freedom_players:
					m2.add(p.name, p.name)
				m2.send(e.peer_id)
				return
			if parsed[1]=="free" and send_yesno_question(g.players[index].peer_id,"Are you sure you want to go to freedom fight map? You will lose all the items you have.")=="yes":
				index=g.get_player_index_from(name)
				if g.players[index].map=="massacre_in_the_city": return
				g.players[index].matchmode=""
				j=g.players[index]
				item_map={}
				for item in g.dontlose:
					if j is not None and j.get_item_count(item)>0: item_map[item]=j.get_item_count(item)
				try: j.inv=dict()
				except: pass
				for item in item_map.keys():
					if j is not None: j.give(item,item_map[item])

				for i in g.players:
					if i.map=="massacre_in_the_city":
						i.matchmode=""
#					g.players[index].give("mkek_yavuz16",1)
#					g.players[index].give("9mm",30)
				g.players[index].randomweapongive()
				g.players[index].give("vitality_potion",1)
				g.players[index].give("revival_nectar",1)
				g.players[index].give("parachute",1)
				g.n.send_reliable(e.peer_id,"stopmoving",0)
				g.n.send_reliable(g.players[index].peer_id,"play_s helicopterstart.ogg",0)

				g.players[index].stunned=True
				g.players[index].stuntime=1500
				g.players[index].stuntimer.restart()
				name=g.players[index].name
				delay(1500)
				index=g.get_player_index_from(name)
				move_player(index,random(0,500),random(0,500),5,"helicopter")
				if not g.players[index].hidden: g.n.broadcast("distsound helicopterdist "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z)+" massacre_in_the_city",0)
				g.players[index].freedomhelicopter=True
				g.players[index].freedomhelicoptertimer.restart()
				g.players[index].helijumptimer.restart()

			if parsed[1]=="create":
				m=server_menu()
				m.intro="Select match visibility"
				m.initial_packet="matchv"
				m.add("Public match","public")
				m.add("Private match","private")
				m.send(e.peer_id)
			if parsed[1]=="join":
				if len(g.matches)<=0:
					g.n.send_reliable(g.players[index].peer_id,"No match created yet",0)
					g.players[index].prevmenu()
					return
				m=server_menu()
				m.intro="Please select a match to join."
				m.initial_packet="joinmatch"
				excluded_modes = {"snow", "sniper", "g", "teamk2", "teamf2", "collect", "sword", "g2", "minecraft", "teaml"}
				for match in g.matches:
					if not match.started:
						common_info = f"Match of {match.owner}, {match.get_mode()}, {'public' if match.password=='' else 'private'}, "
						player_info = f"{match.playersinoneteam} " + ("vs " + str(match.playersinoneteam) if match.mode not in {"snow", "sniper", "teamk2", "teamf2", "sword", "collect", "g", "g2", "minecraft", "teaml"} else "members required") + f", not started, with {len(match.players)} players"

						if match.mode not in excluded_modes:
							m.add(common_info + player_info, match.owner)
						elif match.mode in {"snow", "sniper", "teaml", "teamk2", "teamf2", "sword", "collect", "minecraft", "g", "g2"}:
							m.add(common_info + player_info.replace(" vs " + str(match.playersinoneteam), ""), match.owner)

				for match in g.matches:
					if match.started:
						common_info = f"Match of {match.owner}, in progress, {match.get_mode()}, {'public' if match.password=='' else 'private'}, "
						player_info = f"{match.playersinoneteam} " + ("vs " + str(match.playersinoneteam) if match.mode not in {"snow", "sniper", "teamk2", "teamf2", "sword", "collect", "g", "g2", "minecraft", "teaml"} else "members required") + f", with {len(match.players)} players"

						if match.mode not in excluded_modes:
							m.add(common_info + player_info, match.owner)
						elif match.mode in {"snow", "sniper", "teaml", "teamk2", "teamf2", "sword", "collect", "minecraft", "g", "g2"}:
							m.add(common_info + player_info.replace(" vs " + str(match.playersinoneteam), ""), match.owner)

				m.send(e.peer_id)
	elif(parsed[0]=="joinmatch" and len(parsed)>1):
	
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if len(g.matches)<=0:
				g.n.send_reliable(g.players[index].peer_id,"no matches found",0)
				return
			g.players[index].matchowner=parsed[1]
			for i in range(len(g.matches)):
				if g.matches[i].owner==parsed[1]:
					g.players[index].matchpasswordowner=parsed[1]
					if g.matches[i].password!="" and g.matches[i].owner not in g.players[index].invites:

						send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "matchpassword2", "Please enter to password of this match")
						return
					if g.matches[i].owner==parsed[1]:
						if g.matches[i].started: g.matches[i].add_spectator(g.players[index].name)
						else:
							if g.matches[i].mode=="snow" or g.matches[i].mode=="sniper" or g.matches[i].mode=="teamk2" or g.matches[i].mode=="teamf2" or g.matches[i].mode=="sword" or g.matches[i].mode=="collect" or g.matches[i].mode=="g" or g.matches[i].mode=="g2" or g.matches[i].mode=="minecraft" or g.matches[i].mode=="teaml": g.matches[i].add_player(g.players[index].name,""); return
							m=server_menu()
							m.intro="Select team"
							m.initial_packet="matchteamselect"
							if g.matches[i].players_on_team("red")<g.matches[i].playersinoneteam: m.add("red, "+str(g.matches[i].players_on_team("red"))+" players, "+g.matches[i].player_list_on_team("red"),"red")
							if g.matches[i].players_on_team("blue")<g.matches[i].playersinoneteam: m.add("blue, "+str(g.matches[i].players_on_team("blue"))+" players, "+g.matches[i].player_list_on_team("blue"),"blue")

							m.send(e.peer_id); return
	elif parsed[0]=="matchteamselect2" and len(parsed)>1:
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="" or parsed[1]=="back" or parsed[1]=="[cncel]":
				return
			try: newmatch2(g.players[index].mowner,int(g.players[index].mplayerinoneteam),g.players[index].mmode,g.players[index].mpassword,g.players[index].mbotcount,parsed[1])
			except: pass
	elif parsed[0]=="matchteamselect" and len(parsed)>1:
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="" or parsed[1]=="back" or parsed[1]=="[cncel]":
				return
			for i in range(len(g.matches)):
				if g.matches[i].owner==g.players[index].matchpasswordowner:
					g.matches[i].add_player(g.players[index].name,parsed[1])
	elif parsed[0]=="matchpassword2" and len(parsed)>1:
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="" or parsed[1]=="back" or parsed[1]=="[cncel]":
				return
			for i in range(len(g.matches)):
				if g.matches[i].owner==g.players[index].matchpasswordowner:
					if g.matches[i].password!=parsed[1]:
						g.n.send_reliable(g.players[index].peer_id,"Incorrect password",0);g.players[index].prevmenu(); 
						if g.players[index].is_admin()==True or g.players[index].dev==True:
							g.n.send_reliable(g.players[index].peer_id,g.matches[i].password,2)
						return
					if g.matches[i].started: g.matches[i].add_spectator(g.players[index].name)
					else: 
						if g.matches[i].mode=="snow" or g.matches[i].mode=="sniper" or g.matches[i].mode=="teamk2" or g.matches[i].mode=="teamf2" or g.matches[i].mode=="sword" or g.matches[i].mode=="collect" or g.matches[i].mode=="g" or g.matches[i].mode=="g2" or g.matches[i].mode=="minecraft" or g.matches[i].mode=="teaml": g.matches[i].add_player(g.players[index].name,""); return
						m=server_menu()
						m.intro="Select team"
						m.initial_packet="matchteamselect"
						if g.matches[i].players_on_team("red")<g.matches[i].playersinoneteam: m.add("red, "+str(g.matches[i].players_on_team("red"))+" players, "+g.matches[i].player_list_on_team("red"),"red")
						if g.matches[i].players_on_team("blue")<g.matches[i].playersinoneteam: m.add("blue, "+str(g.matches[i].players_on_team("blue"))+" players, "+g.matches[i].player_list_on_team("blue"),"blue")

						m.send(e.peer_id)

	elif parsed[0]=="matchv" and len(parsed)>1:
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="back" or parsed[1]=="":
				g.n.send_reliable(g.players[index].peer_id,"canceled",0)
				return
			if parsed[1]=="" or parsed[1]=="back":
				return

			if parsed[1]=="private":
				send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "matchpassword", "Please enter a match password")
				return
			if parsed[1]=="public":
				m=server_menu()
				m.intro="Select match mode"
				m.initial_packet="matchpublic"
				m.add("Team dead match","teamd")
				m.add("Knife fight match teamed","teamk")
				m.add("Knife fight match not teamed","teamk2")
				m.add("hand to hand combat teamed","teamf")
				m.add("hand to hand combat not teamed","teamf2")

				m.add("Snowflake survival teamed","teamsnow")
				m.add("Snowflake survival not teamed","snow")
				m.add("Sniper duel teamed","teamsniper")
				m.add("Sniper duel not teamed","sniper")
				m.add("Zombie survival","teamz")
				m.add("Zombie vs player","teamz2")
				m.add("Explosive battle teamed","teamg")
				m.add("Explosive battle not teamed","g")
				m.add("Abyss Clash teamed","teamg2")
				m.add("Abyss Clash not teamed","g2")
				m.add("Sword duel teamed","teamsword")
				m.add("Sword duel not teamed","sword")
				m.add("Collector's arena teamed","teamcollect")
				m.add("Collector's arena not teamed","collect")
				m.add("Capture the flag","teamc")
				m.add("Last man standing","teaml")
				#m.add("Medieval combat teamed","teamminecraft")
				#m.add("Medieval combat not teamed","minecraft")
				m.send(e.peer_id)
				return
	elif parsed[0]=="matchpublic" and len(parsed)>1:
		index=g.get_player_index(e.peer_id)
		if index == -1:
			return

		if parsed[1] == "" or parsed[1] == "back":
			return

		g.players[index].mmode=parsed[1]
		m=server_menu()
		m.intro="Select the match type"
		m.initial_packet="matchmodepublic"

		member_based_modes = {"snow", "sniper", "teamk2", "teamf2", "sword", "collect", "g2", "g", "teaml", "minecraft"}
		team_based_modes = {"teamminecraft", "teamg2", "teamg"}

		if g.players[index].mmode in member_based_modes:
			for i in range(2,11):
				m.add(f"{i} members", str(i))
		elif g.players[index].mmode in team_based_modes:
			for i in range(1,6):
				m.add(f"{i} vs {i}", str(i))
		else:
			for i in range(1,6):
				m.add(f"{i} vs {i}", str(i))

		m.send(e.peer_id)
		return
	elif parsed[0]=="matchmodepublic" and len(parsed)>1:
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="":
				g.n.send_reliable(g.players[index].peer_id,"canceled",0)
				return
			if parsed[1]=="" or parsed[1]=="back":
				return

			if parsed[1]=="0":
				g.n.send_reliable(g.players[index].peer_id,"canceled",0)
				return
			g.players[index].matchtypeamount=parsed[1]
			if g.players[index].mmode=="teamc":
				for m in g.matches:
					if m.owner==g.players[index].name: send_reliable(e.peer_id,"The match you created before didn't end yet, please wait for it to end before you can create a new match.",0); return
				newmatch(g.players[index].name,g.players[index].matchtypeamount,g.players[index].mmode,"",0)
				return
			m=server_menu()
			m.initial_packet="matchmodepublicbot"
			m.intro="Would you like to add bot in this match"
			m.add("yes, i want to add bot in this match","1")
			m.add("no, i dont want to add bot in this match","0")
			m.send(e.peer_id)
			return
	elif parsed[0]=="matchpassword" and len(parsed)>1:
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if parsed[1]=="" or parsed[1]=="back" or parsed[1]=="[cncel]":
				return

			g.players[index].matchpassword=parsed[1]
			m=server_menu()
			m.intro="You choosed to be private match. Select match mode"
			m.initial_packet="matchprivate"
			m.add("Team dead match","teamd")
			m.add("hand to hand combat teamed","teamf")
			m.add("hand to hand combat not teamed","teamf2")

			m.add("Knife fight match teamed","teamk")
			m.add("Knife fight match not teamed","teamk2")
			m.add("Snowflake survival teamed","teamsnow")
			m.add("Snowflake survival not teamed","snow")
			m.add("Sniper duel teamed","teamsniper")
			m.add("Sniper duel not teamed","sniper")
			m.add("Zombie survival","teamz")
			m.add("Zombie vs player","teamz2")
			m.add("Explosive battle teamed","teamg")
			m.add("Explosive battle not teamed","g")
			m.add("Abyss Clash teamed","teamg2")
			m.add("Abyss Clash not teamed","g2")
			m.add("Sword duel teamed","teamsword")
			m.add("Sword duel not teamed","sword")
			m.add("Collector's arena teamed","teamcollect")
			m.add("Collector's arena not teamed","collect")
			m.add("Capture the flag","teamc")
			m.add("Last man standing","teaml")
			#m.add("Medieval combat teamed","teamminecraft")
			#m.add("Medieval combat not teamed","minecraft")
			m.send(e.peer_id)
			return
	elif parsed[0]=="matchprivate" and len(parsed)>1:
		index=g.get_player_index(e.peer_id)
		if index == -1:
			return

		if parsed[1] == "" or parsed[1] == "back":
			g.n.send_reliable(g.players[index].peer_id,"canceled",0)
			return

		g.players[index].mmode=parsed[1]
		m=server_menu()
		m.intro="Select the match type"
		m.initial_packet="matchmodeprivate"

		member_based_modes = {"snow", "sniper", "teamk2", "teamf2", "sword", "g2", "g", "teaml", "collect", "minecraft"}
		team_based_modes = {"teamminecraft", "teamg2", "teamg"}

		if g.players[index].mmode in member_based_modes:
			for i in range(2,11):
				m.add(f"{i} members",str(i))
		elif g.players[index].mmode in team_based_modes:
			for i in range(1,6):
				m.add(f"{i} vs {i}",str(i))
		else:
			for i in range(1,6):
				m.add(f"{i} vs {i}",str(i))

		m.send(e.peer_id)
		return

	return True
