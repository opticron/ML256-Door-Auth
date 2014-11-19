#import json
import subprocess
#from ldapCheck import *

def PlaySound(textToSay):
  #textToSay = "Hello Omegix"
  results = subprocess.check_output(['/home/pi/code/Text-to-Speech/speech.sh', textToSay])


