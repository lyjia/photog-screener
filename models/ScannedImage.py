import os
import cv2
import numpy as np
from PySide6.QtGui import QStandardItem, QImage, QPixmap
from detectors.LaplacianBlurDetector import LaplacianBlurDetector


class ScannedImage(QStandardItem):
    def __init__(self, path, file, laplacian_threshold=100, thumbnail_size_small=192, thumbnail_size_large=1024):
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

        self.setText(self.label)

        self.setEditable(False)
        self.setDragEnabled(False)
        self.setDropEnabled(False)
        self.setCheckable(True)

        # other attrs
        self.error = None

    def do_analysis(self):
        self.cv2_image = self.get_image()
        self.laplacian_variance = LaplacianBlurDetector(self.image_path,
                                                        self.cv2_image).get_laplacian_variance()

        thumbnail_small_cv2 = cv2.resize(self.cv2_image, self.thumbnail_small_size, self.interpolation)
        thumbnail_small_arr = np.require(thumbnail_small_cv2, np.uint8, 'C')
        thumbnail_small_shape = thumbnail_small_cv2.shape

        thumbnail_large_cv2 = cv2.resize(self.cv2_image, self.thumbnail_large_size, self.interpolation)
        thumbnail_large_arr = np.require(thumbnail_large_cv2, np.uint8, 'C')
        thumbnail_large_shape = thumbnail_large_cv2.shape

        self.thumbnail_small = QImage(thumbnail_small_arr.data, thumbnail_small_shape[0], thumbnail_small_shape[1],
                                      QImage.Format_BGR888)
        self.thumbnail_large = QImage(thumbnail_large_arr.data, thumbnail_large_shape[0], thumbnail_large_shape[1],
                                      QImage.Format_BGR888)

        self.setIcon( QPixmap.fromImage(self.thumbnail_small) )

        tooltip_path = "Path: %s" % self.image_path
        tooltip_blur = "Sharpness factor: %i of %i" % (self.laplacian_variance, self.laplacian_threshold)
        if self.is_blurry():
            tooltip_blur += " (BLURRY)"

        self.setToolTip( '\n'.join([tooltip_path, tooltip_blur]) )

    def is_blurry(self):
        return (self.laplacian_variance < self.laplacian_threshold)

    def get_image(self):
        return cv2.imread(self.image_path)