import globals as g
import os
import time
import time as tm
import pickle
import traceback
import json
import datetime
import urllib.parse
import requests
from threading import Thread
from timer import timer
import data_loader

def iositemdo(fn="ioszitemdata.txt"):
	SECONDS_IN_ONE_MONTH = 2592000 

	if not file_exists(fn): return
	f = open(fn, "r")
	data = f.read()
	f.close()

	if data == "":
		return

	d = data.split("\n")
	processed_at_least_one_line = False 

	for line_idx in range(len(d)):
		line_content = d[line_idx]
		if not line_content.strip(): 
			continue

		try:
			parsed = line_content.split("=")
			if len(parsed) < 3:
				continue
		except:
			continue
		
		i, p_name, q_str = parsed[0], parsed[1], parsed[2]
		notify_admins2("zero hour assault, "+p_name+" purchased "+str(q_str)+" "+i+"")
		try:
			q = int(q_str)
			if q <= 0: 
				continue
		except ValueError:
			continue

		player_char_dir = "chars/" + p_name
		if not directory_exists(player_char_dir):
			if "android" not in os.getcwd(): url_post2("https://nbmstudios.com/webfile.php", {"filename": "zitemdata.txt", "nbmcantsend12347665512135699999777777999000990009999987777":"1", "text": ""})
			if "android" in os.getcwd(): url_post2("https://nbmstudios.com/webfile.php", {"filename": "android_zitemdata.txt", "nbmcantsend12347665512135699999777777999000990009999987777":"1", "text": ""})
			file_delete(fn) 
			return 

		index = get_player_index_from(p_name)
		current_time = int(tm.time())
		processed_at_least_one_line = True 

		if i == "paid_account":
			newly_purchased_duration_seconds = SECONDS_IN_ONE_MONTH * q
			current_remaining_duration_seconds = 0.0
			
			if index != -1: 
				player_obj = g.players[index]

				if player_obj.paid and player_obj.paidtime > 0 and player_obj.paidmonths > 0:
					current_subscription_expiry_time = player_obj.paidtime + player_obj.paidmonths
					if current_subscription_expiry_time > current_time:
						current_remaining_duration_seconds = current_subscription_expiry_time - current_time
			else: 
				paid_flag_file = player_char_dir + "/paid.usr"
				paid_time_file = player_char_dir + "/paidtime.usr"
				paid_months_file = player_char_dir + "/paidmonths.usr"

				if file_exists(paid_flag_file):
					try:
						old_paid_start_time = int(file_get_contents(paid_time_file))
						old_paid_duration_seconds = int(file_get_contents(paid_months_file))
						current_subscription_expiry_time = old_paid_start_time + old_paid_duration_seconds
						if current_subscription_expiry_time > current_time:
							current_remaining_duration_seconds = current_subscription_expiry_time - current_time
					except (ValueError, TypeError): 
						current_remaining_duration_seconds = 0.0
			
			final_total_duration_seconds = current_remaining_duration_seconds + newly_purchased_duration_seconds

			if index != -1:
				player_obj = g.players[index]
				player_obj.paid = True
				player_obj.paidtime = current_time
				player_obj.paidmonths = final_total_duration_seconds 

				file_put_contents("chars/" + player_obj.name + "/paid.usr", "")
				file_put_contents("chars/" + player_obj.name + "/paidtime.usr", str(round(current_time)))
				file_put_contents("chars/" + player_obj.name + "/paidmonths.usr", str(final_total_duration_seconds))

				total_months_display = round(final_total_duration_seconds / SECONDS_IN_ONE_MONTH, 1)
				g.n.send_reliable(player_obj.peer_id, f"Your paid account has been updated. It is now active for approximately {total_months_display} months. Thanks for your purchase!", 2)
				g.n.send_reliable(player_obj.peer_id, "play_s misc49.ogg", 0)
			
			else: 
				file_put_contents(player_char_dir + "/paid.usr", "")
				file_put_contents(player_char_dir + "/paidtime.usr", str(round(current_time)))
				file_put_contents(player_char_dir + "/paidmonths.usr", str(final_total_duration_seconds))
		elif i=="backpacks_level2":
			ind=get_player_index_from(p_name)
			if ind>-1:
				g.players[ind].backpacktimer.restart(); g.players[ind].backpacks_level=2
				g.n.send_reliable(g.players[ind].peer_id,"play_s misc49.ogg",0)
				g.n.send_reliable(g.players[ind].peer_id,"you received backpacks level 2, thanks for purchase",2)
			else:
				file_put_contents("chars/"+p_name+"/backpacks_level.usr","2")
				t=timer()
				file_put_contents("chars/"+p_name+"/backpacktimer.usr",pickle.dumps(t),"wb")
		elif i=="backpacks_level3":
			ind=get_player_index_from(p_name)
			if ind>-1:
				g.players[ind].backpacktimer.restart(); g.players[ind].backpacks_level=3
				g.n.send_reliable(g.players[ind].peer_id,"play_s misc49.ogg",0)
				g.n.send_reliable(g.players[ind].peer_id,"you received backpacks level 3, thanks for purchase",2)
			else:
				file_put_contents("chars/"+p_name+"/backpacks_level.usr","3")
				t=timer()
				file_put_contents("chars/"+p_name+"/backpacktimer.usr",pickle.dumps(t),"wb")

		elif i=="event_point":
			ind=get_player_index_from(p_name)
			if ind>-1:
				g.players[ind].eventpoint+=q
				g.n.send_reliable(g.players[ind].peer_id, f"You received {q} {i}, thanks for purchase.", 2)
			else:
				cur=file_get_contents("chars/"+p_name+"/eventpoint.usr")
				if cur=="": cur=0
				else: cur=int(cur)
				cur+=q
				file_put_contents("chars/"+p_name+"/eventpoint.usr",str(cur))
		elif i=="razeon" or i=="shadow" or i=="lord" or i=="hex" or i=="supreme":
			ind=get_player_index_from(p_name)
			if ind>-1:
				g.players[ind].bought_chars.append(i)
				g.n.send_reliable(g.players[ind].peer_id, f"You received the character {i}, thanks for purchase.", 2)
			else:
				cur=pickle.loads(file_get_contents("chars/"+p_name+"/bought_chars.usr","rb"))
				cur.append(i)
				file_put_contents("chars/"+p_name+"/bought_chars.usr",pickle.dumps(cur),"wb")

		else: 
			if index == -1:
				inv_path = player_char_dir + "/storeinventory.usr"
				if i=="KelTecP318": inv_path = player_char_dir + "/inventory.usr"
				inv = {}
				if file_exists(inv_path):
					try:
						inv_data = file_get_contents(inv_path, "rb")
						if inv_data: 
							inv = pickle.loads(inv_data)
					except (pickle.UnpicklingError, EOFError, Exception) as e:
						inv = {}
				
				current_item_quantity = inv.get(i, 0)
				inv[i] = current_item_quantity + q
				file_put_contents(inv_path, pickle.dumps(inv), "wb")
			
			else:
				if i!="KelTecP318": g.players[index].storegive(i, q)
				elif i=="KelTecP318": g.players[index].give(i, q)
				g.n.send_reliable(g.players[index].peer_id, f"You received {q} {i}, thanks for purchase.", 2)
				g.n.send_reliable(g.players[index].peer_id, "play_s misc49.ogg", 0)

	if processed_at_least_one_line:
		if "android" not in os.getcwd(): url_post2("https://nbmstudios.com/webfile.php", {"filename": "zitemdata.txt", "nbmcantsend12347665512135699999777777999000990009999987777":"1", "text": ""})
		if "android" in os.getcwd(): url_post2("https://nbmstudios.com/webfile.php", {"filename": "android_zitemdata.txt", "nbmcantsend12347665512135699999777777999000990009999987777":"1", "text": ""})
		file_delete(fn)


def itemdo(fn="zitemdata.txt"):
	SECONDS_IN_ONE_MONTH = 2592000 

	if not file_exists(fn): return
	f = open(fn, "r")
	data = f.read()
	f.close()

	if data == "":
		return

	d = data.split("\n")
	processed_at_least_one_line = False 

	for line_idx in range(len(d)):
		line_content = d[line_idx]
		if not line_content.strip(): 
			continue

		try:
			parsed = line_content.split("=")
			if len(parsed) < 3:
				continue
		except:
			continue
		
		i, p_name, q_str = parsed[0], parsed[1], parsed[2]
		notify_admins2("zero hour assault, "+p_name+" purchased "+str(q_str)+" "+i+"")
		try:
			q = int(q_str)
			if q <= 0: 
				continue
		except ValueError:
			continue

		player_char_dir = "chars/" + p_name
		if not directory_exists(player_char_dir):
			if "android" not in os.getcwd(): url_post2("https://nbmstudios.com/webfile.php", {"filename": "zitemdata.txt", "nbmcantsend12347665512135699999777777999000990009999987777":"1", "text": ""})
			if "android" in os.getcwd(): url_post2("https://nbmstudios.com/webfile.php", {"filename": "android_zitemdata.txt", "nbmcantsend12347665512135699999777777999000990009999987777":"1", "text": ""})
			file_delete(fn) 
			return 

		index = get_player_index_from(p_name)
		current_time = int(tm.time())
		processed_at_least_one_line = True 

		if i == "paid_account":
			newly_purchased_duration_seconds = SECONDS_IN_ONE_MONTH * q
			current_remaining_duration_seconds = 0.0
			
			if index != -1: 
				player_obj = g.players[index]

				if player_obj.paid and player_obj.paidtime > 0 and player_obj.paidmonths > 0:
					current_subscription_expiry_time = player_obj.paidtime + player_obj.paidmonths
					if current_subscription_expiry_time > current_time:
						current_remaining_duration_seconds = current_subscription_expiry_time - current_time
			else: 
				paid_flag_file = player_char_dir + "/paid.usr"
				paid_time_file = player_char_dir + "/paidtime.usr"
				paid_months_file = player_char_dir + "/paidmonths.usr"

				if file_exists(paid_flag_file):
					try:
						old_paid_start_time = int(file_get_contents(paid_time_file))
						old_paid_duration_seconds = int(file_get_contents(paid_months_file))
						current_subscription_expiry_time = old_paid_start_time + old_paid_duration_seconds
						if current_subscription_expiry_time > current_time:
							current_remaining_duration_seconds = current_subscription_expiry_time - current_time
					except (ValueError, TypeError): 
						current_remaining_duration_seconds = 0.0
			
			final_total_duration_seconds = current_remaining_duration_seconds + newly_purchased_duration_seconds

			if index != -1:
				player_obj = g.players[index]
				player_obj.paid = True
				player_obj.paidtime = current_time
				player_obj.paidmonths = final_total_duration_seconds 

				file_put_contents("chars/" + player_obj.name + "/paid.usr", "")
				file_put_contents("chars/" + player_obj.name + "/paidtime.usr", str(round(current_time)))
				file_put_contents("chars/" + player_obj.name + "/paidmonths.usr", str(final_total_duration_seconds))

				total_months_display = round(final_total_duration_seconds / SECONDS_IN_ONE_MONTH, 1)
				g.n.send_reliable(player_obj.peer_id, f"Your paid account has been updated. It is now active for approximately {total_months_display} months. Thanks for your purchase!", 2)
				g.n.send_reliable(player_obj.peer_id, "play_s misc49.ogg", 0)
			
			else: 
				file_put_contents(player_char_dir + "/paid.usr", "")
				file_put_contents(player_char_dir + "/paidtime.usr", str(round(current_time)))
				file_put_contents(player_char_dir + "/paidmonths.usr", str(final_total_duration_seconds))
		elif i=="backpacks_level2":
			ind=get_player_index_from(p_name)
			if ind>-1:
				g.players[ind].backpacktimer.restart(); g.players[ind].backpacks_level=2
				g.n.send_reliable(g.players[ind].peer_id,"play_s misc49.ogg",0)
				g.n.send_reliable(g.players[ind].peer_id,"you received backpacks level 2, thanks for purchase",2)
			else:
				file_put_contents("chars/"+p_name+"/backpacks_level.usr","2")
				t=timer()
				file_put_contents("chars/"+p_name+"/backpacktimer.usr",pickle.dumps(t),"wb")
		elif i=="backpacks_level3":
			ind=get_player_index_from(p_name)
			if ind>-1:
				g.players[ind].backpacktimer.restart(); g.players[ind].backpacks_level=3
				g.n.send_reliable(g.players[ind].peer_id,"play_s misc49.ogg",0)
				g.n.send_reliable(g.players[ind].peer_id,"you received backpacks level 3, thanks for purchase",2)
			else:
				file_put_contents("chars/"+p_name+"/backpacks_level.usr","3")
				t=timer()
				file_put_contents("chars/"+p_name+"/backpacktimer.usr",pickle.dumps(t),"wb")

		elif i=="event_point":
			ind=get_player_index_from(p_name)
			if ind>-1:
				g.players[ind].eventpoint+=q
				g.n.send_reliable(g.players[ind].peer_id, f"You received {q} {i}, thanks for purchase.", 2)
			else:
				cur=file_get_contents("chars/"+p_name+"/eventpoint.usr")
				if cur=="": cur=0
				else: cur=int(cur)
				cur+=q
				file_put_contents("chars/"+p_name+"/eventpoint.usr",str(cur))
		elif i=="razeon" or i=="shadow" or i=="lord" or i=="hex" or i=="supreme":
			ind=get_player_index_from(p_name)
			if ind>-1:
				g.players[ind].bought_chars.append(i)
				g.n.send_reliable(g.players[ind].peer_id, f"You received the character {i}, thanks for purchase.", 2)
			else:
				cur=pickle.loads(file_get_contents("chars/"+p_name+"/bought_chars.usr","rb"))
				cur.append(i)
				file_put_contents("chars/"+p_name+"/bought_chars.usr",pickle.dumps(cur),"wb")

		else: 
			if index == -1:
				inv_path = player_char_dir + "/storeinventory.usr"
				if i=="KelTecP318": inv_path = player_char_dir + "/inventory.usr"
				inv = {}
				if file_exists(inv_path):
					try:
						inv_data = file_get_contents(inv_path, "rb")
						if inv_data: 
							inv = pickle.loads(inv_data)
					except (pickle.UnpicklingError, EOFError, Exception) as e:
						inv = {}
				
				current_item_quantity = inv.get(i, 0)
				inv[i] = current_item_quantity + q
				file_put_contents(inv_path, pickle.dumps(inv), "wb")
			
			else:
				if i!="KelTecP318": g.players[index].storegive(i, q)
				elif i=="KelTecP318": g.players[index].give(i, q)
				g.n.send_reliable(g.players[index].peer_id, f"You received {q} {i}, thanks for purchase.", 2)
				g.n.send_reliable(g.players[index].peer_id, "play_s misc49.ogg", 0)

	if processed_at_least_one_line:
		if "android" not in os.getcwd(): url_post2("https://nbmstudios.com/webfile.php", {"filename": "zitemdata.txt", "nbmcantsend12347665512135699999777777999000990009999987777":"1", "text": ""})
		if "android" in os.getcwd(): url_post2("https://nbmstudios.com/webfile.php", {"filename": "android_zitemdata.txt", "nbmcantsend12347665512135699999777777999000990009999987777":"1", "text": ""})
		file_delete(fn)


def main():
	global languages, store_data, event_store_data
	import os
	import db as _db
	server_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
	os.chdir(server_dir)
	if not os.path.exists("chars"):
		os.makedirs("chars")

	# ── Read server.conf and init DB first — everything below may touch SQLite ──
	port = 10000 if "android" not in os.getcwd() else 10001
	db_path = "zha_players.db"
	dashboard_port = 8080
	dashboard_password = "changeme"
	dashboard_api_key = ""
	motd_file = "motd.txt"
	if os.path.exists("server.conf"):
		try:
			with open("server.conf", "r") as f:
				for line in f:
					clean_line = line.strip()
					if not clean_line or clean_line.startswith("#") or clean_line.startswith(";"):
						continue
					if "=" in clean_line:
						k, v = clean_line.split("=", 1)
						key = k.strip().lower()
						val = v.strip()
						if key == "port":
							port = int(val)
						elif key == "db_path":
							db_path = val
						elif key == "dashboard_port":
							dashboard_port = int(val)
						elif key == "dashboard_password":
							dashboard_password = val
						elif key == "dashboard_api_key":
							dashboard_api_key = val
						elif key == "motd_file":
							motd_file = val
		except Exception as ex:
			print(f"[!] Error reading server.conf: {ex}")

	_db.init_db(db_path)

	# ── Load game-world state from DB (load functions handle "no data" safely) ──
	load_matches()
	load_chests()
	load_electrics()
	load_corpses()
	load_groups()
	load_communitys()
	load_group_bases()
	load_tickets()
	load_votes()
	load_barricades()
	load_ladders()
	load_rain()
	load_mines()
	load_bikes()
	load_timebombs()
	load_zks()
	load_npcs()
	load_timeditems()
	load_zombies()
	load_items()
	load_flags()

	data = _db.sv_read("language_data.dat")
	if data:
		languages.clear()
		languages.update(pickle.loads(data))
	if os.path.isdir("lang"):
		for fname in os.listdir("lang"):
			if fname.endswith(".lng"):
				lang_name = fname[:-4]
				if lang_name and lang_name not in languages:
					languages[lang_name] = {
						"owner": "Server",
						"official": False,
						"released": True,
						"contributors": []
					}
	for lang in languages.keys():
		if "official" not in languages[lang].keys(): languages[lang]["official"]=languages[lang]["released"]
	store_data.clear()
	store_data.extend(load_store_data())
	event_store_data.clear()
	event_store_data.extend(load_event_store_data())
	init_mapsystem()
	load_compids()

	load_bans()
	load_mailbans()
	load_tempmail_domains()
	if not _db.sv_exists("motd.txt"):
		_db.sv_write_text("motd.txt", "")
	setupserver()

	# Start admin dashboard
	try:
		import sys as _sys, os as _os
		_dashboard_dir = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "..", "dashboard"))
		if _dashboard_dir not in _sys.path:
			_sys.path.insert(0, _os.path.dirname(_dashboard_dir))
		import data_loader as _dl
		from dashboard.app import start_dashboard
		import globals as _g_ref
		start_dashboard(_g_ref, _db, _dl, password=dashboard_password, port=dashboard_port,
		                api_key=dashboard_api_key, motd_file=motd_file)
	except Exception as _dash_ex:
		print(f"[!] Dashboard failed to start: {_dash_ex}")

	print("=" * 65)
	print("                    ZERO HOUR ASSAULT GAME SERVER")
	print("=" * 65)
	print("[*] Initializing server systems...")
	print("[*] Loaded maps system.")
	print("[*] Loaded computer bans & tempmail lists.")
	print("[*] Compiled weapon statistics configuration.")
	print(f"[*] Binding WebSocket server to port {port}...")
	
	g.n.setup_server(port, 100, 100)
	
	print(f"[OK] Server successfully bound to port: {port}")
	print("[*] Network interface: 0.0.0.0 (All incoming connections allowed)")
	print("=" * 65)
	print("STATUS: [RUNNING] Listening for secure WebSocket (TCP) incoming connections...")
	print("Press Ctrl+C to terminate the server at any time.")
	print("=" * 65)

	for base in g.group_bases:
		if not chest_at(20, 25, 0, "basement"+base.name+base.mapappend):
			spawn_chest(20,25,0,"basement"+base.name+base.mapappend)
	perf_monitor = PerformanceMonitor()
	print("[*] Performance logs: logs/performance.log")
	print("[*] Transit logs: logs/transit.log")
	while(True):
		loop_started = tm.perf_counter()
		time.sleep(0.001)
		try:
			net_started = tm.perf_counter()
			netloop()
			net_elapsed_ms = (tm.perf_counter() - net_started) * 1000.0

			game_started = tm.perf_counter()
			gameloops()
			game_elapsed_ms = (tm.perf_counter() - game_started) * 1000.0
			if g.ttchecktimer.elapsed>1000 and file_exists("gift.txt"):
				g.ttchecktimer.restart()
				user=file_get_contents("gift.txt")
				file_delete("gift.txt")
				index=get_player_index_from(user)
				if index>-1:
					gifts=["zero_token","event_point"]
					chosengift=choice(gifts)
					if chosengift=="token": g.players[index].zhtoken+=10;
					if chosengift=="event_point": g.players[index].eventpoint+=10;

					g.n.send_reliable(g.players[index].peer_id,"You received 10 "+chosengift+" because you are active on our team talk server.",2)
					g.n.send_reliable(g.players[index].peer_id,"play_s sound_notif2-132674.ogg",0)
					adminsend(""+g.players[index].name+" got 10 "+chosengift+" gift from team talk event!");
			if paymentchecktimer.elapsed>0:
				itemdo()
				iositemdo()
				paymentchecktimer.restart()
			if g.rebooting==True and g.reboottimer.elapsed>=g.rebootputtime*1000:
				g.reboottimer.restart()
				g.rebooting=False

				for i in range(len(g.players)):
					save_char(i)
				g.n.broadcast("reboot_server",0)
				g.reboot2timer.restart()
				g.reboot2=True
			if g.reboot2==True and g.reboot2timer.elapsed>=500:
				g.reboot2timer.restart()
				g.reboot2=False

				subprocess.Popen(["python3", "zhaserver.py"])
				exit()
			perf_monitor.sample((tm.perf_counter() - loop_started) * 1000.0, net_elapsed_ms, game_elapsed_ms, g)
		except SystemExit:
			os._exit(0)

		except:
			error = traceback.format_exc()
			print(error)
			developersend(error)


def gameloops(match_loop=True,npc_loop=True):
	global survivestage
#	time.sleep(0.0001)
	if g.task==0 and g.freedomsurvivor!="" and survivetimer.elapsed>60000:
		survivetimer.restart()
		survivestage+=1
		for p in g.players:
			if p.map=="massacre_in_the_city":
				try: fi=g.players[get_player_index_from(g.freedomsurvivor)]
				except: return
				g.n.send_reliable(p.peer_id,"play_s teammessage.ogg",0)
				if survivestage!=10: g.n.send_reliable(p.peer_id,"Freedom map selected Player Info: Name: "+fi.name+". Coordinates: "+str(round(fi.x))+", "+str(round(fi.y))+", "+str(round(fi.z))+", time left: "+str((10-survivestage))+" minutes",2)
		if survivestage==10:
			try: fi=g.players[get_player_index_from(g.freedomsurvivor)]
			except: return
			if fi.task_data[0]<5: g.n.send_reliable(fi.peer_id,"You survived for 10 minutes, and you got 10 event points",2)
			for p in g.players:
				if p.map=="massacre_in_the_city":

					g.n.send_reliable(p.peer_id,"play_s teammessage.ogg",0)
					g.n.send_reliable(p.peer_id,fi.name+" successfully survived for 10 minutes! they got 10 event points, and another player will be selected.",2)

			if fi.task_data[0]<5: fi.eventpoint+=10; fi.task_data[0]+=1
			g.freedomsurvivor=""
	if g.task==-1 or tasktimer.elapsed>86400000:
		tasktimer.restart()
		oldtask=get_task_name()
		g.task+=1
		if g.task>3: g.task=0
		for pl in g.players:
			if pl.eventalerts==1:
				g.n.send_reliable(pl.peer_id,"play_s misc251.ogg",0)
				g.n.send_reliable(pl.peer_id,"The event "+oldtask+" has been finished. The new event is "+get_task_name(),2)
		if os.path.exists("chars"):
			for char in find_directories("chars"):
				charfolder=os.path.join("chars",char)
				file_delete(charfolder+"/currenteventpoint.usr")
				file_delete(charfolder+"/task_data.usr")
		for p in g.players:
			p.task_data[0]=0
			p.task_data[1]=0
			p.task_data[2]=0
			p.task_data[3]=0
			p.currenteventpoint=0
	if g.task==0 and freedomchecktimer.elapsed>1000:
		freedomchecktimer.restart()
		if g.freedomsurvivor=="" and select_random_player_from_freedom_fight_map()!="":
			g.freedomsurvivor=select_random_player_from_freedom_fight_map()
			while g.freedomsurvivor==g.last_random_player_chosen: 			g.freedomsurvivor=select_random_player_from_freedom_fight_map()
			g.last_random_player_chosen=g.freedomsurvivor
			survivetimer.restart()
			survivor=g.players[get_player_index_from(g.freedomsurvivor)]
			survivestage=0
			for p in g.players:
				if p.map=="massacre_in_the_city":
					g.n.send_reliable(p.peer_id,"the player selected which should survive for 10 minutes is "+g.freedomsurvivor+", coordinates are "+str(round(survivor.x))+" "+str(round(survivor.y))+" "+str(round(survivor.z)),2)
					g.n.send_reliable(p.peer_id,"play_s teammessage.ogg",0)
		else:
			ind=get_player_index_from(g.freedomsurvivor)
			if ind==-1 and g.freedomsurvivor!="":
				for p in g.players:
					if p.map=="massacre_in_the_city":
						g.n.send_reliable(p.peer_id,"the player selected went offline, a new one will be selected.",2); g.freedomsurvivor=""
			elif ind!=-1 and g.players[ind].hidden:
				for p in g.players:
					if p.map=="massacre_in_the_city":
						g.n.send_reliable(p.peer_id,"the player selected went offline, a new one will be selected.",2); g.freedomsurvivor=""
			elif ind!=-1 and g.players[ind].map!="massacre_in_the_city":
				for p in g.players:
					if p.map=="massacre_in_the_city":
						g.n.send_reliable(p.peer_id,"the player selected left the map, a new one will be selected.",2); g.freedomsurvivor=""

	if g.rain and g.rainvoltimer.elapsed>g.rainvoltime:
		g.rainvoltimer.restart()
		v=random(1,7)
		if v==1: g.rainvolume=-10
		if v==2: g.rainvolume=-15
		if v==3: g.rainvolume=-22
		if v==4: g.rainvolume=-25
		if v==5: g.rainvolume=-35
		if v==6: g.rainvolume=-40
		if v==7: g.rainvolume=-45

		g.rainvoltime=random(15000, 30000)
	if not g.rain and g.rainstarttimer.elapsed>g.rainstarttime:
		g.rainstarttimer.restart()
		g.raintimer.restart()
		g.rain=True
	if g.rain and g.raintimer.elapsed>g.raintime:
		g.rain=False
		g.rainstarttime=random(2000000, 4000000)
		g.raintime=random(200000, 300000)

		g.rainstarttimer.restart()
		g.raintimer.restart()
		g.rainfinish=True
		g.rainfinishtimer.restart()
	if g.rainfinish and g.rainfinishtimer.elapsed>60000:
		g.rainfinish=False
	if backuptimer.elapsed>36000000:
		backuptimer.restart()
		Thread(target=backup).start()
	if chesttimer.elapsed>60000:
		chesttimer.restart()
		chestitemlist = data_loader.get_chest_pool()
		chest_cfg = data_loader.get_chest_config()
		chest_min = chest_cfg.get("items_per_chest_min", 3)
		chest_max = chest_cfg.get("items_per_chest_max", 10)
#		if not chest_at(0, 0, 0, "massacre_in_the_city"):
#			spawn_chest(0,0,0,"massacre_in_the_city")
#			chest=g.chests[len(g.chests)-1]
#		else:
#			chest=get_chest_at(0,0,0,"massacre_in_the_city")
		for map in g.maps:
			for mapchest in map.mapchests:
				if not chest_at(mapchest.x, mapchest.y, mapchest.z, map.name):
					spawn_chest(mapchest.x, mapchest.y, mapchest.z, map.name)
					chest = g.chests[len(g.chests) - 1]
				else:
					chest = get_chest_at(mapchest.x, mapchest.y, mapchest.z, map.name)
				if len(chest.items)==0 or chest.fill:
					chest.fill=False
					for i in range(random(chest_min, chest_max)-len(chest.items)):
						item=choice(list(chestitemlist.keys()))
						while item in chest.items:
							item=choice(list(chestitemlist.keys()))
						amount=random(1,chestitemlist[item])
						chest.items.append(item)
						chest.itemamounts.append(amount)

	if duplicatewalltimer.elapsed>5000:
		duplicatewalltimer.restart()
		ticketcheck()
		votecheck()
		if 1:
			if 1:
				try: current_time=datetime.now()
				except: current_time=datetime.datetime.now()
				TIME_HOUR=current_time.hour
				TIME_MINUTE=current_time.minute
				TIME_SECOND=current_time.second
				if TIME_HOUR==23 and TIME_MINUTE==0 and TIME_SECOND<=10:
					for _row in _db.get_all_players():
						_db.chardelete(_row["name"], "mailsent")
						_db.chardelete(_row["name"], "todaygift")

		if 1:
			for m in g.maps:
				remove_duplicate_mapwalls(m.mapwalls)
				for wall in m.mapwalls:
					if wall.health<=0 and wall.destroyed==False:
						wall.destroyed=True
						targetmap=m.name
						file_put_contents("maps/"+targetmap+".map",file_get_contents("maps/"+targetmap+".map").replace("platform:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type),""))
						update_map(targetmap)
	if npc_loop: npcloop()
	megabossloop()
	spawnerloop()

	if len(g.zombies)>0: zombieloop()
	timebombloop()
	zkloop()
	mineloop()
	group_baseloop()
	if len(g.weapons)>0:
		if g.weaponlaslslaltimer.elapsed>=5:
			g.weaponlaslslaltimer.restart()
			molotofloop()
			weaponloop()
	#mwallloop()
	if itembeeptimer.elapsed>1500:
		itembeeploop()
		itembeeptimer.restart()

	#compbanloop()
	timeditemloop()
#	motorloop()
	bikeloop()
	if hasattr(g, "busloop"): g.busloop()
	molotofloop()
	if len(g.bodyfalls)>0: bodyfallloop()
	if len(g.grenades)>0: grenadeloop()
	if g.playertimer.elapsed>15:
		g.playertimer.restart()
		playerloop()
	if g.chestlolololtimer.elapsed>=10:
		g.chestlolololtimer.restart()
		chestloop()
#	electricloop()
#	timed_electricloop()
	corpseloop()
	if len(g.loots)>0: lootloop()
	if len(g.flags)>0: flagloop()
	if match_loop:
		if len(g.matches)>0: matchloop()

	if g.lolsavetimer.elapsed>=90000:
		g.lolsavetimer.restart()
#		garbage_collect()
		save_all_chars()
		_db.sv_write("language_data.dat", pickle.dumps(languages))


def garbage_collect():
	gc.collect()


def exit():
	os._exit(0)


def backup():
    if 1:
        #Create 'backups' directory if it doesn't exist
        backup_dir = 'backups'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
#        
        # Create a timestamped directory inside 'backups'
        timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        timestamped_dir = os.path.join(backup_dir, timestamp)
        os.makedirs(timestamped_dir)

        # List of files and directories to backup
        items_to_backup = [
            'chars',
            'lang',
            'maps',
            'adminhelp.txt',
            'moderatorhelp.txt',
            'ladders.dat',
            'barricades.dat',

            'builderhelp.txt',
            'suggest.txt',
            'timeditems.dat',
            'tickets.dat',
            'votes.dat',
            'chests.dat',
            'corpses.dat',
            'chesttimer.txt',
            'tasktimer.txt',
            'groups.dat',
            'communitys.dat',

            'group_bases.dat',
            'language_data.dat',
            'mines.dat',
            'timebombs.dat',
            'zks.dat',

            'compbans.svr',
            'languages.txt',
            'changes.txt'

        ]

        # Copy files and directories
        for item in items_to_backup:
            source_path = os.path.join(os.getcwd(), item)
            destination_path = os.path.join(timestamped_dir, item)
#            
            if os.path.isdir(source_path):
                shutil.copytree(source_path, destination_path)
            elif os.path.isfile(source_path):
                shutil.copy2(source_path, destination_path)


def backup():
    """
    Belirtilen dosya ve klasörleri 'backups' dizini içinde
    zaman damgalı tek bir ZIP arşivine yedekler.
    """
    try:
        # 'backups' klasörünün var olduğundan emin ol
        backup_dir = 'backups'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # ZIP dosyası için zaman damgalı bir isim oluştur
        timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        zip_filename = os.path.join(backup_dir, f"{timestamp}.zip")

        # Yedeklenecek dosya ve klasörlerin listesi
        items_to_backup = [
            'chars',
            'lang',
            'maps',
            'adminhelp.txt',
            'moderatorhelp.txt',
            'ladders.dat',
            'barricades.dat',
            'builderhelp.txt',
            'suggest.txt',
            'timeditems.dat',
            'tickets.dat',
            'votes.dat',
            'chests.dat',
            'corpses.dat',
            'chesttimer.txt',
            'tasktimer.txt',
            'groups.dat',
            'communitys.dat',
            'group_bases.dat',
            'language_data.dat',
            'mines.dat',
            'timebombs.dat',
            'zks.dat',
            'compbans.svr',
            'languages.txt',
            'changes.txt'
        ]

        # Yeni bir ZIP dosyası oluştur ve listelenen öğeleri içine ekle
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for item in items_to_backup:
                source_path = os.path.join(os.getcwd(), item)
                
                # Eğer yedeklenecek öğe mevcut değilse atla
                if not os.path.exists(source_path):
                    continue
                
                if os.path.isdir(source_path):
                    # Klasör ise, içindeki tüm dosyaları yürü ve ZIP'e ekle
                    for root, dirs, files in os.walk(source_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            # Dosyanın ZIP içindeki yolu, ana dizine göre ayarlanır
                            arcname = os.path.relpath(file_path, os.getcwd())
                            zipf.write(file_path, arcname)
                elif os.path.isfile(source_path):
                    # Dosya ise, doğrudan ZIP'in kök dizinine ekle
                    arcname = os.path.basename(source_path)
                    zipf.write(source_path, arcname)

    except Exception as e:
        # Hata durumunda (orijinal koddaki gibi geniş kapsamlı) işlemi sessizce sonlandır
        # Gerçek bir uygulamada burada hatayı loglamak daha iyi olurdu.
        # print(f"Yedekleme sırasında bir hata oluştu: {e}")
        pass


def netloop():
    global languages, e
    try:
        e = g.n.request()
        g.e = e
    except:
        return
    if e.type == event_disconnect:
        px = g.get_player_index(e.peer_id)
        if px > -1:
            remove_from_server(px)
    if e.type == event_receive:
        if e.channel == 1:
            import zh_net_chat
            zh_net_chat.handle_channel_1(e)
        elif e.channel == 0:
            import zh_net_gameplay_1, zh_net_gameplay_2, zh_net_gameplay_3, zh_net_gameplay_4, zh_net_gameplay_5, zh_net_gameplay_6
            parsed = string_split(e.message, ' ', True)
            index = g.get_player_index(e.peer_id)
            if index > -1 or (len(parsed) > 0 and parsed[0] in ("login", "create", "pr", "verifycode", "sendverify", "spawn_player")):
                if zh_net_gameplay_1.handle_gameplay_1(e, parsed, index): return
                if zh_net_gameplay_2.handle_gameplay_2(e, parsed, index): return
                if zh_net_gameplay_3.handle_gameplay_3(e, parsed, index): return
                if zh_net_gameplay_4.handle_gameplay_4(e, parsed, index): return
                if zh_net_gameplay_5.handle_gameplay_5(e, parsed, index): return
                if zh_net_gameplay_6.handle_gameplay_6(e, parsed, index): return
        elif e.channel in (2, 5, 6):
            import zh_net_others
            zh_net_others.handle_channel_others(e)

