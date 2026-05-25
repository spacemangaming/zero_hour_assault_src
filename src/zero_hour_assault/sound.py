import os
import traceback
import math
import time
from constants import DIRECTORY_TEMP
import events

# Try FMOD first
FMOD_ACTIVE = False
try:
    import sys
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    FMOD_DLL_DIR = os.path.join(ROOT_DIR, "third_party", "fmod")
    os.environ["PYFMODEX_DLL_PATH"] = os.path.join(FMOD_DLL_DIR, "fmod.dll")
    os.environ["PYFMODEX_STUDIO_DLL_PATH"] = os.path.join(FMOD_DLL_DIR, "fmodstudio.dll")
    if sys.platform == "win32" and hasattr(os, "add_dll_directory"):
        try:
            os.add_dll_directory(FMOD_DLL_DIR)
        except Exception:
            pass
    import fmod_audio
    import pyfmodex
    # Ensure FMOD is initialized successfully
    if fmod_audio.FMOD_AVAILABLE and fmod_audio.init_fmod():
        FMOD_ACTIVE = True
    else:
        reasons = []
        if not fmod_audio.FMOD_AVAILABLE:
            reasons.append("pyfmodex library is not available or failed to import")
        else:
            reasons.append("FMOD system failed to initialize (check fmod_audio initialization log)")
        print(f"FMOD failed to activate in sound.py (Reason: {', '.join(reasons)}). Falling back to OpenAL backend.")
except Exception as e:
    print(f"FMOD initialization failed in sound.py: {e}")

# Try OpenAL bindings (required for voice chat even if FMOD is active, or as fallback)
OPENAL_ACTIVE = False
try:
    from oal import *
    initialize_openal_bindings()
    OPENAL_ACTIVE = True
except Exception as e:
    print(f"OpenAL initialization failed in sound.py: {e}")

from Miscellaneous import *
from file_directories import *
from constants import *
import ctypes
from audio import *
from pack_file import *
from security import *
from variable_management import *
import globals as g

pack = pack_file()
pack.open("sounds.dat")

if FMOD_ACTIVE:
    # ----------------------------------------------------
    # FMOD Audio Backend Implementation
    # ----------------------------------------------------

    class FMODListener(object):
        def __init__(self):
            self._position = [0.0, 0.0, 0.0]
            self._gain = 1.0
            self._hrtf = 2

        def _set_gain(self, value):
            self._gain = value
            if fmod_audio.initialized and fmod_audio.system:
                try:
                    fmod_audio.system.master_channel_group.volume = value
                except Exception as e:
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
            self._position = list(pos)
            if fmod_audio.initialized and fmod_audio.system:
                try:
                    fmod_audio.system.set_3d_listener_attributes(
                        0, pos=self._position, forward=[0.0, 1.0, 0.0], up=[0.0, 0.0, 1.0]
                    )
                except Exception as e:
                    pass

        def delete(self):
            pass

    class FMODPlayerProxy(object):
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
            if self._parent._fmod_sound and self._parent._fmod_sound.channel:
                try:
                    self._parent._fmod_sound.channel.set_position(0, pyfmodex.enums.TIMEUNIT.MS)
                except:
                    pass

        def pause(self):
            return self._parent.pause()

        def delete(self):
            pass

        def remove(self):
            pass

        def add_effect(self, slot, filtr=None):
            pass

        def del_effect(self, slot):
            pass

        def seek(self, offset):
            if self._parent._fmod_sound and self._parent._fmod_sound.channel and self._parent._fmod_sound.sound:
                try:
                    import pyfmodex
                    length = self._parent._fmod_sound.sound.get_length(pyfmodex.enums.TIMEUNIT.MS)
                    self._parent._fmod_sound.channel.set_position(int(length * offset), pyfmodex.enums.TIMEUNIT.MS)
                except:
                    pass

        @property
        def source(self):
            import ctypes
            return ctypes.c_uint(0)

        @property
        def volume(self):
            if self._parent._fmod_sound and self._parent._fmod_sound.channel:
                try:
                    return self._parent._fmod_sound.channel.volume
                except:
                    pass
            return 10 ** (float(self._parent._volume) / 20)

        @volume.setter
        def volume(self, value):
            self._parent.volume = round(math.log10(float(value)) * 20) if float(value) > 0 else -100

        @property
        def pitch(self):
            if self._parent._fmod_sound and self._parent._fmod_sound.channel:
                try:
                    return self._parent._fmod_sound.channel.pitch
                except:
                    pass
            return self._parent._pitch / 100

        @pitch.setter
        def pitch(self, value):
            self._parent.pitch = float(value) * 100

        @property
        def position(self):
            if self._parent._fmod_sound and self._parent._fmod_sound.channel:
                try:
                    pos = self._parent._fmod_sound.channel.position
                    return (pos.x, pos.y, pos.z)
                except:
                    pass
            return tuple(self._parent._position)

        @position.setter
        def position(self, pos):
            self._parent.set_3dposition(pos[0], pos[1], pos[2])

    listener = FMODListener()

    def get_available_output_devices():
        return ["FMOD Default Device"]

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
            
            # Internal properties
            self._volume = 0.0     # Decibels (0 to -100)
            self._pitch = 100.0    # Percentage (100 = normal)
            self._position = [0.0, 0.0, 0.0]
            self._looping = False
            
            # Proxies
            self.player = FMODPlayerProxy(self)
            self.source = self

        def load(self, filename="", downmix=False, load_from_memory=False):
            self.loading = True
            self.internal_filename = filename
            self.downmix = downmix
            
            if self._fmod_sound:
                self.close()

            self._fmod_sound = fmod_audio.fmod_sound()
            
            is_stream = False
            fn_lower = filename.lower()
            if "music" in fn_lower or "ambient" in fn_lower or "stream" in fn_lower or "song" in fn_lower:
                is_stream = True

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
            g.rain = False

        def play(self):
            if not self.is_active:
                return False
            
            self.paused = False
            self._looping = False
            
            mode = pyfmodex.flags.MODE.LOOP_OFF
            if self.player.stationary:
                mode |= pyfmodex.flags.MODE.TWOD
            else:
                mode |= pyfmodex.flags.MODE.THREED
                
            try:
                self._fmod_sound.channel = self._fmod_sound.sound.play(paused=True)
                self._fmod_sound.channel.mode = mode
                self._apply_properties()
                self._fmod_sound.channel.paused = False
                return True
            except Exception as e:
                print(f"FMOD play failed: {e}")
                return False

        def play_wait(self):
            if not self.play():
                return False
            while self.playing():
                events.process_events()
            return True

        def play_looped(self):
            if not self.is_active:
                return False
            
            self.paused = False
            self._looping = True
            
            mode = pyfmodex.flags.MODE.LOOP_NORMAL
            if self.player.stationary:
                mode |= pyfmodex.flags.MODE.TWOD
            else:
                mode |= pyfmodex.flags.MODE.THREED
                
            try:
                self._fmod_sound.channel = self._fmod_sound.sound.play(paused=True)
                self._fmod_sound.sound.loop_count = -1
                self._fmod_sound.channel.mode = mode
                self._apply_properties()
                self._fmod_sound.channel.paused = False
                return True
            except Exception as e:
                print(f"FMOD play_looped failed: {e}")
                return False

        def stop(self):
            if self._fmod_sound:
                self._fmod_sound.stop()
                return True
            return False

        def get_source_object(self):
            return self.player

        def pause(self):
            self.paused = True
            if self._fmod_sound and self._fmod_sound.channel:
                try:
                    self._fmod_sound.channel.paused = True
                except:
                    pass

        def resume(self):
            self.paused = False
            if self._fmod_sound and self._fmod_sound.channel:
                try:
                    self._fmod_sound.channel.paused = False
                    return True
                except:
                    pass
            return False

        def playing(self):
            if self._fmod_sound and self._fmod_sound.channel:
                try:
                    return self._fmod_sound.channel.is_playing
                except:
                    pass
            return False

        @property
        def volume(self):
            if self._fmod_sound and self._fmod_sound.channel:
                try:
                    vol = self._fmod_sound.channel.volume
                    if vol <= 0.0:
                        return -100
                    self._volume = round(math.log10(vol) * 20)
                except:
                    pass
            return self._volume

        @volume.setter
        def volume(self, value):
            self._volume = value
            if self._fmod_sound and self._fmod_sound.channel:
                try:
                    vol = 10 ** (float(value) / 20)
                    if vol > 1.0:
                        vol = 1.0
                    self._fmod_sound.channel.volume = vol
                except:
                    pass

        @property
        def pitch(self):
            if self._fmod_sound and self._fmod_sound.channel:
                try:
                    self._pitch = self._fmod_sound.channel.pitch * 100
                except:
                    pass
            return self._pitch

        @pitch.setter
        def pitch(self, value):
            self._pitch = value
            if self._fmod_sound and self._fmod_sound.channel:
                try:
                    self._fmod_sound.channel.pitch = float(value) / 100
                except:
                    pass

        def close(self, delete_effect=True):
            self.loading = True
            if self._fmod_sound:
                self._fmod_sound.close()
                self._fmod_sound = None
            self.loading = False
            return True

        @property
        def is_active(self):
            return self._fmod_sound is not None and self._fmod_sound.sound is not None

        def set_3dposition(self, sound_x, sound_y, sound_z):
            self._position = [sound_x, sound_y, sound_z]
            if self._fmod_sound:
                if self._fmod_sound.channel:
                    try:
                        self._fmod_sound.channel.mode = pyfmodex.flags.MODE.THREED
                        self._fmod_sound.channel.position = self._position
                        
                        # Apply min and max distance for realistic 3D audio rolloff
                        min_dist = 1.0
                        if hasattr(self.player, "rolloff") and self.player.rolloff > 0:
                            min_dist = 1.0 / self.player.rolloff
                        self._fmod_sound.channel.min_distance = min_dist
                        
                        max_dist = 10000.0
                        if hasattr(self.player, "max_distance") and self.player.max_distance > 0:
                            max_dist = float(self.player.max_distance)
                        self._fmod_sound.channel.max_distance = max_dist
                        
                        return True
                    except:
                        pass
            return False

        def _apply_properties(self):
            if not self._fmod_sound or not self._fmod_sound.channel:
                return
            try:
                # Volume
                vol = 10 ** (float(self._volume) / 20)
                if vol > 1.0:
                    vol = 1.0
                self._fmod_sound.channel.volume = vol
                
                # Pitch
                self._fmod_sound.channel.pitch = float(self._pitch) / 100
                
                # Position
                if not self.player.stationary:
                    self._fmod_sound.channel.position = self._position
                    
                    # Apply min and max distance for realistic 3D audio rolloff
                    min_dist = 1.0
                    if hasattr(self.player, "rolloff") and self.player.rolloff > 0:
                        min_dist = 1.0 / self.player.rolloff
                    self._fmod_sound.channel.min_distance = min_dist
                    
                    max_dist = 10000.0
                    if hasattr(self.player, "max_distance") and self.player.max_distance > 0:
                        max_dist = float(self.player.max_distance)
                    self._fmod_sound.channel.max_distance = max_dist
            except Exception as e:
                pass

else:
    # ----------------------------------------------------
    # OpenAL Fallback Implementation (Original Code)
    # ----------------------------------------------------
    from oal import alc
    listener = Listener()
    listener.position = (0, 0, 0)

    import copy
    def get_available_output_devices():
        devices = listener.parse(alc.alcGetString(None, 0x1013))
        if not devices:
            return []
        return devices

    class sound(object):
        cache = {}

        def __init__(self):
            self.memory = False
            self.paused = False
            self.loading = False
            self.source = None
            self.internal_filename = None
            self.slot = None
            self.effect = None
            self.downmix = False
            self.player = None
            self.usingpack = False
            self.filename = ""

        def load(self, filename="", downmix=False, load_from_memory=False):
            self.loading = True
            downmix = False
            if load_from_memory:
                self.memory = True
                self.source = BufferSound()
                self.source.load(filename)
                self.player = Player(downmix)
                self.player.add(self.source)
                self.player.position = (0, 0, 0)
                self.loading = False
                return self.is_active

            fname = filename
            self.internal_filename = filename
            self.downmix = downmix
            if self.is_active:
                self.close()

            if 1 == 1:
                if (fname, downmix) not in sound.cache:
                    if not pack.file_exists(filename) and not file_exists(filename):
                        self.loading = False
                        return
                    self.filename = pack.get_file(filename)
                else:
                    self.source = LoadSound.from_file(DIRECTORY_TEMP + "/" + self.internal_filename, downmix)
                    self.player = Player(downmix)
                    self.player.add(self.source)
                    self.player.position = (0, 0, 0)
                    self.player.play_thread = None
                    self.player.Playing = False
                    self.loading = False
                    return self.is_active

                if self.filename == False:
                    self.filename = fname
                if self.filename != fname:
                    self.filename = self.filename.read()
                    self.usingpack = True
                    deckey = g.sdeckey
                    if self.filename == False:
                        return

                    if fname not in sound.cache:
                        self.filename = string_decrypt(self.filename, deckey)
                    if fname not in sound.cache:
                        file_put_contents(DIRECTORY_TEMP + "/" + self.internal_filename, self.filename, "wb")

            try:
                if isinstance(self.filename, str):
                    self.source = LoadSound.from_file(DIRECTORY_TEMP + "/" + self.filename, downmix)
                    self.player = Player(downmix)
                    self.player.add(self.source)
                    self.player.position = (0, 0, 0)
                else:
                    self.source = LoadSound.from_file(DIRECTORY_TEMP + "/" + self.internal_filename, downmix)
                    self.player = Player(downmix)
                    self.player.add(self.source)
                    self.player.position = (0, 0, 0)
                    if (fname, downmix) not in sound.cache and self.usingpack:
                        file_delete(DIRECTORY_TEMP + "/" + self.internal_filename)
                    if g.cache == 1:
                        sound.cache[(fname, downmix)] = True

            except:
                return False

            self.loading = False
            return self.is_active

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
            g.rain = False

        def play(self):
            if not self.is_active:
                return False
            self.paused = False
            self.player.play()
            return True

        def play_wait(self):
            if not self.is_active:
                return False
            self.player.loop = False
            self.player.play()
            while self.player.playing():
                events.process_events()
            return True

        def play_looped(self):
            if not self.is_active:
                return False
            self.player.loop = True
            self.player.play()
            return True

        def stop(self):
            if self.is_active and self.player.playing():
                self.player.stop()
                self.player.rewind()
                return True

        def get_source_object(self):
            return self.player

        def pause(self):
            if not self.is_active:
                return
            self.paused = True
            self.player.pause()

        def resume(self):
            if not self.is_active:
                return False
            self.paused = False
            self.player.play()

        @property
        def volume(self):
            if not self.player or not self.source:
                return 0
            return round(math.log10(self.player.volume) * 20)

        @volume.setter
        def volume(self, value):
            if not self.player or not self.source or not self.is_active:
                return False
            vol = 10 ** (float(value) / 20)
            if vol > 1.0:
                vol = 1.0
            if self.player.volume != vol:
                self.player.volume = vol

        @property
        def pitch(self):
            if not self.source:
                return False
            return self.player.pitch * 100

        @pitch.setter
        def pitch(self, value):
            if not self.is_active:
                return False
            self.player.pitch = float(value) / 100

        def close(self, delete_effect=True):
            self.loading = True
            if delete_effect:
                try:
                    if self.effect is not None:
                        self.effect.delete()
                except:
                    pass
            if self.player:
                if self.player.playing():
                    self.stop()
                self.player.remove()
                self.player.delete()
                self.player = None
                if (self.memory or g.cache == 0) and self.source:
                    self.source.delete()
                    self.source = None

                if delete_effect:
                    try:
                        self.slot.delete()
                    except:
                        pass

                return True

        @property
        def is_active(self):
            return self.source and self.player

        def set_3dposition(self, sound_x, sound_y, sound_z):
            try:
                if not self.is_active:
                    return False
                self.player.position = (sound_x, sound_y, sound_z)
            except:
                return False
            return True
