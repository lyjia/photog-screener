from PySide6.QtCore import QObject, QThread, Signal
import os, logging

from models.ScannedImage import ScannedImage

logging.basicConfig(level=logging.INFO)
def scan_file(path, file):
    ret = ScannedImage(path, file)
    ret.do_analysis()
    return ret


class RecursiveDirectoryScanner(QObject):
    file_found = Signal(str, int, int)
    file_scanned = Signal(str, ScannedImage)
    scan_complete = Signal()

    def __init__(self, directory):
        super().__init__()
        self.directory = directory
        pass

    def scan(self):
        logging.info("Beginning scan of %s..." % self.directory)
        for root, dirs, files in os.walk(self.directory):

            files = filter(lambda file: file.endswith('.jpg'), files)
            count = files.count()
            x = 0

            for file in files:
                x += 1
                logging.info("Scanning %s (%i if %i)" % (file, x, count))
                self.file_found.emit(os.path.join(root, file), x, count)
                info = scan_file(root, file)
                self.file_scanned.emit(os.path.join(root, file), info)

        self.scan_complete.emit()
