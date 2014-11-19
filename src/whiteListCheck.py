#!/usr/bin/python
import time, os, re
import sys
from xml.dom import minidom

WHITE_LIST_PATH =  "/home/pi/DoorAuth/DoorAuth1.7/src/whiteList.xml"

def isInWhiteList(uid):
  print ("Got this far 2")
  xmldoc = minidom.parse(WHITE_LIST_PATH)
  itemList = xmldoc.getElementsByTagName('nfc')
  #print "Number of Whitelist Entries: \n" + str( len(itemList) )
  i = 0
  for node in itemList:
    #print node.toxml()
    itemValue = itemList[i].firstChild.nodeValue
    #print itemValue
    if (uid == itemValue):
      return True
    i = i + 1

  itemList = xmldoc.getElementsByTagName('iSerial')
  #print "Number of Whitelist Entries: " + str( len(itemList) )
  i = 0
  for node in itemList:
    #print node.toxml()
    itemValue = itemList[i].firstChild.nodeValue
    #print itemValue
    if (uid == itemValue):
      return True
    i = i + 1

  return False

