import globals as g
from random import randint as random
from variable_management import string_contains
from rotation import get_3d_distance
from file_directories import file_exists
from timer import timer
class flag:
	def __init__(self,x,y,z,map,team):
		self.x=x
		self.beeptimer=timer()
		self.y=y
		self.z=z
		self.map=map
		self.filechecktimer=timer()
		self.team=team
def flagloop():
	for i in range(len(g.flags)):
		if g.flags[i].filechecktimer.elapsed>1000:
			g.flags[i].filechecktimer.restart()
			if not file_exists("maps/"+g.flags[i].map+".map"):
				g.flags.remove(g.flags[i])
				return
		if g.flags[i].beeptimer.elapsed>=2000:
			g.flags[i].beeptimer.restart()
			g.play("flag4",g.flags[i].x,g.flags[i].y,g.flags[i].z,g.flags[i].map)
def spawn_flag(x,y,z,map,team):
	if "flag" not in map: return
	yarrak=flag(x,y,z,map,team)
	g.flags.append(yarrak)