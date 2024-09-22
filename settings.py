# settings.py
from PyQt5 import QtWidgets, QtCore
import utils

class SettingsMenu(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = utils.load_config()
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(QtCore.Qt.Popup)
        layout = QtWidgets.QFormLayout()

        self.api_key_input = QtWidgets.QLineEdit(self.config.get('api_key', ''))
        layout.addRow('API Key:', self.api_key_input)

        self.api_url_input = QtWidgets.QLineEdit(self.config.get('api_url', ''))
        layout.addRow('API URL:', self.api_url_input)

        self.save_location_input = QtWidgets.QLineEdit(self.config.get('save_location', ''))
        browse_button = QtWidgets.QPushButton('Browse')
        browse_button.clicked.connect(self.browse_save_location)
        save_location_layout = QtWidgets.QHBoxLayout()
        save_location_layout.addWidget(self.save_location_input)
        save_location_layout.addWidget(browse_button)
        layout.addRow('Save Location:', save_location_layout)

        save_button = QtWidgets.QPushButton('Save Settings')
        save_button.clicked.connect(self.save_settings)
        cancel_button = QtWidgets.QPushButton('Cancel')
        cancel_button.clicked.connect(self.cancel_settings)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        layout.addRow(buttons_layout)

        self.setLayout(layout)

    def browse_save_location(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Save Location")
        if directory:
            self.save_location_input.setText(directory)

    def save_settings(self):
        self.config['api_key'] = self.api_key_input.text()
        self.config['api_url'] = self.api_url_input.text()
        self.config['save_location'] = self.save_location_input.text()
        utils.save_config(self.config)
        self.close()

    def cancel_settings(self):
        self.close()

    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Escape, QtCore.Qt.Key_C, QtCore.Qt.Key_Q):
            self.close()
