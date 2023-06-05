import sys
from PySide6.QtWidgets import QMainWindow, QWidget, QLineEdit, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, \
    QDockWidget, QTextEdit, QListWidget
from PySide6.QtGui import QColor, Qt
from windows.dockables.LeftBar import LeftBar
colors = [("Red", "#FF0000"),
          ("Green", "#00FF00"),
          ("Blue", "#0000FF"),
          ("Black", "#000000"),
          ("White", "#FFFFFF"),
          ("Electric Green", "#41CD52"),
          ("Dark Blue", "#222840"),
          ("Yellow", "#F9E56d")]


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Hello")
        self.createMenus()
        self.createToolbars()
        self.createDockWidgets()
        self.setUpCentralWidget()
        pass

    def createMenus(self):
        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction("New")
        file_menu.addAction("Open")
        file_menu.addAction("Save")

    def createToolbars(self):
        fileToolbar = self.addToolBar("File")

    def createDockWidgets(self):
        dockWidget = QDockWidget("Dock Widget", self)
        dockWidget.setAllowedAreas(Qt.LeftDockWidgetArea)
        leftBar = LeftBar()
        dockWidget.setWidget(leftBar)
        self.addDockWidget(Qt.LeftDockWidgetArea, dockWidget)

    def setUpCentralWidget(self):
        central = QListWidget()
        self.setCentralWidget(central)
