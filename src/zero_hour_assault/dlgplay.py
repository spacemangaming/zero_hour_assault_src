from sound import sound
from events import process_events, key_pressed
from pygame.locals import *
dlgaudio=sound()
def dlgplay(dlgsound):

	dlgaudio.load(dlgsound)
	dlgaudio.player.stationary=True
	dlgaudio.play()
	while(dlgaudio.player.playing2()):
	
		process_events()
		if(key_pressed(K_RETURN)):
		
			dlgaudio.fade()
			break
			
		
	dlgaudio.close()
