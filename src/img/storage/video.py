#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Storage for images to video file.
    (Implements ImgProcessor, ImgStorageBase interfaces.)
'''

import sys
import os
import cv2
import numpy as np

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.storage.base import ImgStorageBase
from src.img.container.image import Image

class ImgStorageVideo(ImgStorageBase):

    def __init__(self, path: str, codec='mp4v', fps: int = 30):
        super().__init__('dir.' + path)
        self.add_not_none_option('out', path)
        self.add_not_none_option('fps', fps)
        self._path = path
        self._codec = codec
        self._fps = fps
        self._images = []  # [Image]
        self._path = path


    def __del__(self):
        '''
        Store all temoraly tored images images
        '''
        fourcc = cv2.VideoWriter_fourcc(*self._codec)
        # find width and height for output
        widths = []
        heights = []
        for img in self._images:
            widths.append(img.get_width())
            heights.append(img.get_height())
        max_width = max(widths)
        max_height = max(heights)
        os.makedirs(os.path.dirname(self._path), exist_ok=True)
        out = cv2.VideoWriter(self._path, fourcc, self._fps, (max_width, max_height))
        for img in self._images:
            w, h = img.get_width(), img.get_height()
            if w != max_width or h != max_height:
                # put small image to big one (with maximal size in dataset)
                big_image = np.zeros((max_height, max_width, 3), np.uint8)
                big_image[0:h, 0:w,:] = img.get_orig_img_array()
                out.write(big_image)
            else:
                out.write(img.get_orig_img_array())

        out.release()

    def store(self, img: Image) -> Image:
        '''
        @see src.img.storage.base.ImgStorageBase.store
        '''
        self._images.append(img)
        return img

