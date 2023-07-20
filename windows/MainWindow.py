import logging
from pathlib import Path

from PySide6.QtCore import QCoreApplication, Signal
from PySide6.QtGui import Qt, QPixmap, QIcon
from PySide6.QtWidgets import QMainWindow, QDockWidget, QFileDialog, QProgressBar, QLabel, QMessageBox, \
    QStyleFactory

import const
from models.ScannedImage import ScannedImage
from preferences import prefs
from windows.components.CenterPane import CenterPane
from windows.components.FilterBar import FilterBar

logging.basicConfig(level=const.LOG_LEVEL)


class MainWindow(QMainWindow):
    user_requested_dir_scan = Signal(str)
    user_requested_deletion = Signal(object, str)  # object is a list of ScannedImage
    set_up_for_new_run = Signal()

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
        self.status_label = None
        self.progress_bar = None

        self.filter_bar = None
        self.central_image_list = None
        self.center_pane = None

        self.create_menus()
        self.create_dock_widgets()
        self.create_statusbar()
        self.create_center_pane()

        self.set_up_for_new_run.emit()

    ########################
    # setup
    ########################

    def create_menus(self):
        ### File menu
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction("&Scan Folder...").triggered.connect(self.on_file_scan_folder_action)
        file_menu.addAction("&Quit").triggered.connect(self.on_file_quit_action)

        ### View Menu
        view_menu = self.menuBar().addMenu("&View")
        view_menu.addAction("&Image Preview/Info")

        ### Options Menu
        options_menu = self.menuBar().addMenu("&Options")

        # On Removal submenu
        on_delete_menu = options_menu.addMenu("When &removing")
        for item in const.MENU.ON_REMOVAL.keys():
            # QAction doesn't give us a way to access the parent menu (which we need to uncheck all the other menu items)
            # so we stuff it into an attribute on the instantiated class
            act = on_delete_menu.addAction(item)
            act.setCheckable(True)
            act.__setattr__('parent_menu', on_delete_menu)
            act.triggered.connect(self.on_options_removal_select)
            if prefs().get_pref(const.PREFS.GLOBAL.NAME,
                                const.PREFS.GLOBAL.ON_REMOVAL_ACTION,
                                const.PREFS.GLOBAL.ON_REMOVAL_ACTION_VALUES.default) == \
                  const.MENU.ON_REMOVAL.corresponding_prefs[item]:
                act.setChecked(True)

        options_menu.addSeparator()

        # Theme submenu
        styles_menu = options_menu.addMenu("&Theme")
        for style in QStyleFactory.keys():
            act = styles_menu.addAction(style)
            act.setCheckable(True)
            if style.lower() == self.current_style.name().lower():
                act.setChecked(True)
            act.triggered.connect(self.on_options_theme_select)

        # Help menu
        help_menu = self.menuBar().addMenu("&Help")
        help_menu.addAction("&About...")

        # Debug menu
        debug_menu = self.menuBar().addMenu("&Debug")
        act = debug_menu.addAction("Show an error popup")
        act.triggered.connect(self.on_debug_show_error_popup)

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

    def create_center_pane(self):
        self.center_pane = CenterPane()
        self.central_image_list = self.center_pane.get_image_list_widget()
        self.setCentralWidget(self.center_pane)

        # set up event handlers for image deletion
        self.center_pane.user_requested_deletion.connect(self.on_user_requested_deletion)

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
        starting_dir = prefs().get_pref(const.PREFS.GLOBAL.NAME, const.PREFS.GLOBAL.LAST_SCAN_DIR,
                                        const.DEFAULTS.LAST_SCAN_DIR)
        dialog.setDirectory(starting_dir)

        if dialog.exec_():
            folderName = dialog.selectedFiles()[0]
            prefs().set_pref(const.PREFS.GLOBAL.NAME, const.PREFS.GLOBAL.LAST_SCAN_DIR, folderName)

            self.user_requested_dir_scan.emit(folderName)
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
        if target == const.MENU.ON_REMOVAL.DELETE:
            persist = const.PREFS.GLOBAL.ON_REMOVAL_ACTION_VALUES.DELETE
        else:
            persist = const.PREFS.GLOBAL.ON_REMOVAL_ACTION_VALUES.TO_TRASH

        prefs().set_pref(const.PREFS.GLOBAL.NAME, const.PREFS.GLOBAL.ON_REMOVAL_ACTION, persist)
        for action in me.parent_menu.children():
            if me is not action:
                action.setChecked(False)

    def on_debug_show_error_popup(self):
        self.popup_error_box("OMG!! YOUR HAIR IS ON FIRE!!!!!")

    ##########################
    # control actions
    ##########################
    def on_filter_bar_selection_changed(self, label):
        logging.info("User changed filter to %s" % label)
        self.central_image_list.update_viewed_filter(label)

    def on_user_requested_deletion(self, slated_for_execution, deletion_type):
        # pass the event on to the controller
        self.user_requested_deletion.emit(slated_for_execution, deletion_type)

    ##########################
    # controller interface
    ##########################
    def update_progress_bar(self, current, total):
        self.progress_bar.setValue(current)
        self.progress_bar.setMaximum(total)

    def update_status_label(self, text):
        self.status_label.setText(text)

    def set_progress_bar_visibility(self, value):
        if value is True:
            self.progress_bar.show()
        else:
            self.progress_bar.hide()

    def clear_status_label(self):
        self.status_label.setText("")

    def update_filter_bar_counts(self, previous_counts):
        self.filter_bar.update_counts(previous_counts)

    def update_filter_bar_path(self, path):
        self.filter_bar.update_scanned_folder_label(path)

    def update_image_lists(self, previous_scan):
        self.central_image_list.update_image_lists(previous_scan)
        self.central_image_list.update_viewed_filter(self.filter_bar.get_selected_item())

    def popup_error_box(self, text, title=const.APP.NAME, icon=QMessageBox.Warning):
        box = QMessageBox(self)

        box.setWindowTitle(title)
        box.setText(text)
        box.setIcon(icon)
        box.exec()

    #################################
    # deletion events
    #################################
    def on_deletion_started(self, count):
        self.set_enabled(False)
        self.progress_bar.setMaximum(count)
        self.progress_bar.setValue(0)
        self.progress_bar.show()

    def on_image_deleted(self, image: ScannedImage):
        self.center_pane.remove_image_from_image_list(image)
        path = image.image_path
        self.progress_bar.setValue(self.progress_bar.value() + 1)
        self.status_label.setText("Deleted %s!" % path)

    def on_deletion_finished(self, count):
        self.center_pane.refresh_image_list()
        self.set_enabled(True)
        self.status_label.setText("Deleted %i images." % count)
        self.progress_bar.hide()
