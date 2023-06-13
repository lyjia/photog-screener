import math
import os
import cv2
import numpy as np
import send2trash
from PySide6.QtGui import QStandardItem, QImage, QPixmap

from const import Const
from detectors.LaplacianBlurDetector import LaplacianBlurDetector
import logging

logging.basicConfig(level=Const.LOG_LEVEL)


def get_thumbnail_proportional_size(image_shape, long_edge_size):
    y, x, _ = image_shape

    if x > y:
        new_y = (float(long_edge_size) / x) * y
        return (long_edge_size, int(new_y))
    elif x == y:
        return (long_edge_size, long_edge_size)
    else:
        new_x = (float(long_edge_size) / y) * x
        return (int(new_x), long_edge_size)


class ScannedImage(QStandardItem):
    def __init__(self, path, file, laplacian_threshold=100, thumbnail_size_small=192, thumbnail_size_large=1024):
        super().__init__()
        self.image_path = os.path.join(path, file)
        self.label = file

        self.cv2_image = None
        self.laplacian_threshold = laplacian_threshold
        self.interpolation = cv2.INTER_AREA

        # analyzed attributes
        self.thumbnails = {}
        self.thumbnail_sizes = {'small': thumbnail_size_small} #, 'large': thumbnail_size_large}
        self.laplacian_variance = None

        self.setText(self.label)

        self.setEditable(False)
        self.setDragEnabled(False)
        self.setDropEnabled(False)
        self.setCheckable(True)

        # other attrs
        self.error = None

    def do_stuff(self):
        self.do_analysis()
        self.generate_thumbnails()
        self.generate_tooltip()

    def do_analysis(self):
        self.cv2_image = self.get_image()
        self.laplacian_variance = LaplacianBlurDetector(self.image_path,
                                                        self.cv2_image).get_laplacian_variance()

    def generate_tooltip(self):
        tooltip_path = "Path: %s" % self.image_path
        tooltip_blur = "Sharpness factor: %i of %i" % (self.laplacian_variance, self.laplacian_threshold)
        if self.is_blurry():
            tooltip_blur += " (BLURRY)"
        self.setToolTip('\n'.join([tooltip_path, tooltip_blur]))

    def generate_thumbnails(self):
        image_shape = self.cv2_image.shape

        for key in self.thumbnail_sizes:
            # proportional resize seems to get corrupted, this is visible on image thumbnails coming out skewed.
            # problem does not manifest if the destination size is 1:1 ratio
            # TODO: investigate this

            thumb_size = get_thumbnail_proportional_size(image_shape, self.thumbnail_sizes[key])
            thumb_cv2 = cv2.resize(self.cv2_image, thumb_size, interpolation=self.interpolation)
            thumb_arr = np.require(thumb_cv2, np.uint8, 'C')
            self.thumbnails[key] = QImage(thumb_arr.data, thumb_size[0], thumb_size[1], QImage.Format_BGR888)

        self.setIcon(QPixmap.fromImage(self.thumbnails['small']))

    def is_blurry(self):
        return (self.laplacian_variance < self.laplacian_threshold)

    def get_image(self):
        return cv2.imread(self.image_path)

    def delete(self):
        try:
            logging.info("About to delete %s" % self.image_path)
            send2trash.send2trash(self.image_path)
            return True
        except FileNotFoundError:
            logging.error("Could not delete %s: file not found!" % self.image_path)
            return False
        except:
            logging.error("Could not delete %s: unknown error!" % self.image_path)
            return False
