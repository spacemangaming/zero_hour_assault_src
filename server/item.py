import globals as g
from datetime import datetime,timedelta
from random import randint as random
from variable_management import string_contains
from rotation import get_3d_distance
from timer import timer
from file_directories import file_exists
class item:
	def __init__(self,x,y,z,map,itemname,itemamount,dropped=False):
		self.fake=False
		self.x=x
		self.yoursents=[]
		self.dropped=dropped
		self.filechecktimer=timer()
		self.beeptimer=timer()
		self.y=y
		self.z=z
		self.map=map
		self.itemname=itemname
		self.itemamount=itemamount
def itembeeploop():
	played_coordinates=[]
	for i in range(len(g.items)):
		if not hasattr(g.items[i],"fake"): g.items[i].fake=False
		if g.items[i].beeptimer.elapsed>=0:
			g.items[i].beeptimer.restart()
			if (g.items[i].x, g.items[i].y, g.items[i].z, g.items[i].map) not in played_coordinates:
				g.play("itembeep2",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map,pitch=100 if not g.items[i].dropped else 70)
				played_coordinates.append((g.items[i].x, g.items[i].y, g.items[i].z, g.items[i].map))
def itemloop():
	for i in range(len(g.items)):
		if not hasattr(g.items[i],"fake"): g.items[i].fake=False
		if g.items[i].filechecktimer.elapsed>1000:
			g.items[i].filechecktimer.restart()
			if not file_exists("maps/"+g.items[i].map+".map"):
				g.items.remove(g.items[i])
				return

		for p in range(len(g.players)):
			if g.players[p].zombie: continue
			if(g.players[p].map!=g.items[i].map or g.players[p].dead==True):
				continue
			if not g.items[i].dropped and get_3d_distance(g.players[p].x,g.players[p].y,g.players[p].z,g.items[i].x,g.items[i].y,g.items[i].z)<=4 and g.players[p].map==g.items[i].map and (g.players[p].android or g.players[p].ios):
				amount=g.items[i].itemamount
				if g.items[i].itemname in g.invlimits and g.players[p].get_item_count(g.items[i].itemname)+g.items[i].itemamount>g.invlimits[g.items[i].itemname]: amount=g.invlimits[g.items[i].itemname]-g.players[p].get_item_count(g.items[i].itemname)
				if amount<=0:
					if g.players[p].name not in g.items[i].yoursents: g.items[i].yoursents.append(g.players[p].name); g.n.send_reliable(g.players[p].peer_id,"Your inventory cannot hold more of this item",2)
					return
				g.players[p].give(g.items[i].itemname,amount)
				g.n.send_reliable(g.players[p].peer_id,""+str(amount)+" "+str(g.items[i].itemname)+"",2)
				if 1:
					if 1:
						if 1:
							g.players[p].items_got+=1
							if g.players[p].matchmode=="teamcollect":
								for match in g.matches:
									if match.owner==g.players[p].joinedmatch:
										if g.players[p].matchteam=="red": match.redgot+=1
										if g.players[p].matchteam=="blue": match.bluegot+=1

				for p2 in g.players:
					if p2.specplayer==g.players[p].name: g.n.send_reliable(p2.peer_id,""+str(amount)+" "+str(g.items[i].itemname)+"",2)
				if g.items[i].itemname=="small_potion":
					g.play("getcola2",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				if g.items[i].itemname=="vitality_potion":
					g.play("getcola2",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				if g.items[i].itemname=="revival_nectar":
					g.play("getcola2",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

				elif g.items[i].itemname=="5.56x45mm":
					g.play("getmachinegunammo",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="mkek_jng90":
					g.play("mkek_jng90draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="dragunov_psl":
					g.play("dragunov_psldraw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

				elif g.items[i].itemname=="mkek_mpt76k":
					g.play("mkek_mpt76kdraw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="mkek_yavuz16":
					g.play("mkek_yavuz16draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="colt1911":
					g.play("colt1911draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="fnhfnp40":
					g.play("fnhfnp40draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="fnhfnp45":
					g.play("fnhfnp45draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="berettaM9":
					g.play("ks123shotgundraw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)


				elif g.items[i].itemname=="40S&W":
					g.play("getshotgunammo",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

				elif g.items[i].itemname=="IthicaM37":
					g.play("IthicaM37draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

				elif g.items[i].itemname=="9mm":
					g.play("getpistolammo",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="45_ACP":
					g.play("getpistolammo",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

				elif g.items[i].itemname=="12_gauge":
					g.play("getshotgunammo",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="7.62x51mm":
					g.play("getsniperammo",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="molotov_cocktail":
					g.play("getmoolotov",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="hand_grenade":
					g.play("getparachute",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="m4":
					g.play("m4draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

				elif g.items[i].itemname=="binoculars":
					g.play("binocularsclose",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="wooden_sword":
					g.play("getwooden_sword",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="stone_sword":
					g.play("getstone_sword",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="diamond_sword":
					g.play("getdiamond_sword",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

				else:
					g.play("itemget",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				if amount==g.items[i].itemamount: g.items.pop(i)
				else: g.items[i].itemamount-=amount
				return
		for p in range(len(g.npcs)):
			if g.npcs[p].zombie: continue
			if g.npcs[p].map!=g.items[i].map: continue
			if(get_3d_distance(g.npcs[p].x,g.npcs[p].y,g.npcs[p].z,g.items[i].x,g.items[i].y,g.items[i].z)<=4 and g.npcs[p].map==g.items[i].map):
				g.npcs[p].give(g.items[i].itemname,g.items[i].itemamount)
				g.npcs[p].items_got+=1
				if g.npcs[p].matchmode=="teamcollect":
					for match in g.matches:
						if match.owner==g.npcs[p].joinedmatch:
							if g.npcs[p].matchteam=="red": match.redgot+=1
							if g.npcs[p].matchteam=="blue": match.bluegot+=1
				g.npcs[p].targetitem=-1
				for p2 in g.players:
					if p2.specplayer==g.npcs[p].soundname: g.n.send_reliable(p2.peer_id,""+str(g.items[i].itemamount)+" "+str(g.items[i].itemname)+"",2)

				if g.items[i].itemname=="small_potion":
					g.play("getcola2",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				if g.items[i].itemname=="vitality_potion":
					g.play("getcola2",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				if g.items[i].itemname=="revival_nectar":
					g.play("getcola2",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

				elif g.items[i].itemname=="5.56x45mm":
					g.play("getmachinegunammo",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="mkek_jng90":
					g.play("mkek_jng90draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="dragunov_psl":
					g.play("dragunov_psldraw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

				elif g.items[i].itemname=="mkek_mpt76k":
					g.play("mkek_mpt76kdraw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="mkek_yavuz16":
					g.play("mkek_yavuz16draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="colt1911":
					g.play("colt1911draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="fnhfnp40":
					g.play("fnhfnp40draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="fnhfnp45":
					g.play("fnhfnp45draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

				elif g.items[i].itemname=="berettaM9":
					g.play("ks123shotgundraw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

				elif g.items[i].itemname=="40S&W":
					g.play("getshotgunammo",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

				elif g.items[i].itemname=="IthicaM37":
					g.play("IthicaM37draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

				elif g.items[i].itemname=="9mm":
					g.play("getpistolammo",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="45_ACP":
					g.play("getpistolammo",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

				elif g.items[i].itemname=="12_gauge":
					g.play("getshotgunammo",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="7.62x51mm":
					g.play("getsniperammo",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="molotov_cocktail":
					g.play("getmoolotov",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="hand_grenade":
					g.play("getparachute",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="m4":
					g.play("m4draw",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

				elif g.items[i].itemname=="binoculars":
					g.play("binocularsclose",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="wooden_sword":
					g.play("getwooden_sword",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="stone_sword":
					g.play("getstone_sword",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)
				elif g.items[i].itemname=="diamond_sword":
					g.play("getdiamond_sword",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

				else:
					g.play("itemget",g.items[i].x,g.items[i].y,g.items[i].z,g.items[i].map)

				g.items.pop(i)
				return

def spawn_item(x,y,z,map,itemname,itemamount,dropped=False,corpse=None,pindex=-1):
	if dropped:
		for chest in g.chests:
			if get_3d_distance(x, y, z, chest.x, chest.y, chest.z)<=1 and map==chest.map:
				if itemname not in chest.items:
					chest.items.append(itemname)
					chest.itemamounts.append(itemamount)
					for base in g.group_bases:
						if pindex>-1 and g.players[pindex].map=="basement"+base.name+base.mapappend: base.chestlog+=g.players[pindex].name+" put "+str(itemamount)+" "+itemname+" at "+get_current_date()+"\n"
					return
				else:
					index=chest.items.index(itemname)
					chest.itemamounts[index]+=itemamount
					for base in g.group_bases:
						if pindex>-1 and g.players[pindex].map=="basement"+base.name+base.mapappend: base.chestlog+=g.players[pindex].name+" put "+str(itemamount)+" "+itemname+" at "+get_current_date()+"\n"
					return
	if corpse is not None:
		if itemname not in corpse.items:
			corpse.items.append(itemname)
			corpse.itemamounts.append(itemamount)
			return
		else:
			index=corpse.items.index(itemname)
			corpse.itemamounts[index]+=itemamount
			return

	loll=item(x,y,z,map,itemname,itemamount,dropped)
	g.items.append(loll)
g.itemloop=itemloop
def get_current_date():
	return str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
