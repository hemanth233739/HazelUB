import os
import sys

def restart():
  os.execv(sys.executable, [sys.executable] + sys.argv)