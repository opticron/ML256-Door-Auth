#!/usr/bin/python
import binascii
import sys
import json
import subprocess
import time
from ldapCheck import *
from door_utils import unlock_door, schedule_lock
from playSound import *
from whiteListCheck import *
from logger import log
from post_to_red_queen import post_to_red_queen

soundPrefix = "Welcome to Makers Local"
soundSuffix = ""

CHECK_LOCAL_WHITE_LIST = False  #Set this to False if use of local whitelist is not desired
IS_REDQUEEN_ENABLED = True #Set this to true to enable Red Queen IRC Reporting

try:
  while True:
      # Grab the output from poll.py
      results = subprocess.check_output(['/usr/bin/sudo','/usr/bin/python3',
  os.path.join(os.path.dirname(__file__), "poll_old.py")])
      if results:
            log (results)
            log ("NFC detected!")

            # Convert the JSON into a list
            scan_results = json.loads(results)
                #params={'reader_id':scan_results['reader_id'],
                #        'card_uid':scan_results['card_uid'],
                #        'status':scan_results['status'],
                #        'timestamp':timestamp})
            card_uid = scan_results['card_uid']
            #log card_uid

            # Call Ldap checker and provide key to be checked
            trimmed_uid = scan_results['card_full_uid'][-15:]
	    trimmed_uid = trimmed_uid[:-1]
            #I believe the solution is to trim off the first characters IF they are "040804"
            #log("Do we need to snip " + trimmed_uid[0:6] + " to make " + trimmed_uid[6:])
            if trimmed_uid[0:6] == "040804" and len(trimmed_uid) >= 14:
              #then we totes need to trim that shit yo (it's at least 14 chars but the first six are garbage)
              trimmed_uid = trimmed_uid[6:]
            #trimmed_uid = card_uid
            log("Going to search for " + trimmed_uid)
            name = getUsernameFromNFC(trimmed_uid)

            if (CHECK_LOCAL_WHITE_LIST):
              testVar = str(card_uid)
              if ( isInWhiteList(testVar) ):
                log("UID in whitelist")
                unlock_door()
                continue
              # implied else:  go on to check LDAP
              #REMVE NEXT LINE
      	#continue

            #if we get here, the user wasn't in the white list (or we didn't check it)
            log(name)
            #PlaySound(soundPrefix + name + soundSuffix)
            if (name == "NO_USER"):
              post_to_red_queen("NFC Authentication failed. Error: Defense system not implemented.")
              continue
            else:
              #Any result other than NO_USER indicates that the user is in ldap and authenticated
              unlock_door()
	      if (IS_REDQUEEN_ENABLED):
                post_to_red_queen("NFC Authentication Token found. Unlocking for " + name)
              schedule_lock()
except:
  f = open('/home/pi/myPythonErrorFile.txt','w')
  #f.write( sys.exc_info()[0] )
  log( sys.exc_info()[0])
  f.close()
