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

class server_menu:
	def __init__(self):
		self.menuitems=my_list()
		self.menuids=my_list()
		self.menuacts=my_list()
		self.initial_packet=""
		self.store=False
		self.paid_store=False
		self.intro=""
	def add(self, item, id, act=True):
		self.menuitems.append(item)
		self.menuids.append(id)
		self.menuacts.append(act)
	def reset(self):
		self.menuids=my_list()
		self.menuitems=my_list()

	def send(self, id):
		if len(self.menuids)>0 and len(self.menuitems)>0:
			l=""
			for i in range(len(self.menuitems)):
				l+=str(self.menuitems[i])+"<"+str(self.menuids[i])+"<"+str(self.menuacts[i])+"\t"
			index=get_player_index(id)
			if index>-1:
				g.players[index].menuitems=self.menuitems
				g.players[index].menuids=self.menuids
				g.players[index].menuacts=self.menuacts
				g.players[index].initial_packet=self.initial_packet
			send_menu(id, self.intro, self.initial_packet, l, self.store)


def find_directories(path):
	l=my_list()
	if not os.path.exists(path):
		return l
	for each in os.listdir(path):
		if os.path.isdir(path+"/"+each):
			l.append(each)
	return l


def send_menu(id, menuintro, text, items, store=False):
	menuintro=string_replace(menuintro, " ", "[SPCE]", True)
	text=string_replace(text, " ", "[SPCE", True)
	g.n.send_reliable(id, "launchmenu "+menuintro+" "+text+" "+items+"", 0)


def remove_duplicate_mapwalls(mapwalls):
	seen_mapwalls = set()
	index_to_remove = []

	for i, mapwall in enumerate(mapwalls):
		wall_tuple = (
			mapwall.minx,
			mapwall.maxx,
			mapwall.miny,
			mapwall.maxy,
			mapwall.minz,
			mapwall.maxz
		)

		if wall_tuple in seen_mapwalls:
			index_to_remove.append(i)
		else:
			seen_mapwalls.add(wall_tuple)

	for index in reversed(index_to_remove):
		del mapwalls[index]


def bilet_cevapla(soru):
    cevap = qa_chain.run(soru)
    
    if "üzgünüm" in cevap.lower() or len(cevap.strip()) < 10:
        return "Mesajınızı aldık, en kısa zamanda size dönüş yapılacaktır."
    else:
        return cevap


def adminsend(mesaj):
	if file_exists("adminlog.txt")==False:
		f=open("adminlog.txt","w")
		f.close()
	f=open("adminlog.txt","a")
	f.write(""+mesaj+", "+get_date()+", "+get_time(True, True)+"\n")
	f.close()
	for i in g.players:
		if i.is_admin()==True or i.dev==True or i.moderator==True:
			g.n.send_reliable(i.peer_id,"play_s misc205.ogg",0)
			g.n.send_reliable(i.peer_id,"adminmessage "+mesaj,0)


def adminsend2(mesaj):
	if file_exists("adminlog.txt")==False:
		f=open("adminlog.txt","w")
		f.close()
	f=open("adminlog.txt","a")
	f.write(""+mesaj+", "+get_date()+", "+get_time(True, True)+"\n")
	f.close()
	for i in g.players:
		if i.is_admin()==True or i.dev==True or i.moderator==True:
			g.n.send_reliable(i.peer_id,"play_s misc205.ogg",0)
			g.n.send_reliable(i.peer_id,"adminmessage "+mesaj,0)


def adminsendsound(sound):
	for i in g.players:
		if i.is_admin()==True or i.dev==True or i.moderator==True:
			g.n.send_reliable(i.peer_id,"play_s "+sound+".ogg",0)


def get_date(include_weekday=False, numerical=True):
	return ""


def get_time(twelvehour=True, include_seconds=True):
	return str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def developersend(mesaj):
	if 1:
		data=file_get_contents("error.log")
		f=open("error.log","a")
		if not string_contains(data,mesaj,1)>-1: f.write(""+mesaj+"")
		f.close()
		for i in range(len(g.players)):
			if g.players[i].dev==True:
#				g.n.send_reliable(g.players[i].peer_id,"play_s admchat.ogg",0)
				g.n.send_reliable(g.players[i].peer_id,mesaj,2)


def stn(n):
	return string_to_number(n)


def send_reliable(peer, mess, channel, playerindex=None):
	if(playerindex is not None):
	
		x=playerindex.x
		y=playerindex.y
		z=playerindex.z
		for i in range(len(g.players)):
		
			if(g.players[i].x > x-25 and g.players[i].x < x+25 and g.players[i].y > y-25 and g.players[i].y < y+25 and g.players[i].z > z-25 and g.players[i].z < z+25 and g.players[i].map==playerindex.map):
			
				g.n.send_reliable(g.players[i].peer_id, mess, channel)
				
			
		
	else:
	
		g.n.send_reliable(peer, mess, channel)


def send_plus(excluding_name,packet,channel,r=True):
	for i in range(len(g.players)):
	
		if(excluding_name!=g.players[i].name):
		
			if(r==True):
				g.n.send_reliable(g.players[i].peer_id,packet,channel)
			else:
				g.n.send_reliable(g.players[i].peer_id,packet,channel)


def send_plus2(excluding_name,packet,channel,r=True):
	for i in range(len(g.players)):
	
		if(excluding_name!=g.players[i].name):
		
			if(r==True):
				g.n.send_reliable(g.players[i].peer_id,packet,channel)
			else:
				g.n.send_unreliable(g.players[i].peer_id,packet,channel)


class my_list(list):
	def find(self, val):
		for i, x in enumerate(self):
			if x==val:
				return i
		return -1


def sort_descending(input_list):
	return sorted(input_list, reverse=True)


def convert_to_list(arr):
	if len(arr) == 0:
		return ""
	
	processed = []
	for name in arr:
		index = get_player_index_from(name)
		# Oyuncu sunucuda değilse VEYA sunucudaysa ama 'hidden' değeri True ise offline göster
		if index == -1 or g.players[index] is None or g.players[index].hidden:
			processed.append(name + ", offline")
		else:
			processed.append(name + ", online")
	
	if len(processed) == 1:
		return processed[0]
	
	# Listeyi formatla: "isim1, isim2 ve isim3"
	return ", ".join(processed[:-1]) + " and " + processed[-1]


def convert_to_list2(arr):
	list=""
	if len(arr)==0:
		return "no one"
	if len(arr)==1:
		if get_player_index_from(arr[0])==-1: arr[0]=arr[0]+""
		else: arr[0]=arr[0]+""

		return arr[0]
	for i in range(len(arr)):

		if i==len(arr)-1:
			list+=" and "+arr[i]
		else:
			list+=arr[i]+", "
	return list


def send_serverbox(peerid, mode=0, maxlength=-1, autosend=0, keypresses=-1, sendtext="server_box", text="enter text"):
	send_reliable(peerid, "input +=1"+str(mode)+"+=1"+str(maxlength)+"+=1"+str(autosend)+"+=1"+str(keypresses)+"+=1"+str(sendtext)+"+=1"+str(text), 0)


def get_leader_hit_player(b):
	if b.hitby!="":
		i=getpc(b.hitby)
		if i is not None:
			p=i
			if get_tile_at(p.x,p.y,0,p.map)=="hardwood": return p
	if b.matchteam=="red":
		for p in g.players:
			if b.m.redleader in p.hitby2:
				i=getpc(p.name)
				if i is not None:
					p=i
					if get_tile_at(p.x,p.y,0,p.map)=="hardwood": return p

		for p in g.npcs:
			if b.m.redleader in p.hitby2:
				i=getpc(p.name)
				if i is not None:
					p=i
					if get_tile_at(p.x,p.y,0,p.map)=="hardwood": return p


	if b.matchteam=="blue":
		for p in g.players:
			if b.m.blueleader in p.hitby2:
				i=getpc(p.name)
				if i is not None:
					p=i
					if get_tile_at(p.x,p.y,0,p.map)=="hardwood": return p

		for p in g.npcs:
			if b.m.redleader in p.hitby2:
				i=getpc(p.name)
				if i is not None:
					p=i
					if get_tile_at(p.x,p.y,0,p.map)=="hardwood": return p

	return None


def load_store_data(filename="store.txt"):
	data = []

	try:
		with open(filename, 'r') as file:
			for line in file:
				item_info = line.strip().split(':')
				if len(item_info) == 4:
					item_dict = {
						"name": item_info[0],
						"price": item_info[1],
						"category": item_info[2],
						"description": item_info[3]
					}
					data.append(item_dict)

	except FileNotFoundError:
		return {}

	return data


def load_event_store_data(filename="event_store.txt"):
	data = []

	try:
		with open(filename, 'r') as file:
			for line in file:
				item_info = line.strip().split(':')
				if len(item_info) == 3:
					item_dict = {
						"name": item_info[0],
						"price": item_info[1],
						"description": item_info[2]
					}
					data.append(item_dict)

	except FileNotFoundError:
		return {}

	return data


def get_friend_count(p):
	index=get_player_index_from(p)
	ret=0
	for pl in g.players:
		if not pl.hidden and pl.name in g.players[index].friendlist: ret+=1
	return ret


def find_ticket_by_title(title):
	for ticket in g.tickets:
		if ticket["title"]==title: return ticket


def find_ticket_by_id(id):
	for ticket in g.tickets:
		if ticket["id"]==id: return ticket


def get_datetime_difference(input_date):
	date_format = "%Y-%m-%d %H:%M:%S"
	try: input_datetime = datetime.strptime(input_date, date_format)
	except: return ""
	current_datetime = datetime.now()
	time_difference = int((current_datetime - input_datetime).total_seconds())

	time_units = {
		'millennium': 31536000000,
		'century': 3153600000,
		'decade': 315360000,
		'year': 31536000,
		'month': 2592000,
		'day': 86400,
		'hour': 3600,
		'minute': 60,
		'second': 1,
	}

	result = []
	for unit_name, unit_seconds in time_units.items():
		unit_value = time_difference // unit_seconds
		time_difference %= unit_seconds

		if unit_value:
			if unit_name == 'millennium':
				result.append(f'{unit_value} {unit_name if unit_value == 1 else "millennia"}')
			elif unit_name == 'century':
				result.append(f'{unit_value} {unit_name if unit_value == 1 else "centuries"}')
			else:
				result.append(f'{unit_value} {unit_name if unit_value == 1 else unit_name + "s"}')

	if len(result) > 1:
		result[-1] = 'and ' + result[-1]

	return ', '.join(result)


def convert_minutes_to_datetime_object(minutes):
	current_datetime = datetime.now()

	new_datetime = current_datetime + timedelta(minutes=minutes)

	return new_datetime


def send_yesno_question(peer,message):
	g.n.send_reliable(peer,"yesno "+message,0)
	while True:
		netloop()
		if getattr(g, "e", None) is not None and isinstance(g.e.message,str):
			if g.e.message.startswith("yesno "): return g.e.message.replace("yesno ","")
		gameloops()


def strtobool(b):
	if b=="True": return True
	else: return False


def removefriendadd(m,index):
	for pl in g.players[index].friendlist:
		m.add(pl,pl)


def offlinepm(player,player2,message):
	dir="chars/"+player
	if os.path.isfile(dir+"/pmdata.usr"): pmdata=pickle.loads(file_get_contents(dir+"/pmdata.usr","rb"))
	else: pmdata={}
	pmdata[player2]=message
	file_put_contents(dir+"/pmdata.usr",pickle.dumps(pmdata),"wb")


def offlinestaff(player,message):
	dir="chars/"+player
	if os.path.isfile(dir+"/staffdata.usr"): staffdata=pickle.loads(file_get_contents(dir+"/staffdata.usr","rb"))
	else: staffdata={}
#	staffdata[player2]=message
	file_put_contents(dir+"/staffdata.usr",pickle.dumps(staffdata),"wb")


def url_encode(url):
	return urllib.parse.quote(url)


def url_decode(url):
	return urllib.parse.unquote(url)


def url_get(url):
	try:
		raw_response=requests.get(url)
		return raw_response.text
	except:
		return "HTTP Request error!"


def make_request(endpoint, payload):
    try:
        response_data = requests.post(endpoint, data=payload)
        return response_data.text
    except Exception as err:
        return str(err)


def notify_admins(message_text):
    feedback = []
    for admin_uid in ADMIN_IDS:
        answer = make_request(API_ENDPOINT, {
            "chat_id": admin_uid,
            "text": message_text
        })
        feedback.append(answer)
    return feedback


def make_request2(endpoint, payload):
    try:
        response_data = requests.post(endpoint, data=payload)
        return response_data.text
    except Exception as err:
        return str(err)


def notify_admins2(message_text):
    feedback = []
    for admin_uid in ADMIN_IDS2:
        answer = make_request2(API_ENDPOINT2, {
            "chat_id": admin_uid,
            "text": message_text
        })
        feedback.append(answer)
    return feedback


def send_mail(user, sub, mailmess):
	user=url_encode(user)
	mailmess=url_encode(mailmess)
	sub=url_encode(sub)
	res = url_get("https://nbmstudios.com/mailsend.php?id=nbmcantsend&mail="+user+"&mess="+mailmess+"&sub="+sub)
	return res


def load_tempmail_domains():
	global _tempmail_domains
	if file_exists("tempmail_domains.txt"):
		_tempmail_domains={d.lower().strip() for d in file_get_contents("tempmail_domains.txt").split("\n") if d.strip()}


def is_tempmail(mail):
	if "@" not in mail:
		return False
	domain=mail.split("@")[-1].lower().strip()
	return domain in _tempmail_domains


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


def ms_to_readable_time2(milliseconds):
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


def get_group(name):
	for grp in g.groups:
		if grp.name==name: return grp


def get_community(name):
	for grp in g.communitys:
		if grp.name==name: return grp


def randomstring(length=10):
	temp="abcdefghijklmnopqrstuvwxyz1234567890"
	ret=""
	for i in range(length):
		ret=ret+temp[random(0, (len(temp)-1))]
	return ret


def time_difference_exceeds_24_hours(dt1, dt2):
	time_difference = abs(dt1 - dt2)
	return time_difference > timedelta(hours=24)


def time_difference_exceeds_1_week(dt1, dt2):
	time_difference = abs(dt1 - dt2)
	return time_difference > timedelta(days=7)


def time_difference_exceeds_2_hours(dt1, dt2):
	time_difference = abs(dt1 - dt2)
	return time_difference > timedelta(hours=2)


def url_post2(url,params):
	Thread(target=url_post,args=(url,params,)).start()


def minutes_to_timestamp(minutes):
	current_time = int(tm.time())
	future_time = current_time + (minutes * 60)  
	return int(future_time)  


def ticketcheck():
	for ticket in g.tickets:
		if not ticket["closed"] and not ticket["pending"] and ticket["closetimer"].elapsed>172800000:
			if 1:
				ticket["closed"]=True
				ticket["messages"]+="\nThis ticket was closed because it had no activity in the last 2 days in "+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				ticket["lastupdate"]=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				adminsend("the ticket "+ticket["title"]+" was closed because it had no activity in the last 2 days")
				notify_admins("zero hour assault, the ticket "+ticket["title"]+" was closed because it had no activity in the last 2 days")
				getmail=file_get_contents("chars/"+ticket["owner"]+"/mail.usr")
				send_mail(getmail,"your ticket "+ticket["title"]+" has been closed","Hello "+ticket["owner"]+"<br>your ticket "+ticket["title"]+" has been closed because it had no activity in the last 2 days<br>Below is all the ticket messages:<br>"+ticket["messages"]+"<br>If you have more questions or need help, please create a support ticket again from the game or contact us at contact@nbmstudios.com<br>regards,<br>Nbm studios team")

				if 1:
					ind=get_player_index_from(ticket["owner"])
					if ind>-1:
						g.n.send_reliable(g.players[ind].peer_id,"Your ticket with id "+ticket["id"]+" is updated, please check!",0)
						g.n.send_reliable(g.players[ind].peer_id,"play_s misc304.ogg",0)
					else:
						file_put_contents("chars/"+ticket["owner"]+"/ticketinform.usr","Your ticket with "+ticket["id"]+" is updated, please check!")


def is_enabled_ticket_mail(user):
	if not file_exists("chars/"+user+"/ticketmail.usr"): return True
	ret=file_get_contents("chars/"+user+"/ticketmail.usr")
	if ret=="1": return True
	return False


def get_current_date():
	return str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def randomstring(length=10):
	temp="abcdefghijklmnopqrstuvwxyz1234567890"
	ret=""
	for i in range(length):
		ret=ret+temp[random(0, (len(temp)-1))]
	return ret


def get_long_name_for_size_unit(unit):
    unit_names = {
        'B': 'Bytes',
        'KB': 'Kilobytes',
        'MB': 'Megabytes',
        'GB': 'Gigabytes',
        'TB': 'Terabytes',
        'PB': 'Petabytes',
        'EB': 'Exabytes',
        'ZB': 'Zettabytes',
        'YB': 'Yottabytes'
    }
    return unit_names.get(unit, unit)


def get_file_size(filename, return_long_unit=False):
    try:
        size = os.path.getsize(filename)
        return convert_size(size, return_long_unit)
    except:
        return "File size not available"


def get_file_size_b(filename, return_long_unit=False):
    try:
        size = os.path.getsize(filename)
        if return_long_unit:
            unit = get_long_name_for_size_unit('B')
        else:
            unit = 'B'
        return f"{size} {unit}"
    except:
        return "File size not available"


def get_file_size_bit(filename, return_long_unit=False):
    try:
        size = os.path.getsize(filename) * 8
        if return_long_unit:
            unit = get_long_name_for_size_unit('b')
        else:
            unit = 'b'
        return f"{size} {unit}"
    except:
        return "File size not available"


def convert_size(size, return_long_unit=False):
    bytes = int(size)
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    unit_index = 0
    while bytes >= 1024 and unit_index < len(units) - 1:
        bytes /= 1024
        unit_index += 1
    unit = units[unit_index]

    if return_long_unit:
        unit = get_long_name_for_size_unit(unit)

    return f"{round(bytes, 2)} {unit}"


def convert_size_bit(size, return_long_unit=False):
    bytes = int(size / 8)
    units = ['b', 'Kb', 'Mb', 'Gb', 'Tb', 'Pb', 'Eb', 'Zb', 'Yb']
    unit_index = 0
    while bytes >= 1024 and unit_index < len(units) - 1:
        bytes /= 1024
        unit_index += 1
    unit = units[unit_index]

    if return_long_unit:
        unit = get_long_name_for_size_unit(unit)

    return f"{round(bytes, 2)} {unit}"


def get_language_used_count(lng):
	ret=0
	for char in os.listdir("chars"):
		if file_get_contents("chars/"+char+"/lang.usr")==lng: ret+=1
		if file_get_contents("chars/"+char+"/lang.usr")=="" and lng=="English": ret+=1
	return str(ret)


def get_open_ticket_count():
	ret=0
	for ticket in g.tickets:
		if not ticket["pending"] and not ticket["closed"]: ret+=1
	return ret


def get_closed_ticket_count():
	ret=0
	for ticket in g.tickets:
		if ticket["closed"]: ret+=1
	return ret


def get_pending_ticket_count():
	ret=0
	for ticket in g.tickets:
		if ticket["pending"]: ret+=1
	return ret

