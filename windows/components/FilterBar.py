import sys

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout
from PySide6.QtGui import QColor, Qt

from const import const


class QStringList:
    pass


class FilterBar(QWidget):
    filter_changed = Signal(str)

    def __init__(self):
        super().__init__()

        self.filter_tree = None
        self.setWindowTitle("Filters")
        self.layout = QVBoxLayout(self)

        self.tl = None
        self.blurry = None
        self.errored = None

        self.setup()

    def setup(self):
        self.filter_tree = QTreeWidget(self)
        self.filter_tree.setColumnCount(1)
        self.filter_tree.setHeaderLabels(["Category", "Count"])

        self.layout.addWidget(self.filter_tree)

        self.tl = QTreeWidgetItem(self.filter_tree)
        self.tl.setText(0, const.STR.NOTHING_SCANNED)
        self.tl.setText(1, "0")

        self.blurry = QTreeWidgetItem(self.tl)
        self.blurry.setText(0, const.CATEGORY.BLURRY)
        self.blurry.setText(1, "0")

        self.errored = QTreeWidgetItem(self.tl)
        self.errored.setText(0, const.CATEGORY.ERRORED)
        self.errored.setText(1, "0")

        self.filter_tree.itemSelectionChanged.connect(self.on_tree_widget_selection_changed)

    def update_counts(self, counts_hash):
        # self.tl.setText(0, counts_hash['path'])
        self.tl.setText(1, str(counts_hash[const.CATEGORY.ALL]))
        self.blurry.setText(1, str(counts_hash[const.CATEGORY.BLURRY]))
        self.errored.setText(1, str(counts_hash[const.CATEGORY.ERRORED]))

    def update_scanned_folder_label(self, path=None):
        if path:
            self.tl.setText(0, path)
        else:
            self.tl.setText(0, "(Nothing scanned yet)")

    def on_tree_widget_selection_changed(self):
        selected = self.get_selected_item()
        self.filter_changed.emit(selected)

    def get_selected_item(self):
        items = self.filter_tree.selectedItems()
        if len(items) is not 0:
            selected = items[0].text(0)
        else:
            selected = const.CATEGORY.ALL

        if selected not in list(const.CATEGORY.keys()):
            selected = const.CATEGORY.ALL

        return selected

