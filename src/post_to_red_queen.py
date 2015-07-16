import requests
from logger import log
from door_utils import get_config_section

RQ_CONFIG = get_config_section("RedQueen")

def post_to_red_queen(textToSay):
  try:
    payload = {"message":textToSay, "channel":RQ_CONFIG['Channel'], \
      "isaction":RQ_CONFIG['IsAction'], "key":RQ_CONFIG['Key']}
    r = requests.post("https://crump.space/rq/relay", json = payload)
  except:
    f = open('/home/pi/myPythonErrorFile.txt','w')
    #f.write( sys.exc_info()[0] )
    log( sys.exc_info()[0])
    f.close()



