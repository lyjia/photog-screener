from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton

from windows.components.ImageList import ImageList


class CenterPane(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.image_list = ImageList()

        self.button_pane = QHBoxLayout()

        self.button_pane_right = QHBoxLayout()
        self.button_pane_left = QHBoxLayout()

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
        pass
