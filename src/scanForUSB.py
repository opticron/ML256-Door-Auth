#!/usr/bin/python
##########################
# This code borrows heavily from the Makers Local 256 Cash-Caching Automoton Project.  This file specifically borrows from tail.py from 
# that project.  ~Omegix 
##########################

import time, os, re, ldap
from ldapCheck import *

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
	getUsernameFromUSB(m.group(1))
        #process(m.group(1))
  except KeyboardInterrupt:
    print "\nBye\n"
    sys.exit()
