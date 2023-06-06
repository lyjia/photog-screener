import sys
from PySide6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout
from PySide6.QtGui import QColor, Qt


class QStringList:
    pass


class FilterBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Filters")
        self.layout = QVBoxLayout(self)

        self.tl = None
        self.blurry = None

        self.setup()

    def setup(self):
        filterTree = QTreeWidget(self)
        filterTree.setColumnCount(1)
        filterTree.setHeaderLabels(["Category", "Count"])

        self.layout.addWidget(filterTree)

        self.tl = QTreeWidgetItem(filterTree)
        self.tl.setText(0, "(Nothing scanned yet)")
        self.tl.setText(1, "321")

        self.blurry = QTreeWidgetItem(self.tl)
        self.blurry.setText(0, "Blurry")
        self.blurry.setText(1, "123")

        self.errored = QTreeWidgetItem(self.tl)
        self.errored.setText(0, "Errored")
        self.errored.setText(1, "12")

    def update_counts(self, counts_hash):
        # self.tl.setText(0, counts_hash['path'])
        self.tl.setText(1, counts_hash['all'])
        self.blurry.setText(1, counts_hash['blurry'])
        self.errored.setText(1, counts_hash['errored'])
