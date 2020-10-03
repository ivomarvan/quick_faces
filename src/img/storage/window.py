#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Show image in cv2 window
    Implements ImgProcessor, ImgStorageBase interfaces.
'''

import sys
import os
import cv2

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.storage.base import ImgStorageBase
from src.img.container.image import Image

class ImgStorageWindow(ImgStorageBase):

    def __init__(self, name: str = ''):
        super().__init__('window.' + name)

    def __del__(self):
        try:
            cv2.destroyAllWindows()
        except Exception:
            pass

    def store(self, img: Image) -> Image:
        '''
        @see src.img.storage.base.ImgStorageBase.store
        Show img in window
        '''
        # show the frame
        cv2.imshow(self._name, img.get_array())
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            raise StopIteration()
            stop = True
        return img
