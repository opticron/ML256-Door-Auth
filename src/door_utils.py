'''Utilities common to much door functionality'''
import json
import time
from os.path import expanduser

CONFIG_FILE = expanduser("~/.doorConfig")

def get_config_section(section_name):
    '''Get a config section'''
    with open(CONFIG_FILE, "r") as config_file:
        json_config = json.load(config_file)
        return json_config[section_name]

GPIO_CONFIG = get_config_section("GPIO")

REED_SENSOR_PIN = GPIO_CONFIG.get("reed_sensor_pin", 22)
DOOR_STATE_OPEN = GPIO_CONFIG.get("door_state_open", 0)  #REED_SENSOR_PIN is has a pullup resistor to 5V
DOOR_STATE_CLOSED = GPIO_CONFIG.get("door_state_closed", 1) #reed switch will be connected to ground
UNLOCK_RELAY_PIN = GPIO_CONFIG.get("unlock_relay_pin", 23)
LOCK_RELAY_PIN = GPIO_CONFIG.get("lock_relay_pin", 24)
RELAY_TOGGLE_DELAY = GPIO_CONFIG.get("relay_toggle_delay", 0.25)
CLOSE_TO_LOCK_DELAY = GPIO_CONFIG.get("close_to_lock_delay", 3)
LOCK_ATTEMPT_BACKOFF_DELAY = GPIO_CONFIG.get("lock_attempt_backoff_delay", 7)

def unlock_door():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(UNLOCK_RELAY_PIN, GPIO.OUT)
  GPIO.output(UNLOCK_RELAY_PIN, GPIO.HIGH)
  time.sleep(RELAY_TOGGLE_DELAY)
  GPIO.output(UNLOCK_RELAY_PIN, GPIO.LOW)

def lock_door():
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
  lock_door()

def schedule_lock():
  #print("Waiting for %d Seconds before scanning for door closure" % LOCK_ATTEMPT_BACKOFF_DELAY)
  ScheduleLockStep(AttemptLock, delay=LOCK_ATTEMPT_BACKOFF_DELAY, override=True)

def PrintReedSwitchState():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(REED_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

  while True:
    input = GPIO.input(REED_SENSOR_PIN)
    print(input)
