# snipping_tool.py
from PyQt5 import QtWidgets, QtGui, QtCore
from settings import SettingsMenu
from response_window import ResponseWindow
import utils

class SnippingTool(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.snip_overlay = None

    @QtCore.pyqtSlot()
    def start_snipping(self):
        self.screen = QtWidgets.QApplication.primaryScreen()
        self.screenshot = self.screen.grabWindow(0)
        self.snip_overlay = SnipOverlay(self.screenshot)
        self.snip_overlay.snip_complete.connect(self.on_snip_complete)
        self.snip_overlay.show()

    def on_snip_complete(self, pixmap):
        # Save the pixmap to file
        filename = utils.generate_filename('jpeg')
        save_location = utils.get_save_location()
        filepath = QtCore.QDir(save_location).filePath(filename)
        pixmap.save(filepath, 'JPEG')
        # Now, proceed to open the response window
        self.response_window = ResponseWindow(pixmap)
        self.response_window.show()

class SnipOverlay(QtWidgets.QWidget):
    snip_complete = QtCore.pyqtSignal(QtGui.QPixmap)

    def __init__(self, screenshot):
        super().__init__()
        self.screenshot = screenshot
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setWindowState(QtCore.Qt.WindowActive | QtCore.Qt.WindowFullScreen)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.is_drawing = False
        self.settings_menu = None
        self.setCursor(QtCore.Qt.CrossCursor)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(0, 0, self.screenshot)
        if self.is_drawing:
            rect = QtCore.QRect(self.begin, self.end)
            painter.setPen(QtGui.QPen(QtGui.QColor('red'), 2))
            painter.drawRect(rect.normalized())

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.begin = event.pos()
            self.end = event.pos()
            self.is_drawing = True
            self.update()
        elif event.button() == QtCore.Qt.RightButton:
            self.open_settings_menu(event.globalPos())

    def mouseMoveEvent(self, event):
        if self.is_drawing:
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.end = event.pos()
            self.is_drawing = False
            self.capture_snip()
            self.snip_complete.emit(self.captured_pixmap)
            self.close()

    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Escape, QtCore.Qt.Key_C, QtCore.Qt.Key_Q):
            self.close()

    def capture_snip(self):
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())
        rect = QtCore.QRect(x1, y1, x2 - x1, y2 - y1)
        self.captured_pixmap = self.screenshot.copy(rect)

    def open_settings_menu(self, position):
        self.settings_menu = SettingsMenu(self)
        self.settings_menu.move(position)
        self.settings_menu.show()
