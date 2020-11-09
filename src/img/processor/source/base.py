#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Base img source.
    (Like webcamera file, video, directory of images, ...)
    Interface.
'''
import sys
import os

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '../..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.image import Image
from src.img.processor.processor import ImgProcessor
from src.img.container.result import ImageProcessorResult

class ImgSourceBase(ImgProcessor):

    def __init__(self, name: str):
        super().__init__('source.' + name)

    def init_hardware(self, *args, **kwargs):
        '''
        Any action for hardware reset
        '''
        pass

    def get_next_image(self) -> Image:
        '''

        Returns Image container.
        '''
        raise NotImplementedError(f'Do not use instance of interface: "{self.__class__.__name__}"')

    def _process_image(self, img:Image = None) -> Image:
        return self.get_next_image(), ImageProcessorResult(self)