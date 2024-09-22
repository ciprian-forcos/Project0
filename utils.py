# utils.py
import random
import string

def generate_filename(extension='jpeg'):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + f'.{extension}'
