import os
from PySide6.QtGui import QStandardItem
from detectors.LaplacianBlurDetector import LaplacianBlurDetector

class ScannedFile(QStandardItem):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.label = os.path.basename(image_path)

        # analyzed attributes
        self.image_thumbnail = None
        self.laplacian_variance = None

    def DoAnalysis(self):
        self.laplacian_variance = LaplacianBlurDetector(self.image_path)


