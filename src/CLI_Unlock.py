#!/usr/bin/python

from door_utils import schedule_lock, unlock_door
from logger import log
from post_to_red_queen import post_to_red_queen

#GLOBALS
IS_REDQUEEN_ENABLED = True #Set this to true to enable Red Queen IRC Reporting

if len(sys.argv) <= 1:
	name = "root"
	str = "Authentication system bypassed. Unlocking for " + name
else:
	name = sys.argv.pop()
	str = "LDAP credentials verified. Unlocking for " + name

unlock_door()

log("unlocked via CLI for:")
log(name)

if (IS_REDQUEEN_ENABLED):
	post_to_red_queen(str)
	print str

schedule_lock()


