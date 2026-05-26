# miscellaneous functions written by nbm studios


import pyperclip, sys, time, os, threading

import pygame, sound, speech
import globals as g
import ctypes

def clipboard_copy_text(text):
    try:
        pyperclip.copy(text)
        return True
    except:
        return False


def clipboard_read_text():
    return pyperclip.paste()


def exit():

    g.p.play_stationary("gamedoorclose.ogg",False)
    g.exiting=True
    speech.speak("Exiting ...")
    g.delay(1700)
    ctypes.windll.kernel32.ExitProcess(0)

def is_game_window_active():
    if g.window_handle is None: g.window_handle=pygame.display.get_wm_info()["window"]
    return ctypes.windll.user32.GetForegroundWindow()==g.window_handle


def show_game_window(title):
    try:
        infoObject = pygame.display.Info()
        screen_width, screen_height = infoObject.current_w, infoObject.current_h


        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption(title)
        center_x = screen_width // 2
        center_y = screen_height // 2
        pygame.mouse.set_pos((center_x, center_y))
        g.screen=screen
        return screen
    except:
        return False


def wait(miliseconds):
    try:
        time.sleep(miliseconds / 1000)  # this function needs time in seconds
        return True
    except:
        return False


def read_environment_variable(variable):
    return os.environ.get(variable)
