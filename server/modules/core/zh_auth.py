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

ANN_DIR = os.path.normpath(
	os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "announcements")
)


def login(user, password, mail, compid, peer_id):
	compbanloop()

	# Reject invalid characters before any DB lookup
	if "/" in user or ":" in user:
		g.n.send_reliable(peer_id,"banned Your account name contains an unexpected symbol. Please contact the developers.",0)
		return

	# Check player exists in DB
	if not _db.player_exists(user):
		g.n.send_reliable(peer_id,"doesnotexist",0)
		return

	compbanned=is_compbanned(compid)
	compbanned2=is_compbanned(compid,user)
	if compbanned2 and not compbanned:
		if _db.charexists(user,"permaban") and _db.charread(user,"permaban")=="1":
			send_reliable(peer_id, "banned Error. You have been permanently banned. Reason: "+_db.charread(user,"banreason"),0)
		elif _db.charexists(user,"banenddate"):
			send_reliable(peer_id, "banned Error. You have been banned. Reason: "+_db.charread(user,"banreason")+". The ban will end after "+get_playerban_end_time(user), 0)
		return
	elif compbanned:
		user2=get_player_from_compid(compid)
		perm1 = _db.charread(user2,"permaban","0")=="1" if _db.player_exists(user2) else False
		perm2 = _db.charread(user,"permaban","0")=="1"
		if not perm1 and not perm2:
			send_reliable(peer_id, "banned Error. You have been banned. Reason: "+get_compban_reason(compid)+". The ban will end after "+get_compban_end_time(compid), 0)
		else:
			send_reliable(peer_id, "banned Error. You have been permanently banned. Reason: "+get_compban_reason(compid),0)
		return

	# Verify password and mail
	stored_pass = _db.charread(user, "pass")
	if stored_pass != password:
		g.n.send_reliable(peer_id,"wrongpass",0)
		return

	stored_mail = _db.charread(user, "mail")
	if stored_mail != mail:
		g.n.send_reliable(peer_id,"wrongmail",0)
		return

	# Kick duplicate session (same compid) or reject (different compid)
	for i in range(len(g.players)):
		if g.players[i].name == user:
			if compid == g.players[i].compid:
				remove_from_server(i)
			else:
				g.n.send_reliable(peer_id,"banned This user is already logged in.",0)
				return

	if not compid_handlercheck(compid):
		add_compid(compid, user)

	# Persist current compid
	_db.charwrite(user, "compid", compid)

	# Update authorized compids list
	auth_raw = _db.charread(user, "authorized_compids", "")
	auth_computers = [c for c in auth_raw.split("\n") if c]
	if compid not in auth_computers:
		auth_computers.append(compid)
	_db.charwrite(user, "authorized_compids", "\n".join(auth_computers))

	# Send map data
	m = _db.charread(user, "map", "lobby")
	for i in g.matches:
		if i.get_cwmap()==m and user not in i.players: m="lobby"
	if get_map_index(m) < 0:
		m="lobby"
	stuff=g.maps[get_map_index(m)].rawdata
	g.n.send_reliable(peer_id,"mapdata "+stuff,0)
	g.n.send_reliable(peer_id, "facing "+_db.charread(user,"facing","0"), 0)
	g.n.send_reliable(peer_id, "x "+_db.charread(user,"x","5"), 0)
	g.n.send_reliable(peer_id, "y "+_db.charread(user,"y","0"), 0)
	g.n.send_reliable(peer_id, "z "+_db.charread(user,"z","0"), 0)
	g.n.send_reliable(peer_id,"startmoving",0)
	if file_exists("frozen.txt"):
		g.n.send_reliable(peer_id,"stopmoving",0)
		g.n.send_reliable(peer_id,"play_s important.ogg",0)
		g.n.send_reliable(peer_id,"Attention. The game is frozen. Please be patient.",2)

	g.n.send_reliable(peer_id, "loggedin", 0)
	try:
		_send_pinned_announcements(peer_id)
	except Exception as ex:
		print(f"Error sending pinned announcements on login: {ex}")



def getplayer_by_peer(id):
	for i in range(len(g.players)):
	
		if(g.players[i].peer_id==id):
		
			return i
			
		
	return -1


def get_player_index(id):
	founds=[]
	for i in range(len(g.players)):
		try:
			if g.players[i].peer_id==id: founds.append(i)
		except: pass
	try: return founds[-1]
	except: return -1


def get_player_index_from(name):
	founds=[]
	for i in range(len(g.players)):
		if g.players[i] is not None and g.players[i].name.lower()==name.lower(): founds.append(i)
	try: return founds[-1]
	except: return -1


def get_player_index_fromnpc(name):
	for i in range(len(g.players)):
		if g.players[i] is not None and g.players[i].name.lower()==name.lower(): return i
	for i in range(len(g.npcs)):
		if g.npcs[i] is not None and g.npcs[i].name.lower()==name.lower(): return i

	return -1


def getpc(name):
	for i in range(len(g.players)):
		if g.players[i] is not None and g.players[i].name.lower()==name.lower(): return g.players[i]
	for i in range(len(g.npcs)):
		if g.npcs[i] is not None and g.npcs[i].name.lower()==name.lower(): return g.npcs[i]

	return None


def create(un,pw,mail,gender,compid,id):
	if " " in un or "." in un or ":" in un or "/" in un:
		g.n.send_reliable(id,"banned invalid input",0); return
	if not un.isascii():
		g.n.send_reliable(id, "banned Username must contain only ASCII characters (English alphabet/numbers).", 0)
		return
	compbanloop()
	compbanned=is_compbanned(compid)
	if compbanned:
		banned_player = get_player_from_compid(compid)
		perm = _db.player_exists(banned_player) and _db.charread(banned_player,"permaban","0")=="1"
		if not perm:
			g.n.send_reliable(id, "banned Error. You have been banned. Reason: "+get_compban_reason(compid)+". The ban will end after "+get_compban_end_time(compid), 0)
		else:
			g.n.send_reliable(id, "banned Error. You have been permanently banned. Reason: "+get_compban_reason(compid), 0)
		return

	if is_mailbanned(mail):
		g.n.send_reliable(id, "banned This email address is not allowed to create an account.", 0)
		return
	if is_tempmail(mail):
		g.n.send_reliable(id, "banned Temporary/disposable email addresses are not allowed. Please use a real email address.", 0)
		return

	# Check if username already exists (case-insensitive)
	if _db.player_exists_icase(un):
		g.n.send_reliable(id,"alreadyexists",0)
		return
	for i in range(len(usernames)):
		if un == usernames[i]:
			g.n.send_reliable(id,"alreadyexists",0)
			return

	if not compid or len(compid) < 5:
		g.n.send_reliable(id, "banned Invalid computer hardware identifier.", 0)
		return
	numaccounts=0
	for ch in g.comphandles:
		if ch.compid==compid: numaccounts+=1
	if numaccounts>=2:
		g.n.send_reliable(id, "message you only have right to create two accounts per computer.", 0); return

	# Create the player row in SQLite with default values
	_db.create_player_row(un)
	_db.charwrite(un, "pass",                pw)
	_db.charwrite(un, "mail",               mail)
	_db.charwrite(un, "gender",             gender)
	_db.charwrite(un, "compid",             compid)
	_db.charwrite(un, "authorized_compids", compid)
	_db.charwrite(un, "x",                  5)
	_db.charwrite(un, "y",                  0)
	_db.charwrite(un, "z",                  0)
	_db.charwrite(un, "map",               "lobby")
	_db.charwrite(un, "facing",             0)
	_db.charwrite(un, "health",             100)
	_db.charwrite(un, "scorepoint",         0)
	_db.charwrite(un, "createdate",         datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

	add_compid(compid, un)
	g.n.broadcast("play_s alert2.ogg",0)
	g.n.broadcast("A new character named "+un+" has been created! We wish them an epic journey in the game.",2)
	g.n.send_reliable(id,"created",0)


def remove_from_server(ind2=-1,force=False):
	if ind2 > -1 and ind2 < len(g.players) and g.players[ind2] is not None:
		if getattr(g.players[ind2], "controlled_turret", None) is not None:
			g.players[ind2].controlled_turret.operator = None
			g.players[ind2].controlled_turret = None

	if g.players[ind2].flag>0:
		for f in range(g.players[ind2].flag): spawn_flag(g.players[ind2].x, g.players[ind2].y, g.players[ind2].z, g.players[ind2].map, g.players[ind2].matchteam)
		g.players[ind2].flag=0


	for bomb in g.timebombs:
		if not force and not g.players[ind2].blockoffline and g.players[ind2].distancecheck(bomb.x,bomb.y,bomb.z)<=50 and bomb.map==g.players[ind2].map:
			g.players[ind2].blockoffline=True
			g.players[ind2].blockofflinetimer.restart()
			return

	for base in g.group_bases:
		if not force and g.players[ind2].map=="basement"+base.name+base.mapappend:
			move_player(ind2,base.x,base.y,base.z,base.map)
	if(not force and ind2>-1) :
		try: save_char(ind2)
		except: pass
		for m in g.matches:
			if 1:
				m.removeplayertimer.restart()
		if not g.players[ind2].hidden:
			for i in g.players:
				if i is None:
					continue
				if getattr(i, "friendonlinemessage", 0) == 1 and g.players[ind2] is not None and getattr(g.players[ind2], "friendlist", None) is not None and i.name in g.players[ind2].friendlist:
					g.n.send_reliable(i.peer_id,"offline "+str(g.players[ind2].x)+" "+str(g.players[ind2].y)+" "+str(g.players[ind2].z)+" "+g.players[ind2].name+" "+g.players[ind2].map,0)
				else:
					g.n.send_reliable(i.peer_id,"offline2 "+str(g.players[ind2].x)+" "+str(g.players[ind2].y)+" "+str(g.players[ind2].z)+" "+g.players[ind2].name+" "+g.players[ind2].map,0)
	if ind2>-1:
		g.players[ind2]=None
		g.players.pop(ind2)


def _send_pinned_announcements(peer_id):
	if not os.path.exists(ANN_DIR):
		return
	for f in os.listdir(ANN_DIR):
		if f.endswith(".announcement"):
			try:
				with open(os.path.join(ANN_DIR, f), "r", encoding="utf-8") as file:
					data = json.load(file)
				if data.get("pinned"):
					title = data.get("title", "No Title")
					content = data.get("content", "")
					author = data.get("author", "Admin")
					timestamp = data.get("timestamp", "")
					msg = f"Announcement: {title}\nBy {author} ({timestamp})\n\n{content}"
					g.n.send_reliable(peer_id, "play_s important.ogg", 0)
					g.n.send_reliable(peer_id, msg, 2)
			except Exception as ex:
				print(f"Error loading/sending announcement {f}: {ex}")


