from PySide6.QtCore import QObject, QThread, Signal
import os, logging

import const
from models.ScannedImage import ScannedImage

logging.basicConfig(level=const.LOG_LEVEL)

SUPPORTED_TYPES = ['.jpg', '.jpeg', '.jpe', '.png', '.webp', '.tiff', '.tif']


def scan_file(path, file):
    ret = ScannedImage(path, file)
    ret.do_stuff()
    return ret


def ends_with_a_readable_type(file):
    for type in SUPPORTED_TYPES:
        if file.endswith(type):
            return True
    return False


class RecursiveDirectoryScanWorker(QObject):
    file_found = Signal(str, int, int)
    file_scanned = Signal(str, ScannedImage)
    scan_complete = Signal()
    scan_error = Signal(str)

    def __init__(self, directory):
        super().__init__()
        self.directory = directory
        pass

    def scan(self):
        try:
            logging.info("Beginning scan of %s..." % self.directory)
            for root, dirs, files in os.walk(self.directory):

                files = list(filter(lambda fil: ends_with_a_readable_type(fil), files))
                count = len(files)
                x = 0

                for file in files:
                    x += 1
                    logging.info("Scanning %s (%i if %i)" % (file, x, count))

                    self.file_found.emit(os.path.join(root, file), x, count)

                    info = scan_file(root, file)

                    self.file_scanned.emit(os.path.join(root, file), info)
        except:
            self.scan_error.emit("Unknown error during scan. Please see log for more information")
        finally:
            self.scan_complete.emit()
