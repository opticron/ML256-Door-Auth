import time
import RPi.GPIO as GPIO
from door_utils import get_config_section, unlock_door, schedule_lock

GPIO_CONFIG = get_config_section("GPIO")

BUTTON_STATE_PRESSED = GPIO_CONFIG.get("button_state_pressed", 0)
BUTTON_STATE_RELEASED = GPIO_CONFIG.get("button_state_released", 1)
UNLOCK_BUTTON_PIN = GPIO_CONFIG.get("unlock_button_pin", 27)

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
        unlock_door()
        schedule_lock()

