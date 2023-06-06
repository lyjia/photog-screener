from PySide6.QtWidgets import QMainWindow, QDockWidget, QListWidget
from PySide6.QtGui import Qt
from windows.components.FilterBar import FilterBar

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("PhotogScreener by Lyjia")
        self.createMenus()
        #self.createToolbars()
        self.createDockWidgets()
        self.setUpCentralWidget()
        pass

    def createMenus(self):
        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction("Scan Folder...")
        file_menu.addAction("Quit")

        view_menu = self.menuBar().addMenu("View")
        view_menu.addAction("Image Preview/Info")

        help_menu = self.menuBar().addMenu("Help")
        help_menu.addAction("About...")

    def createToolbars(self):
        fileToolbar = self.addToolBar("File")

    def createDockWidgets(self):

        # create the filter widget
        dockWidget = QDockWidget("Filters", self)
        dockWidget.setAllowedAreas(Qt.LeftDockWidgetArea)
        dockWidget.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
        leftBar = FilterBar()
        dockWidget.setWidget(leftBar)
        self.addDockWidget(Qt.LeftDockWidgetArea, dockWidget)

    def setUpCentralWidget(self):
        central = QListWidget()
        self.setCentralWidget(central)
