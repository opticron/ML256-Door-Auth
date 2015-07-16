#!/usr/bin/python
import time, os, re, ldap
import serial
import sys
from door_utils import get_config_section

LDAP_CONFIG = get_config_section("LDAP")

LDAP_URI = LDAP_CONFIG["Address"]

def getAllFromUID(uid):
  ld = ldap.initialize(LDAP_URI)
  try:
    ld.simple_bind_s()
  except ldap.LDAPError, e:
    if type(e.message) == dict and e.message.has_key('desc'):
      print e.message['desc']
    else:
      print e
  else:
    basedn = "dc=makerslocal,dc=org"
    filter = "uid="+uid
    results = ld.search_s(basedn,ldap.SCOPE_SUBTREE,filter)
  finally:
    ld.unbind()
    return results

def getUsernameFromUSB(usbsn):
  ld = ldap.initialize(LDAP_URI)
  name = "NO_USER"
  try:
    ld.simple_bind_s()
  except ldap.LDAPError, e:
    if type(e.message) == dict and e.message.has_key('desc'):
      print e.message['desc']
    else:
      print e
  else:
    basedn = "dc=makerslocal,dc=org"
    filter = "usbSerial="+usbsn
    results = ld.search_s(basedn,ldap.SCOPE_SUBTREE,filter)
    name = results[0][1]['uid'][0]
    print name
  finally:
    ld.unbind()
    return name

def getUsernameFromNFC(nfcsn):
  ld = ldap.initialize(LDAP_URI)
  name = "NO_USER"
  try:
    ld.simple_bind_s()
  except ldap.LDAPError, e:
    if type(e.message) == dict and e.message.has_key('desc'):
      print e.message['desc']
    else:
      print e
  else:
    basedn = "dc=makerslocal,dc=org"
    filter = "nfcID="+nfcsn
    results = ld.search_s(basedn,ldap.SCOPE_SUBTREE,filter)
    name = results[0][1]['uid'][0]
  finally:
    ld.unbind()
    return name

