from settings import GREETING_ART
import subprocess
import sys

while True:
    # args = sys.argv
    print(GREETING_ART)
    subprocess.Popen([sys.executable, "vks.py"]).wait()

