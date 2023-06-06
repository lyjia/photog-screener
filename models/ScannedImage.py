import os
import cv2
from PySide6.QtGui import QStandardItem
from detectors.LaplacianBlurDetector import LaplacianBlurDetector


class ScannedImage(QStandardItem):
    def __init__(self, path, file, laplacian_threshold=100, thumbnail_size_small=128, thumbnail_size_large=1024):
        super().__init__()
        self.image_path = os.path.join(path, file)
        self.label = file

        self.cv2_image = None
        self.laplacian_threshold = laplacian_threshold
        self.thumbnail_small_size = (thumbnail_size_small, thumbnail_size_small)
        self.thumbnail_large_size = (thumbnail_size_large, thumbnail_size_large)
        self.interpolation = cv2.INTER_AREA

        # analyzed attributes
        self.thumbnail_small = None
        self.thumbnail_large = None
        self.laplacian_variance = None

        # other attrs
        self.error = None

    def do_analysis(self):
        self.cv2_image = self.get_image()
        self.laplacian_variance = LaplacianBlurDetector(self.image_path,
                                                        self.cv2_image).get_laplacian_variance()
        self.thumbnail_small = cv2.resize(self.cv2_image, self.thumbnail_small_size, self.interpolation)
        self.thumbnail_large = cv2.resize(self.cv2_image, self.thumbnail_large_size, self.interpolation)

    def is_blurry(self):
        return self.laplacian_variance < self.laplacian_threshold

    def get_image(self):
        return cv2.imread(self.image_path)
