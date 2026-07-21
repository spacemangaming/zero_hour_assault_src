from file_directories import file_exists, file_put_contents
from random import randint as random
import globals as g
from speech import speak
from Miscellaneous import clipboard_copy_text
from constants import DIRECTORY_APPDATA
import pickle
from translation import google_translate
from threading import Thread
from input import get_input
from timer import timer

class buffer:
	def __init__(self,n):
		self.pos=0
		self.muted=False
		self.name=""
		self.items=[]
		self.item_ids=[]
		self.item_timers={}

		self.name=n


def create_buffer(bname, snd=""):
	for b in g.buffers:
		if b.name==bname: return
	b1=buffer(bname)
	g.buffers.append(b1)

def firstbuffer():
	g.bufferpos=0
	progress_pitch_and_pan(g.bpos, g.bufferpos, len(g.buffers),False)
	speakfocusedbuffer()

def lastbuffer():
	g.bufferpos=len(g.buffers)-1
	progress_pitch_and_pan(g.bpos, g.bufferpos, len(g.buffers),False)
	speakfocusedbuffer()

def bufferleft():
	if (g.bufferpos<=0):

		g.bufferpos=0
		progress_pitch_and_pan(g.bpos, g.bufferpos, len(g.buffers),False)
		speakfocusedbuffer()

	else:

		g.bufferpos-=1
		progress_pitch_and_pan(g.bpos, g.bufferpos, len(g.buffers),False)
		speakfocusedbuffer()

def bufferright():
	if (g.bufferpos>=(len(g.buffers)-1)):

		if (len(g.buffers)>0):
			g.bufferpos=len(g.buffers)-1
		progress_pitch_and_pan(g.bpos, g.bufferpos, len(g.buffers),False)
		speakfocusedbuffer()

	else:

		g.bufferpos+=1
		progress_pitch_and_pan(g.bpos, g.bufferpos, len(g.buffers),False)
		speakfocusedbuffer()


def nextbufferitem():
	if g.buffers[g.bufferpos].pos<(len(g.buffers[g.bufferpos].items)-1):

		g.buffers[g.bufferpos].pos+=1
		progress_pitch_and_pan(g.bnext, g.buffers[g.bufferpos].pos, len(g.buffers[g.bufferpos].items))
		if not hasattr(g.buffers[g.bufferpos],"item_timers"): g.buffers[g.bufferpos].item_timers={}
		if g.buffers[g.bufferpos].item_ids[g.buffers[g.bufferpos].pos] not in g.buffers[g.bufferpos].item_timers: speak(g.buffers[g.bufferpos].items[g.buffers[g.bufferpos].pos])
		if g.buffers[g.bufferpos].item_ids[g.buffers[g.bufferpos].pos] in g.buffers[g.bufferpos].item_timers:
			speak(
				g.buffers[g.bufferpos].items[g.buffers[g.bufferpos].pos] +
				", " +
				(ms_to_readable_time(g.buffers[g.bufferpos].item_timers[g.buffers[g.bufferpos].item_ids[g.buffers[g.bufferpos].pos]].elapsed) + " ago.").replace("Just now ago.","Just now.")
			)


def prevbufferitem():
	if (g.buffers[g.bufferpos].pos>0):

		g.buffers[g.bufferpos].pos-=1
		progress_pitch_and_pan(g.bnext, g.buffers[g.bufferpos].pos, len(g.buffers[g.bufferpos].items))
		if not hasattr(g.buffers[g.bufferpos],"item_timers"): g.buffers[g.bufferpos].item_timers={}
		if g.buffers[g.bufferpos].item_ids[g.buffers[g.bufferpos].pos] not in g.buffers[g.bufferpos].item_timers: speak(g.buffers[g.bufferpos].items[g.buffers[g.bufferpos].pos])
		if g.buffers[g.bufferpos].item_ids[g.buffers[g.bufferpos].pos] in g.buffers[g.bufferpos].item_timers:
			speak(
				g.buffers[g.bufferpos].items[g.buffers[g.bufferpos].pos] +
				". " + # Dikkat: nextbufferitem'da "," vardı, burada "." var, orijinaline sadık kalındı.
				(ms_to_readable_time(g.buffers[g.bufferpos].item_timers[g.buffers[g.bufferpos].item_ids[g.buffers[g.bufferpos].pos]].elapsed) + " ago.").replace("Just now ago.","Just now.")
			)



def topbufferitem():
	if (len(g.buffers[g.bufferpos].items)>0):

		g.buffers[g.bufferpos].pos=0
		progress_pitch_and_pan(g.bnext, g.buffers[g.bufferpos].pos, len(g.buffers[g.bufferpos].items))
		if not hasattr(g.buffers[g.bufferpos],"item_timers"): g.buffers[g.bufferpos].item_timers={}
		if g.buffers[g.bufferpos].item_ids[g.buffers[g.bufferpos].pos] not in g.buffers[g.bufferpos].item_timers: speak(g.buffers[g.bufferpos].items[g.buffers[g.bufferpos].pos])
		if g.buffers[g.bufferpos].item_ids[g.buffers[g.bufferpos].pos] in g.buffers[g.bufferpos].item_timers:
			speak(
				g.buffers[g.bufferpos].items[g.buffers[g.bufferpos].pos] +
				". " +
				(ms_to_readable_time(g.buffers[g.bufferpos].item_timers[g.buffers[g.bufferpos].item_ids[g.buffers[g.bufferpos].pos]].elapsed) + " ago.").replace("Just now ago.","Just now.")
			)



def bottombufferitem():
	if (len(g.buffers[g.bufferpos].items)>0):

		g.buffers[g.bufferpos].pos = (len(g.buffers[g.bufferpos].items) - 1)
		progress_pitch_and_pan(g.bnext, g.buffers[g.bufferpos].pos, len(g.buffers[g.bufferpos].items))
		if not hasattr(g.buffers[g.bufferpos],"item_timers"): g.buffers[g.bufferpos].item_timers={}
		if g.buffers[g.bufferpos].item_ids[g.buffers[g.bufferpos].pos] not in g.buffers[g.bufferpos].item_timers: speak(g.buffers[g.bufferpos].items[g.buffers[g.bufferpos].pos])
		if g.buffers[g.bufferpos].item_ids[g.buffers[g.bufferpos].pos] in g.buffers[g.bufferpos].item_timers:
			speak(
				g.buffers[g.bufferpos].items[g.buffers[g.bufferpos].pos] +
				". " +
				(ms_to_readable_time(g.buffers[g.bufferpos].item_timers[g.buffers[g.bufferpos].item_ids[g.buffers[g.bufferpos].pos]].elapsed) + " ago.").replace("Just now ago.","Just now.")
			)


def copy_buffer_item():
	if len(g.buffers[g.bufferpos].items)>0:
		clipboard_copy_text(g.buffers[g.bufferpos].items[g.buffers[g.bufferpos].pos])
def translate_buffer_item():
	if len(g.buffers[g.bufferpos].items)>0:
		def func():
			translation=google_translate(g.buffersourcelang, g.buffertargetlang, g.buffers[g.bufferpos].items[g.buffers[g.bufferpos].pos])
			if translation is None: speak("No language selected for translation"); return
			speak(translation)


		Thread(target=func).start()


def add_buffer_item(buffername,item, snd=""):
	if g.bufferlog==1:
		if file_exists("log.txt")==False:
			f=open("log.txt","w",encoding="utf-8")
		f=open("log.txt","a",encoding="utf-8")
		f.write("the message has been added as in "+buffername+" buffer, the text is: "+item+"\n")
		f.close()
	for i in range(len(g.buffers)):

		if (g.buffers[i].name==buffername or g.buffers[i].name=="all"):

			if (g.buffers[i].name!="all"):


				if not g.buffers[i].muted: speak(item)
				g.buffers[i].items.append(item)
				itemid=randomstring()
				g.buffers[i].item_ids.append(itemid)
				if not hasattr(g.buffers[i],"item_timers"): g.buffers[i].item_timers={}
				g.buffers[i].item_timers[itemid]=timer()

			if (g.buffers[i].name=="all"):
				itemid=randomstring()
				g.buffers[i].items.append(item)
				g.buffers[i].item_ids.append(itemid)
				if not hasattr(g.buffers[i],"item_timers"): g.buffers[i].item_timers={}
				g.buffers[i].item_timers[itemid]=timer()



	file_put_contents(g.appdata_dir+"/buffers3.dat",pickle.dumps(g.buffers),"wb")

def speakfocusedbuffer():
	if (len(g.buffers[g.bufferpos].items)>0):
		speak(g.buffers[g.bufferpos].name+"."+" "+str(len(g.buffers[g.bufferpos].items)))
	else:
		speak(g.buffers[g.bufferpos].name+"."+" Empty.")

def find_buffer(name) :
	for i in range(len(g.buffers)):
		if (g.buffers[i].name==name):
			return i
	return -1
def progress_pan(handle, current, max):
	handle.pan = (current * 200 / max) - 100
	handle.play()  # Play the sound after setting properties

def progress_pitch(handle, current, max):
	handle.pitch = (current * 200 / max)
	handle.play()  # Play the sound after setting properties

def progress_pitch_and_pan(handle, current, max, change_pitch=True):

	if handle.player.playing(): handle.stop()
	handle.player.alhrtf=True
	handle.set_3dposition(((current * 200 / max) - 100) / 10, 10, 0)
	handle.player.rolloff = 0.1

	handle.play()  # Play the sound after setting properties

from concurrent.futures import ThreadPoolExecutor

def quote():
	name = g.buffers[g.bufferpos].name
	try:
		item = g.buffers[g.bufferpos].items[g.buffers[g.bufferpos].pos]
	except:
		return

	if name not in ["General_Chats", "map messages", "group messages", "team messages", "admin messages"]:
		speak("You cannot quote messages in this buffer")
		return

	message = get_input("enter reply")
	if message == "":
		return

	def send_message(translated_message):
		if translated_message is None: speak("No language selected for translation"); return
		mess = item
		if name == "General_Chats":
			g.n.send_reliable(0, translated_message + ". Quoted message: " + mess, 1)
		elif name == "map messages":
			g.n.send_reliable(0, "mapmessage " + translated_message + ". Quoted message: " + mess, 0)
		elif name == "group messages":
			g.n.send_reliable(0, "groupmessage " + translated_message + ". Quoted message: " + mess, 0)
		elif name == "team messages":
			g.n.send_reliable(0, "teammessage " + translated_message + ". Quoted message: " + mess, 0)
		elif name == "admin messages":
			g.n.send_reliable(0, "admchat " + translated_message + ". Quoted message: " + mess, 0)

	if g.should_translate:
		with ThreadPoolExecutor() as executor:
			future = executor.submit(google_translate, g.sendsourcelang, g.sendtargetlang, message)
			future.add_done_callback(lambda fut: send_message(fut.result()))
	else:
		send_message(message)
import math

def ms_to_readable_time(milliseconds):
	milliseconds = math.floor(milliseconds)
	seconds = math.floor((milliseconds / 1000) % 60)
	minutes = math.floor((milliseconds / (1000 * 60)) % 60)
	hours = math.floor((milliseconds / (1000 * 60 * 60)) % 24)
	days = math.floor(milliseconds / (1000 * 60 * 60 * 24))

	# Just now kontrolü
	if days == 0 and hours == 0 and minutes == 0 and seconds == 0:
		return "Just now"

	time_components = []

	if days >= 365:
		years = days // 365
		time_components.append(f"{years} {plural(years, 'year', 'years')}")
		days %= 365

	if days >= 30:
		months = days // 30
		time_components.append(f"{months} {plural(months, 'month', 'months')}")
		days %= 30

	if days >= 7:
		weeks = days // 7
		time_components.append(f"{weeks} {plural(weeks, 'week', 'weeks')}")
		days %= 7

	if days > 0:
		time_components.append(f"{days} {plural(days, 'day', 'days')}")

	if hours > 0:
		time_components.append(f"{hours} {plural(hours, 'hour', 'hours')}")

	if minutes > 0:
		time_components.append(f"{minutes} {plural(minutes, 'minute', 'minutes')}")

	if seconds > 0:
		time_components.append(f"{seconds} {plural(seconds, 'second', 'seconds')}")

	return ", ".join(time_components)
def plural(n, singular, plural):
	if n == 1:
		return singular
	return plural
def randomstring(length=10):
	temp="abcdefghijklmnopqrstuvwxyz1234567890"
	ret=""
	for i in range(length):
		ret=ret+temp[random(0, (len(temp)-1))]
	return ret