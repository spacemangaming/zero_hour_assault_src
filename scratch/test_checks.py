import os
import sys

# Ensure Python can import modules from the package directory
script_dir = r"e:\git-project\zero_hour_assault_src"
sys.path.insert(0, os.path.join(script_dir, "src"))
sys.path.insert(0, os.path.join(script_dir, "src", "zero_hour_assault"))

if sys.platform == "win32":
	os.environ["PATH"] = script_dir + os.pathsep + os.environ["PATH"]
if hasattr(os, "add_dll_directory"):
	try:
		os.add_dll_directory(script_dir)
	except Exception:
		pass

import zero_hour_assault
print("is_vm exists on module?", hasattr(zero_hour_assault, 'is_vm'))
print("is_vm():", zero_hour_assault.is_vm())
try:
    print("hash anticheat:", zero_hour_assault.file_get_hash_sha256("anticheat.dll"))
except Exception as e:
    print("hash anticheat error:", e)
