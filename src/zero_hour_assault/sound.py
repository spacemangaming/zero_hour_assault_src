
import os
import traceback
import math
from constants import DIRECTORY_TEMP


import events


from oal import *
initialize_openal_bindings()
from Miscellaneous import *
from file_directories import *
from constants import *
import ctypes
from audio import *
from pack_file import *
from security import *
from variable_management import *
import globals as g
from oal import alc

pack = pack_file()
pack.open("sounds.dat")
listener = Listener()
listener.position = (0, 0, 0)

import copy
def get_available_output_devices(): #bu fonksiyonu sınıf dışına aldık
    """Returns a list of available output device names."""
    devices = listener.parse(alc.alcGetString(None, 0x1013))
    if not devices:
        return []

    return devices

class sound(object):
    cache = {}

    def __init__(self):
        self.memory = False
        self.paused=False
        self.loading=False
        self.source = None
        self.internal_filename = None  # dont modify from inside a script.
        self.slot=None
        self.effect=None
        self.downmix = False
        self.player = None
        self.usingpack = False
        self.filename = ""

    def load(self, filename="", downmix=False, load_from_memory=False):

        self.loading=True
        downmix = False # no longer used, we use AL_SPATIALIZE_SOFT for auto downmixing
        if load_from_memory:
            self.memory = True
            self.source = BufferSound()
            self.source.load(
                filename
            )  # this function can only load raw audio data. İf you want to load encoded audio data, first decode it.
            self.player = Player(downmix)
            self.player.add(self.source)
            self.player.position = (0, 0, 0)
            self.loading=False
            return self.is_active

        fname = filename
        self.internal_filename = filename
        self.downmix = downmix
        if self.is_active:
            self.close()

        if 1 == 1:
            if (fname, downmix) not in sound.cache:
                if not pack.file_exists(filename) and not file_exists(filename):         self.loading=False; return
                self.filename = pack.get_file(filename)
            else:
                self.source = LoadSound.from_file(DIRECTORY_TEMP+"/"+self.internal_filename, downmix)
                self.player = Player(downmix)
                self.player.add(self.source)
                self.player.position = (0, 0, 0)
                self.player.play_thread=None
                self.player.Playing=False
                self.loading=False
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
                    file_put_contents(DIRECTORY_TEMP+"/"+self.internal_filename, self.filename, "wb")

        try:
            if isinstance(self.filename, str):
                self.source = LoadSound.from_file(DIRECTORY_TEMP+"/"+self.filename, downmix)
                self.player = Player(downmix)
                self.player.add(self.source)
                self.player.position = (0, 0, 0)
            else:
                self.source = LoadSound.from_file(DIRECTORY_TEMP+"/"+self.internal_filename, downmix)
                self.player = Player(downmix)
                self.player.add(self.source)
                self.player.position = (0, 0, 0)
                if (fname, downmix) not in sound.cache and self.usingpack:
                    file_delete(DIRECTORY_TEMP+"/"+self.internal_filename)
                if g.cache==1:
                    sound.cache[(fname, downmix)] = True

        except:
            #traceback.print_exc()
            return False

        self.loading=False
        return self.is_active
    def fade(self, close=True):
        while self.volume>=-50:
            self.volume -= 4
            time.sleep(0.05)
        if close: self.close()
        else: self.pause()
    def fade2(self, close=True):
        while self.volume>=-50:
            self.volume -= 1
            time.sleep(0.5)
        if close: self.close()
        else: self.pause()
        g.rain=False
    def play(self):

        if not self.is_active:
            return False
        if 1 == 1:
            # self.player.loop = False
            self.paused=False
            self.player.play()
        return True

    def play_wait(self):
        if not self.is_active:
            return False
        if 1 == 1:
            self.player.loop = False
            self.player.play()
        while self.player.playing():
            events.process_events()
        return True

    def play_looped(self):
        if not self.is_active:
            return False
        if 1 == 1:

            self.player.loop = True
            self.player.play()
        return True

    def stop(self):
        if self.is_active and self.player.playing():
            if 1 == 1:
                self.player.stop()
                self.player.rewind()
            return True

    def get_source_object(self):
        return self.player

    def pause(self):
        if not self.is_active:
            return
        if 1 == 1:
            self.paused=True
            self.player.pause()

    def resume(self):
        if not self.is_active:
            return False
        if 1 == 1:
            self.paused=False
            self.player.play()

    @property
    def volume(self):
        if not self.player:
            return 0
        if not self.source:
            return 0
        return round(math.log10(self.player.volume) * 20)

    @volume.setter
    def volume(self, value):
        """Volume between 0 (full volume) to -100 silence"""
        if not self.player:
            return False
        if not self.source:
            return False

        if not self.is_active:
            return False
        vol = 10 ** (float(value) / 20)
        if vol > 1.0:
            vol = 1.0
        if 1 == 1:
            if self.player.volume!=vol: self.player.volume = vol

    @property
    def pitch(self):
        if not self.source:
            return False
        return self.player.pitch * 100

    @pitch.setter
    def pitch(self, value):
        if not self.is_active:
            return False
        if 1 == 1:
            self.player.pitch = float(value) / 100

    def close(self, delete_effect=True):
        self.loading=True
        if delete_effect:
            try:
                if self.effect is not None: self.effect.delete()
            except:             pass
        if self.player:
            if self.player.playing():
                self.stop()
            if 1 == 1:
                self.player.remove()
                self.player.delete()
                self.player = None
                if (self.memory or g.cache==0) and self.source:
                    self.source.delete()
                    self.source = None

                # self.__init__()
                if delete_effect:
                    try: self.slot.delete()
                    except:             pass

                return True

    @property
    def is_active(self):
        return self.source and self.player

    def set_3dposition(
        self, sound_x, sound_y, sound_z
    ):
        try:
            if not self.is_active:
                return False

            if 1 == 1:
                self.player.position = (sound_x, sound_y, sound_z)
        except:
            #traceback.print_exc()
            return False

        return True
