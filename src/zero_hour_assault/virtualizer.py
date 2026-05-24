from variable_management import string_contains
from variable_management import string_is_upper_case
from events import process_events
from events import key_down
from pygame.locals import *
from events import key_pressed
from variable_management import string_left
from variable_management import get_characters
from speech import speak
from sound import sound
from Miscellaneous import clipboard_copy_text, clipboard_read_text
import globals as g
class virtualizer:
	def input(self, text, online=True, secure=False):
		self.charrepeat=1
		self.capmode=1
	
		cursor=0
		message=""
		capbeep=sound()
		capbeep.load("cap.ogg")
		speak(text)
		cursor=0
		ms=[]
		get_characters()
		while(True):
		
			process_events()
			if(online):
				g.mainloop()
			char=string_left(get_characters(), 1)
			if(key_pressed(K_TAB)):
			
				speak(text)
				
			if(key_down(K_LSHIFT) or key_down(K_RSHIFT)):
			
				if(key_pressed(K_BACKSPACE)):
				
					ms.clear()
					cursor=0
					speak("Text cleared")
					
				
			if (key_down(K_LCTRL) or key_down(K_RCTRL)):
			
				if (key_pressed(K_v)):
				
					if(secure):
					
						speak("You may not paste text into secure input boxes!")
						
					else:
					
						speak("text pasted")
						cl=clipboard_read_text()
						for i in range(len(cl)):
						
							ms.insert(cursor,cl[i])
							cursor+=1
							
						
					
				if (key_pressed(K_c)):
				
					if(secure):
					
						speak("You may not copy text from secure input boxes!")
						
					else:
					
						a=""
						for i in range(len(ms)):
						
							a+=ms[i]
							
						speak("text copied")
						clipboard_copy_text(a)
						
					
				
			if (key_pressed(K_F2)) :
				if (self.capmode==0) :
					self.capmode=1
					speak("Beep for capital letters")
					
				elif (self.capmode==1) :
					self.capmode=2
					speak("Say “cap” in front of the capital letters")
					
				else :
					self.capmode=0
					speak("Treat capital letters no different.")
					
				
			if (key_pressed(K_F1)):
			
				if (self.charrepeat==1):
				
					speak("character repeat off")
					self.charrepeat=0
					
				else:
				
					speak("character repeat on")
					self.charrepeat=1
					
				
			if(char!=""):
			
				if (self.charrepeat==1):
				
					if (string_is_upper_case(char)):
						if (self.capmode==1) :
							capbeep.stop();
							capbeep.play()
							speak("*" if secure==True else char)
							
						elif (self.capmode==2):
							speak("Cap "+"*" if secure==True else char)
						else:
							speak("*" if secure==True else char)
						
					elif(string_contains(char, " ", 1)>-1):
					
						speak("*" if secure==True else "Space")
						
					else:
					
						speak("*" if secure==True else char)
						
					
				ms.insert(cursor,char)
				cursor+=1
				
			if(key_pressed(K_BACKSPACE) and len(ms) > 0 and cursor>=1):
			
				if(online):
					g.n.send_reliable(0,"playsnd keytype_delete.ogg",0)
				else:
					g.p.play_stationary("keytype_delete.ogg",False)
				char=ms[cursor-1]
				if (char==" "):
					speak("*" if secure==True else "space")
				else :
					if (string_is_upper_case(char)) :
						if (self.capmode==1) :
							capbeep.stop();
							capbeep.play()
							speak("*" if secure==True else char)
							
						elif (self.capmode==2):
							speak("Cap "+"*" if secure==True else char)
						else:
							speak("*" if secure==True else char)
						
					else:
						speak("*" if secure==True else char)
					
				ms.remove(ms[cursor-1])
				cursor-=1
				
			if(key_pressed(K_DELETE) and len(ms) > 0 and cursor>0 and cursor<len(ms)):
			
				if(online):
					g.n.send_reliable(0,"playsnd keytype_delete.ogg",0)
				else:
					g.p.play_stationary("keytype_delete.ogg",False)
				char=ms[cursor+1]
				if (char==" "):
					speak("*" if secure==True else "space")
				else :
					if (string_is_upper_case(char)) :
						if (self.capmode==1) :
							capbeep.stop();
							capbeep.play()
							speak("*" if secure==True else char)
							
						elif (self.capmode==2):
							speak("cap"+("*" if secure==True else char))
						else:
							speak("*" if secure==True else char)
						
					else:
						speak("*" if secure==True else char)
					
				ms.remove(ms[cursor+1])
				
			if(key_pressed(K_DOWN) or key_pressed(K_UP)):
			
				if(secure==True):
				
					speak(str(len(ms))+" *")
					
				else:
				
					a=""
					for i in range(len(ms)):
					
						a+=ms[i]
						
					speak(a)
					
				
			if(key_pressed(K_LEFT) and cursor>0):
			
				if(len(ms)>0):
				
					cursor-=1
					if (cursor>=len(ms)):
					
						speak("Blank")
						
					elif (ms[cursor]==" "):
						speak("*" if secure==True else "space")
					else:
					
						if (string_is_upper_case(ms[cursor])) :
							if (self.capmode==1) :
								capbeep.stop();
								capbeep.play()
								speak("*" if secure==True else ms[cursor])
								
							elif (self.capmode==2):
								speak("Cap " + ("*" if secure else ms[cursor]))
							else:
								speak("*" if secure else ms[cursor])
						else:
							speak("*" if secure else ms[cursor])
			if(key_pressed(K_RIGHT) and cursor<len(ms)):
			
				if(len(ms) > 0):
				
					cursor+=1
					if (cursor>=len(ms)):
						speak("Blank")
					elif (ms[cursor]==" "):
						speak("*" if secure else "space")
					else:
					
						if (string_is_upper_case(ms[cursor])) :
							if (self.capmode==1) :
								capbeep.stop();
								capbeep.play()
								speak("*" if secure else ms[cursor])
								
							elif (self.capmode==2):
								speak("cap"+("*" if secure else ms[cursor]))
							else:
								speak("*" if secure else ms[cursor])
							
						else:
							speak("*" if secure else ms[cursor])
						
					
				else:
					speak("blank")
				
			if(key_pressed(K_HOME)):
			
				if(len(ms) > 0):
				
					cursor=0
					if (cursor>=len(ms)):
						speak("Blank")
					elif (ms[cursor]==" "):
						speak("*" if secure else "space")
					else:
					
						if (string_is_upper_case(ms[cursor])) :
							if (self.capmode==1) :
								capbeep.stop();
								capbeep.play()
								speak("*" if secure else ms[cursor])
								
							elif (self.capmode==2):
								speak("cap"+("*" if secure else ms[cursor]))
							else:
								speak("*" if secure else ms[cursor])
							
						else:
							speak("*" if secure else ms[cursor])
						
					
				else:
					speak("blank")
				
			if(key_pressed(K_END)):
			
				if(len(ms) > 0):
				
					cursor=len(ms)
					if (cursor>=len(ms)):
						speak("Blank")
					elif (ms[cursor]==" "):
						speak("*" if secure else "space")
					else:
					
						if (string_is_upper_case(ms[cursor])) :
							if (self.capmode==1) :
								capbeep.stop();
								capbeep.play()
								speak("*" if secure else ms[cursor])
								
							elif (self.capmode==2):
								speak("cap"+("*" if secure else ms[cursor]))
							else:
								speak("*" if secure else ms[cursor])
							
						else:
							speak("*" if secure else ms[cursor])
						
					
				else:
					speak("blank")
				
			if(key_pressed(K_ESCAPE)):
			
				speak("Cancel.")
				return ""
				
			elif(key_pressed(K_RETURN)):
			
				if(online):
					g.n.send_reliable(0,"playsnd keytype_return.ogg",0)
				else:
					g.p.play_stationary("keytype_return.ogg",False)
				if (len(ms) > 0):
				
					for i in range(len(ms)):
					
						message+=ms[i]
						
					return message
					
				elif (len(ms)==0):
				
					speak("Cancel.")
					return ""
					
				
			
		return ""
		
	
