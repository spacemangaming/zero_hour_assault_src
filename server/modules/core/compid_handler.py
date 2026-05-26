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
	chars=find_directories("chars")
	for i in range(len(chars)):
		if file_exists("chars/"+chars[i]+"/compid.usr")==False:
			continue
		compid=file_get_contents("chars/"+chars[i]+"/compid.usr")
		add_compid(compid, chars[i])
