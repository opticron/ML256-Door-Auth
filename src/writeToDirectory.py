import subprocess
import time


DIRECTORYPATH = "/home/pi/.willie/TextToSay/"
FILENAME = "somethingToSay"
PATH_AND_NAME = DIRECTORYPATH + FILENAME

def WriteToDirectory(name):
  textToWrite = "Unlocking for " + name
  f = open(PATH_AND_NAME, 'w')
  f.write(textToWrite)
  f.close




