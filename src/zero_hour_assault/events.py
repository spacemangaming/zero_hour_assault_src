# window events written by nbm studios
import os,time
from joystick import joystick

import platform
import sys
import pygame
import ctypes
import globals as g
from pygame.locals import *
from speech import speak

from timer import timer
current_key_pressed = -1
current_key_released = -1
pygame.init()
pygame.font.init()
clock=pygame.time.Clock()
stickchecktimer=timer()
def process_events():
	global current_key_pressed, current_key_released
	if g.yavaslat==1 or g.steam==1:
		clock.tick(1000)
	if stickchecktimer.elapsed>=1000:
		stickchecktimer.restart()
		if len(g.sticks)!=pygame.joystick.get_count():
			if len(g.sticks)<pygame.joystick.get_count(): speak("Joystick inserted")
			if len(g.sticks)>pygame.joystick.get_count(): speak("Joystick removed")
			for stick in g.sticks: stick.joystick.quit()
			g.sticks.clear()
			for i in range(pygame.joystick.get_count()): g.sticks.append(joystick(i))
	if g.captiontoset!="":
		pygame.display.set_caption(g.captiontoset); g.captiontoset=""
	g.current_scancode=-1
	current_key_pressed = -1
	current_key_released = -1
	events = pygame.event.get()
	for stick in g.sticks:
		stick.update(events)
	for event in events:
		if event.type == QUIT and not g.exiting:
			if g.died: return
			if g.mapname!="lobby" and g.cannotexit: speak("You have to wait 1 minutes to be able to exit after hit"); return
			if g.mapname!="lobby" and g.near2: speak("You cannot exit because someone near you"); return
			try:    g.mus.fade()
			except: pass
			try: g.n.send_reliable(0,"close",0)
			except: return
			speak("Exiting ...")
			g.exiting=True


			g.p.play_stationary("gamedoorclose.ogg",False)
			delay(1700)
			try: g.n.send_reliable(0,"close",0)
			except: pass
			g.writeprefs(); g.reset()

			pygame.quit()
			ctypes.windll.kernel32.ExitProcess(0)
			break
		if event.type == pygame.KEYDOWN:
			#g.sral.SRAL_StopSpeech()
			g.current_scancode=event.scancode
			g.keys_held.append(event.key)
			current_key_pressed = event.key
		if event.type == pygame.KEYUP:
			if event.key in g.keys_held: g.keys_held.remove(event.key)
			if hasattr(event,"unicode") and event.unicode == g.lastchar:
				g.lastchar = ""
			current_key_released = event.key
	g.lastevents = events
	return events


def key_pressed(key_code):
	return current_key_pressed == key_code


def key_released(key_code):
	return current_key_released == key_code


def key_down(key_code):
	return key_code in g.keys_held


def key_up(key_code):
	return key_code not in g.keys_held
def delay(ms):
	waittimer=timer()
	while waittimer.elapsed<ms:
		process_events()
g.delay=delay
def delay2(ms):
	waittimer=timer()
	while waittimer.elapsed<ms:
		process_events()
		try: g.netloop()
		except: pass
g.delay2=delay2