from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout

import const


class MassDeleteConfirmation(QDialog):

    def __init__(self, target_images):
        super().__init__()

        self.setWindowTitle("Are you ABSOLUTELY sure?")
        self.target_images = target_images

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(
            "You are about to send all checked images to the %s, are you sure you wish to do this?" % const.STR.TRASH)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
