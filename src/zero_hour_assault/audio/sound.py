import math
import os
import sys
import time

from constants import DIRECTORY_TEMP

# Resolve absolute path to the project root directory
if getattr(sys, "frozen", False):
	ROOT_DIR = os.path.dirname(sys.executable)
	FMOD_DLL_DIR = ROOT_DIR
else:
	ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
	FMOD_DLL_DIR = os.path.join(ROOT_DIR, "third_party", "fmod")

SOUNDS_DIR = os.path.join(ROOT_DIR, "sounds")

# Pack File Loader initialization (for FMOD backend and general use)
try:
	from pack_file import pack_file
	pack = pack_file()
	try:
		pack.open("sounds.dat")
	except Exception:
		pass
except Exception:
	pack = None

# Try to initialize FMOD
FMOD_ACTIVE = False
try:
	os.environ["PYFMODEX_DLL_PATH"] = os.path.join(FMOD_DLL_DIR, "fmod.dll")
	os.environ["PYFMODEX_STUDIO_DLL_PATH"] = os.path.join(FMOD_DLL_DIR, "fmodstudio.dll")
	if sys.platform == "win32" and hasattr(os, "add_dll_directory"):
		try:
			if os.path.isdir(FMOD_DLL_DIR):
				os.add_dll_directory(FMOD_DLL_DIR)
		except Exception:
			pass
	import fmod_audio
	import pyfmodex
	if fmod_audio.FMOD_AVAILABLE and fmod_audio.init_fmod():
		FMOD_ACTIVE = True
except Exception as fmod_err:
	print(f"[sound] FMOD initialization failed, falling back to OpenAL: {fmod_err}")

# Try to initialize OpenAL as fallback
_oal_available = False
if not FMOD_ACTIVE:
	try:
		import oal
		oal.initialize_openal_bindings()
		_oal_available = True
	except Exception as _oal_err:
		print(f"[sound] OpenAL unavailable: {_oal_err}")
		_oal_available = False


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _to_linear_volume(db_value):
	try:
		v = 10 ** (float(db_value) / 20)
	except Exception:
		return 1.0
	return max(0.0, min(1.0, v))


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


def _resolve_sound_path(filename):
	if isinstance(filename, bytes):
		filename = filename.decode("utf-8", errors="ignore")
	if os.path.isabs(filename):
		return filename
	return os.path.join(SOUNDS_DIR, filename)


def get_raycast_occlusion(listener_x, listener_y, listener_z, source_x, source_y, source_z):
	try:
		from map import get_tile_at
	except Exception:
		return 0.0

	dx = source_x - listener_x
	dy = source_y - listener_y
	dz = source_z - listener_z
	distance = math.sqrt(dx*dx + dy*dy + dz*dz)

	if distance < 1.5:
		return 0.0

	steps = int(distance)
	wall_count = 0

	for i in range(1, steps):
		t = i / distance
		check_x = listener_x + dx * t
		check_y = listener_y + dy * t
		check_z = listener_z + dz * t

		tile = get_tile_at(round(check_x), round(check_y), round(check_z))
		if tile and ("wall" in tile or tile.startswith("wall")):
			wall_count += 1
			if wall_count >= 3:
				break

	if wall_count > 0:
		return min(0.85, 0.45 + 0.15 * wall_count)
	return 0.0


def is_short_movement_or_combat_sound(filename):
	if not filename:
		return False
	if isinstance(filename, bytes):
		filename = filename.decode("utf-8", errors="ignore")
	fn = filename.lower()
	if "music" in fn or "ambient" in fn or "stream" in fn or "song" in fn:
		return False
	
	movement_keywords = ["step", "foot", "walk", "run", "jump", "land", "tile", "wood", "grass", "gravel", "concrete", "ceramic", "dirt", "stone", "floor", "sand", "snow", "water"]
	combat_keywords = ["shoot", "fire", "shot", "gun", "ak47", "m4a1", "awp", "pistol", "glock", "usp", "deagle", "shotgun", "grenade", "explosion", "rpg", "knife"]
	
	for kw in movement_keywords + combat_keywords:
		if kw in fn:
			return True
	return False


# ---------------------------------------------------------------------------
# FMOD Audio Implementation
# ---------------------------------------------------------------------------

class FMODListener(object):
	def __init__(self):
		self._position = [0.0, 0.0, 0.0]
		self._gain = 1.0
		self._hrtf = 2
		self._facing = 0.0

	def _set_gain(self, value):
		self._gain = value
		try:
			import fmod_audio
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
			import fmod_audio
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
				import pyfmodex
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
			import pyfmodex
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


class FMODSound(object):
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
		import fmod_audio
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
		import pyfmodex
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
		import pyfmodex
		return self._start_channel(pyfmodex.flags.MODE.LOOP_NORMAL)

	def _start_channel(self, loop_mode):
		try:
			import pyfmodex
			mode = loop_mode
			mode |= pyfmodex.flags.MODE.TWOD if self.player.stationary else pyfmodex.flags.MODE.THREED
			self._fmod_sound.channel = self._fmod_sound.sound.play(paused=True)
			self._fmod_sound.channel.mode = mode
			
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
				import pyfmodex
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


# ---------------------------------------------------------------------------
# OpenAL Audio Implementation
# ---------------------------------------------------------------------------

class _OALListener(object):
	def __init__(self):
		self._position = [0.0, 0.0, 0.0]
		self._gain = 1.0
		self._hrtf = 2
		self._facing = 0.0
		self._oal = None
		if _oal_available:
			try:
				self._oal = oal.Listener()
			except Exception as e:
				print(f"[sound] OAL Listener init failed: {e}")

	def _set_gain(self, value):
		self._gain = value
		if self._oal:
			try:
				self._oal._set_gain(value)
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
		if self._oal:
			try:
				self._oal.hrtf = value
			except Exception:
				pass

	@property
	def position(self):
		return self._position

	@position.setter
	def position(self, pos):
		self._position = [float(pos[0]), float(pos[1]), float(pos[2])]
		self._apply()

	def set_facing(self, facing):
		self._facing = float(facing)
		self._apply()

	def _apply(self):
		if self._oal:
			try:
				self._oal.position = self._position
				self._oal.at_orientation = _vector_from_angle(self._facing)
			except Exception:
				pass

	def delete(self):
		if self._oal:
			try:
				self._oal.delete()
			except Exception:
				pass


class OpenALSound(object):
	cache = {}

	def __init__(self):
		self.memory = False
		self.paused = False
		self.loading = False
		self._loaded_sound = None
		self.internal_filename = None
		self.slot = None
		self.effect = None
		self.downmix = False
		self.usingpack = False
		self.filename = ""
		self._volume = 0.0
		self._pitch = 100.0
		self._pan = 0.0
		self._looping = False
		self._delete_on_close = None
		if _oal_available:
			try:
				self.player = oal.Player()
			except Exception:
				self.player = None
		else:
			self.player = None
		self.source = self.player

	def load(self, filename="", downmix=False, load_from_memory=False):
		self.loading = True
		self.internal_filename = filename
		self.downmix = downmix
		if self._loaded_sound is not None:
			self.close()
		if not _oal_available or self.player is None:
			self.loading = False
			return False
		path = _resolve_sound_path(filename)
		if not os.path.exists(path):
			self.loading = False
			return False
		try:
			ls = oal.LoadSound.from_file(path, downmix)
			while len(self.player.queue) > 0:
				self.player.remove()
			self.player.add(ls)
			self._loaded_sound = ls
			self.loading = False
			return True
		except Exception as e:
			self.loading = False
			return False

	def play(self):
		if not self.is_active:
			return False
		self.paused = False
		self._looping = False
		self.player.loop = False
		try:
			self.player.play()
			return True
		except Exception:
			return False

	def play_wait(self):
		if not self.play():
			return False
		while self.playing():
			try:
				import events
				events.process_events()
			except Exception:
				time.sleep(0.01)
		return True

	def play_looped(self):
		if not self.is_active:
			return False
		self.paused = False
		self._looping = True
		self.player.loop = True
		try:
			self.player.play()
			return True
		except Exception:
			return False

	def stop(self):
		if self.player:
			try:
				self.player.stop()
			except Exception:
				pass
			return True
		return False

	def get_source_object(self):
		return self.player

	def pause(self):
		self.paused = True
		if self.player:
			try:
				self.player.pause()
			except Exception:
				pass

	def resume(self):
		self.paused = False
		if self.player:
			try:
				self.player.paused = False
				oal.al.alSourcePlay(self.player.source)
				return True
			except Exception:
				return False
		return False

	def playing(self):
		if self.player:
			try:
				return self.player.playing()
			except Exception:
				pass
		return False

	def close(self, delete_effect=True):
		self.loading = True
		if self.player:
			try:
				self.player.reset()
			except Exception:
				pass
		self._loaded_sound = None
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
		return self.player is not None and self._loaded_sound is not None

	def set_3dposition(self, sound_x, sound_y, sound_z):
		if self.player:
			self.player.position = [float(sound_x), float(sound_y), float(sound_z)]
		return True

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

	@property
	def volume(self):
		if self.player:
			return _to_db_volume(self.player.volume)
		return self._volume

	@volume.setter
	def volume(self, value):
		self._volume = value
		if self.player:
			self.player.volume = _to_linear_volume(value)

	@property
	def pan(self):
		return self._pan

	@pan.setter
	def pan(self, value):
		self._pan = max(-100.0, min(100.0, float(value)))

	@property
	def pitch(self):
		if self.player:
			return self.player.pitch * 100
		return self._pitch

	@pitch.setter
	def pitch(self, value):
		self._pitch = value
		if self.player:
			self.player.pitch = float(value) / 100.0

	@property
	def direct_occlusion(self):
		return 0.0

	@direct_occlusion.setter
	def direct_occlusion(self, value):
		pass

	@property
	def reverb_occlusion(self):
		return 0.0

	@reverb_occlusion.setter
	def reverb_occlusion(self, value):
		pass

	@property
	def position(self):
		if self.player and self._loaded_sound is not None:
			try:
				return self.player.seek
			except Exception:
				pass
		return 0

	@position.setter
	def position(self, value):
		if self.player and self._loaded_sound is not None:
			try:
				self.player.seek = float(value)
			except Exception:
				pass


# ---------------------------------------------------------------------------
# Dynamic Audio Backend Selector
# ---------------------------------------------------------------------------

if FMOD_ACTIVE:
	listener = FMODListener()
	sound = FMODSound
	def get_available_output_devices():
		return ["FMOD Default Device"]
else:
	listener = _OALListener()
	sound = OpenALSound
	def get_available_output_devices():
		try:
			if listener._oal is None:
				return []
			# ALC_ALL_DEVICES_SPECIFIER = 0x1013
			raw = oal.alc.alcGetString(None, 0x1013)
			return [d.decode("utf-8", errors="replace") for d in listener._oal.parse(raw)]
		except Exception:
			return []
