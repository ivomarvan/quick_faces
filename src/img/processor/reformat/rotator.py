#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Img processor for resizing
'''
import sys
import os
import numpy as np
import cv2

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.image import Image
from src.img.processor.processor import ImgProcessor
from src.img.container.result import ImageProcessorResult
import imutils

class ImgRotateProcessor(ImgProcessor):

    def __init__(self, rotate_both: bool = True, angle: int = 90):

        super().__init__('rotation')
        self.add_not_none_option('rotate_both', rotate_both)
        self._rotate_both = rotate_both
        self._angle = angle

    def _rotate(self, img_array: np.ndarray)-> np.ndarray:
        '''
        # @todo Remove hack, do not accept all degrees
        # flip image vertically
        img_array = cv2.flip(img_array, 0)

        # transpose image
        img_array = cv2.transpose(img_array)
        '''


        return imutils.rotate_bound(img_array, self._angle)

    def _process_image(self, img: Image = None) -> Image:

        img.set_work_img_array(self._rotate(img_array=img.get_work_img_array()))
        if self._rotate_both:
            img.set_orig_img_array(self._rotate(img_array=img.get_orig_img_array()))

        return img, ImageProcessorResult(self)