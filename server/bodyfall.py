from timer import timer
import globals as g
from map import get_tile_at
class bodyfall:
	def __init__(self,bx,by,bz,bmap,bodytime=3000):
		self.btime=3000
		self.x=bx
		self.y=by
		self.z=bz
		self.map=bmap
		self.btimer=timer()

	
		self.x=bx
		self.y=by
		self.z=bz
		self.map=bmap
		self.btime=bodytime
		
	
def bodyfallloop():
	for i in range(len(g.bodyfalls)):
	
		if (g.bodyfalls[i].btimer.elapsed>=g.bodyfalls[i].btime):
		
			g.play(get_tile_at(g.bodyfalls[i].x,g.bodyfalls[i].y,g.bodyfalls[i].z,g.bodyfalls[i].map)+"fall", g.bodyfalls[i].x, g.bodyfalls[i].y, g.bodyfalls[i].z, g.bodyfalls[i].map)

			g.bodyfalls.remove(g.bodyfalls[i])
			return
			
		
	
def spawn_bodyfall(x,y,z,map,time=30):
	b1=bodyfall(x,y,z,map, time)
	g.bodyfalls.append(b1)
	
