import sys
import os

# Add src and src/zero_hour_assault to path so everything resolves
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, "src"))
sys.path.insert(0, os.path.join(current_dir, "src", "zero_hour_assault"))

# Set working directory to root
os.chdir(current_dir)

# Import and run the actual main
import zero_hour_assault.core.main
