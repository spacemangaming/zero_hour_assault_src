from menu_system import menu
import time
from variable_management import string_split
import pygame
from cid import generate_computer_id
from variable_management import string_replace
from speech import speak
from network import event_receive

from network import event_connect
from variable_management import string_contains
from timer import timer
import globals as g
from input import get_input
import updater
import requests
#netaddress=requests.get("https://nbmstudios.com/zero_hour_assault/ip.txt").text
netport=55918
netaddress="0user"
m=menu()
peer_id=0
connectiontimer=timer()
connectiontime=10000
from dlg import dlg
import menu
from events import process_events, key_pressed
from pygame.locals import *
from map import load_map
import sys
g.compid=generate_computer_id()
def login():
	try:
		updater.check()
	except: pass
	if(g.name=="" or g.password=="") or g.savemail=="":
	
		dlg("An account is not established. Please set up or create an account if you have one.")
		menu.login_settings()
		
	connectiontimer.restart()
	g.n.setup_client(100, 100)
	g.n.connect(netaddress,netport)
	speak("connecting to the server, please wait...")
	while(True):
		process_events()
		g.e=g.n.request()
		if (key_pressed(K_ESCAPE)):
		
			menu.login_settings()
			
		if(connectiontimer.elapsed>connectiontime and g.connected==False):
		
			speak("The server is currently not active. An attempt will be made to connect to the server again within 10 seconds. If this persists further, please contact the developers.")
			connectiontimer.restart()
			g.delay(10000)
			login()
#			menu.login_settings()
			
		if(g.e.type==event_connect):
		
			g.peer_id=g.e.peer_id
			g.n.send_reliable(0,"zero"*4,0)
			g.n.send_reliable(0, "login "+g.name+" "+g.password+" "+g.savemail+" "+g.compid,0)
			g.connected=True
			speak("Logging in ...")
		elif g.e.type == event_receive and g.e.message.startswith("banned"):
			dlg(g.e.message.replace("banned ",""))
			menu.login_settings()		
		elif g.e.type == event_receive and g.e.message=="verifyincorrect":
			dlg("Invalid code")
			menu.login_settings()		
		elif g.e.type == event_receive and g.e.message=="verifycorrect":
			speak("Logging in ...")
			g.n.send_reliable(0, "login "+g.name+" "+g.password+" "+g.savemail+" "+g.compid,0)
		elif g.e.type == event_receive and g.e.message=="verify":	
			m.reset(True)
			menu.setupmenu()
			m.add_item_tts("Yes","yes")
			m.add_item_tts("No","no")
			m.callback2=netdummy
			mres=m.run("You have tried to log into this account from a different computer than the one in which it is created. To be sure you are indeed the owner, we will send an verification code to the email address you wrote when creating this account. Please enter the code you received, to authorize this computer. After you authorize this computer, you can log into your account from this computer and all your other authorized computers. You can later on remove the authorization from the game menu from any of the your authorized computers. Do you want to authorize this computer?")
			if m.get_item_name(mres)=="yes":
				g.n.send_reliable(0,"sendverify "+g.name,0)
				code=get_input("Please enter the code sent to your mail.")
				if code=="":
					dlg("Code cannot be blank")
					menu.login_settings()		
				g.n.send_reliable(0,"verifycode "+g.name+" "+code+" "+g.compid,0)
				speak("Verifying code ...")
			else: menu.login_settings()
		elif g.e.type == event_receive and g.e.message.startswith("message"):
			dlg(g.e.message.replace("message ",""))
			menu.login_settings()		
	

		elif(g.e.type==event_receive and g.e.message=="loggedin"):
		
			m.kill_music()
			g.game()
			
		elif(g.e.type==event_receive and g.e.message=="alreadyin"):
		
			dlg("This user is already loged in")
			menu.login_settings()
			
		elif(g.e.type==event_receive and g.e.message=="doesnotexist"):
		
			dlg("No such account exists.")
			menu.login_settings()
			
		elif(g.e.type==event_receive and g.e.message=="wrongpass"):
		
			dlg("The password provided for this account is not correct")
			menu.login_settings()
			
		elif(g.e.type==event_receive and g.e.message=="wrongmail"):
		
			dlg("The eMail provided for this account is not correct")
			menu.login_settings()
			

		elif(g.e.type==event_receive and g.e.message=="oldver"):
		
			dlg("Your version is an old version. Please re-download the game from the website.")
			menu.login_settings()
			
		elif(g.e.type==event_receive and g.e.message=="banned"):
		
			dlg("You are currently banned from the game please try again later")
			menu.login_settings()
			
		elif(g.e.type==event_receive and string_contains(g.e.message,"banned",1)>-1):
		
			dlg("you only have right to create one account per computer")
			menu.login_settings()
			

		elif(g.e.type==event_receive):
		
			parsed=string_split(g.e.message, " ", False)
			if(parsed[0]=="x"):
			
				g.me.x=float(parsed[1])
				
			elif(parsed[0]=="y"):
			
				g.me.y=float(parsed[1])
				
			elif(parsed[0]=="z"):
			
				g.me.z=float(parsed[1])
				
			elif(parsed[0]=="mapdata"):
			
				load_map(string_replace(g.e.message, "mapdata ", "", False))
				#g.mapready=True
			elif(parsed[0]=="facing"):
			
				g.facing=int(parsed[1])
				
			
		
	
def create():
	g.creating=False
	user=get_input("Enter the username you would like. No spaces.")
	mail=get_input("Please enter a valid email address. If you enter an incorrect e-mail address, you will have no chance of recovering your account. No spaces.")
	cmail=get_input("Retype the mail. If you enter an incorrect e-mail address, you will have no chance of recovering your account. No spaces.")
	passwd=get_input("Enter the password you would like. No spaces.")
	cpasswd=get_input("Retype the password. No spaces.")
	m.reset(True)
	menu.setupmenu()
	m.add_item_tts("Male", "Male")
	m.add_item_tts("Female", "Female")
	mres=m.run("Choose a gender for your character.", True)
	gender=m.get_item_name(mres)
	if user == "":
		dlg("Username cannot be empty.")
		menu.login_settings()
	elif " " in user:
		dlg("Username cannot contain spaces.")
		menu.login_settings()
	elif mail == "":
		dlg("Email cannot be empty.")
		menu.login_settings()
	elif " " in mail:
		dlg("Email cannot contain spaces.")
		menu.login_settings()
	elif "@" not in mail:
		dlg("Email must contain '@' symbol.")
		menu.login_settings()
	elif cmail == "":
		dlg("Please confirm your email.")
		menu.login_settings()
	elif cmail != mail:
		dlg("Email confirmation does not match.")
		menu.login_settings()
	elif passwd == "":
		dlg("Password cannot be empty.")
		menu.login_settings()
	elif " " in passwd:
		dlg("Password cannot contain spaces.")
		menu.login_settings()
	elif cpasswd == "":
		dlg("Please confirm your password.")
		menu.login_settings()
	elif " " in cpasswd:
		dlg("Password confirmation cannot contain spaces.")
		menu.login_settings()
	elif cpasswd != passwd:
		dlg("Password confirmation does not match.")
		menu.login_settings()
	elif gender == "":
		dlg("Please select your gender.")
		menu.login_settings()
	connectiontimer.restart()
	g.n.setup_client(100, 100)
	g.n.connect(netaddress,netport)
	while(True):
		process_events()
		g.e=g.n.request()
		if(connectiontimer.elapsed>connectiontime and g.creating==False):
		
			dlg("Error, Server lost")
			menu.login_settings()
			
		if key_pressed(K_ESCAPE):
			menu.login_settings()
		if(g.e.type==event_connect and g.creating==False):
		
			g.creating=True
			speak("Creating account")

			g.peer_id=g.e.peer_id
			g.n.send_reliable(0,"zero"*4,0)
			g.n.send_reliable(0,"create "+user+" "+passwd+" "+mail+" "+gender+" "+g.compid,0)
		if g.e.type == event_receive and g.e.message.startswith("banned"):
			dlg(g.e.message.replace("banned ",""))
			menu.login_settings()
		if g.e.type == event_receive and g.e.message.startswith("message"):
			dlg(g.e.message.replace("message ",""))
			menu.login_settings()

		elif(g.e.type==event_receive and g.e.message=="alreadyexists"):

			dlg("This account is exist")
			menu.login_settings()

		elif(g.e.type==event_receive and g.e.message=="created"):

			g.p.play_stationary("success.ogg",False)
			dlg("done! Account created successfully. Please press enter to log in")
			g.delay(1000)
			g.name=user
			g.password=passwd
			g.savemail=mail
			g.writeprefs()
			g.creating=False
			login()
			
		
	
def netdummy():
	try: g.n.request()
	except: pass