# main.py
import sys
import keyboard
from PyQt5 import QtWidgets
from snipping_tool import SnippingTool
from utils import load_config

def start_snipping_tool():
    app = QtWidgets.QApplication(sys.argv)
    window = SnippingTool()
    window.show()
    app.exec_()

def on_hotkey():
    keyboard.remove_hotkey('ctrl+o')
    start_snipping_tool()
    keyboard.add_hotkey('ctrl+o', on_hotkey)

if __name__ == '__main__':
    config = load_config()
    keyboard.add_hotkey('ctrl+o', on_hotkey)
    print("Project01 is running. Press Ctrl+O to snip.")
    keyboard.wait()
