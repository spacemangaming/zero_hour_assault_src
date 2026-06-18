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

ANN_DIR = os.path.normpath(
	os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "announcements")
)


def login(user, password, mail, compid, peer_id):
	compbanloop()
	#for p in g.players:
		#if p.compid==compid: g.n.send_reliable(peer_id,"banned error. You can't login to the game from the same computer 2 or more times",0); return
	#for p in g.players:
		#if str(g.n.get_peer_address(p.peer_id))==str(g.n.get_peer_address(peer_id)): g.n.send_reliable(peer_id,"banned error. You can't login to the game from the same network 2 or more times",0); return
#	if file_exists("chars/"+user+"/beta.usr")==False and file_exists("chars/"+user+"/developer.usr")==False: g.n.send_reliable(peer_id,"banned you are not betatester of this version. Contact with developers for more assistance",0); return

	if(not directory_exists("chars/"+user) or 
		not file_exists("chars/"+user+"/pass.usr") or 
		not file_exists("chars/"+user+"/mail.usr") or
		not file_exists("chars/"+user+"/map.usr") or
		not file_exists("chars/"+user+"/facing.usr") or
		not file_exists("chars/"+user+"/x.usr") or
		not file_exists("chars/"+user+"/y.usr") or
		not file_exists("chars/"+user+"/z.usr")):
	
		g.n.send_reliable(peer_id,"doesnotexist",0)
		return
	if "/" in user:
		g.n.send_reliable(peer_id,"banned Your account name contain an unexpected symbol. Please contact with developers for more info.",0)
		return
	if ":" in user:
		g.n.send_reliable(peer_id,"banned Your account name contain an unexpected symbol. Please contact with developers for more info.",0)
		return

	"""
	if(not file_exists("chars/"+user+"/developer.usr")):
	
		g.n.send_reliable(peer_id,"banned You cannot log in to the game at this time. Reason: The game will be updated turkiye time at 9:30 PM. We kindly ask for your patience during this time.",0)
		return
"""
	compbanned=is_compbanned(compid)
	compbanned2=is_compbanned(compid,user)
	if compbanned2 and not compbanned:
		if file_exists("chars/"+user+"/permaban.usr"): send_reliable(peer_id, "banned Error. You have been permanently banned. Reason: "+file_get_contents("chars/"+user+"/banreason.usr"),0)
		elif file_exists("chars/"+user+"/banenddate.usr"): send_reliable(peer_id, "banned Error. You have been banned. Reason: "+file_get_contents("chars/"+user+"/banreason.usr")+". The ban will end after "+get_playerban_end_time(user), 0)
		return
	elif compbanned:
		user2=get_player_from_compid(compid)
		if not file_exists("chars/"+user2+"/permaban.usr") and not file_exists("chars/"+user+"/permaban.usr"): send_reliable(peer_id, "banned Error. You have been banned. Reason: "+get_compban_reason(compid)+". The ban will end after "+get_compban_end_time(compid), 0)
		elif file_exists("chars/"+user2+"/permaban.usr") or file_exists("chars/"+user+"/permaban.usr"): send_reliable(peer_id, "banned Error. You have been permanently banned. Reason: "+get_compban_reason(compid),0)
		return
	dir="chars/"+user
	f=open(dir+"/pass.usr","r")
	contents=f.read()
	f.close()
	if(contents!=password):
	
		g.n.send_reliable(peer_id,"wrongpass",0)
		return
		
	f=open(dir+"/mail.usr","r")
	contents2=f.read()
	f.close()
	if(contents2!=mail):
	
		g.n.send_reliable(peer_id,"wrongmail",0)
		return
		
	# if file_exists("chars/"+user+"/pending_email_verify.usr"):
	# 	g.n.send_reliable(peer_id,"verify",0)
	# 	return

	compids=file_get_contents("chars/"+user+"/authorized_compids.usr").split("\n")
	authreq=0
	if file_exists("chars/"+user+"/authreq.usr"): authreq=int(file_get_contents("chars/"+user+"/authreq.usr"))
	# if authreq==1 and compid not in compids:
	# 	if file_exists("chars/"+user+"/lastverify.usr"):
	# 		verifydate=pickle.loads(file_get_contents("chars/"+user+"/lastverify.usr","rb"))
	# 		if not time_difference_exceeds_2_hours(datetime.now(),verifydate):
	# 			g.n.send_reliable(peer_id,"message Error. This computer is not authorized to log into your account, but you already authorized one computer in the last 2 hours. You can only authorize one computer per 2 hours.",0); return
	# 	g.n.send_reliable(peer_id,"verify",0)
	# 	return

	for i in range(len(g.players)):
		if(g.players[i].name==user):
			if compid==g.players[i].compid: remove_from_server(i)
			else: g.n.send_reliable(peer_id,"banned This user is already logged in.",0); return
	if not compid_handlercheck(compid):
		add_compid(compid, user)

	f=open(dir+"/compid.usr", "w")
	f.write(compid)
	f.close()

	f=open(dir+"/map.usr","r")
	m=f.read()
	f.close()
	for i in g.matches:
		if i.get_cwmap()==m and user not in i.players: m="lobby"
	if(get_map_index(m)<0):
		m="lobby"
	stuff=g.maps[get_map_index(m)].rawdata
	g.n.send_reliable(peer_id,"mapdata "+stuff,0)
	f=open(dir+"/facing.usr","r")
	g.n.send_reliable(peer_id, "facing "+f.read(), 0)
	f.close()
	f=open(dir+"/x.usr","r")
	g.n.send_reliable(peer_id, "x "+f.read(), 0)
	f.close()
	f=open(dir+"/y.usr","r")
	g.n.send_reliable(peer_id, "y "+f.read(), 0)
	f.close()
	f=open(dir+"/z.usr","r")
	g.n.send_reliable(peer_id, "z "+f.read(), 0)
	f.close()
	g.n.send_reliable(peer_id,"startmoving",0)
	if file_exists("frozen.txt")==True:
		g.n.send_reliable(peer_id,"stopmoving",0)

		g.n.send_reliable(peer_id,"play_s important.ogg",0)
		g.n.send_reliable(peer_id,"Attention. The game is frozen. Please be patient.",2)

	auth_computers=file_get_contents("chars/"+user+"/authorized_compids.usr").split("\n")
	if compid not in auth_computers: auth_computers.append(compid)
	file_put_contents("chars/"+user+"/authorized_compids.usr","\n".join(auth_computers))

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
	if " " in un or "." in un or ":" in un or "/" in un: g.n.send_reliable(id,"banned invalid input",0); return
	if not un.isascii():
		g.n.send_reliable(id, "banned Username must contain only ASCII characters (English alphabet/numbers).", 0)
		return
	compbanloop()
	if(not directory_exists("chars")):
		directory_create("chars")
#	if file_exists("chars/"+un+"/beta.usr")==False: g.n.send_reliable(id,"banned you are not betatester of this version. Contact with developers for more assistance",0); return
	compbanned=is_compbanned(compid)
	if compbanned==True:
		if not file_exists("chars/"+get_player_from_compid(compid)+"/permaban.usr"): g.n.send_reliable(id, "banned Error. You have been banned. Reason: "+get_compban_reason(compid)+". The ban will end after "+get_compban_end_time(compid), 0)
		if file_exists("chars/"+get_player_from_compid(compid)+"/permaban.usr"): g.n.send_reliable(id, "banned Error. You have been permanently banned. Reason: "+get_compban_reason(compid), 0)
		return

	if is_mailbanned(mail):
		g.n.send_reliable(id, "banned This email address is not allowed to create an account.", 0)
		return

	if is_tempmail(mail):
		g.n.send_reliable(id, "banned Temporary/disposable email addresses are not allowed. Please use a real email address.", 0)
		return

	dir="chars/"+un

	if(directory_exists2(dir.lower())):

		g.n.send_reliable(id,"alreadyexists",0)
		return

	for i in range(len(usernames)):
		if un==usernames[i]:
			g.n.send_reliable(id,"alreadyexists",0)
			return
	if not compid or len(compid) < 5:
		g.n.send_reliable(id, "banned Invalid computer hardware identifier.", 0)
		return
	numaccounts=0
	for ch in g.comphandles:
		if ch.compid==compid:
			numaccounts+=1
	if numaccounts>=2: g.n.send_reliable(id, "message you only have right to create two accounts per computer.", 0); return
	g.n.broadcast("play_s alert2.ogg",0)
	g.n.broadcast("A new character named "+un+" has been created! We wish them an epic journey in the game.",2)
	directory_create(dir)
	f=open(dir+"/x.usr","w")
	f.write("5")
	f.close()
	f=open(dir+"/scorepoint.usr","w")
	f.write("0")
	f.close()

	f=open(dir+"/y.usr","w")
	f.write("0")
	f.close()
	f=open(dir+"/z.usr","w")
	f.write("0")
	f.close()
	f=open(dir+"/map.usr","w")
	f.write("lobby")
	f.close()
	f=open(dir+"/gender.usr","w")
	f.write(gender)
	f.close()


	f=open(dir+"/facing.usr","w")
	f.write("0")
	f.close()
	f=open(dir+"/pass.usr","w")
	f.write(pw)
	f.close()
	f=open(dir+"/mail.usr","w")
	f.write(mail)
	f.close()

	f=open(dir+"/health.usr","w")
	f.write("100")
	f.close()
	try:
		f=open(dir+"/maldied.usr","w")
		f.close()
	except: pass
	f=open(dir+"/compid.usr", "w")
	f.write(compid)
	f.close()
	f=open(dir+"/authorized_compids.usr", "w")
	f.write(compid)
	f.close()

	# file_put_contents(dir+"/pending_email_verify.usr", "")
	add_compid(compid, un)
	charwrite(un,"createdate",str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
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


