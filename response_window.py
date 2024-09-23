# response_window.py
from PyQt5 import QtWidgets, QtGui, QtCore
import openai
from utils import load_config
import threading
import os
from PIL import Image
import pytesseract

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
        if pixmap.width() > 500 or pixmap.height() > 600:
            pixmap = pixmap.scaled(500, 600, QtCore.Qt.KeepAspectRatio)
        image_label.setPixmap(pixmap)
        layout.addWidget(image_label)

        # Right: AI Response
        self.response_text = QtWidgets.QTextEdit()
        self.response_text.setReadOnly(True)
        self.response_text.setText('Processing...')
        layout.addWidget(self.response_text)

        self.setLayout(layout)

    def process_image(self):
        # Start OCR and API call in a separate thread
        self.thread = threading.Thread(target=self.run_ocr_and_query)
        self.thread.start()

    def run_ocr_and_query(self):
        try:
            # Step 1: OCR - Extract text from the image
            image = Image.open(self.image_path)
            text = pytesseract.image_to_string(image)

            # Step 2: OpenAI API Call using the new SDK
            # Initialize the OpenAI client
            client = openai.OpenAI(
                api_key=self.config.get('api_key'),
                # If you have a custom API base URL
                base_url=self.config.get('api_url', 'https://api.openai.com/v1')
            )

            # Make the API call using the new syntax
            chat_completion = client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=[
                    {
                        "role": "user",
                        "content": text
                    }
                ]
            )

            # Extract the AI's response
            ai_response = chat_completion.choices[0].message.content

            # Step 3: Update the UI in the main thread
            QtCore.QMetaObject.invokeMethod(
                self.response_text,
                "setText",
                QtCore.Qt.QueuedConnection,
                QtCore.Q_ARG(str, ai_response)
            )
        except openai.APIError as e:
            # Handle API errors
            error_message = f"API Error: {e}"
            self.display_error(error_message)
        except Exception as e:
            # Handle other exceptions
            error_message = f"Error: {e}"
            self.display_error(error_message)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif event.key() == QtCore.Qt.Key_Q and event.modifiers() & QtCore.Qt.ControlModifier:
            self.close()
        elif event.key() == QtCore.Qt.Key_C and event.modifiers() & QtCore.Qt.ControlModifier:
            self.close()
        elif event.key() == QtCore.Qt.Key_1 and event.modifiers() & QtCore.Qt.ShiftModifier:
            self.close()
        else:
            super().keyPressEvent(event)

    def display_error(self, message):
        # Update the UI with the error message
        QtCore.QMetaObject.invokeMethod(
            self.response_text,
            "setText",
            QtCore.Qt.QueuedConnection,
            QtCore.Q_ARG(str, message)
        )
