import globals as g
from timer import timer
def pathfind(orig_x, orig_y, target_x, target_y, map,npc_loop=""):
	return None
	g.pathfinding=True
	orig_x=round(orig_x)
	orig_y=round(orig_y)
	target_x=round(target_x)
	target_y=round(target_y)
	if target_x<0 or target_y<0: g.pathfinding=False; return None
	if orig_x==target_x and orig_y==target_y: g.pathfinding=False;return None
	tile=g.get_tile_at(orig_x, orig_y, 0, map)
	tile2=g.get_tile_at(target_x, target_y, 0, map)
	if tile.startswith("wall"): g.pathfinding=False; return None
	if tile2.startswith("wall"): g.pathfinding=False; return None
	if tile!="hardwood" and tile2=="hardwood": g.pathfinding=False; return None
	if tile=="hardwood" and tile2!="hardwood": g.pathfinding=False; return None
	def heuristic(a, b):
		return abs(b[0] - a[0]) + abs(b[1] - a[1])

	def get_neighbors(curr_node):
		cx, cy = curr_node
		neighbors = [(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)]
		valid_neighbors = []
		for neighbor in neighbors:
			g.netloop(); g.gameloops(True,False) 
			if not g.get_tile_at(neighbor[0], neighbor[1], 0, map).startswith("wall"):
				valid_neighbors.append(neighbor)
		return valid_neighbors

	open_set = {(orig_x, orig_y)}
	came_from = {}
	g_score = {node: float('inf') for node in open_set}
	g_score[(orig_x, orig_y)] = 0
	f_score = {node: float('inf') for node in open_set}
	f_score[(orig_x, orig_y)] = heuristic((orig_x, orig_y), (target_x, target_y))

	while open_set:
		g.netloop(); g.gameloops(True,False) 
		current = min(open_set, key=lambda node: f_score[node])

		if current == (target_x, target_y):
			path = []
			while current in came_from:
				g.netloop(); g.gameloops(True,False) 
				path.append(current)
				current = came_from[current]
			path.append((orig_x, orig_y))
			g.pathfinding=False; return path

		open_set.remove(current)
		for neighbor in get_neighbors(current):
			g.netloop(); g.gameloops(True,False) 
			tentative_g_score = g_score[current] + 1  # Assuming each step cost is 1
			if tentative_g_score < g_score.get(neighbor, float('inf')):
				came_from[neighbor] = current
				g_score[neighbor] = tentative_g_score
				f_score[neighbor] = tentative_g_score + heuristic(neighbor, (target_x, target_y))
				if neighbor not in open_set:
					open_set.add(neighbor)
	g.pathfinding=False
	return None