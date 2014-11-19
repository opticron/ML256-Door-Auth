import json
import subprocess
from ldapCheck import *
from playSound import *

playSounds = True

while True:
    # Grab the output from poll.py
    results = subprocess.check_output(['/usr/bin/sudo','/usr/bin/python3',
'/home/pi/code/DoorAuth1.7/src/poll.py'])
    print "Card scanned!"
    print results

    # Convert the JSON into a list
    scan_results = json.loads(results)
        #params={'reader_id':scan_results['reader_id'],
        #        'card_uid':scan_results['card_uid'],
        #        'status':scan_results['status'],
        #        'timestamp':timestamp})
    card_uid = scan_results['card_uid']
    print card_uid

    # Call Ldap checker and provide key to be checked
    name = getUsernameFromNFC(card_uid)
    print name
    if (playSounds):
      PlaySound("Welcome " + name)
