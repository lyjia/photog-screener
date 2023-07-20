from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QListWidget, QListView, QAbstractItemView

import const
from models.ScannedImage import ScannedImage


class ImageList(QListView):

    def __init__(self):
        super().__init__()
        self.model = QStandardItemModel(self)
        self.image_list_hash = {}
        self.viewed_filter = None

        self.setViewMode(QListView.ViewMode.IconMode)
        self.setGridSize(QSize(256, 256))
        self.setIconSize(QSize(192, 192))
        self.setMovement(QListView.Movement.Static)
        self.setResizeMode(QListView.ResizeMode.Adjust)
        # self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

    # you will need to call update_viewed_filter to display selected filter
    # immediately after calling this
    def update_image_lists(self, image_list_hash):
        self.image_list_hash = image_list_hash

    def update_viewed_filter(self, filter_name = None):
        self.model.clear()

        if filter_name is None:
            if self.viewed_filter is not None:
                filter_name = self.viewed_filter
            else:
                raise("viewed_filter must be set!")

        for item in self.image_list_hash[filter_name]:
            self.model.appendRow(item)

        self.setModel(self.model)
        self.viewed_filter = filter_name

    def set_all_checked(self):
        for i in range(self.model.rowCount()):
            for j in range(self.model.columnCount()):
                item = self.model.item(i, j)
                item.setCheckState(Qt.CheckState.Checked)

    def set_all_unchecked(self):
        for i in range(self.model.rowCount()):
            for j in range(self.model.columnCount()):
                item = self.model.item(i, j)
                item.setCheckState(Qt.CheckState.Unchecked)

    def get_checked_images(self):
        toret = []

        for i in range(self.model.rowCount()):
            for j in range(self.model.columnCount()):
                item = self.model.item(i, j)
                if item.checkState() == Qt.CheckState.Checked:
                    toret.append(item)

        return toret

    def remove_image(self, deleted: ScannedImage):
        for cat in const.CATEGORY.keys():
            for image in self.image_list_hash[cat]:
                if deleted.id == image.id:
                    self.image_list_hash[cat].remove(image)
                    break