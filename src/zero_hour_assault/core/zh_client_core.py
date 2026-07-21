import globals as g
import os
import time
import sys
import math
import traceback
import ctypes
import pygame
import pickle
import opuslib
import constants
import sound
import menu

# Visual minimap HUD (sighted players) — safe to import; no-ops if screen absent
try:
    from ui.visual_hud import hud as _visual_hud
except Exception:
    _visual_hud = None

def handle_exception(exc_type, exc_value, exc_traceback):
	if not compiled:
		with open("errors.log","a") as f: 		traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)


	ctypes.windll.user32.MessageBoxW(None,"A critical error has occurred that prevented the program from continue executing. Please send the error information you will see after pressing enter to the developers to Identify the cause of the error and fix it.","Error!",16)


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
	_appdata = os.getenv("appdata") or os.getenv("HOME") or ""
	if _appdata and not file_exists(_appdata+"/alsoft.ini"):
		try:
			f=open(_appdata+"/alsoft.ini","w")
			f.write("""[General]
sources=100000
slots=100000

[decoder]
hq-mode=true""")
			f.close()
		except Exception: pass
	if 1:
		langs=os.listdir("lang")
		for lang in langs:
			if file_get_contents("lang/"+lang,"r","utf-8")!="": file_encrypt("lang/"+lang,g.langkey)
	if compiled and check_if_already_running():
		dlg("You cannot open the game twice")
		pygame.quit()
		if sys.platform == "win32":
			ctypes.windll.kernel32.ExitProcess(0)
		else:
			sys.exit(0)
	set_sound_decryption_key("asdasdasdasasdasdsa1231232132112321321$$1231231231221321312%*]9CfY%!yfo?3.m]C16(VW:?DB:70v4n7d`tht}jiylhC%L&;ix(Y;9BB?`k-hYhR^=n%C;#kykxV?)GFbzC5x6R<-W?o<c|xQw")

	if (getattr(sys, "frozen", False) or os.environ.get("FORCE_UPDATE_CHECK") == "1") and sys.platform == "win32":
		try:
			updater.check()
			updater.sndcheck()
		except Exception:
			pass
	g.distpool.behind_pitch_decrease=5
	g.distpool.max_distance=2000
	g.p.behind_pitch_decrease=-5
	g.weapons.append("punch")
	g.weapons2.append("feet")
	if (not directory_exists(DIRECTORY_APPDATA+"/nbm-studios")):
		directory_create(DIRECTORY_APPDATA+"/nbm-studios")
	if(not directory_exists(DIRECTORY_APPDATA+"/nbm-studios/zero_hour_assault")):
		directory_create(DIRECTORY_APPDATA+"/nbm-studios/zero_hour_assault")
	_settings_is_new = not file_exists(g.sd.fn)
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


	if sys.platform == "win32":
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

	# ── First-run visual mode prompt ──────────────────────────────────────────
	if _settings_is_new and not g.sd.exists("visual_mode"):
		_ask_visual_mode()

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
		if sys.platform == "android" or "ANDROID_ARGUMENT" in os.environ or "ANDROID_BOOTSTRAP" in os.environ:
			g.n.send_reliable(0, "android", 0)
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


def _ask_visual_mode():
	"""First-run dialog asking whether to enable visual mode.

	Rendered on-screen with pygame so sighted players who cannot hear
	the TTS can still make a choice.  Audio players will also hear the
	question spoken aloud.
	"""
	speak("Welcome! Do you want to play in Visual Mode? Visual mode turns off text-to-speech and always shows the minimap on screen. Press Y for yes, N for no.")
	if g.screen:
		try:
			g.screen.fill((10, 20, 40))
			font_big  = pygame.font.SysFont("segoeui", 36, bold=True)
			font_med  = pygame.font.SysFont("segoeui", 22)
			font_sm   = pygame.font.SysFont("segoeui", 16)
			sw, sh = g.screen.get_size()
			lines = [
				font_big.render("Visual Mode", True, (230, 237, 243)),
				font_med.render("Do you want to play in Visual Mode?", True, (200, 210, 220)),
				font_med.render("", True, (0,0,0)),
				font_med.render("Visual Mode turns off text-to-speech announcements", True, (180, 190, 200)),
				font_med.render("and always shows the minimap on screen.", True, (180, 190, 200)),
				font_med.render("", True, (0,0,0)),
				font_sm.render("Recommended for sighted players.", True, (139, 148, 158)),
				font_sm.render("Blind players should press N.", True, (139, 148, 158)),
				font_big.render("", True, (0,0,0)),
				font_big.render("Y  =  Yes, enable Visual Mode", True, (79, 195, 247)),
				font_big.render("N  =  No, keep audio mode", True, (251, 146, 60)),
			]
			total_h = sum(s.get_height() + 6 for s in lines)
			y = (sh - total_h) // 2
			for surf in lines:
				g.screen.blit(surf, ((sw - surf.get_width()) // 2, y))
				y += surf.get_height() + 6
			pygame.display.flip()
		except Exception:
			pass

	# Wait for Y or N
	while True:
		process_events()
		if key_pressed(K_y):
			g.visual_mode = 1
			speak("Visual mode enabled.")
			if g.screen:
				try:
					g.screen.fill((10, 20, 40))
					f = pygame.font.SysFont("segoeui", 28, bold=True)
					s = f.render("Visual Mode enabled!", True, (79, 195, 247))
					sw, sh = g.screen.get_size()
					g.screen.blit(s, ((sw - s.get_width()) // 2, (sh - s.get_height()) // 2))
					pygame.display.flip()
				except Exception:
					pass
			g.delay(1200)
			break
		if key_pressed(K_n):
			g.visual_mode = 0
			speak("Audio mode kept. Enjoy the game!")
			g.delay(800)
			break


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

	if(g.sd.exists("visual_mode")):
		g.visual_mode=g.sd.readn("visual_mode")


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
	g.sd.add("visual_mode",g.visual_mode)

	g.sd.save()


def check_if_already_running():
	current_pid = os.getpid()
	current_process = psutil.Process(current_pid)
	process_name = current_process.name()
	for proc in psutil.process_iter(['pid', 'name']):
		if proc.info['name'] == process_name and proc.info['pid'] != current_pid:
			return True
	return False


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

	# ── Visual minimap HUD ────────────────────────────────────────────────────
	# Visual mode: always on. Audio mode: Alt+M to toggle.
	if _visual_hud is not None and g.screen is not None and g.inthegame:
		try:
			if g.visual_mode:
				_visual_hud.visible = True
			else:
				from zh_client_gameplay import alt_is_down
				if key_pressed(K_m) and alt_is_down():
					_visual_hud.toggle()
			_visual_hud.draw(g.screen, g)
			if _visual_hud.visible:
				pygame.display.flip()
		except Exception:
			pass


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
		if(key_pressed(K_RETURN) or key_pressed(pygame.K_KP_ENTER) or (g.stick is not None and g.stick.get_hat(0)==(1,0))):
			waitjoyhat()
			speak("disconnecting")
			peer = getattr(g.n, "peer", None) or getattr(g.n, "secure_peer", None)
			if peer is not None:
				try: g.n.disconnect_peer(peer)
				except: pass
			try: g.n.destroy()
			except: pass
			g.connected = False
			g.x = True
			g.xtimer.restart()
			return