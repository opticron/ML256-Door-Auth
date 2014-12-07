import requests

def PostToRedQueen(textToSay):
  textToSay = "Unlocking for: Tyler Please Put a #makerslocal Key in PostToRedQueen.py"
  payload = {"message":textToSay, "channel":"##rqtest", "isaction":False, "key":"13371234"}
  r = requests.post("https://restirc.tylercrumpton.com/relay", json = payload)


