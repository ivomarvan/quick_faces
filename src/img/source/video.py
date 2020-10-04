#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Images from video.
'''
import sys
import os


# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.source.base import ImgSourceBase
from src.img.container.image import Image

class ImgSourceDir(ImgSourceBase):

    def __init__(self, path: str):
        super().__init__('video.' + path)
        self._path = path



    def get_next_image(self) -> Image:
        '''
        @see from src.img.source.base.ImgSourceBase#get_next_image
        '''
        raise NotImplemented('Sorry, not implemented yet.')




