#!/usr/bin/python
##########################
# This code borrows from the Makers Local 256 Cash-Caching Automoton Project.  This file specifically borrows from tail.py from 
# that project.  ~Omegix 
##########################

import time, os, re, ldap
from ldapCheck import *
from door_utils import unlock_door, schedule_lock
from whiteListCheck import *
from logger import log
from post_to_red_queen import post_to_red_queen

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
            unlock_door()
            continue
        # implied else:  go on to check LDAP 
        # Call Ldap checker and provide key to be checked
        log(name)
        if (name == "NO_USER"):
          post_to_red_queen("USB authentication failed.  Error: defense system not implemented.")
          continue
        else:
          #Any result other than NO_USER indicates that the user is authenticated
          unlock_door()
	  if (IS_REDQUEEN_ENABLED):
	    post_to_red_queen("USB Authentication Token Found. Unlocking for " + name)
          schedule_lock()
  except KeyboardInterrupt:
    log( "\nBye\n")
    sys.exit()
