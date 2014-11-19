#!/usr/bin/env python

import os
import re

#proc = subprocess.Popen(["cat", "nfc_poll_test.txt"], stdout=subprocess.PIPE, shell=True)
#(out, err) = proc.communicate()
#print("program output:", out)

shit = os.popen('cat nfc_poll_test.txt').read()
shit = os.popen('sudo nfc-poll').read()
#print (shit)
for thing in shit.split('\n'):
	#print(thing)
	match = re.search(r'UID.+: (.+)', thing)
	if match != None:
		uid = match.group(1).replace(' ','')
		print('{"reader_id":"1","card_uid":"' + uid + '","card_full_uid":"' + match.group(0) + '","status":"OK"}')
