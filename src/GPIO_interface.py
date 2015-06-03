import subprocess
#import json
#import requests
import time
#import ConfigParser
#import hashlib
import RPi.GPIO as GPIO


 # Is it valid?
def UnlockDoor():
  button_pin = 23 # Set to whatever your pin is
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(button_pin, GPIO.OUT)
  GPIO.output(button_pin, GPIO.HIGH)
  time.sleep(0.25)
  GPIO.output(button_pin, GPIO.LOW)  
    
def LockDoor():
  button_pin = 24 # Set to whatever your pin is
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(button_pin, GPIO.OUT)
  GPIO.output(button_pin, GPIO.HIGH)
  time.sleep(0.25)
  GPIO.output(button_pin, GPIO.LOW)
  print("Door Should Now be Locked.")

  
def WaitToCloseThenLock():
  #print("Waiting for 10 Seconds before scanning for door closure")
  time.sleep(7)
  #input = 0
  reedSensor_pin = 22
  doorStateOpen = 0  #reedSensor_pin is has a pullup resistor to 5V
  doorStateClosed = 1 #reed switch will be connected to ground
  #GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(reedSensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  #input = GPIO.input(reedSensor_pin)
  #print(input) 
  print("Awaiting Door To Close")

  while True:
    input = GPIO.input(reedSensor_pin)
    print(input)
    if (input == doorStateClosed):
      #Check For Debounce
      print("DoorClosedDetected:  Checking for Debounce")
      time.sleep(0.5)
      input = GPIO.input(reedSensor_pin)
      if (input == doorStateOpen):
        print("Debounce Failed")
        continue
      else:
        print("Door-Closed-Sensor Debounce Test Passed")
        time.sleep(3)
        input = GPIO.input(reedSensor_pin)
        if (input == doorStateClosed):
          print("Door Closed for 3 Seconds, Locking Door")
          #Lock Door
	  LockDoor()
          break
        else:
          print("Door No Longer Closed, Continuing to wait for door closure.")
          continue


def PrintReedSwitchState():
  reedSensor_pin = 22
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(reedSensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

  while True:
    input = GPIO.input(reedSensor_pin)
    print(input)


def WaitForButtonUnlockThenLock():
  buttonPressedState = 0
  buttonReleasedState = 1
  unlockButton_pin = 27
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(unlockButton_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

  while True:
    myResult = GPIO.input(unlockButton_pin)
    #print(myResult)
    if (myResult == buttonPressedState):
      #Check For Debounce
      print("Button Press Detected:  Checking for Debounce")
      time.sleep(0.5)   
      input = GPIO.input(unlockButton_pin)
      if (myResult == buttonReleasedState):
        print("Button Press Debounce Failed")
        continue
      else:
        print("Button Pressed Debounce Test Passed")
        UnlockDoor()
        WaitToCloseThenLock()

