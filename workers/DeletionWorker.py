from PySide6.QtCore import Signal, QObject

from models.ScannedImage import ScannedImage


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
        try:
            total = len(self.slated)
            self.deletion_started.emit(total)

            for image in self.slated:
                result = image.delete
                if result:
                    self.image_deleted.emit(image)

        except:
            self.deletion_error.emit("Unknown error deleting %s" % self.image_path)
        finally:
            self.deletion_complete.emit()
