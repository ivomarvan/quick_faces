#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Container for image (as numpy.array) and some other information about it.
'''
import sys
import os
import numpy as np
import cv2
from typing import Any

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.results import ImageProcessorResults

class Image:

    SUPORTED_EXTENSIONS = [
        'bmp', 'dib', 'jpeg', 'jpg', 'jpe', 'jp2', 'png', 'webp',
        'pbm', 'pgm', 'ppm', 'pxm', 'pnm', 'pfm',
        'sr', 'ras', 'tiff', 'tif', 'exr'
    ]

    def __init__(
        self,
        array: np.ndarray,
        id: Any
    ):
        self._array = array
        self._id = id
        self._results = ImageProcessorResults()

    def get_array(self):
        return self._array

    def set_array(self, array:np.ndarray):
        self._array = array

    def get_id(self):
        return self._id

    def get_width(self) -> int:
        return self.get_shape()[1]

    def get_height(self) -> int:
        return self.get_shape()[0]

    def get_results(self) -> ImageProcessorResults:
        return self._results

    def get_shape(self):
        return self._array.shape

    def __str__(self) -> str:
        return f'img:{self._id}, shape:{self.get_shape()}, {self._results}'


    def _change_extension(self, path: str, forced_extension: str = None, default_extension = 'jpg' ) -> str:
        path_parts = path.split('.')
        path_extension = path_parts[-1]
        if forced_extension is None:
            # keep stored or use default
            if path_extension in self.SUPORTED_EXTENSIONS:
                # no change
                return path
            else:
                # use default
                path_parts.append(default_extension)
                return '.'.join(path_parts)
        else:
            # replace given

            return '.'.join(path_parts + [forced_extension])

    def store_to_file(self, path: str, extension: str = None, params=None) -> bool:
        path = os.path.join(path, str(self.get_id()))
        path = self._change_extension(path=path, forced_extension=extension)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        cv2.imwrite(filename=path, img=self._array, params=params)

    @classmethod
    def read_from_file(cls, path:str, color_flag: int = cv2.IMREAD_UNCHANGED, img_id: str = '') -> 'Image':
        img = Image(
            array= cv2.imread(path, color_flag),
            id=img_id
        )
        return img

    @classmethod
    def get_extension(cls, path: str):
        return path.split('.')[-1]

    @classmethod
    def acceptable_file(cls, dirname:str, basename:str) -> bool:
        '''
        Condition for "good" filename
        '''
        extension = basename.split('.')[-1]
        return extension in cls.SUPORTED_EXTENSIONS