from item import spawn_item
from file_directories import file_exists
from weapon import get_weapon_range, spawn_weapon, get_weapon_spread
from pathfinder import pathfind
from grenade import launch_grenade
from moving_sound_serverside_handler import update_moving_sound, destroy_moving_sound
from rotation import vector
usernames=['ArcticAvenger', 'AlphaAssassin', 'LethalLynx', 'NeonNinja', 'BlazeBerserker', 'RadiantRebel', 'DeltaDestroyer', 'IroncladInferno', 'RustRaptor', 'RadiantRogue', 'InfernoInfantry', 'NeuralNinja', 'MidnightMystic', 'ThunderousTempest', 'NightshadeNinja', 'IronCommander', 'NightmareNomad', 'AuroraAssailant', 'CrimsonReaper', 'RogueRaptor', 'ZenZephyr', 'CyberCrusader', 'ThunderTrooper', 'CosmicConqueror', 'PlasmaPhantom', 'DesertPhantom', 'CrimsonCyclone', 'ApexAssailant', 'PhantomPatriot', 'OmegaOutlaw', 'SapphireScorpion', 'CyberStorm', 'PhantomProwess', 'FrostFire', 'BattleBravo', 'TerraTactician', 'SolarSpectre', 'MaverickMayhem', 'ApexAvenger', 'ChaosChameleon', 'NovaNomad', 'MidnightMercenary', 'TitanicTerror', 'PhantomPhoenix', 'EclipseEagle', 'TacticalTitan', 'SpectralSpartan', 'ShadowShogun', 'ShadowStriker', 'PolarPredator', 'NovaNemesis', 'StormSergeant', 'CobaltCorsair', 'ShadowSoldier', 'StormySniper', 'SkystormSlayer', 'CelestialCenturion', 'RagingRaptor', 'SilentShadowblade', 'XenonXenith', 'RiftReaper', 'ObsidianOutlaw', 'WarlordWraith', 'VolatileValkyrie', 'AtomicAvenger', 'SonicSniper', 'EclipseExecutioner', 'PolarPirate', 'SilentStorm', 'RagingRevenant', 'PlatinumPaladin', 'EternalEmber', 'PlasmaPirate', 'SniperSpecter', 'ChaosChampion', 'TitanTamer', 'AbyssalAvenger', 'BlackOpsBerserker', 'AstralAssassin', 'WarMachineX', 'CyberAssassin', 'DoomsdayDynamo', 'PhoenixProwler', 'NebulaNinja', 'FeralFlame', 'LunarLancer', 'BulletStorm', 'BlitzBrigand', 'MysticMaverick', 'InfernoInquisitor', 'TitanTornado', 'ZenithZombie', 'SapphireSpartan', 'OmegaOutrider', 'WarpWizard', 'BlitzBattalion', 'BlazeBattlemage', 'OmegaOverlord', 'NuclearNemesis', 'PlasmaProwess', 'VenomVanguard', 'StormborneSentinel', 'MysticMarauder', 'ZenithZephyr', 'WastelandWarrior', 'SilentSniperX', 'ThunderousThorn', 'VenomVigilante', 'SonicSoldier', 'PhantomPatriarch', 'VanguardViper', 'ChaosChieftain', 'NebulaNomad', 'VoidVoyager', 'CosmicCrusader', 'SteelPatriot', 'FrostbiteFury', 'GhostGrenadier', 'VortexVigilante', 'RapidRogue', 'ViperVindicator', 'BlazeBrigadier', 'SonicSamurai','CyberBlitz', 'PixelBlast', 'BotCraft', 'VoltBladeX', 'MechByteX', 'RoboPulse', 'RoboRhythm', 'VoltByte', 'BotRider', 'QuantumByte', 'ByteCyber', 'RoboSprintX', 'QuantumRider', 'CypherByte', 'TurboDroid', 'CodeBurstX', 'BotBlaster', 'CyberCyber', 'CodeSprintX', 'CodeRiderX', 'BotBurst', 'QuantumCraftX', 'TurboBot', 'CodeBlastX', 'SynthBlade', 'QuantumMatrix', 'CyberMeld', 'ByteCyberX', 'QuantumPilot', 'NeonCyborg', 'NeuralBurst', 'CyberRider', 'PixelCircuit', 'BinaryBot', 'RoboCraftX', 'PixelCraft', 'NeuralByte', 'PixelBlade', 'BotVortex', 'SynthBurstX', 'RoboNova', 'RoboWarp', 'RoboPulseX', 'CypherMeld', 'CyberNexus', 'BotBlitzX', 'CypherCircuit', 'SynthCraftX', 'QuantumSparkX', 'CyberPulseX', 'QuantumSprintX', 'VoltCyber', 'CyberVortex', 'ByteCraft', 'CyberSpark', 'CodeMatrix', 'MechPulseX', 'VoltMeld', 'CypherCraft', 'CypherSpark', 'PixelByteX', 'RoboMatrix', 'SynthMatrixX', 'RoboCraft', 'MechMeld', 'CypherMatrix', 'QuantumBladeX', 'BotSpark', 'BotByte', 'QuantumBlade', 'SynthRider', 'CyberByteZ', 'DynamoVortex', 'SynthByteX', 'SynthBlitz', 'PixelCyber', 'QuantumCode', 'QuantumCraft', 'CodeNovaX', 'NeuralBurstX', 'BinaryBlitz', 'ByteVortexX', 'PixelPilot', 'PulseDroid', 'ByteSparkX', 'MechNovaX', 'VoltPulse', 'MechBlitz', 'CypherSparkX', 'DynamoPulse', 'CyberBladeX', 'MechSprint', 'BinaryGizmo', 'ByteMatrix', 'AutomatonZ', 'BotPulseX', 'CyberNovaX', 'CodeSparkX', 'QuantumBlitz', 'CyberByteX', 'RoboSpark', 'ByteBladeX', 'VoltBlade', 'NeuralBladeX', 'BotByteX', 'MechSpark', 'PixelPulse', 'CyberBurstX', 'QuantumSprint', 'MechVibe', 'NeuralCraftX', 'ByteBlitz', 'DynamoDrive', 'PixelMeld', 'CyberBlade', 'MechPulse', 'RoboSprint', 'QuantumNova', 'MechByte', 'VoltCyberX', 'CodeByteX', 'BotVortexX', 'MechNova', 'SynthMatrix', 'DynamoByte', 'RoboRider', 'MechByteZ', 'SynthPulse', 'ByteRiderX', 'DynamoBladeX', 'DynamoPulseX', 'PixelCyberX', 'CyberCircuit', 'VoltNova', 'CypherBlade', 'ByteSprint', 'CypherBladeX', 'RoboCyber', 'MechCyber', 'NeuralCyberX', 'SynthCyberX', 'VoltCraft', 'MechCraft', 'CypherRider', 'TechnoSprite', 'MechVortex', 'RoboFury', 'CyberByte', 'DynamoBlitz', 'NeuralBlitzX', 'ByteSpark', 'NeuralSpark', 'VoltMaven', 'ByteVortex', 'ByteBuzzer', 'PixelMatrix', 'CircuitDroid', 'CodeNova', 'NanoBlitz', 'CircuitCoder', 'QuantumRiderX', 'ByteBlast', 'CypherCode', 'TechnoPulse', 'PixelMatrixX', 'MechSparkX', 'DynamoBlitzX', 'ByteRider', 'DynamoSprint', 'RoboBlast', 'CyberEcho', 'BotCraftX', 'BotonicWave', 'CodeBotX', 'BotSprintX', 'DynamoMatrixX', 'SynthByteZ', 'CypherMeldX', 'VoltCircuit', 'ByteBurst', 'PixelPilotX', 'MechRiderX', 'BotMatrix', 'VoltByteX', 'ByteBlaster', 'PixelNova', 'QuantumCircuit', 'SynthSprint', 'CodeBurst', 'BotPulse', 'DynamoNova', 'CodeCrusher', 'DynamoByteX', 'DynamoMatrix', 'SynthSquad', 'MechMatrix', 'BotNovaX', 'CyberVortexX', 'AutomatonX', 'QuantumSpark', 'CircuitCraft', 'CypherPulse', 'NeuralVortexX', 'SynthByte', 'MechRider', 'RoboMatrixX', 'DynamoCraft', 'CyberCraft', 'VoltByteZ', 'NeuralNova', 'ByteCraftX', 'NeonByte', 'NeuralMatrix', 'CodeMatrixX', 'BotRiderX', 'RoboBlade', 'NeuralBlade', 'SynthCraft', 'VoltSprint', 'NeuralMatrixX', 'NeuralSprint', 'DynamoCircuit']
import globals as g
from random import randint as random
from random import choice

from variable_management import string_contains, string_split
from rotation import get_3d_distance, calculate_x_y_angle
import data_loader


from timer import timer
from guns import guns, guns2
from file_directories import file_delete
class npc:
	def __init__(self, voiceamount, voicemaxamount, name, map, voicesound, walktime, attack, getattack, mindammage, maxdammage, painsound, painsoundamount, targethitsound, targethitsoundamount, deathtime, hitrange, maxhealth, deathsound, deathsoundamount, shoottime, minx, maxx, miny, maxy, z, voicetime, maxamount, maxwalktime,match="",matchteam=""):
		self.netlooptimer=timer()
		self.hidden=False
		self.aim_mode=1
		self.specplayer=""
		self.paid=False
		self.binocularsplayer=""
		self.items_got=0
		self.leghits=0
		self.legshots=0
		self.headhits=0
		self.headshots=0
		self.silenced=[]
		self.tokentimer=timer()
		self.shielded=False
		self.shieldhitchance=0
		self.helmeted=False
		self.helmethitchance=0

		self.group=""
		self.faint=False
		self.weapon2=""
		self.fainted=False
		self.snowcollecttimer=timer()
		self.playerchecktimer=timer()
		self.itemchecktimer=timer()
		self.targetchecktimer=timer()
		self.weaponchecktimer=timer()
		self.snowtimer=timer()
		self.jumpchecktimer=timer()
		self.stunned=False
		self.stuntimer=timer()
		self.stuntime=0
		self.weapon=""
		self.grenadepin=False
		self.grenadetime=0
		self.grenadepintimer=timer()
		self.grenadetimer=timer()
		self.grenadethrowtimer=timer()
		self.otarget=False
		self.otargetx=0
		self.tokentimer.elapsed=300000
		self.otargety=0

		self.otargetz=0
		self.stoploot=False
		self.stoploottimer=timer()
		self.aim=0
		self.comename=""
		self.vi=-1
		self.looting=False
		self.filechecktimer=timer()
		self.exithouse=False
		self.zhtoken=0
		self.randomwalking=False
		self.zombie=False
		self.path=None
		self.dontkill=False
		self.ducking=False
		self.plusdammage=0
		self.inhouse=False
		self.facing=0
		self.exithouse=False
		self.targetinghouse=False
		self.targeting=False
		self.targetinghouseexit=False
		self.targeting=False
		self.dontenterhouse=False

		self.matchmode=""
		self.jumpdotimer=timer()
		self.colatimer=timer()

		self.targetname=""
		self.falltimer=timer()
		self.falltime=90
		self.falldistance=0
		self.msoundtimers=[]
		self.oldx=0
		self.oldy=0
		self.oldz=0

		self.jumping=False
		self.jumptimer=timer()
		self.jumptime=100
		self.jumplandz=0
		self.falling=False
		self.jumpup=0
		self.molotovthrowtimer=timer()

		self.isbot=True
		self.reloading=False
		self.reloadtimer=timer()
		self.reloadtime=0

		self.x=0
		self.y=0
		self.z=0
		self.hitsoundtoplayer=""
		self.hts=""
		self.privatehitsound=False
		self.targetx=0
		self.targetitem=-1
		self.hitattack=False
		self.hitsounds=0
		self.targety=0
		self.targetz=0
		self.fulldied=False
		self.haspain=True
		names=[]
		for npc in g.npcs:
			
			names.append(npc.name)
		target_username=choice(usernames)
		while target_username in names:
			
			target_username=choice(usernames)
		self.name=target_username
		self.match=match
		self.msounds=[]
		self.joinedmatch=match
		self.team=matchteam
		self.matchteam=matchteam
		if self.match!="":
			for m in g.matches:
				if m.owner==self.match:
					m.players.append(self.name)
					if self.team=="red" and m.redleader=="": m.redleader=self.name
					if self.team=="blue" and m.blueleader=="": m.blueleader=self.name
					self.m=m
					self.matchmode=m.mode
		self.soundname=self.name
		self.mindamage=0
		self.maxdamage=0

		self.targeting=False
		self.map=""
		self.voicetimer=timer()
		self.trackwho=random(1,2)
		self.hitby=""
		self.hitby2=""
		self.dietime=0
		self.dietimer=timer()
		self.painrandom=0

		self.loopsrandom=0
		self.range=0
		self.voicetime=0
		self.health=0


		self.walktime=0
		self.maxwalktime=0

		self.walktimer=timer()
		self.attack=False
		self.dying=False
		self.attacktimer=timer()
		self.attacktime=0
		self.voicemaxamount = voicemaxamount
		self.voicetime = voicetime
		self.voiceamount = voiceamount

		self.map = map
		self.voicesound = voicesound
		self.walktime = walktime
		self.maxwalktime = maxwalktime

		self.attack = True if attack == 1 else False
		self.getattack = getattack
		self.mindammage = mindammage
		self.maxdammage = maxdammage
		self.painsound = painsound
		self.painsoundamount = painsoundamount
		self.targethitsound = targethitsound
		self.targethitsoundamount = targethitsoundamount
		self.dietime = deathtime

		self.range = hitrange
		self.health = maxhealth
		self.deathsound = deathsound
		self.deathsoundamount = deathsoundamount
		self.attacktime = shoottime
		self.minx = minx
		self.maxx = maxx
		self.miny = miny
		self.maxy = maxy
		self.z = z
		self.x=random(minx,maxx)
		self.y=random(miny,maxy)
		self.inv=dict()
		self.ammo={}
		loadout = data_loader.get_npc_loadout(self.matchmode)
		if loadout.get("weapons"):
			if loadout["weapons"] == ["random"]:
				self.randomweapongive()
			else:
				for w in loadout["weapons"]:
					self.give(w, 1)
					wdata = data_loader.get_weapon(w)
					if wdata.get("ammo_type"):
						self.give(wdata["ammo_type"], wdata.get("mag_size", 0) * 4)
		if loadout.get("items"):
			for item, count in loadout["items"].items():
				self.give(item, count)

		g.n.broadcast("update_player " + str(self.x) + " " + str(self.y) + " " + str(self.z) + " " + self.map+" "+self.name+" "+str(self.facing), 20)
	def send_bulletbody(self):
		packet="play_s bullet_impact_body"+str(random(1,2))+".ogg"
		for p in g.players:
			if p.specplayer==self.name: 		g.n.send_reliable(p.peer_id,packet,0)
	def msoundloop(self):
		if self.stunned and self.stuntimer.elapsed>self.stuntime:
			self.stunned=False
			self.stuntimer.restart()
			self.stuntime=0
			if self.faint: self.health=0
		if not self.stunned and (self.map.startswith("snow") or self.map.startswith("knife")) and self.snowcollecttimer.elapsed>1000:
			self.snowcollecttimer.restart()
			if self.get_item_count("snowflake_shard")<=5:
				self.give("snowflake_shard",1)
				self.playsound("snowhit3")
				self.snowcollecttimer.restart()
		if self.stoploot and self.stoploottimer.elapsed>2000 if not self.reloading else self.reloadtime:
			self.stoploottimer.restart()
			self.looting=False
			self.stoploot=False
		for i in range(len(self.msoundtimers)):
			if self.msoundtimers[i].elapsed>=15000:
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

	def jump(self):
		if "collect" in self.map or self.zombie or "knife" in self.map: return
		if round(self.x)==round(self.targetx) and round(self.y)==round(self.targety): return
		if self.jumpdotimer.elapsed>0:
			self.jumpdotimer.restart()
			self.playsound("jump"+str(random(1,4)))
			self.jumping=True
			self.jumpup=1
			self.jumplandz=self.z
	def fallloop(self):
		if(self.jumptimer.elapsed > self.jumptime and self.jumping==True):
		
				self.jumptimer.restart()
				if(self.jumpup==1):
				
						if(self.z <=self.jumplandz+5):
						
								self.z+=1
								if g.get_tile_at(self.x, self.y, self.z, self.map)!="":
								
										self.jumpup=0
										self.jumplandz=self.z
										
								
						else:
						
								self.jumpup=0
								
						
				elif(self.jumpup==0):
				
						if(self.z > self.jumplandz):
						
								self.z-=1
								if g.get_tile_at(self.x, self.y, self.z, self.map)!="":
								
										self.playsound(g.get_tile_at(self.x, self.y, self.z, self.map)+"land")
										self.jumpdotimer.restart()
										self.jumping=False
										
								
						else:
						
								if g.get_tile_at(self.x, self.y, self.z, self.map)=="":
								
										self.falling=True
										self.falldistance=0
										self.falltimer.restart()
										self.jumping=False
										return
										
								self.jumping=False
								
						
				
		


	def fallcheck(self):
		tile=g.get_tile_at(self.x, self.y, self.z, self.map)
		if tile=="" and self.falling==False and self.z>0 and self.jumping==False or tile=="blank" and self.falling==False and self.jumping==False and self.z>0:
		
				self.falling=True
				self.falldistance=0
				self.falltimer.restart()
				self.playsound("fall")

				
		
	def fallingloop(self):
		if(self.falling==True and self.falltimer.elapsed > self.falltime):
		
				if(g.get_tile_at(self.x, self.y, self.z, self.map)!="" or self.z==0):
				
						self.falling=False
						if(self.falldistance < 10):
						
								self.playsound(g.get_tile_at(self.x, self.y, self.z, self.map)+"land")

								self.falling=False
								
						else:
						
								self.playsound(g.get_tile_at(self.x, self.y, self.z, self.map)+"fall")

								self.falling=False
								
						return
						
				self.falltimer.restart()
				self.falldistance+=1
				self.z-=1

				
		

	def get_item_count(self,item):
	
		if not item in self.inv:
		
			return 0
			
		ret=0
		ret=self.inv[item]
		if(ret<0):
		
			del self.inv[item]
			return 0
			
		return ret
		

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
				
			
		
	
	def randomweapongive(self):
		loadouts = data_loader.get_npc_random_loadouts()
		chosen = loadouts[random(0, len(loadouts)-1)]
		self.give(chosen["weapon"], 1)
		if chosen.get("ammo_type") and chosen.get("ammo_count"):
			self.give(chosen["ammo_type"], chosen["ammo_count"])


	def give(self, item, amount):
		a = 0
		if item not in self.inv:
			self.inv[item] = amount
		else:
			a = self.inv[item]
			if a + amount <= 0:
				del self.inv[item]
			else:
				self.inv[item] = a + amount
		self.neg_inv_check()
	def neg_inv_check(self):
		k=self.inv.keys()
		for i in k:
			v=0
			v=self.inv[i]
			if v<=0 or i==-1:
				del self.inv[i]
				return

	def play_hit_sound(self):
		if self.painsoundamount>0:
			g.play(self.painsound+str(random(1,self.painsoundamount)), self.x, self.y, self.z, self.map)
		else:
			g.play(self.painsound, self.x, self.y, self.z, self.map)
	def playsound2(self, snd, delimiter=""):
		self.playsound(self.soundname+delimiter+snd)
	def playsoundmoving(self,snd):
		g.playmoving(self.x,self.y,self.z,self.map,snd,self)
	def play_walk_sound(self):
		if round(self.x)==round(self.targetx) and round(self.y)==round(self.targety): return
		til=g.get_tile_at(self.x,self.y,self.z)
		if til!="":

			g.play(til+"step"+str(random(1, 5)), self.x, self.y, self.z, self.map)
	def playsound(self, snd):
		if snd==self.voicesound:
			for p in g.players:
				if (p.specmap==self.map or p.map==self.map) and p.beacon==1 and p.specplayer!=self.name and self.distancecheck(p.x,p.y,p.z)<=30 and (p.map==self.map or p.specmap==self.map):
					if p.matchteam!=self.matchteam and self.matchteam!="":
						g.n.send_unreliable(p.peer_id,self.voicesound+" "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" "+self.map+" 100",3)
					else:
						g.n.send_unreliable(p.peer_id,"teambeacon "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" "+self.map+" 100",3)
		else:
			if self.zombie and "step" in snd: g.play(snd, self.x, self.y, self.z, self.map, None, True, 3, 80)
			else: g.play(snd, self.x, self.y, self.z, self.map)
	def stun(self, ms):
		self.stuntime=ms
		self.stunned=True
		self.stuntimer.restart()
	def distancecheck(self, xx, yy, zz):
		return get_3d_distance(self.x, self.y, self.z, xx, yy, zz)
	def approaching_wall(self):
		return False
		tile1=g.get_tile_at(self.x+1,self.y,self.z,self.map)
		tile2=g.get_tile_at(self.x-1,self.y,self.z,self.map)
		tile3=g.get_tile_at(self.x,self.y+1,self.z,self.map)
		tile4=g.get_tile_at(self.x,self.y-1,self.z,self.map)
		if "wall" in tile1 or "wall" in tile2 or "wall" in tile3 or "wall" in tile4: return True
		return False
	def loop1(self):
		if self.grenadepin and self.grenadepintimer.elapsed>4000:
			launch_grenade(self.x, self.y, self.z, self.map, self, self.grenadedir)
			g.grenades[len(g.grenades)-1].explodetimer.elapsed=self.grenadepintimer.elapsed
			self.grenadepin=False
			self.give("hand_grenade",-1)
		if self.grenadepin and self.grenadetimer.elapsed>self.grenadetime:
			self.playsound("grenadethrow")
			self.give("hand_grenade",-1)
			self.grenadepin=False
			launch_grenade(self.x, self.y, self.z, self.map, self, self.grenadedir)
			g.grenades[len(g.grenades)-1].explodetimer.elapsed=self.grenadepintimer.elapsed

		if self.health>100: self.health=100
		if not self.zombie and self.map.startswith("zombie2") and self.matchteam=="blue": self.zombie=True
		if self.zombie and self.voicesound!="zombievoice":
			self.voicesound="zombievoice"
			self.voiceamount=1
			self.voicemaxamount=5
			self.painsound="zombiehurt"
			self.deathsound="zombiedie"
			self.voicetime=6500
		if self.inhouse:
			if self.team=="red" and self.m.reddoorhealth<=0 or self.team=="blue" and self.m.bluedoorhealth<=0:
				self.inhouse=False
				self.targetinghouse=False
				self.targeting=False
				self.dontenterhouse=True
				self.randomwalking=False
		if not self.inhouse and not self.targetinghouse and self.m.mode=="teamz":
			if not self.looting and g.get_nearest_zombie(self.x, self.y, self.z, self.map)>-1:
				p=g.zombies[g.get_nearest_zombie(self.x, self.y, self.z, self.map)]
				self.targetx=p.x
				self.targety=p.y
				self.targetz=p.z
				self.targetitem=-1
				self.facing=calculate_x_y_angle(self.x, self.y, self.targetx, self.targety)
				self.targeting=True
				self.randomwalking=False
			else:
				self.targeting=False
				self.targetname=""
				self.randomwalking=False
		if self.trackwho==1 and self.m.mode!="teamz" and self.playerchecktimer.elapsed>0:
			self.playerchecktimer.restart()
			if "collect" not in self.map and g.get_nearest_player(self.x, self.y, self.z, self.map, self, 50)>-1:
				p=g.players[g.get_nearest_player(self.x, self.y, self.z, self.map, -1, 50)]
				if not self.looting:
					self.targetx=p.x
					self.targety=p.y
					self.targetz=p.z
					self.targetitem=-1
					self.facing=calculate_x_y_angle(self.x, self.y, self.targetx, self.targety)
					self.targeting=True
					self.targetname=p.name
					self.randomwalking=False
			else:
				self.trackwho=2
				if not self.randomwalking and not self.looting:
					self.targeting=True
					self.targetname=""
					if self.otarget:
						self.targetx=self.otargetx
						self.targety=self.otargety
						self.targetz=self.otargetz
						self.otarget=False
					else:
						self.targetx=random(0,self.maxx)
						self.targety=random(0,self.maxy)
					self.randomwalking=True
					self.targetitem=-1
		if self.inhouse:
			if self.m.mode=="teamz":
				if g.get_leader_hit_player(self) is not None:
					p=g.get_leader_hit_player(self)
					if p.name==self.name:
						p=g.getpc(self.m.redleader if self.team=="red" else self.m.blueleader)
					if not self.looting:
						self.targetx=p.x
						self.targety=p.y
						self.targetz=p.z
						self.targetitem=-1
						self.facing=calculate_x_y_angle(self.x, self.y, self.targetx, self.targety)
						self.targetname=p.name
						self.randomwalking=False
						self.targeting=True
				else:
					self.targeting=False
					self.targetname=""
					self.randomwalking=False
		if self.playerchecktimer.elapsed>0 and self.trackwho==2 and self.m.mode!="teamz":
			self.playerchecktimer.restart()
			if 1:
				if "collect" not in self.map and g.get_nearest_npc(self.x, self.y, self.z, self.map, self, 50)>-1:
					p=g.npcs[g.get_nearest_npc(self.x, self.y, self.z, self.map, self, 50)]
					if not self.looting:
						self.targetx=p.x
						self.targety=p.y
						self.targetz=p.z
						self.targetitem=-1
						self.facing=calculate_x_y_angle(self.x, self.y, self.targetx, self.targety)
						self.targetname=p.name

						self.targeting=True
						self.randomwalking=False
				else:
					self.trackwho=1
					if not self.randomwalking and not self.looting:
						self.targeting=True
						self.targetname=""

						self.targetx=random(0,self.maxx) if not self.otarget else self.otargetx
						self.targety=random(0,self.maxy) if not self.otarget else self.otargety
						self.randomwalking=True
						self.targetitem=-1
						self.otarget=False
		self.targetloop()
		if "collect" not in self.map: self.attackloop()
		if self.targetx==self.x and self.y==self.targety and self.randomwalking: self.randomwalking=False
		if self.weapon!="knife" and self.weapon!="punch" and not self.looting and "zombie" not in self.map and self.targetx==self.x and self.y==self.targety and not self.randomwalking:
			self.looting=True
			self.targetx=random(0,self.maxx)
			self.targety=random(0,self.maxy)
			self.stoploot=True
			self.stoploottimer.restart()
			self.randomwalking=False
		if not self.looting and self.reloading and not self.randomwalking:
			self.looting=True
			self.targetx=random(0,self.maxx)
			self.targety=random(0,self.maxy)
			self.stoploot=True
			self.stoploottimer.restart()
			self.randomwalking=False

		if self.targetx==self.x and self.y==self.targety and self.looting: self.looting=False
	def ps(self):
		return # removed
	def exithousenow(self):
		if self.matchteam=="red":
			self.targetinghouseexit=True
			self.targetx=self.m.redhousex
			self.targety=self.m.redhousey+2
			self.randomwalking=False
			self.targetitem=-1
			self.facing=calculate_x_y_angle(self.x, self.y, self.targetx, self.targety)
			self.targeting=True
		if self.matchteam=="blue":
			self.targetinghouseexit=True
			self.targetx=self.m.bluehousex
			self.targety=self.m.bluehousey+2
			self.randomwalking=False
			self.targetitem=-1
			self.facing=calculate_x_y_angle(self.x, self.y, self.targetx, self.targety)
			self.targeting=True


	def targetloop(self):
		if self.health>30 and self.targetinghouse:
			self.targetinghouse=False
			self.targetinghouseexit=False
		if self.inhouse:
			if self.matchteam=="red":
				step_1=g.getpc(self.m.redleader)
				if step_1==-1 or step_1==None: self.exithousenow()
				lp=step_1
				if lp==-1 or lp==None: self.exithousenow()
				try: step_2=lp.exithouse
				except: step_2=None
				if step_2 is not None:
					lp.exithouse=False
					self.exithousenow()
			if self.matchteam=="blue":
				step_1=g.get_player_index_fromnpc(self.m.blueleader)
				if step_1==-1: self.exithousenow()
				lp=g.getpc(self.m.blueleader)
				if lp is None: self.exithousenow(); return
				step_2=lp.exithouse
				if step_2:
					lp.exithouse=False

		for _heal in data_loader.get_npc_healing():
			_item = _heal["item"]
			_cooldown = _heal.get("cooldown", 5000)
			_threshold = _heal.get("use_below_hp", 80)
			if self.colatimer.elapsed > _cooldown and self.health <= _threshold and self.get_item_count(_item) >= 1 and not self.zombie:
				if _heal.get("heal_to"):
					self.health = _heal["heal_to"]
				else:
					self.health += _heal.get("heal_amount", 0)
				self.colatimer.restart()
				self.playsound("cola2")
				self.give(_item, -1)
				break
		if self.itemchecktimer.elapsed>0 and (self.get_item_count("small_potion")<=0 or self.get_item_count("vitality_potion")<=0 or self.get_item_count("revival_nectar")<=0):
			self.itemchecktimer.restart()
			if not self.dontenterhouse and self.health<=80 and self.m.mode=="teamz" and not self.looting:
				if not self.targetinghouse and not self.inhouse and self.m.reddoorhealth>0 and self.matchteam=="red":
					self.targetinghouse=True
					self.targetx=self.m.redhousex
					self.targety=self.m.redhousey
					self.randomwalking=False
					self.targetitem=-1
					self.facing=calculate_x_y_angle(self.x, self.y, self.targetx, self.targety)
					self.targeting=True
				if not self.targetinghouse and not self.inhouse and self.m.bluedoorhealth>0 and self.matchteam=="blue":
					self.targetinghouse=True
					self.targetx=self.m.bluehousex
					self.targety=self.m.bluehousey
					self.randomwalking=False
					self.targetitem=-1
					self.facing=calculate_x_y_angle(self.x, self.y, self.targetx, self.targety)
					self.targeting=True
		if self.comename!="":
			index=g.get_player_index_from(self.comename)
			if index==-1:
				self.comename=""
				self.looting=False
				self.randomwalking=False
				return
			else:
				p=g.players[index]
				if p.map!=self.map:
					self.comename=""
					self.looting=False
					self.randomwalking=False
					return
				else:
					self.targetx=p.x
					self.targety=p.y
					self.targetz=p.z
					self.targetitem=-1
		if self.targeting and self.walktimer.elapsed>(200 if not self.jumping else 100):
			self.walktimer.restart()
			if self.path is None and self.approaching_wall(): self.path=pathfind(self.x, self.y, self.targetx, self.targety, self.map, self.soundname)
			elif not self.approaching_wall(): self.path=None
			for j, i in enumerate(g.items):
				if self.zombie: break
				if i.map==self.map and self.targetitem==-1 and not self.inhouse and not self.targetinghouse and not self.targetinghouseexit and get_3d_distance(self.x,self.y,self.z,i.x,i.y,i.z)<=25 :
					self.otarget=True
					self.otargetx=self.targetx
					self.otargety=self.targety
					self.otargetz=self.targetz
					self.targetx=i.x
					self.targety=i.y
					self.targetz=i.z
					self.targetitem=j
					self.randomwalking=False
					break

			if self.path is not None and len(self.path)>0:
				next_x, next_y = self.path.pop()
				self.x=next_x
				self.y=next_y
				self.facing=calculate_x_y_angle(self.x, self.y, self.targetx, self.targety)
				if 1:
					for p in g.players:

						if p.specplayer==self.name or (p.map==self.map and p.distancecheck(self.x,self.y,self.z)<=30):
							if g.get_hidden_area_at(p.x, p.y, p.z, p.map)==g.get_hidden_area_at(self.x, self.y, self.z, self.map): g.n.send_unreliable(p.peer_id,"update_player " + str(self.x) + " " + str(self.y) + " " + str(self.z) + " " + self.map+" "+self.name+" "+str(self.facing), 20)
				self.ps()
			else:
				self.targetx=round(self.targetx)
				self.targety=round(self.targety)
				updateplayer=False
				if self.x<self.targetx:
					self.x+=1
					self.facing=calculate_x_y_angle(self.x, self.y, self.targetx, self.targety)
					updateplayer=True

				elif self.x>self.targetx:
					self.x-=1
					self.facing=calculate_x_y_angle(self.x, self.y, self.targetx, self.targety)
					updateplayer=True

				if self.y>self.targety:
					self.y-=1
					self.facing=calculate_x_y_angle(self.x, self.y, self.targetx, self.targety)
					updateplayer=True

				elif self.y<self.targety:
					self.y+=1
					self.facing=calculate_x_y_angle(self.x, self.y, self.targetx, self.targety)
					updateplayer=True
				if updateplayer:
					for p in g.players:

						if p.specplayer==self.name or (p.map==self.map and p.distancecheck(self.x,self.y,self.z)<=30):
							if g.get_hidden_area_at(p.x, p.y, p.z, p.map)==g.get_hidden_area_at(self.x, self.y, self.z, self.map): g.n.send_unreliable(p.peer_id,"update_player " + str(self.x) + " " + str(self.y) + " " + str(self.z) + " " + self.map+" "+self.name+" "+str(self.facing), 20)
				if self.matchmode=="teamd" or self.matchmode=="teamz2":
					for p in g.players:
						if self.distancecheck(p.x,p.y,p.z)<=3 and p.map==self.map and p.faint and p.matchteam==self.matchteam:
							p.faint=False
							p.fainted=False
							g.n.send_reliable(p.peer_id,"startmoving",0)
							g.n.send_reliable(p.peer_id,self.name+" waked you",0)
							g.play(p.get_current_char()+"voice32",p.x,p.y,p.z,p.map)
					for p in g.npcs:
						if self.distancecheck(p.x,p.y,p.z)<=3 and p.map==self.map and p.faint and p.matchteam==self.matchteam:
							p.faint=False
							p.fainted=False
							p.stunned=False
							g.play("voice32",p.x,p.y,p.z,p.map)

				g.itemloop()
				self.fallcheck()
				for mine in g.mines:
					if mine.map==self.map and mine.x==self.x and mine.y==self.y and mine.z==self.z: mine.health=0
		if self.targetinghouse and self.x==self.targetx and self.y==self.targety:
			g.play("houseenter",self.x,self.y,self.z,self.map)
			self.y+=2
			self.facing=calculate_x_y_angle(self.x, self.y, self.targetx, self.targety)
			g.n.broadcast("update_player " + str(self.x) + " " + str(self.y) + " " + str(self.z) + " " + self.map+" "+self.name+" "+str(self.facing), 20)
			self.inhouse=True
			self.targetinghouse=False
			self.targeting=False
			self.randomwalking=False
			g.play("houseexit",self.x,self.y,self.z,self.map)
		if self.targetinghouseexit and self.x==self.targetx and self.y==self.targety:
			g.play("houseenter",self.x,self.y,self.z,self.map)
			self.y-=2
			self.facing=calculate_x_y_angle(self.x, self.y, self.targetx, self.targety)
			g.n.broadcast("update_player " + str(self.x) + " " + str(self.y) + " " + str(self.z) + " " + self.map+" "+self.name+" "+str(self.facing), 20)
			self.targetinghouseexit=False
			self.targeting=False
			self.randomwalking=False
			self.inhouse=False
			self.dontenterhouse=True
			g.play("houseexit",self.x,self.y,self.z,self.map)
	def select_weapon(self):
		self.weapon=""
		if self.zombie:
			gun="claw"
			self.weapon=gun
			g.play(self.weapon+"draw",self.x,self.y,self.z,self.map)
			self.attacktime=int(g.wdata[self.weapon].split(" ")[0])
			self.range=get_weapon_range(self.weapon)
			return
		for gun in guns2:
			
			if self.get_item_count(gun)>=1 and (self.get_item_count(g.get_ammotype(gun))>=1 or not g.requires_ammo(gun)):
				self.weapon=gun
				g.play(self.weapon+"draw",self.x,self.y,self.z,self.map)
				self.attacktime=int(g.wdata[self.weapon].split(" ")[0])
				self.range=get_weapon_range(self.weapon)
				return
		if self.weapon=="":
			if "minecraft" not in self.matchmode:
				if self.get_item_count("knife")>0: self.weapon="knife"
				else: self.weapon="punch"
			if "minecraft"  in self.matchmode: self.weapon="stick"
			g.play(self.weapon+"draw",self.x,self.y,self.z,self.map)
			self.attacktime=1000
			self.range=get_weapon_range(self.weapon)
			return
	def reload(self):
		if 1:
			if 1:
				if(self.reloading==False):
				
					if(self.get_ammo_count_from(self.weapon)==g.get_max_ammo(self.weapon)):
					
						return
						
						
					else:
					
						ammoamount=self.ammocheck(self.weapon)
						self.playsoundmoving(self.weapon+"reload")
						self.reloadtime=g.get_reloadtime(self.weapon)
						self.reloadtimer.restart()
						self.reloading=True
						
					
				

	def attackloop(self):
		if self.targetname!="" and self.targetchecktimer.elapsed>0:
			self.targetchecktimer.restart()
			p=g.getpc(self.targetname)
			if p is None:
				self.targetname=""
				self.targeting=False
				self.randomwalking=False
				return
			if p.health<=0:
				self.targetname=""
				self.targeting=False
				self.randomwalking=False
				return
		if self.targetinghouse or self.targetinghouseexit: return
		if 1:
			if self.grenadethrowtimer.elapsed>4000 and self.get_item_count("hand_grenade")>=1 and self.grenadepin==False:
				canhit2=can_hit(self,"hand_grenade")
				if canhit2!=-1:
					self.grenadethrowtimer.restart()
					self.grenadepin=True
					self.grenadetime=random(500,4000)
					self.grenadetimer.restart()
					self.playsound("grenadepul"+str(random(1,2)))
					self.grenadedir=canhit2
		if self.get_item_count("snowflake_shard")>=1 and self.snowtimer.elapsed>4000:
			self.snowtimer.restart()
			canhit2=can_hit(self,"snowflake_shard")
			if not self.zombie and canhit2!=-1:
				self.give("snowflake_shard",-1)
				self.playsound("grenadethrow")
				miss=random(1,50)
				if miss<30: spawn_weapon(self.x, self.y, self.z, canhit2, "snowflake_shard", self.map, self)
				else: spawn_weapon(self.x, self.y, self.z+5, canhit2, "snowflake_shard", self.map, self)

		if self.get_item_count("molotov_cocktail")>=1 and self.molotovthrowtimer.elapsed>6000:
			canhit2=can_hit(self,"molotov_cocktail")
			if not self.zombie and canhit2!=-1:
				self.playsound("molotovthrow")
				self.molotovthrowtimer.restart()
				miss=random(1,50)
				if miss<30: spawn_weapon(self.x, self.y, self.z, canhit2, "molotov_cocktail", self.map, self)
				else: spawn_weapon(self.x, self.y, self.z+5, canhit2, "molotov_cocktail", self.map, self)
				self.give("molotov_cocktail",-1)

		if self.weaponchecktimer.elapsed>0:
			self.weaponchecktimer.restart()
			if self.weapon=="": self.select_weapon()
			if g.requires_ammo(self.weapon) and self.weapon!="" and (self.get_item_count(self.weapon)<=0 or (self.get_item_count(g.get_ammotype(self.weapon))<=0 and self.get_ammo_count_from(self.weapon)<=0)): self.select_weapon()
			for gun in guns2:
				if self.weapon==gun: break			
				if not self.zombie and self.get_item_count(gun)>=1 and (not g.requires_ammo(gun) or self.get_item_count(g.get_ammotype(gun))>=1) and self.weapon!=gun: self.select_weapon(); break

			if g.requires_ammo(self.weapon) and self.get_ammo_count_from(self.weapon)<=0 and self.weapon!="": self.reload()
			if g.requires_ammo(self.weapon) and (self.randomwalking or self.looting) and self.get_item_count(g.get_ammotype(self.weapon))>=g.get_max_ammo(self.weapon) and self.get_ammo_count_from(self.weapon)<g.get_max_ammo(self.weapon) and self.weapon!="": self.reload()
		if self.attacktimer.elapsed>self.attacktime:
			self.attacktimer.restart()

			canhit=can_hit(self)
			#canhit=-1
			if self.matchmode!="g" and self.matchmode!="teamg" and self.matchmode!="g2" and self.matchmode!="teamg2" and not self.targetinghouse and not self.targetinghouseexit and (get_3d_distance(self.x, self.y, self.z, self.targetx, self.targety, 0)<=self.range and not self.randomwalking and self.targetitem==-1 and not self.looting or canhit!=-1) and self.targeting:
				if canhit!=-1: self.facing=canhit
				if not self.reloading:
					ind=g.getpc(self.targetname)
					if ind is not None: self.ducking=ind.ducking
					miss=random(1,50)
					if self.m.mode=="teamz" or self.weapon=="punch" or self.weapon=="knife" or self.weapon=="wooden_sword" or self.weapon=="stone_sword" or self.weapon=="diamond_sword" or self.weapon=="stick" or self.weapon=="claw": miss=1
					if miss<30:
						spawn_weapon(self.x, self.y, self.z, self.facing, self.weapon, self.map, self)
						if self.weapon=="punch": spawn_weapon(self.x, self.y, self.z, self.facing, "feet", self.map, self)
					elif miss>=20: spawn_weapon(self.x, self.y, self.z+get_weapon_spread(self.weapon)*2, self.facing, self.weapon, self.map, self)
					if "sword" not in self.weapon: self.playsound(""+self.weapon+"fire"+str(random(1,3))+"")
					if "sword" in self.weapon: self.playsound(""+self.weapon+"fire")
					if self.weapon=="punch": self.playsound("feetfire"+str(random(1,3))+"")
					if self.weapon!="punch" and self.weapon!="knife" and self.weapon!="stick" and self.weapon!="claw" and self.weapon!="wooden_sword" and self.weapon!="stone_sword" and self.weapon!="diamond_sword":
						for pl in range(len(g.players)):
							if g.players[pl].dead: continue
							if g.players[pl].specmap==self.map or g.players[pl].map==self.map:
								try: g.n.send_reliable(g.players[pl].peer_id,"distsound "+self.weapon+"dist"+str(random(1,3))+" "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" "+self.map,0)
								except: pass
						for n in g.npcs:
							if n.map==self.map and n.name==self.name: continue
							if n.randomwalking and n.map==self.map and "zombie" not in n.map:
								n.targetx=self.x
								n.targety=self.y
								n.targetz=self.z
					self.ammogive(self.weapon,-1)

	def loop2(self):
		if self.attack:
			return
		if self.targeting==False and not self.looting:
			self.targetx=random(self.minx, self.maxx) if not self.otarget else self.otargetx
			self.targety=random(self.miny, self.maxy) if not self.otarget else self.otargety
			self.randomwalking=True
			self.targetitem=-1
			self.otarget=False
			self.facing=calculate_x_y_angle(self.x, self.y, self.targetx, self.targety)
			self.targeting=True
		if self.x==self.targetx and self.y==self.targety  and self.targeting and self.comename=="":
			self.targeting=False; self.randomwalking=False; self.looting=False
def npcloop(npc_loop=""):
	for i in range(len(g.npcs)):
		#if npc_loop!="" and g.npcs[i].soundname==npc_loop: continue

		try:
			g.npcs[i].m
		except:
			g.npcs.remove(g.npcs[i]); return
		if not hasattr(g.npcs[i],"items_got"): g.npcs[i].items_got=0
		g.npcs[i].msoundloop()
		g.npcs[i].fallloop()
		g.npcs[i].fallingloop()

		if g.npcs[i].filechecktimer.elapsed>1000:
			g.npcs[i].filechecktimer.restart()
			if g.npcs[i].map.startswith("helicopter"):
				owner=g.npcs[i].map.replace("helicopter","").replace(".map","")
				found=False
				for m in g.matches:
					if m.owner==owner: found=True
				if not found:
					g.npcs[i].health=0; g.npcs[i].dontkill=True
			elif g.npcs[i].map.startswith("match"):
				owner=g.npcs[i].map.replace("match","").replace(".map","")
				found=False
				for m in g.matches:
					if m.owner==owner: found=True
				if not found:
					g.npcs[i].health=0; g.npcs[i].dontkill=True
			elif g.npcs[i].map.startswith("abyss_clash"):
				owner=g.npcs[i].map.replace("abyss_clash","").replace(".map","")
				found=False
				for m in g.matches:
					if m.owner==owner: found=True
				if not found:
					g.npcs[i].health=0; g.npcs[i].dontkill=True
			elif g.npcs[i].map.startswith("sword"):
				owner=g.npcs[i].map.replace("sword","").replace(".map","")
				found=False
				for m in g.matches:
					if m.owner==owner: found=True
				if not found:
					g.npcs[i].health=0; g.npcs[i].dontkill=True

			elif g.npcs[i].map.startswith("collect"):
				owner=g.npcs[i].map.replace("collect","").replace(".map","")
				found=False
				for m in g.matches:
					if m.owner==owner: found=True
				if not found:
					g.npcs[i].health=0; g.npcs[i].dontkill=True



			elif g.npcs[i].map.startswith("main"):
				owner=g.npcs[i].map.replace("main","").replace(".map","")
				found=False
				for m in g.matches:
					if m.owner==owner: found=True
				if not found:
					g.npcs[i].health=0; g.npcs[i].dontkill=True
			elif g.npcs[i].map.startswith("knife"):
				owner=g.npcs[i].map.replace("knife","").replace(".map","")
				found=False
				for m in g.matches:
					if m.owner==owner: found=True
				if not found:
					g.npcs[i].health=0; g.npcs[i].dontkill=True
			elif g.npcs[i].map.startswith("zombie2"):
				owner=g.npcs[i].map.replace("zombie2","").replace(".map","")
				found=False
				for m in g.matches:
					if m.owner==owner: found=True
				if not found:
					g.npcs[i].health=0; g.npcs[i].dontkill=True
			elif g.npcs[i].map.startswith("zombie"):
				owner=g.npcs[i].map.replace("zombie","").replace(".map","")
				found=False
				for m in g.matches:
					if m.owner==owner: found=True
				if not found:
					g.npcs[i].health=0; g.npcs[i].dontkill=True
			elif g.npcs[i].map.startswith("grenade"):
				owner=g.npcs[i].map.replace("grenade","").replace(".map","")
				found=False
				for m in g.matches:
					if m.owner==owner: found=True
				if not found:
					g.npcs[i].health=0; g.npcs[i].dontkill=True
			elif g.npcs[i].map.startswith("flag"):
				owner=g.npcs[i].map.replace("flag","").replace(".map","")
				found=False
				for m in g.matches:
					if m.owner==owner: found=True
				if not found:
					g.npcs[i].health=0; g.npcs[i].dontkill=True


			if not file_exists("maps/"+g.npcs[i].map+".map") or g.npcs[i].map=="lobby": g.npcs[i].health=0; g.npcs[i].dontkill=True
		if not g.npcs[i].jumping and g.npcs[i].reloading: g.npcs[i].jump()
		if g.npcs[i].jumpchecktimer.elapsed>1000 and not g.npcs[i].jumping and not g.npcs[i].stoploot and "zombie" not in g.npcs[i].map and not g.npcs[i].randomwalking:
			g.npcs[i].jumpchecktimer.restart()
			if can_hit(g.npcs[i])==-1 : g.npcs[i].jump()

		if not g.npcs[i].jumping and g.npcs[i].targetinghouse: g.npcs[i].jump()
		if not g.npcs[i].jumping and (g.npcs[i].x!=g.npcs[i].targetx or g.npcs[i].y!=g.npcs[i].targety) and g.npcs[i].comename!="": g.npcs[i].jump()
		if(g.npcs[i].reloading):
		
			if(g.npcs[i].reloadtimer.elapsed>g.npcs[i].reloadtime):
			
				g.npcs[i].reloading=False
				p=g.npcs[i]
				amount=0
				if(p.get_item_count(g.get_ammotype(p.weapon))<g.get_max_ammo(p.weapon)):
					amount=p.get_item_count(g.get_ammotype(p.weapon))
					amount=p.get_item_count(g.get_ammotype(p.weapon))-g.npcs[i].get_ammo_count(g.npcs[i].weapon)
					if(amount>g.npcs[i].get_item_count(g.get_ammotype(g.npcs[i].weapon))):
						amount=g.npcs[i].get_item_count(g.get_ammotype(g.npcs[i].weapon))
					p.ammogive(p.weapon,amount)
					p.give(g.get_ammotype(p.weapon),-amount)					

				else:
					amount=g.get_max_ammo(p.weapon)
				
					amount=g.get_max_ammo(g.npcs[i].weapon)-g.npcs[i].get_ammo_count(g.npcs[i].weapon)
					if(amount>g.npcs[i].get_item_count(g.get_ammotype(g.npcs[i].weapon))):
						amount=g.npcs[i].get_item_count(g.get_ammotype(g.npcs[i].weapon))
					p.ammogive(p.weapon,amount)
					p.give(g.get_ammotype(p.weapon),-amount)					
				
			

		if g.npcs[i].dying==False:
			if not g.npcs[i].stunned and g.npcs[i].attack:
				g.npcs[i].loop1()
			else:
				if not g.npcs[i].stunned: g.npcs[i].loop2()
			try: g.npcs[i]
			except: return
			if g.npcs[i].voicetimer.elapsed>g.npcs[i].voicetime:
				g.npcs[i].voicetimer.restart()
				if g.npcs[i].voiceamount>0:
					g.npcs[i].playsoundmoving(g.npcs[i].voicesound+str(random(g.npcs[i].voiceamount,g.npcs[i].voicemaxamount)))
				else:
					g.npcs[i].playsound(g.npcs[i].voicesound)
			if g.npcs[i].health<=0 and g.npcs[i].dying==False:
				g.npcs[i].fulldied=True
				g.npcs[i].dying=True
				for m in g.matches:
					if g.npcs[i].joinedmatch!="" and m.owner==g.npcs[i].joinedmatch:
						if g.npcs[i].name in m.players and m.mode!="teamc": m.players.remove(g.npcs[i].name); m.deadplayers.append(g.npcs[i].name)
						if m.started and len(m.players)==1 and (m.mode=="teamk2" or m.mode=="collect" or m.mode=="teamf2" or m.mode=="snow" or m.mode=="sniper" or m.mode=="minecraft" or m.mode=="sword" or m.mode=="g" or m.mode=="g2" or m.mode=="teaml"):
							try: m.send("Match ended. "+g.getpc(m.players[0]).name+" won!",2)
							except: pass
							try: g.n.send_reliable(g.getpc(m.players[0]).peer_id,"play_s win.ogg",0)
							except: pass
							m.send_except(m.players[0],"play_s misc171.ogg",0)
							j=g.getpc(m.players[0])
							item_map={}
							for item in g.dontlose:
								try:
									if j.get_item_count(item)>0: item_map[item]=j.get_item_count(item)
								except: pass
							try: g.getpc(m.players[0]).inv=dict()
							except: pass
							for item in item_map.keys():
								try: j.give(item,item_map[item])
								except: pass

							if m.mode=="teamz": m.clearzombies()
							try:
								g.move_player(g.get_player_index_from(m.players[0]),5,0,0,"lobby")
							except: pass
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
						if len(m.players)==0:
							m.send("Match ended. No one won!",2)
							if m.mode=="teamz": m.clearzombies()
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


				for k in range(len(g.players)):
					if not g.npcs[i].dontkill and (g.players[k].specmap==g.npcs[i].map or g.players[k].map==g.npcs[i].map) and g.players[k].killn==1:
						if g.players[k].matchteam!="" and g.players[k].matchteam!=g.npcs[i].matchteam: g.n.send_reliable(g.players[k].peer_id,"killn enemy "+g.npcs[i].soundname+" has been killed by "+g.npcs[i].hitby+" at coordinates "+str(round(g.npcs[i].x))+", "+str(round(g.npcs[i].y))+", "+str(round(g.npcs[i].z))+". "+g.npcs[i].soundname+" had "+g.npcs[i].weapon,0)
						if g.players[k].matchteam=="": g.n.send_reliable(g.players[k].peer_id,"killn enemy "+g.npcs[i].soundname+" has been killed by "+g.npcs[i].hitby+" at coordinates "+str(round(g.npcs[i].x))+", "+str(round(g.npcs[i].y))+", "+str(round(g.npcs[i].z))+". "+g.npcs[i].soundname+" had "+g.npcs[i].weapon,0)
						if g.players[k].matchteam!="" and g.players[k].matchteam==g.npcs[i].matchteam: g.n.send_reliable(g.players[k].peer_id,"killn teammate "+g.npcs[i].soundname+" has been killed by "+g.npcs[i].hitby+" at coordinates "+str(round(g.npcs[i].x))+", "+str(round(g.npcs[i].y))+", "+str(round(g.npcs[i].z))+". "+g.npcs[i].soundname+" had "+g.npcs[i].weapon,0)
						if "minecraft" not in g.players[k].matchmode: g.n.send_reliable(g.players[k].peer_id,"play_s teammessage2.ogg",0)
						if "minecraft" in g.players[k].matchmode: g.n.send_reliable(g.players[k].peer_id,"play_s killthunder.ogg",0)

				if g.npcs[i].deathsoundamount>0:
					if not g.npcs[i].dontkill: g.play(g.npcs[i].deathsound+str(random(1,g.npcs[i].deathsoundamount)), g.npcs[i].x, g.npcs[i].y, g.npcs[i].z, g.npcs[i].map)
				else:
					if not g.npcs[i].dontkill: g.play(g.npcs[i].deathsound, g.npcs[i].x, g.npcs[i].y, g.npcs[i].z, g.npcs[i].map)
				g.npcs[i].dietimer.restart()
		if g.npcs[i].dietimer.elapsed>0 and g.npcs[i].dying:
			g.npcs[i].dietimer.restart()
			faint=random(1,2)
			if faint==2 and g.npcs[i].fainted==False and (g.npcs[i].matchmode=="teamd" or g.npcs[i].matchmode=="teamz2"):
				g.npcs[i].fainted=True
				g.npcs[i].faint=True
				g.npcs[i].health=20
				g.npcs[i].stun(180000)
				for m in g.matches:
					if g.npcs[i].name in m.players:
						m.teamsend(g.npcs[i].matchteam,g.npcs[i].name+" fainted in coordinates "+str(round(g.npcs[i].x))+", "+str(round(g.npcs[i].y))+", "+str(round(g.npcs[i].z))+".",0)
				g.npcs[i].dying=False
				g.npcs[i].fulldied=False
				return
			if not g.npcs[i].dontkill: g.play(g.get_tile_at(g.npcs[i].x, g.npcs[i].y, g.npcs[i].z, g.npcs[i].map)+"hardland", g.npcs[i].x, g.npcs[i].y, g.npcs[i].z, g.npcs[i].map)
			for weapon in list(g.npcs[i].ammo.keys()):
				c=g.npcs[i].get_ammo_count(weapon)
				g.npcs[i].give(g.get_ammotype(weapon), c)

			g.spawn_corpse(g.npcs[i].x,g.npcs[i].y,g.npcs[i].z,g.npcs[i].map)
			corp=g.corpses[-1]
			corp.owner=g.npcs[i].name
			for key in g.npcs[i].inv.keys():
				spawn_item(g.npcs[i].x,g.npcs[i].y,g.npcs[i].z,g.npcs[i].map,key,g.npcs[i].get_item_count(key),False,corp)

			killer=""
			if string_contains(g.npcs[i].hitby, "'", 1)>-1:
				s=string_split(g.npcs[i].hitby, "'", True)
				killer=s[0]
			else:
				killer=g.npcs[i].hitby
			ind=g.get_player_index_from(killer)
			if ind>-1 and g.players[ind].group!="":
				grp=g.get_group(g.players[ind].group)
				grp.add_kill()
			p=g.get_player_index_from(killer)
			if(p>-1):
				if g.players[p].scoretimer.elapsed>300000:
					if not g.players[p].paid:
						g.players[p].scorepoint+=1
						g.n.send_reliable(g.players[p].peer_id,"You get 1 score point for killing "+g.npcs[i].name+"",2)
					if g.players[p].paid:
						g.players[p].scorepoint+=2
						g.n.send_reliable(g.players[p].peer_id,"You get 2 score point for killing "+g.npcs[i].name+"",2)
					g.n.send_reliable(g.players[p].peer_id,"play_s getpoint.ogg",0)

					g.players[p].scoretimer.restart()
				pc=g.getpc(killer)
				if pc.map!="massacre_in_the_city" and pc.tokentimer.elapsed>300000:
					pc.tokentimer.restart()
					a=random(3,5)
					if pc.paid: a*=2
					pc.zhtoken+=a
					try: g.n.send_reliable(pc.peer_id,"you got "+str(a)+"  zero token",2)
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
				g.players[p].botkills+=1
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

			g.n.broadcast("offline2 "+str(g.npcs[i].x)+" "+str(g.npcs[i].y)+" "+str(g.npcs[i].z)+" "+g.npcs[i].soundname,0)
			g.npcs.remove(g.npcs[i])
			return
def destroy_all_npcs():
	g.npcs.clear()
def can_hit(n,w=""):
	oldw=n.weapon
	if w!="": n.weapon=w
	if 1:
		if 1:
			for wall in g.maps[g.get_map_index(n.map)].mapwalls:

				if wall.health<=0: continue
				wr=vector(n.x,n.y,n.z+n.aim)
				if 1:
					if n.aim>=20: wr.z+=1
					if n.aim<=-20: wr.z-=1

					for wx in range(wall.minx,wall.maxx+1):
						for wy in range(wall.miny,wall.maxy+1):
							for wz in range(wall.minz,wall.maxz+1):

								if(get_3d_distance(wr.x, wr.y, wr.z, wx, wy, wz)<=get_weapon_range(n.weapon)):

									n.weapon=oldw; return calculate_x_y_angle(n.x, n.y, wx, wy)
								else: break

			for x in range(len(g.players)):

				if g.players[x].faint: continue

				if g.players[x].map!=n.map or g.players[x].health<=0: continue
				if g.players[x].ducking and n.aim>-get_weapon_spread(n.weapon): continue
				if g.players[x].joinedmatch==n.joinedmatch and n.joinedmatch!="" and g.players[x].matchteam==n.matchteam and n.matchmode!="teaml"  and n.matchmode!="snow"  and n.matchmode!="sniper"  and n.matchmode!="teamk2" and n.matchmode!="teamf2" and n.matchmode!="sword"  and n.matchmode!="collect"  and n.matchmode!="g" and n.matchmode!="g2" and n.matchmode!="minecraft"  and g.players[x].joinedmatch!="" and g.players[x].matchmode!="" and n.matchmode!="": continue
				wr=vector(n.x,n.y,n.z+n.aim)
				if g.players[x].matchmode=="teamz" and n.joinedmatch==g.players[x].joinedmatch and g.get_tile_at(wr.x, wr.y, 0, n.map)!="hardwood": continue
				if 1:
					if n.aim>=20: wr.z+=1
					if n.aim<=-20: wr.z-=1

					if(get_3d_distance(wr.x, wr.y, wr.z, g.players[x].x, g.players[x].y, g.players[x].z)<=get_weapon_range(n.weapon)):
						n.weapon=oldw; return calculate_x_y_angle(n.x, n.y, g.players[x].x, g.players[x].y)
					else: break
			for x in range(len(g.npcs)):

				if g.npcs[x].faint: continue

				if g.npcs[x].soundname==n.soundname: continue
				if g.npcs[x].joinedmatch==n.joinedmatch and g.npcs[x].matchteam==n.matchteam and n.matchmode!="teaml" and n.matchmode!="snow" and n.matchmode!="sniper" and n.matchmode!="g" and n.matchmode!="teamk2" and n.matchmode!="teamf2" and n.matchmode!="g2" and n.matchmode!="minecraft" and n.matchmode!="sword" and n.matchmode!="collect"  and n.joinedmatch!="": continue
				if g.npcs[x].map!=n.map or g.npcs[x].health<=0: continue
				wr=vector(n.x,n.y,n.z+n.aim)
				if g.npcs[x].matchmode=="teamz" and n.joinedmatch==g.npcs[x].joinedmatch and g.get_tile_at(wr.x, wr.y, 0, n.map)!="hardwood": continue
				if 1:
					if n.aim>=20: wr.z+=1
					if n.aim<=-20: wr.z-=1
					if(get_3d_distance(wr.x, wr.y, wr.z, g.npcs[x].x, g.npcs[x].y, g.npcs[x].z)<=get_weapon_range(n.weapon)):
						n.weapon=oldw; return calculate_x_y_angle(n.x, n.y, g.npcs[x].x, g.npcs[x].y)
					else: break
			for x in range(len(g.motors)):
				oi=g.get_player_index_from(g.motors[x].owner)
				if oi>-1 and g.players[oi].matchteam!="" and g.players[oi].matchteam==n.matchteam: continue

				if len(g.motors[x].players)!=0: continue
				if g.motors[x].map!=n.map or g.motors[x].health<=0: continue
				wr=vector(n.x,n.y,n.z+n.aim)
				if 1:
					if n.aim>=20: wr.z+=1
					if n.aim<=-20: wr.z-=1
					if(get_3d_distance(wr.x, wr.y, wr.z, g.motors[x].x, g.motors[x].y, g.motors[x].z)<=get_weapon_range(n.weapon)):
						n.weapon=oldw; return calculate_x_y_angle(n.x, n.y, g.motors[x].x, g.motors[x].y)
					else: break

			for x in range(len(g.zombies)):

				if g.zombies[x].map!=n.map: continue
				wr=vector(n.x,n.y,n.z+n.aim)
				if 1:
					if n.aim>=20: wr.z+=1
					if n.aim<=-20: wr.z-=1


					if(get_3d_distance(wr.x, wr.y, wr.z, g.zombies[x].x, g.zombies[x].y, g.zombies[x].z)<=get_weapon_range(n.weapon)):
						n.weapon=oldw; return calculate_x_y_angle(n.x, n.y, g.zombies[x].x, g.zombies[x].y)
					else: break
	n.weapon=oldw; return -1