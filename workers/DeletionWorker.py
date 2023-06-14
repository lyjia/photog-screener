from PySide6.QtCore import Signal, QObject

import const
from models.ScannedImage import ScannedImage
import logging
logging.basicConfig(level=const.LOG_LEVEL)



class DeletionWorker(QObject):
    deletion_started = Signal(int)
    deletion_error = Signal(str)
    image_deleted = Signal(ScannedImage)
    deletion_complete = Signal()

    def __init__(self, images_to_delete):
        super().__init__()
        self.slated = images_to_delete
        pass

    def delete_all(self):
        total = len(self.slated)

        logging.info("Slated to delete %i iamges, starting..." % total)

        try:
            self.deletion_started.emit(total)

            for image in self.slated:
                logging.info("About to delete %s" % image.image_path)
                result = image.trash_image
                if result:
                    self.image_deleted.emit(image)

        except Exception as e:
            self.deletion_error.emit("Error while deleting %s: %s" % self.image_path, getattr(e, 'message', repr(e)))
        finally:
            self.deletion_complete.emit()
