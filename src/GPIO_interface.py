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


from threading import Timer, RLock
CLOSE_TIMER = {
  'lock': RLock(),
  'waiting_timer': None
}

def ScheduleLockStep(lock_stage, delay=0.5, override=False):
  with CLOSE_TIMER['lock']:
    if CLOSE_TIMER['waiting_timer']:
      if override:
        # if there's a timer running, kill it
        CLOSE_TIMER['waiting_timer'].cancel()
        CLOSE_TIMER['waiting_timer'] = None
      else:
        # not overriding, bail
        return
    CLOSE_TIMER['waiting_timer'] = Timer(delay, lock_stage)
    CLOSE_TIMER['waiting_timer'].start()

REED_SENSOR_PIN = 22
DOOR_STATE_OPEN = 0  #REED_SENSOR_PIN is has a pullup resistor to 5V
DOOR_STATE_CLOSED = 1 #reed switch will be connected to ground
BUTTON_STATE_PRESSED = 0
BUTTON_STATE_RELEASED = 1
UNLOCK_BUTTON_PIN = 27


def CleanTimer():
  with CLOSE_TIMER['lock']:
    CLOSE_TIMER['waiting_timer'] = None

def AttemptLock():
  '''Door lock attempt initiation routine'''
  CleanTimer()
  # do work which may include scheduling another timer
  #GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(REED_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

  input = GPIO.input(REED_SENSOR_PIN)
  print("Waiting for door to close, input: %s" % input)
  if (input != DOOR_STATE_CLOSED):
    # Door not closed, reschedule check for later
    ScheduleLockStep(AttemptLock)
    return

  # Door appears closed, check For Debounce
  print("DoorClosedDetected:  Checking for Debounce")
  ScheduleLockStep(DoDebounce)

def DoDebounce():
  '''Door lock debounce check'''
  CleanTimer()
  input = GPIO.input(REED_SENSOR_PIN)
  if (input == DOOR_STATE_OPEN):
    print("Debounce Failed")
    ScheduleLockStep(AttemptLock)
    return

  print("Door-Closed-Sensor Debounce Test Passed")
  ScheduleLockStep(FinalDoorCheck, delay=3)

def FinalDoorCheck():
  '''Make sure someone didn't change their mind right after closing the door and reopen it'''
  CleanTimer()
  input = GPIO.input(REED_SENSOR_PIN)
  if (input != DOOR_STATE_CLOSED):
    print("Door No Longer Closed, Continuing to wait for door closure.")
    ScheduleLockStep(AttemptLock)
    return

  print("Door Closed for 3 Seconds, Locking Door")
  LockDoor()
  
def WaitToCloseThenLock():
  #print("Waiting for 7 Seconds before scanning for door closure")
  ScheduleLockStep(AttemptLock, delay=7, override=True)

def PrintReedSwitchState():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(REED_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

  while True:
    input = GPIO.input(REED_SENSOR_PIN)
    print(input)


def WaitForButtonUnlockThenLock():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(UNLOCK_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

  while True:
    myResult = GPIO.input(UNLOCK_BUTTON_PIN)
    #print(myResult)
    if (myResult == BUTTON_STATE_PRESSED):
      #Check For Debounce
      print("Button Press Detected:  Checking for Debounce")
      time.sleep(0.5)   
      input = GPIO.input(UNLOCK_BUTTON_PIN)
      if (myResult == BUTTON_STATE_RELEASED):
        print("Button Press Debounce Failed")
        continue
      else:
        print("Button Pressed Debounce Test Passed")
        UnlockDoor()
        WaitToCloseThenLock()

