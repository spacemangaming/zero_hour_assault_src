import json # Import json for storing comments

import importlib
import zhaserver
import os
import time as tm
charlist=["aria","kade","razeon","shadow","hex","supreme","lord"]
from timer import timer
from variable_management import string_contains
import time
import pickle
languages={}
from guns import guns,guns2
from npc import npcloop
from zombie import zombieloop
import gc

from internet import url_post
from file_directories import file_put_contents
from npc import npc
from compban import comp_ban, comp_unban, load_bans, compbanloop, get_compban_reason, get_compban_end_time, get_playerban_end_time, get_compid_from_player, save_bans, get_comp_bans, get_player_from_compid
from rotation import calculate_x_y_string, getdir, north, northeast, east, southeast, south, southwest, west, northwest
from match import newmatch2, newmatch, delay, chestloop, spawn_chest, corpseloop, spawn_corpse, electricloop, timed_electricloop
from moving_sound_serverside_handler import spawn_moving_sound, update_moving_sound, destroy_moving_sound
from rotation import calculate_x_y_angle
import traceback
from player import spawn_player
from compid_handler import load_compids, compid_handlercheck, add_compid
from compban import is_compbanned
from match import matchloop
from map import get_tile_at, mwallloop



from file_directories import file_exists

from map import get_map_index

from file_directories import directory_create, directory_delete
from file_directories import directory_exists, directory_exists2

from npc import usernames
from network import event_receive
from network import event_disconnect

from weapon import weaponloop, get_weapon_range, get_weapon_spread, get_mindamage, get_maxdamage
from molotof import spawn_molotof, molotofloop
from bodyfall import bodyfallloop

from variable_management import string_left
from variable_management import string_split
from variable_management import string_to_lower_case, string_to_number
from variable_management import string_replace
from file_directories import find_files
from file_directories import find_directories
from map import init_mapsystem
from network import network, network_event
import globals as g
from file_directories import file_delete
from random import randint as random
from rotation import get_3d_distance
import subprocess
from weapon import spawn_weapon
from map import delinear
from map import linear

import sys
from player import playerloop



from item import itemloop, itembeeploop
from loot import lootloop
from flag import flagloop, spawn_flag
from item import spawn_item
class server_menu:
	def __init__(self):
		self.menuitems=my_list()
		self.menuids=my_list()
		self.menuacts=my_list()
		self.initial_packet=""
		self.store=False
		self.paid_store=False
		self.intro=""
	def add(self, item, id, act=True):
		self.menuitems.append(item)
		self.menuids.append(id)
		self.menuacts.append(act)
	def reset(self):
		self.menuids=my_list()
		self.menuitems=my_list()

	def send(self, id):
		if len(self.menuids)>0 and len(self.menuitems)>0:
			l=""
			for i in range(len(self.menuitems)):
				l+=str(self.menuitems[i])+"<"+str(self.menuids[i])+"<"+str(self.menuacts[i])+"\t"
			index=get_player_index(id)
			if index>-1:
				g.players[index].menuitems=self.menuitems
				g.players[index].menuids=self.menuids
				g.players[index].menuacts=self.menuacts
				g.players[index].initial_packet=self.initial_packet
			send_menu(id, self.intro, self.initial_packet, l, self.store)
g.server_menu=server_menu
def find_directories(path):
	l=my_list()
	for each in os.listdir(path):
		if os.path.isdir(path+"/"+each):
			l.append(each)
	return l

def send_menu(id, menuintro, text, items, store=False):
	menuintro=string_replace(menuintro, " ", "[SPCE]", True)
	text=string_replace(text, " ", "[SPCE", True)
	g.n.send_reliable(id, "launchmenu "+menuintro+" "+text+" "+items+"", 0)
import datetime
from timeditem import timeditemloop
from motor import motorloop, add_motor, send_platform, remove_platform
from group import create_group, rename_group
from community import create_community, rename_community

from base import create_group_base, group_baseloop
import copy
from grenade import launch_grenade, grenadeloop
from zk import place_zk
from timebomb import timebombloop
from zk import zkloop

from mine import mineloop
invweapons="mkek_jng90 dragunov_psl mkek_mpt76k m4 mkek_yavuz16 gsg5 colt1911 IthicaM37 wooden_sword stone_sword diamond_sword fnhfnp40 fnhfnp45 MosinNagant maverick88 S&WModel66 knife berettaM9 KelTecP318"
invdrinks="vitality_potion revival_nectar small_potion"
invexplosives="hand_grenade molotov_cocktail snowflake_shard timebomb tm62 zk91"
invequipment="parachute binoculars base_life_amplifier metal_shield ladder fire_suppressant barricade invisibility_shield steel_helmet silencer"
invammos="7.62x51mm 5.56x45mm dragunov_psl_ammo_cartrigges gsg5_ammo_cartrigges 357_magnum 9mm 45_ACP 12_gauge 40S&W 22_LR_Long_Rifle m4_ammo_cartrigges colt1911_ammo_cartrigges fnhfnp40_ammo_cartrigges 7.62x54mmR"
from threading import Thread
from vector import vector
paymentchecktimer=timer()
import time 
import pickle 
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
chesttimer=timer()
tasktimer=timer()
from random import choice
itembeeptimer=timer()
backuptimer=timer()
from rotation import move
pistols=["colt1911","S&WModel66","mkek_yavuz16","fnhfnp40","fnhfnp45","berettaM9","KelTecP318"]
snipers=["dragunov_psl","mkek_jng90","gsg5","maverick88","MosinNagant"]
machineguns=["m4","mkek_mpt76k"]
survivetimer=timer()
survivestage=0
freedomchecktimer=timer()
from bike import bikeloop, bike
from molotof import molotofloop
def main():
	global languages, store_data, event_store_data
	if file_exists("matches.dat"): load_matches()
	if file_exists("chests.dat"): load_chests()
	if file_exists("electrics.dat"): load_electrics()
	if file_exists("corpses.dat"): load_corpses()

	if file_exists("groups.dat"): load_groups()
	if file_exists("communitys.dat"): load_communitys()

	if file_exists("group_bases.dat"): load_group_bases()

	if file_exists("tickets.dat"): load_tickets()
	if file_exists("votes.dat"): load_votes()
	if file_exists("barricades.dat"): load_barricades()
	if file_exists("ladders.dat"): load_ladders()
	if file_exists("rain.dat"): load_rain()
	if file_exists("mines.dat"): load_mines()
	if file_exists("bikes.dat"): load_bikes()
	if file_exists("timebombs.dat"): load_timebombs()
	if file_exists("zks.dat"): load_zks()

	"""
	try:
		if file_exists("motors.dat"): load_motors()
	except: pass
"""
	if file_exists("npcs.dat"): load_npcs()
	if file_exists("timeditems.dat"): load_timeditems()
	if file_exists("zombies.dat"): load_zombies()
	if file_exists("items.dat"): load_items()
	if file_exists("flags.dat"): load_flags()
	if file_exists("language_data.dat"):
		f=open("language_data.dat","rb")
		languages=pickle.loads(f.read())
		f.close()
	for lang in languages.keys():
		if "official" not in languages[lang].keys(): languages[lang]["official"]=languages[lang]["released"]
	store_data=load_store_data()
	event_store_data=load_event_store_data()
	if not file_exists("compbans.svr"): open("compbans.svr","wb").close()
	init_mapsystem()
	load_compids()

	load_bans()
	load_mailbans()
	load_tempmail_domains()
	if file_exists("motd.txt")==False:
		f=open("motd.txt","w")
		f.close()
	f=open("motd.txt","r")
	f.close()
	setupserver()
	port = 55918 if "android" not in os.getcwd() else 55919
	
	print("=" * 65)
	print("                    ZERO HOUR ASSAULT GAME SERVER")
	print("=" * 65)
	print("[*] Initializing server systems...")
	print("[*] Loaded maps system.")
	print("[*] Loaded computer bans & tempmail lists.")
	print("[*] Compiled weapon statistics configuration.")
	print(f"[*] Binding ENet host to port {port}...")
	
	g.n.setup_server(port, 100, 100)
	
	print(f"[OK] Server successfully bound to port: {port}")
	print("[*] Network interface: 0.0.0.0 (All incoming connections allowed)")
	print("=" * 65)
	print("STATUS: [RUNNING] Listening for reliable UDP incoming connections...")
	print("Press Ctrl+C to terminate the server at any time.")
	print("=" * 65)

	for base in g.group_bases:
		if not chest_at(20, 25, 0, "basement"+base.name+base.mapappend):
			spawn_chest(20,25,0,"basement"+base.name+base.mapappend)
	while(True):
		time.sleep(0.001)
		try:
			netloop()

			gameloops()
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
		except SystemExit:
			os._exit(0)

		except:
			error = traceback.format_exc()
			developersend(error)
duplicatewalltimer=timer()
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
		for char in os.listdir("chars"):
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
		chestitemlist={"silencer":1,"berettaM9":1,"357_magnum":10,"S&WModel66":1,"fire_suppressant":1,"invisibility_shield":1,"fnhfnp45":1,"knife":1,"barricade":1,"ladder":1,"tm62":1,"7.62x54mmR":10,"metal_shield":1,"steel_helmet":1,"vitality_potion":1,"timebomb":1,"22_LR_Long_Rifle":30,"gsg5":1,"base_life_amplifier":9,"dragunov_psl":1,"fnhfnp40":1,"40S&W":40,"parachute":1,"mkek_jng90":1,"mkek_mpt76k":1,"m4":1,"mkek_yavuz16":1,"colt1911":1,"IthicaM37":1,"wooden_sword":1,"stone_sword":1,"diamond_sword":1,"molotov_cocktail":4,"7.62x51mm":20,"5.56x45mm":50,"9mm":20,"45_ACP":20,"12_gauge":15,"40S&W":50,"revival_nectar":1,"small_potion":2,"binoculars":1,"hand_grenade":3}
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
					for i in range(random(3,10)-len(chest.items)):
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
					charfolders=find_directories("chars")
					for dir in charfolders:
						if os.path.isfile("chars/"+dir+"/mailsent.usr"): os.remove("chars/"+dir+"/mailsent.usr")
						if os.path.isfile("chars/"+dir+"/todaygift.usr"): os.remove("chars/"+dir+"/todaygift.usr")

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
		f=open("language_data.dat","wb")
		f.write(pickle.dumps(languages))
		f.close()
g.gameloops=gameloops
def garbage_collect():
	gc.collect()

def file_get_contents(filename, mode="r"):
	ret=""
	if file_exists(filename)==False:
		return ""
	f=open(filename, mode)
	ret=f.read()
	f.close()
	return ret
def remove_duplicate_mapwalls(mapwalls):
	seen_mapwalls = set()
	index_to_remove = []

	for i, mapwall in enumerate(mapwalls):
		wall_tuple = (
			mapwall.minx,
			mapwall.maxx,
			mapwall.miny,
			mapwall.maxy,
			mapwall.minz,
			mapwall.maxz
		)

		if wall_tuple in seen_mapwalls:
			index_to_remove.append(i)
		else:
			seen_mapwalls.add(wall_tuple)

	for index in reversed(index_to_remove):
		del mapwalls[index]
e=None
def bilet_cevapla(soru):
    cevap = qa_chain.run(soru)
    
    if "üzgünüm" in cevap.lower() or len(cevap.strip()) < 10:
        return "Mesajınızı aldık, en kısa zamanda size dönüş yapılacaktır."
    else:
        return cevap


def netloop():
	global languages,e
	try:
		e=g.n.request()
	except:
		return
	if(e.type==event_disconnect) :
		px=g.get_player_index(e.peer_id)
		if(px>-1) :
			remove_from_server(px)
			
		
	if(e.type==event_receive):
	
		if (e.channel==1):
		
			parsed=string_split(e.message, " ",True)
			if (e.channel==1):
			
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
							f=os.listdir("chars/"+parsed[1]+"")
							final=""+parsed[1]+" has the following accounts.\n"
							if len(f)<=0:
								g.n.send_reliable(g.players[index].peer_id, "char not found", 0)
								return
							accounts=0
							mainid=file_get_contents("chars/"+parsed[1]+"/compid.usr")
							c=os.listdir("chars")
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
							chars=os.listdir("chars")
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
							chars=os.listdir("chars")
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
							chars=os.listdir("chars")
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
										chars=os.listdir("chars")
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
										chars=os.listdir("chars")
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
								chars=os.listdir("chars")
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
								chars=os.listdir("chars")
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
								filename="store.txt"
								with open(filename, "a") as file:
										file.write(""+item_name+":"+item_price+":"+category+":no description\n")
								
								g.n.send_reliable(e.peer_id, f"Item '{item_name}' added to store.", 0)
							else:
								g.n.send_reliable(e.peer_id, "You do not have permission to use this command.", 0)
						# --- /removeitemstore command ---
						elif parsed[0] == "/removeitemstore" and len(parsed) > 2:
							if g.players[index].is_admin():

								filename="store.txt"
								category=parsed[1]
								item_name = parsed[2]
								found_and_removed = False
								for ind, item in enumerate(store_data):
									if item["category"]==category and item["name"] == item_name:
										del store_data[ind]
										found_and_removed = True
										break
								
								if found_and_removed:
									with open(filename, 'w') as file:
										for item in store_data:
											file.write(f"{item['name']}:{item['price']}:{item['category']}:{item['description']}\n")

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

								filename="event_store.txt"
								with open(filename, "a") as file:
										file.write(""+item_name+":"+item_price+":no description\n")
								g.n.send_reliable(e.peer_id, f"Item '{item_name}' added to event store.", 0)
							else:
								g.n.send_reliable(e.peer_id, "You do not have permission to use this command.", 0)

						# --- /removeitemeventstore command ---
						elif parsed[0] == "/removeitemeventstore" and len(parsed) > 1:
							if g.players[index].is_admin():

								item_name = parsed[1]
								filename="event_store.txt"
								found_and_removed = False
								for ind, item in enumerate(event_store_data):
									if item["name"] == item_name:
										del event_store_data[ind]
										found_and_removed = True
										break
								

								if found_and_removed:
									with open(filename, 'w') as file:
										for item in event_store_data:
											file.write(f"{item['name']}:{item['price']}:{item['description']}\n")

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
								chars = os.listdir("chars")
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
									if numm==1: f=open("chars/"+parsed[1]+"/moderator.usr","w"); f.close(); adminsend(""+parsed[1]+" is now moderator by "+g.players[index].name+""); return

								else:
								
									num=string_to_number(parsed[2])
									if(num==1):
									
										adminsend(""+g.players[ind2].name+" is now moderator of the game by "+g.players[index].name+"")
										g.players[ind2].moderator=True
#										g.players[ind2].title="Moderator"
#										g.players[ind2].title2="Moderator"

#										g.n.broadcast(""+g.players[ind2].name+" is now moderator of zero_hour_assault!",2)
#										g.n.broadcast("play_s error-2-126514.ogg",0)
										f=open("chars/"+g.players[ind2].name+"/moderator.usr","w")
										f.close()
										
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
							f=open("chars/"+parsed[1]+"/beta.usr","w")
							f.close()
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
									if numm==1: f=open("chars/"+parsed[1]+"/admin.usr","w"); f.close(); adminsend(""+parsed[1]+" is now admin by "+g.players[index].name+""); return


								else:
								
									num=string_to_number(parsed[2])
									if(num==1):
									
										adminsend(""+g.players[ind2].name+" is now admin of the game by "+g.players[index].name+"")
										g.players[ind2].admin=True
#										g.players[ind2].title="Administrator"
#										g.players[ind2].title2="Administrator"

#										g.n.broadcast(""+g.players[ind2].name+" is now admin of zero_hour_assault!",2)
#										g.n.broadcast("play_s error-2-126514.ogg",0)
										f=open("chars/"+g.players[ind2].name+"/admin.usr","w")
										f.close()
										
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
							f=open("zitemdata.txt","w")
							f.write(parsed[2]+"="+parsed[1]+"="+parsed[3])
							f.close()
						elif parsed[0]=="/givepack2":
							adminsend(""+g.players[index].name+" gived "+parsed[1]+" to "+parsed[2]+" "+str(parsed[3])+"")
							f=open("ioszitemdata.txt","w")
							f.write(parsed[2]+"="+parsed[1]+"="+parsed[3])
							f.close()

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

									f=open("chars/"+parsed[1]+"/zhtoken.usr","w")
									f.write(str(finaly))
									f.close()
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
									if numm==1: f=open("chars/"+parsed[1]+"/builder.usr","w"); f.close(); adminsend(""+parsed[1]+" is now builder by "+g.players[index].name+""); return

								else:
								
									num=string_to_number(parsed[2])
									if(num==1):
									
										adminsend(""+g.players[ind2].name+" is now builder of the game by "+g.players[index].name+"")
										g.players[ind2].builder=True
#										g.players[ind2].title="Builder"
#										g.players[ind2].title2="Builder"

#										g.n.broadcast(""+g.players[ind2].name+" is now builder of zero_hour_assault!",2)
#										g.n.broadcast("play_s error-2-126514.ogg",0)
										f=open("chars/"+g.players[ind2].name+"/builder.usr","w")
										f.close()
										
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

								f=open("motd.txt","w")
								f.write(mess)
								f.close()
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
								if file_exists("changes.txt")==False:
									f=open("changes.txt", "w")
									f.close()
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
								if file_exists("frozen.txt")==False:
									f=open("frozen.txt","w")
									f.close()

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
							chars=os.listdir("chars")
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
									
								
							
						
					
				
			
		
	if e.channel==5:
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if g.players[index].hidden: return
			mess=e.message
			send_to=[]
			if 1:
				for i in g.players:
					if g.players[index].name in i.blocks or i.name in send_to or i.voicemessage==0: continue
					if i.name==g.players[index].name and g.players[index].listen==1: g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,5); send_to.append(i.name); continue
					if i.name==g.players[index].name and g.players[index].listen==0: continue
					if i.map!=g.players[index].map or (i.map==g.players[index].map and i.distancecheck(g.players[index].x,g.players[index].y,g.players[index].z)>30): continue
					#if i.name not in send_to: g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,5); send_to.append(i.name)

			if g.players[index].voicechatmap==1:
				for i in g.players:
					if i.voicechatmap==0 or g.players[index].name in i.blocks or i.name in send_to or i.voicemessage==0: continue
					if i.name==g.players[index].name and g.players[index].listen==1: g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,5); send_to.append(i.name); continue
					if i.name==g.players[index].name and g.players[index].listen==0: continue
					if i.map!=g.players[index].map or (i.map==g.players[index].map and i.distancecheck(g.players[index].x,g.players[index].y,g.players[index].z)>30): continue
					g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,5); send_to.append(i.name)
			if g.players[index].voicechatgroup==1:
				for i in g.players:
					if i.voicechatgroup==0 or g.players[index].name in i.blocks or i.name in send_to or i.voicemessage==0: continue
					if i.name==g.players[index].name and g.players[index].listen==1: g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,5); send_to.append(i.name); continue
					if i.name==g.players[index].name and g.players[index].listen==0: continue
					if i.group!=g.players[index].group: continue
					if i.group=="": continue
					g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,5); send_to.append(i.name)

			if g.players[index].voicechatteam==1:
				for i in g.players:
					if i.voicechatteam==0 or g.players[index].name in i.blocks or i.name in send_to or i.voicemessage==0: continue
					if i.name==g.players[index].name and g.players[index].listen==1: g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,5); send_to.append(i.name); continue
					if i.name==g.players[index].name and g.players[index].listen==0: continue
					if i.matchteam!=g.players[index].matchteam and i.matchteam!="" and g.players[index].matchteam!="": continue
					if i.matchteam=="": continue
					g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,5); send_to.append(i.name)
			if g.players[index].voicechatfriend==1:
				for i in g.players:
					if i.voicechatfriend==0 or g.players[index].name in i.blocks or i.name in send_to or i.voicemessage==0: continue
					if i.name==g.players[index].name and g.players[index].listen==1: g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,5); send_to.append(i.name); continue
					if i.name==g.players[index].name and g.players[index].listen==0: continue
					if i.name not in g.players[index].friendlist: continue
					g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,5); send_to.append(i.name)
	if e.channel==6:
		index=g.get_player_index(e.peer_id)
		if(index>-1):
			if g.players[index].hidden: return
			mess=e.message
			send_to=[]
			if 1:
				for i in g.players:
					if g.players[index].name in i.blocks or i.name in send_to or i.voicemessage2==0: continue
					try:
						if i.name==g.players[index].name and g.players[index].listen==1: g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,6); send_to.append(i.name); continue
					except: pass
					if i.name==g.players[index].name and g.players[index].listen==0: continue
					if i.map!=g.players[index].map: continue
					#if i.name not in send_to: g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,6); send_to.append(i.name)

			if 1:
				for i in g.players:
					if g.players[index].name in i.blocks or i.name in send_to or i.voicemessage2==0: continue
					if i.name==g.players[index].name and g.players[index].listen==1:
						try: g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,6); send_to.append(i.name); continue
						except: pass
					if i.name==g.players[index].name and g.players[index].listen==0: continue
					if i.community!=g.players[index].community: continue
					if i.community=="": continue
					try: g.n.send_unreliable(i.peer_id,g.players[index].name.encode()+b" "+mess,6); send_to.append(i.name)
					except: pass


	if (e.channel==2):
	
		parsed=string_split(e.message, "{}[]", True)
		if parsed[0]=="answerticket":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				ticket=find_ticket_by_title(parsed[1])
				if ticket is None:
					g.n.send_reliable(e.peer_id,"Error, ticket not found!",0); return
				if ticket["closed"]:
					g.n.send_reliable(e.peer_id,"This ticket is closed, you can't answer!",0); return
				ticket["pending"]=False
				if g.players[index].dev:
					prank = "Support Team"
				elif g.players[index].is_admin():
					prank = "Support Team"
				elif g.players[index].moderator==True:
					prank = "Support Team"
				elif g.players[index].builder:
					prank = "Support Team"
				else:
					prank = ""
				if prank!="":
					ticket["messages"]+="\nSupport Team, "+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"\n"+parsed[2]

				elif prank=="":
					ticket["messages"]+="\n"+g.players[index].name+", "+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"\n"+parsed[2]

				ticket["lastupdate"]=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				g.n.send_reliable(e.peer_id,"Done, answer sent successfully.",0)
				adminsend(g.players[index].name+" answered to the "+ticket["title"]+" ticket, "+parsed[2])
				notify_admins("zero_hour_assault, "+g.players[index].name+" answered to the "+ticket["title"]+" ticket, "+parsed[2])

				getmail=file_get_contents("chars/"+ticket["owner"]+"/mail.usr")
				ticket["closetimer"].restart()
				#if is_enabled_ticket_mail(ticket["owner"]): send_mail(getmail,"Your ticket "+ticket["title"]+" has been updated","Hello<br>You'r ticket "+ticket["title"]+" is updated and answered by staff.<br>"+g.players[index].name+" answered you: "+parsed[2]+"<br>We will wait your answer back.<br>If you do not answer back within 24 hours, the ticket will automaticaly be closed.<br>Regards,<br>Nbm studios team")

				if g.players[index].name!=ticket["owner"]:
					ind=get_player_index_from(ticket["owner"])
					if ind>-1:
						g.n.send_reliable(g.players[ind].peer_id,"Your ticket with id "+ticket["id"]+" is updated, please check!",2)
						g.n.send_reliable(g.players[ind].peer_id,"play_s misc304.ogg",0)
					else:
						file_put_contents("chars/"+ticket["owner"]+"/ticketinform.usr","Your ticket with "+ticket["id"]+" is updated, please check!")
		if parsed[0]=="pointticket":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				file_delete("chars/"+g.players[index].name+"/rateneeded.usr")
				ticket=find_ticket_by_title(parsed[1])
				if ticket is None:
					g.n.send_reliable(e.peer_id,"Error, ticket not found!",0); return
				ticket["messages"]+="\n"+g.players[index].name+" rated this ticket "+parsed[2]+" points at "+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"\n"
				ticket["lastupdate"]=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				g.n.send_reliable(e.peer_id,"Done, rating sent successfully.",0)
				adminsend(g.players[index].name+" rated "+parsed[2]+" points to the "+ticket["title"]+" ticket")
				notify_admins("zero hour assault, "+g.players[index].name+" rated "+parsed[2]+" points to the "+ticket["title"]+" ticket")


		if parsed[0]=="closeticket":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				ticket=find_ticket_by_title(parsed[1])
				if ticket is None:
					g.n.send_reliable(e.peer_id,"Error, ticket not found!",0); return
				if ticket["closed"]:
					g.n.send_reliable(e.peer_id,"This ticket is already closed!",0); return
				ticket["closed"]=True
				ticket["messages"]+="\nThis ticket was closed by Support Team in "+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				ticket["lastupdate"]=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				adminsend(g.players[index].name+" closed the "+ticket["title"]+" ticket.")
				notify_admins("zero hour assault, "+g.players[index].name+" closed the "+ticket["title"]+" ticket.")
				getmail=file_get_contents("chars/"+ticket["owner"]+"/mail.usr")
				if is_enabled_ticket_mail(ticket["owner"]): send_mail(getmail,"your ticket "+ticket["title"]+" has been resolved and closed","Hello "+ticket["owner"]+"<br>your ticket "+ticket["title"]+" has been closed by Support Team.<br>Below is all the ticket messages:<br>"+ticket["messages"].replace("\n","<br>")+"<br>If you have more questions or need help, please create a support ticket again from the game or contact us at contact@nbmstudios.com<br>regards,<br>Nbm studios team")

				file_put_contents("chars/"+ticket["owner"]+"/rateneeded.usr","")
				g.n.send_reliable(g.players[index].peer_id,"Done, ticket closed successfully.",0)
				if g.players[index].name!=ticket["owner"]:
					ind=get_player_index_from(ticket["owner"])
					if ind>-1:
						g.n.send_reliable(g.players[ind].peer_id,"Your ticket with id "+ticket["id"]+" is closed",2)
					else:
						file_put_contents("chars/"+ticket["owner"]+"/ticketinform.usr","Your ticket with "+ticket["id"]+" is closed")

		if parsed[0]=="openticket":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				ticket=find_ticket_by_title(parsed[1])
				if ticket is None:
					g.n.send_reliable(e.peer_id,"Error, ticket not found!",0); return
				if not ticket["closed"]:
					g.n.send_reliable(e.peer_id,"This ticket is not closed!",0); return
				ticket["closed"]=False
				ticket["closetimer"].restart()
				ticket["messages"]+="\nThis ticket was reopened by Support Team at "+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				ticket["lastupdate"]=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				adminsend(g.players[index].name+" reopened the "+ticket["title"]+" ticket.")
				notify_admins("zero hour assault, "+g.players[index].name+" reopened the "+ticket["title"]+" ticket.")
				g.n.send_reliable(e.peer_id,"Done, ticket reopened successfully.",0)
				getmail=file_get_contents("chars/"+ticket["owner"]+"/mail.usr")
				if is_enabled_ticket_mail(ticket["owner"]): send_mail(getmail,"your ticket "+ticket["title"]+" has been reopened","Hello "+ticket["owner"]+"<br>your ticket "+ticket["title"]+" has been reopened by Support Team.<br>We will answer you as soon as possible. We will resolve your issue soon.<br>regards,<br>Nbm studios team")

				if g.players[index].name!=ticket["owner"]:
					ind=get_player_index_from(ticket["owner"])
					if ind>-1:
						g.n.send_reliable(g.players[ind].peer_id,"Your ticket with id "+ticket["id"]+" is reopened",0)
					else:
						file_put_contents("chars/"+ticket["owner"]+"/ticketinform.usr","Your ticket with "+ticket["id"]+" is reopened")

		if parsed[0]=="maketicketpending":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				ticket=find_ticket_by_title(parsed[1])
				if ticket is None:
					g.n.send_reliable(e.peer_id,"Error, ticket not found!",0); return
				if ticket["pending"]:
					g.n.send_reliable(e.peer_id,"This ticket is already pending!",0); return
				ticket["pending"]=True
				ticket["messages"]+="\nThis ticket was marked as pending by Support Team at "+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				ticket["lastupdate"]=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				adminsend(g.players[index].name+" made pending the "+ticket["title"]+" ticket.")
				notify_admins("zero hour assault, "+g.players[index].name+" made pending the "+ticket["title"]+" ticket.")
				g.n.send_reliable(e.peer_id,"Done, ticket made pending successfully.",0)
				#getmail=file_get_contents("chars/"+ticket["owner"]+"/mail.usr")
				#if is_enabled_ticket_mail(ticket["owner"]): send_mail(getmail,"your ticket "+ticket["title"]+" has been marked as pending","Hello "+ticket["owner"]+"<br>your ticket "+ticket["title"]+" has been marked as pending by "+g.players[index].name+"<br>We will answer you as soon as possible. We will resolve your issue soon.<br>Staff will make your ticket not pending and answer you once a solution is found to your problem.<br>regards,<br>Nbm studios team")

				if g.players[index].name!=ticket["owner"]:
					ind=get_player_index_from(ticket["owner"])
					if ind>-1:
						g.n.send_reliable(g.players[ind].peer_id,"Your ticket with id "+ticket["id"]+" is marked as pending",0)
					else:
						file_put_contents("chars/"+ticket["owner"]+"/ticketinform.usr","Your ticket with "+ticket["id"]+" is marked as pending")


		if parsed[0]=="maketicketnotpending":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				ticket=find_ticket_by_title(parsed[1])
				if ticket is None:
					g.n.send_reliable(e.peer_id,"Error, ticket not found!",0); return
				if not ticket["pending"]:
					g.n.send_reliable(e.peer_id,"This ticket is not pending!",0); return
				ticket["pending"]=False
				ticket["messages"]+="\nThis ticket was marked as not pending by Support Team at "+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				ticket["lastupdate"]=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				ticket["closetimer"].restart()
				ticket["closetimer"].pause()
				adminsend(g.players[index].name+" made not pending the "+ticket["title"]+" ticket.")
				notify_admins("zero hour assault, "+g.players[index].name+" made not pending the "+ticket["title"]+" ticket.")
				g.n.send_reliable(e.peer_id,"Done, ticket made not pending successfully.",0)
				getmail=file_get_contents("chars/"+ticket["owner"]+"/mail.usr")
				if is_enabled_ticket_mail(ticket["owner"]): send_mail(getmail,"your ticket "+ticket["title"]+" has been marked as not pending","Hello "+ticket["owner"]+"<br>your ticket "+ticket["title"]+" has been marked as not pending by Support Team.<br>We will answer you as soon as possible. We will resolve your issue soon.<br>regards,<br>Nbm studios team")

				if g.players[index].name!=ticket["owner"]:
					ind=get_player_index_from(ticket["owner"])
					if ind>-1:
						g.n.send_reliable(g.players[ind].peer_id,"Your ticket with id "+ticket["id"]+" is marked as not pending",0)
					else:
						file_put_contents("chars/"+ticket["owner"]+"/ticketinform.usr","Your ticket with "+ticket["id"]+" is marked as not pending")


		if parsed[0]=="newticket":
			index=g.get_player_index(e.peer_id)
			if(index>-1):
				if file_exists("chars/"+g.players[index].name+"/rateneeded.usr"): g.n.send_reliable(e.peer_id,"you cannot create a new ticket without raing your last closed ticket",0); return
				found_tickets=0
				for ticket in g.tickets:
					if not ticket["closed"] and ticket["owner"]==g.players[index].name:
						found_tickets+=1
				if found_tickets>=5: g.n.send_reliable(e.peer_id,"You can't have more than 5 open tickets",0); return
				title=parsed[1]
				title="#"+str(len(g.tickets)+1)+" "+title
				g.tickets.append({"title":title,"closetimer":timer(),"messages":title+"\ndepartment\n"+parsed[3]+"\n"+g.players[index].name+", "+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\n"+parsed[2]),"department":parsed[3],"closed":False,"pending":False,"owner":g.players[index].name,"id":"#"+str(len(g.tickets)+1),"lastupdate":str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),"createdate":str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))})
				g.n.send_reliable(g.players[index].peer_id,"play_s misc216.ogg",0)
				g.n.send_reliable(e.peer_id,"Done, ticket has been created with id: #"+str(len(g.tickets)),0)
				adminsend("The "+title+" ticket was created by "+g.players[index].name)
				notify_admins("zero hour assault, The "+title+" ticket was created by "+g.players[index].name + "\n\nMessages:\n" + g.tickets[-1]["messages"])
				save_tickets()
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
				if g.players[index].ios: f=open("ioszitemdata.txt","a")
				elif not g.players[index].ios: f=open("zitemdata.txt","a")
				f.write(e.message.replace("writeitemdata ","")+"\n")
				f.close()
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
				if file_exists("suggest.txt")==False:
					f=open("suggest.txt","w")
					f.close()
				f=open("suggest.txt","a")
				f.write(""+g.players[index].name+": "+message+", "+get_date()+", "+get_time(True, True)+"\n")
				f.close()
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
		
		elif parsed[0]=="ticket_create_department": # Department chosen, finalize ticket (NEW FLOW)
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
				
				os.chdir("maps")
				for base in g.group_bases:
					if base.name==old_group_name: # Changed to check against old_group_name variable for safety
						if file_exists("basement"+old_group_name+base.mapappend+".map"):
							os.rename("basement"+old_group_name+base.mapappend+".map","basement"+parsed[1]+base.mapappend+".map")
						for chest in g.chests:
							if chest.map=="basement"+old_group_name+base.mapappend: chest.map="basement"+parsed[1]+base.mapappend

				os.chdir("..")
				
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
				os.chdir("chars")
				g.n.send_reliable(e.peer_id,"Done",0)
				oldname=g.players[index].name
				remove_from_server(index)

				try: os.rename(oldname,parsed[1])
				except: pass
				os.chdir("..")
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
					r=open("adminlog.txt", "r")
					changes=string_split(r.read(), "\n", True)
					if len(changes)<=0 or not file_exists("adminlog.txt") or file_get_contents("adminlog.txt")=="":
						send_reliable(e.peer_id, "no logs", 0)
						g.players[index].prevmenu()
						r.close()
						return
					r.close()
					m=server_menu()
					m.intro="Command logs."
					m.initial_packet="latest"
					for i in range(len(changes)):
						m.add(string_replace(changes[i], ":", ".", True), string_replace(changes[i], ":", ".", True),False)
					m.send(e.peer_id)
				if parsed[1]=="adminhelp":
					r=open("adminhelp.txt", "rb")
#					changes=string_split(r.read(), "\n", True)
					changes=string_split(r.read().decode("utf-8",errors="ignore"), "\n", True)
					if len(changes)<=0 or not file_exists("adminhelp.txt") or file_get_contents("adminhelp.txt")=="":
						send_reliable(e.peer_id, "no help", 0)
						g.players[index].prevmenu()
						r.close()
						return
					r.close()
					m=server_menu()
					m.intro="Admin help menu. Here you can view commands for admins."
					m.initial_packet="latest"
					for i in range(len(changes)):
						m.add(string_replace(changes[i], ":", ".", True), string_replace(changes[i], ":", ".", True),False)
					m.send(e.peer_id)
				if parsed[1]=="moderatorhelp":
					r=open("moderatorhelp.txt", "r")
					changes=string_split(r.read(), "\n", True)
					if len(changes)<=0 or not file_exists("moderatorhelp.txt") or file_get_contents("moderatorhelp.txt")=="":
						send_reliable(e.peer_id, "no help", 0)
						g.players[index].prevmenu()
						r.close()
						return
					r.close()
					m=server_menu()
					m.intro="moderator help menu. Here you can view commands for moderators."
					m.initial_packet="latest"
					for i in range(len(changes)):
						m.add(string_replace(changes[i], ":", ".", True), string_replace(changes[i], ":", ".", True),False)
					m.send(e.peer_id)

				if parsed[1]=="builderhelp":
					r=open("builderhelp.txt", "r")
					changes=string_split(r.read(), "\n", True)
					if len(changes)<=0 or not file_exists("builderhelp.txt") or file_get_contents("builderhelp.txt")=="":
						send_reliable(e.peer_id, "no help", 0)
						g.players[index].prevmenu()
						r.close()
						return
					r.close()
					m=server_menu()
					m.intro="Builder help menu. Here you can view commands for builders."
					m.initial_packet="latest"
					for i in range(len(changes)):
						m.add(string_replace(changes[i], ":", ".", True), string_replace(changes[i], ":", ".", True),False)
					m.send(e.peer_id)


				if parsed[1]=="suggestion":
					r=open("suggest.txt", "r")
					changes=string_split(r.read(), "\n", True)
					if len(changes)<=0 or not file_exists("suggest.txt") or file_get_contents("suggest.txt")=="":
						send_reliable(e.peer_id, "no suggestions", 0)
						g.players[index].prevmenu()
						r.close()
						return
					r.close()
					m=server_menu()
					m.intro="Suggestions."
					m.initial_packet="latest"
					for i in range(len(changes)):
						m.add(string_replace(changes[i], ":", ".", True), string_replace(changes[i], ":", ".", True),False)
					m.send(e.peer_id)
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
					r=open("changes.txt", "r")
					changes=string_split(r.read(), "\n", True)
					if len(changes)<=0 or not file_exists("changes.txt") or file_get_contents("changes.txt")=="":
						send_reliable(e.peer_id, "no Latest Additions", 0)
						r.close()
						return
					r.close()
					m=server_menu()
					m.intro="Latest Additions."
					m.initial_packet="latest"
					for i in range(len(changes)):
						m.add(string_replace(changes[i], ":", ".", True), string_replace(changes[i], ":", ".", True),False)
					m.send(e.peer_id)
				if parsed[1]=="rules":
					r=open("rules.txt", "rb")
					changes=string_split(r.read().decode("utf-8",errors="ignore"), "\n", True)
					if len(changes)<=0 or not file_exists("rules.txt"):
						send_reliable(e.peer_id, "no rules.", 0)
						r.close()
						return
					r.close()
					m=server_menu()
					m.intro="Rules."
					m.initial_packet="latest"
					for i in range(len(changes)):
						m.add(string_replace(changes[i], ":", ".", True), string_replace(changes[i], ":", ".", True),False)
					m.send(e.peer_id)

				if parsed[1]=="readme":
					r=open("readme.txt", "r")
					changes=string_split(r.read(), "\n", True)
					if len(changes)<=0 or not file_exists("readme.txt") or file_get_contents("readme.txt")=="":
						send_reliable(e.peer_id, "The file could be not found.", 0)
						r.close()
						return
					r.close()
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
					
				

		elif parsed[0]=="move_map":
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
		elif parsed[0]=="matchmodeprivate" and len(parsed)>1:
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


		elif parsed[0]=="enter":
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
			
			


		elif(parsed[0]=="create" and len(parsed)>4):
		
			create(parsed[1],parsed[2],parsed[3],parsed[4],parsed[5],e.peer_id)
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
		elif parsed[0]=="bikemove":
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

				# 3. Klasörü işletim sistemi seviyesinde taşı (Eskiyi siler, yeniyi yaratır)
				try:
					os.chdir("chars")
					os.rename(old_name, new_name)
					os.chdir("..")
				except Exception as ex:
					os.chdir("..") # Hata olsa bile ana dizine dön
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
			
				if g.players[index].renaming: remove_from_server(index); return
				if g.players[index].movetimer.elapsed>=0:
					g.players[index].movetimer.restart()
					g.players[index].weapon_rays=None
					g.players[index].weapon_rays2=None
					charname=g.players[index].name
					g.players[index].x=float(parsed[1])
					g.players[index].y=float(parsed[2])
					g.players[index].z=float(parsed[3])
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
			
				if g.players[index].move2timer.elapsed>=0:
					g.players[index].move2timer.restart()
					g.players[index].weapon_rays=None
					g.players[index].weapon_rays2=None

					name=g.players[index].name
					g.players[index].x=float(parsed[1])
					g.players[index].y=float(parsed[2])
					g.players[index].z=float(parsed[3])
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
			
				if g.players[index].move3timer.elapsed>=0:
					g.players[index].move3timer.restart()
					name=g.players[index].name
					g.players[index].weapon_rays=None
					g.players[index].weapon_rays2=None

					g.players[index].x=float(parsed[1])
					g.players[index].y=float(parsed[2])
					g.players[index].z=float(parsed[3])
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
					g.players[index].wx=float(parsed[1])
					g.players[index].wy=float(parsed[2])
					g.players[index].wz=float(parsed[3])
				
			
		
		
		
g.netloop=netloop
def exit():
	os._exit(0)
def adminsend(mesaj):
	if file_exists("adminlog.txt")==False:
		f=open("adminlog.txt","w")
		f.close()
	f=open("adminlog.txt","a")
	f.write(""+mesaj+", "+get_date()+", "+get_time(True, True)+"\n")
	f.close()
	for i in g.players:
		if i.is_admin()==True or i.dev==True or i.moderator==True:
			g.n.send_reliable(i.peer_id,"play_s misc205.ogg",0)
			g.n.send_reliable(i.peer_id,"adminmessage "+mesaj,0)
def adminsend2(mesaj):
	if file_exists("adminlog.txt")==False:
		f=open("adminlog.txt","w")
		f.close()
	f=open("adminlog.txt","a")
	f.write(""+mesaj+", "+get_date()+", "+get_time(True, True)+"\n")
	f.close()
	for i in g.players:
		if i.is_admin()==True or i.dev==True or i.moderator==True:
			g.n.send_reliable(i.peer_id,"play_s misc205.ogg",0)
			g.n.send_reliable(i.peer_id,"adminmessage "+mesaj,0)

def adminsendsound(sound):
	for i in g.players:
		if i.is_admin()==True or i.dev==True or i.moderator==True:
			g.n.send_reliable(i.peer_id,"play_s "+sound+".ogg",0)

def get_date(include_weekday=False, numerical=True):
	return ""
def get_time(twelvehour=True, include_seconds=True):
	return str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def developersend(mesaj):
	if 1:
		data=file_get_contents("error.log")
		f=open("error.log","a")
		if not string_contains(data,mesaj,1)>-1: f.write(""+mesaj+"")
		f.close()
		for i in range(len(g.players)):
			if g.players[i].dev==True:
#				g.n.send_reliable(g.players[i].peer_id,"play_s admchat.ogg",0)
				g.n.send_reliable(g.players[i].peer_id,mesaj,2)
def stn(n):
	return string_to_number(n)

def send_reliable(peer, mess, channel, playerindex=None):
	if(playerindex is not None):
	
		x=playerindex.x
		y=playerindex.y
		z=playerindex.z
		for i in range(len(g.players)):
		
			if(g.players[i].x > x-25 and g.players[i].x < x+25 and g.players[i].y > y-25 and g.players[i].y < y+25 and g.players[i].z > z-25 and g.players[i].z < z+25 and g.players[i].map==playerindex.map):
			
				g.n.send_reliable(g.players[i].peer_id, mess, channel)
				
			
		
	else:
	
		g.n.send_reliable(peer, mess, channel)
		
	
g.send_reliable=send_reliable
def login(user, password, mail, compid, peer_id):
	compbanloop()
	#for p in g.players:
		#if p.compid==compid: g.n.send_reliable(peer_id,"banned error. You can't login to the game from the same computer 2 or more times",0); return
	#for p in g.players:
		#if str(g.n.get_peer_address(p.peer_id))==str(g.n.get_peer_address(peer_id)): g.n.send_reliable(peer_id,"banned error. You can't login to the game from the same network 2 or more times",0); return
#	if file_exists("chars/"+user+"/beta.usr")==False and file_exists("chars/"+user+"/developer.usr")==False: g.n.send_reliable(peer_id,"banned you are not betatester of this version. Contact with developers for more assistance",0); return

	if(not directory_exists("chars/"+user)):
	
		g.n.send_reliable(peer_id,"doesnotexist",0)
		return
	if "/" in user:
		g.n.send_reliable(peer_id,"banned Your account name contain an unexpected symbol. Please contact with developers for more info.",0)
		return
	if ":" in user:
		g.n.send_reliable(peer_id,"banned Your account name contain an unexpected symbol. Please contact with developers for more info.",0)
		return

	"""
	if(not file_exists("chars/"+user+"/developer.usr")):
	
		g.n.send_reliable(peer_id,"banned You cannot log in to the game at this time. Reason: The game will be updated turkiye time at 9:30 PM. We kindly ask for your patience during this time.",0)
		return
"""
	compbanned=is_compbanned(compid)
	compbanned2=is_compbanned(compid,user)
	if compbanned2 and not compbanned:
		if file_exists("chars/"+user+"/permaban.usr"): send_reliable(peer_id, "banned Error. You have been permanently banned. Reason: "+file_get_contents("chars/"+user+"/banreason.usr"),0)
		elif file_exists("chars/"+user+"/banenddate.usr"): send_reliable(peer_id, "banned Error. You have been banned. Reason: "+file_get_contents("chars/"+user+"/banreason.usr")+". The ban will end after "+get_playerban_end_time(user), 0)
		return
	elif compbanned:
		user2=get_player_from_compid(compid)
		if not file_exists("chars/"+user2+"/permaban.usr") and not file_exists("chars/"+user+"/permaban.usr"): send_reliable(peer_id, "banned Error. You have been banned. Reason: "+get_compban_reason(compid)+". The ban will end after "+get_compban_end_time(compid), 0)
		elif file_exists("chars/"+user2+"/permaban.usr") or file_exists("chars/"+user+"/permaban.usr"): send_reliable(peer_id, "banned Error. You have been permanently banned. Reason: "+get_compban_reason(compid),0)
		return
	dir="chars/"+user
	f=open(dir+"/pass.usr","r")
	contents=f.read()
	f.close()
	if(contents!=password):
	
		g.n.send_reliable(peer_id,"wrongpass",0)
		return
		
	f=open(dir+"/mail.usr","r")
	contents2=f.read()
	f.close()
	if(contents2!=mail):
	
		g.n.send_reliable(peer_id,"wrongmail",0)
		return
		
	# if file_exists("chars/"+user+"/pending_email_verify.usr"):
	# 	g.n.send_reliable(peer_id,"verify",0)
	# 	return

	compids=file_get_contents("chars/"+user+"/authorized_compids.usr").split("\n")
	authreq=0
	if file_exists("chars/"+user+"/authreq.usr"): authreq=int(file_get_contents("chars/"+user+"/authreq.usr"))
	# if authreq==1 and compid not in compids:
	# 	if file_exists("chars/"+user+"/lastverify.usr"):
	# 		verifydate=pickle.loads(file_get_contents("chars/"+user+"/lastverify.usr","rb"))
	# 		if not time_difference_exceeds_2_hours(datetime.now(),verifydate):
	# 			g.n.send_reliable(peer_id,"message Error. This computer is not authorized to log into your account, but you already authorized one computer in the last 2 hours. You can only authorize one computer per 2 hours.",0); return
	# 	g.n.send_reliable(peer_id,"verify",0)
	# 	return

	for i in range(len(g.players)):
		if(g.players[i].name==user):
			if compid==g.players[i].compid: remove_from_server(i)
			else: g.n.send_reliable(peer_id,"banned This user is already logged in.",0); return
	if not compid_handlercheck(compid):
		add_compid(compid, user)

	f=open(dir+"/compid.usr", "w")
	f.write(compid)
	f.close()

	f=open(dir+"/map.usr","r")
	m=f.read()
	f.close()
	for i in g.matches:
		if i.get_cwmap()==m and user not in i.players: m="lobby"
	if(get_map_index(m)<0):
		m="lobby"
	stuff=g.maps[get_map_index(m)].rawdata
	g.n.send_reliable(peer_id,"mapdata "+stuff,0)
	f=open(dir+"/facing.usr","r")
	g.n.send_reliable(peer_id, "facing "+f.read(), 0)
	f.close()
	f=open(dir+"/x.usr","r")
	g.n.send_reliable(peer_id, "x "+f.read(), 0)
	f.close()
	f=open(dir+"/y.usr","r")
	g.n.send_reliable(peer_id, "y "+f.read(), 0)
	f.close()
	f=open(dir+"/z.usr","r")
	g.n.send_reliable(peer_id, "z "+f.read(), 0)
	f.close()
	g.n.send_reliable(peer_id,"startmoving",0)
	if file_exists("frozen.txt")==True:
		g.n.send_reliable(peer_id,"stopmoving",0)

		g.n.send_reliable(peer_id,"play_s important.ogg",0)
		g.n.send_reliable(peer_id,"Attention. The game is frozen. Please be patient.",2)

	auth_computers=file_get_contents("chars/"+user+"/authorized_compids.usr").split("\n")
	if compid not in auth_computers: auth_computers.append(compid)
	file_put_contents("chars/"+user+"/authorized_compids.usr","\n".join(auth_computers))

	g.n.send_reliable(peer_id, "loggedin", 0)
	
def getplayer_by_peer(id):
	for i in range(len(g.players)):
	
		if(g.players[i].peer_id==id):
		
			return i
			
		
	return -1
	
def get_player_index(id):
	founds=[]
	for i in range(len(g.players)):
		try:
			if g.players[i].peer_id==id: founds.append(i)
		except: pass
	try: return founds[-1]
	except: return -1
g.get_player_index=get_player_index
def get_player_index_from(name):
	founds=[]
	for i in range(len(g.players)):
		if g.players[i].name==name: founds.append(i)
	try: return founds[-1]
	except: return -1
def get_player_index_fromnpc(name):
	for i in range(len(g.players)):
		if g.players[i].name==name: return i
	for i in range(len(g.npcs)):
		if g.npcs[i].name==name: return i

	return -1
g.get_player_index_fromnpc=get_player_index_fromnpc
def getpc(name):
	for i in range(len(g.players)):
		if g.players[i].name==name: return g.players[i]
	for i in range(len(g.npcs)):
		if g.npcs[i].name==name: return g.npcs[i]

	return None
g.getpc=getpc

g.get_player_index_from=get_player_index_from
def create(un,pw,mail,gender,compid,id):
	if " " in un or "." in un or ":" in un or "/" in un: g.n.send_reliable(id,"banned invalid input",0); return
	if not un.isascii():
		g.n.send_reliable(id, "banned Username must contain only ASCII characters (English alphabet/numbers).", 0)
		return
	compbanloop()
	if(not directory_exists("chars")):
		directory_create("chars")
#	if file_exists("chars/"+un+"/beta.usr")==False: g.n.send_reliable(id,"banned you are not betatester of this version. Contact with developers for more assistance",0); return
	compbanned=is_compbanned(compid)
	if compbanned==True:
		if not file_exists("chars/"+get_player_from_compid(compid)+"/permaban.usr"): g.n.send_reliable(id, "banned Error. You have been banned. Reason: "+get_compban_reason(compid)+". The ban will end after "+get_compban_end_time(compid), 0)
		if file_exists("chars/"+get_player_from_compid(compid)+"/permaban.usr"): g.n.send_reliable(id, "banned Error. You have been permanently banned. Reason: "+get_compban_reason(compid), 0)
		return

	if is_mailbanned(mail):
		g.n.send_reliable(id, "banned This email address is not allowed to create an account.", 0)
		return

	if is_tempmail(mail):
		g.n.send_reliable(id, "banned Temporary/disposable email addresses are not allowed. Please use a real email address.", 0)
		return

	dir="chars/"+un

	if(directory_exists2(dir.lower())):

		g.n.send_reliable(id,"alreadyexists",0)
		return

	for i in range(len(usernames)):
		if un==usernames[i]:
			g.n.send_reliable(id,"alreadyexists",0)
			return
	numaccounts=0
	for i in os.listdir("chars"):
		if compid==file_get_contents("chars/"+i+"/compid.usr"):
			numaccounts+=1
	if numaccounts>=2: g.n.send_reliable(id, "message you only have right to create two accounts per computer.", 0); return
	g.n.broadcast("play_s alert2.ogg",0)
	g.n.broadcast("A new character named "+un+" has been created! We wish them an epic journey in the game.",2)
	directory_create(dir)
	f=open(dir+"/x.usr","w")
	f.write("5")
	f.close()
	f=open(dir+"/scorepoint.usr","w")
	f.write("0")
	f.close()

	f=open(dir+"/y.usr","w")
	f.write("0")
	f.close()
	f=open(dir+"/z.usr","w")
	f.write("0")
	f.close()
	f=open(dir+"/map.usr","w")
	f.write("lobby")
	f.close()
	f=open(dir+"/gender.usr","w")
	f.write(gender)
	f.close()


	f=open(dir+"/facing.usr","w")
	f.write("0")
	f.close()
	f=open(dir+"/pass.usr","w")
	f.write(pw)
	f.close()
	f=open(dir+"/mail.usr","w")
	f.write(mail)
	f.close()

	f=open(dir+"/health.usr","w")
	f.write("100")
	f.close()
	try:
		f=open(dir+"/maldied.usr","w")
		f.close()
	except: pass
	f=open(dir+"/compid.usr", "w")
	f.write(compid)
	f.close()
	f=open(dir+"/authorized_compids.usr", "w")
	f.write(compid)
	f.close()

	# file_put_contents(dir+"/pending_email_verify.usr", "")
	add_compid(compid, un)
	charwrite(un,"createdate",str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
	g.n.send_reliable(id,"created",0)
	
def charwrite(name,thing,value):
	try:
		f=open("chars/"+name+"/"+thing+".usr","w")
		f.write(str(value))
		f.close()
	except: pass
def charwriteb(name,thing,value):
	try:
		f=open("chars/"+name+"/"+thing+".usr","wb")
		f.write(value)
		f.close()
	except: pass
	
def save_char(index):
	np=g.players[index].name
	charwrite(np, "last_admin_login_ticket_count", g.players[index].last_admin_login_ticket_count)
	charwrite(np,"x",g.players[index].x)
	charwrite(np,"spatialized_by",g.players[index].spatialized_by)
	charwrite(np,"spatializertimer",g.players[index].spatializertimer.elapsed)
	charwrite(np,"backpacks_level",g.players[index].backpacks_level)
	charwrite(np,"beacon",g.players[index].beacon)
	charwrite(np,"parachuted",("1" if g.players[index].parachuted else "0"))
	charwriteb(np,"backpacktimer",pickle.dumps(g.players[index].backpacktimer))
	charwrite(np,"adrenalinetime",g.players[index].adrenalinetimer.elapsed)
	charwrite(np,"jammertime",g.players[index].jammertimer.elapsed)
	charwrite(np,"helitimer",g.players[index].helitimer.elapsed)
	charwrite(np,"weapon",g.players[index].weapon)
	charwrite(np,"weapon2",g.players[index].weapon2)
	charwrite(np,"helijumptimer",g.players[index].helijumptimer.elapsed)
	charwrite(np,"freedomhelicopter",str(g.players[index].freedomhelicopter))
	charwrite(np,"freedomhelicoptertimer",str(g.players[index].freedomhelicoptertimer.elapsed))
	charwrite(np,"ticketmail",g.players[index].ticketmail)
	charwrite(np,"communitymessage",g.players[index].communitymessage)
	charwrite(np,"matchinvite",g.players[index].matchinvite)
	charwrite(np,"eventalerts",g.players[index].eventalerts)
	charwrite(np,"mapsound",g.players[index].mapsound)
	charwrite(np,"tokentransfer",g.players[index].tokentransfer)
	charwrite(np,"authreq",g.players[index].authreq)
	charwrite(np,"votenotify",g.players[index].votenotify)
	charwrite(np,"motorhistory",g.players[index].motorhistory)
	charwrite(np,"headhits",g.players[index].headhits)
	charwrite(np,"headshots",g.players[index].headshots)
	charwrite(np,"leghits",g.players[index].leghits)
	charwrite(np,"legshots",g.players[index].legshots)

	charwrite(np,"istyping",g.players[index].istyping)
	charwrite(np,"chestpickupnotify",g.players[index].chestpickupnotify)



	charwrite(np,"fainttime",g.players[index].fainttimer.elapsed)
	if g.players[index].faint: 	charwrite(np,"faint","")
	else:
		file_delete("chars/"+g.players[index].name+"/faint.usr")
		file_delete("chars/"+g.players[index].name+"/fainttime.usr")
	if not g.players[index].hidden: charwrite(np,"lastactive",str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))


	charwrite(np,"mapmessage",g.players[index].mapmessage)
	charwrite(np,"groupmessage",g.players[index].groupmessage)
	charwrite(np,"groupinvitation",g.players[index].groupinvitation)
	charwrite(np,"communityinvitation",g.players[index].communityinvitation)

	charwrite(np,"pmmessage",g.players[index].pmmessage)
	charwrite(np,"friendmessage",g.players[index].friendmessage)
	charwrite(np,"voicemessage",g.players[index].voicemessage)
	charwrite(np,"voicemessage2",g.players[index].voicemessage2)
	charwrite(np,"matchmessage",g.players[index].matchmessage)
	charwrite(np,"teammessage",g.players[index].teammessage)
	charwrite(np,"friendonlinemessage",g.players[index].friendonlinemessage)
	charwrite(np,"playerkills",g.players[index].playerkills)
	charwrite(np,"playerdeaths",g.players[index].playerdeaths)
	charwrite(np,"botkills",g.players[index].botkills)
	charwrite(np,"botdeaths",g.players[index].botdeaths)
	charwrite(np,"flag",g.players[index].flag)
	charwrite(np,"zhtoken",g.players[index].zhtoken)
	charwrite(np,"eventpoint",g.players[index].eventpoint)
	charwrite(np,"currenteventpoint",g.players[index].currenteventpoint)
	charwriteb(np,"task_data",pickle.dumps(g.players[index].task_data))
	charwrite(np,"matchteam",g.players[index].matchteam)
	charwrite(np,"joinedmatch",g.players[index].joinedmatch)
	charwrite(np,"matchmode",g.players[index].matchmode)

	charwrite(np,"lang",g.players[index].lang)
	charwrite(np,"y",g.players[index].y)
	charwrite(np,"z",g.players[index].z)
	try:
		f=open("chars/"+g.players[index].name+"/banned.usr","wb")
		f.write(pickle.dumps(g.players[index].matchbanned))
		f.close()
	except: pass
	charwrite(np,"map",g.players[index].map)
	charwrite(np,"gender",g.players[index].gender)
	charwrite(np,"status",g.players[index].status)

	charwrite(np,"blockvoice3",g.players[index].blockvoice3)
	charwrite(np,"hidden",("1" if g.players[index].hidden else "0"))

	charwrite(np,"langchan",g.players[index].langchan)
	charwrite(np,"shieldhitchance",g.players[index].shieldhitchance)
	charwrite(np,"helmethitchance",g.players[index].helmethitchance)
	charwrite(np,"lasthelmethitchance",g.players[index].lasthelmethitchance)
	charwrite(np,"chesttoken",g.players[index].chesttoken)


	charwrite(np,"health",g.players[index].health)
	charwrite(np,"corpse_bomb",g.players[index].corpse_bomb)
	charwrite(np,"scorepoint",g.players[index].scorepoint)
	charwrite(np,"scorerank",g.players[index].scorerank)

	charwrite(np,"facing",g.players[index].facing)
	charwriteb(np,"inventory",pickle.dumps(g.players[index].inv))
	charwriteb(np,"storeinventory",pickle.dumps(g.players[index].storeinv))
	charwriteb(np,"ammo",pickle.dumps(g.players[index].ammo))
	charwriteb(np,"current_char",pickle.dumps(g.players[index].current_char))
	charwriteb(np,"tokenplayers",pickle.dumps(g.players[index].tokenplayers))
	charwriteb(np,"silenced",pickle.dumps(g.players[index].silenced))
	charwriteb(np,"bought_chars",pickle.dumps(g.players[index].bought_chars))
	charwriteb(np,"pendingfriendlist",pickle.dumps(g.players[index].pendingfriendlist))
	charwriteb(np,"blocks",pickle.dumps(g.players[index].blocks))

	charwriteb(np,"groupinvitations",pickle.dumps(g.players[index].groupinvitations))
	charwriteb(np,"communityinvitations",pickle.dumps(g.players[index].communityinvitations))

	charwriteb(np,"friendlist",pickle.dumps(g.players[index].friendlist))
g.save_char=save_char
def save_all_chars():
	for i in range(len(g.players)):
	
		save_char(i)
		
	save_matches()
	save_chests()
	save_electrics()
	save_corpses()
	save_votes()
	save_tickets()
	save_barricades()
	save_ladders()
	save_rain()
	save_mines()
	save_timebombs()
	save_zks()

	save_motors()
	save_bikes()
	save_npcs()
	save_timeditems()
	save_groups()
	save_communitys()

	save_group_bases()
	save_zombies()
	save_items()
	save_flags()
g.save_all_chars=save_all_chars
def send_plus(excluding_name,packet,channel,r=True):
	for i in range(len(g.players)):
	
		if(excluding_name!=g.players[i].name):
		
			if(r==True):
				g.n.send_reliable(g.players[i].peer_id,packet,channel)
			else:
				g.n.send_reliable(g.players[i].peer_id,packet,channel)
		
	
def send_plus2(excluding_name,packet,channel,r=True):
	for i in range(len(g.players)):
	
		if(excluding_name!=g.players[i].name):
		
			if(r==True):
				g.n.send_reliable(g.players[i].peer_id,packet,channel)
			else:
				g.n.send_unreliable(g.players[i].peer_id,packet,channel)
		
	

g.send_plus=send_plus
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

	
g.play=play
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
		
	
g.move_player=move_player
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
		
	
g.move_player2=move_player2

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

		
		
	

g.update_map=update_map
def get_map_data(mapname):
	if(not file_exists("maps/"+mapname+".map")):
	
		return "That map does not exist."
		
	f=open("maps/"+mapname+".map","r")
	ret=f.read()
	f.close()
	if(ret=="" or ret=="\n"):
	
		return "Empty map."
		
	return ret
	
def remove_from_server(ind2=-1,force=False):

	if g.players[ind2].flag>0:
		for f in range(g.players[ind2].flag): spawn_flag(g.players[ind2].x, g.players[ind2].y, g.players[ind2].z, g.players[ind2].map, g.players[ind2].matchteam)
		g.players[ind2].flag=0


	for bomb in g.timebombs:
		if not force and not g.players[ind2].blockoffline and g.players[ind2].distancecheck(bomb.x,bomb.y,bomb.z)<=50 and bomb.map==g.players[ind2].map:
			g.players[ind2].blockoffline=True
			g.players[ind2].blockofflinetimer.restart()
			return

	for base in g.group_bases:
		if not force and g.players[ind2].map=="basement"+base.name+base.mapappend:
			move_player(ind2,base.x,base.y,base.z,base.map)
	if(not force and ind2>-1) :
		try: save_char(ind2)
		except: pass
		for m in g.matches:
			if 1:
				m.removeplayertimer.restart()
		if not g.players[ind2].hidden:
			for i in g.players:
				if i.friendonlinemessage==1 and i.name in g.players[ind2].friendlist: g.n.send_reliable(i.peer_id,"offline "+str(g.players[ind2].x)+" "+str(g.players[ind2].y)+" "+str(g.players[ind2].z)+" "+g.players[ind2].name+" "+g.players[ind2].map,0)
				else: g.n.send_reliable(i.peer_id,"offline2 "+str(g.players[ind2].x)+" "+str(g.players[ind2].y)+" "+str(g.players[ind2].z)+" "+g.players[ind2].name+" "+g.players[ind2].map,0)
	if ind2>-1:
		g.players[ind2]=None
		g.players.pop(ind2)
	
g.remove_from_server=remove_from_server
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
	
g.get_nearest_player=get_nearest_player
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
	
g.get_nearest_zombie=get_nearest_zombie

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
	
g.get_nearest_npc=get_nearest_npc
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
	
g.get_nearest_npc2=get_nearest_npc2


def setupserver():
	g.wdata["mkek_jng90"]="2000 norm"
	g.wdata["dragunov_psl"]="1000 norm"

	g.wdata["knife"]="1000 norm"
	g.wdata["stick"]="180 norm"
	g.wdata["wooden_sword"]="1200 norm"
	g.wdata["stone_sword"]="1000 norm"
	g.wdata["feet"]="500 norm"
	g.wdata["punch"]="300 norm"
	g.wdata["diamond_sword"]="800 norm"

	g.wdata["claw"]="800 norm"
	g.wdata["mkek_mpt76k"]="130 auto"
	g.wdata["m4"]="120 auto"

	g.wdata["mkek_yavuz16"]="120 norm"
	g.wdata["gsg5"]="1500 norm"

	g.wdata["fnhfnp40"]="170 norm"
	g.wdata["fnhfnp45"]="140 norm"
	g.wdata["berettaM9"]="170 norm"
	g.wdata["KelTecP318"]="120 norm"

	g.wdata["S&WModel66"]="420 norm"

	g.wdata["colt1911"]="270 norm"
	g.wdata["IthicaM37"]="1500 norm"
	g.wdata["maverick88"]="200 norm"

	g.wdata["MosinNagant"]="1500 norm"

	
def requires_ammo(w):
	try:
		guns.index(w)
		return True
	except:
		return False
	
g.requires_ammo=requires_ammo
def get_max_ammo(w):
	if(w=="mkek_jng90"):
		return 2
	if(w=="dragunov_psl"):
		return 3

	if(w=="mkek_mpt76k"):
		return 20
	if(w=="m4"):
		return 30

	if(w=="mkek_yavuz16"):
		return 10
	if(w=="gsg5"):
		return 15

	if(w=="fnhfnp40"):
		return 14
	if(w=="fnhfnp45"):
		return 15
	if(w=="berettaM9"):
		return 16
	if(w=="KelTecP318"):
		return 20


	if(w=="S&WModel66"):
		return 6

	if(w=="colt1911"):
		return 7

	if(w=="IthicaM37"):
		return 3
	if(w=="maverick88"):
		return 6

	if(w=="MosinNagant"):
		return 5

	return -1
	
g.get_max_ammo=get_max_ammo
def get_ammotype(w):
	if w=="mkek_jng90":
		return "7.62x51mm"
	if w=="dragunov_psl":
		return "7.62x51mm"

	if w=="mkek_mpt76k" or w=="m4":
		return "5.56x45mm"
	if w=="mkek_yavuz16":
		return "9mm"
	if w=="gsg5":
		return "22_LR_Long_Rifle"

	if w=="fnhfnp40":
		return "40S&W"
	if w=="fnhfnp45":
		return "45_ACP"
	if w=="KelTecP318":
		return "45_ACP"

	if w=="berettaM9":
		return "9mm"

	if w=="S&WModel66":
		return "357_magnum"

	if w=="colt1911":
		return "45_ACP"

	if w=="IthicaM37":
		return "12_gauge"
	if w=="maverick88":
		return "12_gauge"

	if w=="MosinNagant":
		return "7.62x54mmR"

	return -1
g.get_ammotype=get_ammotype
def get_reloadtime(weapon):
	if(weapon=="mkek_jng90"):
	
		return 3000
		
	if(weapon=="dragunov_psl"):
	
		return 5000
		

	if(weapon=="mkek_mpt76k"):
	
		return 3000
		
	if(weapon=="m4"):
	
		return 4000
		

	if(weapon=="mkek_yavuz16"):
	
		return 2000
		
	if(weapon=="gsg5"):
	
		return 3500
		

	if(weapon=="KelTecP318"):
	
		return 2000
		

	if(weapon=="fnhfnp40"):
	
		return 3000
		
	if(weapon=="fnhfnp45"):
	
		return 3000
		
	if(weapon=="berettaM9"):
	
		return 2200
		


	if(weapon=="S&WModel66"):
	
		return 2000
		



	if(weapon=="colt1911"):
	
		return 4000
		

	if(weapon=="IthicaM37"):
	
		return 4000
		
	if(weapon=="maverick88"):
	
		return 3200
		

	if(weapon=="MosinNagant"):
	
		return 4800
		

	else:
		return -1
	
g.get_reloadtime=get_reloadtime
class my_list(list):
	def find(self, val):
		for i, x in enumerate(self):
			if x==val:
				return i
		return -1
def sort_descending(input_list):
	return sorted(input_list, reverse=True)

def convert_to_list(arr):
	if len(arr) == 0:
		return ""
	
	processed = []
	for name in arr:
		index = get_player_index_from(name)
		# Oyuncu sunucuda değilse VEYA sunucudaysa ama 'hidden' değeri True ise offline göster
		if index == -1 or g.players[index].hidden:
			processed.append(name + ", offline")
		else:
			processed.append(name + ", online")
	
	if len(processed) == 1:
		return processed[0]
	
	# Listeyi formatla: "isim1, isim2 ve isim3"
	return ", ".join(processed[:-1]) + " and " + processed[-1]

def convert_to_list2(arr):
	list=""
	if len(arr)==0:
		return "no one"
	if len(arr)==1:
		if get_player_index_from(arr[0])==-1: arr[0]=arr[0]+""
		else: arr[0]=arr[0]+""

		return arr[0]
	for i in range(len(arr)):

		if i==len(arr)-1:
			list+=" and "+arr[i]
		else:
			list+=arr[i]+", "
	return list

def send_serverbox(peerid, mode=0, maxlength=-1, autosend=0, keypresses=-1, sendtext="server_box", text="enter text"):
	send_reliable(peerid, "input +=1"+str(mode)+"+=1"+str(maxlength)+"+=1"+str(autosend)+"+=1"+str(keypresses)+"+=1"+str(sendtext)+"+=1"+str(text), 0)
def get_leader_hit_player(b):
	if b.hitby!="":
		i=getpc(b.hitby)
		if i is not None:
			p=i
			if get_tile_at(p.x,p.y,0,p.map)=="hardwood": return p
	if b.matchteam=="red":
		for p in g.players:
			if b.m.redleader in p.hitby2:
				i=getpc(p.name)
				if i is not None:
					p=i
					if get_tile_at(p.x,p.y,0,p.map)=="hardwood": return p

		for p in g.npcs:
			if b.m.redleader in p.hitby2:
				i=getpc(p.name)
				if i is not None:
					p=i
					if get_tile_at(p.x,p.y,0,p.map)=="hardwood": return p


	if b.matchteam=="blue":
		for p in g.players:
			if b.m.blueleader in p.hitby2:
				i=getpc(p.name)
				if i is not None:
					p=i
					if get_tile_at(p.x,p.y,0,p.map)=="hardwood": return p

		for p in g.npcs:
			if b.m.redleader in p.hitby2:
				i=getpc(p.name)
				if i is not None:
					p=i
					if get_tile_at(p.x,p.y,0,p.map)=="hardwood": return p

	return None
g.get_leader_hit_player=get_leader_hit_player
g.server_menu=server_menu
store_data=[]
def load_store_data(filename="store.txt"):
	data = []

	try:
		with open(filename, 'r') as file:
			for line in file:
				item_info = line.strip().split(':')
				if len(item_info) == 4:
					item_dict = {
						"name": item_info[0],
						"price": item_info[1],
						"category": item_info[2],
						"description": item_info[3]
					}
					data.append(item_dict)

	except FileNotFoundError:
		return {}

	return data
event_store_data=[]
def load_event_store_data(filename="event_store.txt"):
	data = []

	try:
		with open(filename, 'r') as file:
			for line in file:
				item_info = line.strip().split(':')
				if len(item_info) == 3:
					item_dict = {
						"name": item_info[0],
						"price": item_info[1],
						"description": item_info[2]
					}
					data.append(item_dict)

	except FileNotFoundError:
		return {}

	return data

def save_matches():
	with open("matches.dat","wb") as f:
		f.write(pickle.dumps(g.matches))
def load_matches():
	with open("matches.dat","rb") as f:
		try: g.matches=pickle.loads(f.read())
		except: pass
	for m in g.matches: m.removeplayertimer.restart()
def save_chests():
	with open("chesttimer.txt","w") as f: f.write(str(chesttimer.elapsed))
	with open("tasktimer.txt","w") as f: f.write(str(tasktimer.elapsed))
	with open("task.txt","w") as f: f.write(str(g.task))
	with open("survivestage.txt","w") as f: f.write(str(survivestage))
	with open("survivetime.txt","w") as f: f.write(str(survivetimer.elapsed))
	with open("freedomsurvivor.txt","w") as f: f.write(str(g.freedomsurvivor))
	with open("chests.dat","wb") as f:
		f.write(pickle.dumps(g.chests))
def load_chests():
	with open("chests.dat","rb") as f:
		try: g.chests=pickle.loads(f.read())
		except: pass
	if file_exists("chesttimer.txt"):
		with open("chesttimer.txt","r") as f: chesttimer.elapsed=int(f.read())
	if file_exists("survivestage.txt"):
		with open("survivestage.txt","r") as f: survivestage=int(f.read())
	if file_exists("freedomsurvivor.txt"):
		with open("freedomsurvivor.txt","r") as f: g.freedomsurvivor=str(f.read())

	if file_exists("survivetime.txt"):
		with open("survivetime.txt","r") as f: survivetimer.elapsed=int(f.read())

	if file_exists("tasktimer.txt"):
		with open("tasktimer.txt","r") as f: tasktimer.elapsed=int(f.read())
	if file_exists("task.txt"):
		with open("task.txt","r") as f: g.task=int(f.read())

def save_electrics():
	with open("electrics.dat","wb") as f:
		f.write(pickle.dumps(g.electrics))
def load_electrics():
	with open("electrics.dat","rb") as f:
		try: g.electrics=pickle.loads(f.read())
		except: pass
	for e in g.electrics:
		e.mid=spawn_moving_sound("electricty.ogg",e.x,e.y,e.z,e.map,"",100)
def save_corpses():
	with open("corpses.dat","wb") as f:
		f.write(pickle.dumps(g.corpses))
def load_corpses():
	with open("corpses.dat","rb") as f:
		try: g.corpses=pickle.loads(f.read())
		except: pass
def save_tickets():
	with open("tickets.dat","wb") as f:
		f.write(pickle.dumps(g.tickets))
def save_votes():
	with open("votes.dat","wb") as f:
		f.write(pickle.dumps(g.votes))
def save_rain():
	with open("rain.dat","wb") as f:
		ls=[g.rain,g.rainstarttimer,g.rainstarttime,g.raintime,g.rainvoltimer,g.rainvoltime,g.rainvolume,g.raintimer]
		f.write(pickle.dumps(ls))
def save_ladders():
	with open("ladders.dat","wb") as f:
		f.write(pickle.dumps(g.ladders))
def save_barricades():
	with open("barricades.dat","wb") as f:
		f.write(pickle.dumps(g.barricades))
def load_rain():
	with open("rain.dat","rb") as f:
		ls=pickle.loads(f.read())
		g.rain=ls[0]
		g.rainstarttimer=ls[1]
		g.rainstarttime=ls[2]
		g.raintime=ls[3]
		g.rainvoltimer=ls[4]
		g.rainvoltime=ls[5]
		g.rainvolume=ls[6]
		g.raintimer=ls[7]
def load_ladders():
	with open("ladders.dat","rb") as f:
		g.ladders=pickle.loads(f.read())
def load_barricades():
	with open("barricades.dat","rb") as f:
		g.barricades=pickle.loads(f.read())

def load_tickets():
	with open("tickets.dat","rb") as f:
		g.tickets=pickle.loads(f.read())
	for ticket in g.tickets:
		if "closetimer" not in ticket.keys(): ticket["closetimer"]=timer()
def load_votes():
	with open("votes.dat","rb") as f:
		g.votes=pickle.loads(f.read())
	# NEW: Initialize 'comments' attribute for older loaded polls if it doesn't exist
	for v in g.votes:
		if not hasattr(v,"stick"): v.stick=False
		if not hasattr(v,"comments"): v.comments=[] # NEW: Ensure comments list exists for old data
        
def save_timebombs():
	with open("timebombs.dat","wb") as f:
		f.write(pickle.dumps(g.timebombs))
def load_timebombs():
	with open("timebombs.dat","rb") as f:
		g.timebombs=pickle.loads(f.read())
def save_zks():
	with open("zks.dat","wb") as f:
		f.write(pickle.dumps(g.zks))
def load_zks():
	with open("zks.dat","rb") as f:
		g.zks=pickle.loads(f.read())

def save_mines():
	with open("mines.dat","wb") as f:
		f.write(pickle.dumps(g.mines))
def load_mines():
	with open("mines.dat","rb") as f:
		g.mines=pickle.loads(f.read())
def save_bikes():
	with open("bikes.dat","wb") as f:
		f.write(pickle.dumps(g.bikes))
def load_bikes():
	with open("bikes.dat","rb") as f:
		g.bikes=pickle.loads(f.read())


def save_motors():
	with open("motors.dat","wb") as f:
		f.write(pickle.dumps(g.motors))
def load_motors():
	with open("motors.dat","rb") as f:
		g.motors=pickle.loads(f.read())
	for m in g.motors:
		if m.running: m.running=False; m.pitch=100

def save_npcs():
	with open("npcs.dat","wb") as f:
		f.write(pickle.dumps(g.npcs))
def load_npcs():
	with open("npcs.dat","rb") as f:
		g.npcs=pickle.loads(f.read())
	for n in g.npcs:
		if not hasattr(n,"tokentimer"): n.tokentimer=timer()
		if not hasattr(n,"scoretimer"): n.scoretimer=timer()
		if not hasattr(n,"hidden"): n.hidden=False
def save_zombies():
	with open("zombies.dat","wb") as f:
		f.write(pickle.dumps(g.zombies))
def load_zombies():
	with open("zombies.dat","rb") as f:
		g.zombies=pickle.loads(f.read())
def save_timeditems():
	with open("timeditems.dat","wb") as f:
		f.write(pickle.dumps(g.timeditems))
def load_timeditems():
	with open("timeditems.dat","rb") as f:
		g.timeditems=pickle.loads(f.read())
def save_groups():
	with open("groups.dat","wb") as f:
		f.write(pickle.dumps(g.groups))
def load_groups():
	with open("groups.dat","rb") as f:
		g.groups=pickle.loads(f.read())
	for group in g.groups:
		if not hasattr(group,"freedomhit"): group.freedomhit=1
		if not hasattr(group,"zhtoken"): group.zhtoken=0
		if not hasattr(group,"donations"): group.donations=""
		if not hasattr(group,"actions"): group.actions=""
		if not hasattr(group,"announcement"): group.announcement=""
	for item in g.groups:
		if not hasattr(item, "join_requests"): item.join_requests=[]
def save_communitys():
	with open("communitys.dat","wb") as f:
		f.write(pickle.dumps(g.communitys))
def load_communitys():
	with open("communitys.dat","rb") as f:
		g.communitys=pickle.loads(f.read())
	for community in g.communitys:
		if not hasattr(community,"actions"): community.actions=""
		if not hasattr(community,"announcement"): community.announcement=""
	for item in g.communitys:
		if not hasattr(item, "join_requests"): item.join_requests=[]

def save_group_bases():
	with open("group_bases.dat","wb") as f:
		f.write(pickle.dumps(g.group_bases))
def load_group_bases():
	with open("group_bases.dat","rb") as f:
		g.group_bases=pickle.loads(f.read())
	for base in g.group_bases:
		if not hasattr(base,"mapappend"): base.mapappend=""
		if not hasattr(base,"ammo"): base.ammo=10
		if not hasattr(base,"firetimer"): base.firetimer=timer()
		if not hasattr(base,"password"): base.password=""
		if not hasattr(base,"doorontimer"): base.doorontimer=timer()
		if not hasattr(base,"dooropening"): base.dooropening=False
		if not hasattr(base,"chestlog"): base.chestlog=""
def save_items():
	with open("items.dat","wb") as f:
		f.write(pickle.dumps(g.items))
def load_items():
	with open("items.dat","rb") as f:
		g.items=pickle.loads(f.read())
	for item in g.items:
		if not hasattr(item,"yoursents"): item.yoursents=[]
def save_flags():
	with open("flags.dat","wb") as f:
		f.write(pickle.dumps(g.flags))
def load_flags():
	with open("flags.dat","rb") as f:
		g.flags=pickle.loads(f.read())

def playmoving(x,y,z,map,snd,obj):
	msoundid=spawn_moving_sound(snd+".ogg",x,y,z,map,obj.name,playmoving=True)
	obj.msounds.append(msoundid)
	obj.msoundtimers.append(timer())
g.playmoving=playmoving
def playmoving2(x,y,z,map,snd,obj):
	msoundid=spawn_moving_sound(snd+".ogg",x,y,z,map,obj.name,sendowner=False,playmoving=True)
	obj.msounds.append(msoundid)
	obj.msoundtimers.append(timer())
g.playmoving2=playmoving2

def get_friend_count(p):
	index=get_player_index_from(p)
	ret=0
	for pl in g.players:
		if not pl.hidden and pl.name in g.players[index].friendlist: ret+=1
	return ret
def find_ticket_by_title(title):
	for ticket in g.tickets:
		if ticket["title"]==title: return ticket
def find_ticket_by_id(id):
	for ticket in g.tickets:
		if ticket["id"]==id: return ticket
from datetime import datetime,timedelta


def get_datetime_difference(input_date):
	date_format = "%Y-%m-%d %H:%M:%S"
	try: input_datetime = datetime.strptime(input_date, date_format)
	except: return ""
	current_datetime = datetime.now()
	time_difference = int((current_datetime - input_datetime).total_seconds())

	time_units = {
		'millennium': 31536000000,
		'century': 3153600000,
		'decade': 315360000,
		'year': 31536000,
		'month': 2592000,
		'day': 86400,
		'hour': 3600,
		'minute': 60,
		'second': 1,
	}

	result = []
	for unit_name, unit_seconds in time_units.items():
		unit_value = time_difference // unit_seconds
		time_difference %= unit_seconds

		if unit_value:
			if unit_name == 'millennium':
				result.append(f'{unit_value} {unit_name if unit_value == 1 else "millennia"}')
			elif unit_name == 'century':
				result.append(f'{unit_value} {unit_name if unit_value == 1 else "centuries"}')
			else:
				result.append(f'{unit_value} {unit_name if unit_value == 1 else unit_name + "s"}')

	if len(result) > 1:
		result[-1] = 'and ' + result[-1]

	return ', '.join(result)
def convert_minutes_to_datetime_object(minutes):
	current_datetime = datetime.now()

	new_datetime = current_datetime + timedelta(minutes=minutes)

	return new_datetime
def send_yesno_question(peer,message):
	global e
	g.n.send_reliable(peer,"yesno "+message,0)
	while True:
		netloop()
		if isinstance(e.message,str):
			if e.message.startswith("yesno "): return e.message.replace("yesno ","")
		gameloops()
def strtobool(b):
	if b=="True": return True
	else: return False
def removefriendadd(m,index):
	for pl in g.players[index].friendlist:
		m.add(pl,pl)
g.removefriendadd=removefriendadd
def offlinepm(player,player2,message):
	dir="chars/"+player
	if os.path.isfile(dir+"/pmdata.usr"): pmdata=pickle.loads(file_get_contents(dir+"/pmdata.usr","rb"))
	else: pmdata={}
	pmdata[player2]=message
	file_put_contents(dir+"/pmdata.usr",pickle.dumps(pmdata),"wb")
def offlinestaff(player,message):
	dir="chars/"+player
	if os.path.isfile(dir+"/staffdata.usr"): staffdata=pickle.loads(file_get_contents(dir+"/staffdata.usr","rb"))
	else: staffdata={}
#	staffdata[player2]=message
	file_put_contents(dir+"/staffdata.usr",pickle.dumps(staffdata),"wb")

import urllib.parse,requests
def url_encode(url):
	return urllib.parse.quote(url)
def url_decode(url):
	return urllib.parse.unquote(url)
def url_get(url):
	try:
		raw_response=requests.get(url)
		return raw_response.text
	except:
		return "HTTP Request error!"

BOT_KEY = "8358511609:AAEtEE3Dvp4zVxfGzbT4XnF9fl8yu8qwnEE"   # kendi bot token'iniz
ADMIN_IDS = ["1577175242","350483154","5669845199","7978393633"]   # birden fazla admin id buraya eklenebilir
API_ENDPOINT = f"https://api.telegram.org/bot{BOT_KEY}/sendMessage"

def make_request(endpoint, payload):
    try:
        response_data = requests.post(endpoint, data=payload)
        return response_data.text
    except Exception as err:
        return str(err)

def notify_admins(message_text):
    feedback = []
    for admin_uid in ADMIN_IDS:
        answer = make_request(API_ENDPOINT, {
            "chat_id": admin_uid,
            "text": message_text
        })
        feedback.append(answer)
    return feedback

BOT_KEY2 = "8358511609:AAEtEE3Dvp4zVxfGzbT4XnF9fl8yu8qwnEE"   # kendi bot token'iniz
ADMIN_IDS2 = ["1577175242"]   # birden fazla admin id buraya eklenebilir
API_ENDPOINT2 = f"https://api.telegram.org/bot{BOT_KEY2}/sendMessage"

def make_request2(endpoint, payload):
    try:
        response_data = requests.post(endpoint, data=payload)
        return response_data.text
    except Exception as err:
        return str(err)

def notify_admins2(message_text):
    feedback = []
    for admin_uid in ADMIN_IDS2:
        answer = make_request2(API_ENDPOINT2, {
            "chat_id": admin_uid,
            "text": message_text
        })
        feedback.append(answer)
    return feedback

def send_mail(user, sub, mailmess):
	user=url_encode(user)
	mailmess=url_encode(mailmess)
	sub=url_encode(sub)
	res = url_get("https://nbmstudios.com/mailsend.php?id=nbmcantsend&mail="+user+"&mess="+mailmess+"&sub="+sub)
	return res

def load_mailbans():
	if file_exists("mailbans.txt"):
		g.mailbans=[m.lower().strip() for m in file_get_contents("mailbans.txt").split("\n") if m.strip()]
	else:
		g.mailbans=[]

def save_mailbans():
	file_put_contents("mailbans.txt","\n".join(g.mailbans))

def is_mailbanned(mail):
	return mail.lower().strip() in g.mailbans

def ban_mail(mail):
	m=mail.lower().strip()
	if m and m not in g.mailbans:
		g.mailbans.append(m)
		save_mailbans()

_tempmail_domains=set()
def load_tempmail_domains():
	global _tempmail_domains
	if file_exists("tempmail_domains.txt"):
		_tempmail_domains={d.lower().strip() for d in file_get_contents("tempmail_domains.txt").split("\n") if d.strip()}

def is_tempmail(mail):
	if "@" not in mail:
		return False
	domain=mail.split("@")[-1].lower().strip()
	return domain in _tempmail_domains
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
g.chestadd=chestadd
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
g.corpseadd=corpseadd

import math

def ms_to_readable_time(milliseconds):
	milliseconds = math.floor(milliseconds)
	seconds = math.floor((milliseconds / 1000) % 60)
	minutes = math.floor((milliseconds / (1000 * 60)) % 60)
	hours = math.floor((milliseconds / (1000 * 60 * 60)) % 24)
	days = math.floor(milliseconds / (1000 * 60 * 60 * 24))
	
	time_components = []

	if days >= 365:
		years = days // 365
		time_components.append(f"{years} {plural(years, 'year', 'years')}")
		days %= 365

	if days >= 30:
		months = days // 30
		time_components.append(f"{months} {plural(months, 'month', 'months')}")
		days %= 30

	if days >= 7:
		weeks = days // 7
		time_components.append(f"{weeks} {plural(weeks, 'week', 'weeks')}")
		days %= 7

	if days > 0:
		time_components.append(f"{days} {plural(days, 'day', 'days')}")

	if hours > 0:
		time_components.append(f"{hours} {plural(hours, 'hour', 'hours')}")

	if minutes > 0:
		time_components.append(f"{minutes} {plural(minutes, 'minute', 'minutes')}")

	time_components.append(f"{seconds} {plural(seconds, 'second', 'seconds')}")

	return ", ".join(time_components)
def ms_to_readable_time2(milliseconds):
	milliseconds = math.floor(milliseconds*1000)
	seconds = math.floor((milliseconds / 1000) % 60)
	minutes = math.floor((milliseconds / (1000 * 60)) % 60)
	hours = math.floor((milliseconds / (1000 * 60 * 60)) % 24)
	days = math.floor(milliseconds / (1000 * 60 * 60 * 24))
	
	time_components = []

	if days >= 365:
		years = days // 365
		time_components.append(f"{years} {plural(years, 'year', 'years')}")
		days %= 365

	if days >= 30:
		months = days // 30
		time_components.append(f"{months} {plural(months, 'month', 'months')}")
		days %= 30

	if days >= 7:
		weeks = days // 7
		time_components.append(f"{weeks} {plural(weeks, 'week', 'weeks')}")
		days %= 7

	if days > 0:
		time_components.append(f"{days} {plural(days, 'day', 'days')}")

	if hours > 0:
		time_components.append(f"{hours} {plural(hours, 'hour', 'hours')}")

	if minutes > 0:
		time_components.append(f"{minutes} {plural(minutes, 'minute', 'minutes')}")

	time_components.append(f"{seconds} {plural(seconds, 'second', 'seconds')}")

	return ", ".join(time_components)


def plural(n, singular, plural):
	if n == 1:
		return singular
	return plural
def get_group(name):
	for grp in g.groups:
		if grp.name==name: return grp
g.get_group=get_group

def get_community(name):
	for grp in g.communitys:
		if grp.name==name: return grp
g.get_community=get_community

def randomstring(length=10):
	temp="abcdefghijklmnopqrstuvwxyz1234567890"
	ret=""
	for i in range(length):
		ret=ret+temp[random(0, (len(temp)-1))]
	return ret

def time_difference_exceeds_24_hours(dt1, dt2):
	time_difference = abs(dt1 - dt2)
	return time_difference > timedelta(hours=24)
def time_difference_exceeds_1_week(dt1, dt2):
	time_difference = abs(dt1 - dt2)
	return time_difference > timedelta(days=7)

def time_difference_exceeds_2_hours(dt1, dt2):
	time_difference = abs(dt1 - dt2)
	return time_difference > timedelta(hours=2)

import os
import shutil
import time

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
	if pack=="bronze_token_pack": return 1000
	if pack=="silver_token_pack": return 1400
	if pack=="gold_token_pack": return 2600
	if pack=="platinum_token_pack": return 3000
	if pack=="diamond_token_pack": return 6200
	if pack=="master_token_pack": return 13000
def match_exists(owner):
	for m in g.matches:
		if m.owner==owner: return True
	return False
g.match_exists=match_exists
def url_post2(url,params):
	Thread(target=url_post,args=(url,params,)).start()
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
def minutes_to_timestamp(minutes):
	current_time = int(tm.time())
	future_time = current_time + (minutes * 60)  
	return int(future_time)  
def ticketcheck():
	for ticket in g.tickets:
		if not ticket["closed"] and not ticket["pending"] and ticket["closetimer"].elapsed>172800000:
			if 1:
				ticket["closed"]=True
				ticket["messages"]+="\nThis ticket was closed because it had no activity in the last 2 days in "+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				ticket["lastupdate"]=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				adminsend("the ticket "+ticket["title"]+" was closed because it had no activity in the last 2 days")
				notify_admins("zero hour assault, the ticket "+ticket["title"]+" was closed because it had no activity in the last 2 days")
				getmail=file_get_contents("chars/"+ticket["owner"]+"/mail.usr")
				send_mail(getmail,"your ticket "+ticket["title"]+" has been closed","Hello "+ticket["owner"]+"<br>your ticket "+ticket["title"]+" has been closed because it had no activity in the last 2 days<br>Below is all the ticket messages:<br>"+ticket["messages"]+"<br>If you have more questions or need help, please create a support ticket again from the game or contact us at contact@nbmstudios.com<br>regards,<br>Nbm studios team")

				if 1:
					ind=get_player_index_from(ticket["owner"])
					if ind>-1:
						g.n.send_reliable(g.players[ind].peer_id,"Your ticket with id "+ticket["id"]+" is updated, please check!",0)
						g.n.send_reliable(g.players[ind].peer_id,"play_s misc304.ogg",0)
					else:
						file_put_contents("chars/"+ticket["owner"]+"/ticketinform.usr","Your ticket with "+ticket["id"]+" is updated, please check!")

def is_enabled_ticket_mail(user):
	if not file_exists("chars/"+user+"/ticketmail.usr"): return True
	ret=file_get_contents("chars/"+user+"/ticketmail.usr")
	if ret=="1": return True
	return False
def get_current_date():
	return str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
def randomstring(length=10):
	temp="abcdefghijklmnopqrstuvwxyz1234567890"
	ret=""
	for i in range(length):
		ret=ret+temp[random(0, (len(temp)-1))]
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
g.play2=play2
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
g.votes=[]
def votecheck():
	for v in g.votes:
		if not hasattr(v,"stick"): v.stick=False
		if not v.ended and v.timer.elapsed>86400000 and not v.stick:
			v.ended=True
			for p in g.players:
				if p.votenotify==1:
					g.n.send_reliable(p.peer_id,v.owner+"'s vote has been ended",2)
					g.n.send_reliable(p.peer_id,"play_s misc162.ogg",0)

g.get_current_date=get_current_date
import os

def get_long_name_for_size_unit(unit):
    unit_names = {
        'B': 'Bytes',
        'KB': 'Kilobytes',
        'MB': 'Megabytes',
        'GB': 'Gigabytes',
        'TB': 'Terabytes',
        'PB': 'Petabytes',
        'EB': 'Exabytes',
        'ZB': 'Zettabytes',
        'YB': 'Yottabytes'
    }
    return unit_names.get(unit, unit)

def get_file_size(filename, return_long_unit=False):
    try:
        size = os.path.getsize(filename)
        return convert_size(size, return_long_unit)
    except:
        return "File size not available"

def get_file_size_b(filename, return_long_unit=False):
    try:
        size = os.path.getsize(filename)
        if return_long_unit:
            unit = get_long_name_for_size_unit('B')
        else:
            unit = 'B'
        return f"{size} {unit}"
    except:
        return "File size not available"

def get_file_size_bit(filename, return_long_unit=False):
    try:
        size = os.path.getsize(filename) * 8
        if return_long_unit:
            unit = get_long_name_for_size_unit('b')
        else:
            unit = 'b'
        return f"{size} {unit}"
    except:
        return "File size not available"

def convert_size(size, return_long_unit=False):
    bytes = int(size)
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    unit_index = 0
    while bytes >= 1024 and unit_index < len(units) - 1:
        bytes /= 1024
        unit_index += 1
    unit = units[unit_index]

    if return_long_unit:
        unit = get_long_name_for_size_unit(unit)

    return f"{round(bytes, 2)} {unit}"

def convert_size_bit(size, return_long_unit=False):
    bytes = int(size / 8)
    units = ['b', 'Kb', 'Mb', 'Gb', 'Tb', 'Pb', 'Eb', 'Zb', 'Yb']
    unit_index = 0
    while bytes >= 1024 and unit_index < len(units) - 1:
        bytes /= 1024
        unit_index += 1
    unit = units[unit_index]

    if return_long_unit:
        unit = get_long_name_for_size_unit(unit)

    return f"{round(bytes, 2)} {unit}"
def play_delay(snd,x,y,z,map,time_wait):
	time_wait=500
	temptimer=timer()
	def func():
		while 1:
			time.sleep(0.001)
			if temptimer.elapsed>time_wait: play(snd,x,y,z,map); return
	Thread(target=func).start()
g.play_delay=play_delay
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
def get_language_used_count(lng):
	ret=0
	for char in os.listdir("chars"):
		if file_get_contents("chars/"+char+"/lang.usr")==lng: ret+=1
		if file_get_contents("chars/"+char+"/lang.usr")=="" and lng=="English": ret+=1
	return str(ret)
def get_open_ticket_count():
	ret=0
	for ticket in g.tickets:
		if not ticket["pending"] and not ticket["closed"]: ret+=1
	return ret
def get_closed_ticket_count():
	ret=0
	for ticket in g.tickets:
		if ticket["closed"]: ret+=1
	return ret
def get_pending_ticket_count():
	ret=0
	for ticket in g.tickets:
		if ticket["pending"]: ret+=1
	return ret
import os
import shutil
import time
from datetime import datetime
import zipfile  # ZIP dosyaları oluşturmak için gerekli

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
if __name__=="__main__":
	main()