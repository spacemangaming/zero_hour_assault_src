import requests
import os
import sys
import ctypes
from file_directories import file_get_contents, file_put_contents
import subprocess
from downloader import download_file
from dlg import dlg
import zipfile
from speech import speak
import globals as g
import time
APP_VERSION = g.ver
VERSION_URL = "https://spacemangaming.vineyard.haus/zero/version.txt"

def check():
    with requests.get(VERSION_URL, timeout=5) as response:
        remote_version = response.content.decode().strip()

    if remote_version > APP_VERSION:
        g.p.play_stationary("misc166.ogg",False)
        user32 = ctypes.windll.user32
        response = user32.MessageBoxW(
            0,
            "There's an update available for the game, would you like to download?",
            "Update available",
            36,
        )

        if response == 6:
            for pyd in g.pyds:
                pyd_path = os.path.join("_internal", pyd)
                if os.path.exists(pyd_path):
                    try:
                        os.rename(pyd_path, pyd_path + ".1")
                    except Exception:
                        pass
            if os.path.exists("zero_hour_assault.exe"):
                try:
                    os.rename("zero_hour_assault.exe", "zero_hour_assault1.exe")
                except Exception:
                    pass
            speak("Downloading update package ...")
            download_file("https://spacemangaming.vineyard.haus/zero/update_package.zip")
            speak("Extracting update package ...")
            unzip("update_package.zip")
            os.remove("update_package.zip")
            speak("Update complete! The game will now restart.")
            time.sleep(2)
            subprocess.Popen(["zero_hour_assault.exe"])
            os._exit(0)
        else:
            user32.MessageBoxW(0, "You didn't choose to update. The game will now exit", "Update not chosen", 0)
            os._exit(0)
SND_VERSION = file_get_contents("sndversion.txt")
SND_VERSION_URL = "https://spacemangaming.vineyard.haus/zero/sndversion.txt"

def sndcheck():
    remote_version = requests.get(SND_VERSION_URL).text.strip()

    if remote_version > SND_VERSION:
        g.p.play_stationary("misc166.ogg",False)
        user32 = ctypes.windll.user32

        response = user32.MessageBoxW(
            0,
            "There's an update available for the game sounds, would you like to download?",
            "Update available",
            36,
        )

        if response == 6:
            download_file("https://spacemangaming.vineyard.haus/zero/sounds1.dat")
            file_put_contents("sndver.txt", remote_version)
            dlg("Update complete! Please restart the game.")
            os._exit(0)
        else:
            user32.MessageBoxW(0, "You didn't choose to update. The game will now exit", "Update not chosen", 0)
            os._exit(0)

def unzip(file_path, extract_to=None):
    if not extract_to:
        extract_to = "."
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        for member in zip_ref.infolist():
            target_path = os.path.join(extract_to, member.filename)
            target_dir = os.path.dirname(target_path)
            if target_dir and not os.path.exists(target_dir):
                try:
                    os.makedirs(target_dir, exist_ok=True)
                except Exception:
                    pass
            
            if os.path.exists(target_path) and not os.path.isdir(target_path):
                try:
                    if os.path.exists(target_path + ".old"):
                        os.remove(target_path + ".old")
                except Exception:
                    pass
                try:
                    os.rename(target_path, target_path + ".old")
                except Exception:
                    pass
            
            try:
                zip_ref.extract(member, extract_to)
            except Exception as e:
                print(f"Failed to extract {member.filename}: {e}")
    return extract_to