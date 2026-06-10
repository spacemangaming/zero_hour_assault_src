# --- AUTOMATIC PATH RESOLUTION AND MODULE REGISTRATION ---
import sys
import os

CLIENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Resolve the absolute project root directory
if getattr(sys, 'frozen', False):
	script_dir = os.path.dirname(sys.executable)
else:
	current_dir = CLIENT_DIR
	if os.path.basename(current_dir) == "zero_hour_assault":
		script_dir = os.path.dirname(os.path.dirname(current_dir))
	elif os.path.basename(current_dir) == "src":
		script_dir = os.path.dirname(current_dir)
	else:
		script_dir = current_dir

# Add project root to DLL search paths on Windows FIRST before importing submodules
if sys.platform == "win32":
	os.environ["PATH"] = script_dir + os.pathsep + os.environ["PATH"]
if hasattr(os, "add_dll_directory"):
	try:
		os.add_dll_directory(script_dir)
	except Exception:
		pass

subdirs = ['core', 'audio', 'ui', 'net', 'utils']
for subdir in subdirs:
	p = os.path.join(CLIENT_DIR, subdir)
	if os.path.isdir(p) and p not in sys.path:
		sys.path.insert(0, p)

# --- AUTOMATIC TOP MODULE BINDER ---
import types
import zh_client_core
import zh_client_net
import zh_client_gameplay
import zh_client_ui

submodules = [
	zh_client_core, zh_client_net, zh_client_gameplay, zh_client_ui
]
shared_globals_top = {}
for mod in submodules:
	for name, val in mod.__dict__.items():
		if not name.startswith('__') and not isinstance(val, types.ModuleType):
			shared_globals_top[name] = val
sys.modules[__name__].__dict__.update(shared_globals_top)

os.chdir(script_dir)

# Ensure Python can import modules from the package directory
sys.path.insert(0, os.path.join(script_dir, "src"))
sys.path.insert(0, os.path.join(script_dir, "src", "zero_hour_assault"))



import psutil
import math
import os
import traceback
while os.path.isfile("zero_hour_assault1.exe"):
	try: os.remove("zero_hour_assault1.exe")
	except: pass
import pyaudio
import ctypes
from threading import Thread
CHUNK_SIZE=960
FORMAT=pyaudio.paInt16
CHANNELS=1
guns=[]
doorclose="doorclose\ndoorclose2\ndoorclose3\ndoorclose4\ndoorclose5\ndoorclose6"
dooropen="dooropen\ndooropen2\ndooropen3\ndooropen4\ndooropen5\ndooropen6\ndooropen7\ndooropen8\ndooropen9\ndooropen10\ndooropen11\ndooropen12\ndooropen13"
tiletypes="""appartment
balloon
bare
bathtub
bathtub2
bathtub3
beam
bleacher
bleacher2
branch
branch2
bridge
bridge2
broken_glass
chair
carpet
carpet2
carpet3
carpet4
cave
cement
cement2
cement3
cement4
ceramic
ceramic2
ceramic3
ceramic4
clay
cloth
concrete
concrete14
concrete2
concrete24
concrete25
concrete26
concrete27
concrete28
concrete3
concrete4
concrete5
concrete6
concrete7
concrete8
concrete9
debris
deck
deepsand
deepsnow
deepwater
diamond
dirt
dirt2
dirt3
dirt4
dirt5
dirt6
dirt7
dirt8
dirt9
generic
glass
glass2
glass3
grass
grass2
grass3
grass4
grate
gravel
gravel2
gravel3
gravel4
gravel5
gravel6
hardwood
hardwood2
hardwood3
hardwood4
hardwood5
ice
ice1
metal
metal10
metal11
metal12
metal13
metal14
metal15
metal16
metal17
metal2
metal3
metal4
metal5
metal6
metal7
metal8
metal9
metalpipe
mud
sand
water
wetdirt
wood
wood10
wood2
wood3
wood4
wood5
wood6
wood7
wood8
wood9
woodenfloor"""
tiletypes+="""
wallair
wallbank
wallbarrel
wallbars
wallbeaulon
wallbigmetal
wallbigmetal2
wallboard
wallbody
wallborder
wallbranch
wallbrick
wallbrick2
wallbrick3
wallbrush
wallbrush2
wallbrushtangle
wallbucket
wallbuilding
wallbuilding2
wallbuilding3
wallbuilding4
wallbuilding5
wallbuilding6
wallbuilding7
wallbushleaves
wallbushleaves2
wallbushleaves3
wallbushleaves4
wallcar
wallcar2
wallcar3
wallcardboard
wallcardboardbox
wallcelle
wallcelle2
wallcelle3
wallcelle4
wallcelle5
wallchain
wallchest
wallchest2
wallclock
wallclock2
wallcloth
wallclothing
wallcomputer
wallcone
wallcontainer
wallcorpse
wallcorpse2
wallcouch
wallcounter
wallcrate
walldebris
walldebris2
walldebris3
walldebris4
walldebris5
walldesk
walldesk2
walldesk3
walldesk4
walldestroy
walldestroy2
walldestroy3
walldestroy4
walldestroy5
walldirt
walldirt2
walldoor
walldoor2
walldoor3
walldrown
wallfence
wallfence2
wallfence3
wallfence4
wallfence5
wallfence6
wallfence7
wallfence8
wallfoliage
wallfurniture
wallgate
wallgeneric
wallgeneric2
wallglass
wallglass2
wallglass3
wallglass4
wallglass5
wallglass6
wallglass7
wallglass8
wallglass9
wallglass10
wallglass11
wallglass12
wallgrass
wallgrass2
wallgrass2reverb
wallgrassdirt
wallhard
wallhit1
wallhit2
wallhit3
wallhit4
wallhit5
wallhit6
wallhit7
wallhit8
wallhit9
wallmedal
wallmedal2
wallmedal3
wallmedal4
wallmedaldebris
wallmedalsheet
wallmedalsheet2
wallmetal
wallmetal2
wallmetal3
wallmetal4
wallmetal5
wallmetal6
wallmetal7
wallmetal8
wallmetal9
wallmetal10
wallmetal11
wallmetal12
wallmetal13
wallmetal14
wallmetal15
wallmetal16
wallmetal17
wallmetal18
wallmetal19
wallmetal20
wallmetal21
wallmetal22
wallmetal23
wallmetalglass
wallmud
wallobject
wallplastic
wallpot
wallpunch
wallrail
wallrockdirt
wallrocks
wallrocks2
wallrocks3
wallscreen
wallsilence
wallslam
wallsofa
wallspaceship
wallspaceshipreverb
wallstand
wallstone
wallstone2
wallstreet
walltable
walltile
walltree
wallunderwater
wallunderwater2
wallwater
wallwood
wallwood2
wallwood3
wallwood4
wallwood5
wallwood6
wallwood7
wallwood8
wallwood9
wallwood10
wallwood11
wallwood12
wallwood13
wallwood14
wallwood15
wallwood16
wallwood17
wallwood18
wallwoodcrate
wallwooddoor
wallwoodpile"""
from internet import url_get
from file_directories import file_get_contents
srctypes="airport\namb1\namb2\namb3\namb4\namb5\namb6\namb7\namb8\namb9\namb10\namb11\namb12\namb13\namb14\namb15\namb16\namb17\namb18\nbeach\nbirds\nbirds2\nbirds3\nbirds4\nbirds5\nbirds6\nbirds7\ncafe\ncafe2\ncafetaria\ncafetaria2\ncafetaria3\ncave\nceiling_fan\nceiling_fan2\ncity_ambience\ncity_ambience2\ncity_ambience3\ncity_ambience4\ndark\ndark2\ndark3\ndark4\ndarkforest\ndarkforest2\ndeepocean\ndepartment_store\ndepartment_store2\ndesert\ndesert_ambience_day_1\ndesert_ambience_day_2\ndesert_ambience_day_3\ndesert_ambience_evening_1\ndesert_ambience_mix\ndesert_ambience_morning_1\ndesert_ambience_night_1\ndesert_ambience_night_2\ndesert_ambience_night_3\ndesert_wind_day\ndesert_wind_evening\ndesert_wind_morning\ndesert_wind_morning_2\ndesert_wind_night\ndesert_wind_whistle\ndesertnight\ndesktop\ndungeon\ngeneric\ngrave_yart\ngrocery_store\nhaunted_forest\nhelicopter\nhell_place\nlobby_ambience\nmotorengine\nmountain\nmountain2\nmountain3\nmountain4\nnbmambience\nnbmambience2\nnbmambience3\nnbmambience4\nnbmambience5\nnbmambience6\nocean\nocean2\npet_shop\nrain_forest\nship\nsrc1\nsrc2\nsrc3\nsrc4\nsrc5\nsrc6\nsrc7\nsrc8\nstreet\nstreet2\nstreet3\nsuper_market\nsuper_market2\nsuper_market3\nsuper_market4\nsuper_market5\ntrophical_ocean\ntrophical_ocean2\ntrophical_ocean3\nunder_water\nunder_water2\nwallclock\nwallclock2\nwallmetal17\nwarfare\nwater_ambience\nwater_ambience2"
import webbrowser
import time
import pyaudio
import opuslib
from security import string_hash
from random import randint as random
p=pyaudio.PyAudio()
pstream=None



from buffer import lastbuffer, quote
from buffer import firstbuffer
from map import gct
from moving_sound_client_handler import createmsound, updatemsound, destroymsound, destroy_all_msounds,msoundloop
from sign import signcheck,signloop
from file_directories import file_exists,file_put_contents
from key_hold import key_holding
from variable_management import string_to_number, string_contains
from map import get_tile_at, get_staircase_at
from map import playcamera, cameramove, playstep
from map import clear_map
from rotation import snapleft, getdir, snapright, dir_to_string, turnleft, turnright, move, vector
from inventory import cycle_inv
from map import get_zone_at
from constants import *
from rotation import calculate_theta
from source import sourcecheckloop
from map import move_player
from network import event_receive, network_event
from network import event_disconnect



from player import get_player_index

import globals as g
import constants
for pyd in g.pyds:
	try:
		if os.path.isfile(pyd+".1"): os.remove(pyd+".1")
		if os.path.isfile("_internal\\"+pyd+".1"): os.remove("_internal\\"+pyd+".1")
	except: pass
g.pa=p
from rotation import get_3d_distance,north,east,south,west
from rotation import calculate_x_y_angle
from rotation import calculate_x_y_string
from player import remove_player
from player import remove_all_players
from Miscellaneous import clipboard_copy_text, clipboard_read_text

from dlg import dlg

from variable_management import string_is_digits, get_characters, string_is_alphanumeric
from variable_management import string_replace
from map import load_map
from inventory import useitem, dropitem, set_favoriitem,set_favoriitem2
from inventory import get_item_count
import pickle,json
from events import key_released
from events import process_events
from events import key_up
from player import spawn_player
from player import update_player_coordinates, update_player_coordinates2
from pygame.locals import *
from events import key_down
from door import doorcheckloop

from events import key_pressed
from events import key_down

import sys
from Miscellaneous import show_game_window, is_game_window_active
from audio import set_sound_storage, set_sound_decryption_key
from buffer import create_buffer, add_buffer_item, bufferleft, bufferright, prevbufferitem, nextbufferitem, topbufferitem, bottombufferitem,copy_buffer_item,translate_buffer_item

from file_directories import directory_exists, directory_create, directory_delete
from dlgplay import dlgplay
from constants import DIRECTORY_APPDATA

from variable_management import string_len
from variable_management import string_split
from variable_management import string_trim_left

import menu
import pygame

import sound

from source import destroy_all_sources
from downloader import download_file
import updater
from key_hold import key_holding
from variable_management import string_left

m=menu.menu()

parachute_sound=None
falling_sound=None
inside_bus_handle=None
bus_audio_state={"stopped":False,"doors_open":False,"moving":False,"speed":0}

from speech import speak
from input import get_input
from ticket_dialogs import ticket_dialog, create_ticket_dialog, ticket_dialog2
import wx
g.app=wx.App()
from translation import translate as _, google_get_translation_languages, google_translate
from timer import timer
recordvoicetimer=timer()
opus_encoder=None
import copy
windowchecktimer=timer()
try:
	import vlc, pafy
except Exception:
	vlc = None
	pafy = None
	print("[game] WARNING: vlc/pafy not available (libvlc.dll missing?). YouTube audio player disabled.")
import requests
from net import login, create
from net import login, netaddress
from net import login, netport


weaponswitchtimer=timer()
turntimer=timer()
aimtimer=timer()
import speech,sound
compiled=getattr(sys,"frozen",False)
sys.excepthook=handle_exception
import sound
mousetimer=timer()
from map import spawn_platform, remove_platform, update_platform, spawn_zone, remove_zone
import shutil
from file_directories import file_delete
from source import pause_all_sources, resume_all_sources
msoundtimer=timer()
cannotdraw=[]
tilechecktimer=timer()
from downloader import download_file
ctimer=timer()
ctimer2=timer()
from security import file_encrypt
turnsoundtimer=timer()
rainfadeintimer=timer()
bikehorntimer=timer()
	
	
g.game=game

	
	
	
	
	



#	if(g.sd.exists("playcanlogo")):
#		g.playcanlogo=g.sd.readn("playcanlogo")
	
g.writeprefs=writeprefs
	

voice_temp_counter=0


				
			
		
	

g.netloop=netloop
g.reset=reset
	
	
g.left_button_down=False
middle_button_down=False
g.right_button_down=False
g.left_button_pressed=False
middle_button_pressed=False
g.right_button_pressed=False
MOUSE_X=0
MOUSE_Y=0
OLD_MOUSE_X=0
OLD_MOUSE_Y=0
MOUSE_Xreal=0
MOUSE_Yreal=0
scrollup=False
scrolldown=False


altimer=timer()
g.mainloop=mainloop

			
		
	

				
			
		
	
g.fallloop=fallloop
		
	
		
	
g.fallingloop=fallingloop
def int_to_bool(num):
	if(num==1):
	
		return True
		
	return False
	
def bool_to_string_to_number(b):
	if(b==True):
	
		return 1
		
	return 0
	
chtimer=timer()
autotracktimer=timer()
biketimer=timer()
anticheattimer=timer()
			
		


	
		
	
		
	

g.p1=[]
g.p2=[]
g.p3=[]
g.p4=[]
g.pcleartimer=timer()
g.serverside_menu=serverside_menu





g.reinit_voicechat=reinit_voicechat

def tell_where(x, y, z, saycoords=True):
	x=round(x); y=round(y); z=round(z)
	if x==-1 or y==-1:
		speak("you are not tracking anything")
		return
	tracktext=""
	if 1:
		if 1:
			locstring=calculate_x_y_string(calculate_x_y_angle(g.me.x, g.me.y, x, y, g.facing))
			dist=int(get_3d_distance(g.me.x, g.me.y, g.me.z, x, y, z))
			if saycoords:
				if z>g.me.z:
					tracktext="above, "
				elif z<g.me.z:
					tracktext="below, "
				speak(tracktext+" "+locstring+" ("+str(dist)+" tiles away) at "+str(x)+", "+str(y)+", "+str(z))
				tracktext=""



if 1:
	if 1:
		if 1:
			def buffertransmenu():
				m.reset(True)
				menu.setupmenu()
				m.callback2=mainloop
				items=google_get_translation_languages()
				for item in items: m.add_item_tts(item,item)
				mres=m.run("Select the source language you want to use for translating buffer messages")
				process_events()
				if mres==0: return
				g.buffersourcelang=m.get_item_name(mres)
				writeprefs()
				m.reset(True)
				menu.setupmenu()
				m.callback2=mainloop
				items=google_get_translation_languages()
				for item in items: m.add_item_tts(item,item)
				mres=m.run("Select the target language you want to use for translating buffer messages")
				process_events()
				if mres==0: return
				g.buffertargetlang=m.get_item_name(mres)
				writeprefs()
			def sendtransmenu():
				m.reset(True)
				menu.setupmenu()
				m.callback2=mainloop
				items=google_get_translation_languages()
				for item in items: m.add_item_tts(item,item)
				mres=m.run("Select the source language you want to use for translating sent messages")
				process_events()
				if mres==0: return
				g.sendsourcelang=m.get_item_name(mres)
				writeprefs()
				m.reset(True)
				menu.setupmenu()
				m.callback2=mainloop
				items=google_get_translation_languages()
				for item in items: m.add_item_tts(item,item)
				mres=m.run("Select the target language you want to use for translating sent messages")
				process_events()
				if mres==0: return
				g.sendtargetlang=m.get_item_name(mres)
				writeprefs()

			def yesno(q):
				m.reset(True)
				menu.setupmenu()
				m.callback2=mainloop
				m.add_item_tts("yes","yes")
				m.add_item_tts("no","no")
				mres=m.run(q)
				process_events()
				if mres==0:
					return "no"
				else:
					choice=m.get_item_name(mres)
					return choice
import os
import shutil




			
		

g.mouse_update=mouse_update
g.get_rain_sound=get_rain_sound


g.get_rain_sound_camera=get_rain_sound_camera
g.oldfacing=0
g.fallcheck=fallcheck
import sys
import os

# The WMI library is only needed on Windows, so we handle the import carefully.
if sys.platform == 'win32':
	try:
		import wmi
	except ImportError:
		wmi = None

import ctypes
import os
import time

anticheat_lib = ctypes.CDLL("anticheat.dll")

if 1:
	anticheat_lib.anticheat_init.argtypes = []
	anticheat_lib.anticheat_init.restype = None

	anticheat_lib.anticheat_check.argtypes = []
	anticheat_lib.anticheat_check.restype = None

	anticheat_lib.is_memory_scan_detected.argtypes = []
	anticheat_lib.is_memory_scan_detected.restype = ctypes.c_bool

	anticheat_lib.is_speed_hack_detected.argtypes = []
	anticheat_lib.is_speed_hack_detected.restype = ctypes.c_bool

	anticheat_lib.anticheat_deinit.argtypes = []
	anticheat_lib.anticheat_deinit.restype = None


anticheat_lib.anticheat_init()

is_memory_scan_detected = anticheat_lib.is_memory_scan_detected
is_speed_hack_detected = anticheat_lib.is_speed_hack_detected
anticheat_check=anticheat_lib.anticheat_check
import hashlib

import os
import re
import sys
import time
import ctypes
import platform
import subprocess
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from functools import partial
from typing import List, Set, Dict

# Platform-specific imports
if platform.system() == "Windows":
	try:
		import wmi
		import pywintypes
	except ImportError:
		wmi = None
		pywintypes = None
else:
	wmi = None
	pywintypes = None

try:
	import psutil
except ImportError:
	psutil = None
# --- AUTOMATIC BOTTOM MODULE BINDER ---
shared_globals_bottom = {}
for name, val in sys.modules[__name__].__dict__.items():
	if not name.startswith('__'):
		shared_globals_bottom[name] = val
for mod in submodules:
	mod.__dict__.update(shared_globals_bottom)

if __name__=="__main__": main()
