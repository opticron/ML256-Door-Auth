#!/usr/bin/python
#import time, os, re, ldap
#import serial
import sys
from ldapCheck import *


while 1:
  try:
    uid= str(sys.argv[1])
    results = getAllFromUID(uid)    
    print results
    break
  except KeyboardInterrupt:
    print "\nBye\n"
    sys.exit()



