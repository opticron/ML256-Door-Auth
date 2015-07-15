#!/bin/bash

PYTHON=/usr/bin/python

function myprocess {
     $PYTHON `dirname $0`/scanForUSB_Unlock.py \
     | tee -a `dirname $0`/usb.log
}


until myprocess; do
     NOW=$(date +"%b-%d-%y")
     echo "$NOW Prog crashed. Restarting..." >> errorFreq.txt
     sleep 1
done
