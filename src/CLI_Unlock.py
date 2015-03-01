#!/usr/bin/python

import time, os, re, ldap
from ldapCheck import *
from GPIO_interface import *
from whiteListCheck import *
from writeToDirectory import *
from logger import *
from PostToRedQueen import *

#GLOBALS
IS_REDQUEEN_ENABLED = True #Set this to true to enable Red Queen IRC Reporting

if len(sys.argv) <= 1:
	name = "root"
	str = "Authentication system bypassed. Unlocking for " + name
else:
	name = sys.argv.pop()
	str = "LDAP credentials verified. Unlocking for " + name

UnlockDoor()

log("unlocked via CLI for:")
log(name)

if (IS_REDQUEEN_ENABLED):
	PostToRedQueen(str)
	print str

WaitToCloseThenLock()


