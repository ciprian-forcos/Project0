# response_window.py
import os
from PyQt5 import QtWidgets, QtGui, QtCore
import openai
import utils
from PIL import Image
import pytesseract  # Requires installation

class ResponseWindow(QtWidgets.QWidget):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.config = utils.load_config()
        self.init_ui()
        self.get_ai_response()

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
        self.response_area = QtWidgets.QTextBrowser()
        self.response_area.setReadOnly(True)
        layout.addWidget(self.response_area)

        self.setLayout(layout)
        self.resize(1000, 600)  # Adjust the window size as needed

        # Loading Indicator
        self.loading_label = QtWidgets.QLabel()
        movie = QtGui.QMovie('loading.gif')
        self.loading_label.setMovie(movie)
        movie.start()
        self.response_area.setViewportMargins(0, 0, 0, 0)
        self.response_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.response_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.response_area.setAlignment(QtCore.Qt.AlignCenter)
        self.response_area.setText('')
        self.response_area.setCentralWidget(self.loading_label)

    def get_ai_response(self):
        # Extract text from image using OCR
        temp_filepath = 'temp_image.png'
        self.image.save(temp_filepath, 'PNG')
        try:
            text_in_image = pytesseract.image_to_string(Image.open(temp_filepath))
        except Exception as e:
            self.response_area.setText(f"Error extracting text from image: {str(e)}")
            return
        finally:
            os.remove(temp_filepath)

        # Prepare the prompt
        prompt = f"Please help me with the following text:\n\n{text_in_image}"

        # Call OpenAI API asynchronously to avoid blocking the UI
        self.thread = QtCore.QThread()
        self.worker = OpenAIWorker(prompt, self.config.get('api_key'), self.config.get('api_url'))
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.display_response)
        self.worker.error.connect(self.display_error)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def display_response(self, response_text):
        self.response_area.setText(response_text)

    def display_error(self, error_message):
        self.response_area.setText(f"Error: {error_message}")

class OpenAIWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal(str)
    error = QtCore.pyqtSignal(str)

    def __init__(self, prompt, api_key, api_url):
        super().__init__()
        self.prompt = prompt
        self.api_key = api_key
        self.api_url = api_url

    def run(self):
        try:
            openai.api_key = self.api_key
            response = openai.Completion.create(
                engine="davinci",
                prompt=self.prompt,
                max_tokens=150
            )
            text = response.choices[0].text.strip()
            self.finished.emit(text)
        except Exception as e:
            self.error.emit(str(e))
