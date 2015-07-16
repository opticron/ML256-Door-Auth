#!/usr/bin/python
import sys
from ldapCheck import getAllFromUID


while 1:
  try:
    uid= str(sys.argv[1])
    results = getAllFromUID(uid)    
    print results
    break
  except KeyboardInterrupt:
    print "\nBye\n"
    sys.exit()



