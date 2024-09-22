# settings.py
from PyQt5 import QtWidgets, QtCore
import utils

class SettingsMenu(QtWidgets.QWidget):
    settings_saved = QtCore.pyqtSignal()
    settings_canceled = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = utils.load_config()
        self.init_ui()

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

        buttons = QtWidgets.QDialogButtonBox()
        save_btn = buttons.addButton('Save Settings', QtWidgets.QDialogButtonBox.AcceptRole)
        cancel_btn = buttons.addButton('Cancel', QtWidgets.QDialogButtonBox.RejectRole)
        buttons.accepted.connect(self.save_settings)
        buttons.rejected.connect(self.cancel_settings)
        layout.addWidget(buttons)

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
        self.settings_saved.emit()
        self.close()

    def cancel_settings(self):
        self.settings_canceled.emit()
        self.close()
