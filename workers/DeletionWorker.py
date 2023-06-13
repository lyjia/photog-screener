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
        total = len(self.slated)

        try:
            self.deletion_started.emit(total)

            for image in self.slated:
                result = image.delete
                if result:
                    self.image_deleted.emit(image)

        except Exception as e:
            self.deletion_error.emit("Error while deleting %s: %s" % self.image_path, getattr(e, 'message', repr(e)))
        finally:
            self.deletion_complete.emit()
