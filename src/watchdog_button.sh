#!/bin/bash

PYTHON=/usr/bin/python

function myprocess {

$PYTHON `dirname $0`/scanForButton_Unlock.py >> `dirname $0`/error.txt

}
NOW=$(date +"%b-%d-%y")

until myprocess; do
     echo "$NOW Prog crashed. Restarting..." > errorFreq.txt
     sleep 1
done
