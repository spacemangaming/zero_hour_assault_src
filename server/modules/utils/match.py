import globals as g
import math
from timer import timer
from loot import spawn_loot
import pickle
from file_directories import file_delete, file_exists
from file_directories import file_get_contents, file_put_contents
from item import spawn_item
from zombie import spawn_zombie
from npc import npc
from npc import usernames
from variable_management import string_replace, string_contains, string_split
from flag import spawn_flag
from random import choice
from random import randint as random
import time
import copy
from motor import remove_platform, send_platform
from moving_sound_serverside_handler import update_moving_sound, destroy_moving_sound, spawn_moving_sound
class match:
	def __init__(self,owner,playerinoneteam,mode,password,botcount):
		self.players=[]
		self.redgot=0
		self.bluegot=0
		self.endtimer=timer()
		self.endannouncetimer=timer()
		self.max_items=200
		self.shrink_count=0
		self.startcounter=4
		self.starttimer=timer()
		self.shrinktimer=timer()
		self.deadplayers=[]
		self.removeplayertimer=timer()
		self.maxx=500
		self.thingtimer=timer()
		self.maxy=500
		self.spectators=[]
		self.botadded=False
		self.lootspawntimer=timer()
		self.itemspawntimer=timer()
		self.redhousex=-50
		self.redhousey=-50
		self.bluehousex=-50
		self.bluehousey=-50

		self.inprogress=False
		self.redleader=""
		self.blueleader=""
		self.zombietimer=timer()
		self.reddoorhealth=100
		self.bluedoorhealth=100
		self.botcount=botcount
		self.playersinoneteam=0
		self.redflagpoint=0
		self.blueflagpoint=0
		self.password=password
		self.mode=mode
		#self.mapname=""
		import data_loader
		mode_config = data_loader.get_match_mode(self.mode)
		self.mapname = mode_config.get("map", "main") if mode_config else "main"
		self.playersinoneteam=playerinoneteam
		self.owner=owner
		self.helitimer=timer()
		self.started=False
		self.starting=False
		m=g.get_map_index(self.mapname)
		self.maxx=g.maps[m].max.x
		self.maxy=g.maps[m].max.y
	def startloop(self):
		if self.starting and self.starttimer.elapsed>1000:
			self.starttimer.restart()
			self.startcounter-=1
			if self.startcounter!=0: self.send(str(self.startcounter),0)
			else: self.send("go!",0)
			if self.startcounter<=0:
				self.starting=False
				self.start()
	def givezhtokenteam(self,t):
		for p in self.players:
			if g.getpc(p) is None: continue
			try:
				if g.getpc(p).matchteam==t:
					if not g.getpc(p).paid: g.getpc(p).zhtoken+=1
					if g.getpc(p).paid: g.getpc(p).zhtoken+=2
			except:
				pass
			try:
				if g.getpc(p).matchteam==t: g.getpc(p).health=g.getpc(p).maxhealth
			except: pass
		for p in self.deadplayers:
			if g.getpc(p) is None: continue
			try:

				if g.getpc(p).matchteam==t:
					if not g.getpc(p).paid: g.getpc(p).zhtoken+=1
					if g.getpc(p).paid: g.getpc(p).zhtoken+=2
			except: pass
			try:
				if g.getpc(p).matchteam==t: g.getpc(p).health=g.getpc(p).maxhealth
			except: pass
	def givezhtokenteamten(self,t):
		for p in self.players:
			if g.getpc(p) is None: continue
			try:
				if g.getpc(p).matchteam==t:
					if not g.getpc(p).paid: g.getpc(p).zhtoken+=10
					if g.getpc(p).paid: g.getpc(p).zhtoken+=20

			except:
				pass
			try:
				if g.getpc(p).matchteam==t: g.getpc(p).health=g.getpc(p).maxhealth
			except: pass
		for p in self.deadplayers:
			if g.getpc(p) is None: continue
			try:
				if g.getpc(p).matchteam==t:
					if not g.getpc(p).paid: g.getpc(p).zhtoken+=10
					if g.getpc(p).paid: g.getpc(p).zhtoken+=20

			except: pass
			try:
				if g.getpc(p).matchteam==t: g.getpc(p).health=g.getpc(p).maxhealth
			except: pass


	def givezhtoken(self,n):
		for p in self.players:
			if g.getpc(p) is None: continue
			try:
				if g.getpc(p).name==n:
					if not g.getpc(p).paid: g.getpc(p).zhtoken+=1
					if g.getpc(p).paid: g.getpc(p).zhtoken+=2
			except:
				pass
			try:
				if g.getpc(p).name==n: g.getpc(p).health=g.getpc(p).maxhealth
			except: pass

	def cancel(self):
		self.send("startmoving",0)
		for i in range(len(self.players)):
			try:
				index=g.get_player_index_from(self.players[i])
				if index>-1:
					j=g.players[index]
					item_map={}
					for item in g.dontlose:
						if j is not None and j.get_item_count(item)>0: item_map[item]=j.get_item_count(item)
					try: j.inv=dict()
					except: pass
					for item in item_map.keys():
						if j is not None: j.give(item,item_map[item])


				g.move_player(g.get_player_index_from(self.players[i]),5,0,0,"lobby")
				g.players[g.get_player_index_from(self.players[i])].joinedmatch=""
				g.players[g.get_player_index_from(self.players[i])].matchteam=""
			except: pass
		if self.mode=="teamz": self.clearzombies()
		for n in g.npcs:
			if n.map==self.get_cwmap():
				n.health=0; n.dontkill=True
				n.hitby=""
				n.hitby2=""
		self.clearitems()
		file_delete("maps/match"+self.owner+".map")
		file_delete("maps/main"+self.owner+".map")
		file_delete("maps/flag"+self.owner+".map")
		file_delete("maps/combo"+self.owner+".map")
		file_delete("maps/zombie"+self.owner+".map")
		file_delete("maps/knife"+self.owner+".map")
		file_delete("maps/zombie2"+self.owner+".map")
		file_delete("maps/helicopter"+self.owner+".map")
		file_delete("maps/sword"+self.owner+".map")
		file_delete("maps/one_shot_one_kill"+self.owner+".map")
		file_delete("maps/snow"+self.owner+".map")

		file_delete("maps/abyss_clash"+self.owner+".map")

		g.init_mapsystem()
		try: g.matches.remove(self)
		except: pass
	def leave(self,p):
		p.packet("startmoving",0)
		g.move_player(g.get_player_index_from(p.name),5,0,0,"lobby")
		try: self.players.remove(p.name)
		except: pass
		self.send(p.name+" left the match!",2)
		self.send("play_s misc36.ogg",0)
		p.joinedmatch=""
		p.matchteam=""
	def clearzombies(self):
		for z in g.zombies:
			if z.m==self.owner: z.health=0
	def clearitems(self):
		for z in g.items:
			try:
				if z.map==self.get_cwmap(): g.items.remove(z)
			except: pass

	def helicopterloop(self,p):
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
				if string_contains(g.get_tile_at(p.x,p.y,p.z,p.map),"wall",1)>-1:
					p.x-=1
					if not p.hidden: g.n.broadcast("update_player2 "+str(p.x)+" "+str(p.y)+" "+str(p.z)+" "+p.map+" "+p.name+" "+str(p.facing),20)

				g.n.send_reliable(p.peer_id,"move "+str(p.x)+" "+str(p.y)+" "+str(p.z),0)

			if p.x>p.targetx:
				p.x-=1
				if not p.hidden: g.n.broadcast("update_player2 "+str(p.x)+" "+str(p.y)+" "+str(p.z)+" "+p.map+" "+p.name+" "+str(p.facing),20)
				if string_contains(g.get_tile_at(p.x,p.y,p.z,p.map),"wall",1)>-1:
					p.x+=1
					if not p.hidden: g.n.broadcast("update_player2 "+str(p.x)+" "+str(p.y)+" "+str(p.z)+" "+p.map+" "+p.name+" "+str(p.facing),20)

				g.n.send_reliable(p.peer_id,"move "+str(p.x)+" "+str(p.y)+" "+str(p.z),0)

			if p.y>p.targety:
				p.y-=1

				if not p.hidden: g.n.broadcast("update_player2 "+str(p.x)+" "+str(p.y)+" "+str(p.z)+" "+p.map+" "+p.name+" "+str(p.facing),20)
				if string_contains(g.get_tile_at(p.x,p.y,p.z,p.map),"wall",1)>-1:
					p.y+=1

					if not p.hidden: g.n.broadcast("update_player2 "+str(p.x)+" "+str(p.y)+" "+str(p.z)+" "+p.map+" "+p.name+" "+str(p.facing),20)


				g.n.send_reliable(p.peer_id,"move "+str(p.x)+" "+str(p.y)+" "+str(p.z),0)

			if p.y<p.targety:
				p.y+=1

				if not p.hidden: g.n.broadcast("update_player2 "+str(p.x)+" "+str(p.y)+" "+str(p.z)+" "+p.map+" "+p.name+" "+str(p.facing),20)
				if string_contains(g.get_tile_at(p.x,p.y,p.z,p.map),"wall",1)>-1:
					p.y-=1

					if not p.hidden: g.n.broadcast("update_player2 "+str(p.x)+" "+str(p.y)+" "+str(p.z)+" "+p.map+" "+p.name+" "+str(p.facing),20)


				g.n.send_reliable(p.peer_id,"move "+str(p.x)+" "+str(p.y)+" "+str(p.z),0)

	def heliendloop(self):
		if self.helitimer.elapsed>=30000 and self.started and not self.inprogress:
			self.helitimer.restart()
			self.helitimer.pause()

			file_delete("maps/helicopter"+self.owner+".map")
			g.init_mapsystem()
			for p in self.players:
				p2=g.getpc(p)
				if p2 is not None:
					if p2.map=="helicopter"+self.owner: g.move_player(g.get_player_index_from(p),p2.x,p2.y,119,self.get_cwmap())
			import data_loader
			mode_config = data_loader.get_match_mode(self.mode)
			is_team = mode_config.get("team_based", True) if mode_config else True
			required_players = self.playersinoneteam * 2 if is_team else self.playersinoneteam
			if self.botcount==-1 and len(self.players)<required_players: 
				self.botadded=True
				counter=len(self.players)
				while(counter<required_players):
					g.npcs.append(npc(0, 0, "bot", self.get_cwmap(), "botbeacon", 150, 1, 1, 30, 50, "voice", 16, "nothing", 0, 5000, 30, 100, "voice17", 0, 10, 0, self.maxx, 0, self.maxy, 0, 750, 5, 200, self.owner, self.get_free_team()))
					counter+=1
			self.inprogress=True

	def start(self):
		if self.started: return
		startplayers=len(self.players)
		self.started=True
		self.starting=True


		for p in g.players:
			if p.matchmessage==1 and p.map=="lobby":
				g.n.send_reliable(p.peer_id,"Match of "+self.owner+" type "+self.get_mode()+" started!",2)
				g.n.send_reliable(p.peer_id,"play_s misc13.ogg",0)
		self.lootspawntimer.restart()
		self.send("stopmoving",0)
		self.starting=False
		if len(self.players)!=startplayers or g.getpc(self.owner) is None: self.cancel(); return
		if self.mode=="teamk2" or self.mode=="teamk2" or self.mode=="teamk": self.send("draw knife",0)
		if self.mode=="teamf2" or self.mode=="teamf": self.send("draw punch",0); self.send("draw2 feet",0)
		if self.mode=="teamminecraft" or self.mode=="minecraft": self.send("draw stick",0)
		if self.mode=="sword" or self.mode=="teamsword": self.send("draw wooden_sword",0)
		if self.mode=="sniper" or self.mode=="teamsniper": self.send("draw mkek_jng90",0)
		if self.mode=="snow" or self.mode=="teamsnow": self.send("draw punch",0); self.send("draw2 feet",0)
		for i in g.items:
			if i.map==self.get_cwmap(): g.items.remove(i)
		self.send("play_s countdownfinish.ogg",0)

		mainmap= string_replace(file_get_contents("maps/"+self.mapname+".map"),"mapname:"+self.mapname,"mapname:"+self.mapname+self.owner,False)
		ind=g.get_map_index(self.mapname)
		for wall in g.maps[ind].mapwalls:
			mainmap+="\nplatform:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type)
			mainmap=mainmap.replace("wall:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type),"")
			wall.health=50
			wall.destroyed=False
		file_put_contents("maps/"+self.mapname+self.owner+".map",mainmap)
		helicoptermap=string_replace(file_get_contents("maps/helicopter.map"),"mapname:helicopter","mapname:helicopter"+self.owner,False)
		helicoptermap=helicoptermap.replace("maxx:500","maxx:500")
		helicoptermap=helicoptermap.replace("maxy:500","maxy:500")
		file_put_contents("maps/helicopter"+self.owner+".map",helicoptermap)
		g.init_mapsystem()
		self.helitimer.restart()
		import data_loader
		mode_config = data_loader.get_match_mode(self.mode)
		use_heli = mode_config.get("use_helicopter", False) if mode_config else False
		if use_heli:
			self.send("play_s helicopterstart.ogg",0)
			delay(1500)
		self.send("startmoving",0)
		for p in self.players:
			if g.get_player_index_from(p)>-1:
				index=g.get_player_index_from(p)
				j=g.players[index]
				j.health=j.maxhealth
				if self.mode=="teamf" or self.mode=="teamf2": g.players[index].give("revival_nectar",2)
				if self.mode=="teamk" or self.mode=="teamk2": g.players[index].give("knife",1)
				if self.mode!="snow" and self.mode!="teamsnow" and self.mode!="sniper" and self.mode!="teamsniper" and self.mode!="teamk2" and self.mode!="teamf2" and self.mode!="teamf" and self.mode!="g" and self.mode!="g2" and self.mode!="teamg" and self.mode!="teamg2" and self.mode!="teamk" and self.mode!="teamf" and self.mode!="minecraft" and self.mode!="sword" and self.mode!="teamsword" and self.mode!="teamcollect" and self.mode!="collect" and self.mode!="teamminecraft":
#					g.players[index].give("mkek_yavuz16",1)
#					g.players[index].give("9mm",30)
					g.players[index].randomweapongive()
					g.players[index].give("small_potion",3)
					g.players[index].give("vitality_potion",2)
					g.players[index].give("revival_nectar",1)

					g.players[index].give("parachute",1)
					g.players[index].give("molotov_cocktail",2)
				else:
					if self.mode=="sniper" or self.mode=="teamsniper":
						g.players[index].give("mkek_jng90",1)
						g.players[index].give("dragunov_psl",1)

						g.players[index].give("7.62x51mm",500)
					if self.mode=="g2" or self.mode=="teamg2" or self.mode=="g" or self.mode=="teamg" or self.mode=="teamg2":
						g.players[index].give("vitality_potion",5)
						if self.mode!="teamg2" and self.mode!="g2": g.players[index].give("molotov_cocktail",5)
						g.players[index].give("hand_grenade",20)
						g.players[index].give("metal_shield",2)
					if self.mode=="minecraft" or self.mode=="teamminecraft":
						g.players[index].give("vitality_potion",3)
					if self.mode=="sword" or self.mode=="teamsword":
						g.players[index].give("wooden_sword",1)
						g.players[index].give("vitality_potion",2)
					else:
						if self.mode!="collect" and self.mode!="teamcollect" and self.mode!="teamf" and self.mode!="teamf2" and self.mode!="sniper" and self.mode!="teamsniper" and self.mode!="snow" and self.mode!="teamsnow":
							g.players[index].give("small_potion",3)
							g.players[index].give("vitality_potion",2)
							g.players[index].give("revival_nectar",1)

				g.n.send_reliable(g.players[index].peer_id,pickle.dumps(g.players[index].inv),19)
				if self.mode!="snow" and self.mode!="teamcollect" and self.mode!="collect" and self.mode!="teamsnow" and self.mode!="sniper" and self.mode!="teamsniper" and self.mode!="teamk2" and self.mode!="teamf2" and self.mode!="sword" and self.mode!="teamsword" and self.mode!="teamg2" and self.mode!="g2" and self.mode!="g" and self.mode!="teamg" and self.mode!="teamc" and self.mode!="teamz2" and self.mode!="teamk" and self.mode!="teamf" and self.mode!="minecraft" and self.mode!="teamminecraft":
					g.move_player(g.get_player_index_from(p),random(0,500),random(0,500),0,"helicopter"+self.owner)
					g.getpc(p).helijumptimer.restart()
				else:
					if self.mode!="sword" and self.mode!="teamsword" and self.mode!="g2" and self.mode!="teamg2": g.move_player(g.get_player_index_from(p),random(0,self.maxx),random(0,self.maxy),0,self.get_cwmap())
					if self.mode=="g2" or self.mode=="teamg2": g.move_player(g.get_player_index_from(p),random(0,75),random(0,45),1,self.get_cwmap())
					if self.mode=="sword" or self.mode=="teamsword": g.move_player(g.get_player_index_from(p),random(0,50),random(0,19),0,self.get_cwmap())
		if "minecraft" in self.mode:
			for i in range(100):
				itemamount=random(0,3)
				spawn_chest(random(0,self.maxx),random(0,self.maxy),0,self.get_cwmap())
				itemlist=["arrow","bow","wooden_sword_body","wooden_sword_handle","diamond_sword_body","diamond_sword_handle","iron_sword_body","iron_sword_handle","small_potion","vitality_potion","revival_nectar"]
				chest=g.chests[len(g.chests)-1]
				for j in range(itemamount):
					item=choice(itemlist)
					chest.items.append(item)
					chest.itemamounts.append(random(1,getmaxamountchest(item)))
		if self.mode=="teamc":
			spawn_flag(random(0, 100), random(0, 100), 0, self.get_cwmap(), "red")
			spawn_flag(random(0, 100), random(0, 100), 0, self.get_cwmap(), "blue")
		import data_loader
		mode_config = data_loader.get_match_mode(self.mode)
		use_heli = mode_config.get("use_helicopter", False) if mode_config else False
		if not use_heli:
			is_team = mode_config.get("team_based", True) if mode_config else True
			required_players = self.playersinoneteam * 2 if is_team else self.playersinoneteam
			if self.botcount==-1 and len(self.players)<required_players: 
				self.botadded=True
				counter=len(self.players)
				while(counter<required_players):
					g.npcs.append(npc(0, 0, "bot", self.get_cwmap(), "botbeacon", 150, 1, 1, 30, 50, "voice", 16, "nothing", 0, 5000, 30, 100, "voice17", 0, 10, 0, self.maxx, 0, self.maxy, 0, 750, 5, 200, self.owner, self.get_free_team()))
					counter+=1
			self.inprogress=True
	def get_max_item_amount(self):
		if "collect" in self.mode or self.mode=="teamc": return 15
		if "sword" in self.mode: return 10
		if self.mode=="g" or self.mode=="teamg" or self.mode=="g2" or self.mode=="teamg2": return 10
		else: return self.max_items
	def get_free_team(self):
		if self.players_on_team("red")<self.playersinoneteam: return "red"
		else: return "blue"
	def players_on_team(self,team):
		ret=0
		for p in self.players:
			pl=g.getpc(p)
			if pl is not None and pl.matchteam==team: ret+=1
		for n in g.npcs:
			if n.joinedmatch == self.owner and n.matchteam == team and n.health > 0:
				ret += 1
		return ret
	def player_list_on_team(self,team):
		ret=""
		for p in self.players:
			pl=g.getpc(p)
			if pl is not None and pl.matchteam==team: ret+=p+", "
		for n in g.npcs:
			if n.joinedmatch == self.owner and n.matchteam == team and n.health > 0:
				ret += n.name + ", "
		return ret

	def get_mode(self):
		import data_loader
		mode_config = data_loader.get_match_mode(self.mode)
		if mode_config:
			return mode_config.get("display_name", self.mode)
		return self.mode

	def get_cwmap(self):
		return self.mapname+self.owner
	def get_cwmap2(self):
		return "match"+self.owner

	def send(self, mess, chan, killn=False):
		if chan==2:
			mess="matchmessage "+mess
			chan=0
		sented=[]
		for p in self.players:
			i=g.get_player_index_from(p)
			if i>-1:
				if g.players[i].killn==0 and killn: continue
				if p not in sented: sented.append(p); g.n.send_reliable(g.players[i].peer_id,mess,chan)
				if killn: g.n.send_reliable(g.players[i].peer_id,"play_s teammessage2.ogg",0)
		for p in self.deadplayers:
			i=g.get_player_index_from(p)
			if i>-1:
				if g.players[i].killn==0 and killn: continue
				if p not in sented: sented.append(p); g.n.send_reliable(g.players[i].peer_id,mess,chan)
				if killn: g.n.send_reliable(g.players[i].peer_id,"play_s teammessage2.ogg",0)

		for p in self.spectators:
			i=g.get_player_index_from(p)
			if i>-1:
				if g.players[i].killn==0 and killn: continue
				if p not in sented: sented.append(p); g.n.send_reliable(g.players[i].peer_id,mess,chan)
				if killn: g.n.send_reliable(g.players[i].peer_id,"play_s teammessage2.ogg",0)
	def send_except(self, pl, mess, chan, killn=False):
		if chan==2:
			mess="matchmessage "+mess
			chan=0
		sented=[]
		for p in self.players:
			if p==pl: continue
			i=g.get_player_index_from(p)
			if i>-1:
				if g.players[i].killn==0 and killn: continue
				if p not in sented: sented.append(p); g.n.send_reliable(g.players[i].peer_id,mess,chan)
				if killn: g.n.send_reliable(g.players[i].peer_id,"play_s teammessage2.ogg",0)
		for p in self.deadplayers:
			if p==pl: continue
			i=g.get_player_index_from(p)
			if i>-1:
				if g.players[i].killn==0 and killn: continue
				if p not in sented: sented.append(p); g.n.send_reliable(g.players[i].peer_id,mess,chan)
				if killn: g.n.send_reliable(g.players[i].peer_id,"play_s teammessage2.ogg",0)

		for p in self.spectators:
			if p==pl: continue
			i=g.get_player_index_from(p)
			if i>-1:
				if g.players[i].killn==0 and killn: continue
				if p not in sented: sented.append(p); g.n.send_reliable(g.players[i].peer_id,mess,chan)
				if killn: g.n.send_reliable(g.players[i].peer_id,"play_s teammessage2.ogg",0)

	def send2(self, mess, chan, killn=False):
		if chan==2:
			mess="matchmessage "+mess
			chan=0
		sented=[]
		for p in g.players:
			i=g.get_player_index_from(p)
			if i>-1:
				if g.players[i].name in self.players: continue
				if g.players[i].killn==0 and killn: continue
				if p not in sented: sented.append(p); g.n.send_reliable(g.players[i].peer_id,mess,chan)
				if killn: g.n.send_reliable(g.players[i].peer_id,"play_s teammessage2.ogg",0)

	def teamsend(self, team, mess, chan):
		sented=[]
		if chan==2:
			mess="matchmessage "+mess
			chan=0

		for p in self.players:
			i=g.get_player_index_from(p)
			if i>-1:
				if p not in sented and g.players[i].matchteam==team: g.n.send_reliable(g.players[i].peer_id,mess,chan); sented.append(p)
		for p in self.deadplayers:
			i=g.get_player_index_from(p)
			if i>-1:
				if p not in sented and g.players[i].matchteam==team: g.n.send_reliable(g.players[i].peer_id,mess,chan); sented.append(p)

		for p in self.spectators:
			i=g.get_player_index_from(p)
			if i>-1:
				if p not in sented and g.players[i].matchteam==team: g.n.send_reliable(g.players[i].peer_id,mess,chan); sented.append(p)

	def add_spectator(self,name):
		i=g.get_player_index_from(name)
		g.players[i].specmatch=self.owner
		g.n.send_reliable(g.players[i].peer_id,"echo matchwatch "+self.players[0],0)
	def add_player(self,name,team):
		for p in self.players:
			if p==name: self.players.remove(p)

		p=g.players[g.get_player_index_from(name)]
		import data_loader
		mode_config = data_loader.get_match_mode(self.mode)
		is_team = mode_config.get("team_based", True) if mode_config else True
		if is_team:
			if self.players_on_team(team)>=self.playersinoneteam: g.n.send_reliable(p.peer_id,"team full",0); return
		else:
			if len(self.players)>=self.playersinoneteam: g.n.send_reliable(p.peer_id,"match full",0); return
		p2=g.players[g.get_player_index_from(self.owner)]
		if p.name in p2.matchbanned:
			g.n.send_reliable(p.peer_id,"Your banned from this player's all matches",0)
			return
		p.matchteam=team
		if self.redleader=="" and p.matchteam=="red": self.redleader=p.name
		if self.blueleader=="" and p.matchteam=="blue": self.blueleader=p.name

		p.joinedmatch=self.owner
		p.matchmode=self.mode
		if is_team: self.send(p.name+" joined! They're in the "+p.matchteam+" team, match needs "+str((self.playersinoneteam*2)-len(self.players)-1)+" more players. If the owner turned on bots, and the match gets started without enough players, bots will fill in.",2)
		if not is_team: self.send(p.name+" joined! match needs "+str((self.playersinoneteam*1)-len(self.players)-1)+" more players. If the owner turned on bots, and the match gets started without enough players, bots will fill in.",2)
		self.send("play_s misc35.ogg",0)
		g.move_player(g.get_player_index_from(p.name),0,0,0,"match"+self.owner)
		self.players.append(p.name)
		if self.mode=="teamz2" and p.matchteam=="blue": g.n.send_reliable(p.peer_id,"zombie",0)
		g.n.send_reliable(p.peer_id,"stopmoving",0)
def newmatch(owner,playerinoneteam,mode,password,botcount):
#	if mode!="teamd": return
	index=g.get_player_index_from(owner)
	if index>-1 and g.players[index].map!="lobby": return
#	if g.players[index].zhtoken<=0:
#		g.n.send_reliable(g.players[index].peer_id,"You need at least 1 zero token to be able to create a new match",0)
#		return
	g.players[index].mowner=owner
	g.players[index].mplayerinoneteam=playerinoneteam
	g.players[index].mmode=mode
	g.players[index].mpassword=password
	g.players[index].mbotcount=botcount
	import data_loader
	mode_config = data_loader.get_match_mode(mode)
	is_team = mode_config.get("team_based", True) if mode_config else True
	if not is_team: newmatch2(g.players[index].mowner,int(g.players[index].mplayerinoneteam),g.players[index].mmode,g.players[index].mpassword,g.players[index].mbotcount,""); return
	m=g.server_menu()
	m.intro="select team"
	m.initial_packet="matchteamselect2"
	m.add("red","red")
	m.add("blue","blue")
	m.send(g.players[index].peer_id)
def newmatch2(owner,playerinoneteam,mode,password,botcount,team):
	m=match(owner,int(playerinoneteam),mode,password,botcount)
	m.players.append(owner)
	if team=="red": m.redleader=owner
	if team=="blue": m.blueleader=owner
	if mode=="teamz":
		m.redhousex=random(0,m.maxx)
		m.bluehousex=random(0,m.maxx)
		m.redhousey=random(0,m.maxy)
		m.bluehousey=random(0,m.maxy)

	g.matches.append(m)
	matchmap=string_replace(file_get_contents("maps/match.map"),"mapname:match","mapname:match"+owner,False)
	file_put_contents("maps/match"+owner+".map",matchmap)
	if mode=="teamz":
		matchmap=string_replace(file_get_contents("maps/zombie.map"),"mapname:zombie","mapname:zombie"+owner,False)
		matchmap+=f"""
door:{m.redhousex}:{m.redhousey}:0:{m.redhousex}:{m.redhousey+2}:0:5000:houseenter.ogg:houseexit.ogg
door:{m.redhousex}:{m.redhousey+2}:0:{m.redhousex}:{m.redhousey}:0:5000:houseenter.ogg:houseexit.ogg
platform:{m.redhousex-1}:{m.redhousex-1}:{m.redhousey+2}:{m.redhousey+20}:0:10:walldoor
platform:{m.redhousex}:{m.redhousex+20}:{m.redhousey+1}:{m.redhousey+1}:0:10:walldoor
platform:{m.redhousex}:{m.redhousex+19}:{m.redhousey+2}:{m.redhousey+19}:0:0:hardwood
platform:{m.redhousex+20}:{m.redhousex+20}:{m.redhousey}:{m.redhousey+20}:0:10:walldoor
platform:{m.redhousex}:{m.redhousex+20}:{m.redhousey+20}:{m.redhousey+20}:0:10:walldoor
door:{m.bluehousex}:{m.bluehousey}:0:{m.bluehousex}:{m.bluehousey+2}:0:5000:houseenter.ogg:houseexit.ogg
door:{m.bluehousex}:{m.bluehousey+2}:0:{m.bluehousex}:{m.bluehousey}:0:5000:houseenter.ogg:houseexit.ogg
platform:{m.bluehousex-1}:{m.bluehousex-1}:{m.bluehousey+2}:{m.bluehousey+20}:0:10:walldoor
platform:{m.bluehousex}:{m.bluehousex+20}:{m.bluehousey+1}:{m.bluehousey+1}:0:10:walldoor
platform:{m.bluehousex}:{m.bluehousex+19}:{m.bluehousey+2}:{m.bluehousey+19}:0:0:hardwood
platform:{m.bluehousex+20}:{m.bluehousex+20}:{m.bluehousey}:{m.bluehousey+20}:0:10:walldoor
platform:{m.bluehousex}:{m.bluehousex+20}:{m.bluehousey+20}:{m.bluehousey+20}:0:10:walldoor
"""
		ind=g.get_map_index("zombie")
		nwalls=[]
		for wall in g.maps[ind].mapwalls:
			matchmap+="\nplatform:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type)
			matchmap=matchmap.replace("wall:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type),"")
			nwalls.append(copy.deepcopy(wall))
		file_put_contents("maps/zombie"+owner+".map",matchmap)
		g.init_mapsystem()
		ind=g.get_map_index("zombie"+owner)
		for item in nwalls:
			item.destroyed=False
			item.health=50
			g.maps[ind].mapwalls.append(copy.deepcopy(item))

	if mode=="teamc":
		matchmap=string_replace(file_get_contents("maps/flag.map"),"mapname:flag","mapname:flag"+owner,False)
		ind=g.get_map_index("flag")
		nwalls=[]
		for wall in g.maps[ind].mapwalls:
			matchmap+="\nplatform:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type)
			matchmap=matchmap.replace("wall:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type),"")
			nwalls.append(copy.deepcopy(wall))
		file_put_contents("maps/flag"+owner+".map",matchmap)
		g.init_mapsystem()
		ind=g.get_map_index("flag"+owner)
		for item in nwalls:
			item.destroyed=False
			item.health=50
			g.maps[ind].mapwalls.append(copy.deepcopy(item))
	if mode=="g" or mode=="teamg":
		matchmap=string_replace(file_get_contents("maps/grenade.map"),"mapname:grenade","mapname:grenade"+owner,False)
		ind=g.get_map_index("grenade")
		nwalls=[]
		for wall in g.maps[ind].mapwalls:
			matchmap+="\nplatform:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type)
			matchmap=matchmap.replace("wall:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type),"")
			nwalls.append(copy.deepcopy(wall))
		file_put_contents("maps/grenade"+owner+".map",matchmap)
		g.init_mapsystem()
		ind=g.get_map_index("grenade"+owner)
		for item in nwalls:
			item.destroyed=False
			item.health=50
			g.maps[ind].mapwalls.append(copy.deepcopy(item))
	if mode=="g2" or mode=="teamg2":
		matchmap=string_replace(file_get_contents("maps/abyss_clash.map"),"mapname:abyss_clash","mapname:abyss_clash"+owner,False)
		ind=g.get_map_index("abyss_clash")
		nwalls=[]
		for wall in g.maps[ind].mapwalls:
			matchmap+="\nplatform:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type)
			matchmap=matchmap.replace("wall:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type),"")
			nwalls.append(copy.deepcopy(wall))
		file_put_contents("maps/abyss_clash"+owner+".map",matchmap)
		g.init_mapsystem()
		ind=g.get_map_index("abyss_clash"+owner)
		for item in nwalls:
			item.destroyed=False
			item.health=50
			g.maps[ind].mapwalls.append(copy.deepcopy(item))


	if mode=="teamminecraft" or mode=="minecraft":
		matchmap=string_replace(file_get_contents("maps/minecraft.map"),"mapname:minecraft","mapname:minecraft"+owner,False)
		ind=g.get_map_index("minecraft")
		nwalls=[]
		for wall in g.maps[ind].mapwalls:
			matchmap+="\nplatform:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type)
			matchmap=matchmap.replace("wall:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type),"")
			nwalls.append(copy.deepcopy(wall))
		file_put_contents("maps/minecraft"+owner+".map",matchmap)
		g.init_mapsystem()
		ind=g.get_map_index("minecraft"+owner)
		for item in nwalls:
			item.destroyed=False
			item.health=50
			g.maps[ind].mapwalls.append(copy.deepcopy(item))

	if mode=="teamsword" or mode=="sword":
		matchmap=string_replace(file_get_contents("maps/sword.map"),"mapname:sword","mapname:sword"+owner,False)
		ind=g.get_map_index("sword")
		nwalls=[]
		for wall in g.maps[ind].mapwalls:
			matchmap+="\nplatform:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type)
			matchmap=matchmap.replace("wall:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type),"")
			nwalls.append(copy.deepcopy(wall))
		file_put_contents("maps/sword"+owner+".map",matchmap)
		g.init_mapsystem()
		ind=g.get_map_index("sword"+owner)
		for item in nwalls:
			item.destroyed=False
			item.health=50
			g.maps[ind].mapwalls.append(copy.deepcopy(item))


	if mode=="teamcollect" or mode=="collect":
		matchmap=string_replace(file_get_contents("maps/collect.map"),"mapname:collect","mapname:collect"+owner,False)
		ind=g.get_map_index("collect")
		nwalls=[]
		for wall in g.maps[ind].mapwalls:
			matchmap+="\nplatform:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type)
			matchmap=matchmap.replace("wall:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type),"")
			nwalls.append(copy.deepcopy(wall))
		file_put_contents("maps/collect"+owner+".map",matchmap)
		g.init_mapsystem()
		ind=g.get_map_index("collect"+owner)
		for item in nwalls:
			item.destroyed=False
			item.health=50
			g.maps[ind].mapwalls.append(copy.deepcopy(item))




	if mode=="teamz2":
		matchmap=string_replace(file_get_contents("maps/zombie2.map"),"mapname:zombie2","mapname:zombie2"+owner,False)
		ind=g.get_map_index("zombie2")
		nwalls=[]
		for wall in g.maps[ind].mapwalls:
			matchmap+="\nplatform:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type)
			matchmap=matchmap.replace("wall:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type),"")
			nwalls.append(copy.deepcopy(wall))
		file_put_contents("maps/zombie2"+owner+".map",matchmap)
		g.init_mapsystem()
		ind=g.get_map_index("zombie2"+owner)
		for item in nwalls:
			item.destroyed=False
			item.health=50
			g.maps[ind].mapwalls.append(copy.deepcopy(item))
	if mode=="teamk":
		matchmap=string_replace(file_get_contents("maps/knife.map"),"mapname:knife","mapname:knife"+owner,False)
		ind=g.get_map_index("knife")
		nwalls=[]
		for wall in g.maps[ind].mapwalls:
			matchmap+="\nplatform:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type)
			matchmap=matchmap.replace("wall:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type),"")
			nwalls.append(copy.deepcopy(wall))
		file_put_contents("maps/knife"+owner+".map",matchmap)
		g.init_mapsystem()
		ind=g.get_map_index("knife"+owner)
		for item in nwalls:
			item.destroyed=False
			item.health=50
			g.maps[ind].mapwalls.append(copy.deepcopy(item))
	if mode=="teamf2" or mode=="teamf":
		matchmap=string_replace(file_get_contents("maps/combo.map"),"mapname:combo","mapname:combo"+owner,False)
		ind=g.get_map_index("combo")
		nwalls=[]
		for wall in g.maps[ind].mapwalls:
			matchmap+="\nplatform:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type)
			matchmap=matchmap.replace("wall:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type),"")
			nwalls.append(copy.deepcopy(wall))
		file_put_contents("maps/combo"+owner+".map",matchmap)
		g.init_mapsystem()
		ind=g.get_map_index("combo"+owner)
		for item in nwalls:
			item.destroyed=False
			item.health=50
			g.maps[ind].mapwalls.append(copy.deepcopy(item))

	if mode=="snow" or mode=="teamsnow":
		matchmap=string_replace(file_get_contents("maps/snow.map"),"mapname:snow","mapname:snow"+owner,False)
		ind=g.get_map_index("snow")
		nwalls=[]
		for wall in g.maps[ind].mapwalls:
			matchmap+="\nplatform:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type)
			matchmap=matchmap.replace("wall:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type),"")
			nwalls.append(copy.deepcopy(wall))
		file_put_contents("maps/snow"+owner+".map",matchmap)
		g.init_mapsystem()
		ind=g.get_map_index("snow"+owner)
		for item in nwalls:
			item.destroyed=False
			item.health=50
			g.maps[ind].mapwalls.append(copy.deepcopy(item))

	if mode=="sniper" or mode=="teamsniper":
		matchmap=string_replace(file_get_contents("maps/one_shot_one_kill.map"),"mapname:one_shot_one_kill","mapname:one_shot_one_kill"+owner,False)
		ind=g.get_map_index("one_shot_one_kill")
		nwalls=[]
		for wall in g.maps[ind].mapwalls:
			matchmap+="\nplatform:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type)
			matchmap=matchmap.replace("wall:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type),"")
			nwalls.append(copy.deepcopy(wall))
		file_put_contents("maps/one_shot_one_kill"+owner+".map",matchmap)
		g.init_mapsystem()
		ind=g.get_map_index("one_shot_one_kill"+owner)
		for item in nwalls:
			item.destroyed=False
			item.health=50
			g.maps[ind].mapwalls.append(copy.deepcopy(item))


	if mode=="teamk2":
		matchmap=string_replace(file_get_contents("maps/knife.map"),"mapname:knife","mapname:knife"+owner,False)
		ind=g.get_map_index("knife")
		nwalls=[]
		for wall in g.maps[ind].mapwalls:
			matchmap+="\nplatform:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type)
			matchmap=matchmap.replace("wall:"+str(wall.minx)+":"+str(wall.maxx)+":"+str(wall.miny)+":"+str(wall.maxy)+":"+str(wall.minz)+":"+str(wall.maxz)+":"+str(wall.type),"")
			nwalls.append(copy.deepcopy(wall))
		file_put_contents("maps/knife"+owner+".map",matchmap)
		g.init_mapsystem()
		ind=g.get_map_index("knife"+owner)
		for item in nwalls:
			item.destroyed=False
			item.health=50
			g.maps[ind].mapwalls.append(copy.deepcopy(item))



	g.move_player(g.get_player_index_from(owner),0,0,0,m.get_cwmap2())
	g.players[g.get_player_index_from(owner)].joinedmatch=owner
	g.players[g.get_player_index_from(owner)].matchmode=mode
	g.players[g.get_player_index_from(owner)].matchteam="red"
	g.players[g.get_player_index_from(owner)].matchteam=team
	owner_pc=g.getpc(owner)
	if owner_pc is None or not owner_pc.hidden:
		for ii in g.players:
			if ii.map=="lobby" and ii.matchmessage==1:
				import data_loader
				mode_config = data_loader.get_match_mode(m.mode)
				is_team = mode_config.get("team_based", True) if mode_config else True
				required_size = m.playersinoneteam * 2 if is_team else m.playersinoneteam
				if m.password=="": g.n.send_reliable(ii.peer_id,"The player "+owner+" created a new public match! The match mode is "+m.get_mode()+", Amount of members required is "+str(required_size),2)
				if m.password!="": g.n.send_reliable(ii.peer_id,"The player "+owner+" created a new private match! The match mode is "+m.get_mode()+", Amount of members required is "+str(required_size),2)
			if ii.map=="lobby" and ii.matchmessage==1: g.n.send_reliable(ii.peer_id,"play_s misc260.ogg",0)
	if mode=="teamz2" and g.players[g.get_player_index_from(owner)].matchteam=="blue": g.n.send_reliable(g.players[g.get_player_index_from(owner)].peer_id,"zombie",0)
	g.n.send_reliable(g.players[g.get_player_index_from(owner)].peer_id,"stopmoving",0)
def matchloop():
	for m in g.matches:
		m.heliendloop()
		m.startloop()
		if not hasattr(m,"endtimer"): m.endtimer=timer()
		if not hasattr(m,"endannouncetimer"): m.endannouncetimer=timer()
		if m.endannouncetimer.elapsed>60000 and "collect" in m.mode:
			m.endannouncetimer.restart()
			m.send("match will end after "+ms_to_readable_time(600000-m.endtimer.elapsed)+".",2)
		if m.endtimer.elapsed>600000:
			m.endtimer.restart()
			if m.mode=="teamcollect":
				if m.bluegot>m.redgot: winner="blue"
				else: winner="red"
				m.send("Match ended. "+winner+" team won! red team collected golds: "+str(m.redgot)+". Blue team collected golds: "+str(m.bluegot),2)
				m.givezhtokenteamten(winner)
				if winner=="blue":
					m.teamsend("blue","play_s win.ogg",0)
					m.teamsend("red","play_s misc171.ogg",0)
				if winner=="red":
					m.teamsend("red","play_s win.ogg",0)
					m.teamsend("blue","play_s misc171.ogg",0)

				if m.mode=="teamz": m.clearzombies()
				for n in g.npcs:
					if n.map==m.get_cwmap():
						n.health=0; n.dontkill=True
						n.hitby=""
						n.hitby2=""

				for pl in m.players:
					p=g.getpc(pl)
					if p is not None:
						g.move_player(g.get_player_index_from(pl),5,0,0,"lobby"); g.getpc(pl).matchteam=""; g.getpc(pl).joinedmatch=""
					else:
						try: g.getpc(pl).matchteam=""; g.getpc(pl).joinedmatch=""
						except: pass
					j=g.getpc(pl)
					item_map={}
					for item in g.dontlose:
						if j is not None and j.get_item_count(item)>0: item_map[item]=j.get_item_count(item)
					try: g.getpc(pl).inv=dict()
					except: pass
					for item in item_map.keys():
						if j is not None: j.give(item,item_map[item])
				file_delete("maps/match"+m.owner+".map")
				file_delete("maps/main"+m.owner+".map");file_delete("maps/grenade"+m.owner+".map")
				file_delete("maps/flag"+m.owner+".map")
				file_delete("maps/combo"+m.owner+".map")
				file_delete("maps/zombie"+m.owner+".map")
				file_delete("maps/zombie2"+m.owner+".map")
				file_delete("maps/knife"+m.owner+".map")
				file_delete("maps/helicopter"+m.owner+".map")
				file_delete("maps/sword"+m.owner+".map")
				file_delete("maps/abyss_clash"+m.owner+".map")
				file_delete("maps/one_shot_one_kill"+m.owner+".map")
				file_delete("maps/snow"+m.owner+".map"); file_delete("maps/collect"+m.owner+".map")

				g.init_mapsystem()
				g.matches.remove(m)
				return

			if m.mode=="collect":
				players_items={}
				winner=m.players[0]
				for p in m.players:
					pl=g.getpc(p)
					if pl is not None: players_items[p]=pl.items_got
				max_item=0
				winner=""
				for p in list(players_items.keys()):
					if players_items[p]>max_item: max_item=players_items[p]; winner=p
				for p in list(players_items.keys()):
					if players_items[p]>max_item: max_item=players_items[p]; winner=p

				try: m.send("Match ended. "+winner+" won!",2)
				except: pass
				try: g.n.send_reliable(g.getpc(winner).peer_id,"play_s win.ogg",0)
				except: pass
				m.send_except(winner,"play_s misc171.ogg",0)
				try: g.move_player(g.get_player_index_from(winner),5,0,0,"lobby")
				except: pass
				for p in m.players:
					try: g.move_player(g.get_player_index_from(p),5,0,0,"lobby")
					except: pass
				try: g.getpc(winner).zhtoken+=10
				except: pass
				for p in m.players:
					j=g.getpc(p)
					item_map={}
					for item in g.dontlose:
						try:
							if j.get_item_count(item)>0: item_map[item]=j.get_item_count(item)
						except: pass
					try:
						j.inv=dict()
					except: pass
					for item in item_map.keys():
						try: j.give(item,item_map[item])
						except: pass
				if m.mode=="teamz": m.clearzombies()
				for n in g.npcs:
					if n.map==m.get_cwmap():
						n.health=0; n.dontkill=True
						n.hitby=""
						n.hitby2=""
	
				file_delete("maps/match"+m.owner+".map")
				file_delete("maps/main"+m.owner+".map");file_delete("maps/grenade"+m.owner+".map")
				file_delete("maps/flag"+m.owner+".map")
				file_delete("maps/combo"+m.owner+".map")
				file_delete("maps/zombie"+m.owner+".map")
				file_delete("maps/zombie2"+m.owner+".map")
				file_delete("maps/knife"+m.owner+".map")
				file_delete("maps/helicopter"+m.owner+".map")
				file_delete("maps/sword"+m.owner+".map")
				file_delete("maps/abyss_clash"+m.owner+".map")
				file_delete("maps/one_shot_one_kill"+m.owner+".map")
				file_delete("maps/snow"+m.owner+".map"); file_delete("maps/collect"+m.owner+".map")

				g.init_mapsystem()
				g.matches.remove(m)
				return

		if m.inprogress and m.shrinktimer.elapsed>1000 and (m.mode=="teamd" or m.mode=="teaml" or m.mode=="teamz2"):
			m.shrinktimer.restart()
			m.shrink_count+=1
			if m.shrink_count>=4:
				m.max_items-=1
				m.shrink_count=0
			if m.maxx>50: m.maxx-=1
			if m.maxy>50: m.maxy-=1
			m.send("maxx "+str(m.maxx),0)
			m.send("maxy "+str(m.maxy),0)
			for p in g.players:
				if p.map==m.get_cwmap() and p.x>m.maxx:
					p.x=m.maxx
					g.n.send_reliable(p.peer_id,"move "+str(p.x)+" "+str(p.y)+" "+str(p.z),0)
				if p.map==m.get_cwmap() and p.y>m.maxy:
					p.y=m.maxy
					g.n.send_reliable(p.peer_id,"move "+str(p.x)+" "+str(p.y)+" "+str(p.z),0)
			for p in g.motors:
				if p.map==m.get_cwmap() and p.x>m.maxx:
					p.x=m.maxx
				if p.map==m.get_cwmap() and p.y>m.maxy:
					p.y=m.maxy
			for p in g.npcs:
				if p.map==m.get_cwmap() and p.x>m.maxx:
					p.x=m.maxx
				if p.map==m.get_cwmap() and p.y>m.maxy:
					p.y=m.maxy

			for p in g.items:
				if p.map==m.get_cwmap() and p.x>m.maxx:
					p.x=m.maxx
				if p.map==m.get_cwmap() and p.y>m.maxy:
					p.y=m.maxy

			for p in g.corpses:
				if p.map==m.get_cwmap() and p.x>m.maxx:
					p.x=m.maxx
				if p.map==m.get_cwmap() and p.y>m.maxy:
					p.y=m.maxy



		if m.removeplayertimer.elapsed>120000:
			m.removeplayertimer.restart()
			for p in m.players:
				if g.get_player_index_fromnpc(p)==-1: m.players.remove(p)
			for p in m.deadplayers:
				if g.get_player_index_from(p)==-1: m.deadplayers.remove(p)

		if 1:
			if m.mode!="collect" and m.mode!="teamcollect" and m.mode!="snow" and m.mode!="teamsnow" and m.mode!="sniper" and m.mode!="teamsniper" and m.mode!="teamk2" and m.mode!="teamf2" and m.mode!="g" and m.mode!="teamsword" and m.mode!="teamg" and m.mode!="g2" and m.mode!="teamg2" and m.mode!="teamk" and m.mode!="teamf" and m.mode!="teamz" and m.mode!="minecraft" and m.mode!="sword" and m.mode!="teamminecraft" and m.inprogress and m.lootspawntimer.elapsed>=300000:
				m.lootspawntimer.restart()
				spawn_loot(random(0,m.maxx),random(0,m.maxy),0,m.get_cwmap(),m)
			if m.inprogress and m.mode!="teamk2" and m.mode!="teamf2" and m.mode!="snow" and m.mode!="teamsnow" and m.mode!="sniper" and m.mode!="teamsniper" and m.mode!="teamk" and m.mode!="teamf" and m.mode!="minecraft" and m.mode!="teamminecraft" and m.itemspawntimer.elapsed>(300 if m.mode!="teamg" and m.mode!="g" and m.mode!="sword" and m.mode!="teamsword" and m.mode!="teamg2" and m.mode!="g2" and m.mode!="teamc" else 1000) and items_on_map(m.get_cwmap())<m.get_max_item_amount():
				m.itemspawntimer.restart()

				if m.mode!="g" and m.mode!="teamg": itemlist=["invisibility_shield","steel_helmet","knife","barricade","ladder","9mm","7.62x54mmR","small_potion","dragunov_psl","mkek_jng90","7.62x51mm","mkek_mpt76k","5.56x45mm","IthicaM37","12_gauge","molotov_cocktail","colt1911","45_ACP","hand_grenade","m4","vitality_potion","revival_nectar","binoculars","tm62","timebomb","metal_shield","40S&W","22_LR_Long_Rifle"]
				if m.mode=="g" or m.mode=="teamg": itemlist=["hand_grenade","molotov_cocktail","vitality_potion"]
				if m.mode=="g2" or m.mode=="teamg2": itemlist=["hand_grenade","vitality_potion"]
				if m.mode=="sword" or m.mode=="teamsword": itemlist=["diamond_sword","small_potion","stone_sword","wooden_sword"]
				if m.mode=="collect" or m.mode=="teamcollect": itemlist=["gold"]
				res=choice(itemlist)
				spawn_item(random(0,m.maxx),random(0,m.maxy),0,m.get_cwmap(),res,random(1,getmaxamount(res)))

		if m.inprogress and m.mode=="teamz" and m.zombietimer.elapsed>=1000 and zombies_on_map(m.get_cwmap())<50:
			m.zombietimer.restart()
			spawn_zombie(random(0,m.maxx),random(0,m.maxy),0,m.get_cwmap(),m.owner)
		if m.thingtimer.elapsed>1000:
			m.thingtimer.restart()
			for p in m.players:
				p=g.getpc(p)
				if p is not None:
					if p.map=="helicopter"+m.owner: m.helicopterloop(p)
					if m.inprogress and p.map!=m.get_cwmap(): m.players.remove(p.name); break
					if p.map=="massacre_in_the_city": m.players.remove(p.name); break
			if m.inprogress and m.players_on_team("red")==0 and m.mode!="teaml" and m.mode!="snow" and m.mode!="sniper" and m.mode!="teamk2" and m.mode!="teamf2" and m.mode!="g" and m.mode!="g2" and m.mode!="sword" and m.mode!="minecraft" and m.mode!="collect" and m.mode!="teamc":
				m.send("Match ended. Blue team won!",2)
				m.teamsend("blue","play_s win.ogg",0)
				m.teamsend("red","play_s misc171.ogg",0)
				if m.mode=="teamz": m.clearzombies()
				for n in g.npcs:
					if n.map==m.get_cwmap():
						n.health=0; n.dontkill=True
						n.hitby=""
						n.hitby2=""

				for pl in m.players:
					p=g.getpc(pl)
					if p is not None and p.matchteam=="blue":
						g.move_player(g.get_player_index_from(pl),5,0,0,"lobby"); g.getpc(pl).matchteam=""; g.getpc(pl).joinedmatch=""
					else:
						try: g.getpc(pl).matchteam=""; g.getpc(pl).joinedmatch=""
						except: pass
					j=g.getpc(pl)
					item_map={}
					for item in g.dontlose:
						if j is not None and j.get_item_count(item)>0: item_map[item]=j.get_item_count(item)
					try: g.getpc(pl).inv=dict()
					except: pass
					for item in item_map.keys():
						if j is not None: j.give(item,item_map[item])
				file_delete("maps/match"+m.owner+".map")
				file_delete("maps/main"+m.owner+".map");file_delete("maps/grenade"+m.owner+".map")
				file_delete("maps/flag"+m.owner+".map")
				file_delete("maps/combo"+m.owner+".map")
				file_delete("maps/zombie"+m.owner+".map")
				file_delete("maps/zombie2"+m.owner+".map")
				file_delete("maps/knife"+m.owner+".map")
				file_delete("maps/helicopter"+m.owner+".map")
				file_delete("maps/sword"+m.owner+".map")
				file_delete("maps/abyss_clash"+m.owner+".map")
				file_delete("maps/one_shot_one_kill"+m.owner+".map")
				file_delete("maps/snow"+m.owner+".map"); file_delete("maps/collect"+m.owner+".map")

				g.init_mapsystem()
				try: g.matches.remove(m)
				except: pass
				return
			if m.inprogress and m.players_on_team("blue")==0 and m.mode!="teaml" and m.mode!="snow" and m.mode!="sniper" and m.mode!="teamk2" and m.mode!="teamf2" and m.mode!="sword" and m.mode!="g" and m.mode!="g2" and m.mode!="minecraft" and m.mode!="collect" and m.mode!="teamc":
				m.send("Match ended. Red team won!",2)
				m.teamsend("red","play_s win.ogg",0)
				m.teamsend("blue","play_s misc171.ogg",0)
	
				if m.mode=="teamz": m.clearzombies()
				for n in g.npcs:
					if n.map==m.get_cwmap():
						n.health=0; n.dontkill=True
						n.hitby=""
					n.hitby2	=""
	
				for pl in m.players:
					p=g.getpc(pl)
					if p is not None:
						if p.matchteam=="red":
							g.move_player(g.get_player_index_from(pl),5,0,0,"lobby"); g.getpc(pl).matchteam=""; g.getpc(pl).joinedmatch=""
					else:
						if g.getpc(pl) is not None: g.	getpc(pl).matchteam=""; g.getpc(pl).joinedmatch=""
					if 1:
						j=g.getpc(pl)
						item_map={}
						for item in g.dontlose:
							if j is not None and j.get_item_count(item)>0: item_map[item]=j.get_item_count(item)
						try: g.getpc(pl).inv=dict()
						except: pass
						for item in item_map.keys():
							if j is not None: j.give(item,item_map[item])
				file_delete("maps/match"+m.owner+".map")
				file_delete("maps/main"+m.owner+".map");file_delete("maps/grenade"+m.owner+".map")
				file_delete("maps/flag"+m.owner+".map")
				file_delete("maps/combo"+m.owner+".map")
				file_delete("maps/zombie"+m.owner+".map")
				file_delete("maps/zombie2"+m.owner+".map")
				file_delete("maps/knife"+m.owner+".map")
				file_delete("maps/helicopter"+m.owner+".map")
				file_delete("maps/sword"+m.owner+".map")
				file_delete("maps/abyss_clash"+m.owner+".map")
				file_delete("maps/one_shot_one_kill"+m.owner+".map")
				file_delete("maps/snow"+m.owner+".map"); file_delete("maps/collect"+m.owner+".map")

				g.init_mapsystem()
				g.matches.remove(m)
				return


			if m.inprogress and len(m.players)==1 and (m.mode=="minecraft" or m.mode=="snow" or m.mode=="sniper" or m.mode=="teamk2" or m.mode=="teamf2" or m.mode=="sword" or m.mode=="collect" or m.mode=="g" or m.mode=="g2" or m.mode=="teaml"):
				try: m.send("Match ended. "+g.getpc(m.players[0]).name+" won!",2)
				except: pass
				try: g.n.send_reliable(g.getpc(m.players[0]).peer_id,"play_s win.ogg",0)
				except: pass
				m.send_except(m.players[0],"play_s misc171.ogg",0)
				g.move_player(g.get_player_index_from(m.players[0]),5,0,0,"lobby")
				j=g.getpc(m.players[0])
				item_map={}
				for item in g.dontlose:
					try:
						if j.get_item_count(item)>0: item_map[item]=j.get_item_count(item)
					except: pass
				try:
					g.getpc(m.players[0]).inv=dict()
				except: pass
				for item in item_map.keys():
					try: j.give(item,item_map[item])
					except: pass
				if m.mode=="teamz": m.clearzombies()
				for n in g.npcs:
					if n.map==m.get_cwmap():
						n.health=0; n.dontkill=True
						n.hitby=""
						n.hitby2=""
	
				file_delete("maps/match"+m.owner+".map")
				file_delete("maps/main"+m.owner+".map");file_delete("maps/grenade"+m.owner+".map")
				file_delete("maps/flag"+m.owner+".map")
				file_delete("maps/combo"+m.owner+".map")
				file_delete("maps/zombie"+m.owner+".map")
				file_delete("maps/zombie2"+m.owner+".map")
				file_delete("maps/knife"+m.owner+".map")
				file_delete("maps/helicopter"+m.owner+".map")
				file_delete("maps/sword"+m.owner+".map")
				file_delete("maps/abyss_clash"+m.owner+".map")
				file_delete("maps/one_shot_one_kill"+m.owner+".map")
				file_delete("maps/snow"+m.owner+".map"); file_delete("maps/collect"+m.owner+".map")

				g.init_mapsystem()
				g.matches.remove(m)
				return
			if len(m.players)==1 and g.getpc(m.players[0]) is None or (m.starting==False and len(m.players)==0):
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
				file_delete("maps/zombie2"+m.owner+".map")
				file_delete("maps/knife"+m.owner+".map")
				file_delete("maps/helicopter"+m.owner+".map")
				file_delete("maps/sword"+m.owner+".map")
				file_delete("maps/abyss_clash"+m.owner+".map")
				file_delete("maps/one_shot_one_kill"+m.owner+".map")
				file_delete("maps/snow"+m.owner+".map"); file_delete("maps/collect"+m.owner+".map")

				g.init_mapsystem()
				try: g.matches.remove(m)
				except: pass
				return
def delay(ms):
	t=timer()
	while t.elapsed<ms: g.netloop(); g.gameloops(False)
def items_on_map(map):
	ret=0
	for item in g.items:
		if item.map==map: ret+=1
	return ret
def zombies_on_map(map):
	ret=0
	for zombie in g.zombies:
		if zombie.map==map: ret+=1
	return ret
def getmaxamount(item):
	if item=="40S&W": return 40
	if item=="22_LR_Long_Rifle": return 30
	if item=="9mm": return 10
	if item=="45_ACP": return 15
	if item=="small_potion": return 1
	if item=="vitality_potion": return 1
	if item=="revival_nectar": return 1

	if item=="hand_grenade": return 1

	if item=="mkek_jng90": return 1
	if item=="dragunov_psl": return 1

	if item=="colt1911": return 1
	if item=="m4": return 1

	if item=="7.62x51mm": return 10
	if item=="mkek_mpt76k": return 1
	if item=="5.56x45mm": return 10
	if item=="IthicaM37": return 1
	if item=="12_gauge": return 10
	if item=="7.62x54mmR": return 15

	if item=="timebomb": return 1
	if item=="tm62": return 1
	if item=="metal_shield": return 1
	if item=="molotov_cocktail": return 3
	return 1
class chest:
	def __init__(self,x,y,z,map):
		self.x=x
		self.y=y
		self.z=z
		self.taketimer=timer()
		self.map=map
		self.items=[]
		self.itemamounts=[]
		self.looptimer=timer()
		self.filechecktimer=timer()
		self.health=1000
def chestloop():
	for chest in g.chests:
		if not hasattr(chest,"looptime"): chest.looptime=random(3000, 3500)
		if not hasattr(chest,"fill"): chest.fill=False
		if chest.health<=0:
			g.play("chestexplode",chest.x,chest.y,chest.z,chest.map)
			g.n.broadcast("distsound chestexplodedist "+str(chest.x)+" "+str(chest.y)+" "+str(chest.z)+" "+chest.map+"",0)
			for index in range(len(g.players)):
				remove_platform(g.players[index], chest.x, chest.x, chest.y, chest.y, chest.z, chest.z+4, "wallmedal4")
				remove_platform(g.players[index], chest.x, chest.x, chest.y, chest.y, chest.z+5, chest.z+5, "metal5")
			g.chests.remove(chest)
			break
		if chest.filechecktimer.elapsed>1000:
			chest.filechecktimer.restart()
			if not file_exists("maps/"+chest.map+".map"):
				g.chests.remove(chest)
				return
		if chest.looptimer.elapsed>chest.looptime:
			chest.looptimer.restart()
			g.play("chest6",chest.x,chest.y,chest.z,chest.map)
def spawn_chest(x,y,z,map):
	g.chests.append(chest(x,y,z,map))
	ch=g.chests[len(g.chests)-1]
	ch.looptime=random(3000, 3500)
	for index in range(len(g.players)):
		if g.players[index].map==map:
			send_platform(g.players[index], ch.x, ch.x, ch.y, ch.y, ch.z, ch.z+4, "wallmedal4")
			send_platform(g.players[index], ch.x, ch.x, ch.y, ch.y, ch.z+5, ch.z+5, "metal5")


def getmaxamountchest(item):
	return 1
class corpse:
	def __init__(self,x,y,z,map):
		self.bomb=0
		self.x=x
		self.y=y
		self.z=z
		self.map=map
		self.items=[]
		self.itemamounts=[]
		self.looptimer=timer()
		self.filechecktimer=timer()
		self.health=100

		self.owner=""
		self.falltimer=timer()
		self.landed=False
		self.gotimer=timer()
def corpseloop():
	for corpse in g.corpses:
		try:
			if corpse.bleedtimer.elapsed>3000:
				corpse.bleedtimer.restart()
				g.play("bleeding",corpse.x,corpse.y,corpse.z,corpse.map)
		except: corpse.bleedtimer=timer()
		for i, key in enumerate(corpse.items):
			if not isinstance(key,str) or key=="":
				try: corpse.items.pop(i); corpse.itemamounts.pop(i)
				except: pass
		if corpse.health<=0:
			g.corpses.remove(corpse)
			break
		if not corpse.landed and corpse.falltimer.elapsed>50:
			corpse.falltimer.restart()
			if g.get_tile_at(corpse.x, corpse.y, corpse.z, corpse.map)=="": corpse.z-=1
		if not corpse.landed and g.get_tile_at(corpse.x, corpse.y, corpse.z, corpse.map)!="": corpse.landed=True
		if corpse.filechecktimer.elapsed>1000:
			corpse.filechecktimer.restart()
			if corpse.map=="lobby" or not file_exists("maps/"+corpse.map+".map"):
				g.corpses.remove(corpse)
				return
		if corpse.looptimer.elapsed>3000:
			corpse.looptimer.restart()
			g.play("corpseloop"+str(random(1,4)),corpse.x,corpse.y,corpse.z,corpse.map)
		if corpse.gotimer.elapsed>600000 or len(corpse.items)==0:
			g.play("corpsemisc2",corpse.x,corpse.y,corpse.z,corpse.map)
			g.corpses.remove(corpse)
			break

def spawn_corpse(x,y,z,map):
	g.corpses.append(corpse(x,y,z,map))
g.spawn_corpse=spawn_corpse
class electric:
	def __init__(self,x,y,z,map):
		self.health=50
		self.x=x
		self.y=y
		self.z=z
		self.map=map
		self.mid=spawn_moving_sound("electricty.ogg",self.x,self.y,self.z,self.map,"",100)
		self.dptimer=timer()
		for index in range(len(g.players)):
			if g.players[index].map==map:
				send_platform(g.players[index], self.x, self.x, self.y, self.y, self.z, self.z+4, "wallfence6")
				send_platform(g.players[index], self.x, self.x, self.y, self.y, self.z+5, self.z+5, "metal7")

def electricloop():
	for ind, e in enumerate(g.electrics):
		if not hasattr(e,"dptimer"): e.dptimer=timer()
		if e.dptimer.elapsed>10000:
			e.dptimer.restart()
			for ind2, e2 in enumerate(g.electrics):
				if ind!=ind2 and e.x==e2.x and e.y==e2.y and e.z==e2.z and e.map==e2.map:
					g.electrics.remove(e2)
					return
		if e.health<=0:
			g.play("electrictyexplode",e.x,e.y,e.z,e.map)
			g.n.broadcast("distsound electrictyexplodedist "+str(e.x)+" "+str(e.y)+" "+str(e.z)+" "+e.map,0)
			for p in g.players:
				if p.distancecheck(e.x,e.y,e.z)<=40 and p.map==e.map:
					p.playsound("electrictyhit")
					p.health-=random(50,80)
					p.hitby="electric pole"
					p.hitby2="electric pole"
					if not p.sitting: g.n.send_reliable(p.peer_id,"sitstart",0)
					if not p.sitting: p.playsound(g.get_tile_at(p.x,p.y,p.z,p.map)+"fall")
			for index in range(len(g.players)):
				remove_platform(g.players[index], e.x, e.x, e.y, e.y, e.z, e.z+4, "wallfence6")
				remove_platform(g.players[index], e.x, e.x, e.y, e.y, e.z+5, e.z+5, "metal7")

			destroy_moving_sound(e.mid)
			g.timed_electrics.append(timed_electric(e.x,e.y,e.z,e.map))
			g.electrics.remove(e)
			return
g.electric=electric
class timed_electric:
	def __init__(self,x,y,z,map):
		self.timer=timer()
		self.x=x
		self.y=y
		self.z=z
		self.map=map
def timed_electricloop():
	for e in g.timed_electrics:
		if e.timer.elapsed>120000:
			for e2 in g.electrics:
				if e.x==e2.x and e.y==e2.y and e.z==e2.z and e.map==e2.map:
					g.timed_electrics.remove(e)
					return
			g.electrics.append(electric(e.x,e.y,e.z,e.map))
			g.timed_electrics.remove(e)
			return
def ms_to_readable_time(milliseconds):
	milliseconds = math.floor(milliseconds)
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
