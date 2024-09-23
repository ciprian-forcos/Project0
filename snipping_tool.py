# snipping_tool.py
from PyQt5 import QtWidgets, QtGui, QtCore
from settings import SettingsMenu
from response_window import ResponseWindow
from utils import load_config, save_config
import os
import random
import string

def generate_filename():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + '.jpeg'

class SnippingTool(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.is_drawing = False
        self.start_point = QtCore.QPoint()
        self.end_point = QtCore.QPoint()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.showFullScreen()
        self.screen = QtWidgets.QApplication.primaryScreen()
        self.screenshot = self.screen.grabWindow(0)
        self.overlay = QtGui.QPixmap(self.screenshot)
        self.setCursor(QtCore.Qt.CrossCursor)
        self.config = load_config()

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
            self.save_snip()
            self.close()
            self.open_response_window()

    def keyPressEvent(self, event):
            if event.key() == QtCore.Qt.Key_Escape:
                self.close()
            elif event.key() == QtCore.Qt.Key_Q and event.modifiers() & QtCore.Qt.ControlModifier:
                self.close()
            elif event.key() == QtCore.Qt.Key_C and event.modifiers() & QtCore.Qt.ControlModifier:
                self.close()
            elif event.key() == QtCore.Qt.Key_1 and event.modifiers() & QtCore.Qt.ShiftModifier:
                # Shift+1 corresponds to '!'
                self.close()
            else:
                super().keyPressEvent(event)

    def save_snip(self):
        rect = QtCore.QRect(self.start_point, self.end_point).normalized()
        cropped = self.screenshot.copy(rect)
        filename = generate_filename()
        save_location = self.config.get('save_location', os.path.expanduser('~/Desktop'))
        filepath = os.path.join(save_location, filename)
        cropped.save(filepath, 'JPEG')
        self.snip_filepath = filepath

    def open_settings_menu(self, position):
        self.settings_menu = SettingsMenu()
        self.settings_menu.move(position)
        self.settings_menu.show()

    def open_response_window(self):
        self.response_window = ResponseWindow(self.snip_filepath)
        self.response_window.show()
