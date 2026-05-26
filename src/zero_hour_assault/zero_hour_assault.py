import os
import sys
os.environ["PAFY_BACKEND"] = "internal"

if getattr(sys, 'frozen', False):
	script_dir = os.path.dirname(sys.executable)
else:
	current_dir = os.path.dirname(os.path.abspath(__file__))
	if os.path.basename(current_dir) == "zero_hour_assault":
		script_dir = os.path.dirname(os.path.dirname(current_dir))
	elif os.path.basename(current_dir) == "src":
		script_dir = os.path.dirname(current_dir)
	else:
		script_dir = current_dir

os.chdir(script_dir)

# Ensure Python can import modules from the package directory
sys.path.insert(0, os.path.join(script_dir, "src"))
sys.path.insert(0, os.path.join(script_dir, "src", "zero_hour_assault"))

# Add project root to DLL search paths on Windows
if sys.platform == "win32":
	os.environ["PATH"] = script_dir + os.pathsep + os.environ["PATH"]
if hasattr(os, "add_dll_directory"):
	try:
		os.add_dll_directory(script_dir)
	except Exception:
		pass



import psutil
import math
import os
import traceback
if os.path.isfile("sounds1.dat"):
	os.remove("sounds.dat")
	os.rename("sounds1.dat","sounds.dat")
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

class binput:
	def __init__(self, names, input):
		self.indata=input
		self.innames=names
	def num(self, val):
		ix=self.innames.index(val)
		if ix>-1:
			return string_to_number(self.indata[ix])
		return -1
	def str(self, val):
		ix=self.innames.index(val)
		if ix>-1:
			return str(self.indata[ix])
		return -1
	def str(self, val):
		ix=self.innames.index(val)
		if ix>-1:
			return self.indata[ix]
		return ""
def builder_input(spec):
	if spec == "":
		return None
	spec=spec.replace("\t", "", -1).replace("\n", "\n", -1)
	items=delinear(spec)
	names=[]
	vals=[]
	for i in range(len(items)):
		p=string_split(items[i], "=", False)
		names.append(p[0])
		tmp=get_input(p[1])
		if tmp == "":
			speak("canceled")
			return None
		vals.append(tmp)
	res=binput(names, vals)
	return res
m=menu.menu()
def delinear(a): return string_split(a,"\n",True)

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
import vlc,pafy
import requests
from net import login, create
from net import login, netaddress
from net import login, netport


weaponswitchtimer=timer()
turntimer=timer()
aimtimer=timer()
import speech,sound
compiled=getattr(sys,"frozen",False)
def handle_exception(exc_type, exc_value, exc_traceback):
	if not compiled:
		with open("errors.log","a") as f: 		traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)


	ctypes.windll.user32.MessageBoxW(None,"A critical error has occurred that prevented the program from continue executing. Please send the error information you will see after pressing enter to the developers to Identify the cause of the error and fix it.","Error!",16)
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
def main():
	if directory_exists("lang")==False:
		directory_create("lang")
	if file_exists("lang/.lng"): file_delete("lang/.lng")
	jawscheck()
	show_game_window("Zero hour assault "+g.ver)
	g.delay(500)
	speak("loading")
#	time.sleep(2)
	global opus_encoder,pstream
	if not file_exists(os.getenv("appdata")+"/alsoft.ini"):
		f=open(os.getenv("appdata")+"/alsoft.ini","w")
		f.write("""[General]
sources=100000
slots=100000

[decoder]
hq-mode=true""")
		f.close()
	if 1:
		langs=os.listdir("lang")
		for lang in langs:
			if file_get_contents("lang/"+lang,"r","utf-8")!="": file_encrypt("lang/"+lang,g.langkey)
	if compiled and check_if_already_running():
		dlg("You cannot open the game twice")
		pygame.quit()
		ctypes.windll.kernel32.ExitProcess(0)
	set_sound_storage("sounds.dat")
	set_sound_decryption_key("asdasdasdasasdasdsa1231232132112321321$$1231231231221321312%*]9CfY%!yfo?3.m]C16(VW:?DB:70v4n7d`tht}jiylhC%L&;ix(Y;9BB?`k-hYhR^=n%C;#kykxV?)GFbzC5x6R<-W?o<c|xQw")

	try:
		# Disabled for clean public source distribution
		# updater.check()
		# updater.sndcheck()
		pass
	except: pass
	g.distpool.behind_pitch_decrease=5
	g.distpool.max_distance=2000
	g.p.behind_pitch_decrease=-5
	g.weapons.append("punch")
	g.weapons2.append("feet")
	if (not directory_exists(DIRECTORY_APPDATA+"/nbm-studios")):
		directory_create(DIRECTORY_APPDATA+"/nbm-studios")
	if(not directory_exists(DIRECTORY_APPDATA+"/nbm-studios/zero_hour_assault")):
		directory_create(DIRECTORY_APPDATA+"/nbm-studios/zero_hour_assault")
	readprefs()

	readprefs()
	g.bnext=sound.sound();g.bpos=sound.sound()
	g.bpos.load("buffer1.ogg")
	g.bpos.player.alhrtf=True
	g.bnext.load("buffer2.ogg")

	g.bnext.player.alhrtf=True
	g.wind=sound.sound()
	g.wind.load("fallingwithoutparachute.ogg")
	g.wind.player.alhrtf=False
	g.wind.player.stationary=True
	g.wind.volume=-100
	g.wind.play_looped()
	g.flash=sound.sound()
	g.flash.load("flashbangbeep.ogg")
	g.flash.player.alhrtf=False
	g.flash.player.stationary=True
	g.flash.volume=-100
	g.flash.play_looped()


	if g.buffersave==1 and file_exists(DIRECTORY_APPDATA+"/nbm-studios/zero_hour_assault/buffers3.dat"):
		try: g.buffers=pickle.loads(file_get_contents(DIRECTORY_APPDATA+"/nbm-studios/zero_hour_assault/buffers3.dat","rb"))
		except: pass
	if g.buffersave==0:
		file_delete(DIRECTORY_APPDATA+"/nbm-studios/zero_hour_assault/buffers3.dat")
	items_found=False
	for buf in g.buffers:
		if buf.name=="items": items_found=True
	if not items_found: g.buffers=[]
	create_buffer("all")
	create_buffer("General_Chats")

	create_buffer("match messages")
	create_buffer("map messages")
	create_buffer("group messages")
	create_buffer("community messages")

	create_buffer("team messages")
	create_buffer("friend messages")
	create_buffer("notifications")
	create_buffer("group notifications")
	create_buffer("community notifications")

	create_buffer("online and offline notifications")
	create_buffer("items")
	create_buffer("misc")

	create_buffer("near notifications")
	create_buffer("death and kill notifications")

	create_buffer("admin messages")

	for buf in g.buffers:
		if not hasattr(buf,"muted"): buf.muted=False
	opus_encoder = opuslib.Encoder(g.samplerate, CHANNELS, opuslib.APPLICATION_VOIP)
	CHUNK_SIZE=round(20*(g.samplerate/1000))
	try:
		pstream=p.open(format=FORMAT, channels=1, rate=g.samplerate, input=True, frames_per_buffer=CHUNK_SIZE, input_device_index=g.inputdevice)
	except: pass
	opus_encoder.bitrate=g.bitrate
	opus_encoder.complexity=0


	if is_vm():
		ctypes.windll.user32.MessageBoxW(None,"This game cannot run in virtual machines.","Error",16); sys.exit()
	if file_get_hash_sha256(("anticheat.dll" if not hasattr(sys,"frozen") else "_internal/anticheat.dll"))!="bff167f0933774f2de3e9f408ed119dd050ec0dfbebda5354dc6ea9be5ea1141":
		ctypes.windll.user32.MessageBoxW(None,"Game files have been tampered with. Please redownload the game.","Error",16); ctypes.windll.kernel32.ExitProcess(0)
	getmotd()
	#get_input(" ","",True,False)
	pygame.display.set_caption("Zero hour assault "+g.ver)
#	if(g.playcanlogo==1):

	speak("Forge Your Legend!")
	g.p.play_stationary("misc329.ogg",False)
	g.delay(4000)
	g.p.play_stationary("gamedooropen.ogg",False)
	if g.rules3==0:
		g.p.play_stationary("misc81.ogg",False)
		m.reset(True)
		m.click_sound=""
		m.enter_sound=""

		m.allow_escape=False
		f=open("rules.txt","r",encoding="utf-8")
		readme=f.read()
		f.close()
		lines=readme.split("\n")
		for line in lines: m.add_item_tts(line,line,False)
		m.add_item_tts("I have read and not accept the above rules.","noagree")

		m.add_item_tts("I have read and accept the above rules.","agree")
		mres=m.run("Welcome to Zero Hour Assault. The rules of the game are presented below. Read the rules and indicate whether you agree or disagree. At the bottom there is a button to accept or reject the rules.",True)
		if m.get_item_name(mres)=="agree": speak("You accepted the rules. Welcome to the game."); g.p.play_stationary("misc80.ogg",False); g.delay(2000); g.rules3=1; writeprefs()
		if m.get_item_name(mres)=="noagree": g.p.play_stationary("misc140.ogg",False); speak("Unfortunately, you cannot play the game because you do not accept the rules. Exiting the game..."); g.rules3=0; writeprefs(); g.delay(2000); sys.exit()

	writeprefs()
	if g.privacy==0:
		g.p.play_stationary("misc81.ogg",False)
		m.reset(True)
		m.click_sound=""
		m.enter_sound=""

		m.allow_escape=False
		f=open("privacy.txt","r",encoding="utf-8")
		readme=f.read()
		f.close()
		lines=readme.split("\n")
		for line in lines: m.add_item_tts(line,line,False)
		m.add_item_tts("I have read and do not accept the privacy policy above.","noagree")

		m.add_item_tts("I have read and accept the privacy policy above.","agree")
		mres=m.run("Welcome to Zero Hour Assault. The privacy policy of the game is presented below. Please read the privacy policy and indicate whether you agree or disagree. At the bottom, there is a button to accept or reject the privacy policy.",True)
		if m.get_item_name(mres)=="agree": speak("You accepted the privacy Welcome to the game."); g.p.play_stationary("misc80.ogg",False); g.delay(2000); g.privacy=1; writeprefs()
		if m.get_item_name(mres)=="noagree": g.p.play_stationary("misc140.ogg",False); speak("Unfortunately, you cannot play the game because you do not accept the privacy. Exiting the game..."); g.privacy=0; writeprefs(); g.delay(2000); sys.exit()

	writeprefs()


	if g.tutorial==0:
		m.reset(True)
		m.allow_escape=False
		m.add_item_tts("Yes, show me the readme, I want to read.","yes")
		m.add_item_tts("No, Thanks.","no")
		mres=m.run("this is the first time you are playing this game, do you want to view the readme?",True)

		if m.get_item_name(mres)=="yes": speak("Readme file is opening..."); g.tutorial=1; writeprefs(); menu.readmemenu()
		if m.get_item_name(mres)=="no": speak("Okay, well..."); g.tutorial=1; writeprefs(); menu.mainmenu()

	writeprefs()
	menu.mainmenu()
	
def game(d=True):
	constants.steam=g.steam
	constants.cache=g.cache
	if d:

		g.p1.clear()
		g.p2.clear()
		g.p3.clear()
		g.p4.clear()
	if d:
		g.inthegame=True
		g.p.play_stationary("newmenuopen3.ogg",False)
		g.p.play_stationary("misc349.ogg",False)

		g.x=False
		g.xtimer.restart()
		g.n.send_reliable(0, "spawn_player "+str(g.me.x)+" "+str(g.me.y)+" "+str(g.me.z)+" "+g.mapname+" "+g.name+" "+str(g.samplerate), 0)
		g.n.send_reliable(0,"aimmode "+str(g.aim_mode),0)
		g.n.send_reliable(0,"juharjksjkadjknjk12n3kjnkjn1j23kjnkjn12k3nknkn123kjnkn12k3nknk5nknkn32knkn1n1k1k",0)
		g.n.send_reliable(0,"drawsilent punch",0)
		g.n.send_reliable(0,"draw2silent feet",0)
		g.weapons.append("punch")
		g.w=len(g.weapons)-1
		g.weapons2.append("feet")
		g.w2=len(g.weapons2)-1

	g.n.send_reliable(0,"voicechatwho "+g.voicechatwho,0)
	g.n.send_reliable(0,"setversion "+g.ver,0)

	if g.near==0:
		g.n.send_reliable(0,"disablenear",0)
	if g.listen==0:
		g.n.send_reliable(0,"disablelisten",0)

	if g.scope==0:
		g.n.send_reliable(0,"disablescope",0)

	if g.killcounter==0:
		g.n.send_reliable(0,"disablekill",0)
	if g.near==1:
		g.n.send_reliable(0,"enablenear",0)
	if g.itembeep==0:
		g.n.send_reliable(0,"itemdisable",0)

	if g.listen==1:
		g.n.send_reliable(0,"enablelisten",0)

	if g.scope==1:
		g.n.send_reliable(0,"enablescope",0)

	if g.killcounter==1:
		g.n.send_reliable(0,"enablekill",0)
	g.n.send_reliable(0,"voicechatfriend "+str(g.voicechatfriend),0)
	g.n.send_reliable(0,"voicechatmap "+str(g.voicechatmap),0)
	g.n.send_reliable(0,"voicechatgroup "+str(g.voicechatgroup),0)

	g.n.send_reliable(0,"sameteambots "+str(g.sameteambots),0)
	g.n.send_reliable(0,"sameteamplayers "+str(g.sameteamplayers),0)
	g.n.send_reliable(0,"sound "+str(g.sound),0)
	g.n.send_reliable(0,"charvoice "+str(g.charvoice),0)

	g.n.send_reliable(0,"differentteambots "+str(g.differentteambots),0)
	g.n.send_reliable(0,"differentteamplayers "+str(g.differentteamplayers),0)
	g.n.send_reliable(0,"differentgroupplayers "+str(g.differentgroupplayers),0)
	g.n.send_reliable(0,"samegroupplayers "+str(g.differentgroupplayers),0)
	g.n.send_reliable(0,"voicechatteam "+str(g.voicechatteam),0)
	if len(g.p1)!=0:
		p1=g.p1.pop()
		p2=g.p2.pop()
		p3=g.p3.pop()
		p4=g.p4.pop()
		g.n.send_reliable(0,"mpacket "+p1,0)
		g.n.send_reliable(0,"mitems "+p3,0)
		serverside_menu(p1,p2,p3,p4)
		process_events()
	while(True):
		zeroloop()
	
g.game=game
def alt_is_down():
	if key_down(K_LALT) or key_down(K_RALT):
		return True
	return False

def shift_is_down():
	if(key_down(K_LSHIFT) or key_down(K_RSHIFT)):
	
		return True
		
	return False
	
def altdown():
	if(key_down(K_LALT) or key_down(K_RALT)):
	
		return True
		
	return False
	
def control_is_down():
	if(key_down(K_LCTRL) or key_down(K_RCTRL)):
	
		return True
		
	return False
	
def left_control_is_down():
	if(key_down(K_LCTRL)):
	
		return True
		
	return False
	
def right_control_is_down():
	if(key_down(K_RCTRL)):
	
		return True
		
	return False
	


def readprefs():
	g.sd.load()
	if (g.sd.exists("charvoice")):
		g.charvoice=g.sd.readn("charvoice")
	if (g.sd.exists("aim_mode")):
		g.aim_mode=g.sd.readn("aim_mode")

	if (g.sd.exists("sonar")):
		g.sonar=g.sd.readn("sonar")
	if (g.sd.exists("itembeep")):
		g.itembeep=g.sd.readn("itembeep")

	if (g.sd.exists("yavaslat")):
		g.yavaslat=g.sd.readn("yavaslat")

	if (g.sd.exists("sound")):
		g.sound=g.sd.readn("sound")
	if (g.sd.exists("soundcard")):
		g.soundcard=g.sd.read("soundcard")
		constants.soundcard=g.soundcard

	if (g.sd.exists("privacy")):
		g.privacy=g.sd.readn("privacy")

	if (g.sd.exists("listen")):
		g.listen=g.sd.readn("listen")
	if (g.sd.exists("sameteambots")):
		g.sameteambots=g.sd.readn("sameteambots")
	if (g.sd.exists("sameteamplayers")):
		g.sameteamplayers=g.sd.readn("sameteamplayers")
	if (g.sd.exists("differentteambots")):
		g.differentteambots=g.sd.readn("differentteambots")
	if (g.sd.exists("differentteamplayers")):
		g.differentteamplayers=g.sd.readn("differentteamplayers")
	if (g.sd.exists("differentgroupplayers")):
		g.differentgroupplayers=g.sd.readn("differentgroupplayers")
	if (g.sd.exists("samegroupplayers")):
		g.samegroupplayers=g.sd.readn("samegroupplayers")
	if (g.sd.exists("ucd")):
		g.ucd=g.sd.readn("ucd")

	if (g.sd.exists("steam2")):
		g.steam=g.sd.readn("steam2")
		constants.steam=g.steam
	if (g.sd.exists("cache")):
		g.cache=g.sd.readn("cache")
		constants.cache=g.cache

	if (g.sd.exists("qturn")):
		g.qturn=g.sd.readn("qturn")

	if (g.sd.exists("fastwalk")):
		g.fastwalk=g.sd.readn("fastwalk")

	if (g.sd.exists("rules3")):
		g.rules3=g.sd.readn("rules3")
	if (g.sd.exists("speakfacing")):
		g.speakfacing=g.sd.readn("speakfacing")
	if (g.sd.exists("charrepeat")):
		g.charrepeat=g.sd.readn("charrepeat")

	if (g.sd.exists("speakdegree")):
		g.speakdegree=g.sd.readn("speakdegree")

	if (g.sd.exists("tutorial")):
		g.tutorial=g.sd.readn("tutorial")
	if (g.sd.exists("playervolumes")):
		g.playervolumes=g.sd.read("playervolumes")

	if (g.sd.exists("mastervolume2")):
		g.mastervolume2=g.sd.readf("mastervolume2")
		g.mastervolume=g.mastervolume2
		sound.listener._set_gain(g.mastervolume2)

	if (g.sd.exists("buffersave")):
		g.buffersave=g.sd.readn("buffersave")

	if (g.sd.exists("signbeepsound")):
		g.signbeepsound=g.sd.readn("signbeepsound")

	if (g.sd.exists("mapmusicoldversion")):
		g.mapmusicoldversion=g.sd.readn("mapmusicoldversion")
	if (g.sd.exists("keytheme")):
		g.keytheme=g.sd.readn("keytheme")

	if (g.sd.exists("jcontrols")):
		g.jcontrols=json.loads(g.sd.read("jcontrols"))

	if (g.sd.exists("stopaim")):
		g.stopaim=g.sd.readn("stopaim")
	if (g.sd.exists("favoriitem")):
		g.favoriitem=g.sd.read("favoriitem")
	if (g.sd.exists("favoriitem2")):
		g.favoriitem2=g.sd.read("favoriitem2")

	if (g.sd.exists("inputdevice")):
		g.inputdevice=g.sd.readn("inputdevice")

	if (g.sd.exists("complexity")):
		g.complexity=g.sd.readn("complexity")

	if (g.sd.exists("voicechatwho")):
		g.voicechatwho=g.sd.read("voicechatwho")

	if (g.sd.exists("push")):
		g.push=g.sd.readn("push")
	if (g.sd.exists("push2")):
		g.push2=g.sd.readn("push2")

	if (g.sd.exists("lang")):
		g.lang=g.sd.read("lang")

	if (g.sd.exists("bitrate")):
		g.bitrate=g.sd.readn("bitrate")
	if (g.sd.exists("volume")):
		g.volumeg=g.sd.readn("volume")

	if (g.sd.exists("samplerate")):
		g.samplerate=g.sd.readn("samplerate")

	if (g.sd.exists("web_message")):
		g.web_message=g.sd.read("web_message")
	if (g.sd.exists("name")):
		g.name=g.sd.read("name")
	if (g.sd.exists("buffersourcelang")):
		g.buffersourcelang=g.sd.read("buffersourcelang")
	if (g.sd.exists("buffertargetlang")):
		g.buffertargetlang=g.sd.read("buffertargetlang")
	if (g.sd.exists("sendsourcelang")):
		g.sendsourcelang=g.sd.read("sendsourcelang")
	if (g.sd.exists("sendtargetlang")):
		g.sendtargetlang=g.sd.read("sendtargetlang")

	if (g.sd.exists("savemail")):
		g.savemail=g.sd.read("savemail")

	if (g.sd.exists("menumusvol")):
		g.menumusvol=g.sd.read("menumusvol")
	if g.sd.exists("g.focus0"):
		g.focus0=g.sd.read("g.focus0")
	if g.sd.exists("g.focus9"):
		g.focus9=g.sd.read("g.focus9")
	if g.sd.exists("g.focus8"):
		g.focus8=g.sd.read("g.focus8")
	if g.sd.exists("g.focus7"):
		g.focus7=g.sd.read("g.focus7")
	if g.sd.exists("g.focus6"):
		g.focus6=g.sd.read("g.focus6")
	if g.sd.exists("g.focus5"):
		g.focus5=g.sd.read("g.focus5")
	if g.sd.exists("g.focus4"):
		g.focus4=g.sd.read("g.focus4")
	if g.sd.exists("g.focus3"):
		g.focus3=g.sd.read("g.focus3")
	if g.sd.exists("g.focus2"):
		g.focus2=g.sd.read("g.focus2")

	if (g.sd.exists("near")):
		g.near=g.sd.read("near")
	if (g.sd.exists("interrupt")):
		g.interrupt=g.sd.read("interrupt")

	if(g.sd.exists("password")):
		g.password=g.sd.read("password")
	if(g.sd.exists("usehrtf")):
		g.hrtf=g.sd.readn("usehrtf")
	if(g.sd.exists("awindow")):
		g.awindow=g.sd.readn("awindow")
	if(g.sd.exists("scope")):
		g.scope=g.sd.readn("scope")

	if(g.sd.exists("musicplayinthemap")):
		g.musicplayinthemap=g.sd.readn("musicplayinthemap")


	if(g.sd.exists("turningtimeelapsing")):
		g.turningtimeelapsing=g.sd.readn("turningtimeelapsing")

	if(g.sd.exists("usesub")):
		g.usesub=g.sd.readn("usesub")

	if(g.sd.exists("killcounter")):
		g.killcounter=g.sd.readn("killcounter")

	if(g.sd.exists("onlinemsg")):
		g.onlinemsg=g.sd.readn("onlinemsg")

	if(g.sd.exists("usemouse")):
		g.usemouse=g.sd.readn("usemouse")

	if(g.sd.exists("bufferlog")):
		g.bufferlog=g.sd.readn("bufferlog")
		sound.listener.hrtf=2

#	if(g.sd.exists("playcanlogo")):
#		g.playcanlogo=g.sd.readn("playcanlogo")
	
def writeprefs():
	g.sd.add("name",g.name)
	constants.cache=g.cache
	g.sd.add("itembeep",g.itembeep)
	g.sd.add("soundcard",g.soundcard)
	g.sd.add("aim_mode",g.aim_mode)
	g.sd.add("sonar",g.sonar)
	g.sd.add("charvoice",g.charvoice)
	g.sd.add("privacy",g.privacy)

	g.sd.add("sound",g.sound)
	g.sd.add("sameteambots",g.sameteambots)
	g.sd.add("sameteamplayers",g.sameteamplayers)
	g.sd.add("differentteambots",g.differentteambots)
	g.sd.add("differentteamplayers",g.differentteamplayers)
	g.sd.add("samegroupplayers",g.samegroupplayers)
	g.sd.add("differentgroupplayers",g.differentgroupplayers)
	g.sd.add("buffersourcelang",g.buffersourcelang)
	g.sd.add("buffertargetlang",g.buffertargetlang)
	g.sd.add("sendsourcelang",g.sendsourcelang)
	g.sd.add("sendtargetlang",g.sendtargetlang)

	g.sd.add("favoriitem",g.favoriitem)
	g.sd.add("favoriitem2",g.favoriitem2)

	g.sd.add("qturn",g.qturn)
	g.sd.add("ucd",g.ucd)
	g.sd.add("yavaslat",g.yavaslat)

	g.sd.add("steam2",g.steam)
	g.sd.add("cache",g.cache)
	g.sd.add("rules3",g.rules3)
	g.sd.add("fastwalk",g.fastwalk)

	g.sd.add("speakdegree",g.speakdegree)
	g.sd.add("charrepeat",g.charrepeat)

	g.sd.add("speakfacing",g.speakfacing)

	g.sd.add("tutorial",g.tutorial)
	g.sd.add("playervolumes",g.playervolumes)

	g.sd.add("signbeepsound",g.signbeepsound)
	g.sd.add("buffersave",g.buffersave)
	g.sd.add("mastervolume2",sound.listener._get_gain())

	g.sd.add("stopaim",g.stopaim)
	g.sd.add("keytheme",g.keytheme)
	g.sd.add("voicechatteam",g.voicechatteam)
	g.sd.add("voicechatmap",g.voicechatmap)
	g.sd.add("voicechatgroup",g.voicechatgroup)

	g.sd.add("voicechatfriend",g.voicechatfriend)
	g.sd.add("bitrate",g.bitrate)
	g.sd.add("mapmusicoldversion",g.mapmusicoldversion)
	g.sd.add("inputdevice",g.inputdevice)
	g.sd.add("volume",g.volumeg)
	g.sd.add("complexity",g.complexity)
	g.sd.add("jcontrols",json.dumps(g.jcontrols))
	g.sd.add("voicechatwho",g.voicechatwho)
	g.sd.add("samplerate",g.samplerate)
	g.sd.add("lang",g.lang)
	g.sd.add("web_message",g.web_message)
	g.sd.add("listen",g.listen)
	g.sd.add("push",g.push)
	g.sd.add("push2",g.push2)
	g.sd.add("scope",g.scope)

	g.sd.add("turningtimeelapsing",g.turningtimeelapsing)
	g.sd.add("musicplayinthemap",g.musicplayinthemap)

	g.sd.add("menumusvol",g.menumusvol)
	g.sd.add("savemail",g.savemail)

	g.sd.add("password",g.password)
	g.sd.add("g.focus2", g.focus2)
	g.sd.add("g.focus3", g.focus3)
	g.sd.add("g.focus4", g.focus4)
	g.sd.add("g.focus5", g.focus5)
	g.sd.add("g.focus6", g.focus6)
	g.sd.add("g.focus7", g.focus7)
	g.sd.add("g.focus8", g.focus8)
	g.sd.add("g.focus9", g.focus9)
	g.sd.add("g.focus0", g.focus0)

	g.sd.add("interrupt",g.interrupt)
	g.sd.add("near",g.near)
	g.sd.add("onlinemsg",g.onlinemsg)
	g.sd.add("awindow",g.awindow)

	g.sd.add("usesub",g.usesub)

	g.sd.add("killcounter",g.killcounter)

	g.sd.add("usemouse",g.usemouse)

#	g.sd.add("playcanlogo",g.playcanlogo)
	g.sd.add("usehrtf",g.hrtf)
	g.sd.add("bufferlog",g.bufferlog)

	g.sd.save()
g.writeprefs=writeprefs
	
def play_for_voicechat():
	if g.vcdata is not None:
		if g.voicechat==0: g.vcdata=None; return
		vcdata=g.vcdata; g.vcdata=None
		playername=vcdata.split(b" ")[0]
		audio_data=vcdata.replace(playername+b" ",b"")
		index=get_player_index(playername.decode())
		if index>-1:
			g.players[index].audio_buffer.append(audio_data)
def play_for_voicechat2():
	if g.vcdata2 is not None:
		if g.voicechat2==0: g.vcdata2=None; return
		vcdata=g.vcdata2; g.vcdata2=None
		playername=vcdata.split(b" ")[0]
		audio_data=vcdata.replace(playername+b" ",b"")
		index=get_player_index(playername.decode())
		if index>-1:
			g.players[index].audio_buffer2.append(audio_data)

voice_temp_counter=0
def init_voicechat_player(pl):
	pl.opus_decoder = opuslib.Decoder(pl.samplerate, CHANNELS)
	pl.opus_decoder2 = opuslib.Decoder(pl.samplerate, CHANNELS)
	if not hasattr(pl, "voice_sound"): pl.voice_sound=None
	if not hasattr(pl, "voice_sound2"): pl.voice_sound2=None
	Thread(target=handle_voicechat_data,args=(pl,)).start()
	Thread(target=handle_voicechat_data2,args=(pl,)).start()

def play_voice_pcm(pl, pcm_data, second=False):
	global voice_temp_counter
	if not pcm_data:
		return
	try:
		os.makedirs(DIRECTORY_TEMP, exist_ok=True)
	except: pass
	voice_temp_counter+=1
	filename=os.path.join(DIRECTORY_TEMP, "voice_"+str(voice_temp_counter)+".wav")
	try:
		with wave.open(filename, "wb") as wav:
			wav.setnchannels(CHANNELS)
			wav.setsampwidth(2)
			wav.setframerate(pl.samplerate)
			wav.writeframes(pcm_data)
		handle_name="voice_sound2" if second else "voice_sound"
		old=getattr(pl, handle_name, None)
		if old is not None:
			try: old.close()
			except: pass
		handle=sound.sound()
		handle.load(filename)
		handle._delete_on_close=filename
		handle.player.stationary=False
		handle.volume=0
		if pl.name in g.playervolumes:
			handle.volume=round(20*math.log10(max(g.playervolumes[pl.name], 1)/100))
		setattr(pl, handle_name, handle)
		pl.position_voicechat_sound()
		handle.play()
	except:
		pass

def netloop(events=False,request=True):
	global parachute_sound,falling_sound,inside_bus_handle
	try:
		if request: g.e=g.n.request()
		if g.e.channel==5: g.vcdata=g.e.message
		if g.e.channel==6: g.vcdata2=g.e.message
	except:
		return

	if g.me.z==20 and g.parachute==True: parachute_sound.handle.volume=-1
	if g.me.z==19 and g.parachute==True: parachute_sound.handle.volume=-2
	if g.me.z==18 and g.parachute==True: parachute_sound.handle.volume=-3
	if g.me.z==17 and g.parachute==True: parachute_sound.handle.volume=-4
	if g.me.z==16 and g.parachute==True: parachute_sound.handle.volume=-5
	if g.me.z==15 and g.parachute==True: parachute_sound.handle.volume=-6
	if g.me.z==14 and g.parachute==True: parachute_sound.handle.volume=-7
	if g.me.z==13 and g.parachute==True: parachute_sound.handle.volume=-8
	if g.me.z==12 and g.parachute==True: parachute_sound.handle.volume=-9
	if g.me.z==11 and g.parachute==True: parachute_sound.handle.volume=-10
	if g.me.z==10 and g.parachute==True: parachute_sound.handle.volume=-11
	if g.me.z==9 and g.parachute==True: parachute_sound.handle.volume=-12
	if g.me.z==8 and g.parachute==True: parachute_sound.handle.volume=-13
	if g.me.z==7 and g.parachute==True: parachute_sound.handle.volume=-14
	if g.me.z==6 and g.parachute==True: parachute_sound.handle.volume=-15
	if g.me.z==5 and g.parachute==True: parachute_sound.handle.volume=-16
	if g.me.z==4 and g.parachute==True: parachute_sound.handle.volume=-17
	if g.me.z==3 and g.parachute==True: parachute_sound.handle.volume=-18
	if g.me.z==2 and g.parachute==True: parachute_sound.handle.volume=-19
	if g.me.z==1 and g.parachute==True: parachute_sound.handle.volume=-20
	if falling_sound is not None and g.falling==False and g.parachute==False:
		g.p.destroy_sound(falling_sound)
		falling_sound=None
	if falling_sound is not None and g.falling==False and g.me.z==0 and g.parachute==False:
		g.p.destroy_sound(falling_sound)
		falling_sound=None
#edited
	if g.falling==True and g.parachute==False and g.me.z!=0:
		if falling_sound==None:
			falling_sound=g.p.play_stationary("fallingwithoutparachute.ogg",True)
	if falling_sound is not None and g.parachutesoundpositife==True and g.parachutesoundtimer.elapsed>=1500:
		g.parachutesoundtimer.restart()
		g.parachutesoundpositife=False
		g.p.destroy_sound(falling_sound)
		falling_sound=None

	if g.mapname=="lobby" and g.zombie: g.zombie=False; g.walktime-=25

	if g.watching!="" and g.should_watch:
		i=get_player_index(g.watching)
		if i!=-1:
			if g.me.x!=g.players[i].x or g.me.y!=g.players[i].y or g.me.z!=g.players[i].z:
				g.me.x=g.players[i].x
				g.me.y=g.players[i].y
				g.me.z=g.players[i].z
				g.facing=g.players[i].facing
				#g.n.send_reliable(0, "move_to_a2 "+str(g.me.x)+" "+str(g.me.y)+" "+str(g.me.z)+"", 0)
				if g.mapname!="lobby": g.n.send_reliable(0, "wcoords "+str(g.me.x)+" "+str(g.me.y)+" "+str(g.me.z)+"", 0)
	if parachute_sound is not None:
		if g.p.sound_is_playing(parachute_sound) and g.me.z<=0:
			g.p.pause_sound(parachute_sound)
		if not isinstance(parachute_sound,int) and parachute_sound.paused and g.me.z>0 and g.falling==True: g.p.resume_sound(parachute_sound)

	if falling_sound is not None:
		if g.p.sound_is_playing(falling_sound) and g.me.z<=0: g.p.pause_sound(falling_sound)
		if falling_sound.paused and g.me.z>0 and g.falling==True: g.p.resume_sound(falling_sound)



	if events: process_events()
	#if g.recording and recordvoicetimer.elapsed>=5: record_voice(); recordvoicetimer.restart()
	play_for_voicechat()
	play_for_voicechat2()
	if (g.e.type==event_disconnect and g.connected==True):
		speak("Connection lost from the server.")
		reset()
		g.delay(2000)
		login()
	elif g.e.type==event_receive:
		if g.e.channel==19:

			g.inv=pickle.loads(g.e.message)
			if g.invmenu:
				m.items.clear()
				m.first_letters.clear()
				items=list(g.inv.keys())
				for item in items:
					name=item
					amount=g.inv[item]
					try: m.add_item_tts(name+": You have "+str(amount)+".", name)
					except: pass


		elif (g.e.channel==4):
		
			if "{}[]" in g.e.message: parsed=string_split(g.e.message,"{}[]",True)
			if "{}[]" not in g.e.message: parsed=string_split(g.e.message," ",True)
			if parsed[0]=="addzone":
				spawn_zone(stn(parsed[1]), stn(parsed[2]), stn(parsed[3]), stn(parsed[4]), stn(parsed[5]), stn(parsed[6]), parsed[7])
				g.tile_cache.clear()
			elif parsed[0]=="removezone":
				remove_zone(stn(parsed[1]), stn(parsed[2]), stn(parsed[3]), stn(parsed[4]), stn(parsed[5]), stn(parsed[6]), parsed[7])
				g.tile_cache.clear()
				fallcheck(); checkloc()
			elif parsed[0]=="updatezone":
				update_zone(stn(parsed[1]), stn(parsed[2]), stn(parsed[3]), stn(parsed[4]), stn(parsed[5]), stn(parsed[6]), parsed[7], stn(parsed[8]), stn(parsed[9]), stn(parsed[10]), stn(parsed[11]), stn(parsed[12]), stn(parsed[13]), parsed[14])
				fallcheck(); checkloc()



			if parsed[0]=="addplatform":
				spawn_platform(stn(parsed[1]), stn(parsed[2]), stn(parsed[3]), stn(parsed[4]), stn(parsed[5]), stn(parsed[6]), parsed[7])
				g.tile_cache.clear()
			elif parsed[0]=="removeplatform":
				remove_platform(stn(parsed[1]), stn(parsed[2]), stn(parsed[3]), stn(parsed[4]), stn(parsed[5]), stn(parsed[6]), parsed[7])
				g.tile_cache.clear()
				fallcheck(); checkloc()
			elif parsed[0]=="updateplatform":
				update_platform(stn(parsed[1]), stn(parsed[2]), stn(parsed[3]), stn(parsed[4]), stn(parsed[5]), stn(parsed[6]), parsed[7], stn(parsed[8]), stn(parsed[9]), stn(parsed[10]), stn(parsed[11]), stn(parsed[12]), stn(parsed[13]), parsed[14])
				fallcheck(); checkloc()


			elif parsed[0]=="viewticket":
				ticket_dialog(parsed[1],parsed[2],strtobool(parsed[3]),strtobool(parsed[4]))
			elif parsed[0]=="viewticket2":
				ticket_dialog2(parsed[1],parsed[2],strtobool(parsed[3]),strtobool(parsed[4]))


		elif (g.e.channel==0):
		
			parsed=string_split(g.e.message," ",True)
			if parsed[0]=="invcat":
				catinfo=g.e.message.replace("invcat ","")
				catname=catinfo.split(" ")[0]
				catitems=catinfo.replace("catname ","")
				g.invcategories[catname]=catitems.split(" ")
			elif parsed[0]=="ticketcreate": create_ticket_dialog()
			elif parsed[0] == "buildzone":
				dat=builder_input("minx=enter the left x of your zone\nmaxx=enter the right x of your zone\nminy=enter the minimum y of your zone\nmaxy=enter the maximum y of your zone\nminz=enter the bottom z of your zone\nmaxz=enter the top z of your zone\ntext=enter the text of your zone")
				if dat is not None:
					temp=""
					if yesno("Would you like this zone to be trackable?")=="yes": temp=":trackable"
					g.n.send_reliable(0, "addinmap zone:"+dat.str("minx")+":"+dat.str("maxx")+":"+dat.str("miny")+":"+dat.str("maxy")+":"+dat.str("minz")+":"+dat.str("maxz")+":"+dat.str("text")+temp, 0)
					return
				else:
					process_events()
					return
			elif parsed[0] == "buildsign":
				dat=builder_input("minx=enter the x of sign\nminy=enter the y of sign\nminz=enter the z of sign\ntext=enter the text of sign")
				if dat is not None:
					temp=""
					temp=""
					g.n.send_reliable(0, "addinmap sign:"+dat.str("minx")+":"+dat.str("miny")+":"+dat.str("minz")+":"+dat.str("text")+temp, 0)
					return
				else:
					process_events()
					return
			elif parsed[0] == "buildchest":
				dat=builder_input("minx=enter the x of chest\nminy=enter the y of chest\nminz=enter the z of chest")
				if dat is not None:
					temp=""
					temp=""
					g.n.send_reliable(0, "addinmap chest:"+dat.str("minx")+":"+dat.str("miny")+":"+dat.str("minz")+":"+temp, 0)
					return
				else:
					process_events()
					return


			elif parsed[0] == "buildecho":
				dat=builder_input("minx=enter the left x of echo\nmaxx=enter the right x of echo\nminy=enter the minimum y of echo\nmaxy=enter the maximum y of echo\nminz=enter the bottom z of echo\nmaxz=enter the top z of echo\ndelay=enter delay, default is 0.1\nlrdelay=enter lrdelay, default is 0.1\ndamping=enter damping, default is 0.5\nfeedback=enter feedback, default is 0.5\nspread=enter spread, default is -1.0")
				if dat is not None:
					g.n.send_reliable(0, "addinmap echo:"+dat.str("minx")+":"+dat.str("maxx")+":"+dat.str("miny")+":"+dat.str("maxy")+":"+dat.str("minz")+":"+dat.str("maxz")+":"+dat.str("delay")+":"+dat.str("lrdelay")+":"+dat.str("damping")+":"+dat.str("feedback")+":"+dat.str("spread"), 0)
					return
				else:
					process_events()
					return
			elif parsed[0] == "addline":
				addlinelan=get_input("Enter the new LINE")
				if addlinelan != "":
					g.n.send_reliable(0, "addline "+addlinelan+"", 0)
			elif parsed[0] == "editmap":
				data=string_replace(g.e.message, "editmap ", "", False)
				newdata=get_input("map text",data,False)
				if newdata!="": g.n.send_reliable(0,"editmap "+newdata,0)
			elif parsed[0] == "menueditline":
				data=string_replace(g.e.message, "menueditline ", "", False)
				lines=delinear(data)
				m.reset(True)
				menu.setupmenu()
				menu.callback2=mainloop
				for i in range(len(lines)):
					if string_contains(lines[i], "owner:", 1)>-1:
						continue
					m.add_item_tts(lines[i], lines[i])
				mres=m.run("Select a line", True)
				process_events()
				if mres != 0:
					g.n.send_reliable(0, "editlinemenu "+m.get_item_name(mres), 0)
			elif parsed[0] == "editline":
				if parsed[1] == "back":
					return
				l=get_input("Enter the new value for this line")
				if l != "":
					g.n.send_reliable(0, "editlineSPLITS_THE_PARTS_OF_EDITLINE "+string_replace(g.e.message, "editline ", "", False)+"SPLITS_THE_PARTS_OF_EDITLINE"+l, 0)
			elif parsed[0] == "menudeleteline":
				data=string_replace(g.e.message, "menudeleteline ", "", False)
				lines=delinear(data)
				m.reset(True)
				menu.setupmenu()
				menu.callback2=mainloop
				for i in range(len(lines)):
					m.add_item_tts(lines[i], lines[i])
				mres=m.run("Select a line", True)
				process_events()
				# buraya bakılsın
				if mres != 0:
					g.n.send_reliable(0, "deleteline "+m.get_item_name(mres), 0)
			elif parsed[0] == "yesno":
				q=" ".join(parsed).replace("yesno ","")
				m.reset(True)
				menu.setupmenu()
				m.callback2=mainloop
				m.add_item_tts("yes","yes")
				m.add_item_tts("no","no")
				mres=m.run(q)
				process_events()
				if mres==0:
					g.n.send_reliable(0,"yesno no",0)
					if len(g.p1)!=0:
						p1=g.p1.pop()
						p2=g.p2.pop()
						p3=g.p3.pop()
						p4=g.p4.pop()
						g.n.send_reliable(0,"mpacket "+p1,0)
						g.n.send_reliable(0,"mitems "+p3,0)
						serverside_menu(p1,p2,p3,p4)
						process_events()
				else:
					choice=m.get_item_name(mres)
					g.n.send_reliable(0,"yesno "+choice,0)
					if choice=="no":
						if len(g.p1)!=0:
							p1=g.p1.pop()
							p2=g.p2.pop()
							p3=g.p3.pop()
							p4=g.p4.pop()
							g.n.send_reliable(0,"mpacket "+p1,0)
							g.n.send_reliable(0,"mitems "+p3,0)
							serverside_menu(p1,p2,p3,p4)
							process_events()

			elif parsed[0] == "builddoor":
				dat=builder_input("x=enter the x of this door\nmx=enter the mx of this door\ny=enter the y of this door\nmy=enter the my of this door\nz=enter the z of this door\nmz=enter the mz of this door\ndx=enter the destination x of this door\ndy=enter the y of the destination\ndz=enter the z of the destination\ns=enter the speed to move the player to the destination in Milliseconds (1000=1second)")
				if dat is None:
					return
					s3=dropen()
				s3=dropen()
				if s3 == "":
					s4=drclose()
				s4=drclose()
				if s4 == "":
					speak("canceled")
				if dat is not None:
					g.n.send_reliable(0, "addinmap door:"+dat.str("x")+":"+dat.str("mx")+":"+dat.str("y")+":"+dat.str("my")+":"+dat.str("z")+":"+dat.str("mz")+":"+dat.str("dx")+":"+dat.str("dy")+":"+dat.str("dz")+":"+dat.str("s")+":"+s3+".ogg"+":"+s4+".ogg", 0)
				process_events()
			elif parsed[0] == "buildreverb":
				dat=builder_input("minx=enter the left x of reverb\nmaxx=enter the right x of reverb\nminy=enter the minimum y of reverb\nmaxy=enter the maximum y of reverb\nminz=enter the bottom z of reverb\nmaxz=enter the top z of reverb\ndensity=enter density, default is 1.0\ndiffusion=enter diffusion, default is 1.0\ngain=enter gain, default is 0.32\ngainhf=enter gainhf, default is 0.89\ndecay_time=enter decay time, default is 1.49\nhfratio=enter hfratio, default is 0.83\nreflections_gain=enter reflections gain, default is 0.05\nreflections_delay=enter reflections delay, default is 0.007\nlate_reverb_gain=enter late reverb gain, default is 1.26\nlate_reverb_delay=enter late reverb delay, default is 0.011\nair_absorption_gainhf=enter air absorption gainhf, default is 0.994\nroom_rolloff_factor=enter room rolloff factor, default is 0.0")
				if dat is not None:
					g.n.send_reliable(0, "addinmap reverb:"+dat.str("minx")+":"+dat.str("maxx")+":"+dat.str("miny")+":"+dat.str("maxy")+":"+dat.str("minz")+":"+dat.str("maxz")+":"+dat.str("density")+":"+dat.str("diffusion")+":"+dat.str("gain")+":"+dat.str("gainhf")+":"+dat.str("decay_time")+":"+dat.str("hfratio")+":"+dat.str("reflections_gain")+":"+dat.str("reflections_delay")+":"+dat.str("late_reverb_gain")+":"+dat.str("late_reverb_delay")+":"+dat.str("air_absorption_gainhf")+":"+dat.str("room_rolloff_factor"), 0)
					return
				else:
					process_events()
					return
			elif parsed[0] == "buildeaxreverb":
				dat=builder_input("minx=enter the left x of eaxreverb\nmaxx=enter the right x of eaxreverb\nminy=enter the minimum y of eaxreverb\nmaxy=enter the maximum y of eaxreverb\nminz=enter the bottom z of eaxreverb\nmaxz=enter the top z of eaxreverb\ndensity=enter density, default is 1.0\ndiffusion=enter diffusion, default is 1.0\ngain=enter gain, default is 0.32\ngainhf=enter gainhf, default is 0.89\ngainlf=enter gainlf, default is 1.0\ndecay_time=enter decay time, default is 1.49\nhfratio=enter decay hfratio, default is 0.83\nlfratio=enter decay lfratio, default is 1.0\nreflections_gain=enter reflections gain, default is 0.05\nreflections_delay=enter reflections delay, default is 0.007\nreflections_pan=enter reflections pan, default is 0.0\nlate_eaxreverb_gain=enter late eaxreverb gain, default is 1.26\nlate_eaxreverb_delay=enter late eaxreverb delay, default is 0.011\nlate_eaxreverb_pan=enter late eaxreverb pan, default is 0.0\necho_time=enter echo time, default is 0.25\necho_depth=enter echo depth, default is 0.0\nmodulation_time=enter modulation time, default is 0.25\nmodulation_depth=enter modulation depth, default is 0.0\nair_absorption_gainhf=enter air absorption gainhf, default is 0.994\nhfreference=enter hfreference, default is 5000.0\nlfreference=enter lfreference, default is 250.0\nroom_rolloff_factor=enter room rolloff factor, default is 0.0")
				if dat is not None:
					g.n.send_reliable(0, "addinmap eaxreverb:"+dat.str("minx")+":"+dat.str("maxx")+":"+dat.str("miny")+":"+dat.str("maxy")+":"+dat.str("minz")+":"+dat.str("maxz")+":"+dat.str("density")+":"+dat.str("diffusion")+":"+dat.str("gain")+":"+dat.str("gainhf")+":"+dat.str("gainlf")+":"+dat.str("decay_time")+":"+dat.str("hfratio")+":"+dat.str("lfratio")+":"+dat.str("reflections_gain")+":"+dat.str("reflections_delay")+":"+dat.str("reflections_pan")+":"+dat.str("late_eaxreverb_gain")+":"+dat.str("late_eaxreverb_delay")+":"+dat.str("late_eaxreverb_pan")+":"+dat.str("echo_time")+":"+dat.str("echo_depth")+":"+dat.str("modulation_time")+":"+dat.str("modulation_depth")+":"+dat.str("air_absorption_gainhf")+":"+dat.str("hfreference")+":"+dat.str("lfreference")+":"+dat.str("room_rolloff_factor"), 0)
					return
				else:
					process_events()
					return


			elif parsed[0] == "buildsrc":
				dat=builder_input("minx=enter the left x of this source\nmaxx=enter the right x of this source\nminy=enter the minimum y of this source\nmaxy=enter the maximum y of this source\nminz=enter the bottom z of this source\nmaxz=enter the top z of this source")
				if dat is None:
					process_events()
					return
				soundfile=list_ambiences()
				if soundfile == "":
					speak("canceled")
					process_events()
					try: g.s.close()
					except: pass

					return
				process_events()
				g.n.send_reliable(0, "addinmap src:"+dat.str("minx")+":"+dat.str("maxx")+":"+dat.str("miny")+":"+dat.str("maxy")+":"+dat.str("minz")+":"+dat.str("maxz")+":"+soundfile+".ogg:"+str(g.s.volume), 0)
				try: g.s.close()
				except: pass
				return
			elif parsed[0] == "buildsrc2":
				dat=builder_input("minx=enter the left x of this ignore ambience\nmaxx=enter the right x of this ignore ambience\nminy=enter the minimum y of this ignore ambience\nmaxy=enter the maximum y of this ignore ambience\nminz=enter the bottom z of this ignore ambience\nmaxz=enter the top z of this ignore ambience")
				if dat is None:
					process_events()
					return
				process_events()
				g.n.send_reliable(0, "addinmap ignore_amb:"+dat.str("minx")+":"+dat.str("maxx")+":"+dat.str("miny")+":"+dat.str("maxy")+":"+dat.str("minz")+":"+dat.str("maxz"), 0)
				return
			elif parsed[0] == "buildelectric":
				dat=builder_input("x=enter the x of this electric pole\ny=enter the y of this electric pole\nz=enter the z of this electric pole")
				if dat is None:
					process_events()
					return
				process_events()
				g.n.send_reliable(0, "addinmap electric_pole:"+dat.str("x")+":"+dat.str("y")+":"+dat.str("z"), 0)
				return


			elif parsed[0] == "buildamb":
				dat=builder_input("minx=enter the left x of this ambience\nmaxx=enter the right x of this ambience\nminy=enter the minimum y of this ambience\nmaxy=enter the maximum y of this ambience\nminz=enter the bottom z of this ambience\nmaxz=enter the top z of this ambience")
				if dat is None:
					process_events()
					return
				soundfile=list_ambiences()
				if soundfile == "":
					speak("canceled")
					process_events()
					try: g.s.close()
					except: pass

					return
				process_events()
				g.n.send_reliable(0, "addinmap amb:"+dat.str("minx")+":"+dat.str("maxx")+":"+dat.str("miny")+":"+dat.str("maxy")+":"+dat.str("minz")+":"+dat.str("maxz")+":"+soundfile+".ogg:"+str(g.s.volume), 0)
				try: g.s.close()
				except: pass
				return

			elif parsed[0] == "motorspawn":
				if g.inve == False:
					g.inve=True
					g.oldusesub=g.usesub
					g.usesub=1
					g.oldwalktime=g.walktime
					g.walktime=25
			elif parsed[0] == "motorunspawn":
				g.inve=False

				g.usesub=g.oldusesub
				g.wind.volume=-100
				g.flash.volume=-100
			elif parsed[0] == "buildtile":
				dat=builder_input("minx=enter the left x of this tile\nmaxx=enter the right x of this tile\nminy=enter the minimum y of this tile\nmaxy=enter the maximum y of this tile\nminz=enter the bottom z of this tile\nmaxz=enter the top z of this tile")
				if dat is None:
					process_events()
					return
				platform=plattypemenu()
				if platform == "":
					process_events()
					return
				g.n.send_reliable(0, "addinmap platform:"+dat.str("minx")+":"+dat.str("maxx")+":"+dat.str("miny")+":"+dat.str("maxy")+":"+dat.str("minz")+":"+dat.str("maxz")+":"+platform, 0)
				process_events()
				return
			elif parsed[0] == "buildhidden_area":
				dat=builder_input("minx=enter the left x of this hidden_area\nmaxx=enter the right x of this hidden_area\nminy=enter the minimum y of this hidden_area\nmaxy=enter the maximum y of this hidden_area\nminz=enter the bottom z of this hidden_area\nmaxz=enter the top z of this hidden_area")
				if dat is None:
					process_events()
					return
				g.n.send_reliable(0, "addinmap hidden_area:"+dat.str("minx")+":"+dat.str("maxx")+":"+dat.str("miny")+":"+dat.str("maxy")+":"+dat.str("minz")+":"+dat.str("maxz"), 0)
				process_events()
				return

			elif parsed[0] == "buildstairs":
				dat=builder_input("dir=enter the direction in which the player will climb the stairs, x or y\nminx=enter the left x of this staircase\nmaxx=enter the right x of this staircase\nminy=enter the minimum y of this staircase\nmaxy=enter the maximum y of this staircase\nminz=enter the bottom z of this staircase\nmaxz=enter the top z of this staircase")
				if dat is None:
					process_events()
					return
				platform=plattypemenu()
				if platform == "":
					process_events()
					return
				res=yesno("Do you want this staircase to be reverse?")
				if res=="no": g.n.send_reliable(0, "addinmap staircase:"+dat.str("minx")+":"+dat.str("maxx")+":"+dat.str("miny")+":"+dat.str("maxy")+":"+dat.str("minz")+":"+dat.str("maxz")+":"+platform+":"+dat.str("dir"), 0)
				if res=="yes": g.n.send_reliable(0, "addinmap staircase:"+dat.str("minx")+":"+dat.str("maxx")+":"+dat.str("miny")+":"+dat.str("maxy")+":"+dat.str("minz")+":"+dat.str("maxz")+":"+platform+":"+dat.str("dir")+":1", 0)
				process_events()
				return

			elif parsed[0] == "buildwall":
				dat=builder_input("minx=enter the left x of this wall\nmaxx=enter the right x of this wall\nminy=enter the minimum y of this wall\nmaxy=enter the maximum y of this wall\nminz=enter the bottom z of this wall\nmaxz=enter the top z of this wall")
				if dat is None:
					process_events()
					return
				platform=plattypemenuw()
				if platform == "":
					process_events()
					return
				g.n.send_reliable(0, "addinmap platform:"+dat.str("minx")+":"+dat.str("maxx")+":"+dat.str("miny")+":"+dat.str("maxy")+":"+dat.str("minz")+":"+dat.str("maxz")+":"+platform, 0)
				process_events()
				return
			elif parsed[0] == "buildwall2":
				dat=builder_input("minx=enter the left x of this wall\nmaxx=enter the right x of this wall\nminy=enter the minimum y of this wall\nmaxy=enter the maximum y of this wall\nminz=enter the bottom z of this wall\nmaxz=enter the top z of this wall")
				if dat is None:
					process_events()
					return
				platform=plattypemenuw()
				if platform == "":
					process_events()
					return
				g.n.send_reliable(0, "addinmap wall:"+dat.str("minx")+":"+dat.str("maxx")+":"+dat.str("miny")+":"+dat.str("maxy")+":"+dat.str("minz")+":"+dat.str("maxz")+":"+platform, 0)
				process_events()
				return


			elif(parsed[0]=="distsound" and len(parsed)>5):
			
				soundname=parsed[1]
				x=string_to_number(parsed[2])
				y=string_to_number(parsed[3])
				z=string_to_number(parsed[4])
				soundmap=parsed[5]
				if soundmap!=g.mapname: return
				if "misc" in soundname and soundmap!=g.mapname: return
				if "door" in soundname and soundmap!=g.mapname: return
				if "molotov" in soundname and soundmap!=g.mapname: return
				g.distpool.play_3d(soundname+".ogg", g.me.x, g.me.y, g.me.z, x, y, z, calculate_theta(g.facing), False, False, True)
				
			elif(parsed[0]=="distpitchsound" and len(parsed)>6):
			
				soundname=parsed[1]
				x=string_to_number(parsed[2])
				y=string_to_number(parsed[3])
				z=string_to_number(parsed[4])
				soundmap=parsed[5]
				pitch=parsed[6]
				if soundmap!=g.mapname: return
				if "misc" in soundname and soundmap!=g.mapname: return
				if "door" in soundname and soundmap!=g.mapname: return
				if "molotov" in soundname and soundmap!=g.mapname: return
				try: g.distpool.play_3d(soundname+".ogg", g.me.x, g.me.y, g.me.z, x, y, z, calculate_theta(g.facing), False, False, True).handle.pitch=int(pitch)
				except: pass
				

			elif parsed[0] == "parachute_start":
				g.parachute=True
				g.falltime=150
				#g.walktime+=100
				#g.jumping=False
				parachute_sound=g.p.play_stationary("parachuteloop.ogg",True)
				g.parachutesoundtimer.restart()
				g.parachutesoundpositife=True

			elif parsed[0] == "parachute_stop":
				g.parachute=False
				g.falltime=90
				#g.walktime-=100
				g.p.destroy_sound(parachute_sound)
				parachute_sound=None

			elif parsed[0] == "play_inside_bus":
				g.in_bus = True
				if inside_bus_handle is None:
					inside_bus_handle = g.p.play_stationary("inside_bus.ogg", True)
				try:
					inside_bus_handle.volume = -25
					inside_bus_handle.pitch = 100
				except Exception:
					pass

			elif parsed[0] == "stop_inside_bus":
				g.in_bus = False
				if inside_bus_handle is not None:
					g.p.destroy_sound(inside_bus_handle)
					inside_bus_handle = None

			elif parsed[0] == "bus_audio" and len(parsed) >= 5:
				bus_audio_state["stopped"] = parsed[1] == "1"
				bus_audio_state["doors_open"] = parsed[2] == "1"
				bus_audio_state["moving"] = parsed[3] == "1"
				bus_audio_state["speed"] = stn(parsed[4])
				if inside_bus_handle is not None:
					try:
						if bus_audio_state["doors_open"]:
							inside_bus_handle.volume = -18
						elif bus_audio_state["stopped"]:
							inside_bus_handle.volume = -28
						else:
							inside_bus_handle.volume = -22
						inside_bus_handle.pitch = 90 + min(35, max(0, bus_audio_state["speed"] // 2))
					except Exception:
						pass

			elif(parsed[0]=="weaponlist" and len(parsed)>1):
			
				g.weapons.clear()
				g.w=0
				for i in range(1, len(parsed)):
				
					g.weapons.append(parsed[i])
					
				
			elif(parsed[0]=="gunlist" and len(parsed)>1):
			
				guns.clear()
				for i in range(1, len(parsed)):
				
					guns.append(parsed[i])
					
				
			elif(parsed[0]=="nomudtileslist" and len(parsed)>1):
			
				g.nomudtiles.clear()
				for i in range(1, len(parsed)):
				
					g.nomudtiles.append(parsed[i])
					
				


			elif(parsed[0]=="opensettings"): menu.option()
			elif(parsed[0]=="openlink" and len(parsed)>1):
				giveurl=parsed[1]
				speak("Opening the browse with "+parsed[1]+"")
#				time.sleep(2)
				webbrowser.open(giveurl)
			elif(parsed[0]=="weapondata" and len(parsed)>2):
			
				g.firetime=string_to_number(parsed[1])

				if parsed[2]=="auto":
					g.weaponauto=True
				if parsed[2]=="norm":
					g.weaponauto=False

				
			elif(parsed[0]=="weapondata2" and len(parsed)>2):
			
				g.firetime2=string_to_number(parsed[1])

				if parsed[2]=="auto":
					g.weaponauto2=True
				if parsed[2]=="norm":
					g.weaponauto2=False

				

			elif(parsed[0]=="weapondatafast" and len(parsed)>2):
			
				g.firetime=string_to_number(parsed[1])-(string_to_number(parsed[1])*25/100)

				if parsed[2]=="auto":
					g.weaponauto=True
				if parsed[2]=="norm":
					g.weaponauto=False

				
			elif(parsed[0]=="weapondata2fast" and len(parsed)>2):
			
				g.firetime2=string_to_number(parsed[1])-(string_to_number(parsed[1])*25/100)

				if parsed[2]=="auto":
					g.weaponauto2=True
				if parsed[2]=="norm":
					g.weaponauto2=False

				


			elif parsed[0]=="reloading":
				if not g.ducking:
					g.reloading=True; g.oldw=g.walktime; g.walktime+=120
			elif parsed[0]=="chatenable":
				g.chat=True
			elif parsed[0]=="chatdisable":
				g.chat=False

			elif parsed[0]=="notreloading":
				if not g.ducking:
					g.reloading=False; g.walktime=g.oldw

			elif parsed[0]=="cheat":
				try: g.n.send_reliable(0,"close",0)
				except: pass
				g.writeprefs(); g.reset()
				g.p.play_stationary("misc181.ogg",False)
				dlg("You have been kicked from the game due to using cheat tools")
				pygame.quit()
				ctypes.windll.kernel32.ExitProcess(0)
			elif parsed[0]=="drawtime":
				g.drawtime=int(parsed[1])
				g.drawing=True
				g.drawtimer.restart()
			elif parsed[0] == "ping" and len(parsed)>1:
				g.n.send_reliable(0, "pingr "+parsed[1], 0)

			elif(parsed[0]=="draw" and len(parsed)>1):
			
				g.weapons.append(parsed[1])
				g.w=(len(g.weapons)-1)
				speak(g.weapons[g.w])
				g.n.send_reliable(0,"draw "+g.weapons[g.w],0)

				
			elif(parsed[0]=="draw2" and len(parsed)>1):
			
				g.weapons2.append(parsed[1])
				g.w2=(len(g.weapons2)-1)
				speak(g.weapons2[g.w2])
				g.n.send_reliable(0,"draw2 "+g.weapons2[g.w2],0)

				

			elif(parsed[0]=="drawsilent" and len(parsed)>1):
			
				g.weapons.append(parsed[1])
				g.w=(len(g.weapons)-1)
				g.n.send_reliable(0,"drawsilent "+g.weapons[g.w],0)

				
			elif(parsed[0]=="draw2silent" and len(parsed)>1):
			
				g.weapons2.append(parsed[1])
				g.w2=(len(g.weapons2)-1)
				g.n.send_reliable(0,"draw2silent "+g.weapons2[g.w2],0)

				


			elif parsed[0]=="isadmin": g.admin=True
			elif parsed[0]=="isbuilder": g.builder=True
			elif parsed[0]=="isnotadmin": g.admin=False
			elif parsed[0]=="isnotbuilder": g.builder=False

			elif(parsed[0]=="speedup"):
			
				g.walktime-=random(50, 100)
				
			elif parsed[0] == "echo":
				echo=string_replace(g.e.message, "echo ", "", False)
				g.n.send_reliable(0,echo,g.e.channel)
			elif parsed[0] == "echocommand":
				echo=string_replace(g.e.message, "echocommand ", "", False)
				g.n.send_reliable(0,echo,1)


			elif parsed[0] == "input":
				ds=string_split(string_replace(g.e.message, "input +=1", "", False), "+=1", False)
				serverbox(stn(ds[0]), stn(ds[1]), stn(ds[2]), stn(ds[3]), ds[4], ds[5])
				process_events()
			elif parsed[0]=="fallstart":
				g.falling=True
				g.falldistance=0
				g.falltimer.restart()
			elif parsed[0]=="fallstop":
				g.falling=False
				g.falldistance=0
				g.falltimer.restart()
				if g.me.z==1: g.me.z=0

			elif parsed[0]=="facing": g.facing=int(parsed[1])
			elif parsed[0]=="walktime":
				if g.ducking: g.walktime=int(parsed[1])+100
				if not g.ducking: g.walktime=int(parsed[1])
				g.minwalktime=int(parsed[1])

			elif parsed[0]=="jumptime": g.jumptime=int(parsed[1])
			elif parsed[0]=="maxwalktime": g.maxwalktime=int(parsed[1])
			elif parsed[0]=="enablevoicechat": g.voicechat=1
			elif parsed[0]=="disablevoicechat": g.voicechat=0
			elif parsed[0]=="enablevoicechat2": g.voicechat2=1
			elif parsed[0]=="disablevoicechat2": g.voicechat2=0

			elif parsed[0]=="ingroup": g.ingroup=True
			elif parsed[0]=="notingroup": g.ingroup=False
			elif parsed[0]=="incommunity": g.incommunity=True
			elif parsed[0]=="notincommunity": g.incommunity=False

			elif parsed[0]=="matchteammenu": matchteammenu(g.e.message.replace(parsed[0]+" ",""))
			elif parsed[0]=="voicechatvolume": change_voicechat_volume(g.e.message.replace(parsed[0]+" ",""))
			elif parsed[0]=="playrange":
				if parsed[0]=="playrange":

					source_sound = g.p.play_3d(
						parsed[1],
						g.me.x,
						g.me.y,
						g.me.z,
						stn(parsed[2]),
						stn(parsed[4]),
						stn(parsed[6]),
						calculate_theta(g.facing),
						False
					)
					try:
						g.p.update_sound_range_3d(
						source_sound,
						0,
						stn(parsed[3]) - stn(parsed[2]),
						0,
						stn(parsed[5]) - stn(parsed[4]),
						0,
						stn(parsed[7]) - stn(parsed[6]),
						calculate_theta(g.facing),
					)

					except: pass
			elif(parsed[0]=="trackobj"):
				if parsed[1]=="back": return
				if parsed[1]=="stop":
					speak("Stopped tracking")
					g.trackx = -1
					g.tracky = -1
					g.tracked = False
					return

				speak("Tracking")
				coords=g.e.message.split(" ")[1].split(",")
				g.trackx=round(stn(coords[0]))
				g.tracky=round(stn(coords[1]))
				g.trackz=round(stn(coords[2]))
				g.tracked=True
			elif parsed[0]=="canjump": g.canjump=int(parsed[1])
			elif parsed[0]=="canduck": g.canduck=int(parsed[1])
			elif parsed[0]=="restartmotor":
				g.wind.stop()
				g.wind.play_looped()
			elif parsed[0]=="motorvolume": g.wind.volume=int(parsed[1])
			elif parsed[0]=="flashvolume":
				try: g.flash.volume=int(parsed[1])
				except: pass
			elif parsed[0]=="cannotexit":
				g.cannotexit=True
				g.cannotexittime=60000
				g.cannotexittimer.restart()
			elif parsed[0]=="maxx": g.max.x=int(parsed[1])
			elif parsed[0]=="maxy": g.max.y=int(parsed[1])
			elif(parsed[0]=="candraw"): g.candraw=True
			elif(parsed[0]=="cannotdraw"): g.candraw=False
			elif(parsed[0]=="accountlogin"):
				g.n.send_reliable(0,"close",0)
				for i in range(5000): g.netloop()
				g.name=parsed[1]
				g.password=parsed[2]
				g.savemail=parsed[3]

				writeprefs()

				reset()

				login()
			elif parsed[0]=="noweaponauto": g.weaponauto=False
			elif parsed[0]=="pausesources": pause_all_sources()
			elif parsed[0]=="near": g.near2=True
			elif parsed[0]=="notnear": g.near2=False
			elif parsed[0]=="died": g.died=True
			elif parsed[0]=="notdied": g.died=False
			elif parsed[0]=="maxaim": g.maxaim=stn(parsed[1])
			elif parsed[0]=="sitstart":
				g.sitting=True
				g.n.send_reliable(0,"sitstart",0)
			elif parsed[0]=="sitstop":
				g.sitting=False
				g.n.send_reliable(0,"sitstop",0)

			elif(parsed[0]=="setaim"): g.aim=stn(parsed[1])
			elif parsed[0]=="rainstart":
				g.rainsnd.load(get_rain_sound())
				g.rainsnd.player.alhrtf=False
				g.rainsnd.player.stationary=True
				g.rainsound=get_rain_sound()
				g.rainsnd.play_looped()
				g.rainsnd.volume=-50
				g.rainfadein=True
				g.rain=True
			elif parsed[0]=="rainfinishstart": g.rainfinish=True
			elif parsed[0]=="rainfinishstop": g.rainfinish=False
			elif parsed[0]=="rainvolume":
				g.target_rain_volume=stn(parsed[1])
			elif parsed[0]=="rainstop":
				Thread(target=g.rainsnd.fade2).start()
			elif parsed[0]=="inbike": g.inbike=True
			elif parsed[0]=="notinbike": g.inbike=False
			elif(parsed[0]=="destroymolotofburning"):
				for item in g.p.items:
					if item.filename=="molotofburning.ogg": item.handle.stop()
			elif parsed[0]=="mapname": g.mapname=parsed[1]
			elif parsed[0]=="friendlist":
				pl=parsed[1]
				flist="".join(parsed[2:]).split("\n")
				index=get_player_index(pl)
				if index>-1: g.players[index].friendlist=flist

			elif(parsed[0]=="walkmod"):
			
				g.walktime+=random(50, 100)
				
			elif parsed[0]=="matchteam": g.matchteam=parsed[1]
			elif(parsed[0]=="resetwalktime"):
			
				g.walktime=250
				
			elif(parsed[0]=="writefile"):
			
				filename=parsed[1]
				text=string_replace(g.e.message,parsed[0]+" "+parsed[1]+" ","",False)

				f=open(filename,"w")
				f.write(text)
				f.close()
				
			elif(parsed[0]=="pm"):
			
				g.p.play_stationary("misc173.ogg",False)

				message=string_replace(g.e.message,"pm ","",False)
				user=parsed[3]
				if parsed[2]!="to":
					g.reply=user.replace(":","")
				add_buffer_item("friend messages",message)
				
			elif(parsed[0]=="friend"):
			
				message=string_replace(g.e.message,"friend ","",False)
				add_buffer_item("friend messages",message)
				
			elif(parsed[0]=="killn"):
			
				message=string_replace(g.e.message,"killn ","",False)
				add_buffer_item("death and kill notifications",message)
				

			elif(parsed[0]=="mapmessage"):
			
				message=string_replace(g.e.message,"mapmessage ","",False)
				add_buffer_item("map messages",message)
				
			elif(parsed[0]=="groupmessage"):
			
				message=string_replace(g.e.message,"groupmessage ","",False)
				add_buffer_item("group messages",message)

				

			elif(parsed[0]=="groupnotification"):
			
				notification=string_replace(g.e.message,"groupnotification ","",False)
				add_buffer_item("group notifications",notification)
				



			elif(parsed[0]=="communitymessage"):
			
				message=string_replace(g.e.message,"communitymessage ","",False)
				add_buffer_item("community messages",message)

				

			elif(parsed[0]=="communitynotification"):
			
				notification=string_replace(g.e.message,"communitynotification ","",False)
				add_buffer_item("community notifications",notification)
				




			elif(parsed[0]=="nearinfo"):
			
				message=string_replace(g.e.message,"nearinfo ","",False)
				add_buffer_item("near notifications",message)
				
			elif(parsed[0]=="matchmessage"):
			
				message=string_replace(g.e.message,"matchmessage ","",False)
				add_buffer_item("match messages",message)
				
			elif(parsed[0]=="itemmessage"):
			
				message=string_replace(g.e.message,"itemmessage ","",False)
				add_buffer_item("items",message)
				


			elif(parsed[0]=="teammessage"):
			
				message=string_replace(g.e.message,"teammessage ","",False)
				add_buffer_item("team messages",message)
				


			elif(parsed[0]=="adminmessage"):
			
				message=string_replace(g.e.message,"adminmessage ","",False)
				add_buffer_item("admin messages",message)
				



			elif parsed[0] == "launchmenu":
				i=string_replace(parsed[1], "[SPCE]", " ", True)
				t=string_replace(parsed[2], "[SPCE]", " ", True)
				items=string_replace(g.e.message, parsed[0]+" "+parsed[1]+" "+parsed[2]+" ", "", True)

				serverside_menu(t, i, items)
				process_events()

			elif(parsed[0]=="notify"):
			
				mess=string_replace(g.e.message,"notify ","",False)
				g.p.play_stationary("notify.ogg",False)
				add_buffer_item("notifications",mess)
				
			elif(parsed[0]=="stopmoving"):
			
				g.can_move=False
				
			elif(parsed[0]=="startmoving"):
			
				g.can_move=True
				
			elif(parsed[0]=="pong"):
			
				g.pinging=False
				speak("The ping took "+str(g.pingtimer.elapsed)+" milliseconds.")
				g.pingpool.play_extended_3d("misc128.ogg", g.me.x-3, g.me.y, g.me.z, g.me.x, g.me.y, g.me.z, calculate_theta(0), 0, 0, 0, 0, 0, 0, False, 0.0, 0.0, 0.0, 80.0, False)

				
			elif(parsed[0]=="beacon" and len(parsed)>5):
			
				x=string_to_number(parsed[1])
				y=string_to_number(parsed[2])
				z=string_to_number(parsed[3])
				map=parsed[4]
				charname=parsed[5]
				if(charname!=g.name and map==g.mapname):
				
					g.p.play_3d("beacon.ogg",g.me.x,g.me.y,g.me.z,x,y,z,calculate_theta(dummy(g.facing)),False)
					
				
			elif(parsed[0]=="reboot_server"):
			
				reset()
				try: g.n.destroy()
				except: pass

				g.p.play_stationary("misc193.ogg",False)
				speak("The server is rebooting. An attempt will be made to log in shortly. Please wait.")
				g.delay(5000)
				g.p.play_stationary("misc240.ogg",False)
				speak("Reconnecting...")
				g.p.play_stationary("misc154.ogg",False)
				g.delay(1000)

				login()
#				menu.login_settings()()
				
			elif(parsed[0]=="exiting"):
			
				dlg("The server is going offline for maintenance. Don't worry, we'll be back soon. Your client will now disconnect.")
				reset()
				menu.login_settings()
				
			elif(parsed[0]=="jump"):
			
				x=string_to_number(parsed[2])
				y=string_to_number(parsed[3])
				z=string_to_number(parsed[4])
				map=parsed[5]
				if(g.mapname!="lobby" and parsed[1]!=g.name and map==g.mapname):
				
					g.p.play_3d("jump"+str(random(1,4))+".ogg", g.me.x, g.me.y, g.me.z, x, y, z, calculate_theta(dummy(g.facing)), False)
					
				
			elif(parsed[0]=="hardland"):
			
				x=string_to_number(parsed[2])
				y=string_to_number(parsed[3])
				z=string_to_number(parsed[4])
				map=parsed[5]
				if(g.mapname!="lobby" and map==g.mapname):
				
					if g.parachute==True:
						g.p.play_3d(get_tile_at(x, y, z)+"land.ogg", g.me.x, g.me.y, g.me.z, x, y, z, calculate_theta(dummy(g.facing)), False)
					else:
						g.p.play_3d(get_tile_at(x, y, z)+"fall.ogg", g.me.x, g.me.y, g.me.z, x, y, z, calculate_theta(dummy(g.facing)), False)
					
				
			elif parsed[0]=="switchlang":
				filename="lang/"+parsed[1]+".lng"
				content=g.e.message.replace(parsed[0]+" "+parsed[1]+" ","")
				with open(filename,"w",encoding="utf-8") as f: f.write(content)
				g.lngdata=content
				g.transcache.clear()
				g.lang=parsed[1]
				file_encrypt(filename,g.langkey)
			elif parsed[0]=="updatelang":
				filename="lang/"+parsed[1]+".lng"
				content=g.e.message.replace(parsed[0]+" "+parsed[1]+" ","")
				with open(filename,"w",encoding="utf-8") as f: f.write(content)
				if g.lang==parsed[1]: g.lngdata=content
				g.transcache.clear()
				file_encrypt(filename,g.langkey)
			elif parsed[0] == "createmsound" and len(parsed)>=8:
				createmsound(parsed[1], parsed[2], stn(parsed[3]), stn(parsed[4]), stn(parsed[5]), parsed[6], stn(parsed[7]))
			elif parsed[0] == "updatemsound" and len(parsed)>=6:
				updatemsound(parsed[1], stn(parsed[2]), stn(parsed[3]), stn(parsed[4]), stn(parsed[5]))
			elif parsed[0] == "destroymsound" and len(parsed)>1:
				destroymsound(parsed[1])

			elif parsed[0]=="clip":
				clipboard_copy_text(g.e.message.replace(parsed[0]+" ",""))
			elif(parsed[0]=="land"):
			
				x=string_to_number(parsed[2])
				y=string_to_number(parsed[3])
				z=string_to_number(parsed[4])
				map=parsed[5]
				if(g.mapname!="lobby" and parsed[1]!=g.name and map==g.mapname):
				
					g.p.play_3d(get_tile_at(x, y, z)+"land.ogg", g.me.x, g.me.y, g.me.z, x, y, z, calculate_theta(dummy(g.facing)), False)
					
				
			elif(parsed[0]=="fall"):
			
				x=string_to_number(parsed[2])
				y=string_to_number(parsed[3])
				z=string_to_number(parsed[4])
				map=parsed[5]
				if(g.mapname!="lobby" and parsed[1]!=g.name and map==g.mapname):
				
					if g.parachute==True:
						g.p.play_3d(get_tile_at(x, y, z)+"land.ogg", g.me.x, g.me.y, g.me.z, x, y, z, calculate_theta(dummy(g.facing)), False)
					else:
						g.p.play_3d(get_tile_at(x, y, z)+"fall.ogg", g.me.x, g.me.y, g.me.z, x, y, z, calculate_theta(dummy(g.facing)), False)
					
				
			elif(parsed[0]=="die"):
			
				speak("You are dead.")
				g.loldietimer.restart()
				death()
				
			elif parsed[0]=="matchwatch": g.watching=parsed[1]; speak(parsed[1]); g.should_watch=True
			elif parsed[0]=="matchwatchstop": g.watching=""; g.n.send_reliable(0,g.e.message,g.e.channel); g.aim=0
			elif parsed[0]=="matchwatchstopnoserver": g.watching=""; g.aim=0
			elif(parsed[0]=="mapdata"):
			
				load_map(string_replace(g.e.message, "mapdata ", "", False))
				if g.mapready: fallcheck(); checkloc()
				#g.mapready=True
			elif(parsed[0]=="move" and len(parsed)>3):
			
				g.me.x=string_to_number(parsed[1])
				g.me.y=string_to_number(parsed[2])
				g.me.z=string_to_number(parsed[3])
				positions()
				
			elif (parsed[0]=="play_s" and len(parsed)>=2):
			
				if "welcome" in parsed[1]: g.mapready=True; fallcheck(); checkloc()
				g.p.play_stationary(parsed[1],False,False)
				
			elif (parsed[0]=="play_s2" and len(parsed)>=2):
			
				try: g.p.play_stationary(parsed[1],False,False).handle.volume=-25
				except: pass
				

			elif parsed[0]=="zombie":
				if "zombie" not in g.mapname:
					g.zombie=True
					g.n.send_reliable(0,"draw claw",0)
					g.walktime+=25
					g.weapons.append("claw")
					g.w=len(g.weapons)-1
					g.ww=len(g.weapons)-1
			elif(parsed[0]=="offline" and len(parsed)>1):
			
				if(parsed[4]==g.name):
				
					x=False
					reset()
					menu.login_settings()
					
				x=string_to_number(parsed[1])
				y=string_to_number(parsed[2])
				z=string_to_number(parsed[3])
				if(g.me.x > x-20 and g.me.x < x+20 and g.me.y > y-20 and g.me.y < y+20 and g.me.z>z-20 and g.me.z<z+20 and parsed[4]!=g.name and g.mapname==parsed[5] and g.onlinemsg==1):
				
					frnd=g.p.play_3d("friendwent.ogg", g.me.x, g.me.y, g.me.z, x, y, z, calculate_theta(dummy(g.facing)), False)
					frnd.handle.volume=-20
					add_buffer_item("online and offline notifications","Friend "+parsed[4]+" went offline")
					
				else:
				
					if g.onlinemsg==1:
						frnd=g.p.play_stationary("friendwent.ogg", False)
						frnd.handle.volume=-20
						add_buffer_item("online and offline notifications","Friend "+parsed[4]+" went offline")
					
				remove_player(parsed[4])
				
			elif(parsed[0]=="offline2" and len(parsed)>1):
			
				if(parsed[4]==g.name):
				
					x=False
					reset()
					menu.login_settings()
					
				x=string_to_number(parsed[1])
				y=string_to_number(parsed[2])
				z=string_to_number(parsed[3])
				remove_player(parsed[4])
				

			elif(parsed[0]=="forcespawn" and len(parsed)>5) :

				try: spawn_player(float(parsed[1]), float(parsed[2]), float(parsed[3]), parsed[4], parsed[5], int(parsed[6]))
				except: spawn_player(float(parsed[1]), float(parsed[2]), float(parsed[3]), parsed[4], parsed[5], 48000)
				g.n.send_reliable(0,"resetfriends",0)
				pl=g.players[len(g.players)-1]
				init_voicechat_player(pl)

			elif(parsed[0]=="door_at" and len(parsed)==12):
			
				doorx = string_to_number(parsed[1])
				doory = string_to_number(parsed[2])
				doorz = string_to_number(parsed[3])
				finishx = string_to_number(parsed[4])
				finishy = string_to_number(parsed[5])
				finishz = string_to_number(parsed[6])
				dtime = string_to_number(parsed[7])
				ds1 = parsed[8]
				ds2 = parsed[9]
				ds3 = parsed[10]
				ds4 = parsed[11]
				spawn_door(doorx, doory, doorz, dtime, finishx, finishy, finishz, ds1, ds2, ds3, ds4)
				
			elif(parsed[0]=="online"):
			
				x=string_to_number(parsed[1])
				y=string_to_number(parsed[2])
				z=string_to_number(parsed[3])
				if(g.me.x > x-20 and g.me.x < x+20 and g.me.y > y-20 and g.me.y < y+20 and g.me.z>z-20 and g.me.z<z+20 and parsed[4]!=g.name and parsed[5]==g.mapname and g.onlinemsg==1):
				
					frnd=g.p.play_3d("friendcame.ogg", g.me.x, g.me.y, g.me.z, x, y, z, calculate_theta(dummy(g.facing)), False)
					frnd.handle.volume=-20
					add_buffer_item("online and offline notifications","friend "+parsed[4]+" came online")
					
				else:
				
					if g.onlinemsg==1:
						frnd=g.p.play_stationary("friendcame.ogg", False)
						frnd.handle.volume=-20
						add_buffer_item("online and offline notifications","friend "+parsed[4]+" came online")
					
				spawn_player(x, y, z, parsed[5], parsed[4], int(parsed[6]))
				g.n.send_reliable(0,"resetfriends",0)
				pl=g.players[len(g.players)-1]
				init_voicechat_player(pl)

			elif(parsed[0]=="online2"):
			
				x=string_to_number(parsed[1])
				y=string_to_number(parsed[2])
				z=string_to_number(parsed[3])
				try: spawn_player(x, y, z, parsed[5], parsed[4], int(parsed[6]))
				except: spawn_player(x, y, z, parsed[5], parsed[4], 48000)
				g.n.send_reliable(0,"resetfriends",0)
				pl=g.players[len(g.players)-1]
				init_voicechat_player(pl)

			else:
				speak(g.e.message)
			

		elif (g.e.channel==1):
		
			parsed=string_split(g.e.message," ",False)
			if(len(parsed)>1):
			
				action=parsed[0]
				g.p.play_stationary(action+".ogg",False)
				mess=string_trim_left(g.e.message,string_len(action)+1)
				add_buffer_item("General_Chats",mess)
				
			
		elif (g.e.channel==2):
		
			add_buffer_item("misc",g.e.message)
			return
		elif(g.e.channel==3):
		
			parsed=string_split(g.e.message," ",True)
			if(len(parsed)>=6 and is_sound_number(parsed[1]) and is_sound_number(parsed[2]) and is_sound_number(parsed[3])):
			
				if(len(parsed)==6):
				
					if(parsed[4]==g.mapname):
						try:
							if "walldestroy" not in parsed[0] and "explode" not in parsed[0] and "zombie" not in parsed[0] and "fall" not in parsed[0] and "voice17" not in parsed[0] and "itembeep2" not in parsed[0] and "whiz" not in parsed[0]: it=g.p.play_3d(parsed[0]+".ogg", g.me.x, g.me.y, g.me.z, round(string_to_number(parsed[1])), round(string_to_number(parsed[2])), round(string_to_number(parsed[3])), calculate_theta(dummy(g.facing)), False)
							if "walldestroy" in parsed[0] or "explode" in parsed[0] or "zombie" in parsed[0] or "fall" in parsed[0] or "voice17" in parsed[0] or "itembeep2" in parsed[0] or "whiz" in parsed[0]: it=g.p.play_3d(parsed[0]+".ogg", g.me.x, g.me.y, g.me.z, round(string_to_number(parsed[1])), round(string_to_number(parsed[2])), round(string_to_number(parsed[3])), calculate_theta(dummy(g.facing)), False, False, True)
							if int(parsed[len(parsed)-1])!=100: it.start_pitch=int(parsed[len(parsed)-1])
							if int(parsed[len(parsed)-1])!=100: it.handle.pitch=int(parsed[len(parsed)-1])
						except: pass
				
			
		if(g.e.channel==20):
			parsed=string_split(g.e.message, " ",False)
			if(parsed[0]=="update_player") :
				x=string_to_number(parsed[1])
				y=string_to_number(parsed[2])
				z=string_to_number(parsed[3])
				map=parsed[4]
				name=parsed[5]
				update_player_coordinates(name,x,y,z,parsed[4],round(float(parsed[6])))
				
			
		
	
			if(parsed[0]=="update_player2") :
				x=string_to_number(parsed[1])
				y=string_to_number(parsed[2])
				z=string_to_number(parsed[3])
				map=parsed[4]
				name=parsed[5]
				update_player_coordinates2(name,x,y,z,parsed[4],round(float(parsed[6])))
				
			
		
	

g.netloop=netloop
def reset(resetpool=True):
	global inside_bus_handle
	if inside_bus_handle is not None:
		g.p.destroy_sound(inside_bus_handle)
		inside_bus_handle = None
	g.in_bus = False
	g.pinging=False
	g.inbike=False
	g.rainsnd.close()
	g.rain=False
	g.watching=""
	g.should_watch=False
	g.rainfinish=False
	g.cannotexit=False
	g.near2=False
	g.admin=False
	g.builder=False

	g.w=0
	g.w2=0
	g.weapons=["dummy"]
	g.mapready=False
	g.reply=""
	g.reloading=False
	g.mapmusic.stop()
	try: g.flash.volume=-100
	except: pass
	g.ingroup=False
	g.incommunity=False

	g.chat=True
	g.trackx=-1; g.tracky=-1; g.trackz=-1; g.tracked=False
	destroy_all_msounds()
	if g.inve:
		g.inve=False

		g.usesub=g.oldusesub
	g.can_move=True
	g.dmoving=False
	if g.media_player is not None: g.media_player.stop(); g.media_player.release(); g.media_player=None
	g.connected=False
	g.inthegame=False
	clear_map()
	g.pinging=False
	for i in g.players:
		try:
			if i.voice_sound is not None: i.voice_sound.close()
		except: pass
		try:
			if i.voice_sound2 is not None: i.voice_sound2.close()
		except: pass

		g.players.remove(i)
	if resetpool: g.p.destroy_all(); g.distpool.destroy_all()
	g.players.clear()
	g.connected=False
	g.weaponauto=False
	g.w=-1
	if resetpool: g.n.disconnect_peer(g.n.peer)
	destroy_all_sources()
	g.recording=False
	try: g.n.send_reliable(0,"voiceoff",0)
	except: pass
g.reset=reset
def is_sound_number(t):
	t=string_replace(t, ".", "", True)
	t=string_replace(t, "-", "", True)
	if(string_is_digits(t)):
		return True
	return False
	
	
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

def mouse_update():
	global middle_button_down, middle_button_pressed, MOUSE_X, MOUSE_Y, OLD_MOUSE_X, OLD_MOUSE_Y, MOUSE_Xreal, MOUSE_Yreal, scrollup, scrolldown
	scrollup=False
	scrolldown=False
	OLD_MOUSE_X=MOUSE_Xreal
	OLD_MOUSE_Y=MOUSE_Yreal
	MOUSE_Xreal, MOUSE_Yreal=pygame.mouse.get_pos()
	MOUSE_X=MOUSE_Xreal-OLD_MOUSE_X
	MOUSE_Y=MOUSE_Yreal-OLD_MOUSE_Y
	g.left_button_pressed=False
	middle_button_pressed=False
	g.right_button_pressed=False
	for event in g.lastevents:
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 4:
				scrollup=True
			elif event.button == 5:
				scrolldown=True

			if event.button == 1:
				g.left_button_down=True
				g.left_button_pressed=True
			elif event.button == 2:
				middle_button_down=True
				middle_button_pressed=True

			elif event.button == 3:
				g.right_button_down=True
				g.right_button_pressed=True
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				g.left_button_down=False
			if event.button == 2:
				middle_button_down=False

			elif event.button == 3:
				g.right_button_down=False
def mouse_down(button):
	if button == 0:
		return g.left_button_down
	elif button == 1:
		return g.right_button_down
	elif button == 2:
		return middle_button_down

	else:
		return False
def mouse_pressed(button):
	if button == 0:
		return g.left_button_pressed
	elif button == 1:
		return g.right_button_pressed
	elif button == 2:
		return middle_button_pressed

	else:
		return False

def check_if_already_running():
	current_pid = os.getpid()
	current_process = psutil.Process(current_pid)
	process_name = current_process.name()
	for proc in psutil.process_iter(['pid', 'name']):
		if proc.info['name'] == process_name and proc.info['pid'] != current_pid:
			return True
	return False
altimer=timer()
def mainloop():
	global parachute_sound,falling_sound
#	if g.sonartimer.elapsed>50 and g.sonar==1:
#		g.sonartimer.restart()
#		dirs=[north,east,south,west]
#		playeds=[]
#		for dir in dirs:
#			v=vector(g.me.x,g.me.y,g.me.z)
#			for i in range(20):
#				v=move(v.x,v.y,v.z,dir,0)
#				try: tile=get_tile_at(v.x,v.y,v.z)
#				except: tile=""
#				if "wall" in  tile and (v.x,v.y,v.z) not in playeds:
#					g.p.play_extended_3d(tile+".ogg", g.me.x, g.me.y, g.me.z, v.x, v.y, v.z, calculate_theta(g.facing), 0, 0, 0, 0, 0, 0, False, 0.0, 0.0, 0.0, 200.0, False)
#					playeds.append((v.x,v.y,v.z))
#					break
	if not hasattr(g,"sonar_dir_index"):
		g.sonar_dir_index=0
	if g.sonartimer.elapsed>200 and g.sonar==1:
		g.sonartimer.restart()
		playeds = set()
		dirs=[north,east,south,west]
		dir=dirs[g.sonar_dir_index]
		g.sonar_dir_index=(g.sonar_dir_index+1)%len(dirs)
		v=vector(g.me.x, g.me.y, g.me.z)
		for i in range(20):
			v=move(v.x, v.y, v.z,dir,0)
			try:
				tile=get_tile_at(v.x, v.y, v.z)
			except:
				tile=""
			if "wall" in tile:
				key=(v.x, v.y, v.z)
				if key not in playeds:
					g.p.play_extended_3d(tile + ".ogg", g.me.x, g.me.y, g.me.z, v.x, v.y, v.z,calculate_theta(g.facing), 0, 0, 0, 0, 0, 0, False,0.0, 0.0, 0.0, 200.0, False)
					playeds.add(key)
					break
	if g.drawing and g.drawtimer.elapsed>g.drawtime:
		g.drawing=False
	if g.usemouse==1 and mousetimer.elapsed>=0: mouse_update(); mousetimer.restart()
	if msoundtimer.elapsed>1000:
		msoundtimer.restart()
		if file_exists("lang/.lng"): file_delete("lang/.lng")
		for self in g.msounds:
			if g.mapname != self.map and self.loopint != -5:
				g.p.destroy_sound(self.loopint)
				g.msounds.remove(self)
	if altimer.elapsed>1000:
		altimer.restart()
		for pla in g.players:
			if pla.clearbuffertimer.elapsed>5000: pla.audio_buffer.clear(); pla.clearbuffertimer.restart(); pla.alplayed=False
		for pla in g.players:
			if pla.clearbuffertimer2.elapsed>5000: pla.audio_buffer2.clear(); pla.clearbuffertimer2.restart(); pla.alplayed2=False

	netloop()
	if g.awindow==1 and windowchecktimer.elapsed>500:
		windowchecktimer.restart()
		state=is_game_window_active()
		if not g.muted and not state:
			sound.listener._set_gain(0.00000001)
			g.muted=True
		elif g.muted and state:
			sound.listener._set_gain(g.mastervolume)
			g.muted=False

	sourcecheckloop()
	positions()
	g.mr.x=g.me.x
	g.mr.y=g.me.y

	if (g.jumping==True):
	
		if g.walktime>100: g.movetime=g.airtime
		elif g.walktime<100: g.movetime=g.walktime//2
		
	else:
	
		g.movetime=g.walktime
		
	if g.tracked==True and g.trackx==round(g.me.x) and g.tracky==round(g.me.y) and g.trackz==round(g.me.z):
		g.tracktimer.restart()
		g.tracked=False
		g.p.play_extended_3d("misc53.ogg", g.me.x, g.me.y, g.me.z, g.trackx, g.tracky, g.trackz, calculate_theta(g.facing), 0, 0, 0, 0, 0, 0, False, 0.0, 0.0, 0.0, 30.0, False)
		g.trackx=-1; g.tracky=-1; g.trackz=-1


	if g.track2timer.elapsed>=90 and g.tracked==True and g.trackx==round(g.me.x):
		g.track2timer.restart()
#		g.p.play_stationary_extended("misc53.ogg", 0, 0, 0, 0, 0, 0, False, 0.0, 0.0, 0.0, 130.0, False)
		g.p.play_stationary_extended("misc53.ogg",False,0,0,0,130,False,False)
	if g.tracktimer.elapsed>=250 and g.tracked==True:
		g.tracktimer.restart()
		g.p.play_extended_3d("misc53.ogg", g.me.x, g.me.y, g.me.z, g.trackx, g.tracky, g.trackz, calculate_theta(g.facing), 0, 0, 0, 0, 0, 0, False, 0.0, 0.0, 0.0, 100.0, False)

	fallloop()
	fallingloop()
g.mainloop=mainloop
def death():
	g.cannotexit=False
	g.p.play_stationary("misc331.ogg",False)
	g.p.play_stationary("misc333.ogg",False)
	g.p.play_stationary("misc334.ogg",False)

	pause_all_sources()
	g.loldietimer.restart()
	while(True):
		process_events()
		mainloop()
		if g.loldietimer.elapsed>=3500:
			m.reset(True)
			m.allow_escape=False
			m.callback2=mainloop
			m.add_item_tts("Watch the match","watch")
			m.add_item_tts("Go back to lobby","lobby")
			mres=m.run("Select an option",True)
			if mres==0 or m.get_item_name(mres)=="lobby": speak("Respawning"); g.n.send_reliable(0, "regenerate2", 0)
			else: speak("Watching the match"); g.n.send_reliable(0, "regenerate", 0)

			break
	resume_all_sources()
	g.aim=0
	g.n.send_reliable(0,"aim "+str(g.aim),0)
	g.distpool.update_listener_3d(g.me.x, g.me.y, g.me.z, calculate_theta(dummy(g.facing)))
	g.p.update_listener_3d(g.me.x, g.me.y, g.me.z, calculate_theta(dummy(g.facing)))

def exitfunction():
	if g.inve: g.n.send_reliable(0,"outmotor",0); return
	if g.watching!="":
		g.should_watch=False
		g.n.send_reliable(0,"matchwatchstop",0); g.aim=0
		return
	if g.died: return
	if g.mapname!="lobby" and g.cannotexit: speak("You have to wait 1 minutes to be able to exit after hit"); return
	if g.mapname!="lobby" and g.near2: speak("You cannot exit because someone near you"); return
	speak("Are you sure to leave the game, press escape or the left D-pad button of the joystick to cancel, press enter or the right D-pad button of the joystick to disconnect.")
	while(True):
		process_events()
		mainloop()
		if(key_pressed(K_UP) or key_pressed(K_DOWN) or key_pressed(K_LEFT) or key_pressed(K_RIGHT)):
		
				speak("Are you sure to leave the game, press escape or the left D-pad button of the joystick to cancel, press enter or the right D-pad button of the joystick to disconnect.")

			
		if(key_pressed(K_ESCAPE) or g.stick is not None and g.stick.get_hat(0)==(-1,0)):
			waitjoyhat()
			speak("canceled")
			return
		if(key_pressed(K_RETURN) or key_pressed(pygame.K_KP_ENTER or g.stick is not None and g.stick.get_hat(0)==(1,0))):
		
			waitjoyhat()
			speak("exiting...")
			g.n.send_reliable(0, "close", 0)
			g.x=True
			g.xtimer.restart()

			return
			
		
	

def fallloop():
	if g.holding_wall: return
	if g.jumping and g.me.z!=g.jumplandz: pass
	if(g.jumptimer.elapsed > g.jumptime and g.jumping==True):
	
		g.jumptimer.restart()
		if 1:
			if 1:
				if g.me.z!=g.jumplandz and get_tile_at(g.me.x,g.me.y,g.jumplandz)!="" and get_tile_at(g.mr.x, g.mr.y, g.me.z)!="" and not get_tile_at(g.mr.x, g.mr.y, g.me.z).startswith("wall") and get_tile_at(g.mr.x, g.mr.y, g.me.z)!="air" and get_staircase_at(g.me.x,g.me.y,g.me.z)=="":
				
					g.jumplandz=g.me.z
					
					g.p.play_stationary(get_tile_at(g.mr.x, g.mr.y, g.me.z)+"land.ogg", False)
					g.n.send_reliable(0, "land", 0)
					g.jumping=False
					return


		if(g.jumpup==1):
		
			if(g.me.z <=g.jumplandz2+5):
			
				g.me.z+=1
				g.n.send_unreliable(0, "move_to_a "+str(g.me.x)+" "+str(g.me.y)+" "+str(g.me.z)+"", 0)
				if get_tile_at(g.mr.x, g.mr.y, g.me.z)!="" and get_tile_at(g.mr.x, g.mr.y, g.me.z).startswith("wall"):
					g.jumpup=0
					g.p.play_stationary(get_tile_at(g.mr.x, g.mr.y, g.me.z)+".ogg",False)
					return
			else:
			
				g.jumpup=0
				
			
		elif(g.jumpup==0):
		
			if(g.me.z > g.jumplandz):
			
				g.me.z-=1
				g.n.send_unreliable(0, "move_to_a "+str(g.me.x)+" "+str(g.me.y)+" "+str(g.me.z), 0)
			else:
			
				if(get_tile_at(g.mr.x, g.mr.y, g.me.z)=="" or get_tile_at(g.mr.x, g.mr.y, g.me.z)=="air"):
				
					g.jumping=False
					g.falling=True
					g.falldistance=0
					g.falltimer.restart()
					g.p.play_stationary("fall.ogg", False)
					g.n.send_reliable(0, "fall", 0)

					return
					
				g.n.send_reliable(0, "land", 0)
				g.p.play_stationary(get_tile_at(g.mr.x, g.mr.y, g.me.z)+"land.ogg", False)

				g.jumping=False
				
			
		
	
g.fallloop=fallloop
def fallcheck():
	if not g.mapready or g.holding_wall: return
	if g.inve: return
	if(get_tile_at(g.mr.x, g.mr.y, g.me.z)=="" and g.falling==False and g.jumping==False or get_tile_at(g.mr.x, g.mr.y, g.me.z)=="air" and g.falling==False and g.jumping==False and g.me.z>0):
	
		if g.watching=="":
			g.falling=True
			g.falldistance=0
			g.falltimer.restart()
			if g.watching=="": g.p.play_stationary("fall.ogg", False)
			if g.watching=="": g.n.send_reliable(0, "fall", 0)
		
	
def fallingloop():
	if g.holding_wall: return
	if g.watching!="": return
	if(g.falling==True and g.falltimer.elapsed > g.falltime):
	
		if(get_tile_at(g.mr.x, g.mr.y, g.me.z)!="" and not get_tile_at(g.me.x, g.me.y, g.me.z).startswith("wall") and get_tile_at(g.mr.x, g.mr.y, g.me.z)!="air"):
		
			g.falling=False
			if falling_sound is not None: g.p.destroy_sound(falling_sound)
			if parachute_sound is not None: g.p.destroy_sound(parachute_sound)
			if(g.falldistance < 10):
			
				g.p.play_stationary(get_tile_at(g.mr.x, g.mr.y, g.me.z)+"land.ogg", False)
				if g.watching=="": g.n.send_reliable(0, "land", 0)
				g.falling=False
				
			else:
			
				if g.parachute==True:
					g.p.play_stationary(get_tile_at(g.mr.x, g.mr.y, g.me.z)+"land.ogg", False)
				else:
					#g.p.play_stationary(get_tile_at(g.mr.x, g.mr.y, g.me.z)+"fall.ogg", False)
					if g.watching=="": g.n.send_reliable(0, "hardland "+str(g.falldistance)+"", 0)
				g.falling=False
				if g.watching=="": g.n.send_unreliable(0, "move_to_a "+str(g.me.x)+" "+str(g.me.y)+" "+str(g.me.z)+"", 0)
				
			return
			
		g.falltimer.restart()
		g.falldistance+=1
		g.me.z-=1
		if g.watching=="": g.n.send_unreliable(0, "move_to_a "+str(g.me.x)+" "+str(g.me.y)+" "+str(g.me.z)+"", 0)
		
	
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
def zeroloop():
	process_events()
	if g.walktime<40: g.walktime=40
	if g.tiletimer.elapsed>1000: g.tiletimer.restart(); g.tile_count=0
	if anticheattimer.elapsed>1000:
		anticheattimer.restart()
		anticheat_check()
		if is_cheater(): g.n.send_reliable(0,"cheat "+g.name,0)
	if alt_is_down() and key_pressed(K_f):
		g.p.play_stationary("turnfacing.ogg",False)
		g.n.send_reliable(0,"xplay turnfacing",0)
		if g.aim_mode==0:
			g.aim_mode=1
			speak("angle-based aiming")
			g.aim=0
			g.n.send_reliable(0,"aim 0",0)
			g.n.send_reliable(0,"aimmode 1",0)
			g.p.update_listener_3d(g.me.x, g.me.y, g.me.z, calculate_theta(dummy(g.facing)))
		elif g.aim_mode==1:
			g.aim_mode=0
			speak("step-based aiming")
			g.aim=0
			g.n.send_reliable(0,"aim 0",0)
			g.n.send_reliable(0,"aimmode 0",0)
			g.p.update_listener_3d(g.me.x, g.me.y, g.me.z, calculate_theta(dummy(g.facing)))
		return
	if 1:
		if g.inbike and (key_pressed(K_a) or key_pressed(K_LEFT)):
			if g.can_move and key_up(K_g) and g.watching=="" and not shift_is_down():
				if not alt_is_down(): g.facing=getdir(turnleft(getdir(g.facing)))
				if alt_is_down(): g.facing=getdir(turnleft(getdir(g.facing),90))
				if g.speakfacing==1: speak(dir_to_string(g.facing))
				g.p.play_stationary("turn.ogg",False)
				if g.mapname!="lobby": g.n.send_reliable(0,"xplay turn",0)
				g.n.send_reliable(0,"facing "+str(g.facing),0)
				return
			
		if g.inbike and (key_pressed(K_d) or key_pressed(K_RIGHT)):
		
			if g.can_move and g.watching=="" and key_up(K_g) and not shift_is_down():
				if not alt_is_down(): g.facing=getdir(turnright(getdir(g.facing)))
				if alt_is_down(): g.facing=getdir(turnright(getdir(g.facing),90))
				if g.speakfacing==1: speak(dir_to_string(g.facing))
				g.p.play_stationary("turn.ogg",False)
				if g.mapname!="lobby": g.n.send_reliable(0,"xplay turn",0)
				g.n.send_reliable(0,"facing "+str(g.facing),0)
				return
			



	if g.stopaim!=0: g.stopaim=0
	if key_pressed(K_SPACE) and g.inbike and bikehorntimer.elapsed>2000: bikehorntimer.restart(); g.n.send_reliable(0,"bikehorn",0); return
	if key_up(K_g) and g.inbike and key_down(K_UP) and biketimer.elapsed>400: biketimer.restart(); g.n.send_reliable(0,"bikemove",0); return
	if g.inbike and key_pressed(K_ESCAPE): g.n.send_reliable(0,"bikeexit",0); return
	if g.autotrack==1 and autotracktimer.elapsed>0:
		autotracktimer.restart()
		for pl in g.players:
			if pl.autotracktimer.elapsed>300 and get_3d_distance(g.me.x,g.me.y,g.me.z,pl.x,pl.y,pl.z)<=30 and pl.map==g.mapname: g.p.play_3d("beep.ogg",g.me.x,g.me.y,g.me.z,pl.x,pl.y,pl.z,calculate_theta(g.facing),False); pl.autotracktimer.restart()
	if g.rain and g.rainfadein  and rainfadeintimer.elapsed>100:
		rainfadeintimer.restart()
		try: g.rainsnd.volume+=1
		except: pass
		try:
			if g.rainsnd.volume>=0: g.rainfadein=False
		except: pass
	if g.rain and g.rainsnd is not None and g.rainsnd.player is not None:
		if g.rainsnd.volume!=g.target_rain_volume and rainfadeintimer.elapsed>100:
			rainfadeintimer.restart()
			if g.rainsnd.volume>g.target_rain_volume: g.rainsnd.volume-=1
			elif g.rainsnd.volume<g.target_rain_volume: g.rainsnd.volume+=1
	if key_down(K_BACKSPACE) and g.jumping and not g.holding_wall:
		v=move(g.me.x,g.me.y,g.me.z,g.facing,0)
		if "wall" in get_tile_at(v.x,v.y,v.z):
			g.holding_wall=True
			g.p.play_stationary("misc178.ogg",False)
	if not key_down(K_BACKSPACE) and g.jumping and g.holding_wall:
		g.holding_wall=False
		g.p.play_stationary("fall.ogg",False)
	if g.mapname=="lobby" and g.rain:
		if not g.rainsnd.paused: g.rainsnd.pause()
	if g.mapname!="lobby" and g.rain:
		if g.rainsnd.paused: g.rainsnd.play()

	if g.oldfacing!=g.facing and turnsoundtimer.elapsed<=2000: 		g.oldfacing=g.facing
	if g.oldfacing!=g.facing and turnsoundtimer.elapsed>2000:
		turnsoundtimer.restart()
		g.oldfacing=g.facing
		r=random(1,10)
		if g.weapons[g.w] in guns or g.weapons2[g.w2] in guns:
			if g.weapons[g.w]=="punch" and g.weapons2[g.w2] not in guns: return
			g.p.play_stationary("weaponturn"+str(r)+".ogg",False)
			g.n.send_reliable(0,"xplay weaponturn"+str(r),0)
	if g.me.z==0:
		if parachute_sound is not None: g.p.destroy_sound(parachute_sound)
		if falling_sound is not None: g.p.destroy_sound(falling_sound)
	if g.rain:
		rs=get_rain_sound()
		if g.rainsound!=rs:
			if g.rainsnd.player is not None: v=g.rainsnd.volume
			try: g.rainsnd.close()
			except: pass
			try: g.rainsnd.load(rs)
			except: pass
			g.rainsnd.player.alhrtf=False
			g.rainsnd.player.stationary=True

			try: g.rainsnd.volume=v
			except: pass
			try: g.rainsnd.play_looped()
			except: pass
			g.rainsound=rs


	msoundloop()
	if key_pressed(K_F7):
		if g.sonar==0:
			g.sonar=1
			speak("sonar on")
			g.writeprefs()
		elif g.sonar==1:
			g.sonar=0
			speak("sonar off")
			g.writeprefs()

	if shift_is_down():
		if ctimer.elapsed>2000 and left_control_is_down(): g.n.send_reliable(0,"weaponfire",0); ctimer.restart()
		if ctimer2.elapsed>2000 and right_control_is_down(): g.n.send_reliable(0,"weaponfire2",0); ctimer2.restart()
	if g.aim>get_max_aim():
		g.aim=get_max_aim()
		g.n.send_reliable(0,"aim "+str(g.aim),0)
	if g.mapname=="lobby" and g.trackx!=-1:
					g.trackx = -1
					g.tracky = -1
					g.tracked = False

	if g.standing and g.standingtimer.elapsed>1400:
		g.standing=False
		g.n.send_reliable(0,"sitstop",0)
		g.sitting=False
	if alt_is_down():
		if g.qturn==0:
			if g.can_move and g.watching=="" and key_pressed(K_w) and g.usesub==1:
				g.facing=getdir(turnleft(getdir(g.facing),180))
				if g.speakfacing==1: speak(dir_to_string(g.facing))
				g.p.play_stationary("turn.ogg",False)
				if g.mapname!="lobby": g.n.send_reliable(0,"xplay turn",0)
				g.n.send_reliable(0,"facing "+str(g.facing),0)
				return
			if g.watching=="" and g.can_move and key_pressed(K_s) and g.usesub==1:
				g.facing=getdir(turnright(getdir(g.facing),180))
				if g.speakfacing==1: speak(dir_to_string(g.facing))
				g.p.play_stationary("turn.ogg",False)
				if g.mapname!="lobby": g.n.send_reliable(0,"xplay turn",0)
				g.n.send_reliable(0,"facing "+str(g.facing),0)
				return

			if g.watching=="" and g.can_move and key_pressed(K_UP) and g.usesub==0:
				g.facing=getdir(turnleft(getdir(g.facing),180))
				if g.speakfacing==1: speak(dir_to_string(g.facing))
				g.p.play_stationary("turn.ogg",False)
				if g.mapname!="lobby": g.n.send_reliable(0,"xplay turn",0)
				g.n.send_reliable(0,"facing "+str(g.facing),0)
				return
			if g.watching=="" and g.can_move and key_pressed(K_DOWN) and g.usesub==0:
				g.facing=getdir(turnright(getdir(g.facing),180))
				if g.speakfacing==1: speak(dir_to_string(g.facing))
				g.p.play_stationary("turn.ogg",False)
				if g.mapname!="lobby": g.n.send_reliable(0,"xplay turn",0)
				g.n.send_reliable(0,"facing "+str(g.facing),0)
				return
		else:
			if g.watching=="" and g.can_move and key_pressed(K_a) and g.qturn==1:
				g.facing=getdir(turnleft(getdir(g.facing),180))
				if g.speakfacing==1: speak(dir_to_string(g.facing))
				g.p.play_stationary("turn.ogg",False)
				if g.mapname!="lobby": g.n.send_reliable(0,"xplay turn",0)
				g.n.send_reliable(0,"facing "+str(g.facing),0)
				return
			if g.watching=="" and g.can_move and key_pressed(K_d) and g.qturn==1:
				g.facing=getdir(turnright(getdir(g.facing),180))
				if g.speakfacing==1: speak(dir_to_string(g.facing))
				g.p.play_stationary("turn.ogg",False)
				if g.mapname!="lobby": g.n.send_reliable(0,"xplay turn",0)
				g.n.send_reliable(0,"facing "+str(g.facing),0)
				return


	if shift_is_down() and key_pressed(K_p):
		if g.watching=="" and not g.cannotexit: g.n.send_reliable(0,"accounts",0)
		else:
			if g.watching=="": speak("You cannot do this after hit")
	if not g.ducking and key_pressed(K_1):
		if shift_is_down():
			if alt_is_down():
				if g.w2!=0: g.n.send_reliable(0,"unequip2",0); g.w2=0
				else:
					if g.can_move and g.weapondrawtimer.elapsed>=50 and g.getknife==False and g.mapname!="lobby" and not g.zombie and g.reloading==False and "one_shot_one_kill" not in g.mapname and not g.drawing:
						g.weapondrawtimer.restart()
						speak("feet")
						if "minecraft" not in g.mapname: g.n.send_reliable(0, "draw2 feet", 0)
						if "minecraft" in g.mapname: g.n.send_reliable(0, "draw2 stick", 0)
						g.weapons2.append("feet")
						g.w2=len(g.weapons2)-1
						#if g.w!=0 and g.weapons[g.w]=="punch": g.n.send_reliable(0,"unequip",0); g.w=0
			if not alt_is_down() and not g.zombie: g.n.send_reliable(0,"unequip",0); g.w=0
			return
	if g.cannotexit and g.cannotexittimer.elapsed>g.cannotexittime:
		g.cannotexit=False
	if not g.inve and g.walktime==25: g.walktime=g.oldwalktime
	if not g.dmoving and tilechecktimer.elapsed>1000:
		tilechecktimer.restart()
		tile=get_tile_at(g.me.x,g.me.y,g.me.z)
		if not g.inve and not g.jumping and tile.startswith("wall"):
			tile2=get_tile_at(g.me.x+1,g.me.y,g.me.z)
			tile3=get_tile_at(g.me.x-1,g.me.y,g.me.z)
			tile4=get_tile_at(g.me.x,g.me.y+1,g.me.z)
			tile5=get_tile_at(g.me.x,g.me.y-1,g.me.z)
			if tile4!="" and not tile4.startswith("wall"):  g.me.y+=1; return
			if tile5!="" and not tile5.startswith("wall"):  g.me.y-=1; return

			if tile2!="" and not tile2.startswith("wall"):  g.me.x+=1; return
			if tile3!="" and not tile3.startswith("wall"):  g.me.x-=1; return
	if g.pcleartimer.elapsed>500:
		g.pcleartimer.restart()
		g.p1.clear();g.p2.clear();g.p3.clear();g.p4.clear()
	if g.stick is not None and g.stick.get_hat(0)==(0,0): weaponswitchtimer.force(180)
	if g.fastwalk==0 and not g.ducking and not alt_is_down() and g.walktime!=g.minwalktime: g.walktime=g.minwalktime
	if g.fastwalk==1 and not g.ducking and not walking() and g.walktime!=g.minwalktime: g.walktime=g.minwalktime
	if not shift_is_down() and alt_is_down():
					if key_pressed(K_1):
						g.invcategory="weapons"
						cycle_inv(1 if not shift_is_down() else 0)
					if key_pressed(K_2):
						g.invcategory="ammos"
						cycle_inv(1 if not shift_is_down() else 0)
					if key_pressed(K_3):
						g.invcategory="drinks"
						cycle_inv(1 if not shift_is_down() else 0)

					if key_pressed(K_4):
						g.invcategory="explosives"
						cycle_inv(1 if not shift_is_down() else 0)

					if key_pressed(K_5):
						g.invcategory="equipment"
						cycle_inv(1 if not shift_is_down() else 0)



	if shift_is_down()==True:
		if(g.kpgup.pressing()):
			g.mapmusicoldversion+=1
			g.mapmusic.volume=g.mapmusicoldversion
			g.writeprefs()
		elif(g.kpgdn.pressing()):
			g.mapmusicoldversion-=1
			g.mapmusic.volume=g.mapmusicoldversion
			g.writeprefs()
	if alt_is_down() and not shift_is_down() and key_pressed(K_v): g.n.send_reliable(0,"talking",0)
	if not alt_is_down() and shift_is_down() and key_pressed(K_v):
		g.push=not g.push

		speak("Push to talk off" if g.push==0 else "push to talk on")
		if g.push==1: g.p.play_stationary("voice_active.ogg")
		elif g.push==0: g.p.play_stationary("voice_disable.ogg")
		g.writeprefs()
		return
	if g.voicechat==0 and g.recording:
		g.recording=False
		try: g.n.send_reliable(0,"voiceoff",0)
		except: pass

	if g.push==0:
		if not g.recording2 and not alt_is_down() and not shift_is_down() and key_pressed(K_v):
			if g.voicechat==0:
				if g.voicepresstimer.elapsed>=1000:
					g.voicepresstimer.restart()
					speak("You disabled receiving voice chats.")
					return
			else:
				if pstream is None: speak("Error. No input device configured. Please set your input device from game settings."); return
				g.recording=not g.recording
				if not g.recording:
					try: g.n.send_reliable(0,"voiceoff",0)
					except: pass
				if g.recording:
					try: g.n.send_reliable(0,"voiceon",0)
					except: pass


				Thread(target=record_voice).start()
				if g.recording==True: g.p.play_stationary("voice_on.ogg"); speak("Microphone activated")
				elif g.recording==False: g.p.play_stationary("voice_off.ogg"); speak("Microphone disabled")


				return
	if g.push==1:
		if not g.recording and not g.recording2 and not alt_is_down() and not shift_is_down() and key_down(K_v):
			if g.voicechat==0:
				if g.voicepresstimer.elapsed>=1000:
					g.voicepresstimer.restart()
					speak("You disabled receiving voice chats.")
					return
			else:
				if pstream is None: speak("Error. No input device configured. Please set your input device from game settings."); return
				g.recording=True
				g.recording2=False
				if g.recording:
					try: g.n.send_reliable(0,"voiceon",0)
					except: pass

				Thread(target=record_voice).start()
				if g.recording==True: g.p.play_stationary("voice_on.ogg")
				elif g.recording==False: g.p.play_stationary("voice_off.ogg")

				return

		if g.recording and not shift_is_down() and not alt_is_down() and key_up(K_v):
			if g.voicechat==0:
				if g.voicepresstimer.elapsed>=1000:
					g.voicepresstimer.restart()
					speak("You disabled receiving voice chats.")
					return
			else:
				g.recording=False
				if not g.recording:
					try: g.n.send_reliable(0,"voiceoff",0)
					except: pass

				g.p.play_stationary("voice_off.ogg")
				return


	if alt_is_down() and not shift_is_down() and key_pressed(K_b):
		if g.incommunity==False:
			if g.voicepresstimer.elapsed>1000:
				speak("you are not in a community")
				g.voicepresstimer.restart()
			return
		g.n.send_reliable(0,"talking2",0)
	if not alt_is_down() and shift_is_down() and key_pressed(K_b):
		if g.incommunity==False:
			if g.voicepresstimer.elapsed>1000:
				speak("you are not in a community")
				g.voicepresstimer.restart()
			return
		g.push2=not g.push2

		speak("Push to talk off" if g.push2==0 else "push to talk on")
		if g.push2==1: g.p.play_stationary("voice_active.ogg")
		elif g.push2==0: g.p.play_stationary("voice_disable.ogg")
		g.writeprefs()
		return
	if (not g.incommunity or g.voicechat2==0) and g.recording2:
		g.recording2=False
		try: g.n.send_reliable(0,"voiceoff2",0)
		except: pass

	if g.push2==0:
		if not g.recording and not alt_is_down() and not shift_is_down() and key_pressed(K_b):
			if g.incommunity==False:
				if g.voicepresstimer.elapsed>1000:
					speak("you are not in a community")
					g.voicepresstimer.restart()
				return
			if g.voicechat2==0:
				if g.voicepresstimer2.elapsed>=1000:
					g.voicepresstimer2.restart()
					speak("You disabled receiving voice chats.")
					return
			else:
				if pstream is None: speak("Error. No input device configured. Please set your input device from game settings."); return
				g.recording2=not g.recording2
				if not g.recording2:
					try: g.n.send_reliable(0,"voiceoff2",0)
					except: pass
				if g.recording2:
					try: g.n.send_reliable(0,"voiceon2",0)
					except: pass


				Thread(target=record_voice2).start()
				if g.recording2==True: g.p.play_stationary("voice_on.ogg"); speak("community microphone activated")
				elif g.recording2==False: g.p.play_stationary("voice_off.ogg"); speak("community Microphone disabled")


				return
	if g.push2==1:
		if not g.recording2 and not g.recording and not alt_is_down() and not shift_is_down() and key_down(K_b):
			if g.incommunity==False:
				if g.voicepresstimer.elapsed>1000:
					speak("you are not in a community")
					g.voicepresstimer.restart()
				return
			if g.voicechat2==0:
				if g.voicepresstimer2.elapsed>=1000:
					g.voicepresstimer2.restart()
					speak("You disabled receiving voice chats.")
					return
			else:
				if pstream is None: speak("Error. No input device configured. Please set your input device from game settings."); return
				g.recording2=True
				g.recording=False
				if g.recording2:
					try: g.n.send_reliable(0,"voiceon2",0)
					except: pass

				Thread(target=record_voice2).start()
				if g.recording2==True: g.p.play_stationary("voice_on.ogg")
				elif g.recording2==False: g.p.play_stationary("voice_off.ogg")

				return

		if g.recording2 and not shift_is_down() and not alt_is_down() and key_up(K_b):
			if g.incommunity==False:
				if g.voicepresstimer.elapsed>1000:
					speak("you are not in a community")
					g.voicepresstimer.restart()
				return
			if g.voicechat2==0:
				if g.voicepresstimer2.elapsed>=1000:
					g.voicepresstimer2.restart()
					speak("You disabled receiving voice chats.")
					return
			else:
				g.recording2=False
				if not g.recording2:
					try: g.n.send_reliable(0,"voiceoff2",0)
					except: pass

				g.p.play_stationary("voice_off.ogg")
				return




	if (scrolldown or g.stick is not None and g.stick.get_hat(0)==(0,-1) and weaponswitchtimer.elapsed>180) and g.mapname!="lobby" and not g.zombie and g.reloading==False and not g.drawing and not g.sitting and not g.drawing:
		waitjoyhat()
		weaponswitchtimer.restart()

		ind=g.ww+1
		if ind>len(guns)-1:
			ind=len(guns)-1
			return
		if guns[ind]!="feet" and guns[ind]!="punch":

			while True:

				if ind>=len(guns):
					return

				if get_item_count(guns[ind])>0: break
				ind+=1
		g.ww=ind
		g.n.send_reliable(0,"draw "+guns[g.ww],0)
		speak(guns[g.ww])
		g.weapons.append(guns[g.ww])
		g.w=(len(g.weapons)-1)

	if (scrollup or g.stick is not None and g.stick.get_hat(0)==(0,1) and weaponswitchtimer.elapsed>180) and g.mapname!="lobby" and not g.zombie and not g.sitting and g.reloading==False and not g.drawing:
		waitjoyhat()
		weaponswitchtimer.restart()
		ind=g.ww-1
		if ind<0:
			ind=0
			return
		if guns[ind]!="punch" and guns[ind]!="feet":
			while True:

				if ind<0:
					return

				if get_item_count(guns[ind])>0: break
				ind-=1


		g.ww=ind
		g.n.send_reliable(0,"draw "+guns[g.ww],0)
		speak(guns[g.ww])
		g.weapons.append(guns[g.ww])
		g.w=(len(g.weapons)-1)


	if not alt_is_down() and not shift_is_down() and g.can_move and key_pressed(K_1) and g.weapondrawtimer.elapsed>=50 and g.getknife==False and g.mapname!="lobby" and not g.zombie and g.reloading==False and not g.drawing and "one_shot_one_kill" not in g.mapname and not g.sitting and not g.ducking:
		g.weapondrawtimer.restart()
		speak("punch")
		if "minecraft" not in g.mapname: g.n.send_reliable(0, "draw punch", 0)
		if "minecraft" in g.mapname: g.n.send_reliable(0, "draw stick", 0)
		g.weapons.append("punch")
		g.w=len(g.weapons)-1
		#if g.w2!=0 and g.weapons2[g.w2]=="feet": g.n.send_reliable(0,"unequip2",0); g.w2=0
	if alt_is_down() and shift_is_down() and g.can_move and key_pressed(K_1) and g.weapondrawtimer.elapsed>=50 and g.getknife==False and g.mapname!="lobby" and not g.zombie and g.reloading==False and not g.drawing and "one_shot_one_kill" not in g.mapname and not g.sitting and not g.ducking:
		g.weapondrawtimer.restart()
		speak("feet")
		if "minecraft" not in g.mapname: g.n.send_reliable(0, "draw2 feet", 0)
		if "minecraft" in g.mapname: g.n.send_reliable(0, "draw2 stick", 0)
		g.weapons2.append("feet")
		g.w2=len(g.weapons2)-1
		#if g.w!=0 and g.weapons[g.w]=="punch": g.n.send_reliable(0,"unequip",0); g.w=0

	mainloop()
	if g.usemouse == 1:


		if g.mapname!="lobby" and g.mousex != MOUSE_X*1 and MOUSE_X!=0 and g.fupdatetimer.elapsed>=0 and g.can_move:
			g.mousex = MOUSE_X*1


			oldfacing=dir_to_string(getdir(g.facing))
			g.facing += g.mousex
	
			if g.facing < 0:
				g.facing = 360
			elif g.facing >= 360:
				g.facing = 0
			g.facing=round(g.facing)
			g.n.send_reliable(0, "facing " + str(g.facing), 0)

			
	signloop()
	doorcheckloop()
	if alt_is_down() and key_pressed(K_p):
		g.n.send_reliable(0, "build", 0)
	if(key_down(K_g) and g.watching==""):
	
		if(key_pressed(K_t) and g.admin or g.builder):
		
			speak(gct()+" at "+str(round(g.camera.x))+" , "+str(round(g.camera.y))+", "+str(round(g.camera.z)))
			playcamera()
			return
			
		if(get_staircase_at(g.camera.x, g.camera.y, g.camera.z)=="" and g.kpgdn.pressing()):
		
			g.camera.z-=1
			playcamera()
			if string_contains(get_tile_at(g.camera.x, g.camera.y, g.camera.z), "wall", 1) > -1:
				g.camera.z += 1
			
		if(get_staircase_at(g.camera.x, g.camera.y, g.camera.z)=="" and g.kpgup.pressing()):
		
			g.camera.z+=1
			playcamera()

			if string_contains(get_tile_at(g.camera.x, g.camera.y, g.camera.z), "wall", 1) > -1:
				g.camera.z -= 1
			
		if(g.usesub==0 and g.ka.pressing() and g.camera.x>0):
		
			cameramove(Left)
			
		if(g.usesub==1 and g.kleft.pressing() and g.camera.x>0):
		
			cameramove(Left)
			

		if(g.usesub==0 and g.kd.pressing() and g.camera.x<g.max.x):
		
			cameramove(Right)
			
		if(g.usesub==1 and g.kright.pressing() and g.camera.x<g.max.x):
		
			cameramove(Right)
			


		if(g.usesub==0 and g.ks.pressing() and g.camera.y>0):
		
			cameramove(Backward)
			

		if(g.usesub==0 and g.ks.pressing() and g.camera.y>0):
		
			cameramove(Backward)
			
		if(g.usesub==1 and g.kdown.pressing() and g.camera.y>0):
		
			cameramove(Backward)
			


		if(g.usesub==0 and g.kw.pressing() and g.camera.y<g.max.y):
		
			cameramove(Forward)
			
		
		if(g.usesub==1 and g.kup.pressing() and g.camera.y<g.max.y):
		
			cameramove(Forward)
			
		

	if (key_up(K_g)):
	
		g.camera.x=g.me.x
		g.camera.y=g.me.y
		g.camera.z=g.me.z
		
	if(not shift_is_down() and not alt_is_down() and key_pressed(K_z)):
	
		if (g.mapname=="massacre_in_the_city" or g.mapname=="helicopter") and g.watching!="":
			speak("While watching someone on this map, you cannot look at their location")
		else:
			speak("Current area: "+(g.currentloc if g.currentloc!="" else "unknown area")+"")
		
	if(key_pressed(K_F1)):
		g.n.send_reliable(0,"motd",0)
	if(key_pressed(K_F2) and g.pinging==False):
	
		g.pingpool.play_extended_3d("misc128.ogg", g.me.x+3, g.me.y, g.me.z, g.me.x, g.me.y, g.me.z, calculate_theta(0), 0, 0, 0, 0, 0, 0, False, 0.0, 0.0, 0.0, 150.0, False)
		g.pinging=True
		g.pingtimer.restart()
		g.n.send_reliable(0,"ping",0)
	if key_pressed(K_F3):
		g.n.send_reliable(0,"beacontoggle",0)
	if not g.sitting and g.mapname!="lobby":
		if g.can_move and not shift_is_down() and not alt_is_down() and g.reloading==False and not g.drawing:
			if not g.zombie:
				if not g.ducking and key_pressed(K_2):
					if g.focus2 == "":
						pass
					else:
						if not g.candraw and g.weapons2[g.w2] in cannotdraw: return
						if g.weapons[g.w] == g.focus2:
							speak("You already draw this weapon.")
						else:
							if get_item_count(g.focus2)>0:
								g.n.send_reliable(0, "draw "+g.focus2+"", 0)
								speak(g.focus2)
								g.weapons.append(g.focus2)
								g.w=len(g.weapons)-1
								if g.weapons2[g.w2]==g.weapons[g.w]: g.n.send_reliable(0,"unequip2",0); g.w2=0
				if not g.ducking and key_pressed(K_3):
					if g.focus3 == "":
						pass
					else:
						if not g.candraw and g.weapons2[g.w2] in cannotdraw: return
						if g.weapons[g.w] == g.focus3:
							speak("You already draw this weapon.")
						else:
							if get_item_count(g.focus3)>0:
								g.n.send_reliable(0, "draw "+g.focus3+"", 0)
								speak(g.focus3)
								g.weapons.append(g.focus3)
								g.w=len(g.weapons)-1
								if g.weapons2[g.w2]==g.weapons[g.w]: g.n.send_reliable(0,"unequip2",0); g.w2=0
				if not g.ducking and key_pressed(K_4):
					if g.focus4 == "":
						pass
					else:
						if not g.candraw and g.weapons2[g.w2] in cannotdraw: return
						if g.weapons[g.w] == g.focus4:
							speak("You already draw this weapon.")
						else:
							if get_item_count(g.focus4)>0:
								g.n.send_reliable(0, "draw "+g.focus4+"", 0)
								speak(g.focus4)
								g.weapons.append(g.focus4)
								g.w=len(g.weapons)-1
								if g.weapons2[g.w2]==g.weapons[g.w]: g.n.send_reliable(0,"unequip2",0); g.w2=0
				if not g.ducking and key_pressed(K_5):
					if g.focus5 == "":
						pass
					else:
						if not g.candraw and g.weapons2[g.w2] in cannotdraw: return
						if g.weapons[g.w] == g.focus5:
							speak("You already draw this weapon.")
						else:
							if get_item_count(g.focus5)>0:
								g.n.send_reliable(0, "draw "+g.focus5+"", 0)
								speak(g.focus5)
								g.weapons.append(g.focus5)
								g.w=len(g.weapons)-1
								if g.weapons2[g.w2]==g.weapons[g.w]: g.n.send_reliable(0,"unequip2",0); g.w2=0
				if not g.ducking and key_pressed(K_6):
					if g.focus6 == "":
						pass
					else:
						if not g.candraw and g.weapons2[g.w2] in cannotdraw: return
						if g.weapons[g.w] == g.focus6:
							speak("You already draw this weapon.")
						else:
							if get_item_count(g.focus6)>0:
								g.n.send_reliable(0, "draw "+g.focus6+"", 0)
								speak(g.focus6)
								g.weapons.append(g.focus6)
								g.w=len(g.weapons)-1
								if g.weapons2[g.w2]==g.weapons[g.w]: g.n.send_reliable(0,"unequip2",0); g.w2=0

				if not g.ducking and key_pressed(K_7):
					if g.focus7 == "":
						pass
					else:
						if not g.candraw and g.weapons2[g.w2] in cannotdraw: return
						if g.weapons[g.w] == g.focus7:
							speak("You already draw this weapon.")
						else:
							if get_item_count(g.focus7)>0:
								g.n.send_reliable(0, "draw "+g.focus7+"", 0)
								speak(g.focus7)
								g.weapons.append(g.focus7)
								g.w=len(g.weapons)-1
								if g.weapons2[g.w2]==g.weapons[g.w]: g.n.send_reliable(0,"unequip2",0); g.w2=0

				if not g.ducking and key_pressed(K_8):
					if g.focus8 == "":
						pass
					else:
						if not g.candraw and g.weapons2[g.w2] in cannotdraw: return
						if g.weapons[g.w] == g.focus8:
							speak("You already draw this weapon.")
						else:
							if get_item_count(g.focus8)>0:
								g.n.send_reliable(0, "draw "+g.focus8+"", 0)
								speak(g.focus8)
								g.weapons.append(g.focus8)
								g.w=len(g.weapons)-1
								if g.weapons2[g.w2]==g.weapons[g.w]: g.n.send_reliable(0,"unequip2",0); g.w2=0

				if not g.ducking and key_pressed(K_9):
					if g.focus9 == "":
						pass
					else:
						if not g.candraw and g.weapons2[g.w2] in cannotdraw: return
						if g.weapons[g.w] == g.focus9:
							speak("You already draw this weapon.")
						else:
							if get_item_count(g.focus9)>0:
								g.n.send_reliable(0, "draw "+g.focus9+"", 0)
								g.weapons.append(g.focus9)
								g.w=len(g.weapons)-1
								if g.weapons2[g.w2]==g.weapons[g.w]: g.n.send_reliable(0,"unequip2",0); g.w2=0
								speak(g.focus9)
				if not g.ducking and key_pressed(K_0):
					if g.focus0 == "":
						pass
					else:
						if not g.candraw and g.weapons2[g.w2] in cannotdraw: return
						if g.weapons[g.w] == g.focus0:
							speak("You already draw this weapon.")
						else:
							if get_item_count(g.focus0)>0:
								g.n.send_reliable(0, "draw "+g.focus0+"", 0)
								speak(g.focus0)
								g.weapons.append(g.focus0)
								g.w=len(g.weapons)-1
								if g.weapons2[g.w2]==g.weapons[g.w]: g.n.send_reliable(0,"unequip2",0); g.w2=0
		if g.can_move and shift_is_down() and alt_is_down() and g.reloading==False and not g.drawing:
			if not g.zombie:
				if not g.ducking and key_pressed(K_2):
					if g.focus2 == "":
						pass
					else:
						if not g.candraw and g.weapons[g.w] in cannotdraw: return
						if g.weapons2[g.w2] == g.focus2:
							speak("You already draw this weapon.")
						else:
							if get_item_count(g.focus2)>0:
								g.n.send_reliable(0, "draw2 "+g.focus2+"", 0)
								speak(g.focus2)
								g.weapons2.append(g.focus2)
								g.w2=len(g.weapons2)-1
								if g.weapons2[g.w2]==g.weapons[g.w]: g.n.send_reliable(0,"unequip",0); g.w=0
				if not g.ducking and key_pressed(K_3):
					if g.focus3 == "":
						pass
					else:
						if not g.candraw and g.weapons[g.w] in cannotdraw: return
						if g.weapons2[g.w2] == g.focus3:
							speak("You already draw this weapon.")
						else:
							if get_item_count(g.focus3)>0:
								g.n.send_reliable(0, "draw2 "+g.focus3+"", 0)
								speak(g.focus3)
								g.weapons2.append(g.focus3)
								g.w2=len(g.weapons2)-1
								if g.weapons2[g.w2]==g.weapons[g.w]: g.n.send_reliable(0,"unequip",0); g.w=0

				if not g.ducking and key_pressed(K_4):
					if g.focus4 == "":
						pass
					else:
						if not g.candraw and g.weapons[g.w] in cannotdraw: return
						if g.weapons2[g.w2] == g.focus4:
							speak("You already draw this weapon.")
						else:
							if get_item_count(g.focus4)>0:
								g.n.send_reliable(0, "draw2 "+g.focus4+"", 0)
								speak(g.focus4)
								g.weapons2.append(g.focus4)
								g.w2=len(g.weapons2)-1
								if g.weapons2[g.w2]==g.weapons[g.w]: g.n.send_reliable(0,"unequip",0); g.w=0

				if not g.ducking and key_pressed(K_5):
					if g.focus5 == "":
						pass
					else:
						if not g.candraw and g.weapons[g.w] in cannotdraw: return
						if g.weapons2[g.w2] == g.focus5:
							speak("You already draw this weapon.")
						else:
							if get_item_count(g.focus5)>0:
								g.n.send_reliable(0, "draw2 "+g.focus5+"", 0)
								speak(g.focus5)
								g.weapons2.append(g.focus5)
								g.w2=len(g.weapons2)-1
								if g.weapons2[g.w2]==g.weapons[g.w]: g.n.send_reliable(0,"unequip",0); g.w=0

				if not g.ducking and key_pressed(K_6):
					if g.focus6 == "":
						pass
					else:
						if not g.candraw and g.weapons[g.w] in cannotdraw: return
						if g.weapons2[g.w2] == g.focus6:
							speak("You already draw this weapon.")
						else:
							if get_item_count(g.focus6)>0:
								g.n.send_reliable(0, "draw2 "+g.focus6+"", 0)
								speak(g.focus6)
								g.weapons2.append(g.focus6)
								g.w2=len(g.weapons2)-1
								if g.weapons2[g.w2]==g.weapons[g.w]: g.n.send_reliable(0,"unequip",0); g.w=0

				if not g.ducking and key_pressed(K_7):
					if g.focus7 == "":
						pass
					else:
						if not g.candraw and g.weapons[g.w] in cannotdraw: return
						if g.weapons2[g.w2] == g.focus7:
							speak("You already draw this weapon.")
						else:
							if get_item_count(g.focus7)>0:
								g.n.send_reliable(0, "draw2 "+g.focus7+"", 0)
								speak(g.focus7)
								g.weapons2.append(g.focus7)
								g.w2=len(g.weapons2)-1
								if g.weapons2[g.w2]==g.weapons[g.w]: g.n.send_reliable(0,"unequip",0); g.w=0

				if not g.ducking and key_pressed(K_8):
					if g.focus8 == "":
						pass
					else:
						if not g.candraw and g.weapons[g.w] in cannotdraw: return
						if g.weapons2[g.w2] == g.focus8:
							speak("You already draw this weapon.")
						else:
							if get_item_count(g.focus8)>0:
								g.n.send_reliable(0, "draw2 "+g.focus8+"", 0)
								speak(g.focus8)
								g.weapons2.append(g.focus8)
								g.w2=len(g.weapons2)-1
								if g.weapons2[g.w2]==g.weapons[g.w]: g.n.send_reliable(0,"unequip",0); g.w=0

				if not g.ducking and key_pressed(K_9):
					if g.focus9 == "":
						pass
					else:
						if not g.candraw and g.weapons[g.w] in cannotdraw: return
						if g.weapons2[g.w2] == g.focus9:
							speak("You already draw this weapon.")
						else:
							if get_item_count(g.focus9)>0:
								g.n.send_reliable(0, "draw2 "+g.focus9+"", 0)
								g.weapons2.append(g.focus9)
								g.w2=len(g.weapons2)-1
								if g.weapons2[g.w2]==g.weapons[g.w]: g.n.send_reliable(0,"unequip",0); g.w=0

								speak(g.focus9)
				if not g.ducking and key_pressed(K_0):
					if g.focus0 == "":
						pass
					else:
						if not g.candraw and g.weapons[g.w] in cannotdraw: return
						if g.weapons2[g.w2] == g.focus0:
							speak("You already draw this weapon.")
						else:
							if get_item_count(g.focus0)>0:
								g.n.send_reliable(0, "draw2 "+g.focus0+"", 0)
								speak(g.focus0)
								g.weapons2.append(g.focus0)
								g.w2=len(g.weapons2)-1
								if g.weapons2[g.w2]==g.weapons[g.w]: g.n.send_reliable(0,"unequip",0); g.w=0


		if g.mapname!="lobby" and shift_is_down() == True and alt_is_down() == False:
			if g.can_move == True and len(g.weapons)>0 and g.weapons[g.w] != "" and g.weapons[g.w] != "punch" and g.weapons[g.w]!="dummy":
				if not g.ducking and key_pressed(K_2):
					g.focus2=g.weapons[g.w]
					speak(g.weapons[g.w]+" set on this number")
					g.p.play_stationary("fwhisper.wav", False)
				if not g.ducking and key_pressed(K_3):
					g.focus3=g.weapons[g.w]
					speak(g.weapons[g.w]+" set on this number")
					g.p.play_stationary("fwhisper.wav", False)
				if not g.ducking and key_pressed(K_4):
					g.focus4=g.weapons[g.w]
					speak(g.weapons[g.w]+" set on this number")
					g.p.play_stationary("fwhisper.wav", False)
				if not g.ducking and key_pressed(K_5):
					g.focus5=g.weapons[g.w]
					speak(g.weapons[g.w]+" set on this number")
					g.p.play_stationary("fwhisper.wav", False)
				if not g.ducking and key_pressed(K_6):
					g.focus6=g.weapons[g.w]
					speak(g.weapons[g.w]+" set on this number")
					g.p.play_stationary("fwhisper.wav", False)
				if not g.ducking and key_pressed(K_7):
					g.focus7=g.weapons[g.w]
					speak(g.weapons[g.w]+" set on this number")
					g.p.play_stationary("fwhisper.wav", False)
				if not g.ducking and key_pressed(K_8):
					g.focus8=g.weapons[g.w]
					speak(g.weapons[g.w]+" set on this number")
					g.p.play_stationary("fwhisper.wav", False)
				if not g.ducking and key_pressed(K_9):
					g.focus9=g.weapons[g.w]
					speak(g.weapons[g.w]+" set on this number")
					g.p.play_stationary("fwhisper.wav", False)
				if not g.ducking and key_pressed(K_0):
					g.focus0=g.weapons[g.w]
					speak(g.weapons[g.w]+" set on this number")
					g.p.play_stationary("fwhisper.wav", False)

	if key_pressed(K_F4):
		if g.builder or g.admin:
			admchat=get_input("Type your message here.")
			if admchat!="":
				def do(admchat):
					if g.should_translate: admchat=google_translate(g.sendsourcelang, g.sendtargetlang, admchat)
					if admchat is None: speak("No language selected for translation"); return
					g.n.send_reliable(0,"admchat "+admchat,0)
				Thread(target=do,args=(admchat,)).start()
			return
	if g.media_player is not None:
		if not shift_is_down() and key_pressed(K_F6):
			if g.paused: g.paused=False; g.media_player.play()
			elif not g.paused: g.paused=True; g.media_player.pause()
		if shift_is_down() and key_pressed(K_F7):
			g.media_player.stop()
			g.media_player.release()
			if g.video_index==-len(g.video_urls)-1: g.video_index=1
			g.media_player=vlc.MediaPlayer(pafy.new(g.video_urls[g.video_index-1]).getbestaudio().url)
			g.video_index-=1
			g.media_player.set_hwnd(0)
			g.media_player.play()

		if shift_is_down() and key_pressed(K_F8):
			g.media_player.stop()
			g.media_player.release()
			if g.video_index==len(g.video_urls)-1: g.video_index=-1
			g.media_player=vlc.MediaPlayer(pafy.new(g.video_urls[g.video_index+1]).getbestaudio().url)
			g.video_index+=1
			g.media_player.set_hwnd(0)
			g.media_player.play()


		if not shift_is_down() and key_pressed(K_F7): g.media_player.set_time(g.media_player.get_time()-10000)
		if not shift_is_down() and key_pressed(K_F8): g.media_player.set_time(g.media_player.get_time()+10000)
		if shift_is_down()==True and key_pressed(K_END):
			if g.media_player.audio_get_volume()>=10:
				g.media_player.audio_set_volume(g.media_player.audio_get_volume()-10)
			else:
				speak("muted")
		if shift_is_down()==True and key_pressed(K_HOME):
			if g.media_player.audio_get_volume()==150:
				speak("max volume")
			else:
				g.media_player.audio_set_volume(g.media_player.audio_get_volume()+10)
	if key_pressed(K_F9):
		search=get_input("Enter something to search for")
		if search!="":
			speak("Please wait ...")
			results=youtubesearch("AIzaSyCVXGWnl36s5fm16dZguJY8vVlRNiG20-0",search,50)
			if len(results)==0: speak("No results found")
			else:
				m.reset(True)
				menu.setupmenu(False,True)
				m.callback2=mainloop
				g.video_urls.clear()
				for key in results.keys():
					m.add_item_tts(key,results[key])
					g.video_urls.append(results[key])
				mres=m.run(str(len(results))+" results.",True)
				if mres!=0:
					speak("Please wait ...")
					if g.media_player is not None:
						g.media_player.stop()
						g.media_player.release()
					g.media_player=vlc.MediaPlayer(pafy.new(m.get_item_name(mres)).getbestaudio().url)
					g.video_index=0
					g.media_player.play()
		process_events()
	if key_pressed(K_k):
		if g.reply=="":
			speak("There is no private message to reply to.")
		else:
			text=g.reply
			g.n.send_reliable(0,"is_typing "+text+"",0)
			message=get_input("Enter reply")
			if message!="":
				def do(message):
					if g.should_translate: message=google_translate(g.sendsourcelang, g.sendtargetlang, message)
					if message is None: speak("No language selected for translation"); return
					g.n.send_reliable(0,"/pm "+text+" "+message,1)
				Thread(target=do,args=(message,)).start()
			else: 		g.n.send_reliable(0,"is_not_typing "+text+"",0)

	if key_pressed(K_F5): g.n.send_reliable(0,"friendpm",0)
	if key_pressed(K_F11): g.n.send_reliable(0,"selectchannel",0)

	if key_pressed(K_F6): g.n.send_reliable(0,"playermenu",0)

	if key_pressed(K_F10):
		if g.last_spoken_text=="": speak("Nothing spoken yet.")
		else:
			clipboard_copy_text(g.last_spoken_text)
			speak(g.last_spoken_text+" copied to clipboard.")
	if g.mapname!="lobby" and shift_is_down()==True and key_pressed(K_u):
		set_favoriitem()
	if g.mapname!="lobby" and shift_is_down()==False and key_pressed(K_u):
		if g.can_move or g.parachute: g.n.send_reliable(0,"useitem "+g.favoriitem+"",0)
	if key_pressed(K_t): g.n.send_reliable(0,"wakeup",0)
	if g.mapname!="lobby" and shift_is_down()==True and key_pressed(K_y):
		set_favoriitem2()
	if g.mapname!="lobby" and shift_is_down()==False and key_pressed(K_y):
		if g.can_move or g.parachute: g.n.send_reliable(0,"useitem "+g.favoriitem2+"",0)


	if g.watching=="" and g.mapname!="lobby" and key_pressed(K_j):
		admchatt=get_input("Type your team message here.")
		if admchatt!="":
			def do(admchatt):
				if g.should_translate: admchatt=google_translate(g.sendsourcelang, g.sendtargetlang, admchatt)
				if admchatt is None: speak("No language selected for translation"); return
				g.n.send_reliable(0,"teammessage "+admchatt,0)
			Thread(target=do,args=(admchatt,)).start()
		return
	if g.mapname!="lobby" and not g.zombie:
		if joystick_button_pressed(g.jcontrols.get("inv1",-1)): cycle_inv(1)
		if joystick_button_pressed(g.jcontrols.get("inv2",-1)): cycle_inv(0)
	if(key_pressed(K_PAGEUP) and not altdown() and not g.zombie):
		if g.mapname != "lobby":
			g.n.send_reliable(0, "bus_board", 0)

	if(key_pressed(K_TAB) and not altdown() and not g.zombie):
	
		if(shift_is_down()):
			cycle_inv(0)
		else:
			cycle_inv(1)
		
	if(key_pressed(K_RETURN) or key_pressed(pygame.K_KP_ENTER)):
	
		if(shift_is_down() or getattr(g, "in_bus", False)):
		
			if 1:
				doorcheck()
			signcheck()
			g.n.send_reliable(0,"enter",0)
			
		else:
		
			if not alt_is_down() and not control_is_down() and g.mapname!="lobby" and not g.zombie:
				if g.parachute or g.can_move: useitem()
			
			if alt_is_down(): translate_buffer_item()
	if g.can_move and joystick_button_pressed(g.jcontrols.get("invuse",-1)):
		if g.mapname!="lobby" and not g.zombie:
			useitem()
			
		
	if key_pressed(K_DELETE):
		m.reset(True)
		menu.setupmenu()
		m.callback2=mainloop
		m.add_item_tts("quote","quote")
		m.add_item_tts("report","report")
		mres=m.run("Select an action")
		process_events()
		if mres==0:
			return
		if m.get_item_name(mres)=="quote":
			quote()
		if m.get_item_name(mres)=="report":
			if len(g.buffers[g.bufferpos].items)>0:
				report=get_input("Type the reason you want to report this message")
				if report != "":
					g.n.send_reliable(0, "messagereport{}[]"+g.buffers[g.bufferpos].items[g.buffers[g.bufferpos].pos]+", "+""+""+"{}[]"+report,0)

	if((key_pressed(K_BACKSPACE) or joystick_button_pressed(g.jcontrols.get("invdrop",-1))) and g.can_move==True):
	
		if g.falling==True or g.jumping==True:
			pass
		else:
			if g.mapname!="lobby" and not g.zombie:
				dropitem("",shift_is_down())
			
		

	if(g.firetimer.elapsed>=get_firetime() and g.can_move==True and g.mapname!="lobby"):
	
		if (left_control_is_down() or g.usemouse == 1 and mouse_down(0) or joystick_button_down(g.jcontrols.get("fire", -1))) and g.weaponauto == True:

		
			g.firetimer.restart()
			if shift_is_down() and key_up(K_RALT): return
			if not shift_is_down() and key_up(K_RALT): g.n.send_reliable(0,"fire "+g.weapons[g.w],0)
			
		elif(key_pressed(K_LCTRL) or g.usemouse==1 and mouse_pressed(0) or joystick_button_pressed(g.jcontrols.get("fire",-1)) and g.weaponauto==False):
			g.firetimer.restart()
			if shift_is_down() and key_up(K_RALT): return
			if not shift_is_down() and key_up(K_RALT): g.n.send_reliable(0,"fire "+g.weapons[g.w],0)

		
	if(g.firetimer2.elapsed>=get_firetime2() and g.can_move==True and g.mapname!="lobby"):
	
		if (right_control_is_down() ) and g.weaponauto2 == True and not g.sitting:

		
			g.firetimer2.restart()
			try:
				if shift_is_down(): return
				if not shift_is_down(): g.n.send_reliable(0,"fire2 "+g.weapons2[g.w2],0)
			except: pass
			
		elif(key_pressed(K_RCTRL) and g.weaponauto2==False and not g.sitting):
			g.firetimer2.restart()
			try:
				if shift_is_down(): return
				if not shift_is_down(): g.n.send_reliable(0,"fire2 "+g.weapons2[g.w2],0)
			except: pass

		
	if key_pressed(K_SPACE) and shift_is_down(): g.n.send_reliable(0,"throwweaponleft",0)
	if key_pressed(K_SPACE) and alt_is_down(): g.n.send_reliable(0,"throwweaponright",0)
	if((key_pressed(K_SPACE) or joystick_button_pressed(g.jcontrols.get("jump",-1))) and g.jumping==False and g.falling==False and not shift_is_down() and not alt_is_down() and g.can_move==True and not g.inbike and not g.ducking and g.canjump==1 and g.sitting==False and g.zombie==False and (get_tile_at(g.me.x,g.me.y,g.me.z+1).startswith("wall") or get_tile_at(g.me.x,g.me.y,g.me.z+1)=="")):
	
		if g.inve: g.n.send_reliable(0,"motorhorn",0)
		else:
			if "helicopter" not in g.mapname:
				g.p.play_stationary("jump"+str(random(1,4))+".ogg", False)
				g.n.send_reliable(0, "jump", 0)
				g.jumping=True
				g.jumptimer.restart()
				g.jumpup=1
				g.jumplandz=g.me.z
				g.jumplandz2=g.me.z
				g.jumpbeforetile=get_tile_at(g.me.x,g.me.y,g.me.z)
	if key_holding(K_END) and shift_is_down()==False:
		if g.mastervolume<0.1:
			speak("game sounds muted")
		else:
			g.mastervolume -= 0.10
			g.mastervolume2 -= 0.10

			if g.mastervolume<0.1:
				speak("game sounds muted")
			sound.listener._set_gain(g.mastervolume)
			g.writeprefs()

			g.p.play_stationary("menumove2.ogg",False)
	if key_holding(K_HOME) and shift_is_down()==False:
		if g.mastervolume>=1.10:
			speak("max volume")
		else:
			g.mastervolume += 0.10
			g.mastervolume2 += 0.10

			if g.mastervolume==1.10:
				speak("max volume")

			sound.listener._set_gain(g.mastervolume)
			g.writeprefs()

			g.p.play_stationary("menumove2.ogg",False)
	if(key_pressed(K_h)):
	
		g.n.send_reliable(0,"healthcheck",0)
		
	if g.current_scancode==12 and g.can_move == True and not g.jumping:
		g.invmenu=True; invmenu(); g.invmenu=False
		return

	if g.current_scancode==46 or key_pressed(K_EQUALS):
		if g.builder or g.admin:
			chat=get_input("Type an admin command here.")
			if (chat!=""):
				g.n.send_reliable(0,"/"+chat+"",1)
			return
	if g.current_scancode==49:
		if shift_is_down():
			if not g.buffers[g.bufferpos].muted:
				speak(g.buffers[g.bufferpos].name+" muted")
				g.buffers[g.bufferpos].muted=True
			elif g.buffers[g.bufferpos].muted:
				speak(g.buffers[g.bufferpos].name+" unmuted")
				g.buffers[g.bufferpos].muted=False
		else:
			if 1:
				chat=get_input("Type a map message here.")
				if (chat!=""):
					def do(chat):
						if g.should_translate: chat=google_translate(g.sendsourcelang, g.sendtargetlang, chat)
						if chat is None: speak("No language selected for translation"); return
						g.n.send_reliable(0,"mapmessage "+chat+"",0)
					Thread(target=do,args=(chat,)).start()
				return
	if g.current_scancode==52:
		if shift_is_down()==False and alt_is_down()==True: g.n.send_reliable(0,"grouponline",0); return
		if shift_is_down()==True and alt_is_down()==True: g.n.send_reliable(0,"communityonline",0); return
		if shift_is_down()==False:
			if not g.ingroup: speak("You are not in a group")
			else:
				chat=get_input("Type a group message here.")
				if (chat!=""):
					def do(chat):
						if g.should_translate: chat=google_translate(g.sendsourcelang, g.sendtargetlang, chat)
						if chat is None: speak("No language selected for translation"); return
						g.n.send_reliable(0,"groupmessage "+chat+"",0)
					Thread(target=do,args=(chat,)).start()
				return

		if alt_is_down()==False and shift_is_down()==True:
			if not g.incommunity: speak("You are not in a community")
			else:
				chat=get_input("Type a community message here.")
				if (chat!=""):
					def do(chat):
						if g.should_translate: chat=google_translate(g.sendsourcelang, g.sendtargetlang, chat)
						if chat is None: speak("No language selected for translation"); return
						g.n.send_reliable(0,"communitymessage "+chat+"",0)
					Thread(target=do,args=(chat,)).start()
				return



	if joystick_button_pressed(g.jcontrols.get("gamemenu",-1)): g.n.send_reliable(0,"gamemenu",0)
	if g.current_scancode==56 or key_pressed(K_SLASH):
	
		if(shift_is_down()==True):
		
			g.n.send_reliable(0,"whoonline",0)
		else:
			if g.chat==False:
				speak("You cannot send messages because you have disabled chat. Please select a channel by pressing F11")
			else:
				admchat=get_input("Type your message here.")
				if admchat!="":
					def do(admchat):
						if g.should_translate: admchat=google_translate(g.sendsourcelang, g.sendtargetlang, admchat)
						if admchat is None: speak("No language selected for translation"); return
						g.n.send_reliable(0,""+admchat,1)
					Thread(target=do,args=(admchat,)).start()
			return

	if key_pressed(K_o): g.n.send_reliable(0,"gamemenu",0); return

	if g.current_scancode==47:
	
		if (key_down(K_LSHIFT) or key_down(K_RSHIFT)):
		
			firstbuffer()
			
		else:
		
			bufferleft()
			
		
	if g.current_scancode==48:
	
		if (key_down(K_LSHIFT) or key_down(K_RSHIFT)):
		
			lastbuffer()
			
		else:
		
			bufferright()
			
		
	if (key_up(K_LSHIFT) and key_up(K_RSHIFT)):
	
		if g.current_scancode==54:
		
			prevbufferitem()
			
		if g.current_scancode==55:
		
			nextbufferitem()
			
		
	if (key_down(K_LSHIFT) or key_down(K_RSHIFT)):
	
		if g.current_scancode==54:
		
			topbufferitem()
			
		if g.current_scancode==55:
		
			bottombufferitem()
			
		
	if(g.qturn==0 and key_pressed(K_e)):
		if not shift_is_down(): g.n.send_reliable(0,"whonear",0)
		else: autotracktoggle()
	if(not shift_is_down() and g.qturn==1 and key_pressed(K_p)):
		if not shift_is_down(): g.n.send_reliable(0,"whonear",0)
		else: autotracktoggle()

	if key_pressed(K_n):
		if g.tracked==False:
			speak("you are not tracking anything")
		else:
			tell_where(g.trackx, g.tracky, g.trackz)
	if(key_pressed(K_m) and g.mapname!="lobby"):
		if shift_is_down():
			if (g.mapname=="massacre_in_the_city" or g.mapname=="helicopter") and g.watching!="":
				speak("you can not look while watching someone")
			else:
				try: zonemenu(); process_events()
				except: pass
		else: g.n.send_reliable(0,"checkaround",0)

	if key_pressed(K_l):
		if not alt_is_down() and not shift_is_down(): g.n.send_reliable(0,"matchteaminfo",0)
		elif alt_is_down(): buffertransmenu()
		elif shift_is_down(): sendtransmenu()
	if(key_pressed(K_x) and g.mapname!="lobby" and alt_is_down()==False):
		if shift_is_down(): g.n.send_reliable(0,"ammocheck2",0)
		if not shift_is_down(): g.n.send_reliable(0,"ammocheck",0)
	if(key_pressed(K_y)):
		g.n.send_reliable(0,"myscorepoint",0)

	if(g.watching=="" and (g.current_scancode==53 or key_pressed(K_BACKQUOTE))):
		if shift_is_down(): g.n.send_reliable(0,"weaponinfo2",0)
		if not shift_is_down(): g.n.send_reliable(0,"weaponinfo",0)
	if (shift_is_down() or alt_is_down()) and key_pressed(K_z):
		if 1:
			if not g.died and g.can_move and not g.standing and g.sitting:
				g.p.play_stationary("sitstart.ogg",False)
				g.n.send_reliable(0,"xplay sitstart",0)

				g.standing=True
				g.standingtimer.restart()
			elif not g.sitting and not g.died and g.can_move :
				g.sitting=True
				g.p.play_stationary(get_tile_at(g.me.x,g.me.y,g.me.z)+"fall.ogg",False)
				g.n.send_reliable(0,"xplay "+get_tile_at(g.me.x,g.me.y,g.me.z)+"fall",0)
				g.n.send_reliable(0,"sitstart",0)


	if(g.watching=="" and g.usemouse==1 and mouse_pressed(2) and g.mapname!="lobby"): g.n.send_reliable(0,"reload",0)
	if(not g.drawing and not alt_is_down() and g.watching=="" and key_pressed(K_r)):
		if g.mapname!="lobby" and shift_is_down():  		g.n.send_reliable(0,"unload",0)
		else:
			if g.mapname!="lobby": g.n.send_reliable(0,"reload",0)
	if(joystick_button_pressed(g.jcontrols.get("reload",-1)) and g.mapname!="lobby"):
		g.n.send_reliable(0,"reload",0)
	if((key_pressed(K_ESCAPE) or g.stick is not None and g.stick.get_hat(0)==(-1,0)) and g.jumping==False):
		if g.watching=="" and g.falling: return
		waitjoyhat()
		exitfunction()
	if(g.xtimer.elapsed>0 and g.x==True):
	
		reset()
		menu.login_settings()
		
	if key_pressed(K_c) and shift_is_down()==True:
		copy_buffer_item()
		speak("Message copied")
	if(key_pressed(K_c) and shift_is_down()==False):
		if (g.mapname=="massacre_in_the_city" or g.mapname=="helicopter") and g.watching!="":
			speak("While watching someone on this map, you cannot look at their coordinates.")
		else:
			speak(str(round(g.mr.x))+", "+str(round(g.mr.y))+", "+str(round(g.me.z)))
		
	if(joystick_button_pressed(g.jcontrols.get("coordinates",-1)) and shift_is_down()==False):
	
		speak(str(round(g.mr.x))+", "+str(round(g.mr.y))+", "+str(round(g.me.z)))
		

	if(1):
		if key_pressed(K_LEFT):
			if g.watching!="":
				i=get_player_index(g.watching)
				if i>-1:
					while i>=0:
						if (g.mapname=="helicopter" or g.mapname=="massacre_in_the_city") and g.name not in g.players[i].friendlist: i-=1; continue
						if g.players[i].map==g.mapname and g.players[i].name!=g.watching and g.players[i].name!=g.name:
							g.n.send_reliable(0,"matchwatch "+g.players[i].name,0)
							break
						if g.mapname=="helicopter" and g.players[i].map=="massacre_in_the_city" and g.players[i].name!=g.name:
							g.n.send_reliable(0,"matchwatch "+g.players[i].name,0)
							break
						if g.mapname=="massacre_in_the_city" and g.players[i].map=="helicopter" and g.players[i].name!=g.name:
							g.n.send_reliable(0,"matchwatch "+g.players[i].name,0)
							break

						i-=1


		if g.qturn==1 and key_holding(K_e,200,g.turningtimeelapsing):
			turntimer.restart()
			if g.can_move and key_up(K_g) and g.watching=="" and shift_is_down():
				g.facing+=1
				if g.facing>360: g.facing=0
				if g.facing<0: g.facing=360
				if g.speakdegree==1: speak(str(g.facing)+" degrees")
				g.n.send_reliable(0,"facing "+str(g.facing),0)
			
		if g.qturn==1 and key_holding(K_q,200,g.turningtimeelapsing):
			turntimer.restart()
			if g.can_move and key_up(K_g) and g.watching=="" and shift_is_down():
				g.facing-=1
				if g.facing>360: g.facing=0
				if g.facing<0: g.facing=360
				if g.speakdegree==1: speak(str(g.facing)+" degrees")
				g.n.send_reliable(0,"facing "+str(g.facing),0)
			

		if g.qturn==0 and (key_holding(K_LEFT,200,g.turningtimeelapsing) and (g.usesub==0 or g.inve) or key_holding(K_a,200,g.turningtimeelapsing) and g.usesub==1 and not g.inve) or g.stick is not None and g.stick.get_axis(2)<-0.5 and turntimer.elapsed>g.turningtimeelapsing:
			turntimer.restart()
			if g.can_move and key_up(K_g) and g.watching=="" and shift_is_down():
				g.facing-=1
				if g.facing>360: g.facing=0
				if g.facing<0: g.facing=360
				if g.speakdegree==1: speak(str(g.facing)+" degrees")
				g.n.send_reliable(0,"facing "+str(g.facing),0)
			

		if key_pressed(K_RIGHT) and g.watching!="":
			if g.watching!="":
				i=get_player_index(g.watching)
				if i>-1:
					while i<=len(g.players)-1:
						if (g.mapname=="helicopter" or g.mapname=="massacre_in_the_city") and g.name not in g.players[i].friendlist: i+=1; continue
						if g.players[i].map==g.mapname and g.players[i].name!=g.watching and g.name!=g.players[i].name:
							g.n.send_reliable(0,"matchwatch "+g.players[i].name,0)
							break
						if g.mapname=="helicopter" and g.players[i].map=="massacre_in_the_city":
							g.n.send_reliable(0,"matchwatch "+g.players[i].name,0)
							break
						if g.mapname=="massacre_in_the_city" and g.players[i].map=="helicopter":
							g.n.send_reliable(0,"matchwatch "+g.players[i].name,0)
							break

						i+=1

		if(g.qturn==0 and (key_up(K_g) and key_holding(K_RIGHT,200,g.turningtimeelapsing) and (g.usesub==0 or g.inve) or key_holding(K_d,200,g.turningtimeelapsing) and g.usesub==1 and not g.inve and g.mapname!="lobby") or g.stick is not None and g.stick.get_axis(2)>0.5 and turntimer.elapsed>g.turningtimeelapsing):
		
			if g.can_move and g.watching=="" and key_up(K_g) and shift_is_down():
				g.facing+=1
				if g.facing>360: g.facing=0
				if g.facing<0: g.facing=360
				g.n.send_reliable(0,"facing "+str(g.facing),0)
				if g.speakdegree==1: speak(str(g.facing)+" degrees")
			
		if g.qturn==1 and key_up(K_g) and key_holding(K_e,200,g.turningtimeelapsing):
		
			if g.can_move and g.watching=="" and key_up(K_g) and shift_is_down():
				g.facing+=1
				if g.facing>360: g.facing=0
				if g.facing<0: g.facing=360
				g.n.send_reliable(0,"facing "+str(g.facing),0)
				if g.speakdegree==1: speak(str(g.facing)+" degrees")
			

		if(g.qturn==0 and (key_pressed(K_LEFT) and (g.usesub==0 or g.inve) or key_pressed(K_a) and g.usesub==1 and not g.inve)):
			if key_up(K_g) and g.can_move and g.watching=="" and not shift_is_down():
				if not alt_is_down(): g.facing=getdir(turnleft(getdir(g.facing)))
				if alt_is_down(): g.facing=getdir(turnleft(getdir(g.facing),90))
				if g.speakfacing==1: speak(dir_to_string(g.facing))
				g.p.play_stationary("turn.ogg",False)
				if g.mapname!="lobby": g.n.send_reliable(0,"xplay turn",0)
				g.n.send_reliable(0,"facing "+str(g.facing),0)
			
		if(g.qturn==0 and (key_up(K_g) and key_pressed(K_RIGHT) and (g.usesub==0 or g.inve) or key_pressed(K_d) and g.usesub==1 and not g.inve)):
		
			if g.can_move and g.watching=="" and key_up(K_g) and not shift_is_down():
				if not alt_is_down(): g.facing=getdir(turnright(getdir(g.facing)))
				if alt_is_down(): g.facing=getdir(turnright(getdir(g.facing),90))
				if g.speakfacing==1: speak(dir_to_string(g.facing))
				g.p.play_stationary("turn.ogg",False)
				if g.mapname!="lobby": g.n.send_reliable(0,"xplay turn",0)
				g.n.send_reliable(0,"facing "+str(g.facing),0)
			
		if(g.qturn==1 and (key_pressed(K_q))):
			if g.can_move and key_up(K_g) and g.watching=="" and not shift_is_down():
				if not alt_is_down(): g.facing=getdir(turnleft(getdir(g.facing)))
				if alt_is_down(): g.facing=getdir(turnleft(getdir(g.facing),90))
				if g.speakfacing==1: speak(dir_to_string(g.facing))
				g.p.play_stationary("turn.ogg",False)
				if g.mapname!="lobby": g.n.send_reliable(0,"xplay turn",0)
				g.n.send_reliable(0,"facing "+str(g.facing),0)
			
		if(g.qturn==1 and (key_pressed(K_e))):
		
			if g.can_move and g.watching=="" and key_up(K_g) and not shift_is_down():
				if not alt_is_down(): g.facing=getdir(turnright(getdir(g.facing)))
				if alt_is_down(): g.facing=getdir(turnright(getdir(g.facing),90))
				if g.speakfacing==1: speak(dir_to_string(g.facing))
				g.p.play_stationary("turn.ogg",False)
				if g.mapname!="lobby": g.n.send_reliable(0,"xplay turn",0)
				g.n.send_reliable(0,"facing "+str(g.facing),0)
			


		if g.stopaimtimer.elapsed>=2000 and g.stopaim==1 and g.aim!=0 and ((g.usesub==0 and not key_holding(K_UP,250,250) or g.usesub==1 and not key_holding(K_w,250,250)) or (g.usesub==0 and not key_holding(K_DOWN,250,250) or g.usesub==1 and not key_holding(K_s,250,250))):
			g.aim=0
			g.n.send_reliable(0,"aim "+str(g.aim),0)
			g.distpool.update_listener_3d(g.me.x, g.me.y, g.me.z, calculate_theta(dummy(g.facing)))
			g.p.update_listener_3d(g.me.x, g.me.y, g.me.z, calculate_theta(dummy(g.facing)))
		if g.mapname=="lobby" and g.aim!=0 and g.can_move==True:
			g.aim=0
			g.n.send_reliable(0,"aim "+str(g.aim),0)
			g.distpool.update_listener_3d(g.me.x, g.me.y, g.me.z, calculate_theta(dummy(g.facing)))
			g.p.update_listener_3d(g.me.x, g.me.y, g.me.z, calculate_theta(dummy(g.facing)))
		if not alt_is_down() and ((g.can_move) and g.mapname!="lobby" and g.aim<get_max_aim() and (g.usesub==0 and not g.inbike and key_holding(K_UP,500,250) or (g.inbike or g.usesub==1) and g.can_move and key_holding(K_w,500,250))):
			if not g.inve:
				g.p.play_stationary("aiming.ogg",False)
				if shift_is_down(): g.aim+=2
				if not shift_is_down(): g.aim+=1
				g.stopaimtimer.restart()
				if g.aim>get_max_aim(): g.aim=get_max_aim()
				if 1:
					if g.aim!=0:
						speak(get_aim_str())
					else: speak("forward")
				g.n.send_reliable(0,"aim "+str(g.aim),0)
				g.distpool.update_listener_3d(g.me.x, g.me.y, g.me.z, calculate_theta(dummy(g.facing)))
				g.p.update_listener_3d(g.me.x, g.me.y, g.me.z, calculate_theta(dummy(g.facing)))
		if alt_is_down()==True and key_pressed(K_x) and g.jumping==False and g.falling==False:
			if not g.inve and not g.sitting and g.canduck==1 and not g.jumping and not g.inve and g.watching=="" and g.mapname!="lobby" and not g.ducking:
				g.ducking=True
				g.p.play_stationary("duck.ogg")
				g.n.send_reliable(0,"duck",0)

				if not g.inve: g.walktime+=100
			elif g.ducking:
				g.ducking=False
				g.p.play_stationary("unduck.ogg")
				g.n.send_reliable(0,"unduck",0)
				if not g.reloading: g.walktime-=100
		if g.ducking and g.canduck==0:
			g.ducking=False
			g.p.play_stationary("unduck.ogg")
			g.n.send_reliable(0,"unduck",0)
			g.walktime-=100


		if not alt_is_down() and (g.can_move and not g.inve and g.mapname!="lobby" and g.aim>-get_max_aim() and (g.usesub==0 and key_holding(K_DOWN,250,250) or (g.inbike or g.usesub==1) and key_holding(K_s,250,250))):
		
			g.p.play_stationary("aiming.ogg",False)
			if shift_is_down(): g.aim-=2
			else: g.aim-=1
			g.stopaimtimer.restart()
			if g.aim<-get_max_aim(): g.aim=-get_max_aim()
			if 1:
				speak(get_aim_str())
			g.n.send_reliable(0,"aim "+str(g.aim),0)
			g.distpool.update_listener_3d(g.me.x, g.me.y, g.me.z, calculate_theta(dummy(g.facing)))
			g.p.update_listener_3d(g.me.x, g.me.y, g.me.z, calculate_theta(dummy(g.facing)))

		
		
		
	if((key_pressed(K_f) or joystick_button_pressed(g.jcontrols.get("facing",-1)))):
	
		if shift_is_down():
			speak(get_aim_str())
		else:
			speak(_("%s at %d degrees")%(dir_to_string(getdir(g.facing)),g.facing))
		
	if (g.can_move==True and key_up(K_g)):

		if 1:
			if(not g.sitting and g.movetimer.elapsed>(g.movetime if not g.inve else 20) and (g.kpgdn2.pressing() or g.kp7.pressing() or joystick_button_pressed(g.jcontrols.get("climbdown",-1)))):
		
				if get_staircase_at(g.me.x, g.me.y, g.me.z)=="" and get_tile_at(g.me.x,g.me.y,g.me.z-1)!="" and get_tile_at(g.me.x,g.me.y,g.me.z-1).startswith("wall")==False and get_tile_at(g.me.x,g.me.y,g.me.z-1)!="air":
					g.me.z-=1
					g.movetimer.restart()
					playstep()
					g.n.send_unreliable(0, "move_to_a "+str(g.me.x)+" "+str(g.me.y)+" "+str(g.me.z)+"", 0)			
					if not g.parachute and not g.ducking and (g.fastwalk==1 or alt_is_down()) and g.walktime>g.maxwalktime: g.walktime-=10
					g.lastdir=Down
					g.stopwalktimer.restart()

			if(not g.sitting and g.movetimer.elapsed>(g.movetime if not g.inve else 20) and (g.kpgup2.pressing() or g.kp9.pressing() or joystick_button_pressed(g.jcontrols.get("climbup",-1)))):
		
				if get_staircase_at(g.me.x, g.me.y, g.me.z)=="" and get_tile_at(g.me.x,g.me.y,g.me.z+1)!="" and get_tile_at(g.me.x,g.me.y,g.me.z+1).startswith("wall")==False and get_tile_at(g.me.x,g.me.y,g.me.z+1)!="air":
					g.me.z+=1
					g.movetimer.restart()
					playstep()
					g.n.send_unreliable(0, "move_to_a "+str(g.me.x)+" "+str(g.me.y)+" "+str(g.me.z)+"", 0)
					if not g.parachute and not g.ducking and (g.fastwalk==1 or alt_is_down()) and g.walktime>g.maxwalktime: g.walktime-=10
					g.lastdir=Down
					g.stopwalktimer.restart()


			

			if(key_down(K_w) and g.usesub==0 or key_down(K_UP) and g.usesub==1 or (g.usemouse==1 and mouse_down(1))) or g.stick is not None and g.stick.get_axis(1)<-0.5:


				if g.movetimer.elapsed>(g.movetime if not g.inve else 20): g.movetimer.restart(); move_player(Forward); checkloc()
			
			elif(key_down(K_s) and g.usesub==0 or key_down(K_DOWN) and g.usesub==1) or g.stick is not None and g.stick.get_axis(1)>0.5:
		

				if g.movetimer.elapsed>(g.movetime if not g.inve else 20): g.movetimer.restart();move_player(Backward); checkloc()
			
			elif(key_down(K_a) and g.usesub==0 or key_down(K_LEFT) and g.usesub==1) or g.stick is not None and g.stick.get_axis(0)<-0.5:
		

				if g.movetimer.elapsed>(g.movetime if not g.inve else 20): g.movetimer.restart();move_player(Left); checkloc()
			
			elif(key_down(K_d) and g.usesub==0 or key_down(K_RIGHT) and g.usesub==1) or g.stick is not None and g.stick.get_axis(0)>0.5:
		

				if g.movetimer.elapsed>(g.movetime if not g.inve else 20): g.movetimer.restart();move_player(Right); checkloc()
			
		
def getmotd():
	g.motdhash=file_get_contents(DIRECTORY_APPDATA+"/nbm-studios/zero_hour_assault/motdhash.dat")
	motd=url_get("https://nbmstudios.com/zero_hour_assault/web_message.txt")
	if string_hash(motd, 2, False) != g.motdhash:
		g.motdhash=string_hash(motd, 2, False)
		g.p.play_stationary("motd.ogg", False)
		dlg(""+motd+"")
		writeprefs()
		file_put_contents(""+DIRECTORY_APPDATA+"/nbm-studios/zero_hour_assault/motdhash.dat", g.motdhash, "w")

def positions():

	if g.me.x != g.old_x or g.me.y != g.old_y or g.me.z != g.old_z or g.facing != g.old_facing:
		for p in g.players: p.position_voicechat_sound()
		g.distpool.update_listener_3d(g.me.x, g.me.y, g.me.z, calculate_theta(dummy(g.facing)))
		g.p.update_listener_3d(g.me.x, g.me.y, g.me.z, calculate_theta(dummy(g.facing)))
		g.old_x=g.me.x
		g.old_y=g.me.y
		g.old_z=g.me.z
		g.old_facing=g.facing
		checkloc()
		if g.mapready: fallcheck()

	
def checkloc():
	zone=get_zone_at(g.me.x, g.me.y, g.me.z)
	if(zone!=""):
	

		if(g.currentloc!=zone):

		
			if g.mapname=="massacre_in_the_city" and g.watching!="": return
			g.currentloc=zone
			if g.watching=="" or g.mapname=="massacre_in_the_city" and g.watching!="": speak(g.currentloc)
			g.n.send_reliable(0,"update_zone "+g.currentloc,0)
			
		
	elif(zone=="" and g.currentloc!=""):
	
		speak("unknown area")
		g.currentloc=""
		
	
def doorcheck():
	for i in range(len(g.doors)):
	
		if (round(g.me.x)==g.doors[i].dx and round(g.me.y)==g.doors[i].dy and round(g.me.z==g.doors[i].dz) and g.dmoving==False):
		
			g.can_move=False
			g.p.play_extended_3d(g.doors[i].ds3, g.me.x, g.me.y, g.me.z, g.me.x, g.me.y, g.me.z, calculate_theta(g.facing), 0, 0, 0, 0, 0, 0, False, 0.0, 0.0, 0.0, 100.0, False)

			g.n.send_reliable(0,"playonmap "+g.doors[i].ds3,0)
			if g.doors[i].exitdoor: g.n.send_reliable(0,"exithouse",0)

			g.doors[i].moving=True
			g.dmoving=True
			return
			
		elif (i>=len(g.doors)-1):
		
			pass
		
	
def dloop():
	dsnd=string_split(doorsound, "\n", False)
	setupmenu()
	for i in range(len(dsnd)):
		m.add_item(dsnd[i]+".ogg", dsnd[i])
	mres=m.run("Select the door sound, that when the player listen to it", True)
	if mres == 0:
		return ""
	else:
		return m.get_item_name(mres)

def dropen():
	dosnd=string_split(dooropen, "\n", False)
	m.reset(True)
	menu.setupmenu()
	m.callback2=mainloop
	for i in range(len(dosnd)):
#		if g.pf.file_exists(dosnd[i]+".ogg"):
		m.add_item(dosnd[i]+".ogg", dosnd[i])
	mres=m.run("Select the door open sound, that when the player click on it", True)
	if mres == 0:
		return ""
	else:
		return m.get_item_name(mres)
def drclose():
	dcsnd=string_split(doorclose, "\n", False)
	m.reset(True)
	menu.setupmenu()
	m.callback2=mainloop
	for i in range(len(dcsnd)):
#		if g.pf.file_exists(dcsnd[i]+".ogg"):
		m.add_item(dcsnd[i]+".ogg", dcsnd[i])
	mres=m.run("Select the door close sound, that when the player click on it", True)
	if mres == 0:
		return ""
	else:
		return m.get_item_name(mres)
def drmoving():
	dmsnd=string_split(doormovingsnd, "\n", False)
	m.reset(True)
	menu.setupmenu()
	for i in range(len(dmsnd)):
#		if g.pf.file_exists(dmsnd[i]+".ogg"):
		m.add_item(dmsnd[i]+".ogg", dmsnd[i])
	mres=m.run("Select the door moving sound, that when the player moving to the destination coords", True)
	if mres == 0:
		return ""
	else:
		return m.get_item_name(mres)
g.p1=[]
g.p2=[]
g.p3=[]
g.p4=[]
g.pcleartimer=timer()
def serverside_menu(sndtxt, Menu, menuitems, pos=0):
	g.pcleartimer.restart()
	oldpos=m.position
	m.reset(True)

	menu.setupmenu(False, True, Menu=="prevmenu", not sndtxt=="binoculars",True)
	if Menu=="prevmenu": m.position=oldpos
	if menuitems == "" or menuitems == "<" or menuitems == "<		0" or menuitems == "<0":
		return
	items=string_split(menuitems, "\t", False)
	if len(menuitems)<=1:
		return
	for i in items:
		if i == "":
			continue
		parsed=string_split(i, "<", False)
		if len(parsed)>1:
			if 1 == 1:
				try: m.add_item_tts(parsed[0], parsed[1],strtobool(parsed[2]))
				except: pass
		m.sndtxt=sndtxt
		if sndtxt=="friendpmchoose": m.callback2=friendpm
		elif sndtxt=="notifys": m.callback2=notifycb
		else: m.callback2=mainloop
	try:
		mres=m.run(Menu, True, pos)
		g.pcleartimer.restart()
		if (m.get_item_name(mres) == "back" or mres == 0) and len(m.items)!=0:
			for i in range(len(g.p1)):
				if g.p1[i]==sndtxt:
					g.p1.pop(i)
					g.p2.pop(i)
					g.p3.pop(i)
					g.p4.pop(i)
			if len(g.p1)!=0:
				p1=g.p1.pop()
				p2=g.p2.pop()
				p3=g.p3.pop()
				p4=g.p4.pop()
				g.n.send_reliable(0,"mpacket "+p1,0)
				g.n.send_reliable(0,"mitems "+p3,0)
				serverside_menu(p1,p2,p3,p4)
				process_events()
			else: g.n.send_reliable(0, sndtxt+" back", 0)
		else:
	
			if mres==0:
				g.n.send_reliable(0, sndtxt+" back", 0)
			g.n.send_reliable(0, sndtxt+" "+m.get_item_name(mres), 0)
			if menu!="binoculars" and Menu!="prevmenu":
				g.p1.append(sndtxt)
				g.p2.append(Menu)
				g.p3.append(menuitems)
				g.p4.append(m.position)
	except: pass
	process_events()
g.serverside_menu=serverside_menu
def plattypemenu():
	plattype=0
	m.reset(True)
	menu.setupmenu(False,True)
	m.speak_position_information=True
	m.enable_first_letter_navigation=True
	m.callback=plm
	m.callback2=mainloop
	addplattypes()
	netloop()
	mres=m.run("select platform type.", True)
	if mres == 0:
		return ""
	else:
		plattype=m.get_item_name(mres)
		return plattype
def plattypemenuw():
	plattype=0
	m.reset(True)
	menu.setupmenu(False,True)
	m.speak_position_information=True
	m.enable_first_letter_navigation=True
	m.callback=plm
	m.callback2=mainloop
	addplattypesw()
	netloop()
	mres=m.run("select platform type.", True)
	if mres == 0:
		return ""
	else:
		plattype=m.get_item_name(mres)
		return plattype

def list_ambiences():
	ambs=string_split(srctypes, "\n", False)
	m.reset(True)
	menu.setupmenu()
	for i in range(len(ambs)):
		if 1 == 1:
			m.add_item(ambs[i]+".ogg", ambs[i])
	m.wrap=True
	m.callback2=mainloop
	mres=m.run("Select an ambience", True)
	if mres == 0:
		return ""
	else:
		return m.get_item_name(mres)
def addplattypes():
	platforms=string_split(tiletypes, "\n", False)
	for i in range(len(platforms)):
		if not platforms[i].startswith("wall"): m.add_item_tts(platforms[i], platforms[i])
def addplattypesw():
	platforms=string_split(tiletypes, "\n", False)
	for i in range(len(platforms)):
		if platforms[i].startswith("wall"): m.add_item_tts(platforms[i], platforms[i])

def plm(m):
	if key_down(K_SPACE) and g.movetimer.elapsed >= g.movetime:
		g.movetimer.restart()
		if string_left(m.get_item_name(m.position + 1), 4) == "wall":
			g.p.play_stationary(m.get_item_name(m.position + 1) + ".ogg", False)
		else:
			g.p.play_stationary(
				m.get_item_name(m.position + 1) + "step" + str(random(1, 5)) + ".ogg",
				False,
			)
	if key_pressed(K_j):
		g.p.play_stationary(m.get_item_name(m.position + 1) + "land.ogg", False)
	if key_pressed(K_n):
		g.p.play_stationary(m.get_item_name(m.position + 1) + "hardland.ogg", False)
def dummy(d): return d
def stn(n):
	return string_to_number(n)
def record_voice():
	while g.recording:
		time.sleep(0.010)
		try: audio_data = pstream.read(CHUNK_SIZE)
		except: continue
		audio_data=amplify_audio_data(audio_data, g.volumeg/100)
		audio_data = opus_encoder.encode(audio_data,CHUNK_SIZE)
		g.n.send_unreliable(0, audio_data, 5)
def play_audio(p,data,decode=True):
	p.clearbuffertimer.restart()
	if decode:
		for i in range(len(data)):
			try: data[i] = p.opus_decoder.decode(data[i],CHUNK_SIZE)
			except: return
	data=b"".join(data)
	if p.name in g.playervolumes:
		volume=g.playervolumes[p.name]
		data=amplify_audio_data(data, volume/100)
	play_voice_pcm(p, data, False)
	p.audio_buffer.clear()
def record_voice2():
	while g.recording2:
		time.sleep(0.010)
		try: audio_data = pstream.read(CHUNK_SIZE)
		except: continue
		audio_data=amplify_audio_data(audio_data, g.volumeg/100)
		audio_data = opus_encoder.encode(audio_data,CHUNK_SIZE)
		g.n.send_unreliable(0, audio_data, 6)
def play_audio2(p,data,decode=True):
	p.clearbuffertimer2.restart()
	if decode:
		for i in range(len(data)):
			try: data[i] = p.opus_decoder2.decode(data[i],CHUNK_SIZE)
			except: return
	data=b"".join(data)
	if p.name in g.playervolumes:
		volume=g.playervolumes[p.name]
		data=amplify_audio_data(data, volume/100)
	play_voice_pcm(p, data, True)
	p.audio_buffer2.clear()


def strtobool(b):
	b=b.lower()
	if b=="true": return True
	if b=="false": return False
def serverbox(mode=0, maxlength=-1, autosend=0, keypresses=-1, sendtext="server_box", text="enter text"):
	userinput=get_input(text)
	g.pcleartimer.restart()
	if userinput!="":
		g.n.send_reliable(0,sendtext+" "+userinput,0)
	else:
		if 1:
			if len(g.p1)!=0:
				p1=g.p1.pop()
				p2=g.p2.pop()
				p3=g.p3.pop()
				p4=g.p4.pop()
				serverside_menu(p1,p2,p3,p4)
				process_events()
def handle_voicechat_data(p):

	while p in g.players:
		time.sleep(0.010)
		playing=p.voice_sound is not None and p.voice_sound.playing()
		if len(p.audio_buffer)>=20 and not p.alplayed:
			p.alplayed=True
			play_audio(p,p.audio_buffer)
		elif p.alplayed:
			if not playing and len(p.audio_buffer)>=20: play_audio(p,copy.copy(p.audio_buffer))
def reinit_voicechat():
	global p,pstream,opus_encoder
	startrecording=False
	startrecording2=False
	if g.recording:
		g.recording=False
		if not g.recording:
			try: g.n.send_reliable(0,"voiceoff",0)
			except: pass

		startrecording=True
	if g.recording2:
		g.recording2=False
		if not g.recording2:
			try: g.n.send_reliable(0,"voiceoff2",0)
			except: pass


	try: pstream.close()
	except: pass
	p.terminate()
	p=pyaudio.PyAudio()
	g.pa=p
	opus_encoder = opuslib.Encoder(g.samplerate, CHANNELS, opuslib.APPLICATION_VOIP)
	CHUNK_SIZE=round(20*(g.samplerate/1000))
	try: pstream=p.open(format=FORMAT, channels=1, rate=g.samplerate, input=True, frames_per_buffer=CHUNK_SIZE, input_device_index=g.inputdevice)
	except: pass
	opus_encoder.bitrate=g.bitrate
	opus_encoder.complexity=0
	if startrecording:
		g.recording=True
		g.recording2=False
		if g.recording:
			try: g.n.send_reliable(0,"voiceon",0)
			except: pass

		Thread(target=record_voice).start()
	if startrecording2:
		g.recording2=True
		g.recording=False
		if g.recording2:
			try: g.n.send_reliable(0,"voiceon2",0)
			except: pass

		Thread(target=record_voice2).start()

g.reinit_voicechat=reinit_voicechat
def friendpm():
	mainloop()
	if key_pressed(K_SPACE):
		text=string_split(m.get_item_name(m.position+1), ", ", True)[0]
		clipboard_copy_text(text)
		speak(""+text+" copied")
	if key_pressed(K_RETURN) or key_pressed(pygame.K_KP_ENTER):
		text=string_split(m.get_item_name(m.position+1), ", ", True)[0]

		if shift_is_down():
			g.n.send_reliable(0,"friendstats "+text,0)
			g.pcleartimer.restart()
			m.items.clear()
			return
		text=string_split(m.get_item_name(m.position+1), ", ", True)[0]
		g.n.send_reliable(0,"is_typing "+text+"",0)
		message=get_input("Type the private message you would like to send to "+text+".")
		if message!="":
			def do(message):
				if g.should_translate: message=google_translate(g.sendsourcelang, g.sendtargetlang, message)
				if message is None: speak("No language selected for translation"); return
				g.n.send_reliable(0,"/pm "+text+" "+message,1)
			Thread(target=do,args=(message,)).start()
		else: 		g.n.send_reliable(0,"is_not_typing "+text+"",0)
		process_events()
def youtubesearch(apikey, searchterm, maxresults=50):
	base_url = 'https://www.googleapis.com/youtube/v3/search'
	params = {
		'part': 'snippet',
		'q': searchterm,
		'type': 'video',
		'maxResults': min(maxresults, 50),  # Limit maxResults to 50 per request
		'key': apikey
	}

	response = requests.get(base_url, params=params)
	data = response.json()

	results = {}
	for item in data['items']:
		video_title = item['snippet']['title']
		video_id = item['id']['videoId']
		video_url = f'https://www.youtube.com/watch?v={video_id}'
		results[video_title] = video_url

	remaining_results = maxresults - 50
	while remaining_results > 0 and 'nextPageToken' in data:
		params['pageToken'] = data['nextPageToken']
		params['maxResults'] = min(remaining_results, 50)
		response = requests.get(base_url, params=params)
		data = response.json()

		for item in data['items']:
			video_title = item['snippet']['title']
			video_id = item['id']['videoId']
			video_url = f'https://www.youtube.com/watch?v={video_id}'
			results[video_title] = video_url

		remaining_results -= min(remaining_results, 50)

	return results
def joystick_button_pressed(button):
	if g.stick is None: return False
	return g.stick.button_pressed(button)
def joystick_button_down(button):
	if g.stick is None: return False
	return g.stick.button_down(button)
def joystick_button_released(button):
	if g.stick is None: return False
	return g.stick.button_released(button)
def joystick_button_up(button):
	if g.stick is None: return False
	return g.stick.button_up(button)
def waitjoyhat():
	if g.stick is None: return
	while g.stick.get_hat(0)!=(0,0): process_events()
def notifycb():
	mainloop()
	if m.position!=-1 and key_pressed(K_RETURN):
		item=m.get_item_name(m.position+1)
		g.n.send_reliable(0,m.sndtxt+" "+item,0)
		item=m.get_item_text(m.position+1)
		if item.startswith("disable"): m.items[m.position].text=m.items[m.position].text.replace("disable ","enable ")
		elif item.startswith("enable"): m.items[m.position].text=m.items[m.position].text.replace("enable ","disable ")
		process_events()
def matchteammenu(data):
	if data=="" or data==" ": return
	redplayers=[]
	blueplayers=[]
	for line in data.split("\n"):
		parsed=line.split(":")
		if len(parsed)>1:
			if parsed[0]=="red": redplayers.append(parsed[1])
			elif parsed[0]=="blue": blueplayers.append(parsed[1])
	pos=0
	if len(redplayers)==0: redplayers.append("No one to show")
	if len(blueplayers)==0: blueplayers.append("No one to show")
	current_list=redplayers
	if g.lastteam=="blue": current_list=blueplayers
	if len(current_list)>0:
		if g.watching=="": speak("You are on the "+g.matchteam+" team, Press left and right arrow keys to move between teams, up and down keys to see the players in the team you selected, enter key to copy a player's name to clipboard.")
		if g.watching!="": speak("Press left and right arrow keys to move between teams, up and down keys to see the players in the team you selected, enter key to copy a player's name to clipboard.")
	else: return
	while 1:
		process_events()
		mainloop()
		if 1:
			try:
				f = -1
				for i in range(pos, len(current_list)):
					item = current_list[i]
					if item == "":
						continue
					if i == pos:
						continue
					if key_pressed(ord(_(item)[0].lower())):
						f = i
						pos = i
						speak(current_list[pos])
						break
				if f == -1:
					for i, item in enumerate(current_list):
						if item == "":
							continue
						if key_pressed(ord(_(item)[0].lower())):
							pos = i
							speak(current_list[pos])
							break
			except:
				pass
		if key_pressed(K_LEFT) and current_list!=redplayers:
			current_list=redplayers
			if "no one" in current_list[0].lower():  speak("You selected red team, it has 0 members.")
			else: speak("You selected red team, it has "+str(len(current_list))+" members.")
		if key_pressed(K_RIGHT) and current_list!=blueplayers:
			current_list=blueplayers
			if "no one" in current_list[0].lower():  speak("You selected blue team, it has 0 members.")
			else: speak("You selected blue team, it has "+str(len(current_list))+" members.")
		if pos>=len(current_list): pos=len(current_list)-1
		if key_pressed(K_DOWN) and len(current_list)>0:
			if pos==len(current_list)-1: speak(current_list[pos]); continue
			pos+=1
			speak(current_list[pos])
		if key_pressed(K_UP) and len(current_list)>0:
			if pos==0: speak(current_list[pos]); continue
			pos-=1
			speak(current_list[pos])
		if key_pressed(K_RETURN) or key_pressed(pygame.K_KP_ENTER): clipboard_copy_text(current_list[pos].split()[0].replace(",","")); speak(current_list[pos].split()[0].replace(",","")+" copied")
		if key_pressed(K_ESCAPE):
			if current_list==redplayers: g.lastteam="red"
			else: g.lastteam="blue"
			process_events(); return
def amplify_audio_data(audio_data, amplification_factor):
	"""
	Amplifies or attenuates audio data represented as bytes object with raw PCM audio.

	Args:
	- audio_data (bytes): Raw PCM audio data.
	- amplification_factor (float): Factor by which to amplify or attenuate the audio.

	Returns:
	- bytes: Amplified or attenuated audio data.
	"""
	import numpy as np
	amplification_factor*=3

	# Convert bytes to numpy array of int16
	audio_array = np.frombuffer(audio_data, dtype=np.int16)

	# Amplify or attenuate audio
	amplified_audio_array = audio_array.astype(np.float32) * amplification_factor

	# Clip audio to prevent overflow
	amplified_audio_array = np.clip(amplified_audio_array, -32768, 32767)

	# Convert amplified audio back to int16
	amplified_audio_data = amplified_audio_array.astype(np.int16)

	# Convert back to bytes
	amplified_audio_bytes = amplified_audio_data.tobytes()

	return amplified_audio_bytes

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

def calculate_distance(user_x, user_y, user_z, zone_minx, zone_miny, zone_minz):
	return math.sqrt((zone_minx - user_x)**2 + (zone_miny - user_y)**2 + (zone_minz - user_z)**2)

def zonemenu():
	foundzones = False
	m.reset(True)
	zone_distances = []

	for zone in g.mapzones:
		if "trackable" in zone:
			sd = string_split(zone, ":", True)
			minx = int(sd[0])
			maxx = int(sd[1])
			miny = int(sd[2])
			maxy = int(sd[3])
			minz = int(sd[4])
			maxz = int(sd[5])
			text = sd[6]

			if text != "" and text is not None:
				distance = calculate_distance(g.me.x, g.me.y, g.me.z, minx, miny, minz)
				zone_distances.append((distance, text, minx, miny, minz))
				foundzones = True

	zone_distances.sort(key=lambda x: x[0])

	for _, text, minx, miny, minz in zone_distances:
		m.add_item_tts(text, text)

	if g.trackx != -1:
		m.add_item_tts("stop tracking", "stop")

	mres = 0
	if foundzones:
		menu.setupmenu(False, True)
		m.callback2 = mainloop
		mres = m.run("Select a zone to track.", True)

	if mres != 0:
		if m.get_item_name(mres) == "stop":
			speak("Stopped tracking")
			g.trackx = -1
			g.tracky = -1
			g.tracked = False
			return

		for _, text, minx, miny, minz in zone_distances:
			if m.get_item_name(mres) == text:
				speak("Tracking " + text)
				g.tracked = True
				g.trackx = minx
				g.tracky = miny
				g.trackz = minz

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

def get_installed_jaws_versions():
	jaws_path = os.path.join(os.getenv("APPDATA"), "Freedom Scientific", "JAWS")
	try:
		return [folder for folder in os.listdir(jaws_path) if os.path.isdir(os.path.join(jaws_path, folder))]
	except OSError:
		return []

def get_user_languages(jaws_version):
	settings_path = os.path.join(os.getenv("APPDATA"), "Freedom Scientific", "JAWS", jaws_version, "Settings")
	try:
		return [folder for folder in os.listdir(settings_path) if folder not in ["VoiceProfiles", "Notifications"]]
	except OSError:
		return []

def install_language(language, jaws_version):
	source_file = "zero_hour_assault.jkm"
	target_path = os.path.join(os.getenv("APPDATA"), "Freedom Scientific", "JAWS", jaws_version, "Settings", language)

	if os.path.exists(target_path):
		try:
			target_file = os.path.join(target_path, "zero_hour_assault.jkm")
			shutil.copy(source_file, target_file)
			if not compiled:
				target_file = os.path.join(target_path, "python.jkm")
				shutil.copy(source_file, target_file)
			if compiled: os.remove(source_file)
		except OSError:
			pass
	else:
		pass

def jawscheck():
	installed_jaws_versions = get_installed_jaws_versions()

	if installed_jaws_versions:
		for version in installed_jaws_versions:
			user_languages = get_user_languages(version)
			for language in user_languages:
				install_language(language, version)
def change_voicechat_volume(name):
	volume=g.playervolumes.get(name,50)
	speak("Current volume "+str(volume)+". Use the arrow keys to change the volume in 1% increments, page up and page down for 10% increments.")

	while True:
		process_events()
		mainloop()
		if key_pressed(K_ESCAPE) or key_pressed(K_RETURN) or key_pressed(pygame.K_KP_ENTER):
			if 1:
				if len(g.p1)!=0:
					p1=g.p1.pop()
					p2=g.p2.pop()
					p3=g.p3.pop()
					p4=g.p4.pop()
					speak("Volume changed to "+str(volume))
					serverside_menu(p1,p2,p3,p4)
					process_events()
					return
				else:
					speak("Volume changed to "+str(volume))
					process_events()
					return

		if key_holding(K_DOWN) or key_holding(K_LEFT):
			if volume>0:
				volume-=1
				speak(volume)
				g.playervolumes[name]=volume
				g.p.play_stationary("windows_background.ogg",False)
		if key_holding(K_HOME):
			if volume>0:
				volume=0
				speak(volume)
				g.playervolumes[name]=volume
				g.p.play_stationary("windows_background.ogg",False)
		if key_holding(K_END):
			if volume<100:
				volume=100
				speak(volume)
				g.playervolumes[name]=volume
				g.p.play_stationary("windows_background.ogg",False)


		if key_holding(K_UP) or key_holding(K_RIGHT):
			if volume<100:
				volume+=1
				speak(volume)
				g.playervolumes[name]=volume
				g.p.play_stationary("windows_background.ogg",False)

		if key_holding(K_PAGEDOWN):
			if volume>0:
				volume-=10
				if volume<0: volume=0
				speak(volume)
				g.playervolumes[name]=volume
				g.p.play_stationary("windows_background.ogg",False)

		if key_holding(K_PAGEUP):
			if volume<100:
				volume+=10
				if volume>100: volume=100
				speak(volume)
				g.playervolumes[name]=volume
				g.p.play_stationary("windows_background.ogg",False)
def walking():
	if g.stopwalktimer.elapsed<2000: return True
	if g.lastdir==Forward:
		if g.usesub==1 and key_down(K_UP): return True
		if g.usesub==0 and key_down(K_w): return True
	if g.lastdir==Backward:
		if g.usesub==1 and key_down(K_DOWN): return True
		if g.usesub==0 and key_down(K_s): return True
	if g.lastdir==Up:
		if 1 and key_down(K_PAGEUP): return True
	if g.lastdir==Down:
		if 1 and key_down(K_PAGEDOWN): return True

	if g.lastdir==Left:
		if g.usesub==1 and key_down(K_LEFT): return True
		if g.usesub==0 and key_down(K_a): return True
	if g.lastdir==Right:
		if g.usesub==1 and key_down(K_RIGHT): return True
		if g.usesub==0 and key_down(K_d): return True
	return False
def invmenu():
	if g.mapname=="jail": return
	if len(g.inv.keys()) == 0:
		speak("No items")
		return
	m.reset(True)
	m.enable_up_and_down=True
	m.wrap=False
	m.enable_first_letter_navigation=True
	m.wrap_sound=""
	m.allow_escape=True
	m.enable_home_and_end=True
	m.click_sound="category"+str(random(1,6))+".ogg"
	m.enter_sound="invclose.ogg"
	m.open_sound="invopen.ogg"
	m.callback2=invclb
	if g.mapname!="lobby": g.n.send_reliable(0,"xplay invopen",0)
	items=list(g.inv.keys())
	for item in items:
		name=item
		amount=g.inv[item]
		try: m.add_item_tts(name+": You have "+str(amount)+".", name)
		except: pass
	mres=m.run("Inventory menu. You have "+str(len(items))+" items.", True)
	if g.mapname!="lobby": g.n.send_reliable(0,"xplay invclose",0)
	if mres == 0:
		m.play(m.enter_sound)
		return
	else:
		g.invpos=mres-1
		return
def invclb():
	mainloop()
	if key_pressed(K_LEFT):
		try: item=m.get_item_name(m.position+1)
		except: return
		if g.reloading or g.drawing or item not in guns or g.weapons[g.w]==item: return
		g.n.send_reliable(0, "draw "+item+"", 0)
		speak(item)
		g.weapons.append(item)
		g.w=len(g.weapons)-1
		if g.weapons2[g.w2]==g.weapons[g.w]: g.n.send_reliable(0,"unequip2",0); g.w2=0
	if key_pressed(K_RIGHT):
		try: item=m.get_item_name(m.position+1)
		except: return
		if g.reloading or g.drawing or item not in guns or g.weapons2[g.w2]==item: return
		g.n.send_reliable(0, "draw2 "+item+"", 0)
		speak(item)
		g.weapons2.append(item)
		g.w2=len(g.weapons2)-1
		if g.weapons2[g.w2]==g.weapons[g.w]: g.n.send_reliable(0,"unequip",0); g.w=0


	if((key_pressed(K_BACKSPACE) or joystick_button_pressed(g.jcontrols.get("invdrop",-1))) and g.can_move==True):
	
		if g.falling==True or g.jumping==True:
			speak("you can not drop an item right now!")
		else:
			if g.mapname!="lobby" and not g.zombie:
				try: item=m.get_item_name(m.position+1)
				except: pass
				dropitem(item,shift_is_down())
			
		

g.mouse_update=mouse_update
def get_rain_sound():
	if g.get_ignore_ambience_at(round(g.me.x),round(g.me.y),round(g.me.z)): return "rainhome.ogg"
	if g.mapname=="lobby" or "basement" in g.mapname or "match" in g.mapname: return "rainhome.ogg"
	if "flag" in g.mapname or "massacre" in g.mapname or "main" in g.mapname or "zombie" in g.mapname: return "rainext.ogg"
	return "rainhome.ogg"
g.get_rain_sound=get_rain_sound
def handle_voicechat_data2(p):

	while 1:
		time.sleep(0.010)
		playing=p.voice_sound2 is not None and p.voice_sound2.playing()
		if len(p.audio_buffer2)>=20 and not p.alplayed2:
			p.alplayed2=True
			play_audio2(p,p.audio_buffer2)
		elif p.alplayed2:
			if not playing and len(p.audio_buffer2)>=20: play_audio2(p,copy.copy(p.audio_buffer2))


def get_rain_sound_camera():
	if g.get_ignore_ambience_at(round(g.camera.x),round(g.camera.y),round(g.camera.z)): return "rainhome.ogg"
	if g.mapname=="lobby" or "basement" in g.mapname or "match" in g.mapname: return "rainhome.ogg"
	if "massacre" in g.mapname or "main" in g.mapname or "zombie" in g.mapname: return "rainext.ogg"
	return "rainhome.ogg"
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

def get_aim_str():
	if g.aim==0: return" forward"
	if g.aim_mode==0:
		if g.aim<0: return str(abs(g.aim))+" steps down"
		if g.aim>0: return str(g.aim)+" steps up"
	if g.aim==1: return "half up"
	if g.aim==2: return "streight up"
	if g.aim==-1: return "half down"
	if g.aim==-2: return "streight down"
def autotracktoggle():
	if g.autotrack==0:
		g.autotrack=1
		speak("auto tracking enabled")
	elif g.autotrack==1:
		g.autotrack=0
		speak("auto tracking disabled")
def get_max_aim():
	if g.aim_mode==1: return 2
	return g.maxaim
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
def is_cheater():
	if ctypes.windll.kernel32.IsDebuggerPresent(): return True
	return is_memory_scan_detected() or is_speed_hack_detected()
import hashlib

def file_get_hash_sha256(filename):
	sha256 = hashlib.sha256()
	try:
		with open(filename, "rb") as f:
			for chunk in iter(lambda: f.read(4096), b""):
				sha256.update(chunk)
		return sha256.hexdigest()
	except FileNotFoundError:
		return None
	except Exception as e:
		return None
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


class VPDError(Exception):
	"""Base class for exceptions in VirtualPyDetector."""
	def __init__(self, message):
		super().__init__(message)

class Detector:
	"""
	Comprehensive detection system for virtual environments, sandboxes, and debuggers.
	Combines multiple detection techniques across different platforms with multiprocessing.
	"""

	class VMChecks:
		"""Virtual machine detection methods using hardware and system artifacts."""
		
		@staticmethod
		def check_vm_hardware() -> bool:
			"""Detect VM through system hardware information."""
			system = platform.system()
			
			if system == "Windows":
				# MODIFIED: Uses the WMI library instead of the deprecated wmic.exe
				if not wmi: return False
				try:
					c = wmi.WMI()
					# There's typically only one Win32_ComputerSystem instance
					system_info = c.Win32_ComputerSystem()[0]
					model = system_info.Model.lower()
					
					vm_indicators = ("vmware", "virtualbox", "hyper-v", "kvm", "qemu")
					
					return any(indicator in model for indicator in vm_indicators)
				except pywintypes.com_error:
					# This can happen if WMI services are disabled or permissions are denied.
					# Safest to assume it's not a VM in this case.
					return False
				except IndexError:
					# This is rare, but means the WMI query returned no results.
					return False
				except Exception as e:
					raise VPDError(f"An unexpected error occurred during WMI hardware check: {e}")

			elif system == "Darwin":  # macOS
				try:
					output = subprocess.check_output(
						["sysctl", "hw.model"], 
						encoding="utf-8", 
						timeout=3
					)
					return any(vm.lower() in output.lower() for vm in ("VMware", "VirtualBox"))
				except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
					return False

			elif system == "Linux":
				try:
					# systemd-detect-virt is the most reliable modern method
					output = subprocess.check_output(
						["systemd-detect-virt"], 
						encoding="utf-8", 
						timeout=3
					)
					return output.strip() != "none"
				except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
					# Fallback for non-systemd systems could be added here if needed
					return False
				
			return False

		@staticmethod
		def check_mac_address() -> bool:
			"""Check for virtualization-related MAC address prefixes."""
			return False
			vm_mac_prefixes = {
				"00:05:69", "00:0C:29", "00:50:56", # VMware
				"08:00:27", # VirtualBox
				"00:1C:14", # Parallels
				"00:03:FF", # Microsoft Hyper-V
				"52:54:00"  # QEMU
			}
			try:
				for iface, addrs in psutil.net_if_addrs().items():
					for addr in addrs:
						if addr.family == psutil.AF_LINK:
							mac = addr.address.upper().replace("-", ":")
							if mac[:8] in vm_mac_prefixes:
								return True
			except Exception:
				return False
			return False

		@staticmethod
		def check_vm_artifacts() -> bool:
			"""Check for existence of known virtualization software artifacts."""
			vm_paths = []
			if platform.system() == "Windows":
				vm_paths = [
					os.path.expandvars("%ProgramFiles%\\VMware\\VMware Tools"),
					os.path.expandvars("%ProgramFiles%\\Oracle\\VirtualBox Guest Additions")
				]
			elif platform.system() == "Darwin":
				vm_paths = [
					"/Applications/VMware Fusion.app",
					"/Applications/VirtualBox.app"
				]
			return Detector.HelperFunctions.check_paths_exist(vm_paths)

		@staticmethod
		def check_virtualbox_drivers() -> bool:
			"""Detect VirtualBox drivers on Windows systems."""
			return False

			drivers = [
				"VBoxGuest.sys", "VBoxMouse.sys", "VBoxSF.sys", "VBoxVideo.sys"
			]
			driver_paths = [os.path.join(os.environ["SystemRoot"], "System32", "drivers", driver) for driver in drivers]
			return Detector.HelperFunctions.check_paths_exist(driver_paths)

		@staticmethod
		def check_cpu_features() -> bool:
			"""Detect CPU features indicating virtualization environment."""
			if platform.system() == "Linux":
				try:
					with open("/proc/cpuinfo", "r") as cpuinfo:
						return any("hypervisor" in line for line in cpuinfo)
				except FileNotFoundError:
					return False
			elif platform.system() == "Darwin":
				try:
					output = subprocess.check_output(["sysctl", "machdep.cpu.features"], encoding="utf-8", timeout=3)
					return "VMM" in output  # Virtual Machine Monitor flag
				except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
					return False
			return False

	class DebuggerChecks:
		"""Debugger and sandbox detection methods."""
		
		@staticmethod
		def check_hypervisor() -> bool:
			"""Detect hypervisor presence using platform-specific APIs."""
			return False
			if platform.system() == "Windows":
				try: return bool(ctypes.windll.kernel32.IsHypervisorPresent())
				except (AttributeError, OSError): return False
			elif platform.system() == "Darwin":
				try:
					output = subprocess.check_output(["sysctl", "kern.hv_support"], encoding="utf-8", timeout=3)
					return "1" in output
				except (subprocess.CalledProcessError, subprocess.TimeoutExpired): return False
			return False

		@staticmethod
		def check_sandbox_files() -> bool:
			"""Check for files/directories indicative of sandbox environments."""
			if platform.system() != "Windows": return False
			# Check for Windows Sandbox user profile
			sandbox_user_profile = os.path.expandvars("%userprofile%")
			if "WDAGUtilityAccount" in sandbox_user_profile:
				return True
			return False

		@staticmethod
		def detect_debugger() -> bool:
			"""Detect debugger presence through platform-specific methods."""
			if platform.system() == "Windows":
				try:
					return bool(ctypes.windll.kernel32.IsDebuggerPresent())
				except (AttributeError, OSError):
					return False
			elif platform.system() in {"Darwin", "Linux"}:
				if not psutil: return False
				try:
					parent_process = psutil.Process(os.getppid()).name().lower()
					return parent_process in {"lldb", "gdb"}
				except (psutil.NoSuchProcess, psutil.AccessDenied):
					return False
			return False

		@staticmethod
		def anti_timing_check(threshold: float = 0.5) -> bool:
			"""Detect timing anomalies suggestive of virtualization/debugging."""
			return False
			start_time = time.perf_counter()
			for _ in range(1_000_000):
				pass
			elapsed = time.perf_counter() - start_time
			return elapsed > threshold

	class ProcessChecks:
		"""Detection of suspicious processes associated with analysis environments."""
		
		@staticmethod
		def detect_suspicious_processes() -> bool:
			"""Threaded detection of known sandbox/VM-related processes."""
			if not psutil: return False
			suspicious_processes: Set[str] = {
				"vmtoolsd.exe", "vboxservice.exe", "wireshark.exe",
				"fiddler.exe", "charles.exe", "sandboxie.exe", "processhacker.exe"
			}

			def process_check(proc: psutil.Process) -> bool:
				try: return proc.name().lower() in suspicious_processes
				except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess): return False

			with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
				futures = {executor.submit(process_check, p) for p in psutil.process_iter()}
				for future in as_completed(futures):
					if future.result():
						return True
			return False

	class HelperFunctions:
		"""Enhanced utility methods with error handling."""
		
		@staticmethod
		def check_paths_exist(paths: List[str]) -> bool:
			"""Safely check multiple paths for existence."""
			return any(os.path.exists(path) for path in paths)

	def __init__(self):
		# A quick check to make sure necessary libraries are installed
		if platform.system() == "Windows" and wmi is None:
			raise ImportError("The 'WMI' and 'pywin32' packages are required on Windows.")
		if psutil is None:
			raise ImportError("The 'psutil' package is required for process and network checks.")

	@property
	def venv_active(self) -> bool:
		"""
		Optimized multiprocess check that runs all detection methods in parallel
		and returns True as soon as any single check finds something suspicious.
		This is the most efficient way to get a general "is this a suspicious environment?" answer.
		"""
		all_checks = [
			self.VMChecks.check_vm_hardware,
			self.VMChecks.check_mac_address,
			self.VMChecks.check_vm_artifacts,
			self.VMChecks.check_cpu_features,
			self.VMChecks.check_virtualbox_drivers,
			self.DebuggerChecks.check_hypervisor,
			self.DebuggerChecks.check_sandbox_files,
			self.DebuggerChecks.detect_debugger,
			self.DebuggerChecks.anti_timing_check,
			self.ProcessChecks.detect_suspicious_processes,
		]

		try:
			with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
				futures = {executor.submit(check) for check in all_checks}
				for future in as_completed(futures):
					if future.result():
						# As soon as one check is true, we're done.
						# We can tell the other processes to stop, saving resources.
						executor.shutdown(wait=False, cancel_futures=True)
						return True
			return False
		except Exception as e:
			raise VPDError(f"Multiprocess check failed: {e}")

	@property
	def is_virtualized(self) -> bool:
		"""Check if the environment is a virtual machine."""
		return any((
			self.VMChecks.check_vm_hardware(),
			self.VMChecks.check_mac_address(),
			self.VMChecks.check_vm_artifacts(),
			self.VMChecks.check_cpu_features(),
			self.DebuggerChecks.check_sandbox_files(),
			self.VMChecks.check_virtualbox_drivers()
		))

	@property
	def is_debugged(self) -> bool:
		"""Check if a debugger is attached."""
		return any((
			self.DebuggerChecks.detect_debugger(),
			self.DebuggerChecks.anti_timing_check(),
		))

	@property
	def is_sandboxed(self) -> bool:
		"""Check if in a sandbox environment."""
		return any((
			self.DebuggerChecks.check_sandbox_files(),
			self.ProcessChecks.detect_suspicious_processes(),
		))
	
	@property
	def is_analyzed(self) -> bool:
		"""Umbrella check: returns True if virtualized, debugged, or sandboxed."""
		return self.is_virtualized or self.is_debugged or self.is_sandboxed
	
	@property
	def is_safe(self) -> bool:
		"""Returns True if no analysis environment is detected."""
		return not self.is_analyzed
	
	def get_all_checks(self) -> Dict[str, bool]:
		"""Return a dictionary with the results of every individual check."""
		return {
			"is_virtualized": self.is_virtualized,
			"is_debugged": self.is_debugged,
			"is_sandboxed": self.is_sandboxed,
			"venv_active (parallel check)": self.venv_active,
			"detailed_results": {
				"vm_hardware": self.VMChecks.check_vm_hardware(),
				"vm_mac_address": self.VMChecks.check_mac_address(),
				"vm_file_artifacts": self.VMChecks.check_vm_artifacts(),
				"vm_cpu_features": self.VMChecks.check_cpu_features(),
				"vm_vbox_drivers": self.VMChecks.check_virtualbox_drivers(),
				"debugger_present_api": self.DebuggerChecks.detect_debugger(),
				"timing_anomaly": self.DebuggerChecks.anti_timing_check(),
				"suspicious_processes": self.ProcessChecks.detect_suspicious_processes(),
				"sandbox_files": self.DebuggerChecks.check_sandbox_files(),
				"hypervisor_api": self.DebuggerChecks.check_hypervisor(),
			}
		}

# --- New Simple Function ---
def is_vm() -> bool:
	"""
	A simple, standalone function to quickly check if the code is running
	inside a known virtual machine.

	This is a convenient shortcut that creates a Detector instance and
	returns the result of its `is_virtualized` check.

	Returns:
		bool: True if a virtual machine is detected, False otherwise.
	"""
	try:
		detector = Detector()
		return detector.is_virtualized
	except (ImportError, VPDError):
		# If libraries are missing or a major error occurs, assume it's a safe environment.
		return False
def get_firetime():
	if g.weaponauto: return 15
	return 10
def get_firetime2():
	if g.weaponauto2: return 15
	return 10
if __name__=="__main__": main()
