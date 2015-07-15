#!/usr/bin/python
##########################
# This code borrows from the Makers Local 256 Cash-Caching Automoton Project.  This file specifically borrows from tail.py from 
# that project.  ~Omegix 
##########################

import time, os, re, ldap
from ldapCheck import *
from GPIO_interface import *
from whiteListCheck import *
from logger import *
from PostToRedQueen import *

#GLOBALS
CHECK_LOCAL_WHITE_LIST = False  #Set this to False if use of local whitelist is not desired
IS_REDQUEEN_ENABLED = True #Set this to true to enable Red Queen IRC Reporting

#Set the filename and open the file
filename = '/var/log/kern.log'
file = open(filename,'r')

#Find the size of the file and move to the end
st_results = os.stat(filename)
st_size = st_results[6]
file.seek(st_size)

while 1:
  try:
    where = file.tell()
    line = file.readline()
    if os.path.isfile("/storage/lock"):
      continue
    if not line:
        time.sleep(1)
        file.seek(where)
    else:
        m = re.search('SerialNumber: (.*)$', line)        
        if m is None:
          continue
        # proccess receive usbsn
        iSerial =  m.group(1)
	name = getUsernameFromUSB(m.group(1))        
        #Check against whitelist (if enabled)
        if (CHECK_LOCAL_WHITE_LIST):
          if ( isInWhiteList(iSerial) ):
            log( "UID in whitelist")
            UnlockDoor()
            continue
        # implied else:  go on to check LDAP 
        # Call Ldap checker and provide key to be checked
        log(name)
        if (name == "NO_USER"):
          PostToRedQueen("USB authentication failed.  Error: defense system not implemented.")
          continue
        else:
          #Any result other than NO_USER indicates that the user is authenticated
          UnlockDoor()
	  if (IS_REDQUEEN_ENABLED):
	    PostToRedQueen("USB Authentication Token found. Unlocking for " + name)
          WaitToCloseThenLock()
  except KeyboardInterrupt:
    log( "\nBye\n")
    sys.exit()
