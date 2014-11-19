#!/usr/bin/python
import sys

def log(x):
  print x + "\n"
  with open("/home/pi/error.log","a") as file:
    file.write(x + "\n")
    
    