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

class TouchGestureProcessor:
	def __init__(self):
		self.active_touches = {} # finger_id -> {start_x, start_y, last_x, last_y, start_time, moved, hold_keys}
		self.recent_taps = [] # list of (x, y, timestamp)
		self.recent_two_finger_taps = [] # list of timestamps
		
		# Session states for multi-finger gesture classification
		self.session_fingers = 0
		self.session_moved = False
		self.session_start_time = 0
		self.session_start_x = 0
		self.session_start_y = 0
		self.session_dx = 0
		self.session_dy = 0

	def process_pygame_events(self, events):
		simulated_events = []
		now = time.time()
		
		# Check if we are running on Android to avoid duplicate touch-to-mouse events
		is_android = sys.platform == "android" or "ANDROID_ARGUMENT" in os.environ or "ANDROID_BOOTSTRAP" in os.environ
		
		# Get screen size for mouse normalization (for testing gestures on PC)
		surface = pygame.display.get_surface()
		win_w, win_h = (800, 600)
		if surface:
			win_w, win_h = surface.get_size()
			
		for event in events:
			# 1. Translate Mouse Events to simulated Finger Events for testing on PC (Disabled on Android)
			if not is_android and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				x = event.pos[0] / win_w
				y = event.pos[1] / win_h
				sim_event = pygame.event.Event(pygame.FINGERDOWN, finger_id=999, x=x, y=y, touch_id=0)
				simulated_events.extend(self.handle_finger_down(sim_event, now))
			elif not is_android and event.type == pygame.MOUSEMOTION and 999 in self.active_touches:
				x = event.pos[0] / win_w
				y = event.pos[1] / win_h
				sim_event = pygame.event.Event(pygame.FINGERMOTION, finger_id=999, x=x, y=y, touch_id=0)
				simulated_events.extend(self.handle_finger_motion(sim_event, now))
			elif not is_android and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				if 999 in self.active_touches:
					x = event.pos[0] / win_w
					y = event.pos[1] / win_h
					sim_event = pygame.event.Event(pygame.FINGERUP, finger_id=999, x=x, y=y, touch_id=0)
					simulated_events.extend(self.handle_finger_up(sim_event, now))
					
			# 2. Process real Finger Events
			elif event.type == pygame.FINGERDOWN:
				simulated_events.extend(self.handle_finger_down(event, now))
			elif event.type == pygame.FINGERMOTION:
				simulated_events.extend(self.handle_finger_motion(event, now))
			elif event.type == pygame.FINGERUP:
				simulated_events.extend(self.handle_finger_up(event, now))
				
			# 3. Translate Android Back Button
			elif event.type == pygame.KEYDOWN and event.key == getattr(pygame, 'K_AC_BACK', 1073742094):
				event.key = pygame.K_ESCAPE
				
		return simulated_events

	def handle_finger_down(self, event, now):
		fid = event.finger_id
		x, y = event.x, event.y
		
		self.active_touches[fid] = {
			'start_x': x,
			'start_y': y,
			'last_x': x,
			'last_y': y,
			'start_time': now,
			'moved': False,
			'hold_keys': []
		}
		
		num_active = len(self.active_touches)
		if num_active == 1:
			self.session_fingers = 1
			self.session_moved = False
			self.session_start_time = now
			self.session_start_x = x
			self.session_start_y = y
			self.session_dx = 0
			self.session_dy = 0
		else:
			if num_active > self.session_fingers:
				self.session_fingers = num_active
				
		return []

	def handle_finger_motion(self, event, now):
		fid = event.finger_id
		if fid not in self.active_touches:
			return []
			
		t = self.active_touches[fid]
		x, y = event.x, event.y
		dx = x - t['start_x']
		dy = y - t['start_y']
		
		dist = (dx**2 + dy**2)**0.5
		if dist > 0.06:
			t['moved'] = True
			self.session_moved = True
			
		t['last_x'] = x
		t['last_y'] = y
		
		self.session_dx = x - self.session_start_x
		self.session_dy = y - self.session_start_y
		
		sim_events = []
		
		# Swipe & Hold in Middle Center: Walk/Strafe (1 finger)
		if self.session_fingers == 1 and 0.35 <= self.session_start_x < 0.65 and 0.35 <= self.session_start_y < 0.65:
			for k in list(t['hold_keys']):
				sim_events.append(pygame.event.Event(pygame.KEYUP, key=k))
				t['hold_keys'].remove(k)
				
			if self.session_dy < -0.08:
				k = pygame.K_UP
				sim_events.append(pygame.event.Event(pygame.KEYDOWN, key=k, scancode=0))
				t['hold_keys'].append(k)
			elif self.session_dy > 0.08:
				k = pygame.K_DOWN
				sim_events.append(pygame.event.Event(pygame.KEYDOWN, key=k, scancode=0))
				t['hold_keys'].append(k)
				
			if self.session_dx < -0.08:
				k = pygame.K_LEFT
				sim_events.append(pygame.event.Event(pygame.KEYDOWN, key=k, scancode=0))
				t['hold_keys'].append(k)
			elif self.session_dx > 0.08:
				k = pygame.K_RIGHT
				sim_events.append(pygame.event.Event(pygame.KEYDOWN, key=k, scancode=0))
				t['hold_keys'].append(k)
				
		# Swipe & Hold in bottom part: Swipe and hold up/down for motor speed control
		elif self.session_fingers == 1 and self.session_start_y >= 0.65:
			for k in list(t['hold_keys']):
				sim_events.append(pygame.event.Event(pygame.KEYUP, key=k))
				t['hold_keys'].remove(k)
				
			if self.session_dy < -0.08:
				k = pygame.K_UP
				sim_events.append(pygame.event.Event(pygame.KEYDOWN, key=k, scancode=0))
				t['hold_keys'].append(k)
			elif self.session_dy > 0.08:
				k = pygame.K_DOWN
				sim_events.append(pygame.event.Event(pygame.KEYDOWN, key=k, scancode=0))
				t['hold_keys'].append(k)
				
		return sim_events

	def handle_finger_up(self, event, now):
		fid = event.finger_id
		if fid not in self.active_touches:
			return []
			
		t = self.active_touches[fid]
		sim_events = []
		
		for k in t['hold_keys']:
			sim_events.append(pygame.event.Event(pygame.KEYUP, key=k))
			
		del self.active_touches[fid]
		
		if len(self.active_touches) == 0:
			duration = now - self.session_start_time
			if not self.session_moved and duration < 0.35:
				sim_events.extend(self.classify_tap_gesture(self.session_start_x, self.session_start_y, now))
			elif self.session_moved:
				sim_events.extend(self.classify_swipe_gesture(self.session_start_x, self.session_start_y, self.session_dx, self.session_dy, duration))
				
		return sim_events

	def classify_tap_gesture(self, x, y, timestamp):
		sim_events = []
		
		if self.session_fingers == 2:
			self.recent_two_finger_taps = [t for t in self.recent_two_finger_taps if timestamp - t < 0.35]
			tap_count = 1
			if len(self.recent_two_finger_taps) > 0:
				tap_count += 1
			self.recent_two_finger_taps.append(timestamp)
			
			if x < 0.35 and y >= 0.65:
				if tap_count == 1:
					sim_events.extend(self.click_key(pygame.K_x))
				elif tap_count == 2:
					sim_events.extend(self.click_key(pygame.K_BACKQUOTE))
			elif x >= 0.65 and y >= 0.65:
				if tap_count == 1:
					sim_events.extend(self.click_key_with_mod(pygame.K_x, pygame.K_LSHIFT))
				elif tap_count == 2:
					sim_events.extend(self.click_key_with_mod(pygame.K_BACKQUOTE, pygame.K_LSHIFT))
			else:
				if tap_count == 1:
					sim_events.extend(self.click_key(pygame.K_v))
				elif tap_count == 2:
					sim_events.extend(self.click_key(pygame.K_b))
					
		elif self.session_fingers == 1:
			self.recent_taps = [t for t in self.recent_taps if timestamp - t[2] < 0.35]
			tap_count = 1
			for rx, ry, rt in self.recent_taps:
				dist = ((x - rx)**2 + (y - ry)**2)**0.5
				if dist < 0.1:
					tap_count += 1
			self.recent_taps.append((x, y, timestamp))
			
			if 0.35 <= x < 0.65 and 0.35 <= y < 0.65:
				if tap_count == 1:
					sim_events.extend(self.click_key(pygame.K_c))
				elif tap_count == 2:
					sim_events.extend(self.click_key(pygame.K_RETURN))
				elif tap_count == 3:
					sim_events.extend(self.click_key_with_mod(pygame.K_RETURN, pygame.K_LSHIFT))
			elif 0.35 <= x < 0.65 and y < 0.35:
				if tap_count == 1:
					sim_events.extend(self.click_key(pygame.K_h))
				elif tap_count == 2:
					sim_events.extend(self.click_key(pygame.K_o))
			elif x >= 0.65 and 0.35 <= y < 0.65:
				if tap_count == 1:
					sim_events.extend(self.click_key_with_mod(pygame.K_z, pygame.K_LALT))
				elif tap_count == 2:
					sim_events.extend(self.click_key(pygame.K_e))
				elif tap_count == 3:
					sim_events.extend(self.click_key(pygame.K_p))
			elif x < 0.35 and y < 0.35:
				if tap_count == 1:
					sim_events.extend(self.click_key(pygame.K_TAB))
				elif tap_count == 2:
					sim_events.extend(self.click_key(pygame.K_z))
				elif tap_count == 3:
					sim_events.extend(self.click_key(pygame.K_n))
			elif x < 0.35 and y >= 0.65:
				sim_events.extend(self.click_key(pygame.K_LCTRL))
			elif x >= 0.65 and y >= 0.65:
				sim_events.extend(self.click_key(pygame.K_RCTRL))
			elif 0.35 <= x < 0.65 and y >= 0.65:
				sim_events.extend(self.click_key(pygame.K_SPACE))
			elif x < 0.35 and 0.35 <= y < 0.65:
				sim_events.extend(self.click_key_with_mod(pygame.K_x, pygame.K_LALT)) # Alt + X for crouch/duck

		return sim_events

	def classify_swipe_gesture(self, start_x, start_y, dx, dy, duration):
		sim_events = []
		abs_dx = abs(dx)
		abs_dy = abs(dy)
		
		if self.session_fingers == 3:
			if abs_dx > abs_dy and abs_dx > 0.08:
				if dx < 0:
					sim_events.extend(self.click_key(pygame.K_LEFTBRACKET))
				else:
					sim_events.extend(self.click_key(pygame.K_RIGHTBRACKET))
			elif abs_dy > abs_dx and abs_dy > 0.08:
				if dy < 0:
					sim_events.extend(self.click_key(pygame.K_COMMA))
				else:
					sim_events.extend(self.click_key(pygame.K_PERIOD))
					
		elif self.session_fingers == 2:
			if abs_dy > abs_dx and abs_dy > 0.08:
				if dy > 0:
					self.show_action_menu()
				else:
					sim_events.extend(self.click_key(pygame.K_F2))
			elif abs_dx > abs_dy and abs_dx > 0.08:
				if dx < 0:
					sim_events.extend(self.click_key(pygame.K_LEFT))
				else:
					sim_events.extend(self.click_key(pygame.K_RIGHT))
					
		elif self.session_fingers == 1:
			if abs_dx > abs_dy and abs_dx > 0.08:
				if dx < 0:
					if start_y < 0.33:
						sim_events.extend(self.click_key(pygame.K_1))
					elif start_x < 0.35 and start_y >= 0.65:
						sim_events.extend(self.click_key_with_mod(pygame.K_SPACE, pygame.K_LSHIFT))
					elif start_x >= 0.65 and start_y >= 0.65:
						sim_events.extend(self.click_key_with_mod(pygame.K_SPACE, pygame.K_LALT))
				else:
					if start_y < 0.33:
						sim_events.extend(self.click_key(pygame.K_2))
					elif start_x < 0.35 and start_y >= 0.65:
						sim_events.extend(self.click_key_with_mod(pygame.K_LCTRL, pygame.K_LSHIFT))
					elif start_x >= 0.65 and start_y >= 0.65:
						sim_events.extend(self.click_key_with_mod(pygame.K_RCTRL, pygame.K_LSHIFT))
			elif abs_dy > abs_dx and abs_dy > 0.08:
				if dy < 0:
					if start_x < 0.35 and 0.33 <= start_y < 0.66:
						sim_events.extend(self.click_key(pygame.K_m))
					elif start_x >= 0.65 and start_y < 0.33:
						sim_events.extend(self.click_key(pygame.K_UP))
					elif start_y >= 0.65:
						sim_events.extend(self.click_key(pygame.K_r))
					elif start_y < 0.5:
						sim_events.extend(self.click_key(pygame.K_PAGEUP))
				else:
					if start_x < 0.35 and 0.33 <= start_y < 0.66:
						sim_events.extend(self.click_key_with_mod(pygame.K_m, pygame.K_LSHIFT))
					elif start_x >= 0.65 and start_y < 0.33:
						sim_events.extend(self.click_key(pygame.K_DOWN))
					elif start_y < 0.5:
						sim_events.extend(self.click_key(pygame.K_PAGEDOWN))
						
		return sim_events

	def show_action_menu(self):
		if hasattr(g, "action_menu_open") and g.action_menu_open:
			return
		g.action_menu_open = True
		try:
			import menu
			m = menu.menu("Action Menu")
			m.add("Friend Menu", "friend")
			m.add("Player Menu", "player")
			m.add("Language Channel Menu", "langchan")
			m.add("Group Chat", "group")
			m.add("Community Chat", "community")
			m.add("Map Chat", "map")
			m.add("Team Chat", "team")
			res = m.show()
			if res == "friend":
				pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F5, scancode=0))
				pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_F5, scancode=0))
			elif res == "player":
				pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F6, scancode=0))
				pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_F6, scancode=0))
			elif res == "langchan":
				pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F11, scancode=0))
				pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_F11, scancode=0))
			elif res == "group":
				pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_QUOTE, scancode=0))
				pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_QUOTE, scancode=0))
			elif res == "community":
				pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_QUOTE, scancode=0))
				pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LSHIFT, scancode=0))
				pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_QUOTE, scancode=0))
				pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_LSHIFT, scancode=0))
			elif res == "map":
				pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SLASH, scancode=0))
				pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_SLASH, scancode=0))
			elif res == "team":
				pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_j, scancode=0))
				pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_j, scancode=0))
		except Exception as e:
			print(f"[Mobile Action Menu Error] {e}")
		finally:
			g.action_menu_open = False

	def click_key(self, key):
		return [
			pygame.event.Event(pygame.KEYDOWN, key=key, scancode=0),
			pygame.event.Event(pygame.KEYUP, key=key, scancode=0)
		]

	def click_key_with_mod(self, key, mod):
		return [
			pygame.event.Event(pygame.KEYDOWN, key=mod, scancode=0),
			pygame.event.Event(pygame.KEYDOWN, key=key, scancode=0),
			pygame.event.Event(pygame.KEYUP, key=key, scancode=0),
			pygame.event.Event(pygame.KEYUP, key=mod, scancode=0)
		]

gesture_processor = TouchGestureProcessor()

def process_events():
	global current_key_pressed, current_key_released
	try:
		import fmod_audio
		if getattr(fmod_audio, "initialized", False):
			fmod_audio.update_fmod()
	except Exception:
		pass
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

	# Process touch gestures
	try:
		simulated = gesture_processor.process_pygame_events(events)
		if simulated:
			events.extend(simulated)
	except Exception as ex:
		print(f"Error in gesture_processor: {ex}")

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
			if sys.platform == "win32":
				ctypes.windll.kernel32.ExitProcess(0)
			else:
				sys.exit(0)
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