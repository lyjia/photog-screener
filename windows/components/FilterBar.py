import sys
from PySide6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout
from PySide6.QtGui import QColor, Qt


class QStringList:
    pass


class FilterBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Filters")
        self.tl = None
        self.blurry = None
        self.setup()

    def setup(self):
        filterTree = QTreeWidget(self)
        filterTree.setColumnCount(1)
        filterTree.setHeaderLabels(["Category", "Count"])

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(filterTree)

        self.tl = QTreeWidgetItem(filterTree)
        self.tl.setText(0, "(Nothing scanned yet)")
        self.tl.setText(1, "321")

        self.blurry = QTreeWidgetItem(self.tl)
        self.blurry.setText(0, "Blurry")
        self.blurry.setText(1, "123")

        #self.tl.addChild(self.blurry)

    def update_counts(self, counts_hash):
        self.tl.setText(0, counts_hash['path'])
        self.blurry.setText(0, counts_hash['counts_blurry_laplacian'])
