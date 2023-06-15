from PySide6.QtCore import QThread, QCoreApplication
from PySide6.QtWidgets import QMainWindow, QDockWidget, QListWidget, QFileDialog, QProgressBar, QLabel, QMessageBox, \
    QStyleFactory
from PySide6.QtGui import Qt, QPixmap, QIcon, QAction

from pathlib import Path
import const
from models.ScannedImage import ScannedImage
from windows.components.QActionWithMenu import QActionWithMenu
from workers.RecursiveDirectoryScanWorker import RecursiveDirectoryScanWorker
from windows.components.CenterPane import CenterPane
from windows.components.FilterBar import FilterBar
import logging

from windows.components.ImageList import ImageList
from preferences import prefs

logging.basicConfig(level=const.LOG_LEVEL)


class MainWindow(QMainWindow):
    def __init__(self, parent=None, style=None):
        super().__init__()

        self.setWindowTitle("PhotogScreener by Lyjia")

        # load window icon
        # adapted from https://stackoverflow.com/questions/17068003/application-icon-in-pyside-gui
        pixmap = QPixmap()
        pixmap.loadFromData(Path('res/icon.png').read_bytes())
        appIcon = QIcon(pixmap)
        self.setWindowIcon(appIcon)
        self.current_style = style

        # setup
        self.directory_scanner = None
        self.scanner_thread = None
        self.deleter_thread = None
        self.status_label = None
        self.progress_bar = None

        self.previous_scan = None
        self.previous_counts = None

        self.filter_bar = None
        self.central_image_list = None
        self.center_pane = None

        self.create_menus()
        self.create_dock_widgets()
        self.create_statusbar()
        self.set_up_central_image_list()

        self.set_up_for_new_run()

    ########################
    # setup
    ########################

    def create_menus(self):
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction("&Scan Folder...").triggered.connect(self.on_file_scan_folder_action)
        file_menu.addAction("&Quit").triggered.connect(self.on_file_quit_action)

        view_menu = self.menuBar().addMenu("&View")
        view_menu.addAction("&Image Preview/Info")

        options_menu = self.menuBar().addMenu("&Options")
        on_delete_menu = options_menu.addMenu("When &removing")
        for item in const.MENU.ON_REMOVAL.keys():

            # QAction doesn't give us a way to access the parent menu (which we need to uncheck all the other menu items)
            # so we stuff it into an attribute on the instantiated class
            act = on_delete_menu.addAction(item)
            act.setCheckable(True)
            act.__setattr__('parent_menu', on_delete_menu)
            act.triggered.connect(self.on_options_removal_select)
            if prefs().get_pref(const.PREFS.GLOBAL.NAME, const.PREFS.GLOBAL.ON_REMOVAL_ACTION,
                                const.MENU.ON_REMOVAL.TO_TRASH) == item:
                act.setChecked(True)

        options_menu.addSeparator()
        styles_menu = options_menu.addMenu("&Theme")
        for style in QStyleFactory.keys():
            act = styles_menu.addAction(style)
            act.setCheckable(True)
            if style.lower() == self.current_style.name().lower():
                act.setChecked(True)
            act.triggered.connect(self.on_options_theme_select)

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
        self.filter_bar.filter_changed.connect(self.on_filter_bar_selection_changed)
        dockWidget.setWidget(self.filter_bar)
        self.addDockWidget(Qt.LeftDockWidgetArea, dockWidget)

    def create_statusbar(self):
        self.statusBar()

        self.progress_bar = QProgressBar()

        self.status_label = QLabel()
        self.statusBar().addWidget(self.progress_bar)
        self.statusBar().addWidget(self.status_label)

        self.progress_bar.hide()

    def set_up_central_image_list(self):
        self.center_pane = CenterPane()
        self.central_image_list = self.center_pane.get_image_list_widget()
        self.setCentralWidget(self.center_pane)

        # set up event handlers for image deletion
        self.center_pane.deletion_started.connect(self.on_deletion_started)
        self.center_pane.image_deleted.connect(self.on_image_deleted)
        self.center_pane.deletion_complete.connect(self.on_deletion_finished)

    def set_up_for_new_run(self, path=None):
        self.previous_scan = {
            const.STR.PATH:         path,
            const.CATEGORY.ALL:     [],
            const.CATEGORY.BLURRY:  [],
            const.CATEGORY.ERRORED: []
        }

        self.previous_counts = {
            const.CATEGORY.ALL:     0,
            const.CATEGORY.BLURRY:  0,
            const.CATEGORY.ERRORED: 0
        }

        self.progress_bar.show()
        self.filter_bar.update_counts(self.previous_counts)
        self.filter_bar.update_scanned_folder_label(path)
        self.central_image_list.update_image_lists(self.previous_scan)
        self.central_image_list.update_viewed_filter(self.filter_bar.get_selected_item())

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

    def on_file_scan_folder_action(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setDirectory("T:\\PhotogScreenerTestFolder")

        if dialog.exec_():
            folderName = dialog.selectedFiles()[0]
            self.start_directory_scan(folderName)
        else:
            logging.info("User cancelled dialog box")

    def on_file_quit_action(self):
        exit(0)

    def on_options_theme_select(self):
        newstyle = self.sender().text()

        if newstyle != self.current_style:
            msgbox = QMessageBox()
            msgbox.setText(
                "%s must be restarted in order to save this change and apply the style. Do this now?" % const.APP.NAME)
            msgbox.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            msgbox.setIcon(QMessageBox.Icon.Question)
            msgbox.setDefaultButton(QMessageBox.StandardButton.Ok)
            ret = msgbox.exec()
            if ret == QMessageBox.StandardButton.Ok:
                prefs().set_pref(const.PREFS.GLOBAL.NAME, const.PREFS.GLOBAL.APPSTYLE, newstyle)
                QCoreApplication.exit(const.APP.EXIT_CODE_RESTART)

    # not your typical event handler
    def on_options_removal_select(self):
        me = self.sender()
        target = me.text()
        prefs().set_pref(const.PREFS.GLOBAL.NAME, const.PREFS.GLOBAL.ON_REMOVAL_ACTION, target)
        for action in me.parent_menu.children():
            if me is not action:
                action.setChecked(False)

    ##########################
    # control actions
    ##########################
    def on_filter_bar_selection_changed(self, label):
        logging.info("User changed filter to %s" % label)
        self.central_image_list.update_viewed_filter(label)

    #################################
    # directory scanner + events
    #################################
    def start_directory_scan(self, target_path, options={}):
        self.set_enabled(False)
        self.set_up_for_new_run(target_path)

        self.scanner_thread = QThread()
        self.scanner_thread.setObjectName("Scan %s" % target_path)
        self.directory_scanner = RecursiveDirectoryScanWorker(target_path)
        self.directory_scanner.moveToThread(self.scanner_thread)

        # connect events
        self.directory_scanner.file_found.connect(self.on_scan_file_found)
        self.directory_scanner.file_scanned.connect(self.on_scan_file_scanned)
        self.directory_scanner.scan_complete.connect(self.on_scan_complete)
        self.directory_scanner.scan_error.connect(self.on_scan_error)
        self.scanner_thread.started.connect(self.directory_scanner.scan)
        # go!
        self.scanner_thread.start()

    def on_scan_file_found(self, file_path, x, count):
        self.status_label.setText("Scanning %s..." % file_path)
        self.progress_bar.setValue(x)
        self.progress_bar.setMaximum(count)
        pass

    def on_scan_file_scanned(self, path, scanned_image: ScannedImage):
        # there seems to be an issue in passing objects between threads, because sometimes
        # ScannedImage comes back as its superclass, QStandardItem, which causes the following code to crash.
        # TODO: figure this out

        if type(scanned_image).__name__ != "ScannedImage":
            logging.error(
                "I got back a %s instead of ScannedImage! WTF mate??? Skipping!" % type(scanned_image).__name__)
            return

        self.previous_scan[const.CATEGORY.ALL].append(scanned_image)
        self.previous_counts[const.CATEGORY.ALL] += 1

        if scanned_image.is_blurry():
            self.previous_scan[const.CATEGORY.BLURRY].append(scanned_image)
            self.previous_counts[const.CATEGORY.BLURRY] += 1

        if scanned_image.error:
            self.previous_scan[const.CATEGORY.ERRORED].append(scanned_image)
            self.previous_counts[const.CATEGORY.ERRORED] += 1

        self.filter_bar.update_counts(self.previous_counts)

    def on_scan_complete(self):
        self.set_enabled(True)
        self.progress_bar.hide()
        self.central_image_list.update_image_lists(self.previous_scan)
        self.central_image_list.update_viewed_filter(self.filter_bar.get_selected_item())
        self.status_label.setText("Finished scanning %i images." % len(self.previous_scan[const.CATEGORY.ALL]))
        self.scanner_thread.exit()

    def on_scan_error(self, message):
        box = QMessageBox()
        box.setText(message)
        box.exec()

    #################################
    # deletion events
    #################################
    def on_deletion_started(self, count):
        self.set_enabled(False)
        self.progress_bar.setMaximum(count)
        self.progress_bar.setValue(0)
        self.progress_bar.show()

    def on_image_deleted(self, path):
        self.progress_bar.setValue(self.progress_bar.value() + 1)
        self.status_label.setText("Deleted %s!" % path)

    def on_deletion_finished(self, count):
        self.set_enabled(True)
        self.status_label.setText("Deleted %i images." % count)
        self.progress_bar.hide()
