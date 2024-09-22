# response_window.py
from PyQt5 import QtWidgets, QtGui, QtCore
import openai
import utils
import os
import pytesseract
from PIL import Image
import tempfile

class ResponseWindow(QtWidgets.QWidget):
    def __init__(self, image_pixmap):
        super().__init__()
        self.image_pixmap = image_pixmap
        self.init_ui()
        self.process_image()

    def init_ui(self):
        self.setWindowTitle('Project01 Response')
        self.resize(1000, 600)

        layout = QtWidgets.QHBoxLayout()

        # Left side: Image
        image_label = QtWidgets.QLabel()
        pixmap = self.image_pixmap
        if pixmap.width() > 800 or pixmap.height() > 600:
            pixmap = pixmap.scaled(800, 600, QtCore.Qt.KeepAspectRatio)
        image_label.setPixmap(pixmap)
        layout.addWidget(image_label)

        # Vertical line
        vline = QtWidgets.QFrame()
        vline.setFrameShape(QtWidgets.QFrame.VLine)
        vline.setFrameShadow(QtWidgets.QFrame.Sunken)
        layout.addWidget(vline)

        # Right side: AI Response
        self.response_area = QtWidgets.QTextBrowser()
        self.response_area.setReadOnly(True)
        self.response_area.setText('Processing...')
        layout.addWidget(self.response_area)

        self.setLayout(layout)

    def process_image(self):
        # Extract text from image using pytesseract
        temp_image_path = None
        try:
            temp_dir = tempfile.mkdtemp()
            temp_image_path = os.path.join(temp_dir, 'temp_image.png')
            self.image_pixmap.save(temp_image_path)
            image = Image.open(temp_image_path)
            text_in_image = pytesseract.image_to_string(image)
        except Exception as e:
            self.response_area.setText(f"Error processing image: {e}")
            return
        finally:
            if temp_image_path and os.path.exists(temp_image_path):
                os.remove(temp_image_path)

        # Now, send text_in_image to OpenAI API
        self.thread = QtCore.QThread()
        self.worker = OpenAIWorker(text_in_image)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.display_response)
        self.worker.error.connect(self.display_error)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def display_response(self, text):
        self.response_area.setHtml(text)

    def display_error(self, error_message):
        self.response_area.setText(f"Error: {error_message}")

class OpenAIWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal(str)
    error = QtCore.pyqtSignal(str)

    def __init__(self, prompt_text):
        super().__init__()
        self.prompt_text = prompt_text

    def run(self):
        config = utils.load_config()
        api_key = config.get('api_key')
        if not api_key:
            self.error.emit("API Key not set. Please set it in the settings.")
            return
        openai.api_key = api_key
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[{'role': 'user', 'content': self.prompt_text}]
            )
            ai_response = response['choices'][0]['message']['content']
            self.finished.emit(ai_response)
        except Exception as e:
            self.error.emit(str(e))
