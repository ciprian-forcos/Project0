# snipping_tool.py
from PyQt5 import QtWidgets, QtGui, QtCore
from response_window import ResponseWindow
from settings import SettingsMenu
import utils

class SnippingTool(QtWidgets.QWidget):
    closed = QtCore.pyqtSignal()

    def __init__(self, screenshot):
        super().__init__()
        self.screenshot = screenshot
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.showFullScreen()
        self.overlay = QtGui.QPixmap(self.screenshot)
        self.setCursor(QtCore.Qt.CrossCursor)
        self.is_drawing = False
        self.start_point = QtCore.QPoint()
        self.end_point = QtCore.QPoint()

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
        self.settings_menu = SettingsMenu(self)
        self.settings_menu.move(position)
        self.settings_menu.settings_saved.connect(self.restart_snipping)
        self.settings_menu.settings_canceled.connect(self.restart_snipping)
        self.settings_menu.show()

    def process_snip(self):
        rect = QtCore.QRect(self.start_point, self.end_point).normalized()
        cropped = self.screenshot.copy(rect)
        self.response_window = ResponseWindow(cropped)
        self.response_window.show()

    def restart_snipping(self):
        self.close()
        self.parent().start_snipping_tool()

    def keyPressEvent(self, event):
        # Handle global exit shortcuts
        if event.key() in (QtCore.Qt.Key_Escape, QtCore.Qt.Key_C):
            self.close()

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()
