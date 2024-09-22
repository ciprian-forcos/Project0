# settings.py
import json
import os
from PyQt5 import QtWidgets, QtGui, QtCore

CONFIG_FILE = 'config.json'

class SettingsMenu(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_config()
        self.init_ui()

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'w') as f:
                json.dump({
                    "api_key": "",
                    "api_url": "https://api.openai.com/v1/engines/davinci/completions",
                    "save_location": os.path.expanduser("~/Desktop")
                }, f)
        with open(CONFIG_FILE, 'r') as f:
            self.config = json.load(f)

    def save_config(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f)

    def init_ui(self):
        self.setWindowTitle('Settings')
        layout = QtWidgets.QFormLayout()

        self.api_key_input = QtWidgets.QLineEdit(self.config.get('api_key', ''))
        layout.addRow('API Key:', self.api_key_input)

        self.api_url_input = QtWidgets.QLineEdit(self.config.get('api_url', ''))
        layout.addRow('API URL:', self.api_url_input)

        self.save_location_input = QtWidgets.QLineEdit(self.config.get('save_location', ''))
        save_location_btn = QtWidgets.QPushButton('Browse')
        save_location_btn.clicked.connect(self.browse_save_location)
        save_location_layout = QtWidgets.QHBoxLayout()
        save_location_layout.addWidget(self.save_location_input)
        save_location_layout.addWidget(save_location_btn)
        layout.addRow('Save Location:', save_location_layout)

        buttons = QtWidgets.QHBoxLayout()
        save_btn = QtWidgets.QPushButton('Save Settings')
        save_btn.clicked.connect(self.save_settings)
        cancel_btn = QtWidgets.QPushButton('Cancel')
        cancel_btn.clicked.connect(self.cancel_settings)
        buttons.addWidget(save_btn)
        buttons.addWidget(cancel_btn)
        layout.addRow(buttons)

        self.setLayout(layout)

    def browse_save_location(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Save Location")
        if directory:
            self.save_location_input.setText(directory)

    def save_settings(self):
        self.config['api_key'] = self.api_key_input.text()
        self.config['api_url'] = self.api_url_input.text()
        self.config['save_location'] = self.save_location_input.text()
        self.save_config()
        self.close()
        # Re-enter screenshot wizard (handled by parent)

    def cancel_settings(self):
        self.close()
        # Revert settings and re-enter screenshot wizard (handled by parent)
