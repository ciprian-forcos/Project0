# response_window.py
import os
import json
from PyQt5 import QtWidgets, QtGui, QtCore
import openai
import utils

CONFIG_FILE = 'config.json'

class ResponseWindow(QtWidgets.QWidget):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.load_config()
        self.init_ui()
        self.get_ai_response()

    def load_config(self):
        with open(CONFIG_FILE, 'r') as f:
            self.config = json.load(f)
        openai.api_key = self.config.get('api_key')

    def init_ui(self):
        self.setWindowTitle('Project01')
        layout = QtWidgets.QHBoxLayout()

        # Display the screenshot
        self.image_label = QtWidgets.QLabel()
        pixmap = self.image

        # Resize image if necessary
        if pixmap.width() > 800 or pixmap.height() > 600:
            pixmap = pixmap.scaled(800, 600, QtCore.Qt.KeepAspectRatio)

        self.image_label.setPixmap(pixmap)
        layout.addWidget(self.image_label)

        # Divider
        divider = QtWidgets.QFrame()
        divider.setFrameShape(QtWidgets.QFrame.VLine)
        divider.setFrameShadow(QtWidgets.QFrame.Sunken)
        layout.addWidget(divider)

        # AI Response Area
        self.response_area = QtWidgets.QTextEdit()
        self.response_area.setReadOnly(True)
        self.response_area.setText('Loading...')
        layout.addWidget(self.response_area)

        self.setLayout(layout)
        self.resize(1000, 600)  # Adjust the window size as needed

    def get_ai_response(self):
        # Save the image temporarily
        temp_filename = utils.generate_filename('png')
        temp_filepath = os.path.join(self.config.get('save_location', os.path.expanduser('~/Desktop')), temp_filename)
        self.image.save(temp_filepath, 'PNG')

        # Read the image file
        with open(temp_filepath, 'rb') as image_file:
            image_data = image_file.read()

        # Remove the temporary file
        os.remove(temp_filepath)

        # Send the image to OpenAI API
        self.response_area.setText('Processing...')
        QtCore.QTimer.singleShot(100, self.call_openai_api)

    def call_openai_api(self):
        try:
            # Use OpenAI's image recognition or transcription as needed
            # For example purposes, we'll send a dummy request

            # Create a placeholder prompt (since OpenAI API doesn't process images directly in text completion)
            prompt = "Describe the content of the image."

            # Simulate API call
            response = openai.Completion.create(
                engine="davinci",
                prompt=prompt,
                max_tokens=150
            )
            text = response.choices[0].text.strip()
            self.response_area.setText(text)
        except Exception as e:
            self.response_area.setText(f"Error: {str(e)}")
