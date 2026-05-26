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

def handle_gameplay_6(e, parsed, index):
	global languages
	cmds = {"move_to", "wcoords", "accounts", "close", "spawn_player", "force_rn_2", "whonear", "accountlogin", "move_to_a", "update_zone", "whoonline", "move_to_a2", "force_rn_1", "bikemove"}
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

	if parsed[0]=="bikemove":
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			try:
				g.players[index].bike.move(index)
			except: pass
# --- ZORUNLU RENAME ADIM 1: YENI ISIM ISTE ---
	if parsed[0] == "force_rn_1":
		index = g.get_player_index(e.peer_id)
		if index > -1:
			# İptal veya boş giriş kontrolü - İptal ederse oyundan atılır
			if "[cncel]" in e.message:
				g.n.send_reliable(e.peer_id, "Rename required to play.", 0)
				remove_from_server(index, True)
				return

			new_name = e.message.replace("force_rn_1 ", "")

			# Geçerlilik kontrolleri
			if not new_name.isascii():
				send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "force_rn_1", "Invalid format! Use English letters/numbers only. Try again:")
				return
			if " " in new_name:
				send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "force_rn_1", "Invalid name! Use English letters/numbers and do not use spaces. Try again:")
				return


			# İsim dolu mu?
			if directory_exists2("chars/" + new_name) or directory_exists2("chars/" + new_name.lower()):
				send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "force_rn_1", "This username is already taken. Try another:")
				return

			# İsmi geçici olarak kaydet ve 2. onayı iste
			g.players[index].force_new_name_temp = new_name
			send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "force_rn_2", f"Please re-enter '{new_name}' to confirm change:")

	# --- ZORUNLU RENAME ADIM 2: ONAY VE ISLEM ---
	if parsed[0] == "force_rn_2":
		index = g.get_player_index(e.peer_id)
		if index > -1:
			# İptal kontrolü
			if "[cncel]" in e.message:
				remove_from_server(index, True)
				return

			confirm_name = e.message.replace("force_rn_2 ", "")
			
			# İsimler eşleşiyor mu?
			if not hasattr(g.players[index], 'force_new_name_temp') or g.players[index].force_new_name_temp != confirm_name:
				send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "force_rn_1", "Names did not match! Please start over:")
				return

			old_name = g.players[index].name
			new_name = g.players[index].force_new_name_temp

			# --- VERITABANI GUNCELLEMELERI (Normal rename ile aynı işlemler) ---
			
			# Ticketlar
			for ticket in g.tickets:
				if ticket["owner"] == old_name: ticket["owner"] = new_name
			
			# Gruplar
			for grp in g.groups:
				if grp.owner == old_name: grp.owner = new_name
				if old_name in grp.members:
					for m in range(len(grp.members)):
						if grp.members[m] == old_name: grp.members[m] = new_name
				if old_name in grp.admins:
					for m in range(len(grp.admins)):
						if grp.admins[m] == old_name: grp.admins[m] = new_name

			# Topluluklar
			for grp in g.communitys:
				if grp.owner == old_name: grp.owner = new_name
				if old_name in grp.members:
					for m in range(len(grp.members)):
						if grp.members[m] == old_name: grp.members[m] = new_name
				if old_name in grp.admins:
					for m in range(len(grp.admins)):
						if grp.admins[m] == old_name: grp.admins[m] = new_name

			# Arkadaşlar (Online ve Offline dosyalar)
			for friend in g.players[index].friendlist:
				ind = get_player_index_from(friend)
				if ind > -1:
					try:
						if old_name in g.players[ind].friendlist:
							f = g.players[ind].friendlist.index(old_name)
							g.players[ind].friendlist[f] = new_name
					except: pass
				else:
					try:
						if file_exists("chars/" + friend + "/friendlist.usr"):
							flist = pickle.loads(file_get_contents("chars/" + friend + "/friendlist.usr", "rb"))
							if old_name in flist:
								f = flist.index(old_name)
								flist[f] = new_name
								file_put_contents("chars/" + friend + "/friendlist.usr", pickle.dumps(flist), "wb")
					except: pass

			# Timed Itemlar
			for t_item in g.timeditems:
				if t_item.owner == old_name: t_item.owner = new_name
			
			# --- FIZIKSEL RENAME ISLEMI ---
			
			# 1. Mevcut durumu kaydet (eski klasöre)
			save_char(index)
			
			adminsend(f"FORCED RENAME: {old_name} changed to {new_name}")

			g.n.send_reliable(e.peer_id, "Success! Please login with your new name.", 2)
			
			# 2. Oyuncuyu bellekten sil (remove_from_server)
			# Bu sırada save_char tekrar çalışır, sorun yok eski isme yazar.
			remove_from_server(index, True) 

			try:
				os.rename("chars/"+old_name, "chars/"+new_name)
			except Exception as ex:
				adminsend(f"Rename error for {old_name}: {str(ex)}")
	elif(parsed[0]=="spawn_player" and len(parsed) > 5):
	
		_hidden_on_spawn = file_exists("chars/"+parsed[5]+"/hidden.usr") and file_get_contents("chars/"+parsed[5]+"/hidden.usr")=="1"
		spawn_player(float(parsed[1]), float(parsed[2]), float(parsed[3]), parsed[4], parsed[5], e.peer_id, int(parsed[6]), _hidden_on_spawn)
		if parsed[4].startswith("match"): g.n.send_reliable(e.peer_id,"stopmoving",0)	
		index=len(g.players)-1
		if(index>-1):

			dir="chars/"+g.players[index].name
			# NEW: Load last_admin_login_ticket_count
			g.players[index].last_admin_login_ticket_count = 0 # Default
			try:
				if file_exists(dir + "/last_admin_login_ticket_count.usr"):
					g.players[index].last_admin_login_ticket_count = int(file_get_contents(dir + "/last_admin_login_ticket_count.usr"))
			except (ValueError, TypeError):
				g.players[index].last_admin_login_ticket_count = 0 # Reset if corrupted
			# ... (existing loading logic) ...

			# NEW: Check for new tickets if player is admin/dev
			if g.players[index].is_admin() or g.players[index].dev:
				current_open_tickets = get_open_ticket_count()
				new_tickets_since_last_login = current_open_tickets - g.players[index].last_admin_login_ticket_count
				if new_tickets_since_last_login > 0:
					g.n.send_reliable(e.peer_id, f"There are {new_tickets_since_last_login} new support tickets since your last login!", 2)
				# Update their last seen count to current
				g.players[index].last_admin_login_ticket_count = current_open_tickets
				charwrite(g.players[index].name, "last_admin_login_ticket_count", g.players[index].last_admin_login_ticket_count) # Save immediately

			if os.path.isfile(dir+"/pmdata.usr"):
				data=pickle.loads(file_get_contents(dir+"/pmdata.usr","rb"))
				for key in list(data.keys()):
					g.n.send_reliable(g.players[index].peer_id,"pm You have a Pm from "+key+": "+data[key],0)
					del data[key]
				file_put_contents(dir+"/pmdata.usr",pickle.dumps(data),"wb")
			if os.path.isfile(dir+"/staffdata.usr"):
				data=pickle.loads(file_get_contents(dir+"/staffdata.usr","rb"))
				for key in list(data.keys()):
					g.n.send_reliable(g.players[index].peer_id,"adminmessage The staff member of "+key+" sent you a message: "+data[key],0)
					g.n.send_reliable(g.players[index].peer_id,"play_s misc214.ogg",0)
					g.n.send_reliable(g.players[index].peer_id,"play_s misc305.ogg",0)

					del data[key]
				file_put_contents(dir+"/staffdata.usr",pickle.dumps(data),"wb")

			if file_exists("chars/"+g.players[index].name+"/inventory.usr")==True:
				f=open(dir+"/inventory.usr","rb")
				g.players[index].inv=pickle.loads(f.read())
				f.close()
			if os.path.isfile(dir+"/weapon.usr"):
				w=file_get_contents(dir+"/weapon.usr")
				if g.players[index].get_item_count(w)>=1:
					g.players[index].weapon=w
					g.n.send_reliable(e.peer_id,"drawsilent "+w,0)
					g.players[index].get_weapon_properties(w)
			if os.path.isfile(dir+"/weapon2.usr"):
				w=file_get_contents(dir+"/weapon2.usr")
				if g.players[index].get_item_count(w)>=1:
					g.players[index].weapon2=w
					g.n.send_reliable(e.peer_id,"draw2silent "+w,0)
					g.players[index].get_weapon_properties(w)

			if file_exists("chars/"+g.players[index].name+"/storeinventory.usr")==True:
				f=open(dir+"/storeinventory.usr","rb")
				g.players[index].storeinv=pickle.loads(f.read())
				f.close()
			if 1:
				try:
					f=open(dir+"/ammo.usr","rb")
					g.players[index].ammo=pickle.loads(f.read())
					f.close()
				except: pass
				try: 
					f=open(dir+"/bought_chars.usr","rb")
					g.players[index].bought_chars=pickle.loads(f.read())
					f.close()
				except: pass
				try: 
					f=open(dir+"/current_char.usr","rb")
					g.players[index].current_char=pickle.loads(f.read())
					f.close()
					if g.players[index].current_char not in g.players[index].bought_chars: g.players[index].current_char="tristan"
					if "kado" in g.players[index].bought_chars: g.players[index].bought_chars.remove("kado"); g.players[index].bought_chars.append("kade")
					if g.players[index].current_char=="kado": g.players[index].current_char="kade"; g.players[index].get_char_properties()
					if "default" in g.players[index].bought_chars: g.players[index].bought_chars.remove("default"); g.players[index].bought_chars.append("tristan")
					if g.players[index].current_char=="": g.players[index].current_char="tristan"; g.players[index].get_char_properties()
					if g.players[index].current_char=="default": g.players[index].current_char="tristan"; g.players[index].get_char_properties()

					if "default" in g.players[index].bought_chars: g.players[index].bought_chars.remove("default"); g.players[index].bought_chars.append("tristan")
					if g.players[index].current_char=="default": g.players[index].current_char="tristan"; g.players[index].get_char_properties()

				except: pass

				try: 
					f=open(dir+"/blocks.usr","rb")
					g.players[index].blocks=pickle.loads(f.read())
					f.close()

				except: pass
				try: 

					f=open(dir+"/groupinvitations.usr","rb")
					g.players[index].groupinvitations=pickle.loads(f.read())
					f.close()
				except: pass
				try: 

					f=open(dir+"/communityinvitations.usr","rb")
					g.players[index].communityinvitations=pickle.loads(f.read())
					f.close()
				except: pass
				try: 


					f=open(dir+"/pendingfriendlist.usr","rb")
					g.players[index].pendingfriendlist=pickle.loads(f.read())
					f.close()
					if len(g.players[index].pendingfriendlist)>0:
						for item in g.players[index].pendingfriendlist:
							g.n.send_reliable(g.players[index].peer_id,"play_s misc10.ogg",0)
							g.n.send_reliable(g.players[index].peer_id,"friend "+item+" wants to add you as friend!",0)
				except: pass
				try: 

					f=open(dir+"/groupinvitations.usr","rb")
					g.players[index].groupinvitations=pickle.loads(f.read())
					f.close()
				except: pass

				try: 

					f=open(dir+"/friendlist.usr","rb")
					g.players[index].friendlist=pickle.loads(f.read())
					f.close()
				except: pass
				try: 

					if file_exists(dir+"/ticketinform.usr"):
						g.n.send_reliable(e.peer_id,file_get_contents(dir+"/ticketinform.usr"),2)
						file_delete(dir+"/ticketinform.usr")
				except: pass
				try:
					if file_exists(dir+"/jailtime.usr"):
						g.players[index].jailreason=file_get_contents(dir+"/jailreason.usr")
						g.players[index].jailtime=int(file_get_contents(dir+"/jailtime.usr"))
						g.players[index].jailed=True
						g.players[index].jailtimer.elapsed=(tm.time()-int(file_get_contents(dir+"/jailtimestamp.usr")))*1000
				except: pass
				try: 

					if file_exists(dir+"/groupinform.usr"):
						g.n.send_reliable(e.peer_id,"play_s misc263.ogg",0)
						g.n.send_reliable(e.peer_id,"groupnotification "+file_get_contents(dir+"/groupinform.usr"),0)
						file_delete(dir+"/groupinform.usr")
				except: pass

				try: 

					if file_exists(dir+"/communityinform.usr"):
						g.n.send_reliable(e.peer_id,"play_s misc263.ogg",0)
						g.n.send_reliable(e.peer_id,"communitynotification "+file_get_contents(dir+"/communityinform.usr"),0)
						file_delete(dir+"/communityinform.usr")
				except: pass
				try: 

					f=open(dir+"/tokenplayers.usr","rb")
					g.players[index].tokenplayers=pickle.loads(f.read())
					f.close()
				except: pass

				try: 

					f=open(dir+"/silenced.usr","rb")
					g.players[index].silenced=pickle.loads(f.read())
					f.close()
				except: pass

				try: 

					f=open(dir+"/playerkills.usr","r")
					g.players[index].playerkills=int(f.read())
					f.close()
				except: pass
				try: 

					f=open(dir+"/helitimer.usr","r")
					g.players[index].helitimer.elapsed=int(f.read())
					f.close()
				except: pass
				try: 

					f=open(dir+"/helijumptimer.usr","r")
					g.players[index].helijumptimer.elapsed=int(f.read())
					f.close()
				except: pass

				try: 

					f=open(dir+"/freedomhelicoptertimer.usr","r")
					g.players[index].freedomhelicoptertimer.elapsed=int(f.read())
					f.close()
				except: pass

				try: 

					f=open(dir+"/freedomhelicopter.usr","r")
					g.players[index].freedomhelicopter=bool(f.read())
					f.close()
				except: pass

				try: 

					f=open(dir+"/facing.usr","r")
					g.n.send_reliable(e.peer_id,"facing "+str(f.read()),0)
					g.players[index].facing=int(f.read())
					f.close()
				except: pass
				try: 

					f=open(dir+"/adrenalinetime.usr","r")
					g.players[index].adrenalinetimer.elapsed=int(f.read())
					f.close()
					if file_exists(dir+"/adrenaline.usr"): g.players[index].adrenaline=True
				except: pass
				try: 

					f=open(dir+"/jammertime.usr","r")
					g.players[index].jammertimer.elapsed=int(f.read())
					f.close()
					if file_exists(dir+"/jammer.usr"): g.players[index].jammer=True
				except: pass

				try: 

					f=open(dir+"/backpacks_level.usr","r")
					g.players[index].backpacks_level=int(f.read())
					f.close()
				except: pass
				try: 

					f=open(dir+"/beacon.usr","r")
					g.players[index].beacon=int(f.read())
					f.close()
				except: pass
				try: 

					f=open(dir+"/parachuted.usr","r")
					g.players[index].parachuted=int(f.read())
					f.close()
				except: pass

				if g.players[index].parachuted==1: g.players[index].parachuted=True
				elif g.players[index].parachuted==0: g.players[index].parachuted=False
				if g.players[index].parachuted:
					if 1:
						if 1:
							g.n.send_reliable(g.players[index].peer_id,"stopmoving",0)
							g.players[index].playsound("parachuteopen")
							if not g.players[index].hidden: g.n.broadcast("distsound parachute_dist "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z)+" "+g.players[index].map, 0)
							g.n.send_reliable(g.players[index].peer_id, "parachute_start", 0)


				try: 

					f=open(dir+"/spatialized_by.usr","r")
					g.players[index].spatialized_by=f.read()
					f.close()
				except: pass


				try: 

					f=open(dir+"/spatializertimer.usr","r")
					g.players[index].spatializertimer.elapsed=int(f.read())
					f.close()
				except: pass



				try: 

					f=open(dir+"/backpacktimer.usr","rb")
					g.players[index].backpacktimer=pickle.loads(f.read())
					f.close()
				except: pass



				try: 

					f=open(dir+"/playerdeaths.usr","r")
					g.players[index].playerdeaths=int(f.read())
					f.close()
				except: pass
				try: 

					f=open(dir+"/botkills.usr","r")
					g.players[index].botkills=int(f.read())
					f.close()
				except: pass
				try: 

					f=open(dir+"/botdeaths.usr","r")
					g.players[index].botdeaths=int(f.read())
					f.close()
				except: pass
				g.players[index].get_char_properties()
				g.n.send_reliable(g.players[index].peer_id,pickle.dumps(g.players[index].inv),19)
			try:
				f=open(dir+"/compid.usr", "r")
				g.players[index].compid=f.read()
				f.close()
			except: pass
			try:
				g.n.send_reliable(e.peer_id,"updatelang "+g.players[index].lang+" "+file_get_contents("lang/"+g.players[index].lang+".lng"),0)
			except: pass
			#if(file_exists("chars/"+g.players[index].name+"/maldied.usr")==True):
				#file_delete("chars/"+g.players[index].name+"/maldied.usr")
				#g.players[index].x=random(0, 0)
				#g.players[index].y=random(0, 0)
				#move_player(index,random(5,5),random(0,0),0,"lobby")
				#g.n.send_reliable(g.players[index].peer_id, "move "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z),0)
				#g.n.broadcast("update_player "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z)+" "+g.players[index].map+" "+g.players[index].name+" "+str(g.players[index].facing),20)
			f=open(dir+"/health.usr","r")
			g.players[index].health=string_to_number(f.read())
			f.close()
			try:
				f=open(dir+"/zhtoken.usr","r")
				g.players[index].zhtoken=string_to_number(f.read())
				f.close()
			except: pass
			try:
				f=open(dir+"/corpse_bomb.usr","r")
				g.players[index].corpse_bomb=string_to_number(f.read())
				f.close()
			except: pass

			try:
				f=open(dir+"/eventpoint.usr","r")
				g.players[index].eventpoint=string_to_number(f.read())
				f.close()
			except: pass
			try:
				f=open(dir+"/currenteventpoint.usr","r")
				g.players[index].currenteventpoint=string_to_number(f.read())
				f.close()
			except: pass
			try:
				f=open(dir+"/task_data.usr","rb")
				g.players[index].task_data=pickle.loads(f.read())
				f.close()
			except: pass

			try: 

				f=open(dir+"/flag.usr","r")
				g.players[index].flag=string_to_number(f.read())
				f.close()
			except: pass
			try: 

				f=open(dir+"/matchteam.usr","r")
				g.players[index].matchteam=f.read()
				f.close()
			except: pass
			try: 

				f=open(dir+"/joinedmatch.usr","r")
				g.players[index].joinedmatch=f.read()
				f.close()
			except: pass
			try:
				f=open(dir+"/matchmode.usr","r")
				g.players[index].matchmode=f.read()
				f.close()

			except: pass
			try: 

				f=open(dir+"/lang.usr","r")
				g.players[index].lang=f.read()
				if not file_exists("lang/"+g.players[index].lang+".lng"):
					g.players[index].lang="en"
					g.n.send_reliable(e.peer_id,"switchlang en english",0)
				f.close()
			except: pass
			try: 

				f=open(dir+"/specmatch.usr","r")
				g.players[index].specmatch=f.read()
				f.close()

			except: pass
			try: 

				f=open(dir+"/banned.usr","rb")
				g.players[index].matchbanned=pickle.loads(f.read())
				f.close()
			except: pass
			try: 

				if file_exists(dir+"/scorepoint.usr")==True:
					f=open(dir+"/scorepoint.usr","r")
					g.players[index].scorepoint=string_to_number(f.read())
					g.players[index].check_rank()
					f.close()
			except: pass
			try:
				if file_exists(dir+"/langchan.usr")==True:
					f=open(dir+"/langchan.usr","r")
					g.players[index].langchan=f.read()
					f.close()
					if g.players[index].langchan=="disable": g.n.send_reliable(g.players[index].peer_id,"chatdisable",0)



			except: pass
			try:

				if file_exists(dir+"/gender.usr")==True:
					f=open(dir+"/gender.usr","r")
					g.players[index].gender=f.read()
					f.close()
			except: pass
			try:

				if file_exists(dir+"/shieldhitchance.usr")==True:
					f=open(dir+"/shieldhitchance.usr","r")
					g.players[index].shieldhitchance=int(f.read())
					if g.players[index].shieldhitchance>0: g.players[index].shielded=True
					f.close()
			except: pass
			try:

				if file_exists(dir+"/helmethitchance.usr")==True:
					f=open(dir+"/helmethitchance.usr","r")
					g.players[index].helmethitchance=int(f.read())
					if g.players[index].helmethitchance>0: g.players[index].helmeted=True
					f.close()
			except: pass
			try:

				if file_exists(dir+"/lasthelmethitchance.usr")==True:
					f=open(dir+"/lasthelmethitchance.usr","r")
					g.players[index].lasthelmethitchance=int(f.read())
					f.close()
			except: pass

			try:

				if file_exists(dir+"/chesttoken.usr")==True:
					f=open(dir+"/chesttoken.usr","r")
					g.players[index].chesttoken=int(f.read())
					f.close()


			except: pass
			try:

				if file_exists(dir+"/status.usr")==True:
					f=open(dir+"/status.usr","r")
					g.players[index].status=f.read()
					f.close()
			except: pass
			try:

				if file_exists(dir+"/blockvoice3.usr")==True:
					f=open(dir+"/blockvoice3.usr","r")
					g.players[index].blockvoice3=stn(f.read())
					if g.players[index].blockvoice3==1:
						g.n.send_reliable(g.players[index].peer_id,"enablevoicechat",0)

					if g.players[index].blockvoice3==0:
						g.n.send_reliable(g.players[index].peer_id,"disablevoicechat",0)
					f.close()
			except: pass
			try:
				if file_exists(dir+"/hidden.usr")==True:
					g.players[index].hidden=(file_get_contents(dir+"/hidden.usr")=="1")
					if g.players[index].hidden: g.n.send_reliable(g.players[index].peer_id,"You are currently hidden from other players.",0)
			except: pass
			try:

				if file_exists(dir+"/voicemessage.usr")==True:
					f=open(dir+"/voicemessage.usr","r")
					g.players[index].voicemessage=int(f.read())
					if g.players[index].voicemessage==1 and g.players[index].blockvoice3==0: g.n.send_reliable(e.peer_id,"enablevoicechat",0)
					if g.players[index].voicemessage==0:
						g.n.send_reliable(e.peer_id,"disablevoicechat",0)
					f.close()
			except: pass
			try:

				if file_exists(dir+"/voicemessage2.usr")==True:
					f=open(dir+"/voicemessage2.usr","r")
					g.players[index].voicemessage2=int(f.read())
					if g.players[index].voicemessage2==1 and g.players[index].blockvoice3==0: g.n.send_reliable(e.peer_id,"enablevoicechat2",0)
					if g.players[index].voicemessage2==0:
						g.n.send_reliable(e.peer_id,"disablevoicechat2",0)
					f.close()
			except: pass

			try:

				if file_exists(dir+"/scorerank.usr")==True:
					f=open(dir+"/scorerank.usr","r")
					g.players[index].scorerank=f.read()
					f.close()
			except: pass
			try:

				if file_exists(dir+"/ticketmail.usr")==True:
					f=open(dir+"/ticketmail.usr","r")
					g.players[index].ticketmail=stn(f.read())
					f.close()
			except: pass
			try:

				if file_exists(dir+"/matchinvite.usr")==True:
					f=open(dir+"/matchinvite.usr","r")
					g.players[index].matchinvite=stn(f.read())
					f.close()
			except: pass
			try:

				if file_exists(dir+"/communitymessage.usr")==True:
					f=open(dir+"/communitymessage.usr","r")
					g.players[index].communitymessage=stn(f.read())
					f.close()
			except: pass

			try:

				if file_exists(dir+"/paidtime.usr")==True:
					f=open(dir+"/paidtime.usr","r")
					g.players[index].paidtime=stn(f.read())
					f.close()
			except: pass
			try:

				if file_exists(dir+"/paidmonths.usr")==True:
					f=open(dir+"/paidmonths.usr","r")
					g.players[index].paidmonths=stn(f.read())
					f.close()
			except: pass

			try:

				if file_exists(dir+"/paid.usr")==True:
					g.players[index].paid=True
			except: pass

			try:

				if file_exists(dir+"/eventalerts.usr")==True:
					f=open(dir+"/eventalerts.usr","r")
					g.players[index].eventalerts=stn(f.read())
					f.close()
			except: pass

			try:

				if file_exists(dir+"/mapsound.usr")==True:
					f=open(dir+"/mapsound.usr","r")
					g.players[index].mapsound=stn(f.read())
					f.close()
			except: pass

			try:

				if file_exists(dir+"/authreq.usr")==True:
					f=open(dir+"/authreq.usr","r")
					g.players[index].authreq=stn(f.read())
					f.close()
			except: pass
			try:

				if file_exists(dir+"/votenotify.usr")==True:
					f=open(dir+"/votenotify.usr","r")
					g.players[index].votenotify=stn(f.read())
					f.close()
			except: pass

			try:

				if file_exists(dir+"/motorhistory.usr")==True:
					f=open(dir+"/motorhistory.usr","r")
					g.players[index].motorhistory=f.read()
					f.close()
			except: pass

			try:

				if file_exists(dir+"/leghits.usr")==True:
					f=open(dir+"/leghits.usr","r")
					g.players[index].leghits=stn(f.read())
					f.close()
			except: pass
			try:

				if file_exists(dir+"/legshots.usr")==True:
					f=open(dir+"/legshots.usr","r")
					g.players[index].legshots=stn(f.read())
					f.close()
			except: pass
			try:

				if file_exists(dir+"/headshots.usr")==True:
					f=open(dir+"/headshots.usr","r")
					g.players[index].headshots=stn(f.read())
					f.close()
			except: pass
			try:

				if file_exists(dir+"/headhits.usr")==True:
					f=open(dir+"/headhits.usr","r")
					g.players[index].headhits=stn(f.read())
					f.close()
			except: pass

			try:

				if file_exists(dir+"/istyping.usr")==True:
					f=open(dir+"/istyping.usr","r")
					g.players[index].istyping=stn(f.read())
					f.close()
			except: pass

			try:
				if file_exists(dir+"/chestpickupnotify.usr")==True:
					f=open(dir+"/chestpickupnotify.usr","r")
					g.players[index].chestpickupnotify=stn(f.read())
					f.close()
			except: pass

			try:

				if file_exists(dir+"/tokentransfer.usr")==True:
					f=open(dir+"/tokentransfer.usr","r")
					g.players[index].tokentransfer=stn(f.read())
					f.close()
			except: pass
			try:

				if file_exists(dir+"/pmmessage.usr")==True:
					f=open(dir+"/pmmessage.usr","r")
					g.players[index].pmmessage=int(f.read())
					f.close()
			except: pass
			try:

				if file_exists(dir+"/mapmessage.usr")==True:
					f=open(dir+"/mapmessage.usr","r")
					g.players[index].mapmessage=int(f.read())
					f.close()
			except: pass
			try:

				if file_exists(dir+"/groupmessage.usr")==True:
					f=open(dir+"/groupmessage.usr","r")
					g.players[index].groupmessage=int(f.read())
					f.close()
			except: pass
			try:

				if file_exists(dir+"/groupinvitation.usr")==True:
					f=open(dir+"/groupinvitation.usr","r")
					g.players[index].groupinvitation=int(f.read())
					f.close()


			except: pass
			try:

				if file_exists(dir+"/communityinvitation.usr")==True:
					f=open(dir+"/communityinvitation.usr","r")
					g.players[index].communityinvitation=int(f.read())
					f.close()


			except: pass

			try:

				if file_exists(dir+"/friendmessage.usr")==True:
					f=open(dir+"/friendmessage.usr","r")
					g.players[index].friendmessage=int(f.read())
					f.close()
			except: pass
			try:

				if file_exists(dir+"/friendonlinemessage.usr")==True:
					f=open(dir+"/friendonlinemessage.usr","r")
					g.players[index].friendonlinemessage=int(f.read())
					f.close()
			except: pass
			try:

				if file_exists(dir+"/matchmessage.usr")==True:
					f=open(dir+"/matchmessage.usr","r")
					g.players[index].matchmessage=int(f.read())
					f.close()
			except: pass
			try:

				if file_exists(dir+"/voicemessage.usr")==True:
					f=open(dir+"/voicemessage.usr","r")
					g.players[index].voicemessage=int(f.read())
					if g.players[index].voicemessage==1 and g.players[index].blockvoice3==0: g.n.send_reliable(e.peer_id,"enablevoicechat",0)
					if g.players[index].voicemessage==0:
						g.n.send_reliable(e.peer_id,"disablevoicechat",0)
					f.close()

			except: pass
			try:

				if file_exists(dir+"/voicemessage2.usr")==True:
					f=open(dir+"/voicemessage2.usr","r")
					g.players[index].voicemessage2=int(f.read())
					if g.players[index].voicemessage2==1 and g.players[index].blockvoice3==0: g.n.send_reliable(e.peer_id,"enablevoicechat2",0)
					if g.players[index].voicemessage2==0:
						g.n.send_reliable(e.peer_id,"disablevoicechat2",0)
					f.close()
			except: pass

			try:

				if file_exists(dir+"/teammessage.usr")==True:
					f=open(dir+"/teammessage.usr","r")
					g.players[index].teammessage=int(f.read())
					f.close()
			except: pass
			try:

				if file_exists(dir+"/faint.usr")==True:
					g.players[index].faint=True
					g.players[index].fainted=True
					g.n.send_reliable(e.peer_id,"stopmoving",0)
					g.players[index].fainttimer.elapsed=int(file_get_contents("chars/"+g.players[index].name+"/fainttime.usr"))
			except: pass
			try:

				if(file_exists(dir+"/admin.usr") and g.players[index].dev==False and g.players[index].builder==False):
				
					g.players[index].admin=True

#						g.players[index].title="administrator"
#						g.players[index].title2="administrator"

					g.n.send_reliable(g.players[index].peer_id,"Welcome dear admin!",0)
					g.n.send_reliable(g.players[index].peer_id,"isadmin",0)
#						g.n.broadcast(""+g.players[index].name+" is an admin of Zero Hour Assault",2)
			except: pass
			if(file_exists(dir+"/lasthp2.usr")==False):
				f=open(dir+"/lasthp2.usr","w")
				f.close()
				g.players[index].health=g.players[index].maxhealth
			try:

				if(file_exists(dir+"/moderator.usr") and g.players[index].dev==False and g.players[index].builder==False):
				
					g.players[index].moderator=True
#						g.players[index].title="Moderator"
#						g.players[index].title2="Moderator"

					g.n.send_reliable(g.players[index].peer_id,"Welcome dear moderator!",0)
					g.n.send_reliable(g.players[index].peer_id,"isadmin",0)
#						g.n.broadcast(""+g.players[index].name+" is a moderator of Zero Hour Assault",2)
			except: pass
			try:

				if(file_exists(dir+"/builder.usr") and g.players[index].dev==False and g.players[index].admin==False):
			
					g.players[index].builder=True
					g.n.send_reliable(g.players[index].peer_id,"welcome dear builder!",0)
#						g.players[index].title="builder"
#						g.players[index].title2="builder"

					g.n.send_reliable(g.players[index].peer_id,"isadmin",0)
			except: pass
			try:

				if(len(g.players)>0) :
					for i in range(len(g.players)):
						if g.players[i].hidden: continue
						g.players[index].packet("forcespawn "+str(g.players[i].x)+" "+str(g.players[i].y)+" "+str(g.players[i].z)+" "+g.players[i].map+" "+g.players[i].name+" "+str(g.players[i].samplerate),0)
					for i in range(len(g.npcs)):
						g.players[index].packet("forcespawn "+str(g.npcs[i].x)+" "+str(g.npcs[i].y)+" "+str(g.npcs[i].z)+" "+g.npcs[i].map+" "+g.npcs[i].name+" 48000",0)
					
				g.n.send_reliable(e.peer_id,"invcat drinks "+invdrinks,0)
				g.n.send_reliable(e.peer_id,"invcat weapons "+invweapons,0)
				g.n.send_reliable(e.peer_id,"invcat explosives "+invexplosives,0)
				g.n.send_reliable(e.peer_id,"invcat ammos "+invammos,0)
				g.n.send_reliable(e.peer_id,"invcat equipment "+invequipment,0)
				wnames=""
				w=["punch"]
				for i in range(len(w)):
					wnames+=w[i]+" "
				
				g.n.send_reliable(g.players[index].peer_id,"weaponlist "+wnames,0)
				for i in range(len(guns)):
					wnames+=guns[i]+" "
				g.n.send_reliable(g.players[index].peer_id,"gunlist "+wnames,0)
				wnames=""
				for i in range(len(g.nomudtiles)):
					wnames+=g.nomudtiles[i]+" "
				g.n.send_reliable(g.players[index].peer_id,"nomudtileslist "+wnames,0)
				for base in g.group_bases:
					if base.map==g.players[index].map: base.send_platform_to(g.players[index])
				for b in g.bikes:
					if b.map==g.players[index].map: b.send_platform_to(g.players[index])

				for chest in g.chests:
					if chest.map==g.players[index].map:
						send_platform(g.players[index], chest.x, chest.x, chest.y, chest.y, chest.z, chest.z+4, "wallmedal4")
						send_platform(g.players[index], chest.x, chest.x, chest.y, chest.y, chest.z+5, chest.z+5, "metal5")
				for electric in g.electrics:
					if electric.map==g.players[index].map:
						send_platform(g.players[index], electric.x, electric.x, electric.y, electric.y, electric.z, electric.z+4, "wallfence6")
						send_platform(g.players[index], electric.x, electric.x, electric.y, electric.y, electric.z+5, electric.z+5, "metal7")

				for mwall in g.mwalls:
					if not mwall.destroyed and mwall.map==g.players[index].map:
						send_platform(g.players[index], mwall.minx, mwall.maxx, mwall.miny, mwall.maxy, mwall.minz, mwall.maxz, mwall.tile)
				for ladder in g.ladders:
					if not ladder.destroyed and ladder.map==g.players[index].map:
						send_platform(g.players[index], ladder.minx, ladder.maxx, ladder.miny, ladder.maxy, ladder.minz, ladder.maxz, ladder.tile)

				for barricade in g.barricades:
					if not barricade.destroyed and barricade.map==g.players[index].map:
						send_platform(g.players[index], barricade.minx, barricade.maxx, barricade.miny, barricade.maxy, barricade.minz, barricade.maxz, barricade.tile)

						send_platform(g.players[index], barricade.minx, barricade.maxx, barricade.miny, barricade.maxy, barricade.minz+1, barricade.maxz+1, "dirt3")
				for motor in g.motors:
					if g.players[index].map==motor.map: send_platform(g.players[index], motor.x, motor.x, motor.y, motor.y, motor.z, motor.z+4, "wallspaceship")
					if g.players[index].map==motor.map: send_platform(g.players[index], motor.x, motor.x, motor.y, motor.y, motor.z+5, motor.z+5, "cloth")

				if len(g.msounds)>0:
					for i in range(len(g.msounds)):
						if "turnfacing" not in g.msounds[i].soundloop and "category" not in g.msounds[i].soundloop and "invisibility" not in g.msounds[i].soundloop and "helmet" not in g.msounds[i].soundloop and "shield" not in g.msounds[i].soundloop and "reload" not in g.msounds[i].soundloop:
							if not g.msounds[i].playmoving: g.n.send_reliable(g.players[index].peer_id, "createmsound "+str(g.msounds[i].id)+" "+g.msounds[i].soundloop+" "+str(g.msounds[i].x)+" "+str(g.msounds[i].y)+" "+str(g.msounds[i].z)+" "+g.msounds[i].map+" "+str(g.msounds[i].pitch), 0)
#					if not os.path.isfile("chars/"+g.players[index].name+"/sorry.usr"):
#						f=open("zitemdata.txt","w")
#						f.write("razeon="+g.players[index].name+"=1\n")
#						f.write("paid_account="+g.players[index].name+"=1\n")
#						f.close()
#						open("chars/"+g.players[index].name+"/sorry.usr","w").close()
#						g.players[index].zhtoken+=10000
#						g.n.send_reliable(g.players[index].peer_id,"you are received 10000 zero token, razeon character, and one month paid account! we are realy sorry that what happened earlier",2)
#						g.n.send_reliable(g.players[index].peer_id,"play_s sound_notif2-132674.ogg",0)

				g.n.send_reliable(g.players[index].peer_id,"play_s welcome.ogg",0)
				g.n.send_reliable(g.players[index].peer_id,"Welcome to zero_hour_assault! "+g.players[index].get_last_motd_changelog_reboot_counts(),2)
				g.n.send_reliable(g.players[index].peer_id,"current active event is "+get_task_name(),2)
				# --- ASCII KONTROLU VE ZORUNLU RENAME ---
				if not g.players[index].name.isascii():
					# Serverbox ile yeni isim iste
					#send_reliable(g.players[index].peer_id,"stopmoving",0)
					g.players[index].renaming=True
					send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "force_rn_1", "your account needs to be renamed because it contains non-english letters. Please type a new username with just english letters.")
				# ----------------------------------------
			except:
				for base in g.group_bases:
					if base.map==g.players[index].map: base.send_platform_to(g.players[index])
				for b in g.bikes:
					if b.map==g.players[index].map: b.send_platform_to(g.players[index])

				for chest in g.chests:
					if chest.map==g.players[index].map:
						send_platform(g.players[index], chest.x, chest.x, chest.y, chest.y, chest.z, chest.z+4, "wallmedal4")
						send_platform(g.players[index], chest.x, chest.x, chest.y, chest.y, chest.z+5, chest.z+5, "metal5")
				for electric in g.electrics:
					if electric.map==g.players[index].map:
						send_platform(g.players[index], electric.x, electric.x, electric.y, electric.y, electric.z, electric.z+4, "wallfence6")
						send_platform(g.players[index], electric.x, electric.x, electric.y, electric.y, electric.z+5, electric.z+5, "metal7")

				for mwall in g.mwalls:
					if not mwall.destroyed and mwall.map==g.players[index].map:
						send_platform(g.players[index], mwall.minx, mwall.maxx, mwall.miny, mwall.maxy, mwall.minz, mwall.maxz, mwall.tile)
				for ladder in g.ladders:
					if not ladder.destroyed and ladder.map==g.players[index].map:
						send_platform(g.players[index], ladder.minx, ladder.maxx, ladder.miny, ladder.maxy, ladder.minz, ladder.maxz, ladder.tile)

				for barricade in g.barricades:
					if not barricade.destroyed and barricade.map==g.players[index].map:
						send_platform(g.players[index], barricade.minx, barricade.maxx, barricade.miny, barricade.maxy, barricade.minz, barricade.maxz, barricade.tile)

						send_platform(g.players[index], barricade.minx, barricade.maxx, barricade.miny, barricade.maxy, barricade.minz+1, barricade.maxz+1, "dirt3")
				for motor in g.motors:
					if g.players[index].map==motor.map: send_platform(g.players[index], motor.x, motor.x, motor.y, motor.y, motor.z, motor.z+4, "wallspaceship")
					if g.players[index].map==motor.map: send_platform(g.players[index], motor.x, motor.x, motor.y, motor.y, motor.z+5, motor.z+5, "cloth")

				if len(g.msounds)>0:
					for i in range(len(g.msounds)):
						if "turnfacing" not in g.msounds[i].soundloop and "category" not in g.msounds[i].soundloop and "invisibility" not in g.msounds[i].soundloop and "helmet" not in g.msounds[i].soundloop and "shield" not in g.msounds[i].soundloop and "reload" not in g.msounds[i].soundloop:
							if not g.msounds[i].playmoving: g.n.send_reliable(g.players[index].peer_id, "createmsound "+str(g.msounds[i].id)+" "+g.msounds[i].soundloop+" "+str(g.msounds[i].x)+" "+str(g.msounds[i].y)+" "+str(g.msounds[i].z)+" "+g.msounds[i].map+" "+str(g.msounds[i].pitch), 0)
				if(file_exists(dir+"/lasthp.usr")==False):
					f=open(dir+"/lasthp.usr","w")
					f.close()
					g.players[index].health=g.players[index].maxhealth

				if(file_exists(dir+"/admin.usr") and g.players[index].dev==False and g.players[index].builder==False):
				
					g.players[index].admin=True

#						g.players[index].title="administrator"
#						g.players[index].title2="administrator"

					g.n.send_reliable(g.players[index].peer_id,"Welcome dear admin!",0)
					g.n.send_reliable(g.players[index].peer_id,"isadmin",0)
#						g.n.broadcast(""+g.players[index].name+" is an admin of Zero Hour Assault",2)

				if(file_exists(dir+"/moderator.usr") and g.players[index].dev==False and g.players[index].builder==False):
				
					g.players[index].moderator=True
#						g.players[index].title="Moderator"
#						g.players[index].title2="Moderator"

					g.n.send_reliable(g.players[index].peer_id,"Welcome dear moderator!",0)
					g.n.send_reliable(g.players[index].peer_id,"isadmin",0)
#						g.n.broadcast(""+g.players[index].name+" is a moderator of Zero Hour Assault",2)

				if(file_exists(dir+"/builder.usr") and g.players[index].dev==False and g.players[index].admin==False):
			
					g.players[index].builder=True
					g.n.send_reliable(g.players[index].peer_id,"welcome dear builder!",0)
#						g.players[index].title="builder"
#						g.players[index].title2="builder"

					g.n.send_reliable(g.players[index].peer_id,"isadmin",0)

				if(len(g.players)>0) :
					for i in range(len(g.players)):
						if g.players[i].hidden: continue
						g.players[index].packet("forcespawn "+str(g.players[i].x)+" "+str(g.players[i].y)+" "+str(g.players[i].z)+" "+g.players[i].map+" "+g.players[i].name+" "+str(g.players[i].samplerate),0)
					for i in range(len(g.npcs)):
						g.players[index].packet("forcespawn "+str(g.npcs[i].x)+" "+str(g.npcs[i].y)+" "+str(g.npcs[i].z)+" "+g.npcs[i].map+" "+g.npcs[i].name+" 48000",0)
					
				g.n.send_reliable(e.peer_id,"invcat drinks "+invdrinks,0)
				g.n.send_reliable(e.peer_id,"invcat weapons "+invweapons,0)
				g.n.send_reliable(e.peer_id,"invcat explosives "+invexplosives,0)
				g.n.send_reliable(e.peer_id,"invcat ammos "+invammos,0)
				g.n.send_reliable(e.peer_id,"invcat equipment "+invequipment,0)
#					if not os.path.isfile("chars/"+g.players[index].name+"/sorry.usr"):
#						f=open("zitemdata.txt","w")
#						f.write("razeon="+g.players[index].name+"=1\n")
#						f.write("paid_account="+g.players[index].name+"=1\n")
#						f.close()
#						open("chars/"+g.players[index].name+"/sorry.usr","w").close()
#						g.players[index].zhtoken+=10000
#						g.n.send_reliable(g.players[index].peer_id,"you are received 10000 zero token, razeon character, and one month paid account! we are realy sorry that what happened earlier",2)
#						g.n.send_reliable(g.players[index].peer_id,"play_s sound_notif2-132674.ogg",0)

				g.n.send_reliable(g.players[index].peer_id,"play_s welcome.ogg",0)
				g.n.send_reliable(g.players[index].peer_id,"Welcome to zero_hour_assault! "+g.players[index].get_last_motd_changelog_reboot_counts(),2)
				g.n.send_reliable(g.players[index].peer_id,"current active event is "+get_task_name(),2)

				# --- ASCII KONTROLU VE ZORUNLU RENAME ---
				if not g.players[index].name.isascii():
					# Serverbox ile yeni isim iste
					#send_reliable(g.players[index].peer_id,"stopmoving",0)
					g.players[index].renaming=True
					send_serverbox(g.players[index].peer_id, 0, -1, 0, -1, "force_rn_1", "your account needs to be renamed because it contains non-english letters. Please type a new username with just english letters.")

				# ----------------------------------------
			if g.players[index].blockvoice3==1:
				g.n.send_reliable(g.players[index].peer_id,"disablevoicechat",0)
			if file_exists("frozen.txt")==True: g.gamestop=1
			if g.gamestop==1:
				g.n.send_reliable(g.players[index].peer_id,"stopmoving",0)

				g.n.send_reliable(g.players[index].peer_id,"play_s important.ogg",0)
				g.n.send_reliable(g.players[index].peer_id,"Attention. The game is frozen. Please be patient.",2)


				if g.players[index].blockvoice3==1:
					g.n.send_reliable(g.players[index].peer_id,"disablevoicechat",0)
				if len(g.msounds)>0:
					for i in range(len(g.msounds)):
						if "category" not in g.msounds[i].soundloop and "turnfacing" not in g.msounds[i].soundloop and "invisibility" not in g.msounds[i].soundloop and "helmet" not in g.msounds[i].soundloop and "shield" not in g.msounds[i].soundloop and "reload" not in g.msounds[i].soundloop:
							if not g.msounds[i].playmoving: g.n.send_reliable(g.players[index].peer_id, "createmsound "+str(g.msounds[i].id)+" "+g.msounds[i].soundloop+" "+str(g.msounds[i].x)+" "+str(g.msounds[i].y)+" "+str(g.msounds[i].z)+" "+g.msounds[i].map+" "+str(g.msounds[i].pitch), 0)
			if g.players[index].map=="lobby" and (g.players[index].x>100 or g.players[index].y>100):
				move_player(index,5,0,0,"lobby")
			if g.players[index].map=="lobby":
				g.n.send_reliable(e.peer_id,"parachute_stop",0)
				g.players[index].parachuted=False
		
	elif(parsed[0]=="close"):
	
		index=g.get_player_index(e.peer_id)
		if(index > -1):
		
			remove_from_server(index)
			
		
	elif(parsed[0]=="whoonline"):
	
		index=g.get_player_index(e.peer_id)
		if(index > -1):
		
			yrklol=True
			if(yrklol==True):
			
				s=""
				if get_friend_count(g.players[index].name)==0: g.n.send_reliable(e.peer_id,"No friends online",0); return
				s=str(get_friend_count(g.players[index].name))+" friends online: "
				for i in range(len(g.players)):
					if g.players[i].hidden: continue
					if (g.players[i].name in g.players[index].friendlist and i==len(g.players)-1):
						s+=" "+g.players[i].name+": "
					else:
						if g.players[i].name in g.players[index].friendlist: s+=g.players[i].name+", "
						
					
				g.n.send_reliable(g.players[index].peer_id, s, 0)
				
			
		
	elif(parsed[0]=="accounts"):
	
		index = g.get_player_index(e.peer_id)
		if index > -1:
			for boomb in g.players:

				if boomb.name==g.players[index].name: continue
				if g.players[index].distancecheck(boomb.x,boomb.y,boomb.z)<=30 and boomb.map==g.players[index].map and g.players[index].map!="lobby":
					g.n.send_reliable(g.players[index].peer_id,"You cannot exit while there is a player nearby 30 feet away.",0);
					return


			m=server_menu()
			m.intro="Select an account to login"
			m.initial_packet="accountlogin"
			chars=os.listdir("chars")
			for char in chars:
				charfolder=os.path.join("chars",char)
				if char!=g.players[index].name and file_get_contents(charfolder+"/compid.usr")==g.players[index].compid:
					m.add(char,char); break
			if len(m.menuids)==0: g.n.send_reliable(e.peer_id,"You do not have any other account",0); return
			m.send(e.peer_id)
	elif(parsed[0]=="accountlogin"):
	
		index = g.get_player_index(e.peer_id)
		if index > -1:
			if parsed[1]=="back": return
			for boomb in g.players:

				if boomb.name==g.players[index].name: continue
				if g.players[index].distancecheck(boomb.x,boomb.y,boomb.z)<=30 and boomb.map==g.players[index].map and g.players[index].map!="lobby":
					g.n.send_reliable(g.players[index].peer_id,"You cannot exit while there is a player nearby 30 feet away.",0);
					return


			g.n.send_reliable(e.peer_id,"accountlogin "+parsed[1]+" "+file_get_contents("chars/"+parsed[1]+"/pass.usr")+" "+file_get_contents("chars/"+parsed[1]+"/mail.usr"),0)
	elif(parsed[0]=="whonear"):
	
		index = g.get_player_index(e.peer_id)
		if index > -1:
		
			index = g.players[index]
			if index.jammer: 
				g.n.send_reliable(e.peer_id,"cannot get near player info",0); return

			if index.specplayer != "":
				# Original logic: index = getpc(index.specplayer); if index is None: return
				# Assuming getpc is a defined function that retrieves a player character object.
				spec_player_obj = getpc(index.specplayer) 
				if spec_player_obj is None: return
				index = spec_player_obj
			
			s = ""
			# Define a threshold for vertical difference
			vertical_threshold = 0 

			# --- Process Players ---
			for i in range(len(g.players)):
				current_player = g.players[i] 

				# Basic filtering conditions
				if current_player.map != index.map : continue
				if g.get_hidden_area_at(current_player.x, current_player.y, current_player.z, current_player.map) != g.get_hidden_area_at(index.x, index.y, index.z, index.map) : continue
				if current_player.invisible: continue
				if current_player.hidden: continue
				if current_player.name == index.name: continue
			
				# Proximity check
				dist = 30
				if index.binocularsplayer!="" and index.get_item_count("binoculars")>0: dist=120
				else: dist = 30
				if dist==120 and index.binocularsplayer!="" and current_player.name!=index.binocularsplayer: continue
				if (current_player.x < index.x + dist and current_player.x > index.x - dist and 
					current_player.z < index.z + dist and current_player.z > index.z - dist and 
					current_player.y < index.y + dist and current_player.y > index.y - dist):

					# Determine vertical prefix (uses 'z' for players)
					vertical_prefix_str = "" # Stores "above ", "below ", or ""
					if current_player.z > index.z + vertical_threshold:
						vertical_prefix_str = "above "
					elif current_player.z < index.z - vertical_threshold:
						vertical_prefix_str = "below "

					# Send beep based on game rules (unchanged logic)
					if not current_player.dead:
						if (index.map != "massacre_in_the_city" and (index.matchteam != current_player.matchteam or index.matchteam == "") and current_player.map != "lobby" and not current_player.map.startswith("match")):
							g.n.send_reliable(e.peer_id, "beep " + str(round(current_player.x)) + " " + str(round(current_player.y)) + " " + str(round(current_player.z)) + " " + current_player.map + " 100", 3)
						elif index.map == "massacre_in_the_city":
							if index.group != current_player.group:
								g.n.send_reliable(e.peer_id, "beep " + str(round(current_player.x)) + " " + str(round(current_player.y)) + " " + str(round(current_player.z)) + " " + current_player.map + " 100", 3)
							if index.group == current_player.group:
								g.n.send_reliable(e.peer_id, "beep2 " + str(round(current_player.x)) + " " + str(round(current_player.y)) + " " + str(round(current_player.z)) + " " + current_player.map + " 100", 3)
					
					# Construct distance and direction strings
					distance_str = "(" + str(round(get_3d_distance(current_player.x, current_player.y, current_player.z, index.x, index.y, index.z))) + " feet "
					direction_str = calculate_x_y_string(calculate_x_y_angle(index.x, index.y, current_player.x, current_player.y, index.facing)) + ") " 
					
					# Build description string parts
					desc_parts = []

					if current_player.ducking:
						desc_parts.append("Ducking")

					if current_player.health > 0: # Alive
						if current_player.faint and current_player.zombie:
							desc_parts.append("faint zombie")
						elif current_player.faint:
							desc_parts.append("faint")
						elif current_player.zombie:
							desc_parts.append("zombie")
						
						desc_parts.append(current_player.name)

						if vertical_prefix_str: # If "above " or "below "
							desc_parts.append(vertical_prefix_str.strip()) # Add "above" or "below"
						
						desc_parts.append("with " + str(current_player.health) + " hp")
					
					else: # Dead
						if current_player.zombie:
							desc_parts.append("dead zombie")
							desc_parts.append(current_player.name)
							if vertical_prefix_str:
								desc_parts.append(vertical_prefix_str.strip())
						else: # Not zombie, dead
							desc_parts.append(current_player.name)
							if vertical_prefix_str:
								desc_parts.append(vertical_prefix_str.strip())
							desc_parts.append("dead")
					
					# Join parts and add distance/direction
					main_description = " ".join(desc_parts)
					s_player_entry = main_description + " " + distance_str + direction_str
					s += s_player_entry
			
			# --- Process NPCs ---
			for i in range(len(g.npcs)):
				current_npc = g.npcs[i]

				# Basic filtering conditions
				if index.specplayer==current_npc.name or current_npc.map != index.map: continue
				if g.get_hidden_area_at(current_npc.x, current_npc.y, current_npc.z, current_npc.map) != g.get_hidden_area_at(index.x, index.y, index.z, index.map): continue

				# Proximity check
				if (current_npc.x < index.x + 30 and current_npc.x > index.x - 30 and 
					current_npc.z < index.z + 30 and current_npc.z > index.z - 30 and 
					current_npc.y < index.y + 30 and current_npc.y > index.y - 30):

					# Determine vertical prefix (uses 'y' for NPCs)
					vertical_prefix_str = ""
					if current_npc.y > index.y + vertical_threshold:
						vertical_prefix_str = "above "
					elif current_npc.y < index.y - vertical_threshold:
						vertical_prefix_str = "below "

					# Construct distance and direction strings
					distance_str = "(" + str(round(get_3d_distance(current_npc.x, current_npc.y, current_npc.z, index.x, index.y, index.z))) + " feet "
					direction_str = calculate_x_y_string(calculate_x_y_angle(index.x, index.y, current_npc.x, current_npc.y, index.facing)) + ") " 

					desc_parts = [current_npc.name] # Start with NPC name

					if vertical_prefix_str:
						desc_parts.append(vertical_prefix_str.strip())
					
					if current_npc.health > 0:
						desc_parts.append("with " + str(current_npc.health) + " hp")
					else:
						desc_parts.append("dead")
					
					main_description = " ".join(desc_parts)
					s_npc_entry = main_description + " " + distance_str + direction_str
					s += s_npc_entry
			
			# --- Process Zombies (from g.zombies list) ---
			for i in range(len(g.zombies)):
				current_zombie = g.zombies[i]

				# Basic filtering conditions
				if current_zombie.map != index.map: continue
				# Hidden area check was not present for g.zombies in original, preserving that.

				# Proximity check (20 units for g.zombies)
				if (current_zombie.x < index.x + 20 and current_zombie.x > index.x - 20 and 
					current_zombie.z < index.z + 20 and current_zombie.z > index.z - 20 and 
					current_zombie.y < index.y + 20 and current_zombie.y > index.y - 20):

					# Determine vertical prefix (uses 'y' for g.zombies)
					vertical_prefix_str = ""
					if current_zombie.y > index.y + vertical_threshold:
						vertical_prefix_str = "above "
					elif current_zombie.y < index.y - vertical_threshold:
						vertical_prefix_str = "below "

					# Construct distance and direction strings
					distance_str = "(" + str(round(get_3d_distance(current_zombie.x, current_zombie.y, current_zombie.z, index.x, index.y, index.z))) + " feet "
					direction_str = calculate_x_y_string(calculate_x_y_angle(index.x, index.y, current_zombie.x, current_zombie.y, index.facing)) + ") " 

					desc_parts = []
					if current_zombie.health > 0:
						desc_parts.append("zombie") # Base type
					else:
						desc_parts.append("dead zombie") # Base type

					if vertical_prefix_str:
						desc_parts.append(vertical_prefix_str.strip()) # Add "above" or "below"
					
					base_description = " ".join(desc_parts)

					if current_zombie.health > 0:
						s_zombie_entry = base_description + " with " + str(current_zombie.health) + " hp " + distance_str + direction_str
					else:
						s_zombie_entry = base_description + " " + distance_str + direction_str
					s += s_zombie_entry

			if s == "":
				s = "Nobody near you"
				
			# Remove potential leading/trailing space from the entire accumulated string before sending
			g.n.send_reliable(e.peer_id, s.strip(), 0)
	elif(parsed[0]=="update_zone" and len(parsed)>1) :
		index=g.get_player_index(e.peer_id)
		if(index>-1) :
			g.players[index].zone=string_replace(e.message, parsed[0]+" ","",False)
			
		
	elif(parsed[0]=="move_to" and len(parsed) > 3):
	
		index=g.get_player_index(e.peer_id)
		if(index > -1):
			if getattr(g.players[index], "climbing", False): return
		
			if g.players[index].renaming: remove_from_server(index); return
			if g.players[index].movetimer.elapsed>=0:
				g.players[index].movetimer.restart()
				g.players[index].weapon_rays=None
				g.players[index].weapon_rays2=None
				charname=g.players[index].name
				if g.players[index].in_bus and g.players[index].bus_instance is not None:
					bus = g.players[index].bus_instance
					old_lx = getattr(g.players[index], "local_x", None)
					old_ly = getattr(g.players[index], "local_y", None)
					new_lx = int(float(parsed[1])) - bus.x
					new_ly = int(float(parsed[2])) - bus.y
					new_lz = int(float(parsed[3])) - bus.z
					
					# Cabin block check: if door is closed and player tries to enter cabin
					if not bus.doors_open and ((old_ly == 1 and new_ly >= 2) or (old_ly == 14 and new_ly <= 13)):
						new_ly = old_ly
						g.play("doorhit", bus.x + new_lx, bus.y + new_ly, bus.z + new_lz, bus.map)
						g.n.send_reliable(g.players[index].peer_id, "The door is closed. Press Enter to open it.", 0)
					
					if new_lx < 1: new_lx = 1
					if new_lx > 6: new_lx = 6
					if not bus.doors_open:
						if new_ly < 1: new_ly = 1
						if new_ly > 14: new_ly = 14
					
					g.players[index].local_x = new_lx
					g.players[index].local_y = new_ly
					g.players[index].local_z = new_lz
					g.players[index].x = bus.x + new_lx
					g.players[index].y = bus.y + new_ly
					g.players[index].z = bus.z + new_lz
					
					if old_lx != new_lx or old_ly != new_ly:
						if new_lx in (1, 2, 5, 6) and 2 <= new_ly <= 13:
							g.n.send_reliable(g.players[index].peer_id, "Seat", 0)
				else:
					new_x = float(parsed[1])
					new_y = float(parsed[2])
					new_z = float(parsed[3])
					collided = False
					at_ladder = False
					
					collided_bus = None
					for bus in g.transits:
						if bus.map == g.players[index].map and bus.running:
							# Front-side ladder check (only when bus is stopped)
							if bus.is_stopped and bus.x <= new_x <= bus.x + 9 and new_y == bus.y - 1 and abs(new_z - bus.z) <= 5:
								at_ladder = True
							
							# Solid bounding box collision check
							if bus.x <= new_x <= bus.x + 9 and bus.y <= new_y <= bus.y + 19 and abs(new_z - bus.z) <= 5:
								collided = True
								collided_bus = bus
								break
					
					if collided:
						if collided_bus is not None and collided_bus.is_stopped:
							# Stationary bus: act like a wall. Play soft bump sound once, no pushback.
							last_collision_time = getattr(g.players[index], "last_bus_collision_time", 0.0)
							if tm.time() - last_collision_time >= 1.5:
								g.players[index].last_bus_collision_time = tm.time()
								g.play("wall1", g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].map)
							# Block movement but keep checking ladder
						else:
							# Moving bus: full impact — push player back
							last_collision_time = getattr(g.players[index], "last_bus_collision_time", 0.0)
							if tm.time() - last_collision_time >= 1.0:
								g.players[index].last_bus_collision_time = tm.time()
								g.play("wallcar2", g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].map)
							g.n.send_reliable(g.players[index].peer_id, f"move {g.players[index].x} {g.players[index].y} {g.players[index].z}", 0)
							return
					
					if at_ladder:
						if not getattr(g.players[index], "at_ladder", False):
							g.players[index].at_ladder = True
							g.n.send_reliable(g.players[index].peer_id, "ladder", 0)
					else:
						g.players[index].at_ladder = False
					
					g.players[index].x = new_x
					g.players[index].y = new_y
					g.players[index].z = new_z
				if not g.players[index].hidden:
					for p in g.players:
						if g.get_hidden_area_at(p.x, p.y, p.z, p.map)!=g.get_hidden_area_at(g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].map): continue
						if p.name==g.players[index].name: continue
						if p.specplayer==g.players[index].name or (p.map==g.players[index].map and p.distancecheck(g.players[index].x,g.players[index].y,g.players[index].z)<=30): g.n.send_unreliable(p.peer_id,"update_player " + str(g.players[index].x) + " " + str(g.players[index].y) + " " + str(g.players[index].z) + " " + g.players[index].map+" "+g.players[index].name+" "+str(g.players[index].facing), 20)

				itemloop()
				for mine in g.mines:
					if mine.map==g.players[index].map and mine.x==round(g.players[index].x) and mine.y==round(g.players[index].y) and abs(mine.z - g.players[index].z) <= 5: mine.health=0

	elif(parsed[0]=="move_to_a" and len(parsed) > 3):
	
		index=g.get_player_index(e.peer_id)
		if(index > -1):
			if getattr(g.players[index], "climbing", False): return
		
			if g.players[index].move2timer.elapsed>=0:
				g.players[index].move2timer.restart()
				g.players[index].weapon_rays=None
				g.players[index].weapon_rays2=None

				name=g.players[index].name
				if g.players[index].in_bus and g.players[index].bus_instance is not None:
					bus = g.players[index].bus_instance
					old_lx = getattr(g.players[index], "local_x", None)
					old_ly = getattr(g.players[index], "local_y", None)
					new_lx = int(float(parsed[1])) - bus.x
					new_ly = int(float(parsed[2])) - bus.y
					new_lz = int(float(parsed[3])) - bus.z
					
					# Cabin block check: if door is closed and player tries to enter cabin
					if not bus.doors_open and ((old_ly == 1 and new_ly >= 2) or (old_ly == 14 and new_ly <= 13)):
						new_ly = old_ly
						g.play("doorhit", bus.x + new_lx, bus.y + new_ly, bus.z + new_lz, bus.map)
						g.n.send_reliable(g.players[index].peer_id, "The door is closed. Press Enter to open it.", 0)
					
					if new_lx < 1: new_lx = 1
					if new_lx > 6: new_lx = 6
					if not bus.doors_open:
						if new_ly < 1: new_ly = 1
						if new_ly > 14: new_ly = 14
					
					g.players[index].local_x = new_lx
					g.players[index].local_y = new_ly
					g.players[index].local_z = new_lz
					g.players[index].x = bus.x + new_lx
					g.players[index].y = bus.y + new_ly
					g.players[index].z = bus.z + new_lz
					
					if old_lx != new_lx or old_ly != new_ly:
						if new_lx in (1, 2, 5, 6) and 2 <= new_ly <= 13:
							g.n.send_reliable(g.players[index].peer_id, "Seat", 0)
				else:
					new_x = float(parsed[1])
					new_y = float(parsed[2])
					new_z = float(parsed[3])
					collided = False
					at_ladder = False
					
					collided_bus = None
					for bus in g.transits:
						if bus.map == g.players[index].map and bus.running:
							# Front-side ladder check (only when bus is stopped)
							if bus.is_stopped and bus.x <= new_x <= bus.x + 9 and new_y == bus.y - 1 and abs(new_z - bus.z) <= 5:
								at_ladder = True
							
							# Solid bounding box collision check
							if bus.x <= new_x <= bus.x + 9 and bus.y <= new_y <= bus.y + 19 and abs(new_z - bus.z) <= 5:
								collided = True
								collided_bus = bus
								break
					
					if collided:
						if collided_bus is not None and collided_bus.is_stopped:
							# Stationary bus: act like a wall. Play soft bump sound once, no pushback.
							last_collision_time = getattr(g.players[index], "last_bus_collision_time", 0.0)
							if tm.time() - last_collision_time >= 1.5:
								g.players[index].last_bus_collision_time = tm.time()
								g.play("wall1", g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].map)
							# Block movement but keep checking ladder
						else:
							# Moving bus: full impact — push player back
							last_collision_time = getattr(g.players[index], "last_bus_collision_time", 0.0)
							if tm.time() - last_collision_time >= 1.0:
								g.players[index].last_bus_collision_time = tm.time()
								g.play("wallcar2", g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].map)
							g.n.send_reliable(g.players[index].peer_id, f"move {g.players[index].x} {g.players[index].y} {g.players[index].z}", 0)
							return
					
					if at_ladder:
						if not getattr(g.players[index], "at_ladder", False):
							g.players[index].at_ladder = True
							g.n.send_reliable(g.players[index].peer_id, "ladder", 0)
					else:
						g.players[index].at_ladder = False
					
					g.players[index].x = new_x
					g.players[index].y = new_y
					g.players[index].z = new_z
				if float(parsed[3])!=0 and not g.players[index].hidden:
					for p in g.players:
						if g.get_hidden_area_at(p.x, p.y, p.z, p.map)!=g.get_hidden_area_at(g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].map): continue
						if p.name==g.players[index].name: continue
						if p.specplayer==g.players[index].name or (p.map==g.players[index].map and p.distancecheck(g.players[index].x,g.players[index].y,g.players[index].z)<=30): g.n.send_unreliable(p.peer_id,"update_player " + str(g.players[index].x) + " " + str(g.players[index].y) + " " + str(g.players[index].z) + " " + g.players[index].map+" "+g.players[index].name+" "+str(g.players[index].facing), 20)
				if float(parsed[3])==0 and not g.players[index].hidden:
					for p in g.players:
						if g.get_hidden_area_at(p.x, p.y, p.z, p.map)!=g.get_hidden_area_at(g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].map): continue
						if p.name==g.players[index].name: continue
						if p.specplayer==g.players[index].name or (p.map==g.players[index].map and p.distancecheck(g.players[index].x,g.players[index].y,g.players[index].z)<=30): g.n.send_unreliable(p.peer_id,"update_player2 " + str(g.players[index].x) + " " + str(g.players[index].y) + " " + str(g.players[index].z) + " " + g.players[index].map+" "+g.players[index].name+" "+str(g.players[index].facing), 20)

				itemloop()
			
				for mine in g.mines:
					if mine.map==g.players[index].map and mine.x==round(g.players[index].x) and mine.y==round(g.players[index].y) and abs(mine.z - g.players[index].z) <= 5: mine.health=0


		
	elif(parsed[0]=="move_to_a2" and len(parsed) > 3):
	
		index=g.get_player_index(e.peer_id)
		if(index > -1):
			if getattr(g.players[index], "climbing", False): return
		
			if g.players[index].move3timer.elapsed>=0:
				g.players[index].move3timer.restart()
				name=g.players[index].name
				g.players[index].weapon_rays=None
				g.players[index].weapon_rays2=None

				if g.players[index].in_bus and g.players[index].bus_instance is not None:
					bus = g.players[index].bus_instance
					old_lx = getattr(g.players[index], "local_x", None)
					old_ly = getattr(g.players[index], "local_y", None)
					new_lx = int(float(parsed[1])) - bus.x
					new_ly = int(float(parsed[2])) - bus.y
					new_lz = int(float(parsed[3])) - bus.z
					
					# Cabin block check: if door is closed and player tries to enter cabin
					if not bus.doors_open and ((old_ly == 1 and new_ly >= 2) or (old_ly == 14 and new_ly <= 13)):
						new_ly = old_ly
						g.play("doorhit", bus.x + new_lx, bus.y + new_ly, bus.z + new_lz, bus.map)
						g.n.send_reliable(g.players[index].peer_id, "The door is closed. Press Enter to open it.", 0)
					
					if new_lx < 1: new_lx = 1
					if new_lx > 6: new_lx = 6
					if not bus.doors_open:
						if new_ly < 1: new_ly = 1
						if new_ly > 14: new_ly = 14
					
					g.players[index].local_x = new_lx
					g.players[index].local_y = new_ly
					g.players[index].local_z = new_lz
					g.players[index].x = bus.x + new_lx
					g.players[index].y = bus.y + new_ly
					g.players[index].z = bus.z + new_lz
					
					if old_lx != new_lx or old_ly != new_ly:
						if new_lx in (1, 2, 5, 6) and 2 <= new_ly <= 13:
							g.n.send_reliable(g.players[index].peer_id, "Seat", 0)
				else:
					new_x = float(parsed[1])
					new_y = float(parsed[2])
					new_z = float(parsed[3])
					collided = False
					at_ladder = False
					
					collided_bus = None
					for bus in g.transits:
						if bus.map == g.players[index].map and bus.running:
							# Front-side ladder check (only when bus is stopped)
							if bus.is_stopped and bus.x <= new_x <= bus.x + 9 and new_y == bus.y - 1 and abs(new_z - bus.z) <= 5:
								at_ladder = True
							
							# Solid bounding box collision check
							if bus.x <= new_x <= bus.x + 9 and bus.y <= new_y <= bus.y + 19 and abs(new_z - bus.z) <= 5:
								collided = True
								collided_bus = bus
								break
					
					if collided:
						if collided_bus is not None and collided_bus.is_stopped:
							# Stationary bus: act like a wall. Play soft bump sound once, no pushback.
							last_collision_time = getattr(g.players[index], "last_bus_collision_time", 0.0)
							if tm.time() - last_collision_time >= 1.5:
								g.players[index].last_bus_collision_time = tm.time()
								g.play("wall1", g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].map)
							# Block movement but keep checking ladder
						else:
							# Moving bus: full impact — push player back
							last_collision_time = getattr(g.players[index], "last_bus_collision_time", 0.0)
							if tm.time() - last_collision_time >= 1.0:
								g.players[index].last_bus_collision_time = tm.time()
								g.play("wallcar2", g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].map)
							g.n.send_reliable(g.players[index].peer_id, f"move {g.players[index].x} {g.players[index].y} {g.players[index].z}", 0)
							return
					
					if at_ladder:
						if not getattr(g.players[index], "at_ladder", False):
							g.players[index].at_ladder = True
							g.n.send_reliable(g.players[index].peer_id, "ladder", 0)
					else:
						g.players[index].at_ladder = False
					
					g.players[index].x = new_x
					g.players[index].y = new_y
					g.players[index].z = new_z
				if float(parsed[3])!=0 and not g.players[index].hidden:
					for p in g.players:

						if g.get_hidden_area_at(p.x, p.y, p.z, p.map)!=g.get_hidden_area_at(g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].map): continue
						if p.name==g.players[index].name: continue
						if p.specplayer==g.players[index].name or (p.map==g.players[index].map and p.distancecheck(g.players[index].x,g.players[index].y,g.players[index].z)<=30): g.n.send_unreliable(p.peer_id,"update_player " + str(g.players[index].x) + " " + str(g.players[index].y) + " " + str(g.players[index].z) + " " + g.players[index].map+" "+g.players[index].name+" "+str(g.players[index].facing), 20)
				if float(parsed[3])==0 and not g.players[index].hidden:
					for p in g.players:
						if g.get_hidden_area_at(p.x, p.y, p.z, p.map)!=g.get_hidden_area_at(g.players[index].x, g.players[index].y, g.players[index].z, g.players[index].map): continue
						if p.name==g.players[index].name: continue
						if p.specplayer==g.players[index].name or (p.map==g.players[index].map and p.distancecheck(g.players[index].x,g.players[index].y,g.players[index].z)<=30): g.n.send_unreliable(p.peer_id,"update_player2 " + str(g.players[index].x) + " " + str(g.players[index].y) + " " + str(g.players[index].z) + " " + g.players[index].map+" "+g.players[index].name+" "+str(g.players[index].facing), 20)


				itemloop()
				for mine in g.mines:
					if mine.map==g.players[index].map and mine.x==round(g.players[index].x) and mine.y==round(g.players[index].y) and abs(mine.z - g.players[index].z) <= 5: mine.health=0


			
		

			
		
	
	elif(parsed[0]=="wcoords" and len(parsed) > 3):
	
		index=g.get_player_index(e.peer_id)
		if(index > -1):
		
			if g.players[index].move4timer.elapsed>=0:
				g.players[index].move4timer.restart()
				name=g.players[index].name
				if g.players[index].in_bus and g.players[index].bus_instance is not None:
					bus = g.players[index].bus_instance
					g.players[index].wx = bus.x + g.players[index].local_x
					g.players[index].wy = bus.y + g.players[index].local_y
					g.players[index].wz = bus.z + g.players[index].local_z
				else:
					g.players[index].wx=float(parsed[1])
					g.players[index].wy=float(parsed[2])
					g.players[index].wz=float(parsed[3])
			
		
	return True
