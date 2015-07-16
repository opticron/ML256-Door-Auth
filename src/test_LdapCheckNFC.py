#!/usr/bin/python
import sys
from ldapCheck import getUsernameFromNFC


while 1:
  try:
#    nfcsn = "I'm a bad username" 
    nfcsn = str(sys.argv[1])
    name = getUsernameFromNFC(nfcsn)    
    print name
    break
  except KeyboardInterrupt:
    print "\nBye\n"
    sys.exit()



