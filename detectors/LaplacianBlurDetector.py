import cv2
import os
import numpy as np


class LaplacianBlurDetector():

    def __init__(self, image_path, cv2_image):
        self.image_path = image_path
        self.image = cv2_image
        self.gray = None
        self.variance = None
        self.analyze()

    def analyze(self):
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.variance = cv2.Laplacian(self.gray, cv2.CV_64F).var()

    def get_laplacian_variance(self):
        return self.variance

