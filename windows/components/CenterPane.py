import logging

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton

import const
from models.ScannedImage import ScannedImage
from preferences import prefs
from windows.components.ImageList import ImageList
from windows.dialogs.MassDeleteConfirmation import MassDeleteConfirmation

logging.basicConfig(level=const.LOG_LEVEL)


class CenterPane(QWidget):
    user_requested_deletion = Signal(object, str)  # object is a list of ScannedImage

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.image_list = ImageList()

        self.button_pane = QHBoxLayout()

        self.button_pane_right = QHBoxLayout()
        self.button_pane_left = QHBoxLayout()

        self.btn_trash = QPushButton("&Remove")
        self.btn_checkall = QPushButton("&Check all")
        self.btn_uncheckall = QPushButton("&Uncheck all")

        self.setup()

    def setup(self):
        self.layout.addWidget(self.image_list)

        self.button_pane_left.addWidget(self.btn_checkall)
        self.button_pane_left.addWidget(self.btn_uncheckall)
        self.button_pane_right.addWidget(self.btn_trash)

        self.button_pane.addLayout(self.button_pane_left)
        self.button_pane.addStretch()
        self.button_pane.addLayout(self.button_pane_right)

        self.btn_checkall.clicked.connect(self.on_btn_checkall_clicked)
        self.btn_uncheckall.clicked.connect(self.on_btn_uncheckall_clicked)
        self.btn_trash.clicked.connect(self.on_btn_trash_clicked)

        self.layout.addLayout(self.button_pane)

    def get_image_list_widget(self):
        return self.image_list

    def remove_image_from_image_list(self, image: ScannedImage):
        self.image_list.remove_image(image)

    def refresh_image_list(self):
        self.image_list.update_image_lists()

    #####################
    # event handlers
    #####################
    def on_btn_checkall_clicked(self):
        self.image_list.set_all_checked()

    def on_btn_uncheckall_clicked(self):
        self.image_list.set_all_unchecked()

    def on_btn_trash_clicked(self):
        slated_for_execution = self.image_list.get_checked_images()
        deletion_type = prefs().get_pref(const.PREFS.GLOBAL.NAME, const.PREFS.GLOBAL.ON_REMOVAL_ACTION,
                                         const.PREFS.GLOBAL.ON_REMOVAL_ACTION_VALUES.default)

        dlg = MassDeleteConfirmation(slated_for_execution)
        clicked = dlg.exec()

        # if clicked == QDialogButtonBox.Ok: #doesnt work
        if clicked == 1:
            logging.info("CenterPane about to dispatch request for deletion for %i images" % len(slated_for_execution))
            self.user_requested_deletion.emit(slated_for_execution, deletion_type)
