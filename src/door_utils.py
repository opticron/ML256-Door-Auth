'''Utilities common to much door functionality'''
import json
from os.path import expanduser

CONFIG_FILE = expanduser("~/.doorConfig")

def get_config_section(section_name):
    '''Get a config section'''
    with open(CONFIG_FILE, "r") as config_file:
        json_config = json.load(config_file)
        return json_config[section_name]
