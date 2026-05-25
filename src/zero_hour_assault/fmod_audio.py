import os
import sys
import time
import math
from constants import DIRECTORY_TEMP
import globals as g
from audio import *
from pack_file import *
from security import *

# Resolve absolute path to the project root directory
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Resolve absolute path to the third_party/fmod directory
FMOD_DLL_DIR = os.path.join(ROOT_DIR, "third_party", "fmod")

# Set FMOD paths before importing pyfmodex
os.environ["PYFMODEX_DLL_PATH"] = os.path.join(FMOD_DLL_DIR, "fmod.dll")
os.environ["PYFMODEX_STUDIO_DLL_PATH"] = os.path.join(FMOD_DLL_DIR, "fmodstudio.dll")

if sys.platform == "win32" and hasattr(os, "add_dll_directory"):
    try:
        if os.path.isdir(FMOD_DLL_DIR):
            os.add_dll_directory(FMOD_DLL_DIR)
        else:
            print(f"FMOD DLL directory not found: {FMOD_DLL_DIR}")
    except Exception as e:
        print(f"Failed to add FMOD DLL directory: {e}")

try:
    import pyfmodex
    FMOD_AVAILABLE = True
except Exception as e:
    FMOD_AVAILABLE = False
    print(f"pyfmodex import failed: {e}")

system = None
initialized = False

def init_fmod():
    global system, initialized
    if not FMOD_AVAILABLE:
        return False
    if initialized:
        return True
    try:
        system = pyfmodex.System(header_version=0x00020313)
        system.init()
        initialized = True
        return True
    except Exception as e:
        print(f"Failed to initialize FMOD system: {e}")
        return False

def update_fmod():
    if initialized and system:
        try:
            system.update()
        except:
            pass

def set_listener_position(x, y, z, facing_angle=0.0):
    if initialized and system:
        try:
            rad = math.radians(facing_angle)
            forward = [math.sin(rad), math.cos(rad), 0.0]
            system.set_3d_listener_attributes(0, pos=[x, y, z], forward=forward, up=[0.0, 0.0, 1.0])
        except Exception as e:
            pass

# Initialize at module level if available
init_fmod()

class fmod_sound(object):
    def __init__(self):
        self.sound = None
        self.channel = None
        self.internal_filename = None
        self.filename = ""
        self.usingpack = False
        self.paused = False

    def load(self, filename, is_stream=False):
        if not initialized:
            if not init_fmod():
                return False
        
        self.internal_filename = filename
        
        # Import pack dynamically to avoid circular import issues
        from sound import pack
        
        if not pack.file_exists(filename) and not os.path.exists(filename):
            return False
            
        file_path = filename
        if pack.file_exists(filename):
            extracted = pack.get_file(filename)
            if extracted == False:
                file_path = filename
            elif isinstance(extracted, str):
                file_path = os.path.join(DIRECTORY_TEMP, extracted)
            else:
                # Decrypt and write to temp directory
                content = extracted.read() if hasattr(extracted, "read") else extracted
                content = string_decrypt(content, g.sdeckey)
                temp_path = os.path.join(DIRECTORY_TEMP, filename)
                temp_dir = os.path.dirname(temp_path)
                if not os.path.exists(temp_dir):
                    os.makedirs(temp_dir)
                with open(temp_path, "wb") as f:
                    f.write(content)
                file_path = temp_path
                self.usingpack = True
        
        try:
            # Set 3D mode on creation if positioning is needed
            if is_stream:
                self.sound = system.create_stream(file_path)
            else:
                self.sound = system.create_sound(file_path)
            return True
        except Exception as e:
            print(f"FMOD failed to load sound {filename}: {e}")
            return False

    def play(self):
        if not self.sound:
            return False
        try:
            self.channel = self.sound.play()
            self.paused = False
            return True
        except Exception as e:
            print(f"FMOD failed to play sound: {e}")
            return False

    def play_looped(self):
        if not self.sound:
            return False
        try:
            # Configure sound to loop infinitely
            self.sound.mode = pyfmodex.flags.MODE.LOOP_NORMAL
            self.sound.loop_count = -1
            self.channel = self.sound.play()
            self.paused = False
            return True
        except Exception as e:
            print(f"FMOD failed to play looped sound: {e}")
            return False

    def stop(self):
        if self.channel:
            try:
                self.channel.stop()
                return True
            except:
                pass
        return False

    def pause(self):
        if self.channel:
            try:
                self.channel.paused = True
                self.paused = True
                return True
            except:
                pass
        return False

    def resume(self):
        if self.channel:
            try:
                self.channel.paused = False
                self.paused = False
                return True
            except:
                pass
        return False

    @property
    def volume(self):
        if self.channel:
            try:
                vol = self.channel.volume
                if vol <= 0.0:
                    return -100
                return round(math.log10(vol) * 20)
            except:
                pass
        return 0

    @volume.setter
    def volume(self, value):
        if self.channel:
            try:
                vol = 10 ** (float(value) / 20)
                if vol > 1.0:
                    vol = 1.0
                self.channel.volume = vol
            except:
                pass

    @property
    def pitch(self):
        if self.channel:
            try:
                return self.channel.pitch * 100
            except:
                pass
        return 100

    @pitch.setter
    def pitch(self, value):
        if self.channel:
            try:
                self.channel.pitch = float(value) / 100
            except:
                pass

    def set_3dposition(self, sound_x, sound_y, sound_z):
        if self.channel:
            try:
                # Update mode to support 3D positioning
                self.channel.mode = pyfmodex.flags.MODE.THREED
                self.channel.position = [sound_x, sound_y, sound_z]
                return True
            except:
                pass
        return False

    def close(self):
        self.stop()
        if self.sound:
            try:
                self.sound.release()
            except:
                pass
            self.sound = None
        self.channel = None
        if self.usingpack and self.internal_filename:
            temp_path = os.path.join(DIRECTORY_TEMP, self.internal_filename)
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass

    @property
    def is_active(self):
        return self.sound is not None
