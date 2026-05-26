# pack file handling system written by nbm studios
from Miscellaneous import *
from constants import *
from file_directories import *
from security import *
import globals as g


def get_sound_storage():
    return g.sstorage


def set_sound_storage(pack):
    g.sstorage = pack


def set_sound_decryption_key(key):
    g.sdeckey = key
