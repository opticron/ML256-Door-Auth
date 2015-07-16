#!/usr/bin/python
import sys
from ldapCheck import getUsernameFromUSB


while 1:
  try:
#    usbsn = "I'm a bad username" 
    usbsn = str(sys.argv[1])
    name = getUsernameFromUSB(usbsn)    
    print name
    break
  except KeyboardInterrupt:
    print "\nBye\n"
    sys.exit()



