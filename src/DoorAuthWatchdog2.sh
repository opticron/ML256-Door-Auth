#!/bin/bash

PYTHON=/usr/bin/python

function myprocess {
     $PYTHON /home/pi/DoorAuth/DoorAuth1.7/src/scanForNFC_Unlock.py \
     | tee /home/pi/nfc.log \
     | tee -a /home/pi/DoorAuth/DoorAuth1.7/src/error.txt
}


until myprocess; do
     NOW="$(date +"%b-%d-%y")
     echo "$NOW Prog crashed. Restarting..." >> errorFreq.txt
     sleep 1
done
