#!/usr/bin/python
import sys
import json
import subprocess
from GPIO_interface import *
from playSound import *

soundPrefix = "Goodbye!"
soundSuffix = ""


try:
  while True:
      # Grab the output from poll.py
      results = WaitForButtonUnlockThenLock()
      print ("Unlock Button Detected!")
      print (results)

      UnlockDoor()

      #PlaySound(soundPrefix + name + soundSuffix)
      #WaitToCloseThenLock()
except: 
  f = open('/home/pi/myPythonErrorFile.txt','w')
  #f.write( sys.exc_info()[0] )
  print sys.exc_info()[0]
  f.close()
