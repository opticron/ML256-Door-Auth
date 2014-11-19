import os
import sys
import binascii
lib_path = os.path.abspath('/home/pi/DoorAuth/DoorAuth1.7/lib')
sys.path.append(lib_path)

from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *

import hashlib


class nfc_poller:

    def __init__(self):
        self._address = RPI_DEFAULT_I2C_NEW
        self._pn532 = Pn532_i2c()
        self._pn532.SAMconfigure()

    def create_json_response(self, reader_id, card_uid, card_full_uid, status):
        json = """{"reader_id":"<reader_id>","card_uid":"<card_uid>","card_full_uid":"<card_full_uid>","status":"<status>"}"""
        json = json.replace("<reader_id>", str(reader_id))
        json = json.replace("<card_uid>", card_uid)
        json = json.replace("<card_full_uid>", card_full_uid)
        json = json.replace("<status>", status)

        return json

    def poll(self):
        card_uid = self._pn532.read_mifare().get_data()

        a = str(binascii.hexlify(card_uid))
        #cardid = "".join(reversed([a[i:i+2] for i in range(0, len(a), 2)])) #reverse byte array 2 at a time
        #cardid = a #or not
        cardid = a[-9:-1] #last 9 bytes except the last one (I guess?)
        
        json = self.create_json_response(self._address, cardid, a, "OK")
            #self._address, hashlib.sha512(card_uid).hexdigest(), "OK")
            
        return json

    def __exit__(self, type, value, traceback):
        del self._pn532
