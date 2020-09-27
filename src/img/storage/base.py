#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Base img storage.
    (Like video file, directory of images, ...)
    Interface.
'''

import sys
import os

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..'))
sys.path.append(PROJECT_ROOT)


from src.img.processor.base import ImgProcessorBase
from src.img.container.image import Image

class ImgStorageBase(ImgProcessorBase):

    def __init__(self, name: str, options: dict = {}):
        super().__init__('storage.' + name, options)

    def store(self, img: Image) -> Image:
        '''
        Store image.
        Returns success.
        '''
        raise NotImplemented(f'Do not use instance of interface: "{self.__class__.__name__}"')

    def _process_body(self, img:Image = None) -> Image:
        return self.store(img)
