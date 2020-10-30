#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Camera image source.
'''
import sys
import os
import cv2
import numpy as np

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.source.base import ImgSourceBase
from src.img.container.image import Image
from src.img.processor.types import IntType


class Camera(ImgSourceBase):
    """
    Camera input.
    An active switched-on camera whose number is in the given range is searched for.
    """
    def __init__(
            self,
            min_camera_number: IntType('Minimal number (ID) of camera') = 0,
            max_camera_number: IntType('Maximal number (ID) of camera') = 10,
    ):
        super().__init__(name='camera')
        self._capture = None
        self._is_adjusted = False
        self._range_of_camara_numbers = range(min_camera_number, max_camera_number)

    def __del__(self):
        if not self._capture is None:
            self._capture.release()

    def _get_img(self) -> (np.ndarray, int):
        ret, img = self._capture.read()
        # Int id of image. In the case of camera it can be "Current position of the video file in microseconds".
        img_microseconds = int(1000 * self._capture.get(cv2.CAP_PROP_POS_MSEC))
        return img, img_microseconds

    def _img_is_ok(self, img, deep_check: bool=False, treshold: int = 100):
        if img is None:
            return False
        if deep_check:
            # test for some 'sweet' colors
            if np.sum(img > 100) < treshold:
                return False
        return True

    def _adjust_and_return_img(self) -> (np.ndarray, int):
        for i in self._range_of_camara_numbers:
            try:
                self._capture = cv2.VideoCapture(i)
            except Exception as e:
                print(e)
            if self._capture.isOpened():
                img, img_microseconds = self._get_img()
                if self._img_is_ok(img, deep_check=True):
                    self._name += f'.{i}'
                    print('-' * 80)
                    print('Found camera:', i)
                    print('-' * 80)
                    return img, img_microseconds
        return None, None


    def get_next_image(self) -> Image:
        '''
        @see from src.img.source.base.ImgSourceBase#get_next_image
        '''
        if not self._is_adjusted:
            # first initialization
            img, img_microseconds = self._adjust_and_return_img()
        else:
            img, img_microseconds = self._get_img()

        self._is_adjusted = self._img_is_ok(img)

        if self._is_adjusted:
            return Image(array=img, id=img_microseconds)
        else:
            return None



