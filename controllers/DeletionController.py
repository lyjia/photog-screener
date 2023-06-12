from PySide6.QtCore import Signal

from models.ScannedImage import ScannedImage


class DeletionController:
    deletion_started = Signal(int)
    image_deleted = Signal(ScannedImage)
    deletion_complete = Signal()

    def __init__(self, images_to_delete):
        self.slated = images_to_delete
        pass

    def delete_all(self):
        total = len(self.slated)
        self.deletion_started.emit(total)

        for image in self.slated:
            result = image.delete
            if result:
                self.image_deleted.emit(image)

        self.deletion_complete.emit()