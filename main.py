# main.py
import sys
import keyboard
from PyQt5 import QtWidgets
from PIL import ImageGrab
from snipping_tool import SnippingTool

def start_snipping_tool():
    app = QtWidgets.QApplication(sys.argv)
    screen = QtWidgets.QApplication.primaryScreen()
    screenshot = screen.grabWindow(0)
    window = SnippingTool(screenshot)
    window.show()
    app.exec_()

def on_hotkey():
    keyboard.remove_hotkey(hotkey)
    start_snipping_tool()
    register_hotkey()

def register_hotkey():
    global hotkey
    hotkey = keyboard.add_hotkey('ctrl+o', on_hotkey)

if __name__ == '__main__':
    register_hotkey()
    print("Project01 is running. Press Ctrl+O to snip.")
    keyboard.wait()
