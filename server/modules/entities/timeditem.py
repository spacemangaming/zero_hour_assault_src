from timer import timer
import globals as g
from file_directories import file_put_contents, directory_exists, file_get_contents
import pickle
class timeditem:
	def __init__(self,owner,itemname,duration):
		self.owner=owner
		self.itemname=itemname
		self.duration=duration
		self.timer=timer()
def timeditemloop():
	for i in g.timeditems:
		if i.timer.elapsed>=i.duration:
			index=g.get_player_index_from(i.owner)
			if index>-1: g.players[index].give(i.itemname,-1)
			else: offlinegive(i.owner,i.itemname,-1)
			g.timeditems.remove(i)
			return
def new_timeditem(owner,itemname,duration):
	g.timeditems.append(timeditem(owner,itemname,duration))
def offlinegive(pl, item, amount):
	if 1:
		i, p, q = item, pl, int(amount)
		if directory_exists("chars/"+p)==False:
			return
		inv = pickle.loads(file_get_contents("chars/" + p + "/inventory.usr","rb"))
		t = inv.get(i, 0)
		if t > 0:
			fv = q + t
		else:
			fv = q
		if i in inv:
			del inv[i]
		if fv>0:
			inv[i] = fv
		file_put_contents("chars/" + p + "/inventory.usr", pickle.dumps(inv), "wb")
