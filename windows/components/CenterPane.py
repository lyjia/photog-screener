from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QDialogButtonBox

from const import Const
from models.ScannedImage import ScannedImage
from windows.components.ImageList import ImageList
from windows.dialogs.MassDeleteConfirmation import MassDeleteConfirmation
from workers.DeletionWorker import DeletionWorker
import logging
logging.basicConfig(level=Const.LOG_LEVEL)

class CenterPane(QWidget):

    deletion_started = Signal(int)
    image_deleted = Signal(str)
    deletion_complete = Signal(int)

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.image_list = ImageList()

        self.button_pane = QHBoxLayout()

        self.button_pane_right = QHBoxLayout()
        self.button_pane_left = QHBoxLayout()

        self.deletion_thread = None
        self.deletion_controller = None

        self.btn_trash = QPushButton("&Delete")
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

    #####################
    # event handlers
    #####################
    def on_btn_checkall_clicked(self):
        self.image_list.set_all_checked()

    def on_btn_uncheckall_clicked(self):
        self.image_list.set_all_unchecked()

    def on_btn_trash_clicked(self):
        slated_for_execution = self.image_list.get_checked_images()

        dlg = MassDeleteConfirmation(slated_for_execution)
        clicked = dlg.exec()

        #if clicked == QDialogButtonBox.Ok: #doesnt work
        if clicked == 1:
            self.delete_all_images(slated_for_execution)

    #####################################
    # image deletion
    #####################################
    def delete_all_images(self, to_delete):
        self.deletion_thread = QThread()
        self.deletion_thread.setObjectName("Delete images")
        self.deletion_controller = DeletionWorker(to_delete)

        self.deletion_controller.moveToThread(self.deletion_thread)

        self.deletion_thread.started.connect(self.deletion_controller.delete_all)
        self.deletion_controller.deletion_started.connect(self.on_deletion_started)
        self.deletion_controller.deletion_error.connect(self.on_deletion_error)
        self.deletion_controller.deletion_complete.connect(self.on_deletion_completed)
        self.deletion_controller.image_deleted.connect(self.on_image_deleted)

        self.deletion_thread.start()

    def on_deletion_started(self, count):
        self.deletion_started.emit(count)

    def on_deletion_error(self, str):
        logging.error(str)

    def on_image_deleted(self, image: ScannedImage):
        self.image_deleted.emit(image.image_path)

    def on_deletion_completed(self):
        self.deletion_thread.exit()
        self.deletion_complete.emit()
