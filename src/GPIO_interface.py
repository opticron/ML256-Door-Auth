import subprocess
#import json
#import requests
import time
#import ConfigParser
#import hashlib
import RPi.GPIO as GPIO

REED_SENSOR_PIN = 22
DOOR_STATE_OPEN = 0  #REED_SENSOR_PIN is has a pullup resistor to 5V
DOOR_STATE_CLOSED = 1 #reed switch will be connected to ground
BUTTON_STATE_PRESSED = 0
BUTTON_STATE_RELEASED = 1
UNLOCK_BUTTON_PIN = 27
UNLOCK_RELAY_PIN = 23
LOCK_RELAY_PIN = 24
RELAY_TOGGLE_DELAY = 0.25
CLOSE_TO_LOCK_DELAY = 3
LOCK_ATTEMPT_BACKOFF_DELAY = 7

 # Is it valid?
def UnlockDoor():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(UNLOCK_RELAY_PIN, GPIO.OUT)
  GPIO.output(UNLOCK_RELAY_PIN, GPIO.HIGH)
  time.sleep(RELAY_TOGGLE_DELAY)
  GPIO.output(UNLOCK_RELAY_PIN, GPIO.LOW)
    
def LockDoor():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(LOCK_RELAY_PIN, GPIO.OUT)
  GPIO.output(LOCK_RELAY_PIN, GPIO.HIGH)
  time.sleep(RELAY_TOGGLE_DELAY)
  GPIO.output(LOCK_RELAY_PIN, GPIO.LOW)
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
  ScheduleLockStep(FinalDoorCheck, delay=CLOSE_TO_LOCK_DELAY)

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
  #print("Waiting for %d Seconds before scanning for door closure" % LOCK_ATTEMPT_BACKOFF_DELAY)
  ScheduleLockStep(AttemptLock, delay=LOCK_ATTEMPT_BACKOFF_DELAY, override=True)

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

