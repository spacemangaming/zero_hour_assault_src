# FMOD has been removed. This stub exists solely to prevent import errors
# in any code that still references fmod_audio.
FMOD_AVAILABLE = False
initialized = False
system = None
echo_dsp = None
lowpass_dsp = None

def init_fmod(): return False
def update_fmod(): pass
def set_listener_position(*a, **kw): pass
def get_output_devices(): return []
def set_output_device(name): return False
def clear_sound_cache(): pass

class fmod_sound:
    def __init__(self):
        self.sound = None
        self.channel = None
        self.usingpack = False
    def load(self, *a, **kw): return False
    def play(self): return False
    def play_looped(self): return False
    def stop(self): return False
    def close(self): pass
    @property
    def is_active(self): return False
