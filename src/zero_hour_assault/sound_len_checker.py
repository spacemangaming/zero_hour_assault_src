import os
import pyperclip
from pydub import AudioSegment
def main():
	snd=input("Enter the name of the file you would like to check (without .ogg): ").strip()
	if not snd:
		print("write name is not correct")
		return
	filepath=os.path.join("sounds",f"{snd}.ogg")
	if not os.path.isfile(filepath):
		print(f"File '{filepath}' not found.")
		return
	try:
		audio=AudioSegment.from_ogg(filepath)
		length_ms=len(audio)
		print(f"The file is about {length_ms} ms long. If we were to round it, it would be {round(length_ms, 3)} ms.")
		pyperclip.copy(str(length_ms))
		print("Length copied to clipboard.")
	except Exception as e:
		print("Error reading audio file:", e)
if __name__ == "__main__":
	main()