import urllib.request,os,sys
import hashlib
import os
os.environ["PAFY_BACKEND"] = "internal"

if hasattr(sys,"frozen"):
	for file in os.listdir("_internal"):
		if file.endswith(".py"): os.remove("_internal/"+file)
	if os.path.isfile("_internal/anticheat.dll"): os.remove("_internal/anticheat.dll")
	urllib.request.urlretrieve("https://nbmstudios.com/anticheat.dll","_internal/anticheat.dll")
	if not os.path.isfile("_internal/phonon.dll"): urllib.request.urlretrieve("https://nbmstudios.com/phonon.dll","_internal/phonon.dll")
	if not os.path.isfile("_internal/nacl/_sodium.pyd"):
		if not os.path.isdir("_internal/nacl"): os.mkdir("_internal/nacl")
		urllib.request.urlretrieve("https://nbmstudios.com/_sodium.pyd","_internal/nacl/_sodium.pyd")

import os
import sys

if getattr(sys, 'frozen', False):
	script_dir = os.path.dirname(sys.executable)
else:
	current_dir = os.path.dirname(os.path.abspath(__file__))
	if os.path.basename(current_dir) == "zero_hour_assault":
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
if os.path.isfile("sounds1.dat"):
	os.remove("sounds.dat")
	os.rename("sounds1.dat","sounds.dat")

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
import vlc,pafy
import psutil
import zipfile
import unicodedata
import sign
import wmi
from deep_translator import GoogleTranslator
zero_hour_assault.main()
