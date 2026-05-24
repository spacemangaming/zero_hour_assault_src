import globals as g
from speech import speak
from random import randint as random

from input import get_input
from events import key_down
from pygame.locals import *
def give(item, amount):
	a=0
	if (not item in g.inv):
	
		g.inv[item]=amount
		
	else:
	
		a=g.inv[item]
		if (a+amount<=0):
			del g.inv[item]
		else:
			g.inv[item]=a+amount
		
	
def cycle_inv(direction=1):
	if g.mapname=="jail": return
	if g.died: return
	found = False
	
	for item in g.inv.keys():
		if is_item_on_current_category(item):
			found = True
			break
	
	if not found and alt_is_down():
		speak("No items on this category")
		return

	if g.watching != "":
		return
	
	while True:
		g.invpos += direction if direction == 1 else -1
		if g.invpos >= len(g.inv):
			g.invpos = 0
		elif g.invpos < 0:
			g.invpos = len(g.inv) - 1

		if not alt_is_down(): break

		if is_item_on_current_category(list(g.inv.keys())[g.invpos]):
			break
	
	if len(g.inv) > 0:
		item_name = list(g.inv.keys())[g.invpos]
		item_count = g.inv[item_name]
		pos = g.invpos + 1
		speak(f"{item_name}: {item_count}.")
		g.p.play_stationary("category"+str(random(1,6))+".ogg", False)
		g.n.send_reliable(0,"xplay category"+str(random(1,6))+"",0)
	else:
		speak("No items")

def useitem():
	try:
		if len (g.inv)>0: g.n.send_reliable(0, "useitem "+list(g.inv.keys())[g.invpos], 0)
	except: pass
def set_favoriitem():
	try:
		if len (g.inv)>0:
			if g.favoriitem==list(g.inv.keys())[g.invpos]:
				speak("This item is already your favorite item. Please select another item")
			else:
				g.favoriitem=""+list(g.inv.keys())[g.invpos]
				speak(list(g.inv.keys())[g.invpos]+" item Added as your favorite item.")
				g.p.play_stationary("misc53.ogg",False)
	except: pass
	g.writeprefs()
def set_favoriitem2():
	try:
		if len (g.inv)>0:
			if g.favoriitem2==list(g.inv.keys())[g.invpos]:
				speak("This item is already your favorite item. Please select another item")
			else:
				g.favoriitem2=""+list(g.inv.keys())[g.invpos]
				speak(list(g.inv.keys())[g.invpos]+" item Added as your favorite item.")
				g.p.play_stationary("misc53.ogg",False)
	except: pass
	g.writeprefs()
def dropitem(item="",require_amount=False):
	if item=="":
		if len (g.inv)>0:
			try: item=list(g.inv.keys())[g.invpos]
			except: return

	if not require_amount: g.n.send_reliable(0, "dropitem "+item, 0)
	else:
		amount=get_input("How many "+item+" do you want to drop?")
		if not amount.isdigit(): speak("Error, you need to enter a number."); return
		amount=int(amount)
		if get_item_count(item)<amount: speak("You don't have "+str(amount)+" "+item+"!"); return
		g.n.send_reliable(0, "dropitemamount "+item+" "+str(amount), 0)


def count_total_items():
	amount=0
	for i in range(len(g.inv.keys)):
		a=0
		a=g.inv.keys()[i]
		amount+=a
		
	return amount
	
def get_item_count(item):
	
	if not item in g.inv:
		
		return 0
			
	ret=0
	ret=g.inv[item]
	if(ret<0):
		
		del g.inv[item]
		return 0
			
	return ret
		
def is_item_on_current_category(item):
	for cat in list(g.invcategories.keys()):
		if g.invcategory == cat and item in g.invcategories[cat]: return True
	return False
def alt_is_down():
	if key_down(K_LALT) or key_down(K_RALT):
		return True
	return False

