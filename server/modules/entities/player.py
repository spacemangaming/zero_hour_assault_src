from map import get_tile_at, barricade, ladder, get_hidden_area_at
from zh_nav_scanner import update_nav_scanner
import os
import time
from rotation import getdir, north, northeast, east, southeast, south, southwest, west, northwest
import time
from item import spawn_item
from file_directories import file_get_contents, file_put_contents

from rotation import calculate_x_y_string, calculate_x_y_angle
import pickle
import copy
from weapon import get_weapon_spread
from file_directories import file_delete, file_exists
from rotation import move
from timeditem import new_timeditem
from vector import vector
from moving_sound_serverside_handler import update_moving_sound, destroy_moving_sound
from flag import spawn_flag
from npc import get_weapon_range
from random import randint as random
from guns import guns
from weapon import spawn_weapon
from timer import timer
import data_loader
import globals as g
from bodyfall import spawn_bodyfall
from variable_management import string_contains
from variable_management import string_split
from rotation import get_3d_distance
from grenade import launch_grenade
from timebomb import place_timebomb
from mine import place_mine
from npc import usernames
from match import delay
from match import spawn_corpse
class player:
	def __init__(self,px,py,pz,pmap,pname,ppeer_id,srate):
		self.operator=False
		self.in_match_menu=False
		self.renaming=False
		self.renaming=False
		self.baseact=""
		self.silencertimer=timer()
		self.chattimer=timer()
		self.resendtimer=timer()
		self.droidtimer=timer()
		self.zkcontrollertimer=timer()
		self.baseentertime=0
		self.baseentertimer=timer()
		self.friendcount=0
		self.binocularsplayer=""
		self.bike=None
		# Transit / vehicle system
		self.in_bus=False
		self.bus_instance=None
		self.local_x=0
		self.local_y=0
		self.local_z=0
		self.itembeep=1
		self.aim_mode=1
		self.pingtimer=timer()
		self.pinging=False

		self.android=False
		self.ios=False

		self.matchinvite=1
		self.communitymessage=1
		self.use_server_menu_for_tickets = True # NEW: Default to true for server menu based ticket system
		self.ticket_selected_id = "" # NEW: To store the ID of the ticket currently being viewed/acted upon
		self.ticket_selected_department = "" # NEW: To store selected department during ticket creation workflow
		self.votecurrentpoll = None # NEW: To temporarily store the poll object when leaving a comment
		self.last_admin_login_ticket_count = 0 # NEW: For admin ticket notifications

		self.paid=False
		self.paidtime=0
		self.paidmonths=0
		self.items_got=0
		self.corpse_bomb=0
		self.spatialized_by=""
		self.spatializertimer=timer()
		self.backpacks_level=0
		self.backpacktimer=timer()
		self.adrenaline=False
		self.adrenalinetimer=timer()
		self.jammer=False
		self.jammertimer=timer()

		self.taketimer=timer()
		self.task_data={0:0,1:0,2:0,3:0}
		self.eventpoint=0
		self.currenteventpoint=0
		self.tokenplayers={}
		self.targeting=False
		self.targetx=0
		self.targety=0
		self.targetz=0
		self.helitimer=timer()
		self.freedomhelicopter=False
		self.freedomhelicoptertimer=timer()
		self.votenotify=1
		self.invites=[]
		self.motorhistory=""
		self.headhits=0
		self.headshots=0
		self.leghits=0
		self.legshots=0
		self.rain=False
		self.rainfinish=False
		self.rainvolume=0
		self.basemapappend=""
		self.drawtimer=timer()
		self.drawtime=0
		self.drawing=False
		self.chesttoken=0
		self.silenced=[]
		self.can_move=True
		self.flashvolume=100
		self.blockoffline=False
		self.blockofflinetimer=timer()
		self.invisible=False
		self.invisibletimer=timer()
		self.hidden=False
		self.chest=None
		self.corpse=None
		self.tokentransfer=1
		self.weapon_rays=None
		self.sitting=False
		self.weapon_rays2=None
		self.jailtimer=timer()
		self.jailreason=""
		self.jailed=False
		self.tokentimer=timer()
		self.scoretimer=timer()
		self.scoretimer.elapsed=300000
		self.tokentimer.elapsed=300000
		self.ticketmail=1
		self.eventalerts=1
		self.mapsound=1
		self.istyping=1
		self.chestpickupnotify=1
		self.authreq=0
		self.firstrank=True
		self.shielded=False
		self.shieldhitchance=0
		self.helmeted=False
		self.helmethitchance=0
		self.lasthelmethitchance=0

		self.status=""
		self.near=False
		self.placetimebomb=False
		self.placeladder=False
		self.placebarricade=False
		self.placetimebombtimer=timer()
		self.placemine=False
		self.placeminetimer=timer()
		self.placeladdertimer=timer()
		self.placebarricadetimer=timer()
		self.version="1.2.1"
		self.respawn=False
		self.respawntimer=timer()
		self.weapon2=""
		self.movetimer=timer()
		self.move2timer=timer()
		self.move3timer=timer()
		self.move4timer=timer()
		self.move5timer=timer()
		self.move6timer=timer()

		self.suggesttimer=timer()
		self.cannotexit=False
		self.cannotexittimer=timer()
		self.faint=False
		self.fainted=False
		self.fainttimer=timer()
		self.maxhpcheckertimer=timer()
		self.maxhpchecker2timer=timer()
		self.hudtimer=timer()
		self.blockvoice3=0
		self.group=""
		self.community=""

		self.lobytimer=timer()
		self.freedomtimer=timer()
		self.flagtimer=timer()
		self.basetimer=timer()
		self.voiceon=0
		self.voiceon2=0
		self.snowcollecttimer=timer()
		self.snowtimer=timer()
		self.stuntimer=timer()
		self.stuntime=0
		self.stunned=False
		self.mmode=""
		self.voicechatgroup=1

		self.voicechatmap=1
		self.voicechatfriend=1
		self.voicechatteam=1
		self.langchan="english"
		self.gender=""
		self.blocks=[]
		self.botkills=0
		self.botdeaths=0
		self.playerkills=0
		self.playerdeaths=0
		self.cancreatelanguage=0
		self.grenadeonetimer=timer()
		self.grenadetwotimer=timer()
		self.grenadepin=False
		self.grenadepintimer=timer()
		self.specmap=""
		self.ingroup=False
		self.groupinvitations=[]
		self.groupinvitations=[]
		self.incommunity=False
		self.communityinvitations=[]
		self.communityinvitations=[]

		self.wx=0;self.wy=0;self.wz=0
		self.helijumptimer=timer()
		self.inve=False
		self.aim=0
		self.friendtimer=timer()
		self.matchinvitetimer=timer()
		self.motorhorntimer=timer()
		self.mapmessage=1
		self.groupmessage=1
		self.groupinvitation=1
		self.communitymessage=1
		self.communityinvitation=1

		self.menuitems=[]
		self.menuids=[]
		self.nearchecktimer=timer()
		self.menuacts=[]
		self.initial_packet=""
		self.pmmessage=1
		self.vehiclehorntimer=timer()
		self.vi=-1
		self.voicemessage=1
		self.voicemessage2=1
		self.friendmessage=1
		self.matchmessage=1
		self.teammessage=1
		self.friendonlinemessage=1
		self.filechecktimer=timer()
		self.ducking=False
		self.samplerate=srate
		self.rankchecktimer=timer()
		self.listen=1
		self.scorerank=""
		self.scope=1
		self.plusdammage=0
		self.specplayer=""
		self.maxhealth=100
		self.sitregentimer=timer()
		self.audio_buffer=[]
		self.current_char="tristan"
		self.friendlist=[]
		self.pendingfriendlist=[]
		self.voicechatwho="sameteam"
		self.bought_chars=["tristan"]
		self.msounds=[]
		self.msoundtimers=[]
		self.oldx=0
		self.oldy=0
		self.oldz=0
		self.matchbanned=[]

		self.lngmanage=""
		self.matchpasswordowner=""
		self.flag=0
		self.weaponbeeptimer=timer()
		self.weaponbeeptimer2=timer()
		self.matchmode=""
		self.matchtype=""
		self.lang=""
		self.matchpassword=""
		self.matchtypeamount=0
		self.helitimer=timer()
		self.parachuted=False
		self.zhtoken=1
		self.storeitem=""
		self.event_storeitem=""
		self.usetimer=timer()
		self.targetx=0
		self.targety=0
		self.targetz=0
		self.targeting=False
		self.matchteam=""
		self.joinedmatch=""
		self.specmatch=""
		self.exithouse=False
		self.killn=1
		self.nearn=1
		self.sameteambots=1
		self.sameteamplayers=1
		self.differentteambots=1
		self.differentteamplayers=1
		self.samegroupplayers=1
		self.differentgroupplayers=1
		self.charvoice=1
		self.sound=1
		self.ammo={}
		self.beacontimer=timer()
		self.zombienoisetimer=timer()
		self.zombie=False
		self.beacon=1
		self.fivecount=False
		self.fivecounttimer=timer()
		self.killcount=0

		self.invitelist=[]
		self.compid=""
		self.nearbots=[]
		self.isbot=False
		self.hitby2=""
		self.hitby=""
		self.molotovthrowtimer=timer()
		self.drinktimer=timer()
		self.x=0
		self.y=0
		self.z=0
		self.scorepoint=0
		self.map=""
		self.name=""
		self.title=""
		self.title2="Player"

		self.nearplayers=[]
		self.peer_id=-1
		self.zone=""
		self.dev=False
		self.dead=False
		self.reloading=False
		self.hitby="nothing"
		self.health=100
		self.weaponcurrent_weapon=None
		self.weapon=""
		self.firing=False
		self.hittimer=timer()
		self.invchecktimer=timer()
		self.firetimer=timer()
		self.firetimer2=timer()
		self.reloadtimer=timer()
		self.reloadtime=0
		self.weaponauto=False
		self.facing=0
		self.inv=dict()
		self.cachedinv=dict()
		self.storeinv=dict()

		self.beacontimer=timer()
		self.beacontime=850
		self.builder=False
		self.moderator=False
		self.admin=False
		self.replyname=""
		self.safe=False
		self.map=pmap
		self.x=px
		self.y=py
		self.z=pz
		self.name=pname
		self.peer_id=ppeer_id
		self.friendtimer.elapsed=200000
		self.matchinvitetimer.elapsed=200000

		# Navigation Assist – 6-direction wall proximity scanner state.
		# Each entry stores (tiletype | None, distance | None) from the last scan.
		# (None, None) means that direction was clear within SCAN_RANGE tiles.
		self.nav_scan = {
			"right": (None, None),
			"left":  (None, None),
			"front": (None, None),
			"back":  (None, None),
			"up":    (None, None),
			"down":  (None, None),
		}
		# Integer (x, y, z) position at last nav scan; sentinel forces first scan.
		self.last_scan_pos = (-99999, -99999, -99999)

	@property
	def firetime(self):
		try:
			holder=g.wdata[self.weapon]
			stuff=string_split(holder," ",False)
			return int(stuff[0])
		except: return 0
	@property
	def firetime2(self):
		try:
			holder=g.wdata[self.weapon2]
			stuff=string_split(holder," ",False)
			return int(stuff[0])
		except: return 0

	def get_firetime(self):
		if not self.adrenaline: return self.firetime
		return self.firetime-(self.firetime*25/100)
	def get_firetime2(self):
		if not self.adrenaline: return self.firetime2
		return self.firetime2-(self.firetime2*25/100)

	def get_friend_count_in_freedom(self):
		ret=0
		for p in g.players:
			if p.hidden: continue
			if (p.map=="helicopter" or p.map=="massacre_in_the_city") and self.name in p.friendlist: ret+=1
		return ret

	def friendloop(self):
		if self.hidden: return
		if len(self.friendlist)!=self.friendcount:
			self.friendcount=len(self.friendlist)
			for p in g.players: g.n.send_reliable(p.peer_id,"friendlist "+self.name+" "+"\n".join(self.friendlist),0)
	def get_backpack_level_amount(self,orig):
		if self.paid: return 999999999999
		if self.backpacks_level==0: return orig
		if self.backpacks_level==1: return orig*2
		if self.backpacks_level==2: return orig*3
		if self.backpacks_level==3: return orig*4
	def is_completed_task(self):
		if g.task==-1: return False
		if g.task==0: return self.task_data[0]>=5
		if g.task==1: return self.task_data[1]>=20
		if g.task==2: return self.task_data[2]>=50
		if g.task==3: return self.task_data[3]>=15
	def helicopterloop(self):
		p=self
		if p.targeting==False:
			p.targetx=random(0,500)
			p.targety=random(0,500)
			p.targeting=True
		if p.x==p.targetx and p.y==p.targety and p.z==p.targetz and p.targeting:
			p.targeting=False
			return
		if p.targeting and p.helitimer.elapsed>50:
			p.helitimer.restart()
			if p.x<p.targetx:
				p.x+=1
				if string_contains(g.get_nwall_at(p.x,p.y,p.z,p.map),"wall",1)>-1:
					p.x-=1
					if not p.hidden: g.n.broadcast("update_player2 "+str(p.x)+" "+str(p.y)+" "+str(p.z)+" "+p.map+" "+p.name+" "+str(p.facing),20)

				g.n.send_reliable(p.peer_id,"move "+str(p.x)+" "+str(p.y)+" "+str(p.z),0)

			if p.x>p.targetx:
				p.x-=1
				if not p.hidden: g.n.broadcast("update_player2 "+str(p.x)+" "+str(p.y)+" "+str(p.z)+" "+p.map+" "+p.name+" "+str(p.facing),20)
				if string_contains(g.get_nwall_at(p.x,p.y,p.z,p.map),"wall",1)>-1:
					p.x+=1
					if not p.hidden: g.n.broadcast("update_player2 "+str(p.x)+" "+str(p.y)+" "+str(p.z)+" "+p.map+" "+p.name+" "+str(p.facing),20)

				g.n.send_reliable(p.peer_id,"move "+str(p.x)+" "+str(p.y)+" "+str(p.z),0)

			if p.y>p.targety:
				p.y-=1

				if not p.hidden: g.n.broadcast("update_player2 "+str(p.x)+" "+str(p.y)+" "+str(p.z)+" "+p.map+" "+p.name+" "+str(p.facing),20)
				if string_contains(g.get_nwall_at(p.x,p.y,p.z,p.map),"wall",1)>-1:
					p.y+=1

					if not p.hidden: g.n.broadcast("update_player2 "+str(p.x)+" "+str(p.y)+" "+str(p.z)+" "+p.map+" "+p.name+" "+str(p.facing),20)


				g.n.send_reliable(p.peer_id,"move "+str(p.x)+" "+str(p.y)+" "+str(p.z),0)

			if p.y<p.targety:
				p.y+=1

				if not p.hidden: g.n.broadcast("update_player2 "+str(p.x)+" "+str(p.y)+" "+str(p.z)+" "+p.map+" "+p.name+" "+str(p.facing),20)
				if string_contains(g.get_nwall_at(p.x,p.y,p.z,p.map),"wall",1)>-1:
					p.y-=1

					if not p.hidden: g.n.broadcast("update_player2 "+str(p.x)+" "+str(p.y)+" "+str(p.z)+" "+p.map+" "+p.name+" "+str(p.facing),20)


				g.n.send_reliable(p.peer_id,"move "+str(p.x)+" "+str(p.y)+" "+str(p.z),0)

	def heliendloop(self):
		if self.freedomhelicoptertimer.elapsed>=2*60000:
			if self.map=="helicopter":
				g.move_player(g.get_player_index_from(self.name),self.x,self.y,70,"massacre_in_the_city")
				g.n.send_reliable(self.peer_id,"distsound helicopterdist "+str(self.x)+" "+str(self.y+50)+" "+str(self.z)+" massacre_in_the_city",0)
			self.freedomhelicopter=False
	def set_drawtime(self,d):
		if self.paid==True: return
		if d is None: return
		if d is not None: self.drawtime=d
		self.drawing=True
		self.drawtimer.restart()
		g.n.send_reliable(self.peer_id,"drawtime "+str(d),0)
	def get_last_motd_changelog_reboot_counts(self):
		import db as _db
		s="Since your last login, "
		if _db.charexists(self.name,"rebootcount"): s+="the server has been rebooted "+_db.charread(self.name,"rebootcount")+" times. "
		if _db.charexists(self.name,"votecount"): s+=_db.charread(self.name,"votecount")+" new votes created. "
		if _db.charexists(self.name,"motdcount"): s+="The message of the day changed "+_db.charread(self.name,"motdcount")+" times. "
		if _db.charexists(self.name,"changelogcount"): s+="The last changes section updated "+_db.charread(self.name,"changelogcount")+" times. "
		_db.chardelete(self.name,"changelogcount")
		_db.chardelete(self.name,"rebootcount")
		_db.chardelete(self.name,"votecount")
		_db.chardelete(self.name,"motdcount")
		if s=="Since your last login, ": s=""
		return s
	def _chat_check(self, field_time, field_reason, label):
		import db as _db
		if not _db.charexists(self.name, field_time): return True
		try: timestamp = int(_db.charread(self.name, field_time, "0"))
		except: return True
		if int(time.time()) < timestamp:
			reason = _db.charread(self.name, field_reason, "")
			g.n.send_reliable(self.peer_id, f"Error. Your {label} chat is disabled. Reason: {reason}. Re-enabled after {ms_to_readable_time(timestamp-int(time.time()))}.", 0)
			return False
		else:
			_db.chardelete(self.name, field_time)
			_db.chardelete(self.name, field_reason)
			return True

	def disable_public_chat_check(self):
		if self.jailed: g.n.send_reliable(self.peer_id,"You are jailed",0); return False
		return self._chat_check("disablepublicchattime","disablepublicchatreason","public")

	def disable_public_chat_check2(self):
		import db as _db
		if not _db.charexists(self.name,"disablepublicchattime"): return True
		try: timestamp=int(_db.charread(self.name,"disablepublicchattime","0"))
		except: return True
		if int(time.time())<timestamp: return False
		_db.chardelete(self.name,"disablepublicchattime"); _db.chardelete(self.name,"disablepublicchatreason")
		g.n.send_reliable(self.peer_id,"Your public chat feature is enabled",2); return True

	def disable_pm_chat_check2(self):
		import db as _db
		if not _db.charexists(self.name,"disablepmchattime"): return True
		try: timestamp=int(_db.charread(self.name,"disablepmchattime","0"))
		except: return True
		if int(time.time())<timestamp: return False
		_db.chardelete(self.name,"disablepmchattime"); _db.chardelete(self.name,"disablepmchatreason")
		g.n.send_reliable(self.peer_id,"Your pm chat feature is enabled",2); return True

	def disable_team_chat_check2(self):
		import db as _db
		if not _db.charexists(self.name,"disableteamchattime"): return True
		try: timestamp=int(_db.charread(self.name,"disableteamchattime","0"))
		except: return True
		if int(time.time())<timestamp: return False
		_db.chardelete(self.name,"disableteamchattime"); _db.chardelete(self.name,"disableteamchatreason")
		g.n.send_reliable(self.peer_id,"Your team chat feature is enabled",2); return True

	def disable_group_chat_check2(self):
		import db as _db
		if not _db.charexists(self.name,"disablegroupchattime"): return True
		try: timestamp=int(_db.charread(self.name,"disablegroupchattime","0"))
		except: return True
		if int(time.time())<timestamp: return False
		_db.chardelete(self.name,"disablegroupchattime"); _db.chardelete(self.name,"disablegroupchatreason")
		g.n.send_reliable(self.peer_id,"Your group chat feature is enabled",2); return True

	def disable_map_chat_check2(self):
		import db as _db
		if not _db.charexists(self.name,"disablemapchattime"): return True
		try: timestamp=int(_db.charread(self.name,"disablemapchattime","0"))
		except: return True
		if int(time.time())<timestamp: return False
		_db.chardelete(self.name,"disablemapchattime"); _db.chardelete(self.name,"disablemapchatreason")
		g.n.send_reliable(self.peer_id,"Your map chat feature is enabled",2); return True

	def disable_public_chat(self,minutes,reason):
		import db as _db
		_db.charwrite(self.name,"disablepublicchattime",str(minutes_to_timestamp(minutes)))
		_db.charwrite(self.name,"disablepublicchatreason",reason)
		g.n.send_reliable(self.peer_id,"Your public chat feature has been disabled for "+str(minutes)+" minutes for the following reason: "+reason,2)
	def disable_all_chat_check(self):
		if self.jailed: g.n.send_reliable(self.peer_id,"You are jailed",0); return False

		import db as _db
		if not _db.charexists(self.name,"disableallchattime"): return True
		try: timestamp=int(_db.charread(self.name,"disableallchattime","0"))
		except: return True
		if int(time.time())<timestamp:
			reason=_db.charread(self.name,"disableallchatreason","")
			g.n.send_reliable(self.peer_id,"Error. Your all chat is disabled due to following reason: "+reason+". It will be re-enabled after "+ms_to_readable_time(timestamp-int(time.time()))+".",0)
			return False
		else:
			_db.chardelete(self.name,"disableallchattime"); _db.chardelete(self.name,"disableallchatreason"); return True
	def disable_all_chat_check2(self):
		import db as _db
		if not _db.charexists(self.name,"disableallchattime"): return True
		try: timestamp=int(_db.charread(self.name,"disableallchattime","0"))
		except: return True
		if int(time.time())<timestamp: return False
		_db.chardelete(self.name,"disableallchattime"); _db.chardelete(self.name,"disableallchatreason")
		g.n.send_reliable(self.peer_id,"Your all chat feature is enabled",2); return True


	def disable_all_chat(self,minutes,reason):
		import db as _db
		_db.charwrite(self.name,"disableallchattime",str(minutes_to_timestamp(minutes)))
		_db.charwrite(self.name,"disableallchatreason",reason)
		g.n.send_reliable(self.peer_id,"Your all chat feature has been disabled for "+str(minutes)+" minutes for the following reason: "+reason,2)

	def disable_pm_chat_check(self):
		if self.jailed: g.n.send_reliable(self.peer_id,"You are jailed",0); return False
		return self._chat_check("disablepmchattime","disablepmchatreason","pm")

	def disable_vote_check(self):
		if self.jailed: g.n.send_reliable(self.peer_id,"You are jailed",0); return False
		import db as _db
		if not _db.charexists(self.name,"disablevotetime"): return True
		try: timestamp=int(_db.charread(self.name,"disablevotetime","0"))
		except: return True
		if int(time.time())<timestamp:
			reason=_db.charread(self.name,"disablevotereason","")
			g.n.send_reliable(self.peer_id,"Error. Your vote and poll feature is disabled due to following reason: "+reason+". It will be re-enabled after "+ms_to_readable_time(timestamp-int(time.time()))+".",0)
			return False
		_db.chardelete(self.name,"disablevotetime"); _db.chardelete(self.name,"disablevotereason"); return True

	def disable_pm_chat(self,minutes,reason):
		import db as _db
		_db.charwrite(self.name,"disablepmchattime",str(minutes_to_timestamp(minutes)))
		_db.charwrite(self.name,"disablepmchatreason",reason)
		g.n.send_reliable(self.peer_id,"Your pm chat feature has been disabled for "+str(minutes)+" minutes for the following reason: "+reason,2)
	def disable_vote(self,minutes,reason):
		import db as _db
		_db.charwrite(self.name,"disablevotetime",str(minutes_to_timestamp(minutes)))
		_db.charwrite(self.name,"disablevotereason",reason)
		g.n.send_reliable(self.peer_id,"Your vote and poll feature has been disabled for "+str(minutes)+" minutes for the following reason: "+reason,2)

	def disable_team_chat_check(self):
		if self.jailed: g.n.send_reliable(self.peer_id,"You are jailed",0); return False
		return self._chat_check("disableteamchattime","disableteamchatreason","team")

	def disable_team_chat(self,minutes,reason):
		import db as _db
		_db.charwrite(self.name,"disableteamchattime",str(minutes_to_timestamp(minutes)))
		_db.charwrite(self.name,"disableteamchatreason",reason)
		g.n.send_reliable(self.peer_id,"Your team chat feature has been disabled for "+str(minutes)+" minutes for the following reason: "+reason,2)
	def disable_map_chat_check(self):
		if self.jailed: g.n.send_reliable(self.peer_id,"You are jailed",0); return False
		return self._chat_check("disablemapchattime","disablemapchatreason","map")

	def disable_map_chat(self,minutes,reason):
		import db as _db
		_db.charwrite(self.name,"disablemapchattime",str(minutes_to_timestamp(minutes)))
		_db.charwrite(self.name,"disablemapchatreason",reason)
		g.n.send_reliable(self.peer_id,"Your map chat feature has been disabled for "+str(minutes)+" minutes for the following reason: "+reason,2)
	def disable_group_chat_check(self):
		if self.jailed: g.n.send_reliable(self.peer_id,"You are jailed",0); return False
		return self._chat_check("disablegroupchattime","disablegroupchatreason","group")

	def disable_group_chat(self,minutes,reason):
		import db as _db
		_db.charwrite(self.name,"disablegroupchattime",str(minutes_to_timestamp(minutes)))
		_db.charwrite(self.name,"disablegroupchatreason",reason)
		g.n.send_reliable(self.peer_id,"Your group chat feature has been disabled for "+str(minutes)+" minutes for the following reason: "+reason,2)

	def motormove(self):
		if self.vi!=-1:
			motor=g.motors[self.vi]
			motor.x=self.x
			motor.y=self.y
			motor.z=self.z
			motor.map=self.map
			for msound in g.msounds:
				if msound.id==motor.mid:
					msound.map=self.map
					update_moving_sound(motor.mid, motor.x, motor.y, motor.z, motor.pitch)
			for p in g.players:
				if p.map==self.map: send_platform(p, self.x, self.x, self.y, self.y, self.z, self.z+4, "wallspaceship")
				if p.map==self.map: send_platform(p, self.x, self.x, self.y, self.y, self.z+5, self.z+5, "cloth")
	def play_watch_scope(self):
		for p in g.players:
			if p.specplayer==self.name: g.n.send_reliable(p.peer_id,"play_s scope.ogg",0)
	def send_bulletbody(self):
		packet="play_s bullet_impact_body"+str(random(1,2))+".ogg"
		g.n.send_reliable(self.peer_id,packet,0)
		for p in g.players:
			if p.specplayer==self.name: 		g.n.send_reliable(p.peer_id,packet,0)
	def send_bulletbody2(self):
		packet="play_s bullet_impact_body"+str(random(7,9))+".ogg"
		g.n.send_reliable(self.peer_id,packet,0)
		for p in g.players:
			if p.specplayer==self.name: 		g.n.send_reliable(p.peer_id,packet,0)

	def send_teaminfo_menu(self):
		self.packet("matchteam "+self.matchteam,0)
		packet=""
		for m in g.matches:
			if self.joinedmatch==m.owner:
				for pl in m.players:
					p=g.getpc(pl)
					if p is not None:
						if p.matchteam!=self.matchteam:
							packet+=p.matchteam+":"+p.name+"\n"
						elif p.matchteam==self.matchteam:
							packet+=p.matchteam+":"+p.name+", at coordinates "+str(round(p.x))+", "+str(round(p.y))+", "+str(round(p.z))+". They have drawn "+p.weapon+".\n"
				for pl in m.deadplayers:
					p=g.getpc(pl)
					if p is not None:
						packet+=p.matchteam+":"+p.name+", dead\n"
					else:
						import db as _db
						team=_db.charread(pl,"matchteam","")
						if team!="": packet+=team+":"+pl+", dead\n"
		if packet!="":
			self.packet("matchteammenu "+packet,0)

	def prevmenu(self):
		m=g.server_menu()
		m.initial_packet=self.initial_packet
		m.intro="prevmenu"
		m.menuitems=copy.deepcopy(self.menuitems)
		m.menuids=copy.deepcopy(self.menuids)
		m.menuacts=copy.deepcopy(self.menuacts)
		self.menuitems.clear()
		self.menuids.clear()
		self.menuacts.clear()
		if m.initial_packet=="removefriend":
			m.menuitems.clear(); m.menuids.clear(); m.menuacts.clear(); g.removefriendadd(m,g.get_player_index_from(self.name))
		if m.initial_packet=="chest":
			m.menuitems.clear(); m.menuids.clear(); m.menuacts.clear(); g.chestadd(self,self.chest,m,True)
		if m.initial_packet=="community2":
			m.menuitems.clear(); m.menuids.clear(); m.menuacts.clear()

		if m.initial_packet=="group2":
			m.menuitems.clear(); m.menuids.clear(); m.menuacts.clear()
			if 1:
				if 1:
					if 1:
						grp=g.get_group(self.group)
						if grp is None: return
						m.add("group members","members")
						m.add("group admins","admins")
						m.add("donate to this group","donate")
						m.add("view announcement","viewannouncement")
						m.add("view donation history","donate2")
						if grp.owner==self.name or self.name in grp.admins:
							m.add("view group action history","action")
							m.add("view group base chest log","log")
							m.add("clear group action history","action2")
							m.add("kick a member","kick")
							m.add("put a base here","putbase")
							m.add("invite a player to this group","invite")
							m.add("remove invitation of a player to this group","invite2")
							m.add("View group join requests","request")
							if grp.freedomhit==1: m.add("Disable members' hitting each other in freedom fight map","freedom")
							if grp.freedomhit==0: m.add("Enable members' hitting each other in freedom fight map","freedom")
							m.add("view zero token amount donated to this group","donatetoken")
						if grp.owner==self.name:
							m.add("make a member the group administrator","makeadmin")
							m.add("remove a member's group administrator role","removeadmin")
							m.add("change group owner","owner")
							m.add("rename this group","rename")
							m.add("publish announcement","announce")
							m.add("get zero tokens from donated tokens","donate3")

							m.add("delete this group","delete")
						if grp.owner!=self.name and self.name not in grp.admins: m.add("leave this group","leave")
						if grp.owner!=self.name and self.name in grp.admins: m.add("resign from administrating this group","resign")
						if grp.owner==self.name or self.name in grp.admins:
							m.add("View group base info","base")
		if m.initial_packet=="community2":
			m.menuitems.clear(); m.menuids.clear(); m.menuacts.clear()
			if 1:
				if 1:
					if 1:

						grp=g.get_community(self.community)
						if grp is None: return
						m.add("community members","members")
						m.add("community admins","admins")
						m.add("view announcement","viewannouncement")
						if grp.owner==self.name or self.name in grp.admins:
							m.add("view community action history","action")
							m.add("clear community action history","action2")
							m.add("kick a member","kick")
							m.add("invite a player to this community","invite")
							m.add("remove invitation of a player to this community","invite2")
							m.add("View community join requests","request")
						if grp.owner==self.name:
							m.add("make a member the community administrator","makeadmin")
							m.add("remove a member's community administrator role","removeadmin")
							m.add("change community owner","owner")
							m.add("rename this community","rename")
							m.add("publish announcement","announce")
							m.add("delete this community","delete")
						if grp.owner!=self.name and self.name not in grp.admins: m.add("leave this community","leave")
						if grp.owner!=self.name and self.name in grp.admins: m.add("resign from administrating this community","resign")
		if m.initial_packet=="corpse":
			m.menuitems.clear(); m.menuids.clear(); m.menuacts.clear(); g.corpseadd(self,self.corpse,m,True)


		m.send(self.peer_id)
	def check_rank(self):
		oldrank=self.scorerank
		self.scorerank = data_loader.get_rank(self.scorepoint)
		if oldrank!=self.scorerank and not self.firstrank:
			g.n.send_reliable(self.peer_id,"play_s misc295.ogg",0)
			g.n.send_reliable(self.peer_id,"Your score rank is changed to "+self.scorerank+" because you reached "+str(self.scorepoint)+" score points!",2)
		self.firstrank=False
	def get_current_char(self):
		if self.current_char=="default": return "tristan"
		if self.current_char=="": return "tristan"

		else: return self.current_char
	def get_plus_damage(self):
		return data_loader.get_character(self.get_current_char()).get("plus_damage", 0)
	def get_char_properties(self):
		cdata = data_loader.get_character(self.get_current_char())
		walktime = cdata.get("walk_time", 250)
		maxwalktime = cdata.get("max_walk_time", 150)
		health = cdata.get("health", 100)
		plusdammage = cdata.get("plus_damage", 0)
		jumptime = cdata.get("jump_time", 50)
		if self.paid: health+=30
		g.n.send_reliable(self.peer_id,"walktime "+str(walktime),0)
		g.n.send_reliable(self.peer_id,"maxwalktime "+str(maxwalktime),0)
		g.n.send_reliable(self.peer_id,"jumptime "+str(jumptime),0)
		self.maxhealth=health
		self.plusdammage=plusdammage
		self.jumptime=jumptime
	def distancecheck(self, xx, yy, zz):
		return get_3d_distance(self.wx, self.wy, self.wz, xx, yy, zz)

	def is_builder(self):
	
		if(self.builder or self.admin or self.dev):
		
			return True
			
		return False
		
	def is_admin(self):
	
		if(self.admin or self.dev):
		
			return True
			
		return False
		
	def chat(self,message):
	
		file_put_contents("chats.log", ""+self.name+" in channel "+self.langchan+" "+message+"\n", "a")

		for i in range(len(g.players)):
		
			if self.name not in g.players[i].blocks and self.langchan==g.players[i].langchan:
				g.send_reliable(g.players[i].peer_id,"chat "+message,1)
			
		
	def randomweapongive(self):
		loadouts = data_loader.get_player_random_loadouts()
		chosen = loadouts[random(0, len(loadouts)-1)]
		self.give(chosen["weapon"], 1)
		if chosen.get("ammo_type") and chosen.get("ammo_count"):
			self.give(chosen["ammo_type"], chosen["ammo_count"])
		self.give("knife", 1)
	def itemplay(self,item):
		self.playsound(data_loader.get_item_sound(item))

	def playsound(self,sound,include_me=True,SendReliable=False):
	
		if(include_me==True) :
			if(SendReliable==True):
				g.send_reliable(self.peer_id,"play_s "+sound+".ogg",0)
			elif(SendReliable==False):
				if "heart" in sound: g.n.send_unreliable(self.peer_id,"play_s "+sound+".ogg",0)
				if "heart" not in sound: g.n.send_reliable(self.peer_id,"play_s "+sound+".ogg",0)
			
		for p in g.players:
			if p.specplayer==self.name: g.n.send_reliable(p.peer_id,"play_s "+sound+".ogg",0); continue
			if g.get_hidden_area_at(p.x,p.y,p.z,p.map)!=g.get_hidden_area_at(self.x,self.y,self.z,self.map): continue
			if p.name==self.name: continue
			if p.map!=self.map: continue
			g.send_reliable(p.peer_id, sound+" "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" "+self.map+" 100", 3)
		
	def playsoundnonlobby(self,sound,include_me=True,SendReliable=False):
	
		if(include_me==True) :
			if(SendReliable==True):
				g.send_reliable(self.peer_id,"play_s "+sound+".ogg",0)
			elif(SendReliable==False):
				if "heart" in sound: g.n.send_unreliable(self.peer_id,"play_s "+sound+".ogg",0)
				if "heart" not in sound: g.n.send_reliable(self.peer_id,"play_s "+sound+".ogg",0)
			
		for p in g.players:
			if p.specplayer==self.name: g.n.send_reliable(p.peer_id,"play_s "+sound+".ogg",0); continue
			if g.get_hidden_area_at(p.x,p.y,p.z,p.map)!=g.get_hidden_area_at(self.x,self.y,self.z,self.map): continue
			if p.name==self.name: continue
			if p.map!=self.map: continue
			if self.map=="lobby": continue
			g.send_reliable(p.peer_id, sound+" "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" "+self.map+" 100", 3)

	def playsoundmoving(self,snd,include_me=True):
		if include_me: g.playmoving(self.x,self.y,self.z,self.map,snd,self)
		else: g.playmoving2(self.x,self.y,self.z,self.map,snd,self)
	def gettile(self):
		return get_tile_at(self.x, self.y, self.z, self.map)
		
	def packet(self,pkt,chan=2,r=True):
		if(r):
			g.send_reliable(self.peer_id,pkt,chan)
		else:
			g.send_reliable(self.peer_id,pkt,chan)
		
	def get_weapon_properties(self,w):
		self.weapon_rays=None
		self.weapon_rays2=None
		canjump=1
		canduck=1
		walktime=-1
		maxwalktime=-1
		maxaim=get_weapon_spread(self.weapon)*2
		maxaim2=get_weapon_spread(self.weapon2)*2
		if maxaim2>maxaim: maxaim=maxaim2
		g.n.send_reliable(self.peer_id,"maxaim "+str(maxaim),0)
		if self.weapon=="mkek_jng90" or self.weapon2=="mkek_jng90":
#			canjump=0
			walktime=300
			maxwalktime=200
		if self.weapon=="dragunov_psl" or self.weapon2=="dragunov_psl":
			canjump=1
			canduck=1
			walktime=300
			maxwalktime=250
		if w not in g.wdata:
			return
		else :
			holder=""
			holder=g.wdata[w]
			stuff=string_split(holder," ",False)
			time=int(stuff[0])
			state=holder[1]
			if(state!="normal" or state!="norm") :
				self.weaponauto=True
				
			
		
		g.n.send_reliable(self.peer_id,"canjump "+str(canjump),0)
		g.n.send_reliable(self.peer_id,"canduck "+str(canduck),0)
		if walktime!=-1: g.n.send_reliable(self.peer_id,"walktime "+str(walktime),0)
		if maxwalktime!=-1: g.n.send_reliable(self.peer_id,"maxwalktime "+str(maxwalktime),0)
		else: self.get_char_properties()
	def play_hit_sound(self):
		if self.map.startswith("zombie2") and self.matchteam=="blue":
			self.playsound("zombiehurt")
		else: self.playsound(self.get_current_char()+"voice"+str(random(1,16)))
		
	def play_death_sound(self):
		if self.map.startswith("zombie2") and self.matchteam=="blue":
			self.playsound("zombiedie")
		else: self.playsound(self.get_current_char()+"voice17")
		
	def get_item_count(self,item):
	
		if not item in self.inv:
		
			return 0
			
		ret=0
		ret=self.inv[item]
		if(ret<0):
		
			del self.inv[item]
			return 0
			
		return ret
		
#	def give(self,item,amount):
#	
#		a=0
#		if not item in self.inv:
#		
#			self.inv[item]=amount
#			
#		else:
#		
#			a=self.inv[item]
#			if (a+amount<=0):
#				del self.inv[item]
#			else:
#			
#				self.inv[item]=a+amount
#				
#			data=pickle.dumps(self.inv)
#			self.cachedinv=data
#			g.send_reliable(self.peer_id,data,19)
#			
#		
	def give(self, item, amount):
		if item==-1 or item=="-1": return
		a = 0
		if item not in self.inv:
			self.inv[item] = amount
		else:
			a = self.inv[item]
			if a + amount <= 0:
				del self.inv[item]
			else:
				self.inv[item] = a + amount

			data = pickle.dumps(self.inv)
			self.cachedinv = data
			g.send_reliable(self.peer_id, data, 19)
		self.neg_inv_check()
	def neg_inv_check(self):
		k=self.inv.keys()
		for i in k:
			v=0
			v=self.inv[i]
			if v<=0:
				del self.inv[i]
				return
	def storeget_item_count(self,item):
	
		if not item in self.storeinv:
		
			return 0
			
		ret=0
		ret=self.storeinv[item]
		if(ret<0):
		
			del self.storeinv[item]
			return 0
			
		return ret
		
	def storegive(self, item, amount):
		a = 0
		if item not in self.storeinv:
			self.storeinv[item] = amount
		else:
			a = self.storeinv[item]
			if a + amount <= 0:
				del self.storeinv[item]
			else:
				self.storeinv[item] = a + amount

		self.storeneg_inv_check()
	def storeneg_inv_check(self):
		k=self.storeinv.keys()
		for i in k:
			v=0
			v=self.storeinv[i]
			if v<=0:
				del self.storeinv[i]
				return


	def get_ammo_count_from(self,we):
	
		amount=0
		for i in range(len(self.ammo.keys())):
		
			a=0
			if (list(self.ammo.keys())[i]==we):
				a=self.ammo[we]
			amount+=a
			
		return amount
		
	def get_ammo_count(self,w):
	
		return self.get_ammo_count_from(w)
		
	def ammocheck(self,item):
	
		if(item not in self.ammo):
		
			return 0
			
		ret=0
		ret=self.ammo[item]
		if(ret<0):
		
			del self.ammo[item]
			return 0
			
		return ret
		
	def ammogive(self,item,amount):
	
		a=0
		if not item in self.ammo:
		
			self.ammo[item]=amount
			
		else:
		
			a=self.ammo[item]
			if (a+amount<=0):
				del self.ammo[item]
			else:
			
				self.ammo[item]=a+amount
				
			
		
	
	def msoundloop(self):
		for i in range(len(self.msoundtimers)):
			if self.msoundtimers[i].elapsed>=9000:
				self.msoundtimers[i].restart()
				destroy_moving_sound(self.msounds[i])
				self.msoundtimers.remove(self.msoundtimers[i])
				self.msounds.remove(self.msounds[i])
				return
		if self.x!=self.oldx or self.y!=self.oldy or self.z!=self.oldz:
			for i in range(len(self.msounds)):
				update_moving_sound(self.msounds[i],self.x,self.y,self.z,self.map)
			self.oldx=self.x
			self.oldy=self.y
			self.oldz=self.z
def playerloop():
	seen_names = set()
	duplicates = []
	for i in range(len(g.players)):
		try:
			p_name = g.players[i].name
			if p_name in seen_names:
				duplicates.append(i)
			else:
				seen_names.add(p_name)
		except:
			continue
	if len(duplicates) > 0:
		for i in sorted(duplicates, reverse=True):
			g.remove_from_server(i, True)
	for i in range(len(g.players)):
		try: g.players[i]
		except: return

		g.players[i].bought_chars=list(dict.fromkeys(g.players[i].bought_chars))
		if g.players[i].current_char not in g.players[i].bought_chars: g.players[i].current_char="tristan"; g.players[i].get_char_properties()
		if "android" in os.getcwd() and g.players[i].droidtimer.elapsed>5000 and g.players[i].android==False and g.players[i].ios==False and g.players[i].is_admin()==False:
			g.remove_from_server(i)
		g.players[i].friendloop()
		if not g.players[i].shielded and g.players[i].shieldhitchance>0: g.players[i].shielded=True

		if g.players[i].health<=0 and g.players[i].map=="lobby": g.players[i].health=g.players[i].maxhealth
		if g.players[i].spatialized_by!="" and g.players[i].spatializertimer.elapsed>600000: g.players[i].spatialized_by=""
		if g.players[i].backpacktimer.elapsed>604800000 and g.players[i].backpacks_level!=0:
			g.players[i].backpacks_level=0
			g.n.send_reliable(g.players[i].peer_id,"Backpack level "+str(g.players[i].backpacks_level)+" expired. You may lose items!",2); return


		if g.players[i].adrenaline and g.players[i].adrenalinetimer.elapsed>120000:
			g.players[i].adrenaline=False
			g.players[i].playsound("get_adreline_shot")
			g.n.send_reliable(g.players[i].peer_id,"adrenaline shot time expired",2)
			import db as _db; _db.chardelete(g.players[i].name,"adrenaline")
			if g.players[i].weapon!="": 					g.n.send_reliable(g.players[i].peer_id,"weapondata "+g.wdata[g.players[i].weapon],0)
			if g.players[i].weapon2!="": 					g.n.send_reliable(g.players[i].peer_id,"weapondata2 "+g.wdata[g.players[i].weapon2],0)

		if g.players[i].jammer and g.players[i].jammertimer.elapsed>120000:
			g.players[i].jammer=False
			g.n.send_reliable(g.players[i].peer_id,"jammer time expired",2)
			g.players[i].playsound("misc45")
			import db as _db; _db.chardelete(g.players[i].name,"jammer")

		for sw in g.players[i].silenced:
			if g.players[i].get_item_count(sw)<=0: g.players[i].silenced.remove(sw)
		if g.players[i].freedomhelicopter and g.players[i].map=="helicopter":
			g.players[i].helicopterloop()
			g.players[i].heliendloop()
		if not g.players[i].dead and  not g.players[i].stunned:
			for e in g.electrics:
				if e.z==round(g.players[i].z)-5 and e.x==round(g.players[i].x) and e.y==round(g.players[i].y) and e.map==g.players[i].map:
					g.players[i].playsound("electrictyhit")
					g.players[i].hitby="electric pole"
					g.players[i].health=0
					g.players[i].hitby2="electric pole"

		if not g.rain and g.players[i].rain:
			g.players[i].rain=False
			g.n.send_reliable(g.players[i].peer_id,"rainstop",0)
		if g.rain and not g.players[i].rain:
			g.players[i].rain=True
			g.n.send_reliable(g.players[i].peer_id,"rainstart",0)
		if not g.rainfinish and g.players[i].rainfinish:
			g.players[i].rainfinish=False
			g.n.send_reliable(g.players[i].peer_id,"rainfinishstop",0)
		if g.rainfinish and not g.players[i].rainfinish:
			g.players[i].rainfinish=True
			g.n.send_reliable(g.players[i].peer_id,"rainfinishstart",0)

		if g.players[i].rainvolume!=g.rainvolume:
			g.players[i].rainvolume=g.rainvolume
			g.n.send_reliable(g.players[i].peer_id,"rainvolume "+str(g.players[i].rainvolume),0)
		if g.players[i].drawing and g.players[i].drawtimer.elapsed>g.players[i].drawtime:
			g.players[i].drawing=False
		if g.players[i].sitting and g.players[i].sitregentimer.elapsed>1000 and g.players[i].health>0 and g.players[i].faint==False and g.players[i].fainted==False:
			g.players[i].sitregentimer.restart()
			if g.players[i].health<g.players[i].maxhealth: g.players[i].health+=random(2,3)
		if g.players[i].helmeted: g.players[i].lasthelmethitchance=g.players[i].helmethitchance
		if g.players[i].health<=50 and g.players[i].health>0:
			if g.players[i].flashvolume!=g.players[i].health:
				g.players[i].flashvolume=g.players[i].health
				g.n.send_reliable(g.players[i].peer_id,"flashvolume -"+str(g.players[i].flashvolume),0)
		if g.players[i].health>50 or g.players[i].health<=0:
			if g.players[i].flashvolume!=100:
				g.players[i].flashvolume=100
				g.n.send_reliable(g.players[i].peer_id,"flashvolume -100",0)
		if g.players[i].blockoffline and g.players[i].blockofflinetimer.elapsed>120000:
			g.players[i].blockofflinetimer.restart()
			g.remove_from_server(i,True)
			return
		if g.players[i].invisible and g.players[i].invisibletimer.elapsed>15000:
			g.players[i].invisibletimer.restart()
			g.players[i].invisible=False
			g.players[i].playsoundmoving("invisibility_stop")
		if g.players[i].chest is not None and g.players[i].chest not in g.chests: g.players[i].chest=None
		if g.players[i].corpse is not None and g.players[i].corpse not in g.corpses: g.players[i].corpse=None
		if g.players[i].placebarricade==True and g.players[i].placebarricadetimer.elapsed>=2000:
			g.players[i].placebarricade=False
			facing=getdir(g.players[i].facing)
			mx=g.players[i].px; my=g.players[i].py; mz=g.players[i].pz
			if facing==north: my+=1
			elif facing==northeast: my+=1; mx+=1
			elif facing==east: mx+=1
			elif facing==southeast: my-=1; mx+=1
			elif facing==south: my-=1
			elif facing==southwest: my-=1; mx-=1
			elif facing==west: mx-=1
			elif facing==northwest: my+=1; mx-=1

			if g.players[i].map!="lobby": place_barricade(mx,my,mz,g.players[i].map,g.players[i].name)
			g.players[i].placebarricadetimer.restart()
			g.n.send_reliable(g.players[i].peer_id,"startmoving",0)
			g.players[i].stunned=False
			g.players[i].stuntime=0
			g.players[i].stuntimer.restart()
		if g.players[i].placeladder==True and g.players[i].placeladdertimer.elapsed>=5200:
			g.players[i].placeladder=False
			facing=getdir(g.players[i].facing)
			mx=g.players[i].px; my=g.players[i].py; mz=g.players[i].pz
			if facing==north: my+=1
			elif facing==northeast: my+=1; mx+=1
			elif facing==east: mx+=1
			elif facing==southeast: my-=1; mx+=1
			elif facing==south: my-=1
			elif facing==southwest: my-=1; mx-=1
			elif facing==west: mx-=1
			elif facing==northwest: my+=1; mx-=1

			place_ladder(mx,my,mz,g.players[i].map,g.players[i].name)
			g.players[i].placeladdertimer.restart()
			g.n.send_reliable(g.players[i].peer_id,"startmoving",0)
			g.players[i].stunned=False
			g.players[i].stuntime=0
			g.players[i].stuntimer.restart()

		if g.players[i].jailed and g.players[i].map!="jail": g.move_player(i,0,0,0,"jail")
		if g.players[i].jailed and g.players[i].jailtimer.elapsed>g.players[i].jailtime:
			g.players[i].jailed=False
			g.players[i].jailtimer.restart()
			g.players[i].jailreason=""
			g.move_player(i,5,0,0,"lobby")
			import db as _db
			_db.chardelete(g.players[i].name,"jailtime"); _db.chardelete(g.players[i].name,"jailreason"); _db.chardelete(g.players[i].name,"jailtimestamp")
		if g.players[i].jailed==False and g.players[i].map=="jail":
			g.players[i].jailed=False
			g.players[i].jailtimer.restart()
			g.players[i].jailreason=""
			g.move_player(i,5,0,0,"lobby")
			import db as _db
			_db.chardelete(g.players[i].name,"jailtime"); _db.chardelete(g.players[i].name,"jailreason"); _db.chardelete(g.players[i].name,"jailtimestamp")
		if 1:
			g.players[i].group=""
			for grp in g.groups:
				if g.players[i].name in grp.members:
					g.players[i].group=grp.name;
					if not g.players[i].ingroup: g.players[i].ingroup=True; g.n.send_reliable(g.players[i].peer_id,"ingroup",0)
			if g.players[i].ingroup and g.players[i].group=="": g.n.send_reliable(g.players[i].peer_id,"notingroup",0); g.players[i].ingroup=False
			g.players[i].community=""
			for grp in g.communitys:
				if g.players[i].name in grp.members:
					g.players[i].community=grp.name;
					if not g.players[i].incommunity: g.players[i].incommunity=True; g.n.send_reliable(g.players[i].peer_id,"incommunity",0)
			if g.players[i].incommunity and g.players[i].community=="": g.n.send_reliable(g.players[i].peer_id,"notincommunity",0); g.players[i].incommunity=False


		items=list(g.players[i].inv.keys())
		for item in items:
			if item=="hand_grenade" and ("grenade" in g.players[i].map or "abyss_clash" in g.players[i].map): continue
			if item in g.invlimits and g.players[i].get_item_count(item)>g.players[i].get_backpack_level_amount(g.invlimits[item]): g.players[i].give(item,-1)
		if g.players[i].shielded==True and g.players[i].map=="lobby":
			g.players[i].shielded=False
			g.players[i].shieldchance=0
		if g.players[i].shielded==True and g.players[i].shieldhitchance<=0:
			g.players[i].shielded=False
			g.players[i].shieldhitchance=0
			scount=random(1,2)
			if scount==1: g.players[i].playsoundmoving("shieldbreak3")
			if scount==2: g.players[i].playsoundmoving("shieldbreak1")
			for p in g.players:
				if get_3d_distance(g.players[i].x,g.players[i].y,g.players[i].z,p.x,p.y,p.z)<=40 and g.players[i].map==p.map:
					if p.name==g.players[i].name:
						continue
					if g.players[i].hidden: continue
					g.n.send_reliable(p.peer_id,"distsound shieldbreakdist1 "+str(g.players[i].x)+" "+str(g.players[i].y)+" "+str(g.players[i].z)+" "+str(g.players[i].map),0)

		if g.players[i].helmeted==True and g.players[i].helmethitchance<=0:
			g.players[i].helmeted=False
			g.players[i].helmethitchance=0
			g.players[i].playsound("helmetbreak")
			g.players[i].give("steel_helmet",-1)
		if g.players[i].placetimebomb==True and g.players[i].placetimebombtimer.elapsed>=2000:
			g.players[i].placetimebomb=False
			if g.players[i].map!="lobby": place_timebomb(g.players[i].x,g.players[i].y,g.players[i].z,g.players[i].map,g.players[i].name)
			g.players[i].placetimebombtimer.restart()
			g.n.send_reliable(g.players[i].peer_id,"The countdown has started!",2)
			g.n.send_reliable(g.players[i].peer_id,"startmoving",0)
			g.players[i].stunned=False
			g.players[i].stuntime=0
			g.players[i].stuntimer.restart()
		if g.players[i].placemine==True and g.players[i].placeminetimer.elapsed>=2000:
			g.players[i].placemine=False
			if g.players[i].map!="lobby": place_mine(g.players[i].tx,g.players[i].ty,g.players[i].tz,g.players[i].map,g.players[i].name)
			g.players[i].placeminetimer.restart()
			g.n.send_reliable(g.players[i].peer_id,"startmoving",0)
			g.players[i].stunned=False
			g.players[i].stuntime=0
			g.players[i].stuntimer.restart()

		if g.players[i].matchteam!="" and g.players[i].map=="massacre_in_the_city": g.players[i].matchteam=""
		if g.players[i].respawn and g.players[i].respawntimer.elapsed>3500:
			g.players[i].respawntimer.restart()
			g.players[i].respawn=False
			g.n.send_reliable(g.players[i].peer_id,"sitstop",0)
			dname=g.players[i].name
			g.send_reliable(g.players[i].peer_id,"notdied",0)
			if 1:
				#g.send_reliable(g.players[i].peer_id,"startmoving",0)
#				g.players[g.get_player_index_from(dname)].give("mkek_yavuz16",1)
#				g.players[g.get_player_index_from(dname)].give("9mm",39)
				_rdname_idx = g.get_player_index_from(dname)
				if "basement" not in g.players[_rdname_idx].map and g.players[_rdname_idx].map != "megaboss":
					g.players[_rdname_idx].randomweapongive()
					g.players[_rdname_idx].give("vitality_potion",1)
					g.players[_rdname_idx].give("revival_nectar",1)
					g.players[_rdname_idx].give("parachute",1)
				elif g.players[_rdname_idx].map == "megaboss":
					g.players[_rdname_idx].give("dragunov_psl",1)
					g.players[_rdname_idx].give("mkek_jng90",1)
					g.players[_rdname_idx].give("7.62x51mm",250)
					g.players[_rdname_idx].give("mkek_mpt76k",1)
					g.players[_rdname_idx].give("5.56x45mm",400)
					g.players[_rdname_idx].give("berettaM9",1)
					g.players[_rdname_idx].give("9mm",150)
					g.players[_rdname_idx].give("vitality_potion",4)
					g.players[_rdname_idx].give("revival_nectar",2)
				index=g.get_player_index_from(dname)
				g.players[index].health=g.players[index].maxhealth
				g.n.send_reliable(g.players[index].peer_id,"sitstop",0)
				g.players[index].dead=False
				if "basement" not in g.players[index].map and g.players[index].matchmode!="teamc" and g.players[index].map!="massacre_in_the_city" and g.players[index].map!="megaboss":
					for m in g.matches:
						if m.owner==g.players[index].joinedmatch:
							g.players[index].map="lobby"
							g.players[index].x=5
							g.players[index].y=0
							g.move_player(index, random(5, 5), random(0, 0), 0, "lobby")
				else:
					if g.players[index].map=="megaboss":
						if getattr(g,"mega_boss_alive",False):
							g.move_player(index,100,100,0,"megaboss")
						else:
							g.move_player(index,random(5,5),random(0,0),0,"lobby")
					elif "basement" in g.players[index].map:
						g.move_player(index,random(5,5),random(0,0),0,"lobby")
					elif g.players[index].map=="massacre_in_the_city":
						g.n.send_reliable(g.players[index].peer_id,"stopmoving",0)
						g.n.send_reliable(g.players[index].peer_id,"play_s helicopterstart.ogg",0)

						g.players[index].stunned=True
						g.players[index].stuntime=1500
						g.players[index].stuntimer.restart()
						g.players[index].dead=True
						g.players[index].x=random(0,500)
						g.players[index].y=random(0,500)
						g.players[index].z=random(1,1)

						g.players[index].map="helicopter"
						g.players[index].freedomhelicopter=True
						g.players[index].freedomhelicoptertimer.restart()
						g.players[index].helijumptimer.restart()


						delay(1500)
						index=g.get_player_index_from(dname)
						g.players[index].dead=False
						g.move_player(index,g.players[index].x,g.players[index].y,0,"helicopter")
						if not g.players[index].hidden:
							for p in g.players:
								if p.name!=g.players[index].name: g.n.send_reliable(p.peer_id,"distsound helicopterdist "+str(g.players[index].x)+" "+str(g.players[index].y)+" "+str(g.players[index].z)+" massacre_in_the_city",0)
					if "flag" in g.players[index].map: g.move_player(index, random(0, 100), random(0, 100), 0, "flag"+g.players[index].joinedmatch)

				g.n.send_reliable(g.players[index].peer_id,"startmoving",0)
			

		try: g.players[i]
		except: return
		if g.players[i].faint and g.players[i].fainttimer.elapsed>60000:
			p=g.players[i]
			p.faint=False
			p.fainted=False
			g.n.send_reliable(p.peer_id,"startmoving",0)
			g.play(p.get_current_char()+"voice32",p.x,p.y,p.z,p.map)
		if g.players[i].cannotexit and g.players[i].cannotexittimer.elapsed>1000:
			g.players[i].cannotexit=False
		if "flag" not in g.players[i].map and g.players[i].flag>0: g.players[i].flag=0
		if g.players[i].lobytimer.elapsed>1000 and g.players[i].map=="lobby" and g.players[i].z<0:
			g.move_player(i,5,0,0,"lobby")
			g.players[i].lobytimer.restart()
		if g.players[i].freedomtimer.elapsed>1000 and g.players[i].map=="massacre_in_the_city" and g.players[i].z<-100:
			g.move_player(i,g.players[i].x+1,g.players[i].y+1,-95,g.players[i].map)
			g.players[i].freedomtimer.restart()
		if g.players[i].flagtimer.elapsed>1000 and "flag" in g.players[i].map and g.players[i].z<0:
			g.move_player(i,g.players[i].x+1,g.players[i].y+1,0,g.players[i].map)
			g.players[i].flagtimer.restart()


		if g.players[i].basetimer.elapsed>1000 and "basement" in g.players[i].map and g.players[i].z<0:
			g.move_player(i,0,0,1,g.players[i].map)
			g.players[i].basetimer.restart()

		if g.players[i].stunned==True and g.players[i].stuntimer.elapsed>=g.players[i].stuntime:
			g.players[i].stunned=False
			g.players[i].stuntimer.restart()
			g.players[i].stuntime=0
			g.n.send_reliable(g.players[i].peer_id,"startmoving",0)

		if g.players[i].grenadepin and g.players[i].grenadepintimer.elapsed>4000:
			try:
				launch_grenade(g.players[i].x, g.players[i].y, g.players[i].z, g.players[i].map, g.players[i], g.players[i].facing)
				g.grenades[len(g.grenades)-1].explodetimer.elapsed=g.players[i].grenadepintimer.elapsed
			except: pass
			g.players[i].grenadepin=False
			g.players[i].give("hand_grenade",-1)

		if g.players[i].map!="lobby":
			g.players[i].wx=g.players[i].x
			g.players[i].wy=g.players[i].y
			g.players[i].wz=g.players[i].z
		if not g.players[i].inve: g.players[i].vi=-1
		if g.players[i].vi==-1: g.players[i].inve=False
		if g.players[i].inve:
			for ind, m in enumerate(g.motors):
				if g.players[i].name in m.players: g.players[i].vi=ind
		if g.players[i].filechecktimer.elapsed>1000:
			g.players[i].filechecktimer.restart()
			if g.players[i].get_item_count(-1)>0: g.players[i].give(-1,-100)
			if g.players[i].get_item_count("corpse_bomb")<=0 and g.players[i].corpse_bomb: g.players[i].corpse_bomb=False
			try:
				import db as _db
				if g.players[i].paid and time.time()-int(_db.charread(g.players[i].name,"paidtime","0"))>=g.players[i].paidmonths:
					g.players[i].paid=False
					g.n.send_reliable(g.players[i].peer_id,"your paid account is expired",2)
					_db.charwrite(g.players[i].name,"paid",0); _db.chardelete(g.players[i].name,"paidtime"); _db.chardelete(g.players[i].name,"paidmonths")
			except: pass
			if g.players[i].get_item_count("shield")<=0 and g.players[i].shielded:
				g.players[i].shielded=False; g.players[i].shieldchance=0

			for pl in list(g.players[i].tokenplayers.keys()):
				if g.players[i].tokenplayers[pl].elapsed>300000:
					del g.players[i].tokenplayers[pl]
			if g.players[i].helmeted and g.players[i].get_item_count("steel_helmet")<=0:
				g.players[i].helmethitchance=0
				g.players[i].helmeted=False
			g.players[i].disable_public_chat_check2()
			g.players[i].disable_team_chat_check2()
			g.players[i].disable_pm_chat_check2()

			g.players[i].disable_group_chat_check2()
			g.players[i].disable_map_chat_check2()
			g.players[i].disable_all_chat_check2()
			found=False
			for p in g.npcs:
				if p.name!=g.players[i].name and p.map==g.players[i].map and g.players[i].distancecheck(p.x,p.y,p.z)<=50:
					if not g.players[i].near:
						g.players[i].near=True
						g.n.send_reliable(g.players[i].peer_id,"near",0)
					found=True
					return
			for p in g.players:
				if g.get_hidden_area_at(p.x, p.y, p.z, p.map)!=g.get_hidden_area_at(g.players[i].x, g.players[i].y, g.players[i].z, g.players[i].map): continue
				if g.players[i].map=="helicopter" or g.players[i].map=="jail" or "base" in g.players[i].map: continue
				if g.players[i].group!="" and p.group!="" and g.players[i].map==p.map and ("base" in g.players[i].map or g.players[i].map=="massacre_in_the_city") and p.group==g.players[i].group and g.get_group(g.players[i].group).freedomhit==0: continue
				if p.name!=g.players[i].name and p.map==g.players[i].map and g.players[i].distancecheck(p.x,p.y,p.z)<=50:
					if not g.players[i].near:
						g.players[i].near=True
						g.n.send_reliable(g.players[i].peer_id,"near",0)
					found=True
					return

			if not found and g.players[i].near:
				g.players[i].near=False
				g.n.send_reliable(g.players[i].peer_id,"notnear",0)
			if g.players[i].lang=="": g.players[i].lang="english"
			if g.players[i].map=="helicopter" and g.players[i].freedomhelicopter==False:
				g.move_player(i,5,0,0,"lobby")

			if g.players[i].map!="helicopter" and g.players[i].map.startswith("helicopter"):
				owner=g.players[i].map.replace("helicopter","").replace(".map","")
				found=False
				for m in g.matches:
					if m.owner==owner: found=True
				if not found:
					g.move_player(i,5,0,0,"lobby")
			elif g.players[i].map.startswith("match"):
				owner=g.players[i].map.replace("match","").replace(".map","")
				found=False
				for m in g.matches:
					if m.owner==owner: found=True
				if not found:
					g.move_player(i,5,0,0,"lobby")
			elif g.players[i].map.startswith("abyss_clash"):
				owner=g.players[i].map.replace("abyss_clash","").replace(".map","")
				found=False
				for m in g.matches:
					if m.owner==owner: found=True
				if not found:
					g.move_player(i,5,0,0,"lobby")
			elif g.players[i].map.startswith("sword"):
				owner=g.players[i].map.replace("sword","").replace(".map","")
				found=False
				for m in g.matches:
					if m.owner==owner: found=True
				if not found:
					g.move_player(i,5,0,0,"lobby")
			elif g.players[i].map.startswith("collect"):
				owner=g.players[i].map.replace("collect","").replace(".map","")
				found=False
				for m in g.matches:
					if m.owner==owner: found=True
				if not found:
					g.move_player(i,5,0,0,"lobby")


			elif g.players[i].map.startswith("snow"):
				owner=g.players[i].map.replace("snow","").replace(".map","")
				found=False
				for m in g.matches:
					if m.owner==owner: found=True
				if not found:
					g.move_player(i,5,0,0,"lobby")

			elif g.players[i].map.startswith("one_shot_one_kill"):
				owner=g.players[i].map.replace("one_shot_one_kill","").replace(".map","")
				found=False
				for m in g.matches:
					if m.owner==owner: found=True
				if not found:
					g.move_player(i,5,0,0,"lobby")




			elif g.players[i].map.startswith("main"):
				owner=g.players[i].map.replace("main","").replace(".map","")
				found=False
				for m in g.matches:
					if m.owner==owner: found=True
				if not found:
					g.move_player(i,5,0,0,"lobby")
			elif g.players[i].map.startswith("knife"):
				owner=g.players[i].map.replace("knife","").replace(".map","")
				found=False
				for m in g.matches:
					if m.owner==owner: found=True
				if not found:
					g.move_player(i,5,0,0,"lobby")
			elif g.players[i].map.startswith("combo"):
				owner=g.players[i].map.replace("knife","").replace(".map","")
				found=False
				for m in g.matches:
					if m.owner==owner: found=True
				if not found:
					g.move_player(i,5,0,0,"lobby")

			elif g.players[i].map.startswith("zombie2"):
				owner=g.players[i].map.replace("zombie2","").replace(".map","")
				found=False
				for m in g.matches:
					if m.owner==owner: found=True
				if not found:
					g.move_player(i,5,0,0,"lobby")
			elif g.players[i].map.startswith("zombie"):
				owner=g.players[i].map.replace("zombie","").replace(".map","")
				found=False
				for m in g.matches:
					if m.owner==owner: found=True
				if not found:
					g.move_player(i,5,0,0,"lobby")
			elif g.players[i].map.startswith("grenade"):
				owner=g.players[i].map.replace("grenade","").replace(".map","")
				found=False
				for m in g.matches:
					if m.owner==owner: found=True
				if not found:
					g.move_player(i,5,0,0,"lobby")
			elif g.players[i].map.startswith("flag"):
				owner=g.players[i].map.replace("flag","").replace(".map","")
				found=False
				for m in g.matches:
					if m.owner==owner: found=True
				if not found:
					g.move_player(i,5,0,0,"lobby")

			if g.players[i].map=="lobby": g.players[i].killcount=0
			g.players[i].zombie=g.players[i].matchteam=="blue" and g.players[i].map.startswith("zombie2")
			if g.players[i].get_item_count(-1)>0: g.players[i].give(-1,-1)
			if g.players[i].map=="lobby": g.players[i].ammo.clear()
			if not file_exists("maps/"+g.players[i].map+	".map"): g.move_player(i,5,0,0,"lobby")
			for t in g.timeditemlist:
				if g.players[i].weapon==t:
					found=False
					for t2 in g.timeditems:
						if t2.owner==g.players[i].name and t2.itemname==t: found=True; break
					if not found: new_timeditem(g.players[i].name,g.players[i].weapon,get_timeditem_duration(g.players[i].weapon))
		g.players[i].msoundloop()

		# Navigation Assist: run the 6-direction wall scanner only when the
		# player has moved to a different integer tile since the last scan.
		_nav_pos = (round(g.players[i].x), round(g.players[i].y), round(g.players[i].z))
		if _nav_pos != g.players[i].last_scan_pos:
			g.players[i].last_scan_pos = _nav_pos
			try:
				update_nav_scanner(g.players[i])
			except Exception as _nav_err:
				try:
					file_put_contents("errors.log", "nav_scanner error: {}\n".format(_nav_err), "a")
				except Exception:
					pass

		if g.players[i].rankchecktimer.elapsed>=2000:
			g.players[i].rankchecktimer.restart()
			g.players[i].check_rank()
			if g.players[i].specmatch!="" and not g.match_exists(g.players[i].specmatch):
				g.players[i].specplayer=""
				g.players[i].specmatch=""
				g.players[i].specmap=""
				g.n.send_reliable(g.players[i].peer_id,"matchwatchstop",0)
				g.move_player(i,5,0,0,"lobby")
			if g.players[i].specplayer!="" and g.players[i].health<=0: g.players[i].health=100
			if g.get_player_index_fromnpc(g.players[i].specplayer)==-1 and g.players[i].specplayer!="":
				for m in g.matches:
					if not g.players[i].watchingfreedom and m.owner==g.players[i].specmatch:
						g.players[i].specplayer=m.players[0]
						g.n.send_reliable(g.players[i].peer_id,"matchwatch "+m.players[0],0)
						return
				for p in g.players:
					if not p.hidden and p.name in g.players[i].friendlist and g.players[i].watchingfreedom and (p.map=="helicopter" or p.map=="massacre_in_the_city"):
						g.players[i].specplayer=p.name
						g.n.send_reliable(g.players[i].peer_id,"matchwatch "+p.name,0)
						g.n.send_reliable(g.players[i].peer_id,"mapname "+p.map,0)
						return
				g.players[i].specplayer=""
				g.players[i].specmatch=""
				g.players[i].specmap=""
				g.n.send_reliable(g.players[i].peer_id,"matchwatchstop",0)
				g.move_player(i,5,0,0,"lobby")
			if g.get_player_index_fromnpc(g.players[i].specplayer)>-1 and g.players[i].specplayer!="" and (g.getpc(g.players[i].specplayer).hidden or g.getpc(g.players[i].specplayer).map=="lobby"):
				for m in g.matches:
					if not g.players[i].watchingfreedom and m.owner==g.players[i].specmatch:
						g.players[i].specplayer=m.players[0]
						g.n.send_reliable(g.players[i].peer_id,"matchwatch "+m.players[0],0)
						return
				for p in g.players:
					if p.name in g.players[i].friendlist and g.players[i].watchingfreedom and (p.map=="helicopter" or p.map=="massacre_in_the_city"):
						g.players[i].specplayer=p.name
						g.n.send_reliable(g.players[i].peer_id,"matchwatch "+p.name,0)
						g.n.send_reliable(g.players[i].peer_id,"mapname "+p.map,0)
						return
				g.players[i].specplayer=""
				g.players[i].specmatch=""
				g.players[i].specmap=""
				g.n.send_reliable(g.players[i].peer_id,"matchwatchstop",0)
				g.move_player(i,5,0,0,"lobby")
		if g.players[i].specplayer!="" and g.getpc(g.players[i].specplayer) is not None: g.players[i].specmap=g.getpc(g.players[i].specplayer).map
		if g.players[i].specplayer!="" and g.getpc(g.players[i].specplayer) is None: g.players[i].specmap=""
		if "collect" not in g.players[i].map and not g.players[i].jammer and not g.players[i].dead and g.players[i].weaponbeeptimer2.elapsed>=150 and g.players[i].scope==1 and g.players[i].weapon2!="" and g.players[i].map!="lobby" and not g.players[i].map.startswith("match"):
			g.players[i].weaponbeeptimer2.restart()
			# Pre-calculate weapon ray positions
			if g.players[i].weapon_rays is None:
				g.players[i].weapon_rays=[]
				if g.players[i].aim_mode==1: wr = vector(g.players[i].x, g.players[i].y, g.players[i].z)
				if g.players[i].aim_mode==0: wr = vector(g.players[i].x, g.players[i].y, g.players[i].z+g.players[i].aim)
				for x2 in range(get_weapon_range(g.players[i].weapon2)):
					wr = move(wr.x, wr.y, wr.z, g.players[i].facing, 0, 0, 0)
					if g.players[i].aim_mode==1:
						if g.players[i].aim==2 or g.players[i].aim==1: wr.z+=1
						if g.players[i].aim==-2 or g.players[i].aim==-1: wr.z-=1

					if g.players[i].aim_mode==1 and g.players[i].aim==-2 or g.players[i].aim_mode==1 and g.players[i].aim==2: g.players[i].weapon_rays.append(vector(g.players[i].x,g.players[i].y, wr.z))
					else: g.players[i].weapon_rays.append(vector(wr.x,wr.y, wr.z))

			# Check walls
			for wall in g.maps[g.get_map_index(g.players[i].map)].mapwalls:
				if wall.health <= 0: continue
				for wr in g.players[i].weapon_rays:
					for wx in range(wall.minx, wall.maxx + 1):
						for wy in range(wall.miny, wall.maxy + 1):
							for wz in range(wall.minz, wall.maxz + 1):
								if get_3d_distance(wr.x, wr.y, wr.z, wx, wy, wz) <= (get_weapon_spread(g.players[i].weapon2) if g.players[i].aim==0 else get_weapon_spread(g.players[i].weapon2)-1):
									g.n.send_reliable(g.players[i].peer_id, "play_s botbeacon.ogg", 0)
									g.players[i].play_watch_scope()
									return

			# Check players
			for x in range(len(g.players)):
				if g.get_hidden_area_at(g.players[i].x,g.players[i].y,g.players[i].z,g.players[i].map)!=g.get_hidden_area_at(g.players[x].x,g.players[x].y,g.players[x].z,g.players[x].map): continue
				if g.players[x].dead or g.players[x].health<=0 or g.players[x].invisible or g.players[x].hidden: continue
				if ("base" in g.players[x].map or g.players[x].map=="massacre_in_the_city") and g.get_group(g.players[x].group) is not None and g.players[x].group==g.players[i].group and g.get_group(g.players[x].group).freedomhit==0: continue
				if g.players[x].faint: continue
				if g.players[x].vi == g.players[i].vi and g.players[i].vi != -1 and g.players[x].vi != -1: continue
				if g.players[x].map != g.players[i].map or g.players[x].health <= 0: continue
				if g.players[x].ducking and g.players[i].aim > -(get_weapon_spread(g.players[i].weapon2) if g.players[i].aim==0 else get_weapon_spread(g.players[i].weapon2)-1) and not g.players[i].ducking: continue
				if g.players[x].name == g.players[i].name: continue
				if g.players[x].joinedmatch == g.players[i].joinedmatch and g.players[i].joinedmatch != "" and g.players[x].matchteam == g.players[i].matchteam and g.players[i].matchmode not in ["teaml", "teamk2", "teamf", "snow", "sniper", "minecraft", "g", "collect", "g2", "sword"] and g.players[x].joinedmatch != "" and g.players[x].matchmode != "" and g.players[i].matchmode != "": continue
				
				first_ray = g.players[i].weapon_rays[0]  # Use first ray position for initial checks
				if g.players[x].matchmode == "teamz" and g.players[i].joinedmatch == g.players[x].joinedmatch and g.get_tile_at(first_ray.x, first_ray.y, 0, g.players[i].map) != "hardwood": continue
				
				for wr in g.players[i].weapon_rays:
					if get_3d_distance(wr.x, wr.y, wr.z, g.players[x].x, g.players[x].y, g.players[x].z) <= (get_weapon_spread(g.players[i].weapon2) if g.players[i].aim==0 else get_weapon_spread(g.players[i].weapon2)-1):
						if not has_line_of_sight(wr.x,wr.y,wr.z,g.players[x].x,g.players[x].y,g.players[x].z,g.players[x].map): break
						g.n.send_reliable(g.players[i].peer_id, "play_s botbeacon.ogg", 0)
						g.players[i].play_watch_scope()
						return

			# Check NPCs
			for x in range(len(g.npcs)):
				if g.npcs[x].faint: continue
				if g.npcs[x].joinedmatch == g.players[i].joinedmatch and g.npcs[x].matchteam == g.players[i].matchteam and g.players[i].matchmode not in ["teaml", "teamk2", "teamf2", "snow", "sniper", "minecraft", "sword", "collect", "g", "g2"] and g.players[i].joinedmatch != "": continue
				if g.npcs[x].map != g.players[i].map or g.npcs[x].health <= 0: continue
				
				first_ray = g.players[i].weapon_rays[0]
				if g.npcs[x].matchmode == "teamz" and g.players[i].joinedmatch == g.npcs[x].joinedmatch and g.get_tile_at(first_ray.x, first_ray.y, 0, g.players[i].map) != "hardwood": continue
				
				for wr in g.players[i].weapon_rays:
					if get_3d_distance(wr.x, wr.y, wr.z, g.npcs[x].x, g.npcs[x].y, g.npcs[x].z) <= (get_weapon_spread(g.players[i].weapon2) if g.players[i].aim==0 else get_weapon_spread(g.players[i].weapon2)-1):
						g.n.send_reliable(g.players[i].peer_id, "play_s botbeacon.ogg", 0)
						g.players[i].play_watch_scope()
						return

			# Check motors
			for x in range(len(g.motors)):
				oi = g.get_player_index_from(g.motors[x].owner)
				if oi > -1 and g.players[oi].matchteam != "" and g.players[oi].matchteam == g.players[i].matchteam: continue
				if len(g.motors[x].players) != 0: continue
				if g.motors[x].map != g.players[i].map or g.motors[x].health <= 0: continue
				
				for wr in g.players[i].weapon_rays:
					if get_3d_distance(wr.x, wr.y, wr.z, g.motors[x].x, g.motors[x].y, g.motors[x].z) <= (get_weapon_spread(g.players[i].weapon2) if g.players[i].aim==0 else get_weapon_spread(g.players[i].weapon2)-1):
						g.n.send_reliable(g.players[i].peer_id, "play_s botbeacon.ogg", 0)
						g.players[i].play_watch_scope()
						return

			# Check zombies
			for x in range(len(g.zombies)):
				if g.zombies[x].map != g.players[i].map: continue
				
				for wr in g.players[i].weapon_rays:
					if get_3d_distance(wr.x, wr.y, wr.z, g.zombies[x].x, g.zombies[x].y, g.zombies[x].z) <= (get_weapon_spread(g.players[i].weapon2) if g.players[i].aim==0 else get_weapon_spread(g.players[i].weapon2)-1):
						g.n.send_reliable(g.players[i].peer_id, "play_s botbeacon.ogg", 0)
						g.players[i].play_watch_scope()
						return
			for x in range(len(g.electrics)):
				if g.electrics[x].map != g.players[i].map: continue
				
				for wr in g.players[i].weapon_rays:
					if get_3d_distance(wr.x, wr.y, wr.z, g.electrics[x].x, g.electrics[x].y, g.electrics[x].z) <= (get_weapon_spread(g.players[i].weapon2) if g.players[i].aim==0 else get_weapon_spread(g.players[i].weapon2)-1):
						g.n.send_reliable(g.players[i].peer_id, "play_s botbeacon.ogg", 0)
						g.players[i].play_watch_scope()
						return


		# Second weapon check (similar optimization)
		if "collect" not in g.players[i].map and not g.players[i].jammer and not g.players[i].faint and not g.players[i].fainted and not g.players[i].dead and g.players[i].weaponbeeptimer.elapsed>=150 and g.players[i].scope==1 and g.players[i].weapon!="" and g.players[i].map!="lobby" and not g.players[i].map.startswith("match"):
			g.players[i].weaponbeeptimer.restart()
			# Pre-calculate weapon ray positions
			if g.players[i].weapon_rays2 is None:
				g.players[i].weapon_rays2=[]
				if g.players[i].aim_mode==1: wr = vector(g.players[i].x, g.players[i].y, g.players[i].z)
				if g.players[i].aim_mode==0: wr = vector(g.players[i].x, g.players[i].y, g.players[i].z+g.players[i].aim)
				for x2 in range(get_weapon_range(g.players[i].weapon,g.players[i].silenced)):
					wr = move(wr.x, wr.y, wr.z, g.players[i].facing, 0, 0, 0)
					if g.players[i].aim_mode==1:
						if g.players[i].aim==2 or g.players[i].aim==1: wr.z+=1
						if g.players[i].aim==-2 or g.players[i].aim==-1: wr.z-=1

					if g.players[i].aim_mode==1 and g.players[i].aim==-2 or g.players[i].aim_mode==1 and g.players[i].aim==2: g.players[i].weapon_rays2.append(vector(g.players[i].x,g.players[i].y, wr.z))
					else: g.players[i].weapon_rays2.append(vector(wr.x,wr.y, wr.z))


			# Check walls
			for wall in g.maps[g.get_map_index(g.players[i].map)].mapwalls:
				if wall.health <= 0: continue
				for wr in g.players[i].weapon_rays2:
					for wx in range(wall.minx, wall.maxx + 1):
						for wy in range(wall.miny, wall.maxy + 1):
							for wz in range(wall.minz, wall.maxz + 1):
								if get_3d_distance(wr.x, wr.y, wr.z, wx, wy, wz) <= (get_weapon_spread(g.players[i].weapon) if g.players[i].aim==0 else get_weapon_spread(g.players[i].weapon)-1):
									g.n.send_reliable(g.players[i].peer_id, "play_s scope.ogg", 0)
									g.players[i].play_watch_scope()
									return

			# Check players
			for x in range(len(g.players)):
				if g.get_hidden_area_at(g.players[i].x,g.players[i].y,g.players[i].z,g.players[i].map)!=g.get_hidden_area_at(g.players[x].x,g.players[x].y,g.players[x].z,g.players[x].map): continue
				if g.players[x].dead or g.players[x].health<=0 or g.players[x].invisible or g.players[x].hidden: continue
				if ("base" in g.players[x].map or g.players[x].map=="massacre_in_the_city") and g.get_group(g.players[x].group) is not None and g.players[x].group==g.players[i].group and g.get_group(g.players[x].group).freedomhit==0: continue
				if g.players[x].faint: continue
				if g.players[x].vi == g.players[i].vi and g.players[i].vi != -1 and g.players[x].vi != -1: continue
				if g.players[x].map != g.players[i].map or g.players[x].health <= 0: continue
				if g.players[x].ducking and g.players[i].aim > -(get_weapon_spread(g.players[i].weapon) if g.players[i].aim==0 else get_weapon_spread(g.players[i].weapon)-1) and not g.players[i].ducking: continue
				if g.players[x].name == g.players[i].name: continue
				if g.players[x].joinedmatch == g.players[i].joinedmatch and g.players[i].joinedmatch != "" and g.players[x].matchteam == g.players[i].matchteam and g.players[i].matchmode not in ["teaml", "teamk2", "teamf2", "snow", "sniper", "minecraft", "g", "g2", "collect", "sword"] and g.players[x].joinedmatch != "" and g.players[x].matchmode != "" and g.players[i].matchmode != "": continue
				
				first_ray = g.players[i].weapon_rays2[0]
				if g.players[x].matchmode == "teamz" and g.players[i].joinedmatch == g.players[x].joinedmatch and g.get_tile_at(first_ray.x, first_ray.y, 0, g.players[i].map) != "hardwood": continue
				
				for wr in g.players[i].weapon_rays2:
					if get_3d_distance(wr.x, wr.y, wr.z, g.players[x].x, g.players[x].y, g.players[x].z) <= (get_weapon_spread(g.players[i].weapon) if g.players[i].aim==0 else get_weapon_spread(g.players[i].weapon)-1):
						if not has_line_of_sight(wr.x,wr.y,wr.z,g.players[x].x,g.players[x].y,g.players[x].z,g.players[x].map): break
						g.n.send_reliable(g.players[i].peer_id, "play_s scope.ogg", 0)
						g.players[i].play_watch_scope()
						return

			# Check NPCs
			for x in range(len(g.npcs)):
				if g.npcs[x].faint: continue
				if g.npcs[x].joinedmatch == g.players[i].joinedmatch and g.npcs[x].matchteam == g.players[i].matchteam and g.players[i].matchmode not in ["teaml", "teamk2", "teamf2", "snow", "sniper", "minecraft", "sword", "collect", "g", "g2"] and g.players[i].joinedmatch != "": continue
				if g.npcs[x].map != g.players[i].map or g.npcs[x].health <= 0: continue
				
				first_ray = g.players[i].weapon_rays2[0]
				if g.npcs[x].matchmode == "teamz" and g.players[i].joinedmatch == g.npcs[x].joinedmatch and g.get_tile_at(first_ray.x, first_ray.y, 0, g.players[i].map) != "hardwood": continue
				
				for wr in g.players[i].weapon_rays2:
					if get_3d_distance(wr.x, wr.y, wr.z, g.npcs[x].x, g.npcs[x].y, g.npcs[x].z) <= (get_weapon_spread(g.players[i].weapon) if g.players[i].aim==0 else get_weapon_spread(g.players[i].weapon)-1):
						g.n.send_reliable(g.players[i].peer_id, "play_s scope.ogg", 0)
						g.players[i].play_watch_scope()
						return

			# Check motors
			for x in range(len(g.motors)):
				oi = g.get_player_index_from(g.motors[x].owner)
				if oi > -1 and g.players[oi].matchteam != "" and g.players[oi].matchteam == g.players[i].matchteam: continue
				if len(g.motors[x].players) != 0: continue
				if g.motors[x].map != g.players[i].map or g.motors[x].health <= 0: continue
				
				for wr in g.players[i].weapon_rays2:
					if get_3d_distance(wr.x, wr.y, wr.z, g.motors[x].x, g.motors[x].y, g.motors[x].z) <= (get_weapon_spread(g.players[i].weapon) if g.players[i].aim==0 else get_weapon_spread(g.players[i].weapon)-1):
						g.n.send_reliable(g.players[i].peer_id, "play_s scope.ogg", 0)
						g.players[i].play_watch_scope()
						return

			# Check zombies
			for x in range(len(g.zombies)):
				if g.zombies[x].map != g.players[i].map: continue
				
				for wr in g.players[i].weapon_rays2:
					if get_3d_distance(wr.x, wr.y, wr.z, g.zombies[x].x, g.zombies[x].y, g.zombies[x].z) <= (get_weapon_spread(g.players[i].weapon) if g.players[i].aim==0 else get_weapon_spread(g.players[i].weapon)-1):
						g.n.send_reliable(g.players[i].peer_id, "play_s scope.ogg", 0)
						g.players[i].play_watch_scope()
						return
			for x in range(len(g.electrics)):
				if g.electrics[x].map != g.players[i].map: continue
				
				for wr in g.players[i].weapon_rays2:
					if get_3d_distance(wr.x, wr.y, wr.z, g.electrics[x].x, g.electrics[x].y, g.electrics[x].z) <= (get_weapon_spread(g.players[i].weapon) if g.players[i].aim==0 else get_weapon_spread(g.players[i].weapon)-1):
						g.n.send_reliable(g.players[i].peer_id, "play_s scope.ogg", 0)
						g.players[i].play_watch_scope()
						return


		if g.players[i].fivecount==True and g.players[i].fivecounttimer.elapsed>=2000:
			g.players[i].fivecounttimer.restart()
			g.players[i].fivecount=False
			g.n.send_reliable(g.players[i].peer_id,"play_s "+g.players[i].get_current_char()+"voice24.ogg",0)
		if g.players[i].zombienoisetimer.elapsed>=6500 and g.players[i].matchteam=="blue" and g.players[i].map.startswith("zombie2"):
			g.players[i].zombienoisetimer.restart()
			g.playmoving(g.players[i].x,g.players[i].y,g.players[i].z,g.players[i].map,"zombievoice"+str(random(1,5)),g.players[i])
		if not g.players[i].dead and not g.players[i].faint and g.players[i].beacontimer.elapsed>=750 and g.players[i].map!="lobby":
			g.players[i].beacontimer.restart()
			for j in range(len(g.players)):
				if g.players[j].invisible: continue
				if g.players[i].name in g.players[j].friendlist and not g.players[j].name in g.players[i].friendlist: g.players[j].friendlist.remove(g.players[i].name)
				if g.players[j].name in g.players[i].friendlist and not g.players[i].name in g.players[j].friendlist: g.players[i].friendlist.remove(g.players[j].name)
			for p in g.players:
				if g.players[i].hidden: continue
				if g.get_hidden_area_at(p.x,p.y,p.z,p.map)!=g.get_hidden_area_at(g.players[i].x,g.players[i].y,g.players[i].z,g.players[i].map): continue
				if p.dead or p.specplayer==g.players[i].name or g.players[i].specplayer==p.name or p.name==g.players[i].name: continue
				if (p.beacon==1 and (p.map==g.players[i].map or p.specmap==g.players[i].map)) and g.players[i].distancecheck(p.wx,p.wy,p.wz)<=30:
					if p.specplayer=="" and (p.map.startswith("match") or p.map=="lobby"): pass
					else:
						if p.group=="" and g.players[i].group=="" and ("basement" in p.map or p.map=="massacre_in_the_city"): g.n.send_reliable(p.peer_id,"beep "+str(round(g.players[i].x))+" "+str(round(g.players[i].y))+" "+str(round(g.players[i].z))+" "+g.players[i].map+" 100",3); continue
						if p.group=="" and g.players[i].group!="" and ("basement" in p.map or p.map=="massacre_in_the_city"): g.n.send_reliable(p.peer_id,"beep "+str(round(g.players[i].x))+" "+str(round(g.players[i].y))+" "+str(round(g.players[i].z))+" "+g.players[i].map+" 100",3); continue
						if p.group!="" and g.players[i].group=="" and ("basement" in p.map or p.map=="massacre_in_the_city"): g.n.send_reliable(p.peer_id,"beep "+str(round(g.players[i].x))+" "+str(round(g.players[i].y))+" "+str(round(g.players[i].z))+" "+g.players[i].map+" 100",3); continue
						if p.group!="" and g.players[i].group!="" and g.players[i].group!=p.group and ("basement" in p.map or p.map=="massacre_in_the_city"): g.n.send_reliable(p.peer_id,"beep "+str(round(g.players[i].x))+" "+str(round(g.players[i].y))+" "+str(round(g.players[i].z))+" "+g.players[i].map+" 100",3); continue
						if p.map!="massacre_in_the_city" and p.matchmode=="teaml": g.n.send_reliable(p.peer_id,"beep "+str(round(g.players[i].x))+" "+str(round(g.players[i].y))+" "+str(round(g.players[i].z))+" "+g.players[i].map+" 100",3); continue
						if p.map!="massacre_in_the_city" and p.matchmode=="minecraft": g.n.send_reliable(p.peer_id,"beep "+str(round(g.players[i].x))+" "+str(round(g.players[i].y))+" "+str(round(g.players[i].z))+" "+g.players[i].map+" 100",3); continue
						if p.map!="massacre_in_the_city" and p.matchmode=="sword": g.n.send_reliable(p.peer_id,"beep "+str(round(g.players[i].x))+" "+str(round(g.players[i].y))+" "+str(round(g.players[i].z))+" "+g.players[i].map+" 100",3); continue
						if p.map!="massacre_in_the_city" and p.matchmode=="collect": g.n.send_reliable(p.peer_id,"beep "+str(round(g.players[i].x))+" "+str(round(g.players[i].y))+" "+str(round(g.players[i].z))+" "+g.players[i].map+" 100",3); continue
						if p.map!="massacre_in_the_city" and p.matchmode=="teamk2": g.n.send_reliable(p.peer_id,"beep "+str(round(g.players[i].x))+" "+str(round(g.players[i].y))+" "+str(round(g.players[i].z))+" "+g.players[i].map+" 100",3); continue
						if p.map!="massacre_in_the_city" and p.matchmode=="teamf2": g.n.send_reliable(p.peer_id,"beep "+str(round(g.players[i].x))+" "+str(round(g.players[i].y))+" "+str(round(g.players[i].z))+" "+g.players[i].map+" 100",3); continue
						if p.map!="massacre_in_the_city" and p.matchmode=="snow": g.n.send_reliable(p.peer_id,"beep "+str(round(g.players[i].x))+" "+str(round(g.players[i].y))+" "+str(round(g.players[i].z))+" "+g.players[i].map+" 100",3); continue
						if p.map!="massacre_in_the_city" and p.matchmode=="sniper": g.n.send_reliable(p.peer_id,"beep "+str(round(g.players[i].x))+" "+str(round(g.players[i].y))+" "+str(round(g.players[i].z))+" "+g.players[i].map+" 100",3); continue
						if p.map!="massacre_in_the_city" and p.matchmode=="g": g.n.send_reliable(p.peer_id,"beep "+str(round(g.players[i].x))+" "+str(round(g.players[i].y))+" "+str(round(g.players[i].z))+" "+g.players[i].map+" 100",3); continue
						if p.map!="massacre_in_the_city" and p.matchmode=="g2": g.n.send_reliable(p.peer_id,"beep "+str(round(g.players[i].x))+" "+str(round(g.players[i].y))+" "+str(round(g.players[i].z))+" "+g.players[i].map+" 100",3); continue

						if p.map!="massacre_in_the_city" and p.specplayer!=g.players[i].name and p.matchteam!=g.players[i].matchteam and p.matchteam!="" and g.players[i].matchteam!="": g.n.send_reliable(p.peer_id,"beep "+str(round(g.players[i].x))+" "+str(round(g.players[i].y))+" "+str(round(g.players[i].z))+" "+g.players[i].map+" 100",3)
						if p.map!="massacre_in_the_city" and p.specplayer!=g.players[i].name and p.map!="lobby" and p.matchteam==g.players[i].matchteam and p.matchteam!="" and g.players[i].matchteam!="": g.n.send_reliable(p.peer_id,"teambeacon "+str(round(g.players[i].x))+" "+str(round(g.players[i].y))+" "+str(round(g.players[i].z))+" "+g.players[i].map+" 100",3)
						if p.group!="" and g.players[i].group!="" and ("basement" in g.players[i].map or g.players[i].map=="massacre_in_the_city") and p.group==g.players[i].group: g.n.send_reliable(p.peer_id,"teambeacon "+str(round(g.players[i].x))+" "+str(round(g.players[i].y))+" "+str(round(g.players[i].z))+" "+g.players[i].map+" 100",3)
		if g.players[i].map!="lobby" and not g.players[i].map.startswith("match") and g.players[i].nearchecktimer.elapsed>2000:
			g.players[i].nearchecktimer.restart()
			for p in g.players:
				if p.matchteam!=g.players[i].matchteam and p.matchteam!="" and g.players[i].matchteam!="" and g.players[i].differentteamplayers==0: continue
				if p.matchteam==g.players[i].matchteam and p.matchteam!="" and g.players[i].matchteam!="" and g.players[i].sameteamplayers==0: continue
				if p.group!=g.players[i].group and p.group!="" and g.players[i].group!="" and g.players[i].differentgroupplayers==0: continue
				if p.group==g.players[i].group and p.group!="" and g.players[i].group!="" and g.players[i].samegroupplayers==0: continue
				if g.players[i].specplayer!="" or p.specplayer!="" or p.name==g.players[i].name: continue
				if p.hidden: continue

				if p.map==g.players[i].map and p.name not in g.players[i].nearplayers and get_3d_distance(p.x,p.y,p.z,g.players[i].x,g.players[i].y,g.players[i].z)<=50 and get_hidden_area_at(p.x,p.y,p.z,p.map)==get_hidden_area_at(g.players[i].x,g.players[i].y,g.players[i].z,g.players[i].map):
					g.players[i].nearplayers.append(p.name)
					if p.map=="massacre_in_the_city" and p.group==g.players[i].group and p.group!="" and g.players[i].group!="":
						if g.players[i].nearn==1: g.send_reliable(g.players[i].peer_id,"nearinfo group member "+p.name+" is near you! They're "+calculate_x_y_string(calculate_x_y_angle(g.players[i].x,g.players[i].y,p.x,p.y,g.players[i].facing)),0)
						if g.players[i].sound==1 and g.players[i].nearn==1: g.send_reliable(g.players[i].peer_id,"play_s misc287.ogg",0)
					elif p.matchteam==g.players[i].matchteam and p.matchteam!="":
						if g.players[i].nearn==1: g.send_reliable(g.players[i].peer_id,"nearinfo teammate "+p.name+" is near you! They're "+calculate_x_y_string(calculate_x_y_angle(g.players[i].x,g.players[i].y,p.x,p.y,g.players[i].facing)),0)
						if g.players[i].sound==1 and g.players[i].nearn==1: g.send_reliable(g.players[i].peer_id,"play_s misc287.ogg",0)
					else:
						if g.players[i].nearn==1: g.send_reliable(g.players[i].peer_id,"nearinfo enemy "+p.name+" is near you! They're "+calculate_x_y_string(calculate_x_y_angle(g.players[i].x,g.players[i].y,p.x,p.y,g.players[i].facing)),0)
						if g.players[i].sound==1 and g.players[i].nearn==1: g.send_reliable(g.players[i].peer_id,"play_s trackappeared.ogg",0)

					if g.players[i].charvoice==1 and g.players[i].nearn==1: g.send_reliable(g.players[i].peer_id,"play_s "+g.players[i].get_current_char()+"voice28.ogg",0)
				if p.name in g.players[i].nearplayers and (p.map!=g.players[i].map or get_hidden_area_at(p.x,p.y,p.z,p.map)!=get_hidden_area_at(g.players[i].x,g.players[i].y,g.players[i].z,g.players[i].map) or get_3d_distance(p.x,p.y,p.z,g.players[i].x,g.players[i].y,g.players[i].z)>50):
					g.players[i].nearplayers.remove(p.name)
					if p.map=="massacre_in_the_city" and p.group==g.players[i].group and p.group!="" and g.players[i].group!="":
						if g.players[i].nearn==1: g.send_reliable(g.players[i].peer_id,"nearinfo group member "+p.name+" is no longer near you!",0)
						if g.players[i].sound==1 and g.players[i].nearn==1: g.send_reliable(g.players[i].peer_id,"play_s misc276.ogg",0)

					elif p.matchteam==g.players[i].matchteam and p.matchteam!="":
						if g.players[i].nearn==1: g.send_reliable(g.players[i].peer_id,"nearinfo teammate "+p.name+" is no longer near you!",0)
						if g.players[i].sound==1 and g.players[i].nearn==1: g.send_reliable(g.players[i].peer_id,"play_s misc276.ogg",0)
					else:
						if g.players[i].nearn==1: g.send_reliable(g.players[i].peer_id,"nearinfo enemy "+p.name+" is no longer near you!",0)
						if g.players[i].sound==1 and g.players[i].nearn==1: g.send_reliable(g.players[i].peer_id,"play_s trackdisappeared.ogg",0)

					if g.players[i].charvoice==1 and g.players[i].nearn==1: g.send_reliable(g.players[i].peer_id,"play_s "+g.players[i].get_current_char()+"voice29.ogg",0)


			for p in g.npcs:
				if p.matchteam!=g.players[i].matchteam and p.matchteam!="" and g.players[i].matchteam!="" and g.players[i].differentteambots==0: continue
				if p.matchteam==g.players[i].matchteam and p.matchteam!="" and g.players[i].matchteam!="" and g.players[i].sameteambots==0: continue
				if get_hidden_area_at(p.x,p.y,p.z,p.map)!=get_hidden_area_at(g.players[i].x,g.players[i].y,g.players[i].z,g.players[i].map): continue
				if not p.fulldied and p.name not in g.players[i].nearbots and p.map==g.players[i].map and get_3d_distance(p.x,p.y,p.z,g.players[i].x,g.players[i].y,g.players[i].z)<=50:
					g.players[i].nearbots.append(p.name)
					if p.matchteam==g.players[i].matchteam and p.matchteam!="":
						if g.players[i].nearn==1: g.send_reliable(g.players[i].peer_id,"nearinfo teammate "+p.name+" is near you! They're "+calculate_x_y_string(calculate_x_y_angle(g.players[i].x,g.players[i].y,p.x,p.y,g.players[i].facing)),0)
						if g.players[i].sound==1 and g.players[i].nearn==1: g.send_reliable(g.players[i].peer_id,"play_s misc287.ogg",0)
					else:
						if g.players[i].nearn==1: g.send_reliable(g.players[i].peer_id,"nearinfo enemy "+p.name+" is near you! They're "+calculate_x_y_string(calculate_x_y_angle(g.players[i].x,g.players[i].y,p.x,p.y,g.players[i].facing)),0)
						if g.players[i].sound==1 and g.players[i].nearn==1: g.send_reliable(g.players[i].peer_id,"play_s trackappeared.ogg",0)
					if g.players[i].charvoice==1 and g.players[i].nearn==1: g.send_reliable(g.players[i].peer_id,"play_s "+g.players[i].get_current_char()+"voice28.ogg",0)
				if p.name in g.players[i].nearbots and (p.fulldied or p.map!=g.players[i].map or get_3d_distance(p.x,p.y,p.z,g.players[i].x,g.players[i].y,g.players[i].z)>50):
					g.players[i].nearbots.remove(p.name)
					if p.matchteam==g.players[i].matchteam and p.matchteam!="":
						if g.players[i].nearn==1: g.send_reliable(g.players[i].peer_id,"nearinfo teammate "+p.name+" is no longer near you!",0)
						if g.players[i].sound==1 and g.players[i].nearn==1: g.send_reliable(g.players[i].peer_id,"play_s misc276.ogg",0)
					else:
						if g.players[i].nearn==1: g.send_reliable(g.players[i].peer_id,"nearinfo enemy "+p.name+" is no longer near you!",0)
						if g.players[i].sound==1 and g.players[i].nearn==1: g.send_reliable(g.players[i].peer_id,"play_s trackdisappeared.ogg",0)
					if g.players[i].charvoice==1 and g.players[i].nearn==1: g.send_reliable(g.players[i].peer_id,"play_s "+g.players[i].get_current_char()+"voice29.ogg",0)

		if g.players[i].maxhpcheckertimer.elapsed>=1000:
			g.players[i].maxhpcheckertimer.restart()
			if g.players[i].health>g.players[i].maxhealth:
				g.players[i].health=g.players[i].maxhealth
				return
		if g.players[i].maxhpchecker2timer.elapsed>=1000:
			g.players[i].maxhpchecker2timer.restart()
			if g.players[i].map=="lobby" and g.players[i].health!=g.players[i].maxhealth: g.players[i].health=g.players[i].maxhealth
		if g.players[i].hudtimer.elapsed>=500:
			g.players[i].hudtimer.restart()
			try:
				p=g.players[i]
				loaded1=p.ammocheck(p.weapon) if p.weapon and p.weapon!="punch" else -1
				reserve1=p.get_item_count(g.get_ammotype(p.weapon)) if p.weapon and p.weapon!="punch" else -1
				loaded2=p.ammocheck(p.weapon2) if p.weapon2 and p.weapon2!="feet" else -1
				reserve2=p.get_item_count(g.get_ammotype(p.weapon2)) if p.weapon2 and p.weapon2!="feet" else -1
				shield=int(p.shieldhitchance)
				helmet=int(p.helmethitchance)
				g.n.send_reliable(p.peer_id,
					f"hud_data {int(p.health)} {int(p.maxhealth)} {p.weapon or 'none'} {loaded1} {reserve1} {p.weapon2 or 'none'} {loaded2} {reserve2} {shield} {helmet}",
					0)
			except Exception: pass
		if(g.players[i].reloading):
		
			if(g.players[i].weapon!="" and g.players[i].reloadtimer.elapsed>g.players[i].reloadtime):
			
				g.n.send_reliable(g.players[i].peer_id,"notreloading",0)
				g.players[i].get_char_properties()
				g.players[i].get_current_char()
				g.players[i].get_weapon_properties(g.players[i].weapon2)

				g.players[i].get_weapon_properties(g.players[i].weapon)
				g.players[i].reloading=False
				p=g.players[i]
				amount=0
				if(p.get_item_count(g.get_ammotype(p.weapon))<g.get_max_ammo(p.weapon)):
					amount=p.get_item_count(g.get_ammotype(p.weapon))
					amount=p.get_item_count(g.get_ammotype(p.weapon))-g.players[i].get_ammo_count(g.players[i].weapon)
					if(amount>g.players[i].get_item_count(g.get_ammotype(g.players[i].weapon))):
						amount=g.players[i].get_item_count(g.get_ammotype(g.players[i].weapon))
					p.ammogive(p.weapon,amount)
					p.give(g.get_ammotype(p.weapon),-amount)					

				else:
					amount=g.get_max_ammo(p.weapon)
				
					amount=g.get_max_ammo(g.players[i].weapon)-g.players[i].get_ammo_count(g.players[i].weapon)
					if(amount>g.players[i].get_item_count(g.get_ammotype(g.players[i].weapon))):
						amount=g.players[i].get_item_count(g.get_ammotype(g.players[i].weapon))
					p.ammogive(p.weapon,amount)
					p.give(g.get_ammotype(p.weapon),-amount)					
				
			
			if(g.players[i].weapon2!="" and g.players[i].reloadtimer.elapsed>g.players[i].reloadtime):
			
				g.n.send_reliable(g.players[i].peer_id,"notreloading",0)
				g.players[i].get_char_properties()
				g.players[i].get_current_char()
				g.players[i].get_weapon_properties(g.players[i].weapon2)

				g.players[i].get_weapon_properties(g.players[i].weapon)
				g.players[i].reloading=False
				p=g.players[i]
				amount=0
				if(p.get_item_count(g.get_ammotype(p.weapon2))<g.get_max_ammo(p.weapon2)):
					amount=p.get_item_count(g.get_ammotype(p.weapon2))
					amount=p.get_item_count(g.get_ammotype(p.weapon2))-g.players[i].get_ammo_count(g.players[i].weapon2)
					if(amount>g.players[i].get_item_count(g.get_ammotype(g.players[i].weapon2))):
						amount=g.players[i].get_item_count(g.get_ammotype(g.players[i].weapon2))
					p.ammogive(p.weapon2,amount)
					p.give(g.get_ammotype(p.weapon2),-amount)					

				else:
					amount=g.get_max_ammo(p.weapon2)
				
					amount=g.get_max_ammo(g.players[i].weapon2)-g.players[i].get_ammo_count(g.players[i].weapon2)
					if(amount>g.players[i].get_item_count(g.get_ammotype(g.players[i].weapon2))):
						amount=g.players[i].get_item_count(g.get_ammotype(g.players[i].weapon2))
					p.ammogive(p.weapon2,amount)
					p.give(g.get_ammotype(p.weapon2),-amount)					
				
			

		if(g.players[i].firing==True and g.players[i].firetimer.elapsed>=g.players[i].firetime and g.players[i].weapon!=""):
		
			g.players[i].firetimer.restart()
			if g.players[i].get_ammo_count_from(g.players[i].weapon)<=0:
				g.players[i].firing=False
				import data_loader as _dl
				g.players[i].playsound(_dl.get_weapon_sound(g.players[i].weapon,"empty"))
				return
			import data_loader as _dl
			_v=random(1,3)
			g.players[i].playsound(_dl.get_weapon_sound(g.players[i].weapon,"fire",_v))
			if not g.players[i].hidden: g.send_plus(g.players[i].name,"distsound "+_dl.get_weapon_sound(g.players[i].weapon,"dist",_v)+" "+str(g.players[i].x)+" "+str(g.players[i].y)+" "+str(g.players[i].z)+" "+g.players[i].map,0)
			spawn_weapon(g.players[i].x, g.players[i].y, g.players[i].z, g.players[i].facing, g.players[i].weapon, g.players[i].map, g.players[i])
			g.players[i].ammogive(g.players[i].weapon,-1)			
		if(g.players[i].invchecktimer.elapsed>=1000) :
			g.players[i].invchecktimer.restart()
			if(pickle.dumps(g.players[i].inv)!=g.players[i].cachedinv):
			
				data=pickle.dumps(g.players[i].inv)
				g.send_reliable(g.players[i].peer_id, data,19)
				g.players[i].cachedinv=data
				
			
		if g.players[i].health<=0 and g.players[i].dead==False:
			if getattr(g.players[i], "controlled_turret", None) is not None:
				g.players[i].controlled_turret.operator = None
				g.players[i].controlled_turret = None
			if g.players[i].bike is not None:
				g.n.send_reliable(g.players[i].peer_id,"notinbike",0)
				try: g.players[i].bike.players.remove(g.players[i].name)
				except: pass
				g.players[i].bike=None
			faint=random(1,2)
			if g.players[i].matchmode!="teamd" and g.players[i].matchmode!="teamz2": faint=1
			if g.players[i].fainted and faint!=1: faint=1
			if faint==1:
				g.players[i].parachuted=False
				g.n.send_reliable(g.players[i].peer_id,"parachute_stop",0)
				for i2 in g.players:
					if i2.specplayer==g.players[i].name: g.n.send_reliable(i2.peer_id,"parachute_start",0)
				if g.players[i].get_item_count(-1)>0: g.players[i].give(-1,-100)
				spawn_corpse(g.players[i].x,g.players[i].y,g.players[i].z,g.players[i].map)
				corp=g.corpses[-1]
				corp.owner=g.players[i].name
				corp.bomb=g.players[i].corpse_bomb
				for weapon in list(g.players[i].ammo.keys()):
					c=g.players[i].get_ammo_count(weapon)
					spawn_item(g.players[i].x,g.players[i].y,g.players[i].z,g.players[i].map,g.get_ammotype(weapon),c,False,corp)

				for key in g.players[i].inv.keys():
					if key==-1: continue
					if isinstance(key,str) and key not in g.dontlose:
						if g.players[i].weapon==key or g.players[i].weapon2==key: 
							g.players[i].playsound("weapondrop")
							if g.players[i].get_item_count(key)==1: spawn_item(g.players[i].x,g.players[i].y,g.players[i].z,g.players[i].map,key,g.players[i].get_item_count(key),False)
							if g.players[i].get_item_count(key)>1:
								spawn_item(g.players[i].x,g.players[i].y,g.players[i].z,g.players[i].map,key,1,False)
								spawn_item(g.players[i].x,g.players[i].y,g.players[i].z,g.players[i].map,key,g.players[i].get_item_count(key),False,corp)
						else:
							if key!=-1 and key!="-1": spawn_item(g.players[i].x,g.players[i].y,g.players[i].z,g.players[i].map,key,g.players[i].get_item_count(key),False,corp)
				if g.players[i].flag>0:
					for f in range(g.players[i].flag): spawn_flag(g.players[i].x, g.players[i].y, g.players[i].z, g.players[i].map, ("blue" if g.players[i].matchteam=="red" else "blue"))
					g.players[i].flag=0
				g.save_all_chars()
			for k in range(len(g.players)):
				if g.players[i].hidden: continue
				if (g.players[k].specmap==g.players[i].map or g.players[k].map==g.players[i].map or ("base" in g.players[k].map and g.players[i].map=="massacre_in_the_city")) and g.players[k].killn==1:
					if faint==1:
						if g.players[k].matchteam!="" and g.players[k].matchteam!=g.players[i].matchteam: g.n.send_reliable(g.players[k].peer_id,"killn enemy "+g.players[i].name+" has been killed by "+g.players[i].hitby+" at coordinates "+str(round(g.players[i].x))+", "+str(round(g.players[i].y))+", "+str(round(g.players[i].z))+". "+g.players[i].name+" had "+g.players[i].weapon+" and "+g.players[i].weapon2,0)
						if g.players[k].matchteam=="": g.n.send_reliable(g.players[k].peer_id,"killn enemy "+g.players[i].name+" has been killed by "+g.players[i].hitby+" at coordinates "+str(round(g.players[i].x))+", "+str(round(g.players[i].y))+", "+str(round(g.players[i].z))+". "+g.players[i].name+" had "+g.players[i].weapon+" and "+g.players[i].weapon2,0)
						if g.players[k].matchteam!="" and g.players[k].matchteam==g.players[i].matchteam: g.n.send_reliable(g.players[k].peer_id,"killn teammate "+g.players[i].name+" has been killed by "+g.players[i].hitby+" at coordinates "+str(round(g.players[i].x))+", "+str(round(g.players[i].y))+", "+str(round(g.players[i].z))+". "+g.players[i].name+" had "+g.players[i].weapon+" and "+g.players[i].weapon2,0)
						if "minecraft" not in g.players[k].matchmode: g.n.send_reliable(g.players[k].peer_id,"play_s teammessage2.ogg",0)
						if "minecraft" in g.players[k].matchmode: g.n.send_reliable(g.players[k].peer_id,"play_s killthunder.ogg",0)
			if "flag" not in g.players[i].map: g.players[i].silenced.clear()

			g.n.send_reliable(g.players[i].peer_id,"noweaponauto",0)
			g.n.send_reliable(g.players[i].peer_id,"canjump 1",0)
			g.n.send_reliable(g.players[i].peer_id,"canduck 1",0)
			g.players[i].get_char_properties()
			g.n.send_reliable(g.players[i].peer_id,"pausesources",0)
			g.players[i].flashvolume=100
			g.n.send_reliable(g.players[i].peer_id,"flashvolume -"+str(g.players[i].flashvolume),0)
			g.players[i].chest=None
			g.players[i].corpse=None
			g.players[i].shielded=False
			g.players[i].helmeted=False
			g.players[i].shieldhitchance=0
			g.players[i].helmethitchance=0
			g.n.send_reliable(g.players[i].peer_id,"setaim 0",0)
			g.players[i].aim=0
			if "hitting the ground" not in g.players[i].hitby: spawn_bodyfall(g.players[i].x, g.players[i].y ,g.players[i].z, g.players[i].map,1500)
			g.send_reliable(g.players[i].peer_id,"resetwalktime",0)
			g.players[i].play_death_sound()

			if faint==2 and g.players[i].fainted==False and (g.players[i].matchmode=="teamd" or g.players[i].matchmode=="teamz2"):
				g.players[i].fainted=True
				g.players[i].faint=True
				g.players[i].health=20
				g.players[i].fainttimer.restart()
				g.n.send_reliable(g.players[i].peer_id,"stopmoving",0)
				for m in g.matches:
					if g.players[i].name in m.players:
						m.teamsend(g.players[i].matchteam,g.players[i].name+" fainted in coordinates "+str(round(g.players[i].x))+", "+str(round(g.players[i].y))+", "+str(round(g.players[i].z))+".",0)
				return
			g.players[i].weapon="punch"
			g.players[i].weapon2="feet"
			g.players[i].fainted=False
			g.n.send_reliable(g.players[i].peer_id,"drawsilent punch",0)
			g.n.send_reliable(g.players[i].peer_id,"draw2silent feet",0)
			g.players[i].get_weapon_properties(g.players[i].weapon)
			g.players[i].get_weapon_properties(g.players[i].weapon2)

			g.players[i].ammo.clear()
			if g.players[i].group!="":
				grp=g.get_group(g.players[i].group)
				grp.deaths+=1
			if g.players[i].vi!=-1:
				try: g.motors[g.players[i].vi].players.remove(g.players[i].name)
				except: pass
				g.players[i].vi=-1
				g.players[i].inve=False
				g.n.send_reliable(g.players[i].peer_id,"motorunspawn",0)
			killer=""
			if(string_contains(g.players[i].hitby,"'",1)>-1):
				s=string_split(g.players[i].hitby, "'", True)
				killer=s[0]
			else:
				killer=g.players[i].hitby
			if killer in usernames: g.players[i].botdeaths+=1
			if killer not in usernames: g.players[i].playerdeaths+=1
			ind=g.get_player_index_from(killer)
			if ind>-1 and "flag" not in g.players[ind].map and g.players[ind].group!="" and killer!=g.players[i].name:
				grp=g.get_group(g.players[ind].group)
				grp.add_kill()
			for m in g.matches:
				if 1:
					if g.players[i].name in m.players and m.mode!="teamc": m.players.remove(g.players[i].name); m.deadplayers.append(g.players[i].name)

					if m.started and len(m.players)==1 and (m.mode=="teaml" or m.mode=="teamk2" or m.mode=="teamf2" or m.mode=="snow" or m.mode=="sniper" or m.mode=="g2" or m.mode=="sword" or m.mode=="collect" or m.mode=="g" or m.mode=="minecraft"):
						m.send("Match ended. "+m.players[0]+" won!",2)
						#try: m.givezhtoken(g.getpc(m.players[0]).name)
						#except: pass
						try: g.n.send_reliable(g.getpc(m.players[0]).peer_id,"play_s win.ogg",0)
						except: pass
						m.send_except(m.players[0],"play_s misc171.ogg",0)
						j=g.getpc(m.players[0])
						if j is not None:
							item_map={}
							for item in g.dontlose:
								if j.get_item_count(item)>0: item_map[item]=j.get_item_count(item)
							g.getpc(m.players[0]).inv=dict()
							for item in item_map.keys():
								j.give(item,item_map[item])
						if m.mode=="teamz": m.clearzombies()
						for n in g.npcs:
							if n.map==m.get_cwmap():
								n.health=0;n.dontkill=True
								n.hitby=""
								n.hitby2=""

						try: g.move_player(g.get_player_index_from(m.players[0]),5,0,0,"lobby")
						except: pass
						file_delete("maps/match"+m.owner+".map")
						file_delete("maps/main"+m.owner+".map");file_delete("maps/grenade"+m.owner+".map")
						file_delete("maps/flag"+m.owner+".map")
						file_delete("maps/zombie"+m.owner+".map")
						file_delete("maps/combo"+m.owner+".map")
						file_delete("maps/knife"+m.owner+".map")
						file_delete("maps/zombie2"+m.owner+".map")
						file_delete("maps/helicopter"+m.owner+".map")
						file_delete("maps/sword"+m.owner+".map")
						file_delete("maps/abyss_clash"+m.owner+".map")
						file_delete("maps/one_shot_one_kill"+m.owner+".map")
						file_delete("maps/snow"+m.owner+".map"); file_delete("maps/collect"+m.owner+".map")

						g.init_mapsystem()
						g.matches.remove(m)
						break
					if len(m.players)==0:
						m.send("Match ended. No one won!",2)
						if m.mode=="teamz": m.clearzombies()
						for n in g.npcs:
							if n.map==m.get_cwmap():
								g.n.broadcast("offline "+str(n.x)+" "+str(n.y)+" "+str(n.z)+" "+n.name+" "+n.map,0)
								g.npcs.remove(n)

						file_delete("maps/match"+m.owner+".map")
						file_delete("maps/main"+m.owner+".map");file_delete("maps/grenade"+m.owner+".map")
						file_delete("maps/flag"+m.owner+".map")
						file_delete("maps/combo"+m.owner+".map")
						file_delete("maps/zombie"+m.owner+".map")
						file_delete("maps/knife"+m.owner+".map")
						file_delete("maps/zombie2"+m.owner+".map")
						file_delete("maps/helicopter"+m.owner+".map")
						file_delete("maps/sword"+m.owner+".map")
						file_delete("maps/abyss_clash"+m.owner+".map")
						file_delete("maps/one_shot_one_kill"+m.owner+".map")
						file_delete("maps/snow"+m.owner+".map"); file_delete("maps/collect"+m.owner+".map")

						g.init_mapsystem()
						g.matches.remove(m)
						break
			if g.players[i].scorepoint<0:
				g.players[i].scorepoint=0
			j=g.players[i]
			item_map={}
			for item in g.dontlose:
				if j.get_item_count(item)>0: item_map[item]=j.get_item_count(item)
			j.inv=dict()
			for item in item_map.keys():
				j.give(item,item_map[item])

			try:
				import db as _db; _db.charwrite(g.players[i].name,"maldied",1)
			except: pass
			killer=""
			if(string_contains(g.players[i].hitby,"'",1)>-1):
				s=string_split(g.players[i].hitby, "'", True)
				killer=s[0]
			else:
				killer=g.players[i].hitby
			p=g.get_player_index_from(killer)
			if 1:
				if 1:
					if p>-1 and g.task==0:
						if g.freedomsurvivor==g.players[i].name and killer!=g.freedomsurvivor:
							if g.players[p].task_data[0]<5: g.players[p].eventpoint+=10; g.players[p].playsound("misc294"); g.players[p].currenteventpoint+=10; g.n.send_reliable(g.players[p].peer_id,"You got 10 event point",2); g.players[p].task_data[0]+=1
							if g.players[p].task_data[0]>=5: g.players[p].playsound("misc294"); g.players[p].currenteventpoint+=10; g.players[p].task_data[0]+=1
							for p2 in g.players:
								if p2.map=="massacre_in_the_city" and killer!=g.freedomsurvivor:
									g.n.send_reliable(p2.peer_id,"play_s teammessage.ogg",0)
									g.n.send_reliable(p2.peer_id,g.freedomsurvivor+" failed to survive for 10 minutes, they got killed by "+killer+"! As a result, "+killer+" gets 10 event points, and another player will be selected.",2)
							g.freedomsurvivor=""
					if p>-1 and g.task==1 and i!=p and g.players[p].task_data[1]<20 and "flag" not in g.players[p].map:
						g.players[p].eventpoint+=10; g.players[p].playsound("misc294"); g.players[p].currenteventpoint+=10; g.n.send_reliable(g.players[p].peer_id,"You got 10 event point",2); g.players[p].task_data[1]+=1
					elif p>-1 and "flag" not in g.players[p].map and p>-1 and g.task==1 and i!=p and g.players[p].task_data[1]>=20: g.players[p].currenteventpoint+=10

			if(p>-1 and killer!=g.players[i].name):
				if g.players[p].scoretimer.elapsed>0 and g.players[p].map!="massacre_in_the_city":
					if not g.players[p].paid: g.players[p].scorepoint+=1
					if g.players[p].paid: g.players[p].scorepoint+=2
					g.players[p].scoretimer.restart()

				elif g.players[p].map=="massacre_in_the_city":
					if not g.players[p].paid: g.players[p].scorepoint+=1
					if g.players[p].paid: g.players[p].scorepoint+=2
					if not g.players[p].paid: g.n.send_reliable(g.players[p].peer_id,"You get 1 score point for killing "+g.players[i].name+"",2)
					if g.players[p].paid: g.n.send_reliable(g.players[p].peer_id,"You get 2 score point for killing "+g.players[i].name+"",2)
					g.n.send_reliable(g.players[p].peer_id,"play_s getpoint.ogg",0)
				pc=g.getpc(killer)
				if pc.map!="massacre_in_the_city" and g.players[i].name not in pc.tokenplayers:

					pc.tokenplayers[g.players[i].name]=timer()
					a=random(3,5)
					if pc.paid: a*=2
					pc.zhtoken+=a
					try: g.n.send_reliable(pc.peer_id,"you got "+str(a)+" zero token",2)
					except: pass
					if pc.matchteam!="":
						for pl in g.players:
							if pc.name==pl.name: continue
							if pl.map==pc.map and pl.matchteam==pc.matchteam:
								a=random(3,5)
								if pl.paid: a*=2
								pl.zhtoken+=a
								g.n.send_reliable(pl.peer_id,"you got "+str(a)+" zero token",2)

				rnd=random(1,2)
				if g.players[p].map=="massacre_in_the_city" and rnd==2:
					if not g.players[p].paid:
						g.players[p].zhtoken+=1
						g.n.send_reliable(g.players[p].peer_id,"You received 1 zero token",2)
					if g.players[p].paid:
						g.players[p].zhtoken+=2
						g.n.send_reliable(g.players[p].peer_id,"You received 2 zero token",2)

				g.players[p].killcount+=1
				g.players[p].playerkills+=1
				if g.players[p].killcount==1:
					g.send_reliable(g.players[p].peer_id,"play_s "+g.players[p].get_current_char()+"voice25.ogg",0)
				if g.players[p].killcount==2:
					g.send_reliable(g.players[p].peer_id,"play_s "+g.players[p].get_current_char()+"voice18.ogg",0)
				if g.players[p].killcount==3:
					g.send_reliable(g.players[p].peer_id,"play_s "+g.players[p].get_current_char()+"voice19.ogg",0)
				if g.players[p].killcount==5:
					g.send_reliable(g.players[p].peer_id,"play_s "+g.players[p].get_current_char()+"voice22.ogg",0)
					g.n.send_reliable(g.players[p].peer_id,"play_s misc6.ogg",0)
					g.players[p].give("revival_nectar",2)
					g.players[p].give("9mm",50)
				if g.players[p].killcount==4:
					g.send_reliable(g.players[p].peer_id,"play_s "+g.players[p].get_current_char()+"voice26.ogg",0)
					if g.players[p].fivecount==False:
						g.players[p].fivecounttimer.restart()
						g.players[p].fivecount=True

			g.players[i].dead=True
			if g.players[i].map!="massacre_in_the_city" and "basement" not in g.players[i].map and g.players[i].matchmode!="teamc": g.send_reliable(g.players[i].peer_id,"die",0)
			if "basement" in g.players[i].map or g.players[i].map=="massacre_in_the_city" or g.players[i].matchmode=="teamc":
				g.send_reliable(g.players[i].peer_id,"stopmoving",0)
				g.send_reliable(g.players[i].peer_id,"died",0)
				g.send_reliable(g.players[i].peer_id,"play_s misc331.ogg",0)
				g.send_reliable(g.players[i].peer_id,"play_s misc333.ogg",0)
				g.send_reliable(g.players[i].peer_id,"play_s misc334.ogg",0)

				g.players[i].respawn=True
				g.players[i].respawntimer.restart()
			else:
				g.players[i].x=random(1,500)
				g.players[i].y=random(1,500)
				g.players[i].z=0

				return
			
		
	
def spawn_player(x,y,z,map,name,pi,srate,hidden=False):
	p1=player(x,y,z,map,name,pi,srate)
	p1.hidden=hidden
	g.players.append(p1)
	for i in g.players:
		i.friendcount=0
		if g.players[len(g.players)-1].hidden: continue
		if i.friendonlinemessage==1 and g.players[len(g.players)-1].name in i.friendlist: g.n.send_reliable(i.peer_id,"online "+str(x)+" "+str(y)+" "+str(z)+" "+name+" "+map+" "+str(srate), 0)
		else: g.n.send_reliable(i.peer_id,"online2 "+str(x)+" "+str(y)+" "+str(z)+" "+name+" "+map+" "+str(srate), 0)
	
def get_timeditem_duration(item):
	if item=="MosinNagant":
		return 604800000
	if item=="KelTecP318":
		return 1296000000

	if item=="maverick88":
		return 604800000

	return -1
import math

def ms_to_readable_time(milliseconds):
	milliseconds = math.floor(milliseconds*1000)
	seconds = math.floor((milliseconds / 1000) % 60)
	minutes = math.floor((milliseconds / (1000 * 60)) % 60)
	hours = math.floor((milliseconds / (1000 * 60 * 60)) % 24)
	days = math.floor(milliseconds / (1000 * 60 * 60 * 24))
	
	time_components = []

	if days >= 365:
		years = days // 365
		time_components.append(f"{years} {plural(years, 'year', 'years')}")
		days %= 365

	if days >= 30:
		months = days // 30
		time_components.append(f"{months} {plural(months, 'month', 'months')}")
		days %= 30

	if days >= 7:
		weeks = days // 7
		time_components.append(f"{weeks} {plural(weeks, 'week', 'weeks')}")
		days %= 7

	if days > 0:
		time_components.append(f"{days} {plural(days, 'day', 'days')}")

	if hours > 0:
		time_components.append(f"{hours} {plural(hours, 'hour', 'hours')}")

	if minutes > 0:
		time_components.append(f"{minutes} {plural(minutes, 'minute', 'minutes')}")

	time_components.append(f"{seconds} {plural(seconds, 'second', 'seconds')}")

	return ", ".join(time_components)

def plural(n, singular, plural):
	if n == 1:
		return singular
	return plural
def minutes_to_timestamp(minutes):
    current_time = int(time.time())
    future_time = current_time + (minutes * 60)  
    return int(future_time)  
def send_platform(p, minx, maxx, miny, maxy, minz, maxz, tile):
	g.n.send_reliable(p.peer_id, "addplatform " + str(round(minx)) + " " + str(round(maxx)) + " " + str(round(miny)) + " " + str(round(maxy)) + " " + str(round(minz)) + " " + str(round(maxz)) + " " + tile, 4)

def has_line_of_sight(start_x, start_y, start_z, end_x, end_y, end_z, map):
    return True
    start_x=round(start_x)
    start_y=round(start_y)
    start_z=round(start_z)
    end_x=round(end_x)
    end_y=round(end_y)
    end_z=round(end_z)

    # Implement a simple ray-casting algorithm
    steps = max(abs(end_x - start_x), abs(end_y - start_y), abs(end_z - start_z))
    if steps == 0:
        return True

    dx = (end_x - start_x) / steps
    dy = (end_y - start_y) / steps
    dz = (end_z - start_z) / steps

    x, y, z = start_x, start_y, start_z

    for _ in range(int(steps)):
        x += dx
        y += dy
        z += dz
        if "wall" in get_tile_at(int(x), int(y), int(z), map):
            return False
    return True
def place_barricade(x,y,z,map,owner):
	x=round(x)
	y=round(y)
	z=round(z)
	b=barricade(x,x,y,y,z,z+9,map,"wallbarricade",owner)
	g.barricades.append(b)
def place_ladder(x,y,z,map,owner):
	x=round(x)
	y=round(y)
	z=round(z)

	b=ladder(x,x,y,y,z,z+20,map,"ladder",owner)
	g.ladders.append(b)