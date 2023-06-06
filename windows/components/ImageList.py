from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QListWidget, QListView


class ImageList(QListView):

    def __init__(self):
        super().__init__()
        self.model = QStandardItemModel(self)
        self.image_list_hash = None

    # you will need to call update_viewed_filter to display selected filter
    # immediately after calling this
    def update_image_lists(self, image_list_hash):
        self.image_list_hash = image_list_hash

    def update_viewed_filter(self, filter_name):
        self.model.clear()
        for item in self.image_list_hash[filter_name]:
            self.model.appendRow(item)
        self.setModel(self.model)