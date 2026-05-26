import math
import os
import time

from constants import DIRECTORY_TEMP

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FMOD_DLL_DIR = os.path.join(ROOT_DIR, "third_party", "fmod")

import sys

os.environ["PYFMODEX_DLL_PATH"] = os.path.join(FMOD_DLL_DIR, "fmod.dll")
os.environ["PYFMODEX_STUDIO_DLL_PATH"] = os.path.join(FMOD_DLL_DIR, "fmodstudio.dll")
if sys.platform == "win32" and hasattr(os, "add_dll_directory"):
	try:
		os.add_dll_directory(FMOD_DLL_DIR)
	except Exception:
		pass

import fmod_audio
import pyfmodex
from pack_file import *

FMOD_ACTIVE = False

if fmod_audio.FMOD_AVAILABLE and fmod_audio.init_fmod():
	FMOD_ACTIVE = True
else:
	raise RuntimeError("FMOD is required but failed to initialize. Check third_party/fmod DLLs and pyfmodex.")

pack = pack_file()
try:
	pack.open("sounds.dat")
except Exception as e:
	print(f"Warning: Could not open sounds.dat: {e}")



def get_raycast_occlusion(listener_x, listener_y, listener_z, source_x, source_y, source_z):
	try:
		from map import get_tile_at
	except Exception:
		return 0.0

	dx = source_x - listener_x
	dy = source_y - listener_y
	dz = source_z - listener_z
	distance = math.sqrt(dx*dx + dy*dy + dz*dz)

	# If listener and source are extremely close, no occlusion is possible
	if distance < 1.5:
		return 0.0

	steps = int(distance)
	wall_count = 0

	for i in range(1, steps):
		t = i / distance
		check_x = listener_x + dx * t
		check_y = listener_y + dy * t
		check_z = listener_z + dz * t

		# Probe the geometry at this step
		tile = get_tile_at(round(check_x), round(check_y), round(check_z))
		if tile and ("wall" in tile or tile.startswith("wall")):
			wall_count += 1
			# Early out if heavily occluded
			if wall_count >= 3:
				break

	if wall_count > 0:
		# Muffle high frequencies and volume based on wall thickness
		return min(0.85, 0.45 + 0.15 * wall_count)
	return 0.0



def _to_linear_volume(db_value):
	try:
		volume = 10 ** (float(db_value) / 20)
	except Exception:
		return 1.0
	if volume < 0.0:
		return 0.0
	if volume > 1.0:
		return 1.0
	return volume


def _to_db_volume(linear_value):
	try:
		linear_value = float(linear_value)
	except Exception:
		return 0
	if linear_value <= 0.0:
		return -100
	return round(math.log10(linear_value) * 20)


def _vector_from_angle(deg):
	rad = math.radians(deg)
	return [math.sin(rad), math.cos(rad), 0.0]


class FMODListener(object):
	def __init__(self):
		self._position = [0.0, 0.0, 0.0]
		self._gain = 1.0
		self._hrtf = 2
		self._facing = 0.0

	def _set_gain(self, value):
		self._gain = value
		try:
			fmod_audio.system.master_channel_group.volume = value
		except Exception:
			pass

	def _get_gain(self):
		return self._gain

	@property
	def hrtf(self):
		return self._hrtf

	@hrtf.setter
	def hrtf(self, value):
		self._hrtf = value

	@property
	def position(self):
		return self._position

	@position.setter
	def position(self, pos):
		self._position = [float(pos[0]), float(pos[1]), float(pos[2])]
		self.apply()

	def set_facing(self, facing):
		self._facing = float(facing)
		self.apply()

	def apply(self):
		try:
			fmod_audio.system.set_3d_listener_attributes(
				0,
				pos=self._position,
				forward=_vector_from_angle(self._facing),
				up=[0.0, 0.0, 1.0],
			)
		except Exception:
			pass

	def delete(self):
		pass


class FMODPlayer(object):
	def __init__(self, parent_sound):
		self._parent = parent_sound
		self.alhrtf = True
		self.rolloff = 1.0
		self.max_distance = 50.0
		self.stationary = False

	def playing(self):
		return self._parent.playing()

	def playing2(self):
		return self._parent.playing()

	def play(self):
		return self._parent.play()

	def stop(self):
		return self._parent.stop()

	def rewind(self):
		try:
			if self._parent._fmod_sound and self._parent._fmod_sound.channel:
				self._parent._fmod_sound.channel.set_position(0, pyfmodex.enums.TIMEUNIT.MS)
		except Exception:
			pass

	def pause(self):
		return self._parent.pause()

	def delete(self):
		pass

	def remove(self):
		pass

	def add_effect(self, slot, filtr=None):
		return False

	def del_effect(self, slot):
		return False

	def seek(self, offset):
		try:
			length = self._parent._fmod_sound.sound.get_length(pyfmodex.enums.TIMEUNIT.MS)
			self._parent._fmod_sound.channel.set_position(int(length * offset), pyfmodex.enums.TIMEUNIT.MS)
		except Exception:
			pass

	@property
	def source(self):
		return 0

	@property
	def volume(self):
		return _to_linear_volume(self._parent.volume)

	@volume.setter
	def volume(self, value):
		self._parent.volume = _to_db_volume(value)

	@property
	def pitch(self):
		return self._parent.pitch / 100

	@pitch.setter
	def pitch(self, value):
		self._parent.pitch = float(value) * 100

	@property
	def position(self):
		return tuple(self._parent._position)

	@position.setter
	def position(self, pos):
		self._parent.set_3dposition(pos[0], pos[1], pos[2])


listener = FMODListener()


def get_available_output_devices():
	return ["FMOD Default Device"]


def is_short_movement_or_combat_sound(filename):
	if not filename:
		return False
	if isinstance(filename, bytes):
		filename = filename.decode("utf-8", errors="ignore")
	fn = filename.lower()
	if "music" in fn or "ambient" in fn or "stream" in fn or "song" in fn:
		return False
	
	# Movement keywords
	movement_keywords = ["step", "foot", "walk", "run", "jump", "land", "tile", "wood", "grass", "gravel", "concrete", "ceramic", "dirt", "stone", "floor", "sand", "snow", "water"]
	# Combat keywords
	combat_keywords = ["shoot", "fire", "shot", "gun", "ak47", "m4a1", "awp", "pistol", "glock", "usp", "deagle", "shotgun", "grenade", "explosion", "rpg", "knife"]
	
	for kw in movement_keywords + combat_keywords:
		if kw in fn:
			return True
	return False


class sound(object):
	cache = {}

	def __init__(self):
		self.memory = False
		self.paused = False
		self.loading = False
		self._fmod_sound = None
		self.internal_filename = None
		self.slot = None
		self.effect = None
		self.downmix = False
		self.usingpack = False
		self.filename = ""
		self._volume = 0.0
		self._pitch = 100.0
		self._pan = 0.0
		self._position = [0.0, 0.0, 0.0]
		self._looping = False
		self._delete_on_close = None
		self._randomized_pitch_offset = None
		self.player = FMODPlayer(self)
		self.source = self

	def load(self, filename="", downmix=False, load_from_memory=False):
		self.loading = True
		self.internal_filename = filename
		self.downmix = downmix
		if self._fmod_sound:
			self.close()
		self._fmod_sound = fmod_audio.fmod_sound()
		is_stream = False
		if isinstance(filename, str):
			fn_lower = filename.lower()
			is_stream = "music" in fn_lower or "ambient" in fn_lower or "stream" in fn_lower or "song" in fn_lower
		success = self._fmod_sound.load(filename, is_stream=is_stream)
		self.loading = False
		return success

	def fade(self, close=True):
		while self.volume >= -50:
			self.volume -= 4
			time.sleep(0.05)
		if close:
			self.close()
		else:
			self.pause()

	def fade2(self, close=True):
		while self.volume >= -50:
			self.volume -= 1
			time.sleep(0.5)
		if close:
			self.close()
		else:
			self.pause()
		import globals as g
		g.rain = False

	def play(self):
		if not self.is_active:
			return False
		self.paused = False
		self._looping = False
		return self._start_channel(pyfmodex.flags.MODE.LOOP_OFF)

	def play_wait(self):
		if not self.play():
			return False
		while self.playing():
			import events
			events.process_events()
		return True

	def play_looped(self):
		if not self.is_active:
			return False
		self.paused = False
		self._looping = True
		try:
			self._fmod_sound.sound.loop_count = -1
		except Exception:
			pass
		return self._start_channel(pyfmodex.flags.MODE.LOOP_NORMAL)

	def _start_channel(self, loop_mode):
		try:
			mode = loop_mode
			mode |= pyfmodex.flags.MODE.TWOD if self.player.stationary else pyfmodex.flags.MODE.THREED
			self._fmod_sound.channel = self._fmod_sound.sound.play(paused=True)
			self._fmod_sound.channel.mode = mode
			
			# Generate micro-pitch randomizer offset for one-shot movement/combat sounds
			if not self._looping and is_short_movement_or_combat_sound(self.internal_filename):
				import random
				self._randomized_pitch_offset = random.uniform(0.96, 1.04)
			else:
				self._randomized_pitch_offset = None
				
			self._apply_properties()
			self._fmod_sound.channel.paused = False
			return True
		except Exception as e:
			print(f"FMOD play failed: {e}")
			return False

	def stop(self):
		if self._fmod_sound:
			return self._fmod_sound.stop()
		return False

	def get_source_object(self):
		return self.player

	def pause(self):
		self.paused = True
		try:
			self._fmod_sound.channel.paused = True
		except Exception:
			pass

	def resume(self):
		self.paused = False
		try:
			self._fmod_sound.channel.paused = False
			return True
		except Exception:
			return False

	def playing(self):
		try:
			return self._fmod_sound.channel.is_playing
		except Exception:
			return False

	@property
	def volume(self):
		try:
			self._volume = _to_db_volume(self._fmod_sound.channel.volume)
		except Exception:
			pass
		return self._volume

	@volume.setter
	def volume(self, value):
		self._volume = value
		self._apply_properties()

	@property
	def pan(self):
		return self._pan

	@pan.setter
	def pan(self, value):
		self._pan = max(-100.0, min(100.0, float(value)))
		self._apply_properties()

	@property
	def pitch(self):
		try:
			self._pitch = self._fmod_sound.channel.pitch * 100
		except Exception:
			pass
		return self._pitch

	@pitch.setter
	def pitch(self, value):
		self._pitch = value
		self._apply_properties()

	@property
	def direct_occlusion(self):
		if self._fmod_sound and self._fmod_sound.channel:
			try:
				return self._fmod_sound.channel.direct_occlusion
			except Exception:
				pass
		return 0.0

	@direct_occlusion.setter
	def direct_occlusion(self, value):
		if self._fmod_sound and self._fmod_sound.channel:
			try:
				self._fmod_sound.channel.direct_occlusion = float(value)
			except Exception:
				pass

	@property
	def reverb_occlusion(self):
		if self._fmod_sound and self._fmod_sound.channel:
			try:
				return self._fmod_sound.channel.reverb_occlusion
			except Exception:
				pass
		return 0.0

	@reverb_occlusion.setter
	def reverb_occlusion(self, value):
		if self._fmod_sound and self._fmod_sound.channel:
			try:
				self._fmod_sound.channel.reverb_occlusion = float(value)
			except Exception:
				pass

	@property
	def position(self):
		try:
			return self._fmod_sound.channel.position
		except Exception:
			return 0

	@position.setter
	def position(self, value):
		try:
			if self._fmod_sound and self._fmod_sound.channel and self._fmod_sound.sound:
				length = self._fmod_sound.sound.get_length(pyfmodex.enums.TIMEUNIT.MS)
				self._fmod_sound.channel.set_position(int(length * float(value)), pyfmodex.enums.TIMEUNIT.MS)
		except Exception:
			pass

	def close(self, delete_effect=True):
		self.loading = True
		if self._fmod_sound:
			self._fmod_sound.close()
			self._fmod_sound = None
		if self._delete_on_close:
			try:
				os.remove(self._delete_on_close)
			except Exception:
				pass
			self._delete_on_close = None
		self.loading = False
		return True

	@property
	def is_active(self):
		return self._fmod_sound is not None and self._fmod_sound.sound is not None

	def set_3dposition(self, sound_x, sound_y, sound_z):
		self._position = [float(sound_x), float(sound_y), float(sound_z)]
		self._apply_properties()
		return True

	def _apply_properties(self):
		if not self._fmod_sound or not self._fmod_sound.channel:
			return
		try:
			self._fmod_sound.channel.volume = _to_linear_volume(self._volume)
			
			# Check and apply randomized micro-pitch offset
			pitch_val = self._pitch
			if getattr(self, "_randomized_pitch_offset", None) is not None:
				pitch_val = self._pitch * self._randomized_pitch_offset
			self._fmod_sound.channel.pitch = float(pitch_val) / 100
			
			if self.player.stationary:
				self._fmod_sound.channel.pan = float(self._pan) / 100.0
			else:
				self._fmod_sound.channel.position = self._position
				min_dist = 1.0 / self.player.rolloff if self.player.rolloff > 0 else 1.0
				self._fmod_sound.channel.min_distance = min_dist
				self._fmod_sound.channel.max_distance = float(self.player.max_distance or 10000.0)
		except Exception:
			pass
