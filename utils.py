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
        default_config = {
            "api_key": "",
            "api_url": "https://api.openai.com/v1/engines/davinci/completions",
            "save_location": os.path.expanduser("~/Desktop")
        }
        save_config(default_config)
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
