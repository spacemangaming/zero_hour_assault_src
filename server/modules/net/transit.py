import globals as g
import time
from timer import timer
from random import randint as random
from map import get_tile_at
from rotation import get_3d_distance
from file_directories import file_exists
from moving_sound_serverside_handler import spawn_moving_sound, update_moving_sound, destroy_moving_sound
from performance_monitor import get_logger

# Global sound ID allocator for moving engine sounds
_global_sound_counter = 50000

# Performance logging
_perf_log_timer = timer()
_perf_tick_count = 0
_perf_packet_count = 0
_transit_logger = get_logger("transit", "transit.log")

def _bus_perf_log(msg):
	"""Log transit performance info without spamming the server console."""
	_transit_logger.info(msg)

def _bus_perf_tick():
	"""Track tick count and periodically log performance stats."""
	global _perf_tick_count, _perf_packet_count, _perf_log_timer
	_perf_tick_count += 1
	if _perf_log_timer.elapsed >= 30000:
		buses = len(g.transits)
		passengers = sum(len(b.players) for b in g.transits)
		_bus_perf_log(f"Stats (30s): ticks={_perf_tick_count}, packets={_perf_packet_count}, buses={buses}, passengers={passengers}")
		_perf_tick_count = 0
		_perf_packet_count = 0
		_perf_log_timer.restart()

def _count_packet(n=1):
	global _perf_packet_count
	_perf_packet_count += n


class Vehicle:
	def __init__(self, vtype, start_x, start_y, z, mapname, path_id, interior_map, max_health, speed, engine_sound, door_mode):
		global _global_sound_counter
		self.type = vtype
		self.x = start_x
		self.y = start_y
		self.z = z
		self.map = mapname
		self.path_id = path_id
		self.interior_map = interior_map
		self.max_health = max_health
		self.health = max_health
		self.speed = speed  # Movement interval in ms
		self.engine_sound = engine_sound
		self.door_mode = door_mode
		self.spawn_params = (vtype, start_x, start_y, z, mapname, path_id, interior_map, max_health, speed, engine_sound, door_mode)
		
		self.players = []  # List of player names riding
		self.is_stopped = False
		self.stop_timer = timer()
		self.move_timer = timer()
		_global_sound_counter += 1
		self.mid = _global_sound_counter
		self.running = True
		self.facing = 0
		self.speed_timer = timer()
		
		# Engine sound ID for moving 3D sound loop
		self.engine_sound_id = None
		# Throttle timers for heavy operations
		self.sound_update_timer = timer()
		self.passenger_sync_timer = timer()
		
		# Parse the relative interior platforms from the vehicle's dedicated .map blueprint
		self.relative_platforms = []
		self.load_interior_blueprint()
		
		# Spawn engine sound AFTER blueprint load, only if players exist on server
		if self.running and not self.is_stopped and len(self.players) > 0 and self.engine_sound is not None:
			try:
				self.engine_sound_id = spawn_moving_sound(self.engine_sound, self.x, self.y, self.z, self.map, "", 100)
			except Exception as e:
				_bus_perf_log(f"Warning: Could not spawn engine sound on init: {e}")

	def load_interior_blueprint(self):
		if not self.interior_map:
			return
		blueprint_path = "maps/" + self.interior_map + ".map"
		if not file_exists(blueprint_path):
			return
		
		try:
			f = open(blueprint_path, "r", encoding="utf-8")
			mdata = f.read()
			f.close()
			from variable_management import string_split
			for line in mdata.split("\n"):
				line = line.strip()
				if not line or line.startswith("//"):
					continue
				parsed = string_split(line, ":", False)
				if parsed[0] == "platform" and len(parsed) >= 7:
					minx = int(parsed[1])
					maxx = int(parsed[2])
					miny = int(parsed[3])
					maxy = int(parsed[4])
					z = int(parsed[5])
					maxz = z
					try:
						maxz = int(parsed[6])
						tile = parsed[7]
					except:
						tile = parsed[6]
					self.relative_platforms.append((minx, maxx, miny, maxy, z, maxz, tile))
			if self.interior_map == "bus_interior":
				# Reinforce the shell so the bus behaves like a closed vehicle interior.
				self.relative_platforms.extend([
					(0, 0, 0, 15, 0, 5, "wallbuilding"),
					(7, 7, 0, 15, 0, 5, "wallbuilding"),
					(0, 7, 0, 0, 0, 5, "wallbuilding"),
					(0, 7, 15, 15, 0, 5, "wallbuilding"),
					(0, 7, 0, 15, 5, 5, "wallbuilding"),
					(0, 7, 1, 1, 2, 5, "wallbuilding"),
				])
			_bus_perf_log(f"Loaded {len(self.relative_platforms)} interior platforms from {blueprint_path}")
		except Exception as e:
			_bus_perf_log(f"Error loading vehicle interior blueprint {blueprint_path}: {e}")

	def send_initial_platforms(self, player):
		for minx, maxx, miny, maxy, z, maxz, tile in self.relative_platforms:
			send_platform(player, self.x + minx, self.x + maxx, self.y + miny, self.y + maxy, self.z + z, self.z + maxz, tile)
		_count_packet(len(self.relative_platforms))

	def remove_platforms_for(self, player):
		for minx, maxx, miny, maxy, z, maxz, tile in self.relative_platforms:
			remove_platform(player, self.x + minx, self.x + maxx, self.y + miny, self.y + maxy, self.z + z, self.z + maxz, tile)
		_count_packet(len(self.relative_platforms))

	def update_platforms_for_passengers(self, old_x, old_y, old_z):
		"""PERFORMANCE FIX: Only update platforms for passengers riding the bus,
		NOT for every player on the entire map. Non-passengers don't need
		platform data for a moving bus they're not inside."""
		if len(self.players) == 0:
			return
		plat_count = len(self.relative_platforms)
		if plat_count == 0:
			return
		for name in self.players:
			p = g.getpc(name)
			if p is None:
				continue
			for minx, maxx, miny, maxy, z, maxz, tile in self.relative_platforms:
				update_platform(p, old_x + minx, old_x + maxx, old_y + miny, old_y + maxy, old_z + z, old_z + maxz, tile,
								 self.x + minx, self.x + maxx, self.y + miny, self.y + maxy, self.z + z, self.z + maxz, tile)
		_count_packet(len(self.players) * plat_count)

	def add_passenger(self, player):
		if player.name not in self.players:
			self.players.append(player.name)
			player.in_bus = True
			player.bus_instance = self
			player.sitting = False
			
			# Send initial platforms to passenger
			self.send_initial_platforms(player)
			
			# Decouple coordinates into relative local offsets aligned with the bus template
			player.local_x = 3
			player.local_y = 1  # starts at the doorway
			player.local_z = 0
			
			# Sync physical coordinates on the main map
			player.x = self.x + player.local_x
			player.y = self.y + player.local_y
			player.z = self.z + player.local_z
			
			g.n.send_reliable(player.peer_id, "facing " + str(self.facing), 0)
			g.n.send_reliable(player.peer_id, "move " + str(player.x) + " " + str(player.y) + " " + str(player.z), 0)
			g.n.send_reliable(player.peer_id, "play_s misc280.ogg", 0)  # boarding sound
			g.n.send_reliable(player.peer_id, "play_inside_bus", 0)  # play inside bus loop
			g.n.send_reliable(player.peer_id, f"bus_audio {1 if self.is_stopped else 0} {1 if self.doors_open else 0} {1 if self.running and not self.is_stopped else 0} {int(abs(self.speed))}", 0)
			_count_packet(4)
			_bus_perf_log(f"Passenger {player.name} boarded {self.type} at ({self.x},{self.y})")

	def remove_passenger(self, player, fell_off=False):
		if player.name in self.players:
			self.players.remove(player.name)
		player.in_bus = False
		player.bus_instance = None
		player.sitting = False
		
		# Stop inside bus loop on client
		g.n.send_reliable(player.peer_id, "stop_inside_bus", 0)
		
		# Remove platforms for the passenger
		self.remove_platforms_for(player)
		
		g.n.send_reliable(player.peer_id, "motorunspawn", 0)
		_count_packet(2)
		
		if fell_off:
			if not self.is_stopped:
				# Passenger jumped out or fell off while moving
				damage = random(40, 60)
				player.health -= damage
				player.hitby = f"falling off moving {self.type}"
				g.play(get_tile_at(player.x, player.y, player.z, player.map) + "fall", player.x, player.y, player.z, player.map)
				
				if player.health <= 0:
					player.health = 0
					player.die()
				else:
					g.n.send_reliable(player.peer_id, "move " + str(player.x) + " " + str(player.y) + " " + str(player.z), 0)
					_count_packet(1)
			else:
				# Bus is stopped: safe exit, sync position
				g.n.send_reliable(player.peer_id, "move " + str(player.x) + " " + str(player.y) + " " + str(player.z), 0)
				_count_packet(1)
		_bus_perf_log(f"Passenger {player.name} exited {self.type} (fell_off={fell_off})")

	def take_damage(self, amount, attacker):
		self.health -= amount
		# Play muffled metallic impact inside passenger cabin
		for name in list(self.players):
			p = g.getpc(name)
			if p is not None and not p.dead:
				g.n.send_reliable(p.peer_id, "play_s misc263.ogg", 0)  # metal impact sound
				# Blast impact damage to all passengers inside!
				dmg = max(10, int(amount * 0.3))
				p.health -= dmg
				p.hitby = f"blast impact inside damaged {self.type}"
				g.n.send_reliable(p.peer_id, "play_s bus_blast.ogg", 0)  # Play blast sound
				g.n.send_reliable(p.peer_id, f"You suffered {dmg} damage from the blast impact!", 0)
				_count_packet(3)
				
				if p.health <= 0:
					p.health = 0
					p.die()
		
		if self.health <= 0:
			self.health = 0
			self.explode()

	def explode(self):
		self.running = False
		if self.engine_sound_id:
			destroy_moving_sound(self.engine_sound_id)
			self.engine_sound_id = None
		# Play heavy explosion
		g.play("motorexplode", self.x, self.y, self.z, self.map)
		g.n.broadcast(f"distsound motorexplodedist {self.x} {self.y} {self.z} {self.map}", 0)
		
		# Blast passengers back onto the main map, dealing critical damage and throwing them high
		for name in list(self.players):
			p = g.getpc(name)
			if p is not None:
				p.in_bus = False
				p.bus_instance = None
				p.sitting = False
				g.n.send_reliable(p.peer_id, "stop_inside_bus", 0)
				p.health -= 150
				p.hitby = f"exploding {self.type}"
				p.z += 10
				g.n.send_reliable(p.peer_id, "motorunspawn", 0)
				g.n.send_reliable(p.peer_id, f"move {p.x} {p.y} {p.z}", 0)
				_count_packet(3)
				
				if p.health <= 0:
					p.health = 0
					p.die()
		
		# Delete exterior platforms from passengers only (they had them)
		# No need to remove from all players since non-passengers never received them
		self.players.clear()
				
		# Remove from active list
		if self in g.transits:
			g.transits.remove(self)
		_bus_perf_log(f"Vehicle {self.type} exploded at ({self.x},{self.y})")

		# Schedule respawn
		spawn_params = getattr(self, "spawn_params", None)
		if spawn_params:
			from threading import Thread
			import time
			def respawn_func():
				time.sleep(15.0)  # Wait 15 seconds to respawn the bus
				# Create a new bus
				from transit import OpenDoorBus
				v = OpenDoorBus(*spawn_params)
				g.transits.append(v)
				_bus_perf_log(f"Vehicle {spawn_params[0]} respawned at starting coordinates ({spawn_params[1]},{spawn_params[2]})")
			
			Thread(target=respawn_func).start()


class OpenDoorBus(Vehicle):
	def __init__(self, vtype, start_x, start_y, z, mapname, path_id, interior_map, max_health, speed, engine_sound, door_mode):
		super().__init__(vtype, start_x, start_y, z, mapname, path_id, interior_map, max_health, speed, engine_sound, door_mode)
		
		# Load waypoints for navigation
		self.waypoints = []
		self.current_waypoint_idx = 0
		self.load_waypoints()
		
		# Horn warning state
		self.horn_warning_level = 0
		self.horn_timer = None
		self.horn_played = False
		self.doors_open = True
		
		_bus_perf_log(f"Spawned {vtype} at ({start_x},{start_y},{z}) on {mapname}, path={path_id}, speed={speed}ms, waypoints={len(self.waypoints)}")

	def _engine_pitch(self):
		# Convert route speed into a vehicle-like pitch. Faster route timing should not
		# sound like a human voice or a slow footstep loop.
		base = 95 if self.is_stopped else 110
		speed_bonus = max(0, min(55, int((100 - min(self.speed, 100)) * 0.9)))
		return base + speed_bonus

	def load_waypoints(self):
		# We find waypoints matching our path_id
		for w in g.waypoints:
			if w["path_id"] == self.path_id:
				self.waypoints.append(w)
		# Sort waypoints by index
		self.waypoints.sort(key=lambda x: x["index"])

		# Find the closest waypoint to our starting coordinates to align our index
		if len(self.waypoints) > 0:
			best_idx = 0
			best_dist = 999999
			for i, w in enumerate(self.waypoints):
				dist = abs(w["x"] - self.x) + abs(w["y"] - self.y) + abs(w["z"] - self.z)
				if dist < best_dist:
					best_dist = dist
					best_idx = i
			
			if best_dist < 5:  # Spawned close to a waypoint
				self.current_waypoint_idx = (best_idx + 1) % len(self.waypoints)
			else:
				self.current_waypoint_idx = 0

	def set_engine_sound(self, sound_name):
		if self.engine_sound != sound_name or (sound_name is not None and self.engine_sound_id is None):
			self.engine_sound = sound_name
			if self.engine_sound_id:
				try:
					destroy_moving_sound(self.engine_sound_id)
				except:
					pass
				self.engine_sound_id = None
			if self.running and not self.is_stopped and self.engine_sound is not None:
				try:
					self.engine_sound_id = spawn_moving_sound(self.engine_sound, self.x, self.y, self.z, self.map, "", 100)
				except Exception as e:
					_bus_perf_log(f"Warning: Could not spawn engine sound: {e}")

	def tick(self):
		if not self.running:
			return

		if len(self.players) == 0:
			self.is_stopped = True
			self.doors_open = True
			# Play quiet engine hum so players can locate the parked bus by audio
			if self.engine_sound_id is None and self.engine_sound != "bus_engine.ogg":
				try:
					self.engine_sound_id = spawn_moving_sound("bus_engine.ogg", self.x, self.y, self.z, self.map, "", self._engine_pitch())
					self.engine_sound = "bus_engine.ogg"
				except Exception as e:
					_bus_perf_log(f"Warning: Could not spawn idle sound for empty bus: {e}")
			# Throttle position update for idle sound
			if self.engine_sound_id and self.sound_update_timer.elapsed >= 500:
				self.sound_update_timer.restart()
				update_moving_sound(self.engine_sound_id, self.x, self.y, self.z, self._engine_pitch())
			return

		# Check if any passengers are sitting on seats
		any_sitting = False
		for name in self.players:
			p = g.getpc(name)
			if p is not None and getattr(p, "sitting", False):
				any_sitting = True
				break

		if self.is_stopped:
			# Handle stopping for 5 seconds at station
			if self.stop_timer.elapsed >= 5000:
				if any_sitting and not self.doors_open:
					self.is_stopped = False
					self.doors_open = False
					g.play("bus_start", self.x, self.y, self.z, self.map)
					self.horn_warning_level = 0
					self.horn_timer = None
					self.horn_played = False
					# Reset engine sound to drive
					self.set_engine_sound("bus_engine.ogg")
				else:
					# No passenger is sitting yet or doors are open, stay stopped
					pass
			return

		# Idle/start mode: if no passenger is sitting, do not move
		if not any_sitting:
			if not self.doors_open:
				self.doors_open = True
				g.play("bus_stop", self.x, self.y, self.z, self.map)
				g.play("bus_doors_sound_effect", self.x, self.y, self.z, self.map)
			self.set_engine_sound("bus_idle_to_drive_off.ogg")
			# Throttle engine sound loop update
			if self.engine_sound_id and self.sound_update_timer.elapsed >= 200:
				self.sound_update_timer.restart()
				update_moving_sound(self.engine_sound_id, self.x, self.y, self.z, self._engine_pitch())
			return

		# If doors are open, do not move
		if self.doors_open:
			self.set_engine_sound("bus_idle_to_drive_off.ogg")
			# Throttle engine sound loop update
			if self.engine_sound_id and self.sound_update_timer.elapsed >= 200:
				self.sound_update_timer.restart()
				update_moving_sound(self.engine_sound_id, self.x, self.y, self.z, self._engine_pitch())
			return

		# Driving mode: Proceed along waypoints
		self.set_engine_sound("bus_engine.ogg")

		if len(self.waypoints) == 0:
			return

		if self.speed_timer.elapsed >= self.speed:
			self.speed_timer.restart()
			
			target = self.waypoints[self.current_waypoint_idx]
			tx, ty, tz = target["x"], target["y"], target["z"]
			
			# Step towards target waypoint
			dx = tx - self.x
			dy = ty - self.y
			dz = tz - self.z
			
			step_x = 0
			if dx > 0: step_x = 1
			elif dx < 0: step_x = -1
			
			step_y = 0
			if dy > 0: step_y = 1
			elif dy < 0: step_y = -1
			
			step_z = 0
			if dz > 0: step_z = 1
			elif dz < 0: step_z = -1

			# DETECT PLAYER IN FRONT OF THE BUS
			player_in_front = None
			if step_x != 0 or step_y != 0 or step_z != 0:
				for p in g.players:
					if p.map == self.map and not p.in_bus and not p.dead:
						# Check 1 to 3 steps ahead
						for k in range(1, 4):
							cx = self.x + step_x * k
							cy = self.y + step_y * k
							cz = self.z + step_z * k
							if abs(p.x - cx) <= 1 and abs(p.y - cy) <= 1 and abs(p.z - cz) <= 2:
								player_in_front = p
								break
						if player_in_front:
							break

			if player_in_front is not None:
				# Initialize horn timer if not set
				if not hasattr(self, "horn_timer") or self.horn_timer is None:
					self.horn_timer = timer()
					self.horn_played = False
					self.first_detection_time = time.time()
				
				# Wait 1.0 second after first detection before starting to honk
				if time.time() - self.first_detection_time >= 1.0:
					# Play horn sound periodically (every 1.5 seconds)
					if not self.horn_played or self.horn_timer.elapsed >= 1500:
						g.play("bus_horn", self.x, self.y, self.z, self.map)
						self.horn_played = True
						self.horn_timer.restart()
				
				# If warning duration reaches 50 seconds, crush and kill them!
				if time.time() - self.first_detection_time >= 50.0:
					g.play("bus_blast", player_in_front.x, player_in_front.y, player_in_front.z, player_in_front.map)
					player_in_front.x += step_x * 10
					player_in_front.y += step_y * 10
					player_in_front.z += 2
					# Instant death!
					player_in_front.health = 0
					player_in_front.hitby = "being crushed by a city bus"
					
					g.n.send_reliable(player_in_front.peer_id, "You were crushed by the bus!", 0)
					player_in_front.die()
					
					# Reset warning parameters
					self.horn_timer = None
					self.horn_played = False
				
				# Halt the bus: return early so it doesn't move forward
				return
			else:
				# Clear warning state when front is clear
				self.horn_warning_level = 0
				self.horn_timer = None
				self.horn_played = False

			# Warning of arrival: if 10 steps away from a stop waypoint
			dist_to_wp = max(abs(dx), abs(dy))
			if dist_to_wp == 10 and target.get("is_stop", False):
				g.play("bus_is_coming_and_drive_thrue", self.x, self.y, self.z, self.map)

			old_x, old_y, old_z = self.x, self.y, self.z
			
			# Move coordinates
			self.x += step_x
			self.y += step_y
			self.z += step_z
			
			# PERFORMANCE FIX: Throttle sound position updates to every 200ms
			if self.engine_sound_id and self.sound_update_timer.elapsed >= 200:
				self.sound_update_timer.restart()
				update_moving_sound(self.engine_sound_id, self.x, self.y, self.z, self._engine_pitch())
			
			# Update facing direction dynamically based on movement vector
			if step_x == 0 and step_y > 0: self.facing = 0
			elif step_x > 0 and step_y > 0: self.facing = 45
			elif step_x > 0 and step_y == 0: self.facing = 90
			elif step_x > 0 and step_y < 0: self.facing = 135
			elif step_x == 0 and step_y < 0: self.facing = 180
			elif step_x < 0 and step_y < 0: self.facing = 225
			elif step_x < 0 and step_y == 0: self.facing = 270
			elif step_x < 0 and step_y > 0: self.facing = 315
			
			# PERFORMANCE FIX: Only update platforms for passengers, not all players
			self.update_platforms_for_passengers(old_x, old_y, old_z)
			
			# Sync passenger global coordinates
			should_sync_move = self.passenger_sync_timer.elapsed >= 100
			if should_sync_move:
				self.passenger_sync_timer.restart()
			
			for name in list(self.players):
				p = g.getpc(name)
				if p is None or p.map != self.map:
					if name in self.players: self.players.remove(name)
					continue
				
				# Interior limits: x from 1 to 6, y from 1 to 14 (new 8x16 bus)
				# Door gaps at y=0 (front) and y=15 (rear) — stepping out ejects
				if p.local_x < 1 or p.local_x > 6 or p.local_y < 1 or p.local_y > 14:
					self.remove_passenger(p, fell_off=True)
					continue
				
				# Always keep server-side coords up to date (no packets needed)
				p.x = self.x + p.local_x
				p.y = self.y + p.local_y
				p.z = self.z + p.local_z
				
				# Only send move packets at throttled interval
				if should_sync_move:
					g.n.send_reliable(p.peer_id, f"move {p.x} {p.y} {p.z}", 0)
					_count_packet(1)
					if not p.hidden:
						g.send_plus2(p.name, f"update_player2 {p.x} {p.y} {p.z} {p.map} {p.name} {self.facing}", 20, True)
						_count_packet(1)
					g.n.send_unreliable(p.peer_id, f"bus_audio {1 if self.is_stopped else 0} {1 if self.doors_open else 0} {1 if self.running and not self.is_stopped else 0} {int(abs(self.speed))}", 0)
					_count_packet(1)
			
			# Check if waypoint reached
			if self.x == tx and self.y == ty and self.z == tz:
				# Is this waypoint flagged as a stop?
				if target.get("is_stop", False):
					self.is_stopped = True
					self.doors_open = True
					self.stop_timer.restart()
					g.play("bus_stop", self.x, self.y, self.z, self.map)
					g.play("bus_doors_sound_effect", self.x, self.y, self.z, self.map)
					if self.engine_sound_id:
						destroy_moving_sound(self.engine_sound_id)
						self.engine_sound_id = None
					
					# Announce station arrival to passengers inside
					for name in self.players:
						p = g.getpc(name)
						if p is not None:
							g.n.send_reliable(p.peer_id, "play_s misc263.ogg", 0)  # digital chime
							_count_packet(1)
					_bus_perf_log(f"Bus stopped at waypoint ({tx},{ty},{tz}), passengers={len(self.players)}")
				
				# Advance to next waypoint index
				self.current_waypoint_idx += 1
				if self.current_waypoint_idx >= len(self.waypoints):
					# Loop track path (rewind back to start node)
					self.current_waypoint_idx = 0


# Throttled bus loop timer — prevents busloop from running on every gameloops() call
_busloop_timer = timer()

def busloop():
	# PERFORMANCE FIX: Only run bus ticks every 20ms instead of every gameloops() call
	global _busloop_timer
	if _busloop_timer.elapsed < 20:
		return
	_busloop_timer.restart()
	
	_bus_perf_tick()
	for bus in list(g.transits):
		try:
			bus.tick()
		except Exception as e:
			import traceback
			_bus_perf_log(f"Error in bus tick: {e}")
			traceback.print_exc()

g.busloop = busloop

# Network wrappers
def send_platform(p, minx, maxx, miny, maxy, minz, maxz, tile):
	g.n.send_reliable(p.peer_id, "addplatform " + str(round(minx)) + " " + str(round(maxx)) + " " + str(round(miny)) + " " + str(round(maxy)) + " " + str(round(minz)) + " " + str(round(maxz)) + " " + tile, 4)

def update_platform(p, minx, maxx, miny, maxy, minz, maxz, tile, minx2, maxx2, miny2, maxy2, minz2, maxz2, tile2):
	g.n.send_reliable(p.peer_id, "updateplatform " + str(round(minx)) + " " + str(round(maxx)) + " " + str(round(miny)) + " " + str(round(maxy)) + " " + str(round(minz)) + " " + str(round(maxz)) + " " + tile + " " + str(round(minx2)) + " " + str(round(maxx2)) + " " + str(round(miny2)) + " " + str(round(maxy2)) + " " + str(round(minz2)) + " " + str(round(maxz2)) + " " + tile2, 4)

def remove_platform(p, minx, maxx, miny, maxy, minz, maxz, tile):
	g.n.send_reliable(p.peer_id, "removeplatform " + str(round(minx)) + " " + str(round(maxx)) + " " + str(round(miny)) + " " + str(round(maxy)) + " " + str(round(minz)) + " " + str(round(maxz)) + " " + tile, 4)

