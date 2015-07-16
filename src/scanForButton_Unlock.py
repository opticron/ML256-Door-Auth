#!/usr/bin/python
import sys
import json
import subprocess
from scanForButton import WaitForButtonUnlockThenLock
from door_utils import unlock_door
from playSound import *

soundPrefix = "Goodbye!"
soundSuffix = ""


try:
  while True:
      # Grab the output from poll.py
      results = WaitForButtonUnlockThenLock()
      print ("Unlock Button Detected!")
      print (results)

      unlock_door()

      #PlaySound(soundPrefix + name + soundSuffix)
      #WaitToCloseThenLock()
except: 
  f = open('/home/pi/myPythonErrorFile.txt','w')
  #f.write( sys.exc_info()[0] )
  print sys.exc_info()[0]
  f.close()
