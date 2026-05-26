import globals as g
import os
import time
import pickle
import json
import datetime
import urllib.parse
import requests
from threading import Thread
from timer import timer

def file_get_contents(filename, mode="r"):
	ret=""
	if file_exists(filename)==False:
		return ""
	f=open(filename, mode)
	ret=f.read()
	f.close()
	return ret


def charwrite(name,thing,value):
	try:
		f=open("chars/"+name+"/"+thing+".usr","w")
		f.write(str(value))
		f.close()
	except: pass


def charwriteb(name,thing,value):
	try:
		f=open("chars/"+name+"/"+thing+".usr","wb")
		f.write(value)
		f.close()
	except: pass


def save_char(index):
	np=g.players[index].name
	charwrite(np, "last_admin_login_ticket_count", g.players[index].last_admin_login_ticket_count)
	charwrite(np,"x",g.players[index].x)
	charwrite(np,"spatialized_by",g.players[index].spatialized_by)
	charwrite(np,"spatializertimer",g.players[index].spatializertimer.elapsed)
	charwrite(np,"backpacks_level",g.players[index].backpacks_level)
	charwrite(np,"beacon",g.players[index].beacon)
	charwrite(np,"parachuted",("1" if g.players[index].parachuted else "0"))
	charwriteb(np,"backpacktimer",pickle.dumps(g.players[index].backpacktimer))
	charwrite(np,"adrenalinetime",g.players[index].adrenalinetimer.elapsed)
	charwrite(np,"jammertime",g.players[index].jammertimer.elapsed)
	charwrite(np,"helitimer",g.players[index].helitimer.elapsed)
	charwrite(np,"weapon",g.players[index].weapon)
	charwrite(np,"weapon2",g.players[index].weapon2)
	charwrite(np,"helijumptimer",g.players[index].helijumptimer.elapsed)
	charwrite(np,"freedomhelicopter",str(g.players[index].freedomhelicopter))
	charwrite(np,"freedomhelicoptertimer",str(g.players[index].freedomhelicoptertimer.elapsed))
	charwrite(np,"ticketmail",g.players[index].ticketmail)
	charwrite(np,"communitymessage",g.players[index].communitymessage)
	charwrite(np,"matchinvite",g.players[index].matchinvite)
	charwrite(np,"eventalerts",g.players[index].eventalerts)
	charwrite(np,"mapsound",g.players[index].mapsound)
	charwrite(np,"tokentransfer",g.players[index].tokentransfer)
	charwrite(np,"authreq",g.players[index].authreq)
	charwrite(np,"votenotify",g.players[index].votenotify)
	charwrite(np,"motorhistory",g.players[index].motorhistory)
	charwrite(np,"headhits",g.players[index].headhits)
	charwrite(np,"headshots",g.players[index].headshots)
	charwrite(np,"leghits",g.players[index].leghits)
	charwrite(np,"legshots",g.players[index].legshots)

	charwrite(np,"istyping",g.players[index].istyping)
	charwrite(np,"chestpickupnotify",g.players[index].chestpickupnotify)



	charwrite(np,"fainttime",g.players[index].fainttimer.elapsed)
	if g.players[index].faint: 	charwrite(np,"faint","")
	else:
		file_delete("chars/"+g.players[index].name+"/faint.usr")
		file_delete("chars/"+g.players[index].name+"/fainttime.usr")
	if not g.players[index].hidden: charwrite(np,"lastactive",str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))


	charwrite(np,"mapmessage",g.players[index].mapmessage)
	charwrite(np,"groupmessage",g.players[index].groupmessage)
	charwrite(np,"groupinvitation",g.players[index].groupinvitation)
	charwrite(np,"communityinvitation",g.players[index].communityinvitation)

	charwrite(np,"pmmessage",g.players[index].pmmessage)
	charwrite(np,"friendmessage",g.players[index].friendmessage)
	charwrite(np,"voicemessage",g.players[index].voicemessage)
	charwrite(np,"voicemessage2",g.players[index].voicemessage2)
	charwrite(np,"matchmessage",g.players[index].matchmessage)
	charwrite(np,"teammessage",g.players[index].teammessage)
	charwrite(np,"friendonlinemessage",g.players[index].friendonlinemessage)
	charwrite(np,"playerkills",g.players[index].playerkills)
	charwrite(np,"playerdeaths",g.players[index].playerdeaths)
	charwrite(np,"botkills",g.players[index].botkills)
	charwrite(np,"botdeaths",g.players[index].botdeaths)
	charwrite(np,"flag",g.players[index].flag)
	charwrite(np,"zhtoken",g.players[index].zhtoken)
	charwrite(np,"eventpoint",g.players[index].eventpoint)
	charwrite(np,"currenteventpoint",g.players[index].currenteventpoint)
	charwriteb(np,"task_data",pickle.dumps(g.players[index].task_data))
	charwrite(np,"matchteam",g.players[index].matchteam)
	charwrite(np,"joinedmatch",g.players[index].joinedmatch)
	charwrite(np,"matchmode",g.players[index].matchmode)

	charwrite(np,"lang",g.players[index].lang)
	charwrite(np,"y",g.players[index].y)
	charwrite(np,"z",g.players[index].z)
	try:
		f=open("chars/"+g.players[index].name+"/banned.usr","wb")
		f.write(pickle.dumps(g.players[index].matchbanned))
		f.close()
	except: pass
	charwrite(np,"map",g.players[index].map)
	charwrite(np,"gender",g.players[index].gender)
	charwrite(np,"status",g.players[index].status)

	charwrite(np,"blockvoice3",g.players[index].blockvoice3)
	charwrite(np,"hidden",("1" if g.players[index].hidden else "0"))

	charwrite(np,"langchan",g.players[index].langchan)
	charwrite(np,"shieldhitchance",g.players[index].shieldhitchance)
	charwrite(np,"helmethitchance",g.players[index].helmethitchance)
	charwrite(np,"lasthelmethitchance",g.players[index].lasthelmethitchance)
	charwrite(np,"chesttoken",g.players[index].chesttoken)


	charwrite(np,"health",g.players[index].health)
	charwrite(np,"corpse_bomb",g.players[index].corpse_bomb)
	charwrite(np,"scorepoint",g.players[index].scorepoint)
	charwrite(np,"scorerank",g.players[index].scorerank)

	charwrite(np,"facing",g.players[index].facing)
	charwriteb(np,"inventory",pickle.dumps(g.players[index].inv))
	charwriteb(np,"storeinventory",pickle.dumps(g.players[index].storeinv))
	charwriteb(np,"ammo",pickle.dumps(g.players[index].ammo))
	charwriteb(np,"current_char",pickle.dumps(g.players[index].current_char))
	charwriteb(np,"tokenplayers",pickle.dumps(g.players[index].tokenplayers))
	charwriteb(np,"silenced",pickle.dumps(g.players[index].silenced))
	charwriteb(np,"bought_chars",pickle.dumps(g.players[index].bought_chars))
	charwriteb(np,"pendingfriendlist",pickle.dumps(g.players[index].pendingfriendlist))
	charwriteb(np,"blocks",pickle.dumps(g.players[index].blocks))

	charwriteb(np,"groupinvitations",pickle.dumps(g.players[index].groupinvitations))
	charwriteb(np,"communityinvitations",pickle.dumps(g.players[index].communityinvitations))

	charwriteb(np,"friendlist",pickle.dumps(g.players[index].friendlist))


def save_all_chars():
	for i in range(len(g.players)):
	
		save_char(i)
		
	save_matches()
	save_chests()
	save_electrics()
	save_corpses()
	save_votes()
	save_tickets()
	save_barricades()
	save_ladders()
	save_rain()
	save_mines()
	save_timebombs()
	save_zks()

	save_motors()
	save_bikes()
	save_npcs()
	save_timeditems()
	save_groups()
	save_communitys()

	save_group_bases()
	save_zombies()
	save_items()
	save_flags()


def save_matches():
	with open("matches.dat","wb") as f:
		f.write(pickle.dumps(g.matches))


def load_matches():
	with open("matches.dat","rb") as f:
		try: g.matches=pickle.loads(f.read())
		except: pass
	for m in g.matches: m.removeplayertimer.restart()


def save_chests():
	with open("chesttimer.txt","w") as f: f.write(str(chesttimer.elapsed))
	with open("tasktimer.txt","w") as f: f.write(str(tasktimer.elapsed))
	with open("task.txt","w") as f: f.write(str(g.task))
	with open("survivestage.txt","w") as f: f.write(str(survivestage))
	with open("survivetime.txt","w") as f: f.write(str(survivetimer.elapsed))
	with open("freedomsurvivor.txt","w") as f: f.write(str(g.freedomsurvivor))
	with open("chests.dat","wb") as f:
		f.write(pickle.dumps(g.chests))


def load_chests():
	with open("chests.dat","rb") as f:
		try: g.chests=pickle.loads(f.read())
		except: pass
	if file_exists("chesttimer.txt"):
		with open("chesttimer.txt","r") as f: chesttimer.elapsed=int(f.read())
	if file_exists("survivestage.txt"):
		with open("survivestage.txt","r") as f: survivestage=int(f.read())
	if file_exists("freedomsurvivor.txt"):
		with open("freedomsurvivor.txt","r") as f: g.freedomsurvivor=str(f.read())

	if file_exists("survivetime.txt"):
		with open("survivetime.txt","r") as f: survivetimer.elapsed=int(f.read())

	if file_exists("tasktimer.txt"):
		with open("tasktimer.txt","r") as f: tasktimer.elapsed=int(f.read())
	if file_exists("task.txt"):
		with open("task.txt","r") as f: g.task=int(f.read())


def save_electrics():
	with open("electrics.dat","wb") as f:
		f.write(pickle.dumps(g.electrics))


def load_electrics():
	with open("electrics.dat","rb") as f:
		try: g.electrics=pickle.loads(f.read())
		except: pass
	for e in g.electrics:
		e.mid=spawn_moving_sound("electricty.ogg",e.x,e.y,e.z,e.map,"",100)


def save_corpses():
	with open("corpses.dat","wb") as f:
		f.write(pickle.dumps(g.corpses))


def load_corpses():
	with open("corpses.dat","rb") as f:
		try: g.corpses=pickle.loads(f.read())
		except: pass


def save_tickets():
	with open("tickets.dat","wb") as f:
		f.write(pickle.dumps(g.tickets))


def save_votes():
	with open("votes.dat","wb") as f:
		f.write(pickle.dumps(g.votes))


def save_rain():
	with open("rain.dat","wb") as f:
		ls=[g.rain,g.rainstarttimer,g.rainstarttime,g.raintime,g.rainvoltimer,g.rainvoltime,g.rainvolume,g.raintimer]
		f.write(pickle.dumps(ls))


def save_ladders():
	with open("ladders.dat","wb") as f:
		f.write(pickle.dumps(g.ladders))


def save_barricades():
	with open("barricades.dat","wb") as f:
		f.write(pickle.dumps(g.barricades))


def load_rain():
	with open("rain.dat","rb") as f:
		ls=pickle.loads(f.read())
		g.rain=ls[0]
		g.rainstarttimer=ls[1]
		g.rainstarttime=ls[2]
		g.raintime=ls[3]
		g.rainvoltimer=ls[4]
		g.rainvoltime=ls[5]
		g.rainvolume=ls[6]
		g.raintimer=ls[7]


def load_ladders():
	with open("ladders.dat","rb") as f:
		g.ladders=pickle.loads(f.read())


def load_barricades():
	with open("barricades.dat","rb") as f:
		g.barricades=pickle.loads(f.read())


def load_tickets():
	with open("tickets.dat","rb") as f:
		g.tickets=pickle.loads(f.read())
	for ticket in g.tickets:
		if "closetimer" not in ticket.keys(): ticket["closetimer"]=timer()


def load_votes():
	with open("votes.dat","rb") as f:
		g.votes=pickle.loads(f.read())
	# NEW: Initialize 'comments' attribute for older loaded polls if it doesn't exist
	for v in g.votes:
		if not hasattr(v,"stick"): v.stick=False
		if not hasattr(v,"comments"): v.comments=[] # NEW: Ensure comments list exists for old data


def save_timebombs():
	with open("timebombs.dat","wb") as f:
		f.write(pickle.dumps(g.timebombs))


def load_timebombs():
	with open("timebombs.dat","rb") as f:
		g.timebombs=pickle.loads(f.read())


def save_zks():
	with open("zks.dat","wb") as f:
		f.write(pickle.dumps(g.zks))


def load_zks():
	with open("zks.dat","rb") as f:
		g.zks=pickle.loads(f.read())


def save_mines():
	with open("mines.dat","wb") as f:
		f.write(pickle.dumps(g.mines))


def load_mines():
	with open("mines.dat","rb") as f:
		g.mines=pickle.loads(f.read())


def save_bikes():
	with open("bikes.dat","wb") as f:
		f.write(pickle.dumps(g.bikes))


def load_bikes():
	with open("bikes.dat","rb") as f:
		g.bikes=pickle.loads(f.read())


def save_motors():
	with open("motors.dat","wb") as f:
		f.write(pickle.dumps(g.motors))


def load_motors():
	with open("motors.dat","rb") as f:
		g.motors=pickle.loads(f.read())
	for m in g.motors:
		if m.running: m.running=False; m.pitch=100


def save_npcs():
	with open("npcs.dat","wb") as f:
		f.write(pickle.dumps(g.npcs))


def load_npcs():
	with open("npcs.dat","rb") as f:
		g.npcs=pickle.loads(f.read())
	for n in g.npcs:
		if not hasattr(n,"tokentimer"): n.tokentimer=timer()
		if not hasattr(n,"scoretimer"): n.scoretimer=timer()
		if not hasattr(n,"hidden"): n.hidden=False


def save_zombies():
	with open("zombies.dat","wb") as f:
		f.write(pickle.dumps(g.zombies))


def load_zombies():
	with open("zombies.dat","rb") as f:
		g.zombies=pickle.loads(f.read())


def save_timeditems():
	with open("timeditems.dat","wb") as f:
		f.write(pickle.dumps(g.timeditems))


def load_timeditems():
	with open("timeditems.dat","rb") as f:
		g.timeditems=pickle.loads(f.read())


def save_groups():
	with open("groups.dat","wb") as f:
		f.write(pickle.dumps(g.groups))


def load_groups():
	with open("groups.dat","rb") as f:
		g.groups=pickle.loads(f.read())
	for group in g.groups:
		if not hasattr(group,"freedomhit"): group.freedomhit=1
		if not hasattr(group,"zhtoken"): group.zhtoken=0
		if not hasattr(group,"donations"): group.donations=""
		if not hasattr(group,"actions"): group.actions=""
		if not hasattr(group,"announcement"): group.announcement=""
	for item in g.groups:
		if not hasattr(item, "join_requests"): item.join_requests=[]


def save_communitys():
	with open("communitys.dat","wb") as f:
		f.write(pickle.dumps(g.communitys))


def load_communitys():
	with open("communitys.dat","rb") as f:
		g.communitys=pickle.loads(f.read())
	for community in g.communitys:
		if not hasattr(community,"actions"): community.actions=""
		if not hasattr(community,"announcement"): community.announcement=""
	for item in g.communitys:
		if not hasattr(item, "join_requests"): item.join_requests=[]


def save_group_bases():
	with open("group_bases.dat","wb") as f:
		f.write(pickle.dumps(g.group_bases))


def load_group_bases():
	with open("group_bases.dat","rb") as f:
		g.group_bases=pickle.loads(f.read())
	for base in g.group_bases:
		if not hasattr(base,"mapappend"): base.mapappend=""
		if not hasattr(base,"ammo"): base.ammo=10
		if not hasattr(base,"firetimer"): base.firetimer=timer()
		if not hasattr(base,"password"): base.password=""
		if not hasattr(base,"doorontimer"): base.doorontimer=timer()
		if not hasattr(base,"dooropening"): base.dooropening=False
		if not hasattr(base,"chestlog"): base.chestlog=""


def save_items():
	with open("items.dat","wb") as f:
		f.write(pickle.dumps(g.items))


def load_items():
	with open("items.dat","rb") as f:
		g.items=pickle.loads(f.read())
	for item in g.items:
		if not hasattr(item,"yoursents"): item.yoursents=[]


def save_flags():
	with open("flags.dat","wb") as f:
		f.write(pickle.dumps(g.flags))


def load_flags():
	with open("flags.dat","rb") as f:
		g.flags=pickle.loads(f.read())


def load_mailbans():
	if file_exists("mailbans.txt"):
		g.mailbans=[m.lower().strip() for m in file_get_contents("mailbans.txt").split("\n") if m.strip()]
	else:
		g.mailbans=[]


def save_mailbans():
	file_put_contents("mailbans.txt","\n".join(g.mailbans))


def is_mailbanned(mail):
	return mail.lower().strip() in g.mailbans


def ban_mail(mail):
	m=mail.lower().strip()
	if m and m not in g.mailbans:
		g.mailbans.append(m)
		save_mailbans()

