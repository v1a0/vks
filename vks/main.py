from settings import GREETING_ART
import subprocess
import sys

while True:
    print(GREETING_ART)
    subprocess.Popen([sys.executable, "vks.py"]).wait()

# args = sys.argv