from network import event_receive
import subprocess
from network import event_connect
import re
from bs4 import BeautifulSoup
import time
import pyaudio
from network import event_disconnect
from events import process_events, key_pressed
from pygame.locals import *
from variable_management import string_to_number, string_contains, string_split
import webbrowser
import wx
import ctypes
from speech import speak
from variable_management import string_replace
from dlg import dlg
import globals as g
from rotation import calculate_x_y_angle
import sound
from menu_system import menu
from net import login, create
from net import login, netaddress
from net import login, netport

import sys
import pygame
from random import randint as random
import sound
from input import get_input
from Miscellaneous import exit
from translation import translate as _
m=menu()

def lang():
	setupmenu(False)
	m.add_item_tts("English","en")
	m.add_item_tts("Turkish","turkish")
	m.add_item_tts("Vietnamese","Vietnamese")
	m.add_item_tts("Spanish","Spanish")
	m.add_item_tts("português","português")

	m.add_item_tts("Back to main menu","back")
	mres=m.run("Please select a language.",True)
	if mres==0 or m.get_item_name(mres)=="back": mainmenu()
	g.lang=m.get_item_name(mres)
	g.lngdata=""
	g.transcache.clear()
	mainmenu()
def setturningmenu():
	setupmenu(False)
	m.add_item_tts("faster","6")
	m.add_item_tts("default","12")
	m.add_item_tts("slower","18")
	m.add_item_tts("Back to settings","back")
	mres=m.run("Please select an option.",True)
	if (m.get_item_name(mres)=="12"):
		g.turningtimeelapsing=12
		speak("choosed to default")
		g.writeprefs()
		option()
	if (m.get_item_name(mres)=="6"):
		g.turningtimeelapsing=6
		speak("choosed to faster")
		g.writeprefs()
		option()
	if (m.get_item_name(mres)=="18"):
		g.turningtimeelapsing=18
		speak("choosed to slower")
		g.writeprefs()
		option()
	if (m.get_item_name(mres)=="back"):
		option()
def login_settings():
	try: g.n.destroy()
	except: pass
	setupmenu(True)
	if g.name!="" and g.savemail!="":
		m.add_item_tts(_("Sign in as %s")%g.name,"play")

	m.add_item_tts("setup an existing account","setup")

	m.add_item_tts("Create An Account","create")
	m.add_item_tts("Recover your password","pr")
	m.add_item_tts("Back to main menu","back")
	mres=m.run("Please select an option.",True)
	if (m.get_item_name(mres)=="pr"):
		namew=get_input("Enter username")
		mailw=get_input("enter the mail of this account.")

		if namew!="" and mailw!="": pr(namew,mailw)
		login_settings()
	if (m.get_item_name(mres)=="play"):
	
		login()
		
	if (m.get_item_name(mres)=="setup"):
		username=get_input("Type your username")
		if username=="":
			dlg("you can not leave this input blank")
			login_settings()
		maillol=get_input("Type the account mail")
		if maillol=="":
			dlg("you can not leave this input blank")
			login_settings()

		password=get_input("please enter your password")
		if password=="":
			dlg("you can not leave this input blank")
			login_settings()
		g.password=password
		g.name=username
		g.savemail=maillol
		g.writeprefs()
		speak("The account information you entered has been successfully set for login.")
		login_settings()
	if (m.get_item_name(mres)=="create"):
	
		create()
		

	if (m.get_item_name(mres)=="back"):
		mainmenu()
def donatemenu():
	try: g.n.destroy()
	except: pass
	setupmenu(True)
	m.add_item_tts("Donate with using card.","card")
	m.add_item_tts("Donate with PayPal.","paypal")

	m.add_item_tts("Back to main menu","back")
	mres=m.run("Please select an option.",True)
	if (m.get_item_name(mres)=="card"):
		speak("Loading the browser...")
		webbrowser.open("https://nbmstudios.com/donate.php")
		mainmenu()

	if (m.get_item_name(mres)=="paypal"):
		speak("Loading the browser...")
		webbrowser.open("https://paypal.me/nbmdigital")
		mainmenu()

	if (m.get_item_name(mres)=="back"):
		mainmenu()

def option():
	setupmenu(False)
	m.callback2 = option_callback

	toggle_options = [
#		("logo", "playcanlogo", "logo play at startup"),
		("yavaslat", "yavaslat", "game performance. Note: When you disable this, your computer will use more RAM and CPU to deliver the best performance in the game. If you enable it, your game may lag during multitasking or battles, especially if your computer has low specifications."),

		("near", "near", "announcement of near players"),
		("bsave", "buffersave", "saving of buffer items when exiting the game"),
		("interrupt", "interrupt", "speech interrupt"),
		("listen", "listen", "listening your own voice while voicechatting"),
		("push", "push", "push to talk for voicechat"),
		("bufferlog", "bufferlog", "Save buffer messages to the log.txt"),
		("steam", "steam", "Use Steam Audio for 3d audio, disable this if it causes lag issues"),
		#("aim", "stopaim", "Stop aiming when key is not held down"),
		("cache", "cache", "caching of sounds"),
		("itembeep", "itembeep", "Item beeping"),
		("qturn", "qturn", "Turning with q and e"),
		("speakdegree", "speakdegree", "Speak degrees when turning in 1 degree increments"),
		("speakfacing", "speakfacing", "Speak facing direction when turning in 45 degree increments"),
		("fastwalk", "fastwalk", "Auto running"),
		("mouse", "usemouse", "turning and shooting with mouse"),
		("sign", "signbeepsound", "hearing map sign sound"),
		("onlinen", "onlinemsg", "online and offline messages"),
		("killcount", "killcounter", "kill counter notification"),
		("sub", "usesub", "classic walking style"),
		("windowa", "awindow", "muting of speech and audio when the game window is not in focus"),
		("mapmusicarea", "musicplayinthemap", "Play match-specific music in the game"),
		("weaponscope", "scope", "scope"),
	]

	for option_name, attribute, description in toggle_options:
		enabled = getattr(g, attribute) == 1
		action = "Disable" if enabled else "Enable"
		m.add_item_tts(f"{action} {description}", option_name, False)

	m.add_item_tts("Configure joystick buttons", "joy")
	m.add_item_tts(f"Set turning speed. Currently {get_turning_speed()}", "turningchoose")
	m.add_item_tts("Select input device for voicechat", "inputdevice")
	m.add_item_tts("test voicechat", "test")
	#m.add_item_tts("Set who you want to voicechat with", "who")
	m.add_item_tts("Set who's near notifications you want to receive", "who2")
	m.add_item_tts("Set what indicators you want to hear for near players/bots","nearvoice")
	m.add_item_tts("Set voicechat quality", "bitrate")
	m.add_item_tts("Set voicechat volume", "volume")
	m.add_item_tts("Select output device", "outputdevice")
	
	if not g.inthegame:
		m.add_item_tts("back to main menu", "back")
	else:
		m.add_item_tts("back to game menu", "back")

	mres = m.run("zero hour assault settings. Please select an option.", True)
	handle_menu_selection(m.get_item_name(mres))
def option_callback():
	try: g.netloop()
	except: pass
	if key_pressed(K_RETURN):
		item = m.get_item_name(m.position + 1)
		toggle_option(item)

def toggle_option(option_name):
	option_map = {
#		"logo": "playcanlogo",
		"near": "near",
		"yavaslat": "yavaslat",

		"bsave": "buffersave",
		"interrupt": "interrupt",
		"listen": "listen",
		"push": "push",
		"steam": "steam",
		#"aim": "stopaim",
		"cache": "cache",
		"bufferlog": "bufferlog",
		"ucd": "ucd",
		"qturn": "qturn",

		"fastwalk": "fastwalk",
		"speakdegree": "speakdegree",
		"speakfacing": "speakfacing",

		"mouse": "usemouse",
		"sign": "signbeepsound",
		"onlinen": "onlinemsg",
		"killcount": "killcounter",
		"sub": "usesub",
		"windowa": "awindow",
		"mapmusicarea": "musicplayinthemap",
		"weaponscope": "scope",
	}

	if option_name in option_map:
		attribute = option_map[option_name]
		current_value = getattr(g, attribute)
		new_value = 1 - current_value
		setattr(g, attribute, new_value)
		action = "enabled" if new_value == 1 else "disabled"
		speak(action)
		g.writeprefs()
		update_menu_item(option_name, new_value)

def update_menu_item(option_name, new_value):
	for item in m.items:
		if item.name == option_name:
			action = "Disable" if new_value == 1 else "Enable"
			item.text = item.text.replace("Enable", action).replace("Disable", action)
			break

def get_turning_speed():
	if g.turningtimeelapsing == 6:
		return "faster"
	elif g.turningtimeelapsing == 18:
		return "slower"
	else:
		return "default"

def handle_menu_selection(selection):
	menu_actions = {
		"test": testvoicechat,
		"joy": joymenu,
		"inputdevice": inputdevicemenu,
		"who": whomenu,
		"who2": who2menu,
		"nearvoice": nearvoicemenu,
		"bitrate": bitratemenu,
		"volume": volumemenu,
		"turningchoose": setturningmenu,
		"outputdevice": outputdevicemenu,
		"back": lambda: mainmenu() if not g.inthegame else g.game(False)
	}

	if selection in menu_actions:
		menu_actions[selection]()
	else:
		option()
def outputdevicemenu():
	setupmenu(False)
	devices = sound.get_available_output_devices()
	m.add_item_tts("default",None)
	for device_name in devices:
		if isinstance(device_name, bytes):
			label=device_name.decode("utf-8","ignore")
		else:
			label=str(device_name)
		if label!="": m.add_item_tts(label.lower(), device_name)
	m.add_item_tts("Back to settings", "back")
	if g.inthegame: m.callback2 = g.mainloop
	mres = m.run("Please select the audio output device.", True)
	choice = m.get_item_name(mres)
	if mres == 0 or choice == "back":
		option()
	g.soundcard=choice
	restartmenu()
def mainmenu():
	setupmenu(True)
	g.inthegame=False
	m.add_item_tts("Login Options","login_settings")
	m.add_item_tts("settings","option")
	m.add_item_tts("Learn game sounds","sounds")
	m.add_item_tts("View ranking list.","score")
	m.add_item_tts("View game readme file","readme")
	m.add_item_tts("View game rules.","rules")
	m.add_item_tts("View privacy.","privacy")

	m.add_item_tts("Make us a small donation. If you like the game and if you can, a small donation would be appreciated.","donate")
	m.add_item_tts("join the official telegram group of Zero Hour Assault.","telegram")
	m.add_item_tts("Exit the game.","exit")
	mres=m.run("zero hour assault Main Menu. Please select an option using the up and down arrow keys and press enter to confirm. Use the page up and page down keys to adjust the music volume.",True)
	if (m.get_item_name(mres)=="readme"): readmemenu()
	if (m.get_item_name(mres)=="rules"): rulesmenu()
	if (m.get_item_name(mres)=="privacy"): privacymenu()

	if (m.get_item_name(mres)=="sounds"): soundsmenu()

	if (m.get_item_name(mres)=="telegram"): webbrowser.open("https://www.t.me/zerohournbm"); mainmenu()

	if (m.get_item_name(mres)=="donate"): donatemenu()

	if (m.get_item_name(mres)=="score"):
		connect()
	if (m.get_item_name(mres)=="login_settings"):
		g.p.play_stationary("misc250.ogg",False)
		login_settings()

	if (m.get_item_name(mres)=="paypal"):
		speak("Loading the browser...")
		webbrowser.open("https://paypal.me/nbmdigital")
		mainmenu()
	if (m.get_item_name(mres)=="option"):
	
		g.p.play_stationary("misc261.ogg",False)

		option()
	if (m.get_item_name(mres)=="lang"):
	
		lang()

	elif(m.get_item_name(mres)=="exit" or mres==0):
	

		g.writeprefs()
		m.kill_music()

		exit()
	
def connect():
	speak("connecting")
	g.reset(False)
	g.n.setup_client(100, 100)
	g.n.connect(netaddress, netport)
	while(True):
		process_events()
		if(key_pressed(K_ESCAPE)):
			g.reset()
			mainmenu()
		g.e=g.n.request()
		if(g.e.type==event_receive):
			parsed=string_split(g.e.message," ",True)
			if(parsed[0]=="launchmenu"):
				i=string_replace(parsed[1],"[SPCE]"," ",True)
				t=string_replace(parsed[2], "[SPCE]", " ", True)
				items=string_replace(g.e.message,parsed[0]+" "+parsed[1]+" "+parsed[2]+" ","",True)
				serverside_menu(t,i,items,False)
				g.reset()
				mainmenu()

		if(g.e.type==event_connect):
			speak("Successfully connected. Requesting scoreboard table...")
			g.p.play_stationary("newmenuopen1.ogg",False)
			g.n.send_reliable(0,"zero"*4,0)
			g.n.send_reliable(0,"scoreboard",0)
		if(g.e.type==event_disconnect):
			g.reset()
			connect()

def setupmenu(music=False, online=False, prevmenu=False, allowopen=True,canwork=False):
	global m
	if not music:
		m=menu()

	else:
		m=menu(music="menumusic5.ogg")

	m.up_and_down=True
	m.left_and_right=False
	m.pan_sounds=False
	m.wrap=False
	m.wrap_sound="newmenuedge.ogg"
	m.home_and_end=True
	m.edge_sound="newmenuedge.ogg"
	m.click_sound="newmenumove.ogg"
	m.enter_sound="newmenuclick"+str(random(1,6))+".ogg"
	if g.inthegame: m.callback2=g.mainloop
	if not prevmenu and allowopen and canwork==False: g.p.play_stationary("newmenuopen"+str(random(1,3))+".ogg",False)
def menunet(stuff):
	g.mainloop()
	
def select_player(text, data):
	if data=="":
		speak("There is no one on this map.")
		return
	setupmenu(False, True)
	parsed=string_split(data, "\n", True)
	for i in range(len(parsed)):
		if parsed[i]=="": continue
		m.add_item_tts(parsed[i],parsed[i])
		
	m.add_item_tts("Go back","back")
	mres=m.run(text, True)
	if(m.get_item_name(mres)=="back" or mres==0):
		return ""
		
	else:
	
		return m.get_item_name(mres)
	return
		
	
g.select_player=select_player
def invmenu():
	if(len(g.inv)==0):
	
		speak("No items")
		return
		
	m.reset(True)
	m.up_and_down=True
	m.wrap=True
	m.click_sound="invmove.ogg"
	m.enter_sound="newmenuclick"+str(random(1,6))+".ogg"
	m.open_sound="invopen.ogg"
	items=list(g.inv.keys())
	a=0
	for i in range(len(items)):
	
		a=g.inv[items[i]]
		m.add_item_tts(items[i]+": You have "+str(a)+".",items[i])
		
	mres=m.run("Inventory menu. You have "+str(len(items))+" items.",True)
	if(mres==0):
	
		return
		
	else:
	
		g.invpos=mres-1
		return
		
	
def serverside_menu(sndtxt, menu, menuitems, store=False):
	peer = getattr(g.n, "peer", None) or getattr(g.n, "secure_peer", None)
	if peer is not None:
		g.n.disconnect_peer(peer)
	g.n.destroy()
	setupmenu(False, False,True)
	m.enter_sound=""
	m.click_sound=""

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
				m.add_item_tts(parsed[0], parsed[1], enabled=False)
	m.add_item_tts("Back to main menu","back")
	mres=m.run(menu, True)
	if m.get_item_name(mres) == "back":
		g.p.play_stationary("newmenuclick"+str(random(1,6))+".ogg",False)

		g.reset(False)
		mainmenu()
	else:
		if not store:
			g.n.send_reliable(0, sndtxt+" "+m.get_item_name(mres), 0)
def sampleratemenu():
	setupmenu(False)
	m.add_item_tts("8 KHz","8000")
	m.add_item_tts("12 KHz","12000")
	m.add_item_tts("16 KHz","16000")
	m.add_item_tts("24 KHz","24000")
	m.add_item_tts("48 KHz","48000")
	m.add_item_tts("Back to settings","back")
	mres=m.run("Please select a sample rate.",True)
	rate=m.get_item_name(mres)
	if rate=="back" or mres==0: option()
	speak("done")
	g.samplerate=int(rate)
	g.writeprefs()
	g.reinit_voicechat()
	option()
def bitratemenu():
	setupmenu(False)
	m.add_item_tts("Low quality","8000")
	m.add_item_tts("Medium quality","16000")
	m.add_item_tts("High quality (Recommended)","32000")
	m.add_item_tts("Very high quality (may cause choppiness/lag)","64000")
	m.add_item_tts("Back to settings","back")
	if g.inthegame: m.callback2=g.mainloop
	mres=m.run("Select quality",True)
	value=m.get_item_name(mres)
	if mres==0 or value=="back": option()
	value=int(value)
	if value<500: dlg("Value is too small!"); option()
	elif value>300000: dlg("Value is too large!"); option()
	g.bitrate=value
	speak("Done")
	g.writeprefs()
	g.reinit_voicechat()
	option()
def qualitymenu():
	value=get_input("Enter the desired quality, it should be between 0 and 9. Default is 0.")
	if value=="": option()
	try:
		value=int(value)
	except:
		dlg("Invalid value")
		option()
	if value<0: dlg("Value is too small!"); option()
	elif value>9: dlg("Value is too large!"); option()
	g.complexity=value
	speak("Done")
	g.writeprefs()
	g.reinit_voicechat()
	option()

def volumemenu():
	value=prompt_slider("Use the arrow keys to adjust the volume and press the OK button to confirm. Use home and end to set it to 0% and 100%, and use the page up and page down keys to adjust it by 10%.",g.volumeg)
	try:
		value=int(value)
	except:
		dlg("Invalid value")
		option()
	g.volumeg=value
	speak("Done")
	g.writeprefs()
	option()
def whomenu():
	setupmenu(False)
	m.callback2=voice_callback
	m.add_item_tts("With friends: "+("enabled" if g.voicechatfriend==1 else "disabled"),"friend",False)
	m.add_item_tts("With players on the same map as me: "+("enabled" if g.voicechatmap==1 else "disabled"),"map",False)
	m.add_item_tts("With players on the same group as me: "+("enabled" if g.voicechatgroup==1 else "disabled"),"group",False)

	m.add_item_tts("With players who are in the same team as me: "+("enabled" if g.voicechatteam==1 else "disabled"),"team",False)
	m.add_item_tts("Back to settings","back")
	mres=m.run("Please select an option.",True)
	choice=m.get_item_name(mres)
	if mres==0 or choice=="back": option()
	g.voicechatwho=choice
	g.writeprefs()
	option()
def inputdevicemenu():
	setupmenu(False)
	exclude_keywords = ["virtual", "loopback", "line", "stereo mix","Stereo", 
	"vb-audio", "voice mod", "cable", "wavetable", 
	"aux", "monitor", "digital", "wave", "default"]
	for i in range(g.pa.get_device_count()):
		device_info = g.pa.get_device_info_by_index(i)
		device_name = device_info['name'].lower()
		if (not any(keyword in device_name for keyword in exclude_keywords) and 
			device_info['maxInputChannels'] > 0 and 
			device_info['hostApi'] == 0):
			m.add_item_tts(device_info['name'], str(i))
	m.add_item_tts("Back to settings", "back")
	if g.inthegame: m.callback2 = g.mainloop
	mres = m.run("Please select the device you want to use.", True)
	choice = m.get_item_name(mres)
	if mres == 0 or choice == "back":
		option()
	g.inputdevice = int(choice)
	g.writeprefs()
	g.reinit_voicechat()
	option()
def joymenu():
	joyavailcheck()
	dlg("Welcome to joystick button configuration. In this section, you have to set what buttons of your joystick you want to use in the game to perform in-game actions. The game will speak some actions. What you have to do is to press the button on the joystick which you want to use for performing this action. At any time, you can pres escape key or the left D-pad button to cancel the configuration and go back to the options menu. Press enter or the right D-Pad button to continue.")
	joyconf()
def joyavailcheck():
	if len(g.sticks)==0:
		speak("Error, no joystick found. Waiting for joysticks ... Press escape to cancel.")
		while len(g.sticks)==0:
			process_events()
			if key_pressed(K_ESCAPE): option()
		dlg("Joystick found. Press enter to continue.")
def joyavailcheck2():
	if len(g.sticks)<=0:
		speak("Joystick removed. Please reinsert it to continue the configuration process. Press escape to cancel confiugration.")
		while len(g.sticks)<=0:
			process_events()
			if key_pressed(K_ESCAPE): option()
		dlg("Joystick inserted. Press enter to continue.")
def joyconf():
	speak("jump")
	g.jcontrols["jump"]=joyaskbutton()
	speak("reload weapon")
	g.jcontrols["reload"]=joyaskbutton()
	speak("fire weapon")
	g.jcontrols["fire"]=joyaskbutton()
	speak("move to next inventory item")
	g.jcontrols["inv1"]=joyaskbutton()
	speak("move to previous inventory item")
	g.jcontrols["inv2"]=joyaskbutton()
	speak("Use the selected inventory item")
	g.jcontrols["invuse"]=joyaskbutton()
	speak("Drop the selected inventory item")
	g.jcontrols["invdrop"]=joyaskbutton()
	speak("Speak facing direction")
	g.jcontrols["facing"]=joyaskbutton()
	speak("Speak coordinates")
	g.jcontrols["coordinates"]=joyaskbutton()
	speak("Climb up")
	g.jcontrols["climbup"]=joyaskbutton()
	speak("Climb down")
	g.jcontrols["climbdown"]=joyaskbutton()
	speak("Open the game menu")
	g.jcontrols["gamemenu"]=joyaskbutton()
	g.writeprefs()
	speak("Configuration saved.")
	option()
def joyaskbutton():
	while True:
		joyavailcheck2()
		process_events()
		if key_pressed(K_ESCAPE) or g.stick.get_hat(0)==(-1,0): option()
		for event in g.lastevents:
			if event.type==pygame.JOYBUTTONDOWN: return event.button
def pr(namew,mailw):
	if 1:
		if 1:
			if 1:
				speak("Connecting.")
				g.n.setup_client(100, 100)
				g.n.connect(netaddress,netport)
				while(True):
					process_events()
					g.e=g.n.request()
					if (key_pressed(K_ESCAPE)):
		
						login_settings()
			
					if(g.e.type==event_connect): break

				g.n.send_reliable(0,"zero"*4,0)
				g.n.send_reliable(0, "pr "+namew+" "+mailw+" "+g.compid, 0)
				while True:
					process_events()
					if key_pressed(K_ESCAPE):
						speak("Aborting ...")
						login_settings()
					g.e=g.n.request()
					if g.e.type == event_receive:
						if string_contains(g.e.message, "errored", 1)>-1:
							dlg(string_replace(g.e.message, "errored ", "", False))
							login_settings()
						if g.e.message == "checkeml":
							dlg("Success! Your account password has been sent to your e-mail address.")
							login_settings()

class slider(wx.Frame):
	def __init__(self,title,default):
		wx.Frame.__init__(self,None,title=_(title))
		panel=wx.Panel(self)
		self.value=0
		self.slider=wx.Slider(panel)
		self.slider.SetValue(default)
		self.t=wx.Timer()
		self.t.Bind(wx.EVT_TIMER,self.loop)
		self.t.Start(1)
		btn = wx.Button(panel,label="OK")
		btn.Bind(wx.EVT_BUTTON,self.on_ok)
	def loop(self,event):
		pass
	def on_ok(self,event):
		self.value=self.slider.GetValue()
		g.screen.fill((0,0,0)); pygame.display.flip(); self.t.Destroy(); self.Destroy(); g.app.ExitMainLoop(); pygame.event.clear()
def prompt_slider(title,default=0):

	dlg=slider(title,default)
	pygame.display.set_caption(chr(65533))
	ctypes.windll.user32.SetParent(dlg.GetHandle(),pygame.display.get_wm_info()["window"])
	def on_key_down(event):
		if g.shouldsetcaption2: pygame.display.set_caption("Zero hour assault "+g.ver); g.shouldsetcaption2=False
		event.Skip()
	dlg.Bind(wx.EVT_CHAR_HOOK,on_key_down); g.shouldsetcaption2=True

	dlg.Show(); 	dlg.slider.SetFocus(); g.app.MainLoop()
	return dlg.value
FORMAT=pyaudio.paInt16
def testvoicechat():
	speak("Press escape to return.")
	pstream=g.pa.open(format=FORMAT, channels=1, rate=g.samplerate, input=True, frames_per_buffer=1024, input_device_index=g.inputdevice)
	pstream2=g.pa.open(format=FORMAT, channels=1, rate=g.samplerate, output=True, frames_per_buffer=1024, input_device_index=g.inputdevice)
	while 1:
		process_events()
		if g.inthegame: g.mainloop()
		if key_pressed(K_ESCAPE): break
		data=pstream.read(1024)
		data=amplify_audio_data(data, g.volumeg/100)
		pstream2.write(data)
	pstream.close()
	pstream2.close()
	option()
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

	audio_array = np.frombuffer(audio_data, dtype=np.int16)

	amplified_audio_array = audio_array.astype(np.float32) * amplification_factor

	amplified_audio_array = np.clip(amplified_audio_array, -32768, 32767)

	amplified_audio_data = amplified_audio_array.astype(np.int16)

	amplified_audio_bytes = amplified_audio_data.tobytes()

	return amplified_audio_bytes

def soundsmenu():
	setupmenu(False)
	m.click_sound=""
	m.enter_sound=""

	m.callback2=sounds_callback
	m.add_item_tts("The opposing team's beep sound.","beep.ogg",False)
	m.add_item_tts("Teammate's beep sound.","teambeacon.ogg",False)
	m.add_item_tts("Enemy Bot beep sound.","botbeacon.ogg",False)
	m.add_item_tts("General Chat message Tone","chat.ogg",False)
	m.add_item_tts("The Scope for your weapon to can hit a objects or players","scope.ogg",False)
	m.add_item_tts("You bought products from paid store successful","misc49.ogg",False)

	m.add_item_tts("Back to main menu","back")
	m.run("Use up and down arrows to select a sound then press enter to listen to it.",True)
	mainmenu()
def sounds_callback():
	if key_pressed(K_RETURN):
		g.p.play_stationary(m.get_item_name(m.position+1),False)
def voice_callback():
	if g.inthegame: g.mainloop()
	if key_pressed(K_RETURN):
		item=m.get_item_name(m.position+1)
		if item == "team":
			if g.voicechatteam==1: speak("disabled"); g.voicechatteam=0; m.items[m.position].text=m.items[m.position].text.replace("enable","disable")
			elif g.voicechatteam==0: g.voicechatteam=1; speak("enabled"); m.items[m.position].text=m.items[m.position].text.replace("disable","enable")
		if item == "map":
			if g.voicechatmap==1: g.voicechatmap=0; speak("disabled"); m.items[m.position].text=m.items[m.position].text.replace("enable","disable")
			elif g.voicechatmap==0: g.voicechatmap=1; speak("enabled"); m.items[m.position].text=m.items[m.position].text.replace("disable","enable")
		if item == "group":
			if g.voicechatgroup==1: g.voicechatgroup=0; speak("disabled"); m.items[m.position].text=m.items[m.position].text.replace("enable","disable")
			elif g.voicechatgroup==0: g.voicechatgroup=1; speak("enabled"); m.items[m.position].text=m.items[m.position].text.replace("disable","enable")

		if item == "friend":
			if g.voicechatfriend==1: g.voicechatfriend=0; speak("disabled"); m.items[m.position].text=m.items[m.position].text.replace("enable","disable")
			elif g.voicechatfriend==0: g.voicechatfriend=1; speak("enabled"); m.items[m.position].text=m.items[m.position].text.replace("disable","enable")
		g.writeprefs()
def strip_html_tags(text):
	clean = re.compile('<.*?>')
	return re.sub(clean, '', text)
def readmemenu():
	setupmenu(True)
	with open("readme.html", "r", encoding="utf-8") as f:
		readme_html = f.read()
	
	# HTML'i ayrıştır ve sadece görünen metni al
	soup = BeautifulSoup(readme_html, "html.parser")
	
	# <script> ve <style> gibi bölümleri kaldır
	for element in soup(["script", "style"]):
		element.decompose()
	
	visible_text = soup.get_text()
	lines = visible_text.splitlines()
	
	for line in lines:
		line = line.strip()
		if line:  # boş satırları atla
			m.add_item_tts(line, line, False)

	m.click_sound = ""
	m.enter_sound = ""

	m.add_item_tts("Back to main menu", "back")
	m.run("Use the up and down arrow keys to read the readme, escape to go back.", True)
	mainmenu()

def rulesmenu():
	setupmenu(True)
	f=open("rules.txt","r",encoding="utf-8")
	readme=f.read()
	f.close()
	lines=readme.split("\n")
	for line in lines: m.add_item_tts(line,line,False)
	m.click_sound=""
	m.enter_sound=""

	m.add_item_tts("Back to main menu","back")
	m.run("Use the up and down arrow keys to read the rules, escape to go back.",True)
	mainmenu()
def privacymenu():
	setupmenu(True)
	f=open("privacy.txt","r",encoding="utf-8")
	readme=f.read()
	f.close()
	lines=readme.split("\n")
	for line in lines: m.add_item_tts(line,line,False)
	m.click_sound=""
	m.enter_sound=""

	m.add_item_tts("Back to main menu","back")
	m.run("Use the up and down arrow keys to read the privacy, escape to go back.",True)
	mainmenu()

def who2menu():
	setupmenu(False)
	m.callback2=near_callback
	m.add_item_tts("Bots in same team: "+("enabled" if g.sameteambots else "disabled"),"sameteambots",False)
	m.add_item_tts("Bots in different team: "+("enabled" if g.differentteambots else "disabled"),"differentteambots",False)
	m.add_item_tts("players in same team: "+("enabled" if g.sameteamplayers else "disabled"),"sameteamplayers",False)
	m.add_item_tts("players in different team: "+("enabled" if g.differentteamplayers else "disabled"),"differentteamplayers",False)
	m.add_item_tts("players in same group: "+("enabled" if g.samegroupplayers else "disabled"),"samegroupplayers",False)
	m.add_item_tts("players in different group: "+("enabled" if g.differentgroupplayers else "disabled"),"differentgroupplayers",False)
	m.add_item_tts("Back to settings","back")
	mres=m.run("Please select an option.",True)
	choice=m.get_item_name(mres)
	if mres==0 or choice=="back": option()
	g.voicechatwho=choice
	g.writeprefs()
	option()
def near_callback():
	if g.inthegame: g.mainloop()
	if key_pressed(K_RETURN):
		item=m.get_item_name(m.position+1)
		if item == "sameteamplayers":
			if g.sameteamplayers==1: speak("disabled"); g.sameteamplayers=0; m.items[m.position].text=m.items[m.position].text.replace("enable","disable")
			elif g.sameteamplayers==0: g.sameteamplayers=1; speak("enabled"); m.items[m.position].text=m.items[m.position].text.replace("disable","enable")
		if item == "differentteamplayers":
			if g.differentteamplayers==1: speak("disabled"); g.differentteamplayers=0; m.items[m.position].text=m.items[m.position].text.replace("enable","disable")
			elif g.differentteamplayers==0: g.differentteamplayers=1; speak("enabled"); m.items[m.position].text=m.items[m.position].text.replace("disable","enable")
		if item == "sameteambots":
			if g.sameteambots==1: speak("disabled"); g.sameteambots=0; m.items[m.position].text=m.items[m.position].text.replace("enable","disable")
			elif g.sameteambots==0: g.sameteambots=1; speak("enabled"); m.items[m.position].text=m.items[m.position].text.replace("disable","enable")
		if item == "differentteambots":
			if g.differentteambots==1: speak("disabled"); g.differentteambots=0; m.items[m.position].text=m.items[m.position].text.replace("enable","disable")
			elif g.differentteambots==0: g.differentteambots=1; speak("enabled"); m.items[m.position].text=m.items[m.position].text.replace("disable","enable")
		if item == "differentgroupplayers":
			if g.differentgroupplayers==1: speak("disabled"); g.differentgroupplayers=0; m.items[m.position].text=m.items[m.position].text.replace("enable","disable")
			elif g.differentgroupplayers==0: g.differentgroupplayers=1; speak("enabled"); m.items[m.position].text=m.items[m.position].text.replace("disable","enable")
		if item == "samegroupplayers":
			if g.samegroupplayers==1: speak("disabled"); g.samegroupplayers=0; m.items[m.position].text=m.items[m.position].text.replace("enable","disable")
			elif g.samegroupplayers==0: g.samegroupplayers=1; speak("enabled"); m.items[m.position].text=m.items[m.position].text.replace("disable","enable")
def nearvoicemenu():
	setupmenu(False)
	m.callback2=near_callback2
	m.add_item_tts("Character voice: "+("enabled" if g.charvoice else "disabled"),"charvoice",False)
	m.add_item_tts("Sound: "+("enabled" if g.sound else "disabled"),"sound",False)
	m.add_item_tts("Back to settings","back")
	mres=m.run("Please select an option.",True)
	choice=m.get_item_name(mres)
	if mres==0 or choice=="back": option()
	g.voicechatwho=choice
	g.writeprefs()
	option()
def near_callback2():
	if g.inthegame: g.mainloop()
	if key_pressed(K_RETURN):
		item=m.get_item_name(m.position+1)
		if item == "charvoice":
			if g.charvoice==1: speak("disabled"); g.charvoice=0; m.items[m.position].text=m.items[m.position].text.replace("enable","disable")
			elif g.charvoice==0: g.charvoice=1; speak("enabled"); m.items[m.position].text=m.items[m.position].text.replace("disable","enable")
		if item == "sound":
			if g.sound==1: speak("disabled"); g.sound=0; m.items[m.position].text=m.items[m.position].text.replace("enable","disable")
			elif g.sound==0: g.sound=1; speak("enabled"); m.items[m.position].text=m.items[m.position].text.replace("disable","enable")

def restartmenu():
	setupmenu(False)
	m.add_item_tts("yes","yes")
	m.add_item_tts("no","no")
	if g.inthegame: m.callback2 = g.mainloop
	mres = m.run("You need to restart the game for the change to take effect, would you like to restart now?",True)
	choice = m.get_item_name(mres)
	if choice=="yes": restart()
	else: option()
def restart():
		g.writeprefs()
		subprocess.Popen(["zero_hour_assault.exe"])
		ctypes.windll.kernel32.ExitProcess(0)
