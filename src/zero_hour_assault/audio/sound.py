import math
import os
import sys
import time

from constants import DIRECTORY_TEMP

if getattr(sys, "frozen", False):
	ROOT_DIR = os.path.dirname(sys.executable)
else:
	ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SOUNDS_DIR = os.path.join(ROOT_DIR, "sounds")

# Initialize OpenAL bindings
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


# ---------------------------------------------------------------------------
# Listener wrapper
# ---------------------------------------------------------------------------

class _OALListener(object):
	"""Thin wrapper around oal.Listener that matches the FMODListener interface."""
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


listener = _OALListener()


# ---------------------------------------------------------------------------
# Device enumeration
# ---------------------------------------------------------------------------

def get_available_output_devices():
	"""Return list of available OpenAL output device names."""
	try:
		if listener._oal is None:
			return []
		# ALC_ALL_DEVICES_SPECIFIER = 0x1013
		raw = oal.alc.alcGetString(None, 0x1013)
		return [d.decode("utf-8", errors="replace") for d in listener._oal.parse(raw)]
	except Exception:
		return []


# ---------------------------------------------------------------------------
# Sound class
# ---------------------------------------------------------------------------

class sound(object):
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

	# OAL EFX occlusion not wired at this level — no-ops keep interface intact
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
