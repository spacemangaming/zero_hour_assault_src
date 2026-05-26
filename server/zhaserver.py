# --- AUTOMATIC PATH RESOLUTION AND MODULE REGISTRATION ---
import sys
import os
MODULES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules'))
subdirs = ['core', 'net', 'entities', 'utils']
for subdir in subdirs:
    p = os.path.join(MODULES_DIR, subdir)
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)
if MODULES_DIR not in sys.path:
    sys.path.insert(0, MODULES_DIR)

# --- AUTOMATIC TOP MODULE BINDER ---
import types
import zh_utils
import zh_auth
import zh_persistence
import zh_gameplay
import zh_core
import zh_net_chat
import zh_net_others
import zh_net_gameplay_1
import zh_net_gameplay_2
import zh_net_gameplay_3
import zh_net_gameplay_4
import zh_net_gameplay_5
import zh_net_gameplay_6

submodules = [
    zh_utils, zh_auth, zh_persistence, zh_gameplay, zh_core,
    zh_net_chat, zh_net_others,
    zh_net_gameplay_1, zh_net_gameplay_2, zh_net_gameplay_3,
    zh_net_gameplay_4, zh_net_gameplay_5, zh_net_gameplay_6
]
shared_globals_top = {}
for mod in submodules:
    for name, val in mod.__dict__.items():
        if not name.startswith('__') and not isinstance(val, types.ModuleType):
            shared_globals_top[name] = val
sys.modules[__name__].__dict__.update(shared_globals_top)

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
import transit



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
from performance_monitor import PerformanceMonitor



from item import itemloop, itembeeploop
from loot import lootloop
from flag import flagloop, spawn_flag
from item import spawn_item
g.server_menu=server_menu

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
duplicatewalltimer=timer()
g.gameloops=gameloops

e=None




				
			
		
		
		
g.netloop=netloop




		
	
g.send_reliable=send_reliable
	
	
g.get_player_index=get_player_index
g.get_player_index_fromnpc=get_player_index_fromnpc
g.getpc=getpc

g.get_player_index_from=get_player_index_from
	
	
g.save_char=save_char
g.save_all_chars=save_all_chars
		
	
		
	

g.send_plus=send_plus
g.send_plus2=send_plus2

	
g.play=play
		
	
g.move_player=move_player
		
	
g.move_player2=move_player2


		
		
	

g.update_map=update_map
	
	
g.remove_from_server=remove_from_server
	
g.get_nearest_player=get_nearest_player
	
g.get_nearest_zombie=get_nearest_zombie

	
g.get_nearest_npc=get_nearest_npc
	
g.get_nearest_npc2=get_nearest_npc2



	
	
g.requires_ammo=requires_ammo
	
g.get_max_ammo=get_max_ammo
g.get_ammotype=get_ammotype
	
g.get_reloadtime=get_reloadtime



g.get_leader_hit_player=get_leader_hit_player
g.server_menu=server_menu
store_data=[]
event_store_data=[]



        






g.playmoving=playmoving
g.playmoving2=playmoving2

from datetime import datetime,timedelta


g.removefriendadd=removefriendadd

import urllib.parse,requests

BOT_KEY = "8358511609:AAEtEE3Dvp4zVxfGzbT4XnF9fl8yu8qwnEE"   # kendi bot token'iniz
ADMIN_IDS = ["1577175242","350483154","5669845199","7978393633"]   # birden fazla admin id buraya eklenebilir
API_ENDPOINT = f"https://api.telegram.org/bot{BOT_KEY}/sendMessage"



BOT_KEY2 = "8358511609:AAEtEE3Dvp4zVxfGzbT4XnF9fl8yu8qwnEE"   # kendi bot token'iniz
ADMIN_IDS2 = ["1577175242"]   # birden fazla admin id buraya eklenebilir
API_ENDPOINT2 = f"https://api.telegram.org/bot{BOT_KEY2}/sendMessage"








_tempmail_domains=set()

g.chestadd=chestadd
g.corpseadd=corpseadd

import math



g.get_group=get_group

g.get_community=get_community




import os
import shutil
import time

        

g.match_exists=match_exists




g.play2=play2

g.votes=[]

g.get_current_date=get_current_date
import os






g.play_delay=play_delay
import os
import shutil
import time
from datetime import datetime
import zipfile  # ZIP dosyaları oluşturmak için gerekli

# --- AUTOMATIC BOTTOM MODULE BINDER ---
shared_globals_bottom = {}
for name, val in sys.modules[__name__].__dict__.items():
    if not name.startswith('__'):
        shared_globals_bottom[name] = val
for mod in submodules:
    mod.__dict__.update(shared_globals_bottom)

if __name__=="__main__":
	main()
