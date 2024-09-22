# main.py
import sys
from PyQt5 import QtWidgets, QtGui
from snipping_tool import SnippingTool
from settings import SettingsMenu  # Corrected import

class SnipApp(QtWidgets.QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.snipping_tool = None
        # If you need to instantiate SettingsMenu here, uncomment the next line
        # self.settings_menu = SettingsMenu()
        self.init_hotkeys()

    def init_hotkeys(self):
        # Use PyQt's native hotkey system
        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+O'), None)
        shortcut.activated.connect(self.start_snipping_tool)
        # Keep a reference to prevent garbage collection
        self.hotkey = shortcut

    def start_snipping_tool(self):
        if self.snipping_tool is None:
            screen = self.primaryScreen()
            screenshot = screen.grabWindow(0)
            self.snipping_tool = SnippingTool(screenshot)
            self.snipping_tool.show()
            self.snipping_tool.closed.connect(self.snipping_tool_closed)

    def snipping_tool_closed(self):
        self.snipping_tool = None

if __name__ == '__main__':
    app = SnipApp(sys.argv)
    print("Project01 is running. Press Ctrl+O to snip.")
    sys.exit(app.exec_())
