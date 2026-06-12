import sys
import os

if getattr(sys, 'frozen', False):
    # Running as a compiled PyInstaller executable
    app_root = os.path.dirname(sys.executable)
else:
    # Running as a script
    app_root = os.path.dirname(os.path.abspath(__file__))

# Add src and src/zero_hour_assault to path so everything resolves
sys.path.insert(0, os.path.join(app_root, "src"))
sys.path.insert(0, os.path.join(app_root, "src", "zero_hour_assault"))

# Set working directory to root
os.chdir(app_root)

# Import and run the actual main
import zero_hour_assault.core.main
