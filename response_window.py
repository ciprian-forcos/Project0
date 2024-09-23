# response_window.py
from PyQt5 import QtWidgets, QtGui, QtCore
import threading
import openai
import os
from utils import load_config
import pytesseract
from PIL import Image

class ResponseWindow(QtWidgets.QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.config = load_config()
        self.init_ui()
        self.process_image()

    def init_ui(self):
        self.setWindowTitle('AI Response')
        self.resize(1000, 600)
        layout = QtWidgets.QHBoxLayout()

        # Left: Image Display
        image_label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(self.image_path)
        if pixmap.width() > 800 or pixmap.height() > 600:
            pixmap = pixmap.scaled(800, 600, QtCore.Qt.KeepAspectRatio)
        image_label.setPixmap(pixmap)
        layout.addWidget(image_label)

        # Right: AI Response
        self.response_text = QtWidgets.QTextEdit()
        self.response_text.setReadOnly(True)
        layout.addWidget(self.response_text)

        self.setLayout(layout)

    def process_image(self):
        threading.Thread(target=self.run_ocr_and_query).start()

    def run_ocr_and_query(self):
        # OCR
        image = Image.open(self.image_path)
        text = pytesseract.image_to_string(image)

        # OpenAI API Call
        openai.api_key = self.config.get('api_key')
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': text}]
        )
        ai_response = response['choices'][0]['message']['content']

        # Update UI
        self.response_text.setText(ai_response)
