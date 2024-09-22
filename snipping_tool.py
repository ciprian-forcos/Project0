# snipping_tool.py
from PyQt5 import QtWidgets, QtGui, QtCore
from PIL import ImageGrab
import keyboard
import sys
import utils
from settings import SettingsMenu
from response_window import ResponseWindow

class SnippingTool(QtWidgets.QWidget):
    is_drawing = False
    start_point = QtCore.QPoint()
    end_point = QtCore.QPoint()

    def __init__(self, screenshot):
        super().__init__()
        self.screenshot = screenshot
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.showFullScreen()
        self.overlay = QtGui.QPixmap(self.screenshot.toImage())
        self.setCursor(QtCore.Qt.CrossCursor)
        self.init_shortcuts()

    def init_shortcuts(self):
        # Define shortcuts to exit the wizard
        exit_shortcuts = ['esc', 'ctrl+q', 'ctrl+c', 'shift+1']
        for sc in exit_shortcuts:
            keyboard.add_hotkey(sc, self.exit_wizard)

    def exit_wizard(self):
        keyboard.unhook_all_hotkeys()
        self.close()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(0, 0, self.overlay)
        if self.is_drawing:
            rect = QtCore.QRect(self.start_point, self.end_point)
            painter.setPen(QtGui.QPen(QtCore.Qt.red, 2))
            painter.drawRect(rect.normalized())

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.is_drawing = True
            self.start_point = event.pos()
            self.end_point = event.pos()
            self.update()
        elif event.button() == QtCore.Qt.RightButton:
            self.open_settings_menu(event.globalPos())

    def mouseMoveEvent(self, event):
        if self.is_drawing:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.is_drawing = False
            self.end_point = event.pos()
            self.process_snip()
            self.close()

    def open_settings_menu(self, position):
        self.settings_menu = SettingsMenu()
        self.settings_menu.move(position)
        self.settings_menu.show()

    def process_snip(self):
        rect = QtCore.QRect(self.start_point, self.end_point).normalized()
        cropped = self.screenshot.copy(rect)
        # Proceed to display in response window
        self.response_window = ResponseWindow(cropped)
        self.response_window.show()

    def closeEvent(self, event):
        keyboard.unhook_all_hotkeys()
        event.accept()
