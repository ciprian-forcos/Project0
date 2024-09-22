# main.py
import sys
from PyQt5 import QtWidgets, QtCore
from snipping_tool import SnippingTool
from pynput import keyboard
import threading

class HotkeyListener(QtCore.QObject):
    hotkey_pressed = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener_thread = threading.Thread(target=self.listener.start)
        self.listener_thread.daemon = True  # Daemonize thread

    def start(self):
        self.listener_thread.start()

    def on_press(self, key):
        try:
            if key == keyboard.KeyCode.from_char('o') and keyboard.Controller().ctrl_pressed:
                self.hotkey_pressed.emit()
        except AttributeError:
            pass  # Handle special keys that don't have 'char' attribute

def main():
    app = QtWidgets.QApplication(sys.argv)
    snip_tool = SnippingTool()
    listener = HotkeyListener()
    listener.hotkey_pressed.connect(snip_tool.start_snipping)
    listener.start()
    print("Project01 is running. Press Ctrl+O to snip.")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
