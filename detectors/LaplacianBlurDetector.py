import cv2
import os
import numpy as np


class LaplacianBlurDetector():

    def __init__(self, image_path, threshold):
        self.threshold = threshold
        self.image_path = image_path
        self.image = None
        self.gray = None
        self.variance = None
        self.analyze()

    def analyze(self):
        self.image = self.get_image()
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.variance = self.get_laplacian_variance()

    def get_image(self):
        return cv2.imread(self.image_path)

    def get_laplacian_variance(self):
        self.variance = cv2.Laplacian(self.gray, cv2.CV_64F).var()
        return self.variance

    def is_blurry(self):
        return self.variance < self.threshold
