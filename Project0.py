import sys
import os
import random
import string
from PyQt5 import QtWidgets, QtGui, QtCore
from PIL import ImageGrab
import keyboard

# Function to generate a random 8-character filename
def generate_filename():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + '.jpeg'

# Main Window Class for the Cropping Tool
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

    def save_snip(self):
        rect = QtCore.QRect(self.start_point, self.end_point).normalized()
        cropped = self.screenshot.copy(rect)
        filename = generate_filename()
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        filepath = os.path.join(desktop, filename)
        cropped.save(filepath, 'JPEG')
        print(f"Saved snip as {filepath}")

# Function to initiate the snipping tool
def start_snipping_tool():
    app = QtWidgets.QApplication(sys.argv)
    screen = QtWidgets.QApplication.primaryScreen()
    screenshot = screen.grabWindow(0)
    window = SnippingTool(screenshot)
    window.show()
    app.exec_()

# Function to handle the hotkey event
def on_hotkey():
    # Remove the hotkey to prevent re-entry
    keyboard.remove_hotkey(hotkey)
    start_snipping_tool()
    # Re-register the hotkey after snipping is done
    register_hotkey()

# Function to register the hotkey
def register_hotkey():
    global hotkey
    hotkey = keyboard.add_hotkey('ctrl+o', on_hotkey)

if __name__ == '__main__':
    register_hotkey()
    print("Snipping tool is running. Press Ctrl+O to snip.")
    keyboard.wait()  # Keep the script running
