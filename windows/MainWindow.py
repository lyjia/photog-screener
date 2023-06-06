from PySide6.QtCore import QThread
from PySide6.QtWidgets import QMainWindow, QDockWidget, QListWidget, QFileDialog, QProgressBar, QLabel
from PySide6.QtGui import Qt

from scanners.RecursiveDirectoryScanner import RecursiveDirectoryScanner
from windows.components.FilterBar import FilterBar
import logging

logging.basicConfig(level=logging.INFO)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        self.setWindowTitle("PhotogScreener by Lyjia")

        self.directory_scanner = None
        self.scanner_thread = None
        self.status_label = None
        self.progress_bar = None

        self.previous_scan = None
        self.previous_counts = None

        self.filter_bar = None

        self.create_menus()
        self.create_dock_widgets()
        self.create_statusbar()
        self.set_up_central_widget()

        self.set_up_for_new_run()

    ########################
    # setup
    ########################

    def create_menus(self):
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction("&Scan Folder...").triggered.connect(self.file_scan_folder_action)
        file_menu.addAction("&Quit").triggered.connect(self.file_quit_action)

        view_menu = self.menuBar().addMenu("&View")
        view_menu.addAction("&Image Preview/Info")

        help_menu = self.menuBar().addMenu("&Help")
        help_menu.addAction("&About...")

    def create_toolbars(self):
        fileToolbar = self.addToolBar("File")

    def create_dock_widgets(self):

        # create the filter widget
        dockWidget = QDockWidget("Filters", self)
        dockWidget.setAllowedAreas(Qt.LeftDockWidgetArea)
        dockWidget.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.filter_bar = FilterBar()
        dockWidget.setWidget(self.filter_bar)
        self.addDockWidget(Qt.LeftDockWidgetArea, dockWidget)

    def create_statusbar(self):
        self.statusBar()
        self.progress_bar = QProgressBar()
        self.status_label = QLabel()
        self.statusBar().addWidget(self.progress_bar)
        self.statusBar().addWidget(self.status_label)

    def set_up_central_widget(self):
        central = QListWidget()
        self.setCentralWidget(central)

    def set_up_for_new_run(self, path=None):
        self.previous_scan = {
            'path':    path,
            'all':     [],
            'blurry':  [],
            'errored': []
        }

        self.previous_counts = {
            'all':     0,
            'blurry':  0,
            'errored': 0
        }

        self.progress_bar.show()
        self.filter_bar.update_counts(self.previous_counts)
        self.filter_bar.update_scanned_folder_label(path)

    #############################
    # UI actions
    #############################
    def set_enabled(self, value):
        if value is True:
            pass
        else:
            pass

    #################
    # menu actions
    #################

    def file_scan_folder_action(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setDirectory("G:\\Pictures\\PhotogScreener test folder\\test1")

        if dialog.exec_():
            folderName = dialog.selectedFiles()[0]
            self.start_directory_scan(folderName)
        else:
            logging.info("User cancelled dialog box")

    def file_quit_action(self):
        exit(0)

    #################################
    # directory scanner
    #################################
    def start_directory_scan(self, target_path, options={}):
        self.set_enabled(False)
        self.set_up_for_new_run(target_path)

        self.scanner_thread = QThread()
        self.directory_scanner = RecursiveDirectoryScanner(target_path)
        self.directory_scanner.moveToThread(self.scanner_thread)

        # connect events
        self.directory_scanner.file_found.connect(self.on_scan_file_found)
        self.directory_scanner.file_scanned.connect(self.on_scan_file_scanned)
        self.directory_scanner.scan_complete.connect(self.on_scan_complete)
        self.scanner_thread.started.connect(self.directory_scanner.scan)

        # go!
        self.scanner_thread.start()

    def on_scan_file_found(self, file_path, x, count):
        self.status_label.setText("Scanning %s..." % file_path)
        self.progress_bar.setValue(x)
        self.progress_bar.setMaximum(count)
        pass

    def on_scan_file_scanned(self, path, scanned_image):
        self.previous_scan['all'].append(scanned_image)
        self.previous_counts['all'] += 1

        if scanned_image.is_blurry:
            self.previous_scan['blurry'].append(scanned_image)
            self.previous_counts['blurry'] += 1

        if scanned_image.error:
            self.previous_scan['errored'].append(scanned_image)
            self.previous_counts['errored'] += 1

        self.filter_bar.update_counts(self.previous_counts)

    def on_scan_complete(self):
        self.set_enabled(True)
        self.progress_bar.hide()
        self.status_label.setText("Finished scanning %i images." % len(self.previous_scan['all']))
