# utils.py
import json
import os

CONFIG_FILE = 'config.json'

def load_config():
    if not os.path.exists(CONFIG_FILE):
        config = {
            'api_key': '',
            'api_url': '',
            'save_location': os.path.expanduser('~/Desktop')
        }
        save_config(config)
    else:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    return config

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
