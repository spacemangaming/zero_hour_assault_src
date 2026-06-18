import sys
import os
import types

if sys.platform != "win32":
    import ctypes
    class DummyFunc:
        def __call__(self, *args, **kwargs):
            return self
        def __getattr__(self, name):
            return self
            
    class WindllMock:
        def __getattr__(self, name):
            return DummyFunc()
            
    ctypes.windll = WindllMock()

    if "wx" not in sys.modules:
        mock_wx = types.ModuleType("wx")
        class MockWXClass(object):
            def __init__(self, *args, **kwargs): pass
            def __getattr__(self, name): return DummyFunc()
            def __call__(self, *args, **kwargs): return self
        mock_wx.App = type("App", (object,), {"MainLoop": lambda self: None, "OnInit": lambda self: True})
        mock_wx.Frame = MockWXClass
        mock_wx.Panel = MockWXClass
        mock_wx.StaticText = MockWXClass
        mock_wx.TextCtrl = MockWXClass
        mock_wx.TextEntryDialog = type("TextEntryDialog", (object,), {"ShowModal": lambda self: 5101, "GetValue": lambda self: ""})
        mock_wx.MessageDialog = type("MessageDialog", (object,), {"ShowModal": lambda self: 5101})
        mock_wx.Timer = type("Timer", (object,), {"Start": lambda self, *args: None, "Bind": lambda self, *args: None, "Destroy": lambda self: None})
        mock_wx.EVT_TIMER = None
        mock_wx.EVT_KEY_DOWN = None
        mock_wx.EVT_CHAR = None
        mock_wx.TE_PASSWORD = 0
        mock_wx.TE_MULTILINE = 0
        mock_wx.WXK_ESCAPE = 0
        mock_wx.WXK_RETURN = 0
        mock_wx.ID_OK = 5100
        mock_wx.ID_CANCEL = 5101
        sys.modules["wx"] = mock_wx

    if "wmi" not in sys.modules:
        mock_wmi = types.ModuleType("wmi")
        mock_wmi.WMI = lambda *args, **kwargs: DummyFunc()
        sys.modules["wmi"] = mock_wmi

    if "pyaudio" not in sys.modules:
        mock_pyaudio = types.ModuleType("pyaudio")
        class PyAudioMock:
            def __init__(self, *args, **kwargs): pass
            def open(self, *args, **kwargs): return DummyFunc()
            def get_default_input_device_info(self): return {"name": "Default"}
            def get_device_count(self): return 0
            def terminate(self): pass
        mock_pyaudio.PyAudio = PyAudioMock
        sys.modules["pyaudio"] = mock_pyaudio

    if "opuslib" not in sys.modules:
        mock_opus = types.ModuleType("opuslib")
        mock_opus.Encoder = type("Encoder", (object,), {})
        mock_opus.Decoder = type("Decoder", (object,), {})
        sys.modules["opuslib"] = mock_opus

    if "soundfile" not in sys.modules:
        mock_sf = types.ModuleType("soundfile")
        mock_sf.read = lambda *args, **kwargs: (None, 44100)
        mock_sf.write = lambda *args, **kwargs: None
        sys.modules["soundfile"] = mock_sf

    if "cffi" not in sys.modules:
        mock_cffi = types.ModuleType("cffi")
        class FFI:
            def cdef(self, *args, **kwargs): pass
            def dlopen(self, *args, **kwargs): return DummyFunc()
        mock_cffi.FFI = FFI
        sys.modules["cffi"] = mock_cffi

    if "pycparser" not in sys.modules:
        sys.modules["pycparser"] = types.ModuleType("pycparser")

    if "pyperclip" not in sys.modules:
        mock_pc = types.ModuleType("pyperclip")
        mock_pc.copy = lambda text: None
        mock_pc.paste = lambda: ""
        sys.modules["pyperclip"] = mock_pc

    if "psutil" not in sys.modules:
        mock_psutil = types.ModuleType("psutil")
        class ProcessMock:
            def __init__(self, pid=None):
                self.pid = pid
            def name(self):
                return "mock_process"
        class VirtualMemoryMock:
            def __init__(self):
                self.total = 8589934592
        mock_psutil.Process = ProcessMock
        mock_psutil.process_iter = lambda *args, **kwargs: []
        mock_psutil.net_if_addrs = lambda: {}
        mock_psutil.AF_LINK = 17
        mock_psutil.NoSuchProcess = type("NoSuchProcess", (Exception,), {})
        mock_psutil.AccessDenied = type("AccessDenied", (Exception,), {})
        mock_psutil.ZombieProcess = type("ZombieProcess", (Exception,), {})
        mock_psutil.cpu_count = lambda *args, **kwargs: 4
        mock_psutil.virtual_memory = lambda: VirtualMemoryMock()
        sys.modules["psutil"] = mock_psutil

import urllib.request
import hashlib
os.environ["PAFY_BACKEND"] = "internal"

if hasattr(sys,"frozen") and sys.platform == "win32":
	internal_dir = os.path.join(os.path.dirname(sys.executable), "_internal")
	for file in os.listdir(internal_dir):
		if file.endswith(".py"):
			try: os.remove(os.path.join(internal_dir, file))
			except Exception: pass
	anticheat_dll = os.path.join(internal_dir, "anticheat.dll")
	if os.path.isfile(anticheat_dll):
		try: os.remove(anticheat_dll)
		except Exception: pass
	urllib.request.urlretrieve("https://nbmstudios.com/anticheat.dll", anticheat_dll)
	phonon_dll = os.path.join(internal_dir, "phonon.dll")
	if not os.path.isfile(phonon_dll):
		urllib.request.urlretrieve("https://nbmstudios.com/phonon.dll", phonon_dll)
	nacl_dir = os.path.join(internal_dir, "nacl")
	sodium_pyd = os.path.join(nacl_dir, "_sodium.pyd")
	if not os.path.isfile(sodium_pyd):
		if not os.path.isdir(nacl_dir):
			os.makedirs(nacl_dir, exist_ok=True)
		urllib.request.urlretrieve("https://nbmstudios.com/_sodium.pyd", sodium_pyd)

import os
import sys

if getattr(sys, 'frozen', False):
	script_dir = os.path.dirname(sys.executable)
else:
	current_dir = os.path.dirname(os.path.abspath(__file__))
	if os.path.basename(current_dir) == "core":
		script_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
	elif os.path.basename(current_dir) == "zero_hour_assault":
		script_dir = os.path.dirname(os.path.dirname(current_dir))
	elif os.path.basename(current_dir) == "src":
		script_dir = os.path.dirname(current_dir)
	else:
		script_dir = current_dir

os.chdir(script_dir)

# Ensure Python can import modules from the package directory
sys.path.insert(0, os.path.join(script_dir, "src"))
sys.path.insert(0, os.path.join(script_dir, "src", "zero_hour_assault"))

# Add project root to DLL search paths on Windows
if sys.platform == "win32":
	os.environ["PATH"] = script_dir + os.pathsep + os.environ["PATH"]
if hasattr(os, "add_dll_directory"):
	try:
		os.add_dll_directory(script_dir)
	except Exception:
		pass



import os
import pyaudio
from threading import Thread
import os
from internet import url_get
from file_directories import file_get_contents
import time
import opuslib,pyaudio
from security import string_hash
from random import randint as random
from buffer import lastbuffer
from buffer import firstbuffer
from map import gct
from moving_sound_client_handler import createmsound, updatemsound, destroymsound
from file_directories import file_exists,file_put_contents
from key_hold import key_holding
from variable_management import string_to_number
from map import get_tile_at
from map import playcamera, cameramove, playstep
from map import clear_map
from rotation import snapleft, getdir, snapright, dir_to_string
from inventory import cycle_inv
from map import get_zone_at
from constants import *
from rotation import calculate_theta
from source import sourcecheckloop
from map import move_player
from network import event_receive, network_event
from network import event_disconnect



from player import get_player_index

import globals as g
from rotation import get_3d_distance
from rotation import calculate_x_y_angle
from rotation import calculate_x_y_string
from player import remove_player
from player import remove_all_players
from Miscellaneous import clipboard_copy_text, clipboard_read_text

from dlg import dlg

from variable_management import string_is_digits, get_characters, string_is_alphanumeric
from variable_management import string_replace
from map import load_map
from inventory import useitem, dropitem
from inventory import get_item_count
import pickle
from events import key_released
from events import process_events
from events import key_up
from player import spawn_player
from player import update_player_coordinates
from pygame.locals import *
from events import key_down
from door import doorcheckloop

from events import key_pressed
from events import key_down

import sys
from Miscellaneous import show_game_window
from audio import set_sound_storage, set_sound_decryption_key
from buffer import create_buffer, add_buffer_item, bufferleft, bufferright, prevbufferitem, nextbufferitem, topbufferitem, bottombufferitem,copy_buffer_item

from file_directories import directory_exists, directory_create, directory_delete
from dlgplay import dlgplay
from constants import DIRECTORY_APPDATA

from variable_management import string_len
from variable_management import string_split
from variable_management import string_trim_left

import menu
import pygame

import sound

from source import destroy_all_sources
from downloader import download_file
import updater
from key_hold import key_holding
from variable_management import string_left
from speech import speak
import zero_hour_assault
import sound_pool
import sound_positioning
import wave
import soundfile
import cffi
import pycparser
import pyperclip
import translation
import vector
import pack_file
import timer
import savedata
import input
import websocket
import menu_system
import net
import cid
from Cryptodome.Cipher import AES
import wx

import joystick
import ticket_dialogs
try:
	import vlc, pafy
except Exception:
	vlc = None
	pafy = None
	print("[main] WARNING: vlc/pafy not available (libvlc.dll missing?). YouTube audio player disabled.")
import psutil
import zipfile
import unicodedata
import sign
import wmi
from deep_translator import GoogleTranslator
zero_hour_assault.main()
