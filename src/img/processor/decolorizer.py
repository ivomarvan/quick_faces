#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Img processor for decolorization (transformation to gray scale).
'''
import sys
import os
import time
import cv2
import imutils


# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.image import Image
from src.img.processor.processor import ImgProcessor
from src.img.container.result import ImageProcessorResult

class ImgDecolorizeProcessor(ImgProcessor):

    def __init__(self, code=cv2.COLOR_BGR2GRAY):
        super().__init__('decolorize')
        self.add_not_none_option('code', code)

    def _process_body(self, img: Image = None) -> Image:
        img.set_array(
            cv2.cvtColor(
                src=img.get_array(),
                code=self.get_option('code')
            )
        )
        return img, ImageProcessorResult(self)