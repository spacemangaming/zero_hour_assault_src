import globals as g
import os
import time
import sys
import math

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


def delinear(a): return string_split(a,"\n",True)


def is_sound_number(t):
	t=string_replace(t, ".", "", True)
	t=string_replace(t, "-", "", True)
	if(string_is_digits(t)):
		return True
	return False


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


def getmotd():
	g.motdhash=file_get_contents(g.appdata_dir+"/motdhash.dat")
	motd=url_get("https://nbmstudios.com/zero_hour_assault/web_message.txt")
	if string_hash(motd, 2, False) != g.motdhash:
		g.motdhash=string_hash(motd, 2, False)
		g.p.play_stationary("motd.ogg", False)
		dlg(""+motd+"")
		writeprefs()
		file_put_contents(""+g.appdata_dir+"/motdhash.dat", g.motdhash, "w")


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


def get_installed_jaws_versions():
	_appdata = os.getenv("APPDATA")
	if not _appdata:
		return []
	jaws_path = os.path.join(_appdata, "Freedom Scientific", "JAWS")
	try:
		return [folder for folder in os.listdir(jaws_path) if os.path.isdir(os.path.join(jaws_path, folder))]
	except OSError:
		return []


def get_user_languages(jaws_version):
	_appdata = os.getenv("APPDATA")
	if not _appdata:
		return []
	settings_path = os.path.join(_appdata, "Freedom Scientific", "JAWS", jaws_version, "Settings")
	try:
		return [folder for folder in os.listdir(settings_path) if folder not in ["VoiceProfiles", "Notifications"]]
	except OSError:
		return []


def install_language(language, jaws_version):
	_appdata = os.getenv("APPDATA")
	if not _appdata:
		return
	source_file = "zero_hour_assault.jkm"
	target_path = os.path.join(_appdata, "Freedom Scientific", "JAWS", jaws_version, "Settings", language)

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


def get_rain_sound():
	if g.get_ignore_ambience_at(round(g.me.x),round(g.me.y),round(g.me.z)): return "rainhome.ogg"
	if g.mapname=="lobby" or "basement" in g.mapname or "match" in g.mapname: return "rainhome.ogg"
	if "flag" in g.mapname or "massacre" in g.mapname or "main" in g.mapname or "zombie" in g.mapname: return "rainext.ogg"
	return "rainhome.ogg"


def get_rain_sound_camera():
	if g.get_ignore_ambience_at(round(g.camera.x),round(g.camera.y),round(g.camera.z)): return "rainhome.ogg"
	if g.mapname=="lobby" or "basement" in g.mapname or "match" in g.mapname: return "rainhome.ogg"
	if "massacre" in g.mapname or "main" in g.mapname or "zombie" in g.mapname: return "rainext.ogg"
	return "rainhome.ogg"


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


def get_firetime():
	if g.weaponauto: return 15
	return 10


def get_firetime2():
	if g.weaponauto2: return 15
	return 10

