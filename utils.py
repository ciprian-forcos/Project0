# utils.py
import random
import string
import json
import os

CONFIG_FILE = 'config.json'

def generate_filename(extension='jpeg'):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + f'.{extension}'

def load_config():
    if not os.path.exists(CONFIG_FILE):
        config = {
            'api_key': '',
            'api_url': 'https://api.openai.com/v1/chat/completions',
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

def get_save_location():
    config = load_config()
    return config.get('save_location', os.path.expanduser('~/Desktop'))
