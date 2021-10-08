#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Wrapper for MediaPipe FaceMesh solution.
'''
import sys
import os
import mediapipe as mp
import numpy as np

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

mp_selfie_segmentation = mp.solutions.selfie_segmentation

from src.img.processor.media_pipe.abstract import AbstractSolution


class SelfieSegmentationSolution(AbstractSolution):

    BG_COLOR = (192, 192, 192)  # gray

    def __init__(
        self,
        model_selection: int = 0  # 0 or 1
    ):
        super().__init__(
            solution=mp_selfie_segmentation.SelfieSegmentation(model_selection=model_selection)
        )
        self._bg_image = None

    def draw(self, img: np.ndarray) -> np.ndarray:
        # Draw selfie segmentation on the background image.
        # To improve segmentation around boundaries, consider applying a joint
        # bilateral filter to "results.segmentation_mask" with "image".
        condition = np.stack(
            (self._results.segmentation_mask,) * 3, axis=-1) > 0.1
        # The background can be customized.
        #   a) Load an image (with the same width and height of the input image) to
        #      be the background, e.g., self._bg_image = cv2.imread('/path/to/image/file')
        #   b) Blur the input image by applying image filtering, e.g.,
        #      self._bg_image = cv2.GaussianBlur(image,(55,55),0)
        if self._bg_image is None:
            self._bg_image = np.zeros(img.shape, dtype=np.uint8)
            self._bg_image[:] = self.BG_COLOR
        return np.where(condition, img, self._bg_image)
