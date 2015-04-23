import requests
from logger import *

def PostToRedQueen(textToSay):
  try:
    payload = {"message":textToSay, "channel":"#makerslocal", "isaction":False, "key":"KEYGOESHERE"}
    r = requests.post("https://crump.space/rq/relay", json = payload)
  except:
    f = open('/home/pi/myPythonErrorFile.txt','w')
    #f.write( sys.exc_info()[0] )
    log( sys.exc_info()[0])
    f.close()



