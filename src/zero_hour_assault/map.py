from variable_management import string_to_number
from timer import timer
from speech import speak
from source import spawn_source, create_amb
from sign import spawn_sign
from rotation import north, east, south, west, move
from random import randint as random
from variable_management import string_contains
from constants import *
from door import spawn_door
from variable_management import string_left
from variable_management import string_split
from variable_management import string_replace

from source import destroy_all_sources
from door import destroy_all_doors
import globals as g
from rotation import calculate_theta
from variable_management import randomstr
from events import key_down
import pygame
from sound_pool import SoundPool
from sound import sound
def clear_map():
	g.map.clear()
	g.mapstairs.clear()
	g.reverbs.clear()
	g.echos.clear()
	g.eaxreverbs.clear()
	g.mapmusic.close()
	g.mapzones.clear()
	g.mapignore_ambiences.clear()

def spawn_platform(minx, maxx, miny, maxy, minz, maxz, plattype):
	g.map.append((round(minx), round(maxx), round(miny), round(maxy), round(minz), round(maxz), plattype))

def spawn_staircase(minx, maxx, miny, maxy, minz, maxz, plattype, type, reverse):
	g.map.append((round(minx), round(maxx), round(miny), round(maxy), round(minz), round(maxz), plattype))
	g.mapstairs.append(""+str(minx)+":"+str(maxx)+":"+str(miny)+":"+str(maxy)+":"+str(minz)+":"+str(maxz)+":"+plattype+":"+type+":"+reverse)


def spawn_zone( minx, maxx, miny, maxy, minz, maxz, text, trackable=False):
	if not trackable: g.mapzones.append(""+str(minx)+":"+str(maxx)+":"+str(miny)+":"+str(maxy)+":"+str(minz)+":"+str(maxz)+":"+text)
	if trackable: g.mapzones.append(""+str(minx)+":"+str(maxx)+":"+str(miny)+":"+str(maxy)+":"+str(minz)+":"+str(maxz)+":"+text+":trackable")

def get_zone_at(x, y, z):
	ret="Unknown area"
	x=round(x)
	y=round(y)
	z=round(z)
	for i in range(len(g.mapzones)):

		sd=string_split(g.mapzones[i], ":", True)
		minx=string_to_number(sd[0])
		maxx=string_to_number(sd[1])
		miny=string_to_number(sd[2])
		maxy=string_to_number(sd[3])
		minz=string_to_number(sd[4])
		maxz=string_to_number(sd[5])
		text=sd[6]
		if(minx<=x and maxx>=x and miny<=y and maxy>=y and minz<=z and maxz>=z):
			ret=text

	return ret

def spawn_ignore_ambience( minx, maxx, miny, maxy, minz, maxz):
	g.mapignore_ambiences.append(""+str(minx)+":"+str(maxx)+":"+str(miny)+":"+str(maxy)+":"+str(minz)+":"+str(maxz))

def get_ignore_ambience_at(x, y, z):
	ret=False
	x=round(x)
	y=round(y)
	z=round(z)
	for i in range(len(g.mapignore_ambiences)):

		sd=string_split(g.mapignore_ambiences[i], ":", True)
		minx=string_to_number(sd[0])
		maxx=string_to_number(sd[1])
		miny=string_to_number(sd[2])
		maxy=string_to_number(sd[3])
		minz=string_to_number(sd[4])
		maxz=string_to_number(sd[5])
		if(minx<=x and maxx>=x and miny<=y and maxy>=y and minz<=z and maxz>=z):
			ret=True

	return ret

g.get_ignore_ambience_at=get_ignore_ambience_at
def get_tile_at(x, y, z):
	mt=""
	x=round(x)
	y=round(y)
	z=round(z)

	# Check cache first
	if not g.rain and (x, y, z) in g.tile_cache:
		return g.tile_cache[(x, y, z)]

	for i in range(len(g.map)):
		sd=g.map[i]
		minx=string_to_number(sd[0])
		maxx=string_to_number(sd[1])
		miny=string_to_number(sd[2])
		maxy=string_to_number(sd[3])
		minz=string_to_number(sd[4])
		maxz=string_to_number(sd[5])
		tile=sd[6]
		if(minx<=x and maxx>=x and miny<=y and maxy>=y and minz<=z and maxz>=z):
			mt=tile
			g.tile_cache[(x, y, z)] = mt


	if (g.rain or g.rainfinish) and (g.get_rain_sound_camera()=="rainext.ogg") and "wall" not in mt and mt!="" and mt!="air" and mt in g.nomudtiles: mt="mud"
    #No need to cache mud, because rain is dynamic
	return mt
def get_staircase_at(x, y, z):
	mt=""
	x=round(x)
	y=round(y)
	z=round(z)
	for i in range(len(g.mapstairs)):

		sd=string_split(g.mapstairs[i], ":", True)
		minx=string_to_number(sd[0])
		maxx=string_to_number(sd[1])
		miny=string_to_number(sd[2])
		maxy=string_to_number(sd[3])
		minz=string_to_number(sd[4])
		maxz=string_to_number(sd[5])
		staircase=sd[7]
		if(minx<=x and maxx>=x and miny<=y and maxy>=y and minz<=z and maxz>=z):

			mt=staircase


	return mt


def linear(a):
	final=""
	for i in range(len(a)):

		final+=(a[i]+"\n")

	return final

def delinear(a):
	return string_split(a, "\n", False)

def load_map(mdata):
	#g.mapready=True
	g.jumping=False
	g.tile_cache={}
	g.p.destroy_all
	if mdata.find("mapname:"+g.mapname)==-1: g.mapmusic.close()

	destroy_all_doors()
	g.signs=[]
	destroy_all_sources()
	g.map.clear()
	g.mapstairs.clear()
	g.mapzones.clear()
	g.mapignore_ambiences.clear()

	clear_map()
	ldata=delinear(mdata)
	for i in range(len(ldata)):
		try: # Add try-except block here
			parsed=string_split(ldata[i], ":", True)
			if(parsed[0]=="mapname"):

				g.mapname=string_replace(ldata[i], "mapname:", "", False)

			elif(parsed[0]=="door" and len(parsed)>12):

				x=string_to_number(parsed[1])
				mx=string_to_number(parsed[2])
				y=string_to_number(parsed[3])
				my=string_to_number(parsed[4])
				z=string_to_number(parsed[5])
				mz=string_to_number(parsed[6])
				fx=string_to_number(parsed[7])
				fy=string_to_number(parsed[8])
				fz=string_to_number(parsed[9])
				speed=string_to_number(parsed[10])
				snd3=parsed[11]
				snd4=parsed[12]
				spawn_door(x, mx, y, my, z, mz, fx, fy,fz,speed,snd3,snd4,ldata[i-1].startswith("door:"))

			elif parsed[0] == "sign":
				spawn_sign(string_to_number(parsed[1]), string_to_number(parsed[2]), string_to_number(parsed[3]), parsed[4])

			elif(parsed[0]=="door" and len(parsed)>9):

				x=string_to_number(parsed[1])
				mx=x
				y=string_to_number(parsed[2])
				my=y
				z=string_to_number(parsed[3])
				mz=z
				fx=string_to_number(parsed[4])
				fy=string_to_number(parsed[5])
				fz=string_to_number(parsed[6])
				speed=string_to_number(parsed[7])
				snd3=parsed[8]
				snd4=parsed[9]
				spawn_door(x, mx, y, my, z, mz, fx, fy,fz,speed,snd3,snd4,ldata[i-1].startswith("door:"))


			elif parsed[0] == "music" and len(parsed)>1:
				if g.musicplayinthemap==1 and  g.mapmusic.player is None:
					volumeformap=string_to_number(g.mapmusicoldversion)
					g.mapmusic.load(parsed[1])
					g.mapmusic.volume=volumeformap
					g.writeprefs()
					g.mapmusic.play_looped()
			elif parsed[0]=="echo":
				r = mapecho()
				r.minx = string_to_number(parsed[1])
				r.maxx = string_to_number(parsed[2])
				r.miny = string_to_number(parsed[3])
				r.maxy = string_to_number(parsed[4])
				r.minz = string_to_number(parsed[5])
				r.maxz = string_to_number(parsed[6])
				r._delay=float(parsed[7])
				r._LRdelay=float(parsed[8])
				r._damping=float(parsed[9])
				r._feedback=float(parsed[10])
				r._spread=float(parsed[11])
				g.echos.append(r)
			elif parsed[0]=="reverb":
				r = mapreverb()
				r.minx = string_to_number(parsed[1])
				r.maxx = string_to_number(parsed[2])
				r.miny = string_to_number(parsed[3])
				r.maxy = string_to_number(parsed[4])
				r.minz = string_to_number(parsed[5])
				r.maxz = string_to_number(parsed[6])
				r._density = float(parsed[7])
				r._diffusion = float(parsed[8])
				r._gain=float(parsed[9])
				r._gainhf=float(parsed[10])
				r._decay_time = float(parsed[11])
				r._hfratio=float(parsed[12])
				r._reflections_gain = float(parsed[13])
				r._reflections_delay =float(parsed[14])
				r._late_reverb_gain =float(parsed[15])
				r._late_reverb_delay =float(parsed[16])
				r._air_absorption_gainhf =float(parsed[17])
				r._room_rolloff_factor =float(parsed[18])
				g.reverbs.append(r)
			elif parsed[0]=="eaxreverb":
				r = mapeaxreverb()
				r.minx = string_to_number(parsed[1])
				r.maxx = string_to_number(parsed[2])
				r.miny = string_to_number(parsed[3])
				r.maxy = string_to_number(parsed[4])
				r.minz = string_to_number(parsed[5])
				r.maxz = string_to_number(parsed[6])
				r._density = float(parsed[7])
				r._diffusion = float(parsed[8])
				r._gain=float(parsed[9])
				r._gainhf=float(parsed[10])
				r._gainlf=float(parsed[11])
				r._decay_time = float(parsed[12])
				r._decay_hfratio=float(parsed[13])
				r._decay_lfratio = float(parsed[14])
				r._reflections_gain = float(parsed[15])
				r._reflections_delay =float(parsed[16])
				r._reflections_pan =float(parsed[17])
				r._late_reverb_gain =float(parsed[18])
				r._late_reverb_delay =float(parsed[19])
				r._late_reverb_pan=float(parsed[20])
				r._echo_time=float(parsed[21])
				r._echo_depth=float(parsed[22])
				r._modulation_time=float(parsed[23])
				r._modulation_depth=float(parsed[24])
				r._air_absorption_gainhf =float(parsed[25])
				r._hfreference=float(parsed[26])
				r._lfreference=float(parsed[27])
				r._room_rolloff_factor =float(parsed[28])
				g.eaxreverbs.append(r)

			elif(parsed[0]=="platform" or parsed[0]=="staircase"):

				if(len(parsed)>=8):
					if parsed[0]!="staircase": spawn_platform(string_to_number(parsed[1]),string_to_number(parsed[2]),string_to_number(parsed[3]),string_to_number(parsed[4]),string_to_number(parsed[5]),string_to_number(parsed[6]),parsed[7])
					if parsed[0]=="staircase":
						try: spawn_staircase(string_to_number(parsed[1]),string_to_number(parsed[2]),string_to_number(parsed[3]),string_to_number(parsed[4]),string_to_number(parsed[5]),string_to_number(parsed[6]),parsed[7],parsed[8],parsed[9])
						except: spawn_staircase(string_to_number(parsed[1]),string_to_number(parsed[2]),string_to_number(parsed[3]),string_to_number(parsed[4]),string_to_number(parsed[5]),string_to_number(parsed[6]),parsed[7],parsed[8],"0")

				elif(len(parsed)==7):
					spawn_platform(string_to_number(parsed[1]),string_to_number(parsed[2]),string_to_number(parsed[3]),string_to_number(parsed[4]),string_to_number(parsed[5]),string_to_number(parsed[5]),parsed[6])

			elif(parsed[0]=="zone"):

				s=""
				for i in range(7, len(parsed)):

					s+=parsed[i]+" "

				if "trackable" in s:
					spawn_zone(string_to_number(parsed[1]),string_to_number(parsed[2]),string_to_number(parsed[3]),string_to_number(parsed[4]),string_to_number(parsed[5]),string_to_number(parsed[6]),s.replace("trackable",""),True)
				else: spawn_zone(string_to_number(parsed[1]),string_to_number(parsed[2]),string_to_number(parsed[3]),string_to_number(parsed[4]),string_to_number(parsed[5]),string_to_number(parsed[6]),s,False)

			elif(parsed[0]=="ignore_amb"):

				spawn_ignore_ambience(string_to_number(parsed[1]),string_to_number(parsed[2]),string_to_number(parsed[3]),string_to_number(parsed[4]),string_to_number(parsed[5]),string_to_number(parsed[6]))

			elif(parsed[0]=="maxx"):

				g.max.x=string_to_number(parsed[1])

			elif(parsed[0]=="maxy"):

				g.max.y=string_to_number(parsed[1])

			elif(parsed[0]=="maxz"):

				g.max.z=string_to_number(parsed[1])

			elif(parsed[0]=="x"):

				g.me.x=string_to_number(parsed[1])

			elif(parsed[0]=="y"):

				g.me.y=string_to_number(parsed[1])

			elif(parsed[0]=="z"):

				g.me.z=string_to_number(parsed[1])

			elif parsed[0] == "amb" and len(parsed)>8:
				create_amb(string_to_number(parsed[1]), string_to_number(parsed[2]), string_to_number(parsed[3]), string_to_number(parsed[4]), string_to_number(parsed[5]), string_to_number(parsed[6]), parsed[7], string_to_number(parsed[8]))

			elif(parsed[0]=="src" and len(parsed)==9):

				lx=string_to_number(parsed[1])
				rx=string_to_number(parsed[2])
				miny=string_to_number(parsed[3])
				maxy=string_to_number(parsed[4])
				minz=string_to_number(parsed[5])
				maxz=string_to_number(parsed[6])
				spawn_source(lx, rx, miny, maxy, minz, maxz, parsed[7], False, -1, string_to_number(parsed[8]))


			elif(parsed[0]=="src" and len(parsed)==8):

				lx=string_to_number(parsed[1])
				rx=string_to_number(parsed[2])
				miny=string_to_number(parsed[3])
				maxy=string_to_number(parsed[4])
				minz=string_to_number(parsed[5])
				maxz=string_to_number(parsed[6])
				snd=sound()
				snd.load(parsed[7]); snd.close()

				spawn_source(lx, rx, miny, maxy, minz, maxz, parsed[7], False, -1, 0)
		except Exception as e: # Catch general exceptions during parsing
			print(f"Error parsing line {i+1}: {ldata[i]}. Skipping line. Error: {e}") # Print error message for debugging
			pass # Skip the current line and continue to the next

def playstep():
	if g.jumping: return
	if(get_tile_at(g.mr.x, g.mr.y, g.me.z)!=""):
		if g.zombie:
			try: g.p.play_stationary(get_tile_at(g.mr.x, g.mr.y, g.me.z)+"step"+str(random(1, 5))+".ogg", False).handle.pitch=70
			except: pass
		else: g.p.play_stationary(get_tile_at(g.mr.x, g.mr.y, g.me.z)+"step"+str(random(1, 5))+".ogg", False)
sitannouncetimer=timer()
def move_player(dir):
	if g.inbike or g.holding_wall: return
	if g.sitting:
		if sitannouncetimer.elapsed>1000:
			sitannouncetimer.restart()
			speak("You are sitting. Press alt z or shift z to stand up.")
		return
	if "helicopter" in g.mapname: return
	#if alt_is_down(): return
	if g.inve:
		if dir==Forward: g.n.send_reliable(0,"vup",0)
		elif dir==Backward: g.n.send_reliable(0,"vdown",0)
		return
	#if get_tile_at(g.me.x,g.me.y,(g.me.z if not g.jumping else g.jumplandz)).startswith("wall"): return

	if g.dmoving: return
	if len(g.p1)>0: return

	g.lastdir=dir
	g.stopwalktimer.restart()
	if not g.jumping:
		g.tile_count+=1
		#if g.tile_count>25: g.n.send_reliable(0,"cheat "+g.name,0); g.tile_count=0
	if dir == Up and get_staircase_at(g.me.x, g.me.y, (g.me.z if not g.jumping else g.jumplandz))=="":
		if get_tile_at(g.mr.x, g.mr.y, g.me.z+1) != "":
			g.me.z += 1
			checkup()
	if dir == Down and get_staircase_at(g.me.x, g.me.y, (g.me.z if not g.jumping else g.jumplandz))=="":
		if get_tile_at(g.mr.x, g.mr.y, g.me.z-1) != "" and string_left(get_tile_at(g.mr.x, g.mr.y, g.me.z-1), 4) != "wall":
			g.me.z -= 1
			checkdown()
	if dir == Forward:
		ox=g.me.x
		oy=g.me.y
		g.me=move(g.me.x, g.me.y, g.me.z, g.facing, north)
		if round(g.me.x)<=-1 or round(g.me.x)>=g.max.x+1 or round(g.me.y)<=-1 or round(g.me.y)>=g.max.y+1:
			g.me.x=ox
			g.me.y=oy
			return
		checkaround(ox, oy)
	if dir == Backward:
		ox=g.me.x
		oy=g.me.y
		g.me=move(g.me.x, g.me.y, g.me.z, g.facing, south)
		if round(g.me.x)<=-1 or round(g.me.x)>=g.max.x+1 or round(g.me.y)<=-1 or round(g.me.y)>=g.max.y+1:
			g.me.x=ox
			g.me.y=oy
			return
		checkaround(ox, oy)
	if dir == Left:
		ox=g.me.x
		oy=g.me.y
		g.me=move(g.me.x, g.me.y, g.me.z, g.facing, west)
		if round(g.me.x)<=-1 or round(g.me.x)>=g.max.x+1 or round(g.me.y)<=-1 or round(g.me.y)>=g.max.y+1:
			g.me.x=ox
			g.me.y=oy
			return
		checkaround(ox, oy)
	if dir == Right:
		ox=g.me.x
		oy=g.me.y
		g.me=move(g.me.x, g.me.y, g.me.z, g.facing, east)
		if round(g.me.x)<=-1 or round(g.me.x)>=g.max.x+1 or round(g.me.y)<=-1 or round(g.me.y)>=g.max.y+1:
			g.me.x=ox
			g.me.y=oy
			return
		checkaround(ox, oy)
def checkaround(ox, oy):
	g.mr.x=g.me.x
	g.mr.y=g.me.y
	if 1:
		stairs=get_staircase_at(g.me.x, g.me.y, (g.me.z if not g.jumping else g.jumplandz))
		if stairs=="x":
			reverse=is_staircase_reverse(g.me.x, g.me.y, (g.me.z if not g.jumping else g.jumplandz))

			if g.me.x>ox and get_staircase_at((g.me.x-1 if not reverse else g.me.x-1), g.me.y, (g.me.z if not g.jumping else g.jumplandz))!="":
				if not reverse: g.me.z+=1
				elif reverse: g.me.z-=1
				if not reverse: g.jumplandz+=1
				elif reverse: g.jumplandz-=1
			elif g.me.x<ox and get_staircase_at(g.me.x+1, g.me.y, (g.me.z if not g.jumping else g.jumplandz))!="":
				if not reverse: g.me.z-=1
				elif reverse: g.me.z+=1
				if not reverse: g.jumplandz-=1
				elif reverse: g.jumplandz+=1

		if stairs=="y" :
			reverse=is_staircase_reverse(g.me.x, g.me.y, (g.me.z if not g.jumping else g.jumplandz))

			if g.me.y>oy and get_staircase_at(g.me.x, (g.me.y-1 if not reverse else g.me.y-1), (g.me.z if not g.jumping else g.jumplandz))!="":
				if not reverse: g.me.z+=1
				elif reverse: g.me.z-=1
				if not reverse: g.jumplandz+=1
				elif reverse: g.jumplandz-=1

			elif g.me.y<oy and get_staircase_at(g.me.x, (g.me.y+1 if not reverse else g.me.y-1), (g.me.z if not g.jumping else g.jumplandz))!="":
				if not reverse: g.me.z-=1
				elif reverse: g.me.z+=1
				if g.jumping and not reverse: g.jumplandz-=1
				elif g.jumping and reverse: g.jumplandz+=1



		#oz=g.me.z
		#if get_tile_at(g.me.x, g.me.y, g.me.z)=="": g.me.z=oz
#		if g.me.z<0 and get_tile_at(g.me.x, g.me.y, g.me.z)=="": g.me.z=0
		#if not g.jumping and (stairs!="" or (get_tile_at(g.me.x, g.me.y, g.me.z)=="" and get_tile_at(g.me.x, g.me.y, g.me.z-1))!=""):
			#if get_tile_at(g.me.x, g.me.y, g.me.z)=="":
				#if get_tile_at(g.me.x, g.me.y, g.me.z-1)!="": g.me.z-=1
		if not g.jumping and (stairs!="" or (get_tile_at(g.me.x, g.me.y, g.me.z)=="" and get_tile_at(g.me.x, g.me.y, g.me.z+1))!=""):
			if get_tile_at(g.me.x, g.me.y, g.me.z)=="":
				if get_tile_at(g.me.x, g.me.y, g.me.z+1)!="" and "wall" not in get_tile_at(g.me.x, g.me.y, g.me.z+1): g.me.z+=1

		if not g.jumping and get_tile_at(g.me.x,g.me.y,g.me.z)!="" and stairs!="": g.p.play_stationary("stairsmove"+str(random(1,5))+".ogg",False)
		if g.me.z!=0 and get_tile_at(g.me.x, g.me.y, g.me.z).startswith("wall"):
			tile1=get_tile_at(g.me.x,g.me.y,g.me.z+1)
			tile2=get_tile_at(g.me.x,g.me.y,g.me.z+2)
			if tile1!="" and not tile1.startswith("wall"): g.me.z+=1
			if tile2!="" and not tile2.startswith("wall"): g.me.z+=2
	if get_tile_at(g.me.x, g.me.y,g.me.z)=="" and get_tile_at(ox, oy, (g.me.z if not g.jumping else g.jumplandz)).startswith("wall"):
		if 1:
			g.me.x=ox
			g.me.y=oy

			playstep()
			g.n.send_reliable(0, "move_to "+str(g.me.x)+" "+str(g.me.y)+" "+str(g.me.z), 0)

	if string_contains(get_tile_at(g.mr.x, g.mr.y, g.me.z), "wall", 1)>-1:
		if 1:
			#g.p.play_stationary("wall"+string_replace(get_tile_at(g.mr.x, g.mr.y, g.me.z), "wall", "", True)+".ogg", False)
			if g.wallhittimer.elapsed>=500:
				g.wallhittimer.restart()
				g.n.send_reliable(0,"xplay wall"+string_replace(get_tile_at(g.mr.x, g.mr.y, g.me.z), "wall", "", True)+"",0)
				g.p.play_3d("wall"+string_replace(get_tile_at(g.mr.x, g.mr.y, g.me.z), "wall", "", True)+".ogg", ox, oy, g.me.z, g.me.x, g.me.y, g.me.z, calculate_theta(g.facing), False)
			g.me.x=ox
			g.me.y=oy

			playstep()
			#g.n.send_reliable(0, "move_to "+str(g.me.x)+" "+str(g.me.y)+" "+str(g.me.z), 0)
			return
	else:
		playstep()
		g.n.send_reliable(0, "move_to "+str(g.mr.x)+" "+str(g.mr.y)+" "+str(g.me.z), 0)
		if not g.reloading and not g.parachute and not g.ducking and (g.fastwalk==1 or alt_is_down()) and g.walktime>g.maxwalktime and not g.reloading: g.walktime-=10
def checkup():
	if string_contains(get_tile_at(g.mr.x, g.mr.y, g.me.z), "wall", 1)>-1:
		g.p.play_3d("wall"+string_replace(get_tile_at(g.mr.x, g.mr.y, g.me.z), "wall", "", True)+".ogg", ox, oy, g.me.z, g.me.x, g.me.y, g.me.z, calculate_theta(g.facing), False)
		g.n.send_reliable(0,"xplay wall"+string_replace(get_tile_at(g.mr.x, g.mr.y, g.me.z), "wall", "", True)+"",0)
#		g.p.play_3d("wall"+string_replace(get_tile_at(g.mr.x, g.mr.y, g.me.z), "wall", "", True)+".ogg", g.me.x, g.me.y, g.me.z, g.me.x, g.me.y, g.me.z, calculate_theta(g.facing), False)

		g.n.send_reliable(0, "hitwall "+str(g.me.x)+" "+str(g.me.y)+" "+str(g.me.z), 0)
		bounceback(Up)
	else:
		playstep()
		g.n.send_reliable(0, "move_to "+str(g.mr.x)+" "+str(g.mr.y)+" "+str(g.me.z), 0)
		if not g.ducking and (g.fastwalk==1 or alt_is_down()) and g.walktime>g.maxwalktime: g.walktime-=10
def checkdown():
	if string_contains(get_tile_at(g.mr.x, g.mr.y, g.me.z), "wall", 1)>-1:
		g.p.play_3d("wall"+string_replace(get_tile_at(g.mr.x, g.mr.y, g.me.z), "wall", "", True)+".ogg", ox, oy, g.me.z, g.me.x, g.me.y, g.me.z, calculate_theta(g.facing), False)
		g.n.send_reliable(0,"xplay wall"+string_replace(get_tile_at(g.mr.x, g.mr.y, g.me.z), "wall", "", True)+"",0)
#		g.p.play_3d("wall"+string_replace(get_tile_at(g.mr.x, g.mr.y, g.me.z), "wall", "", True)+".ogg", g.me.x, g.me.y, g.me.z, g.me.x, g.me.y, g.me.z, calculate_theta(g.facing), False)

		g.n.send_reliable(1, "hitwall "+g.me.x+" "+g.me.y+" "+str(g.me.z), 0)
		bounceback(Down)
	else:
		playstep()
		g.n.send_reliable(0, "move_to "+str(g.mr.x)+" "+str(g.mr.y)+" "+str(g.me.z), 0)
		if not g.ducking and (g.fastwalk==1 or alt_is_down()) and g.walktime>g.maxwalktime: g.walktime-=10
def bounceback(d):
	if d == Up:
		g.me.z -= 1
	elif d==Down:
		g.me.z+=1
def checkcameratile():
	currentcameratile=get_tile_at(camera.x, camera.y, camera.z)
def gct():
	return get_tile_at(g.camera.x, g.camera.y, g.camera.z)
def playcamera(x=g.me.x, y=g.me.y, z=g.me.z):
	if gct() == "":
		g.p.play_3d("cameraair.ogg", g.me.x, g.me.y, g.me.z, g.camera.x, g.camera.y, g.camera.z, calculate_theta(g.facing), False)
	elif gct() == "hazard":
		g.p.play_3d("camerahazard.ogg", g.me.x, g.me.y, g.me.z, g.camera.x, g.camera.y, g.camera.z, calculate_theta(g.facing), False)
	elif string_contains(gct(), "wall", 1)>-1:
		g.p.play_extended_3d(gct()+".ogg", g.me.x, g.me.y, g.me.z, g.camera.x, g.camera.y, g.camera.z, calculate_theta(g.facing), 0, 0, 0, 0, 0, 0, False, 0.0, 0.0, 0.0, 200.0, False)
	else:
		g.p.play_extended_3d(gct()+"step"+randomstr(1, 5)+".ogg", g.me.x, g.me.y, g.me.z, g.camera.x, g.camera.y, g.camera.z, calculate_theta(g.facing), 0, 0, 0, 0, 0, 0, False, 0.0, 0.0, 0.0, 200.0, False)
def cameramove(dir):
	if dir == Up:
		if string_left(get_tile_at(g.camera.x, g.camera.y, g.camera.z + 1), 4) != "wall":
			g.camera.z += 1
			playcamera()
		else: 			g.camera.z += 1; playcamera(); g.camera.z-=1
	elif dir == Down:
		if string_left(get_tile_at(g.camera.x, g.camera.y, g.camera.z - 1), 4) != "wall":
			g.camera.z -= 1
			playcamera()
		else: g.camera.z-=1; playcamera(); g.camera.z+=1
	elif dir == Forward:
		ox = g.camera.x
		oy = g.camera.y
		stairs=get_staircase_at(g.camera.x, g.camera.y, g.camera.z)
		g.camera = move(g.camera.x, g.camera.y, g.camera.z, g.facing, north)
		stairs2=get_staircase_at(g.camera.x, g.camera.y, g.camera.z)

		#oz=g.me.z
		if stairs2=="x" and stairs=="x": g.camera.z+=g.camera.x-ox
		if stairs2=="y" and stairs=="y" : g.camera.z+=g.camera.y-oy
		#if get_tile_at(g.camera.x, g.camera.y, g.camera.z)=="":
			#if get_tile_at(g.camera.x, g.camera.y, g.camera.z-1)!="": g.camera.z-=1
			#if get_tile_at(g.camera.x, g.camera.y, g.camera.z+1)!="": g.camera.z+=1
		if round(g.camera.x) >= 0 and round(g.camera.x) <= g.max.x and round(g.camera.y) >= 0 and round(g.camera.y) <= g.max.y:
			if string_left(get_tile_at(g.camera.x, g.camera.y, g.camera.z), 4) != "wall":
				playcamera()
			else:
				playcamera()
				g.camera.x = ox
				g.camera.y = oy
	elif dir == Backward:
		ox = g.camera.x
		oy = g.camera.y
		stairs=get_staircase_at(g.camera.x, g.camera.y, g.camera.z)
		g.camera = move(g.camera.x, g.camera.y, g.camera.z, g.facing, south)
		stairs2=get_staircase_at(g.camera.x, g.camera.y, g.camera.z)

		#oz=g.me.z
		if stairs2=="x" and stairs=="x": g.camera.z+=g.camera.x-ox
		if stairs2=="y" and stairs=="y" : g.camera.z+=g.camera.y-oy

		if round(g.camera.x) >= 0 and round(g.camera.x) <= g.max.x and round(g.camera.y) >= 0 and round(g.camera.y) <= g.max.y:
			if string_left(get_tile_at(g.camera.x, g.camera.y, g.camera.z), 4) != "wall":
				playcamera()
			else:
				playcamera()
				g.camera.x = ox
				g.camera.y = oy
	elif dir == Left:
		ox = g.camera.x
		oy = g.camera.y
		stairs=get_staircase_at(g.camera.x, g.camera.y, g.camera.z)
		g.camera = move(g.camera.x, g.camera.y, g.camera.z, g.facing, west)

		stairs2=get_staircase_at(g.camera.x, g.camera.y, g.camera.z)

		#oz=g.me.z
		if stairs2=="x" and stairs=="x": g.camera.z+=g.camera.x-ox
		if stairs2=="y" and stairs=="y" : g.camera.z+=g.camera.y-oy

		if round(g.camera.x) >= 0 and round(g.camera.x) <= g.max.x and round(g.camera.y) >= 0 and round(g.camera.y) <= g.max.y:
			if string_left(get_tile_at(g.camera.x, g.camera.y, g.camera.z), 4) != "wall":
				playcamera()
			else:
				playcamera()
				g.camera.x = ox
				g.camera.y = oy
	elif dir == Right:
		ox = g.camera.x
		oy = g.camera.y
		stairs=get_staircase_at(g.camera.x, g.camera.y, g.camera.z)
		g.camera = move(g.camera.x, g.camera.y, g.camera.z, g.facing, east)
		stairs2=get_staircase_at(g.camera.x, g.camera.y, g.camera.z)

		#oz=g.me.z
		if stairs2=="x" and stairs=="x": g.camera.z+=g.camera.x-ox
		if stairs2=="y" and stairs=="y" : g.camera.z+=g.camera.y-oy


		if round(g.camera.x) >= 0 and round(g.camera.x) <= g.max.x and round(g.camera.y) >= 0 and round(g.camera.y) <= g.max.y:
			if string_left(get_tile_at(g.camera.x, g.camera.y, g.camera.z), 4) != "wall":
				playcamera()
			else:
				playcamera()
				g.camera.x = ox
				g.camera.y = oy
	if round(g.camera.x)<0: g.camera.x=0
	if round(g.camera.y)<0: g.camera.y=0
class mapreverb(object):
	def __init__(self):
		self.minx = 0; self.maxx = 0; self.miny = 0; self.maxy = 0; self.minz = 0; self.maxz = 0
		self._density = 1.0
		self._diffusion = 1.0
		self._gain = 0.32
		self._gainhf = 0.89
		self._decay_time = 1.49
		self._hfratio = 0.83
		self._reflections_gain = 0.05
		self._reflections_delay = 0.007
		self._late_reverb_gain = 1.26
		self._late_reverb_delay = 0.011
		self._air_absorption_gainhf = 0.994
		self._room_rolloff_factor = 0.0
		self._decay_hflimit = True

def get_reverb_at(x, y, z):
	mt=None
	x=round(x)
	y=round(y)
	z=round(z)
	for i in range(len(g.reverbs)):

		minx=g.reverbs[i].minx
		maxx=g.reverbs[i].maxx
		miny=g.reverbs[i].miny
		maxy=g.reverbs[i].maxy
		minz=g.reverbs[i].minz
		maxz=g.reverbs[i].maxz
		if(minx<=x and maxx>=x and miny<=y and maxy>=y and minz<=z and maxz>=z):

			mt=g.reverbs[i]


	return mt

g.get_reverb_at=get_reverb_at
def get_echo_at(x, y, z):
	mt=None
	x=round(x)
	y=round(y)
	z=round(z)
	for i in range(len(g.echos)):

		minx=g.echos[i].minx
		maxx=g.echos[i].maxx
		miny=g.echos[i].miny
		maxy=g.echos[i].maxy
		minz=g.echos[i].minz
		maxz=g.echos[i].maxz
		if(minx<=x and maxx>=x and miny<=y and maxy>=y and minz<=z and maxz>=z):

			mt=g.echos[i]


	return mt

g.get_echo_at=get_echo_at

class mapeaxreverb(object):
	def __init__(self):
		self.minx = 0; self.maxx = 0; self.miny = 0; self.maxy = 0; self.minz = 0; self.maxz = 0
		self._density = 1.0
		self._diffusion = 1.0
		self._gain = 0.32
		self._gainhf = 0.89
		self._gainlf = 1.0
		self._decay_time = 1.49
		self._decay_hfratio = 0.83
		self._decay_lfratio = 1.0
		self._reflections_gain = 0.05
		self._reflections_delay = 0.007
		self._reflections_pan = 0.0
		self._late_reverb_gain = 1.26
		self._late_reverb_delay = 0.011
		self._late_reverb_pan = 0.0
		self._echo_time = 0.25
		self._echo_depth = 0.0
		self._modulation_time = 0.25
		self._modulation_depth = 0.0
		self._air_absorption_gainhf = 0.994
		self._hfreference = 5000.0
		self._lfreference = 250.0
		self._room_rolloff_factor = 0.0
		self._decay_hflimit = True
def get_eaxreverb_at(x, y, z):
	mt=None
	x=round(x)
	y=round(y)
	z=round(z)
	for i in range(len(g.eaxreverbs)):

		minx=g.eaxreverbs[i].minx
		maxx=g.eaxreverbs[i].maxx
		miny=g.eaxreverbs[i].miny
		maxy=g.eaxreverbs[i].maxy
		minz=g.eaxreverbs[i].minz
		maxz=g.eaxreverbs[i].maxz
		if(minx<=x and maxx>=x and miny<=y and maxy>=y and minz<=z and maxz>=z):

			mt=g.eaxreverbs[i]


	return mt

g.get_eaxreverb_at=get_eaxreverb_at
class mapecho(object):
	def __init__(self):
		self.minx = 0; self.maxx = 0; self.miny = 0; self.maxy = 0; self.minz = 0; self.maxz = 0
		self._delay = 0.1
		self._LRdelay = 0.1
		self._damping = 0.5
		self._feedback = 0.5
		self._spread = -1.0
def alt_is_down():
	if(key_down(pygame.K_LALT)):

		return True

	return False

def remove_platform(minx, maxx, miny, maxy, minz, maxz, plattype):
	platform_to_remove = (round(minx), round(maxx), round(miny), round(maxy), round(minz), round(maxz), plattype)
	if platform_to_remove in g.map:
		g.map.remove(platform_to_remove)
def remove_zone(minx, maxx, miny, maxy, minz, maxz, plattype):
	zone_to_remove = (round(minx), round(maxx), round(miny), round(maxy), round(minz), round(maxz), plattype)
	if zone_to_remove in g.mapzones:
		g.mapzones.remove(zone_to_remove)


def update_platform(old_minx, old_maxx, old_miny, old_maxy, old_minz, old_maxz, old_plattype, new_minx, new_maxx, new_miny, new_maxy, new_minz, new_maxz, new_plattype):
	old_platform = (round(old_minx), round(old_maxx), round(old_miny), round(old_maxy), round(old_minz), round(old_maxz), old_plattype)
	new_platform = (round(new_minx), round(new_maxx), round(new_miny), round(new_maxy), round(new_minz), round(new_maxz), new_plattype)

	if old_platform in g.map:
		index = g.map.index(old_platform)
		g.map[index] = new_platform
	else:
		g.map.append(new_platform)
def is_staircase_reverse(x, y, z):
	mt=""
	x=round(x)
	y=round(y)
	z=round(z)
	for i in range(len(g.mapstairs)):

		sd=string_split(g.mapstairs[i], ":", True)
		minx=string_to_number(sd[0])
		maxx=string_to_number(sd[1])
		miny=string_to_number(sd[2])
		maxy=string_to_number(sd[3])
		minz=string_to_number(sd[4])
		maxz=string_to_number(sd[5])
		staircase=sd[7]

		if(minx<=x and maxx>=x and miny<=y and maxy>=y and minz<=z and maxz>=z):
			if g.mapstairs[i].endswith(":1"): return True
			else: return False