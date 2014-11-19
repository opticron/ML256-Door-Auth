#!/bin/bash

PYTHON=/usr/bin/python

function myprocess {


$PYTHON /home/pi/DoorAuth/DoorAuth1.7/src/scanForUSB_Unlock.py >> /home/pi/DoorAuth/DoorAuth1.7/src/errorUSB.txt

}
NOW=$(date +"%b-%d-%y")

until myprocess; do
     echo "$NOW Prog crashed. Restarting..." > errorFreq_USB.txt
     sleep 1
done
