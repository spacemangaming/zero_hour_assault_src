import globals as g
import os
import time
import sys
import math
from typing import List, Dict

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
	if resetpool:
		peer = getattr(g.n, "peer", None) or getattr(g.n, "secure_peer", None)
		if peer is not None:
			g.n.disconnect_peer(peer)
	destroy_all_sources()
	g.recording=False
	try: g.n.send_reliable(0,"voiceoff",0)
	except: pass


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
			if vlc and pafy:
				g.media_player=vlc.MediaPlayer(pafy.new(g.video_urls[g.video_index-1]).getbestaudio().url)
				g.video_index-=1
				g.media_player.set_hwnd(0)
				g.media_player.play()
			else:
				speak("YouTube player not available (VLC not installed)")

		if shift_is_down() and key_pressed(K_F8):
			g.media_player.stop()
			g.media_player.release()
			if g.video_index==len(g.video_urls)-1: g.video_index=-1
			if vlc and pafy:
				g.media_player=vlc.MediaPlayer(pafy.new(g.video_urls[g.video_index+1]).getbestaudio().url)
				g.video_index+=1
				g.media_player.set_hwnd(0)
				g.media_player.play()
			else:
				speak("YouTube player not available (VLC not installed)")


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
					if vlc and pafy:
						g.media_player=vlc.MediaPlayer(pafy.new(m.get_item_name(mres)).getbestaudio().url)
						g.video_index=0
						g.media_player.play()
					else:
						speak("YouTube player not available (VLC not installed)")
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
	
		if (
			getattr(g.doors[i], "map", g.mapname) == g.mapname
			and round(g.me.x) == g.doors[i].dx
			and round(g.me.y) == g.doors[i].dy
			and round(g.me.z) == g.doors[i].dz
			and g.dmoving == False
		):
		
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


def is_cheater():
	if ctypes.windll.kernel32.IsDebuggerPresent(): return True
	return is_memory_scan_detected() or is_speed_hack_detected()


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

