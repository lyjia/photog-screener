from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout, QMessageBox

from const import PREFS, STR
from preferences import prefs


class MassDeleteConfirmation(QDialog):

    def __init__(self, target_images):
        super().__init__()

        self.target_images = target_images

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()

        if prefs().get_pref(PREFS.GLOBAL.NAME, PREFS.GLOBAL.ON_REMOVAL_ACTION,
                            PREFS.GLOBAL.ON_REMOVAL_ACTION_VALUES.default) == PREFS.GLOBAL.ON_REMOVAL_ACTION_VALUES.TO_TRASH:
            #self.setWindowIcon( QPixmap(QMessageBox.Icon.Warning) )
            self.setWindowTitle("Are you sure?")
            message = QLabel(
                "You are about to send all checked images to the %s, are you sure you wish to do this?" % STR.TRASH)
        else:
            #self.setWindowIcon( QPixmap(QMessageBox.Icon.Critical) )
            self.setWindowTitle("Are you ABSOLUTELY sure?")
            message = QLabel("You are about to DELETE ALL CHECKED IMAGES, are you sure you wish to do this?")

        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
