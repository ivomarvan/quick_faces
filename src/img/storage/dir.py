#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Storage for image in directory
    Implements ImgProcessor, ImgStorageBase interfaces.
'''

import sys
import os

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.storage.base import ImgStorageBase
from src.img.container.image import Image

class ImgStorageDir(ImgStorageBase):

    def __init__(self, path: str):
        super().__init__('dir.' + path, {})
        self._path = path

    def store(self, img: Image, params = None, extension: str = None) -> bool:
        '''
        @see src.img.storage.base.ImgStorageBase.store

        extension == None means keep stored extension or use default
        '''
        img.store_to_file(path=self._path, params=params, extension=extension)
        return img

