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
import db as _db


def file_get_contents(filename, mode="r"):
	if file_exists(filename)==False:
		return ""
	if "b" in mode:
		f=open(filename, mode)
		ret=f.read()
		f.close()
		return ret
	else:
		encodings = ["utf-8", "cp1254", "latin-1"]
		for enc in encodings:
			try:
				f=open(filename, mode, encoding=enc)
				ret=f.read()
				f.close()
				return ret
			except UnicodeDecodeError:
				continue
		# Final fallback to prevent any crash
		f=open(filename, mode, encoding="utf-8", errors="replace")
		ret=f.read()
		f.close()
		return ret


# ── SQLite-backed char helpers ────────────────────────────────────────────────

def charwrite(name, thing, value):
	"""Write a text/int/real player field to SQLite."""
	try:
		_db.charwrite(name, thing, value)
	except Exception:
		pass


def charwriteb(name, thing, value):
	"""Write a binary (BLOB) player field to SQLite."""
	try:
		_db.charwriteb(name, thing, value)
	except Exception:
		pass


def charread(name, thing, default=""):
	"""Read a player field from SQLite as a string."""
	return _db.charread(name, thing, default)


def charreadb(name, thing):
	"""Read a binary player field from SQLite as bytes."""
	return _db.charreadb(name, thing)


def charexists(name, thing):
	"""Return True if the player field has been set."""
	return _db.charexists(name, thing)


def chardelete(name, thing):
	"""Clear a player field (set to NULL)."""
	_db.chardelete(name, thing)


def save_char(index):
	np=g.players[index].name
	charwrite(np, "last_admin_login_ticket_count", g.players[index].last_admin_login_ticket_count)
	charwrite(np,"x",g.players[index].x)
	charwrite(np,"spatialized_by",g.players[index].spatialized_by)
	charwrite(np,"spatializertimer",g.players[index].spatializertimer.elapsed)
	charwrite(np,"backpacks_level",g.players[index].backpacks_level)
	charwrite(np,"beacon",g.players[index].beacon)
	# parachuted is intentionally not saved — it resets to False on every login
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
	if g.players[index].faint:
		charwrite(np, "faint", "1")
	else:
		chardelete(np, "faint")
		chardelete(np, "fainttime")
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
		charwriteb(np, "banned", pickle.dumps(g.players[index].matchbanned))
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


def _sv_pickle(key, obj):
	_db.sv_write(key, pickle.dumps(obj))

def _sv_unpickle(key):
	data = _db.sv_read(key)
	if not data: return None
	return pickle.loads(data)


def save_matches():
	_sv_pickle("matches.dat", g.matches)

def load_matches():
	v = _sv_unpickle("matches.dat")
	if v is not None: g.matches = v
	for m in g.matches: m.removeplayertimer.restart()


def save_chests():
	_db.sv_write_text("chesttimer.txt", str(chesttimer.elapsed))
	_db.sv_write_text("tasktimer.txt",  str(tasktimer.elapsed))
	_db.sv_write_text("task.txt",       str(g.task))
	_db.sv_write_text("survivestage.txt", str(survivestage))
	_db.sv_write_text("survivetime.txt",  str(survivetimer.elapsed))
	_db.sv_write_text("freedomsurvivor.txt", str(g.freedomsurvivor))
	_sv_pickle("chests.dat", g.chests)

def load_chests():
	v = _sv_unpickle("chests.dat")
	if v is not None: g.chests = v
	val = _db.sv_read_text("chesttimer.txt")
	if val: chesttimer.elapsed = int(val)
	val = _db.sv_read_text("survivestage.txt")
	if val:
		global survivestage
		survivestage = int(val)
	val = _db.sv_read_text("freedomsurvivor.txt")
	if val: g.freedomsurvivor = val
	val = _db.sv_read_text("survivetime.txt")
	if val: survivetimer.elapsed = int(val)
	val = _db.sv_read_text("tasktimer.txt")
	if val: tasktimer.elapsed = int(val)
	val = _db.sv_read_text("task.txt")
	if val: g.task = int(val)


def save_electrics():
	_sv_pickle("electrics.dat", g.electrics)

def load_electrics():
	v = _sv_unpickle("electrics.dat")
	if v is not None: g.electrics = v
	for e in g.electrics:
		e.mid = spawn_moving_sound("electricty.ogg", e.x, e.y, e.z, e.map, "", 100)


def save_corpses():
	_sv_pickle("corpses.dat", g.corpses)

def load_corpses():
	v = _sv_unpickle("corpses.dat")
	if v is not None: g.corpses = v


def save_tickets():
	_sv_pickle("tickets.dat", g.tickets)

def save_votes():
	_sv_pickle("votes.dat", g.votes)

def save_rain():
	ls = [g.rain, g.rainstarttimer, g.rainstarttime, g.raintime,
	      g.rainvoltimer, g.rainvoltime, g.rainvolume, g.raintimer]
	_sv_pickle("rain.dat", ls)

def save_ladders():
	_sv_pickle("ladders.dat", g.ladders)

def save_barricades():
	_sv_pickle("barricades.dat", g.barricades)

def load_rain():
	ls = _sv_unpickle("rain.dat")
	if ls is None: return
	g.rain, g.rainstarttimer, g.rainstarttime, g.raintime, \
	g.rainvoltimer, g.rainvoltime, g.rainvolume, g.raintimer = ls

def load_ladders():
	v = _sv_unpickle("ladders.dat")
	if v is not None: g.ladders = v

def load_barricades():
	v = _sv_unpickle("barricades.dat")
	if v is not None: g.barricades = v

def load_tickets():
	v = _sv_unpickle("tickets.dat")
	if v is not None: g.tickets = v
	for ticket in g.tickets:
		if "closetimer" not in ticket.keys(): ticket["closetimer"] = timer()

def load_votes():
	v = _sv_unpickle("votes.dat")
	if v is not None: g.votes = v
	for v2 in g.votes:
		if not hasattr(v2, "stick"):    v2.stick = False
		if not hasattr(v2, "comments"): v2.comments = []


def save_timebombs():
	_sv_pickle("timebombs.dat", g.timebombs)

def load_timebombs():
	v = _sv_unpickle("timebombs.dat")
	if v is not None: g.timebombs = v


def save_zks():
	_sv_pickle("zks.dat", g.zks)

def load_zks():
	v = _sv_unpickle("zks.dat")
	if v is not None: g.zks = v


def save_mines():
	_sv_pickle("mines.dat", g.mines)

def load_mines():
	v = _sv_unpickle("mines.dat")
	if v is not None: g.mines = v


def save_bikes():
	_sv_pickle("bikes.dat", g.bikes)

def load_bikes():
	v = _sv_unpickle("bikes.dat")
	if v is not None: g.bikes = v


def save_motors():
	_sv_pickle("motors.dat", g.motors)

def load_motors():
	v = _sv_unpickle("motors.dat")
	if v is not None: g.motors = v
	for m in g.motors:
		if m.running: m.running = False; m.pitch = 100


def save_npcs():
	_sv_pickle("npcs.dat", g.npcs)

def load_npcs():
	v = _sv_unpickle("npcs.dat")
	if v is not None: g.npcs = v
	for n in g.npcs:
		if not hasattr(n, "tokentimer"): n.tokentimer = timer()
		if not hasattr(n, "scoretimer"):  n.scoretimer = timer()
		if not hasattr(n, "hidden"):      n.hidden = False


def save_zombies():
	_sv_pickle("zombies.dat", g.zombies)

def load_zombies():
	v = _sv_unpickle("zombies.dat")
	if v is not None: g.zombies = v


def save_timeditems():
	_sv_pickle("timeditems.dat", g.timeditems)

def load_timeditems():
	v = _sv_unpickle("timeditems.dat")
	if v is not None: g.timeditems = v


def save_groups():
	_sv_pickle("groups.dat", g.groups)

def load_groups():
	v = _sv_unpickle("groups.dat")
	if v is not None: g.groups = v
	for group in g.groups:
		if not hasattr(group, "freedomhit"):   group.freedomhit = 1
		if not hasattr(group, "zhtoken"):      group.zhtoken = 0
		if not hasattr(group, "donations"):    group.donations = ""
		if not hasattr(group, "actions"):      group.actions = ""
		if not hasattr(group, "announcement"): group.announcement = ""
		if not hasattr(group, "join_requests"): group.join_requests = []


def save_communitys():
	_sv_pickle("communitys.dat", g.communitys)

def load_communitys():
	v = _sv_unpickle("communitys.dat")
	if v is not None: g.communitys = v
	for c in g.communitys:
		if not hasattr(c, "actions"):       c.actions = ""
		if not hasattr(c, "announcement"):  c.announcement = ""
		if not hasattr(c, "join_requests"): c.join_requests = []


def save_group_bases():
	_sv_pickle("group_bases.dat", g.group_bases)

def load_group_bases():
	v = _sv_unpickle("group_bases.dat")
	if v is not None: g.group_bases = v
	for base in g.group_bases:
		if not hasattr(base,"mapappend"):       base.mapappend=""
		if not hasattr(base,"ammo"):            base.ammo=10
		if not hasattr(base,"firetimer"):       base.firetimer=timer()
		if not hasattr(base,"password"):        base.password=""
		if not hasattr(base,"doorontimer"):     base.doorontimer=timer()
		if not hasattr(base,"dooropening"):     base.dooropening=False
		if not hasattr(base,"chestlog"):        base.chestlog=""
		if not hasattr(base,"wall_level"):      base.wall_level=1
		if not hasattr(base,"turrets"):         base.turrets=[]
		if not hasattr(base,"generator_on"):    base.generator_on=False
		if not hasattr(base,"generator_fuel"):  base.generator_fuel=0.0
		if not hasattr(base,"generator_timer"): base.generator_timer=timer()
		if not hasattr(base,"siren_timer"):     base.siren_timer=timer()


def save_items():
	_sv_pickle("items.dat", g.items)

def load_items():
	v = _sv_unpickle("items.dat")
	if v is not None: g.items = v
	for item in g.items:
		if not hasattr(item,"yoursents"): item.yoursents=[]


def save_flags():
	_sv_pickle("flags.dat", g.flags)

def load_flags():
	v = _sv_unpickle("flags.dat")
	if v is not None: g.flags = v


def load_mailbans():
	val = _db.sv_read_text("mailbans.txt", "")
	if val:
		g.mailbans = [m.lower().strip() for m in val.split("\n") if m.strip()]
	elif file_exists("mailbans.txt"):
		# fallback to filesystem on first run
		g.mailbans = [m.lower().strip() for m in file_get_contents("mailbans.txt").split("\n") if m.strip()]
		_db.sv_write_text("mailbans.txt", "\n".join(g.mailbans))
	else:
		g.mailbans = []

def save_mailbans():
	_db.sv_write_text("mailbans.txt", "\n".join(g.mailbans))


def is_mailbanned(mail):
	return mail.lower().strip() in g.mailbans


def ban_mail(mail):
	m=mail.lower().strip()
	if m and m not in g.mailbans:
		g.mailbans.append(m)
		save_mailbans()

