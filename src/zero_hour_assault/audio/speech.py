
from translation import translate
from Miscellaneous import is_game_window_active
import pygame
import globals as g
import ctypes
import sys
try:
    sral=ctypes.CDLL("SRAL.dll")
    g.sral=sral
    sral.SRAL_Initialize()
    _sral_available = True
except OSError:
    sral = None
    _sral_available = False

def speak(text, interrupt=True, forceinterrupt=True):
    if not _sral_available:
        return False
    text = str(text)
    if text=="prevmenu": return
    if g.lang!="en": text = translate(text)
    if forceinterrupt: interrupt=True if g.interrupt==1 else False
    if g.awindow==1 and not is_game_window_active(): return
    if text == "":
        return
    g.last_spoken_text=text
    engines = [2, 8, 4]
    for engine in engines:
        res = sral.SRAL_SpeakEx(engine, text.encode(), interrupt)
        if res: return True
    return False