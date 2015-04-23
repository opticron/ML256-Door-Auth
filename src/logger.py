#!/usr/bin/python
import sys

def log(x):
  print str(x) + "\n"
  with open("/home/pi/error.log","a") as file:
    file.write(str(x) + "\n")
    
    
