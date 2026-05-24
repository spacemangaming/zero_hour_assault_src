import globals as g
import pickle
import os
from datetime import datetime
from file_directories import file_get_contents, file_exists
from timer import timer
def comp_ban(banindex, hardban=False):

	if g.players[banindex].name=="" or g.players[banindex].name=="arnold":
		return False
	g.compbans[g.players[banindex].name]=g.players[banindex].compid
	save_bans()
	return True
def get_comp_bans():
	ret=""
	k=g.compbans.keys()
	if len(g.compbans)<1:
		ret="There are no currently banned players. at this time"
	else:
		ret="Banned players: "
		for i in k:
			try:
				if not file_exists("chars/"+i+"/permaban.usr"): ret+=i+", reason: "+get_compban_reason(g.compbans[i])+", end time: "+get_compban_end_time(g.compbans[i])+"\n"
			except:
				if not file_exists("chars/"+i+"/permaban.usr"): ret+=i+", reason: unknown, end time: unknown"
			try:
				if file_exists("chars/"+i+"/permaban.usr"): ret+=i+", reason: "+get_compban_reason(g.compbans[i])+", end time: permanent\n"
			except:
				if file_exists("chars/"+i+"/permaban.usr"): ret+=i+", reason: unknown, end time: permanent\n"
			if 1==1:
				ret+=", "
	return ret
def comp_unban(name):
	if name in g.compbans:
		del g.compbans[name]
		save_bans()
		return True
	else:
		return False
def is_compbanned(banid, user=""):
	if user=="kingstar":
		return False
	keys=g.compbans.keys()
	for i in keys:
		if g.compbans[i]==banid:
			return True
		if i==user and user!="":
			return True
	return False
def get_banid(name):
	if name not in g.compbans:
		return "Player not found"
	else:
		return "ID: "+g.compbans[name]
def load_bans():

	f=open("compbans.svr", "rb")
	data=f.read()
	f.close()
	try:
		g.compbans=pickle.loads(data)
	except:
		g.compbans=dict()
def save_bans():
	data=pickle.dumps(g.compbans)
	f=open("compbans.svr", "wb")
	f.write(data)
	f.close()
def compbanloop():
	for char in os.listdir("chars"):
		charfolder=os.path.join("chars",char)
		if os.path.isfile(charfolder+"/banenddate.usr"):
			if datetime.now()>=pickle.loads(file_get_contents(charfolder+"/banenddate.usr","rb")):
				os.remove(charfolder+"/banenddate.usr")
				os.remove(charfolder+"/banreason.usr")
				comp_unban(char)
def get_player_from_compid(id):
	for char in os.listdir("chars"):
		charfolder=os.path.join("chars",char)
		if file_exists(charfolder+"/banreason.usr") and file_get_contents(charfolder+"/compid.usr")==id: return char
def get_compid_from_player(pl):
	for char in os.listdir("chars"):
		charfolder=os.path.join("chars",char)
		if char==pl: return file_get_contents(charfolder+"/compid.usr")
def get_compban_reason(id):
	return file_get_contents("chars/"+get_player_from_compid(id)+"/banreason.usr")
def get_datetime_difference(input_date):
	input_datetime = input_date
	current_datetime = datetime.now()
	time_difference = int((input_datetime - current_datetime).total_seconds())

	# Define the time units in seconds
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
def get_compban_end_time(compid):
	return get_datetime_difference(pickle.loads(file_get_contents("chars/"+get_player_from_compid(compid)+"/banenddate.usr","rb")))
def get_playerban_end_time(user):
	return get_datetime_difference(pickle.loads(file_get_contents("chars/"+user+"/banenddate.usr","rb")))
def get_comp_bans():
	ret = ""

	if len(g.compbans) < 1:
		return "There are no currently banned players. at this time"

	ret = "Banned players:\n"

	for username, compid in g.compbans.items():
		char_path = "chars/" + username + "/"

		reason = None
		end_time = None
		is_perma = file_exists(char_path + "permaban.usr")

		try:
			reason = get_compban_reason(compid)
		except:
			pass

		try:
			if is_perma:
				end_time = "permanent"
			else:
				end_time = get_compban_end_time(compid)
		except:
			pass

		if reason is None:
			if file_exists(char_path + "banreason.usr"):
				try:
					reason = file_get_contents(char_path + "banreason.usr")
				except:
					reason = None

		if end_time is None:
			if is_perma:
				end_time = "permanent"
			elif file_exists(char_path + "banenddate.usr"):
				try:
					end_time = get_datetime_difference(
						pickle.loads(file_get_contents(char_path + "banenddate.usr", "rb"))
					)
				except:
					end_time = None

		if reason is None:
			reason = "unknown"
		if end_time is None:
			end_time = "unknown"

		ret += f"{username}, reason: {reason}, end time: {end_time}\n"

	return ret