"""
scanDirectory.py - Scans a directory for files, if one appears, willie will say it's content into a channel
Copyright 2013, Jeff Cotten (Omegix) - https://256.makerslocal.org/wiki/User:Omegix
Licensed under the Eiffel Forum License 2.

Thanks to Eyore and Embolalia for helping me get my Willie bot instance up and running, and TylerCrumpton
from Makers Local 256 for helping me understand the regex rules
"""

import willie
import os
import glob

TextToSayDir = "/home/pi/.willie/TextToSay/"

#@willie.module.command('helloworld')
def scanDirectory(bot, trigger):
  sdlock1 = "mySDLock1"
  #If the memory location doesn't exist, then the key 'sdlocks' also will not exist, so go ahead and create.
  if not bot.memory.contains('sdlocks'):
    bot.memory['sdlocks'] = {}
    bot.memory['sdlocks'][sdlock1] = "locked"
  else:
    myStatus = bot.memory['sdlocks'][sdlock1]
    if myStatus == "locked":
      return
    #Implied else:  if sdloock1 doesn't equalck locked, continue

  while True:
    for filename in glob.iglob(os.path.expanduser(os.path.join(TextToSayDir, "*") ) ):
      with open(filename) as f:
        s = f.read()
      f.close()
      bot.say(s)
      #Now Delete File
      os.remove(filename)
scanDirectory.rule = r'.*'
