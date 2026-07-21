import os
import sys

# Safe temp directory detection with fallback
DIRECTORY_TEMP = os.environ.get("temp") or os.environ.get("TEMP") or os.environ.get("TMPDIR") or "/tmp"

# Safe appdata directory detection with fallback
if sys.platform == "win32":
    DIRECTORY_APPDATA = os.environ.get("appdata") or os.environ.get("APPDATA") or os.path.expanduser("~")
else:
    DIRECTORY_APPDATA = os.environ.get("HOME") or os.path.expanduser("~")

Left=-1
Right=1
Backward=0
Forward=2
Down=-2
Up=3
soundcard=None
steam=0
cache=1