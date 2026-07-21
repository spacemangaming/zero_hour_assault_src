import globals as g
import pickle
import os
from datetime import datetime
from file_directories import file_get_contents, file_exists
from timer import timer
import db as _db


def comp_ban(banindex, hardban=False):
	if g.players[banindex].name == "" or g.players[banindex].name == "arnold":
		return False
	g.compbans[g.players[banindex].name] = g.players[banindex].compid
	save_bans()
	return True


def comp_unban(name):
	if name in g.compbans:
		del g.compbans[name]
		save_bans()
		# Clear ban fields in DB
		_db.charwrite(name, "banreason", "")
		_db.chardelete(name, "banenddate")
		_db.charwrite(name, "permaban", 0)
		return True
	return False


def is_compbanned(banid, user=""):
	if user == "kingstar":
		return False
	for name, cid in g.compbans.items():
		if cid == banid:
			return True
		if name == user and user != "":
			return True
	return False


def get_banid(name):
	if name not in g.compbans:
		return "Player not found"
	return "ID: " + g.compbans[name]


def load_bans():
	try:
		data = _db.sv_read("compbans.svr")
		g.compbans = pickle.loads(data) if data else {}
	except Exception:
		g.compbans = {}


def save_bans():
	_db.sv_write("compbans.svr", pickle.dumps(g.compbans))


def compbanloop():
	"""Expire timed bans whose banenddate has passed."""
	for name in list(g.compbans.keys()):
		if not _db.player_exists(name):
			continue
		banenddate_raw = _db.charreadb(name, "banenddate")
		if not banenddate_raw:
			continue
		try:
			end_dt = pickle.loads(banenddate_raw)
			if datetime.now() >= end_dt:
				_db.charwrite(name, "banreason", "")
				_db.chardelete(name, "banenddate")
				_db.charwrite(name, "permaban", 0)
				comp_unban(name)
		except Exception:
			pass


def get_player_from_compid(compid):
	"""Return the username whose stored compid matches, or None."""
	# First check online players (fast path)
	for p in g.players:
		if p is not None and getattr(p, "compid", None) == compid:
			return p.name
	# Fall back to DB
	try:
		from db import _fetchone
		row = _fetchone("SELECT name FROM players WHERE compid=?", (compid,))
		if row:
			return row[0]
	except Exception:
		pass
	return None


def get_compid_from_player(name):
	return _db.charread(name, "compid", "")


def get_compban_reason(compid):
	owner = get_player_from_compid(compid)
	if owner:
		return _db.charread(owner, "banreason", "unknown")
	return "unknown"


def get_datetime_difference(input_date):
	current_datetime = datetime.now()
	time_difference = int((input_date - current_datetime).total_seconds())

	time_units = {
		'millennium': 31536000000,
		'century':    3153600000,
		'decade':     315360000,
		'year':       31536000,
		'month':      2592000,
		'day':        86400,
		'hour':       3600,
		'minute':     60,
		'second':     1,
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
	owner = get_player_from_compid(compid)
	if not owner:
		return "unknown"
	return get_playerban_end_time(owner)


def get_playerban_end_time(user):
	raw = _db.charreadb(user, "banenddate")
	if not raw:
		return "unknown"
	try:
		return get_datetime_difference(pickle.loads(raw))
	except Exception:
		return "unknown"


def get_comp_bans():
	if not g.compbans:
		return "There are no currently banned players at this time"

	ret = "Banned players:\n"
	for username, compid in g.compbans.items():
		is_perma = _db.charread(username, "permaban", "0") == "1"
		reason = _db.charread(username, "banreason", "unknown") or "unknown"
		if is_perma:
			end_time = "permanent"
		else:
			end_time = get_playerban_end_time(username)
		ret += f"{username}, reason: {reason}, end time: {end_time}\n"
	return ret


def is_tempmail(mail: str) -> bool:
	"""Return True if the email domain is a known disposable/temp mail provider."""
	return mail.lower().split("@")[-1] in _db._get_tempmail_domains() if hasattr(_db, "_get_tempmail_domains") else False
