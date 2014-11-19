#!/usr/bin/python
import time, os, re, ldap
import serial
import sys
#from cash_api import *


def getAllFromUID(uid):
  ld = ldap.initialize('ldap://10.56.0.8')
  #name = "NO_USER"
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
    #name = results[0][1]['uid'][0]
    #print name
  finally:
    ld.unbind()
    return results




def getUsernameFromUSB(usbsn):
  ld = ldap.initialize('ldap://10.56.0.8')
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
    #print results
    name = results[0][1]['uid'][0]
    print name
  finally:
    ld.unbind()
    return name


def getUsernameFromNFC(nfcsn):
  ld = ldap.initialize('ldap://10.56.0.8')
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
    #print results
    name = results[0][1]['uid'][0]
  finally:
    ld.unbind()
    return name




