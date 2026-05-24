from timer import timer
import globals as g
from map import get_tile_at
from random import randint as random
from rotation import calculate_theta
from oal import al
import math
from rotation import calculate_theta
from oal import al
class player:

	def __init__(self, px, py, pz, pmap,  pname,srate):
		self.x=0
		self.playing=False
		self.friendlist=[]
		self.slot=None
		self.autotracktimer=timer()
		self.effect=None
		self.playing2=False
		self.slot2=None
		self.effect2=None

		self.y=0
		self.samplerate=srate
		self.reverb=False
		self.eaxreverb=False
		self.echo=False
		self.reverb2=False
		self.eaxreverb2=False
		self.echo2=False

		self.facing=0
		self.alplayed=False
		self.alplayed2=False
		self.z=0
		self.clearbuffertimer=timer()
		self.clearbuffertimer2=timer()
		self.matchteam=""
		self.map=""
		self.name=""
		self.x=px
		self.audio_buffer=[]
		self.audio_buffer2=[]
		self.y=py
		self.z=pz; self.map=pmap

		self.name=pname
	def position_voicechat_sound(self):
		if self.name==g.name: return
		source_x=round(self.x)
		source_y=round(self.y)
		source_z=round(self.z)
		listener_x=round(g.me.x)
		listener_y=round(g.me.y)
		listener_z=round(g.me.z)
		theta=calculate_theta(g.facing)
		delta_x = 0
		delta_y = 0
		delta_z = 0
		rotational_source_x = source_x
		rotational_source_y = source_y
		# First, we calculate the x and y based on the theta the listener is facing.
		if theta > 0.0:
			rotational_source_x = (
				(math.cos(theta) * (source_x - listener_x))
				- (math.sin(theta) * (source_y - listener_y))
				+ listener_x
			)
			rotational_source_y = (
				(math.sin(theta) * (source_x - listener_x))
				+ (math.cos(theta) * (source_y - listener_y))
				+ listener_y
			)
		source_x = rotational_source_x
		source_y = rotational_source_y

		# Next, we calculate the delta between the listener and the source.
		delta_x = source_x - listener_x
		delta_y = source_y - listener_y
		delta_z = source_z - listener_z
		x=delta_x
		y=delta_y
		z=delta_z
		try:
			al.alSourcei(self.alsrc, 4147, (x==0 and y==0 and z==0))
			al.alSource3f(self.alsrc, al.AL_POSITION, x, z, -y)
		except: pass
def spawn_player(x, y,z, map, name,srate):
	if get_player_index(name)>-1: return
	pl=player(x,y,z,map,name,srate)
	g.players.append(pl)
	
def remove_player(username):

	for i in g.players:
	
		if(i.name==username):
			try:
				al.alSourceUnqueueBuffers(i.alsrc, 1, i.albuf)
				al.alSourcei(i.alsrc, al.AL_BUFFER, 0)
				al.alDeleteSources(1, i.alsrc)
				al.alDeleteBuffers(1, i.albuf)
				al.alSourceUnqueueBuffers(i.alsrc2, 1, i.albuf)
				al.alSourcei(i.alsrc2, al.AL_BUFFER, 0)
				al.alDeleteSources(1, i.alsrc2)
				al.alDeleteBuffers(1, i.albuf2)

			except: pass
			g.players.remove(i)
		
	
def remove_all_players():

	g.players.clear()
	
def update_player_coordinates(n,x,y,z,m,f):
	if get_player_index(n)==-1: 	spawn_player(x,y,z,m,n,48000)
	for i in range(len(g.players)):
	
		if(g.players[i].name==n):
		
			g.players[i].x=x
			g.players[i].facing=f
			g.players[i].y=y
			g.players[i].z=z
			if(g.players[i].map!=m):
				g.players[i].map=m
			g.players[i].position_voicechat_sound()
			if(g.mapname!="lobby" and g.players[i].map==g.mapname and g.players[i].name!=g.name):
				if get_tile_at(g.players[i].x,g.players[i].y,g.players[i].z)!="":
					if g.watching!=g.players[i].name: s=g.p.play_3d(get_tile_at(g.players[i].x,g.players[i].y,g.players[i].z)+"step"+str(random(1,5))+".ogg",g.me.x,g.me.y,g.me.z,x,y,z,calculate_theta(g.facing),False)
					if g.watching==g.players[i].name: s=g.p.play_stationary(get_tile_at(g.players[i].x,g.players[i].y,g.players[i].z)+"step"+str(random(1,5))+".ogg",False)
					if g.players[i].map.startswith("zombie2") and g.players[i].matchteam=="blue": s.handle.pitch=80
			return
		
	spawn_player(x,y,z,m,n,48000)
def update_player_coordinates2(n,x,y,z,m,f):
	if get_player_index(n)==-1: 	spawn_player(x,y,z,m,n,48000)
	for i in range(len(g.players)):
	
		if(g.players[i].name==n):
		
			g.players[i].x=x
			g.players[i].facing=f
			g.players[i].y=y
			g.players[i].z=z
			if(g.players[i].map!=m):
				g.players[i].map=m
			return
		
	spawn_player(x,y,z,m,n,48000)

def get_player_index(n):
	for i in range(len(g.players)):
		if(g.players[i].name==n):
			return i
		
	return -1
	
