import importlib
import main
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

print(f"Before reload: {main.version}")
importlib.reload(main)
print(f"After reload: {main.version}")