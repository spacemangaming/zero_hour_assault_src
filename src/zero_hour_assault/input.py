import wx
import unicodedata
import globals as g
import ctypes
import time
import events
import pygame
from speech import speak
from events import process_events
from translation import translate
from threading import Thread
from random import randint as random
from Miscellaneous import is_game_window_active
import sound
import sys
clock=pygame.time.Clock()
compiled=getattr(sys,"frozen",False)
compiled=False
g.binded=False
g.doted=False
class CustomTextInputDialog:
    def __init__(self, title,iconify):
        g.shouldsetcaption=False
        if g.text_ctrl is None and g.label is None: g.tempframe = wx.Frame(None)
        if not g.doted and title!=chr(65533): pygame.display.set_caption(chr(65533))
        d = wx.Frame(None)
        ctypes.windll.user32.SetParent(d.GetHandle(),g.window_handle)
        d.Destroy()






        self.setcaption=False
        g.iconify=iconify
        self.title = title

        if g.templabel is None:
            g.templabel = wx.StaticText(g.tempframe,label="Zero hour assault "+g.ver)

            ctypes.windll.user32.SetParent(g.templabel.GetHandle(), g.window_handle)

        if g.text_ctrl is None:

            if self.title.lower().find("password")!=-1 and self.title.find("who'se password")==-1: g.text_ctrl = wx.TextCtrl(g.tempframe, style=wx.TE_PASSWORD, size=(1920,1080))
            else: g.text_ctrl = wx.TextCtrl(g.tempframe, style=wx.TE_MULTILINE, size=(1920,1080))
            ctypes.windll.user32.SetParent(g.text_ctrl.GetHandle(), g.window_handle)

        else:
            g.text_ctrl.Clear()
            g.text_ctrl.Enable()

        if g.label is None:
            g.label = wx.StaticText(g.tempframe, label=self.title)

            ctypes.windll.user32.SetParent(g.label.GetHandle(), g.window_handle)
        else:
            g.label.SetLabel(self.title)
            g.label.Enable()
        if 1:
            g.text_ctrl.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
            g.text_ctrl.Bind(wx.EVT_CHAR, self.on_char)
    def on_char(self, event):
        keycode = event.GetUnicodeKey()
        char = chr(keycode)

        if unicodedata.category(char)[0] in {'L', 'N', 'P', 'S'}:
            if g.charrepeat==1: speak(input_box_speak(char))
            if g.keytheme==1: g.p.play_stationary("keytype" + str(random(1, 10)) + ".ogg", False)
    
        event.Skip()
    def on_key_down(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_TAB:
            speak(self.title)
            return
        if keycode == wx.WXK_F1:
            if g.keytheme==0: speak("Keyboard theme enabled"); g.keytheme=1; g.writeprefs()
            elif g.keytheme==1: speak("Keyboard theme disabled"); g.keytheme=0; g.writeprefs()
        if keycode == wx.WXK_F2:
            if g.charrepeat==0: speak("Character repeat enabled"); g.charrepeat=1; g.writeprefs()
            elif g.charrepeat==1: speak("Character repeat disabled"); g.charrepeat=0; g.writeprefs()

        if g.keytheme==1 and keycode == wx.WXK_BACK:
            g.p.play_stationary("keybackspace"+str(random(1,5))+".ogg", False)
        if g.keytheme==1 and keycode == wx.WXK_RETURN:
            g.p.play_stationary("keyenter"+str(random(1,5))+".ogg", False)
        if g.charrepeat==1 and keycode == wx.WXK_SPACE: speak("Space")
        if g.keytheme==1 and keycode == wx.WXK_SPACE:
            g.p.play_stationary("keyspace"+str(random(1,5))+".ogg", False)


        if self.setcaption==False: pygame.display.set_caption("Zero hour assault "+g.ver); self.setcaption=True
        if keycode == wx.WXK_RETURN:
            if event.ShiftDown():
                current_pos = g.text_ctrl.GetInsertionPoint()
                text = g.text_ctrl.GetValue()
                new_text = text[:current_pos] + '\n' + text[current_pos:]
                g.text_ctrl.SetValue(new_text)
                g.text_ctrl.SetInsertionPoint(current_pos + 2)
                speak("New line inserted.")
            else:
                if event.ControlDown(): g.should_translate=True
                self.on_ok(None)
        elif keycode == wx.WXK_ESCAPE:
            self.on_cancel(None)
        else:
            event.Skip()

    def on_ok(self, event):
        if g.text_ctrl is not None: g.entered_text = g.text_ctrl.GetValue()
        if not compiled: pygame.display.set_caption(chr(65533))
        ctypes.windll.user32.SetFocus(g.window_handle)
        try: g.text_ctrl.Destroy(); g.text_ctrl=None
        except: pass
        try: g.label.Destroy(); g.label=None
        except: pass
        g.keys_held.clear()
        g.app.ExitMainLoop()

        g.screen.fill((0,0,0))
        pygame.display.flip()




    def on_cancel(self, event):
        if not compiled: pygame.display.set_caption(chr(65533))
        ctypes.windll.user32.SetFocus(g.window_handle)
        try: g.text_ctrl.Destroy(); g.text_ctrl=None
        except: pass
        try: g.label.Destroy(); g.label=None
        except: pass

        g.keys_held.clear()
        g.app.ExitMainLoop()
        g.screen.fill((0,0,0))
        pygame.display.flip()

        g.entered_text = ""






def get_input(title,default_text="",timerr=False,iconify=True):
    g.should_translate=False
    g.keycheck=False
    keys = pygame.key.get_pressed()
    #for key in keys:
        #if key: g.keycheck=True; break
    if g.window_handle is None: g.window_handle = int(pygame.display.get_wm_info()["window"])
    if g.lang!="en": title = translate(title)
    dialog = CustomTextInputDialog(title,iconify)

    timer = wx.Timer()
    timer2 = wx.Timer()
    def on_timer2(event):
        for i in range(100): g.netloop(False)
        g.fallloop()
        g.fallingloop()
        if g.usemouse==1: process_events(); g.mouse_update()
    def on_timer(event):
        window_state = is_game_window_active()
        if g.awindow==1:
            if not g.muted and not window_state:
                sound.listener._set_gain(0.00000001)
                g.muted=True
            elif g.muted and window_state:
                sound.listener._set_gain(g.mastervolume)
                g.muted=False


        if g.text_ctrl is not None and window_state: g.text_ctrl.SetFocus()
    timer.Bind(wx.EVT_TIMER, on_timer)
    timer.Start(1000)
    timer2.Bind(wx.EVT_TIMER, on_timer2)
    timer2.Start(0)
    if timerr:
        t = wx.Timer()
        def ont(event):
            dialog.on_ok(None)

        t.Bind(wx.EVT_TIMER,ont)
        t.Start(0)
    g.text_ctrl.SetValue(default_text); g.text_ctrl.SetFocus()
    g.app.MainLoop()
    g.shouldsetcaption = True
    Thread(target=control_window_title).start()
    g.screen.fill((0,0,0))
    pygame.display.flip()
    timer.Destroy()
    timer2.Destroy()
    if timerr: t.Destroy()

    g.left_button_down=False
    g.right_button_down=False
    g.left_button_pressed=False
    g.right_button_pressed=False

    return g.entered_text
def control_window_title():
    if compiled: g.shouldsetcaption=False; return
    while g.shouldsetcaption:
        time.sleep(0.005)
        if g.shouldsetcaption and not is_game_window_active():
            g.captiontoset="Zero hour assault "+g.ver; g.shouldsetcaption=False; return

if 1:
    def input_box_speak(character):
        if character == " ":
            return "Space"
        if character == "-":
            return "Dash"
        if character == ".":
            return "Dot"
        if character == ",":
            return "Comma"
        if character == "":
            return "At"
        if character == ">":
            return "Greater"
        if character == ";":
            return "Semi"
        if character == ":":
            return "Colon"
        if character == "'":
            return "Tick"
        if character == "<":
            return "Less"
        if character == "_":
            return "Underscore"
        if character == "+":
            return "Plus"
        if character == "=":
            return "Equals"
        if character == "!":
            return "Bang"
        if character == '"':
            return "Quote"
        if character == "\\":
            return "Backslash"
        if character == "/":
            return "Slash"
        if character == "$":
            return "Dollars"
        if character == "%":
            return "Percent"
        if character == "^":
            return "Carret"
        if character == "&":
            return "And"
        if character == "*":
            return "Star"
        if character == "(":
            return "Left Paren"
        if character == ")":
            return "Right Paren"
        if character == "[":
            return "Left Bracket"
        if character == "]":
            return "Right Bracket"
        if character == "{":
            return "Left Brace"
        if character == "}":
            return "Right Brace"

        if character == "|":
            return "Bar"
        if character == "?":
            return "Question Mark"
        if character == "`":
            return "Grave"
        if character == "#":
            return "Number"
        if character == "~":
            return "Tilda"
        return character
