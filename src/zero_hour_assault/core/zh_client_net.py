import globals as g
import os
import time
import sys
import math

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
			elif parsed[0] == "deinput":
				# Data editor text input: deinput <field_key> <prompt text>
				field_key = parsed[1] if len(parsed) > 1 else "_unknown"
				prompt = " ".join(parsed[2:]) if len(parsed) > 2 else "Enter value"
				value = get_input(prompt)
				if value != "":
					g.n.send_reliable(0, "de_setval " + field_key + " " + value, 0)
				process_events()
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
				try:
					import os
					os.makedirs("lang", exist_ok=True)
					with open(filename,"w",encoding="utf-8") as f: f.write(content)
					file_encrypt(filename,g.langkey)
				except Exception as ex:
					pass
				g.lngdata=content
				g.transcache.clear()
				g.lang=parsed[1]
			elif parsed[0]=="updatelang":
				filename="lang/"+parsed[1]+".lng"
				content=g.e.message.replace(parsed[0]+" "+parsed[1]+" ","")
				try:
					import os
					os.makedirs("lang", exist_ok=True)
					with open(filename,"w",encoding="utf-8") as f: f.write(content)
					file_encrypt(filename,g.langkey)
				except Exception as ex:
					pass
				if g.lang==parsed[1]: g.lngdata=content
				g.transcache.clear()
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


def record_voice():
	while g.recording:
		time.sleep(0.010)
		try: audio_data = pstream.read(CHUNK_SIZE)
		except: continue
		audio_data=amplify_audio_data(audio_data, g.volumeg/100)
		audio_data = opus_encoder.encode(audio_data,CHUNK_SIZE)
		g.n.send_unreliable(0, audio_data, 5)


def record_voice2():
	while g.recording2:
		time.sleep(0.010)
		try: audio_data = pstream.read(CHUNK_SIZE)
		except: continue
		audio_data=amplify_audio_data(audio_data, g.volumeg/100)
		audio_data = opus_encoder.encode(audio_data,CHUNK_SIZE)
		g.n.send_unreliable(0, audio_data, 6)


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


def handle_voicechat_data2(p):

	while 1:
		time.sleep(0.010)
		playing=p.voice_sound2 is not None and p.voice_sound2.playing()
		if len(p.audio_buffer2)>=20 and not p.alplayed2:
			p.alplayed2=True
			play_audio2(p,p.audio_buffer2)
		elif p.alplayed2:
			if not playing and len(p.audio_buffer2)>=20: play_audio2(p,copy.copy(p.audio_buffer2))

