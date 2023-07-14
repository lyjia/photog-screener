from PySide6.QtCore import QThread
from PySide6.QtWidgets import QMessageBox

import const
from models.ScannedImage import ScannedImage
from windows.MainWindow import MainWindow
from windows.components.FilterBar import FilterBar
from workers.DeletionWorker import DeletionWorker
from workers.RecursiveDirectoryScanWorker import RecursiveDirectoryScanWorker
import logging
from preferences import prefs

logging.basicConfig(level=const.LOG_LEVEL)


def create_default_scan_structs(path):
    previous_scan = {
        const.STR.PATH:         path,
        const.CATEGORY.ALL:     [],
        const.CATEGORY.BLURRY:  [],
        const.CATEGORY.ERRORED: []
    }

    previous_counts = {
        const.CATEGORY.ALL:     0,
        const.CATEGORY.BLURRY:  0,
        const.CATEGORY.ERRORED: 0
    }

    return previous_scan, previous_counts


class MainWindowController():
    def __init__(self, app):
        self.previous_counts = None
        self.previous_scan = None
        self.directory_scanner = None
        self.scanner_thread = None
        self.main_win = None
        self.qapp = app

    def start_er_up(self):
        self.main_win = MainWindow(style=self.qapp.style())
        self.main_win.user_requested_dir_scan.connect(self.on_user_request_dir_scan)
        self.main_win.set_up_for_new_run.connect(self.set_up_for_new_run)
        self.main_win.show()

    #################################
    # on user events
    #################################
    def on_user_request_dir_scan(self, target_path):
        logging.info("Received request to start dir scan at %s" % target_path)
        self.start_directory_scan(target_path)

    #################################
    # directory scanner + events
    #################################
    def start_directory_scan(self, target_path, options={}):
        self.main_win.set_enabled(False)
        self.main_win.set_progress_bar_visibility(True)

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

    def set_up_for_new_run(self, path=None):
        # self.main_win.set_up_for_new_run(path)
        self.previous_scan, self.previous_counts = create_default_scan_structs(path)

        self.main_win.update_filter_bar_counts(self.previous_counts)
        self.main_win.update_image_lists(self.previous_scan)
        self.main_win.update_filter_bar_path(path)


    def on_scan_file_found(self, file_path, x, count):
        self.main_win.update_status_label("Scanning %s..." % file_path)
        self.main_win.update_progress_bar(x, count)


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

        self.main_win.update_filter_bar_counts(self.previous_counts)


    def on_scan_complete(self):
        self.main_win.set_enabled(True)
        self.main_win.set_progress_bar_visibility(False)

        self.main_win.update_image_lists(self.previous_scan)
        self.main_win.update_status_label("Finished scanning %i images." % len(self.previous_scan[const.CATEGORY.ALL]))
        self.scanner_thread.exit()


    def on_scan_error(self, message):
        self.main_win.popup_error_box(message)

    #####################################
    # image deletion
    #####################################
    def delete_all_images(self, to_delete, deletion_type):
        self.deletion_thread = QThread()
        self.deletion_thread.setObjectName("Delete images")
        self.deletion_wrkr = DeletionWorker(to_delete, deletion_type)

        self.deletion_wrkr.moveToThread(self.deletion_thread)

        self.deletion_thread.started.connect(self.deletion_wrkr.delete_all)

        self.deletion_wrkr.deletion_started.connect(self.on_deletion_started)
        self.deletion_wrkr.deletion_error.connect(self.on_deletion_error)
        self.deletion_wrkr.deletion_complete.connect(self.on_deletion_completed)
        self.deletion_wrkr.image_deleted.connect(self.on_image_deleted)

        self.deletion_thread.start()

    def on_deletion_started(self, count):
        self.deletion_started.emit(count)

    def on_deletion_error(self, str):
        logging.error(str)

    def on_image_deleted(self, image: ScannedImage):
        self.image_deleted.emit(image.image_path)
        self.image_list.remove_image(image)

    def on_deletion_completed(self):
        self.deletion_thread.exit()
        self.deletion_complete.emit(0)
