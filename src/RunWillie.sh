#!/bin/bash

PYTHON=/usr/bin/python

function myprocess {


$PYTHON /home/pi/DoorAuth/willie/willie.py -c /home/pi/.willie/WilliePi.cfg> /home/pi/DoorAuth/DoorAuth1.7/src/WillieError.txt

}

rm /home/pi/.willie/pids/*

NOW=$(date +"%b-%d-%y")

until myprocess; do
     echo "$NOW Prog crashed. Restarting..." > errorFreq.txt
     sleep 1
done
