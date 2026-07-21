import globals as g
from file_directories import find_directories, file_exists, file_get_contents
class compid_handler:
	compid=""
	playername=""
	def __init__(self, cid, pn):
		self.compid=cid
		self.playername=pn
def add_compid(compid, name):
	ch1=compid_handler(compid, name)
	g.comphandles.append(ch1)
def compid_handlercheck(c):
	for i in range(len(g.comphandles)):
		if g.comphandles[i].compid==c:
			return True
	return False
def get_compid_handler_index(c):
	for i in range(len(g.comphandles)):
		if g.comphandles[i].compid==c:
			return i
	return -1
def load_compids():
	import os
	from concurrent.futures import ThreadPoolExecutor

	if not os.path.exists("chars"):
		return

	char_names = [d for d in find_directories("chars") if os.path.isdir(os.path.join("chars", d))]

	def process_char(char_name):
		path = os.path.join("chars", char_name, "compid.usr")
		if os.path.exists(path):
			try:
				with open(path, "r", encoding="utf-8") as f:
					compid = f.read().strip()
				if compid:
					return compid, char_name
			except Exception:
				pass
		return None

	with ThreadPoolExecutor(max_workers=32) as executor:
		results = executor.map(process_char, char_names)

	for res in results:
		if res:
			compid, char_name = res
			add_compid(compid, char_name)
