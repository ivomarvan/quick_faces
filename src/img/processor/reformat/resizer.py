#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Img processor for resizing
'''
import sys
import os
import time
import cv2
import imutils


# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.image import Image
from src.img.processor.processor import ImgProcessor
from src.img.container.result import ImageProcessorResult

class ImgResizeProcessor(ImgProcessor):

    def __init__(self, width=None, height=None, inter=cv2.INTER_AREA, resize_both: bool = True):
        super().__init__('resize')
        self.add_not_none_option('width', width)
        self.add_not_none_option('height', height)
        self.add_not_none_option('inter', inter)
        self.add_not_none_option('resize_both', resize_both)

    def _process_body(self, img: Image = None) -> Image:
        img.set_work_img_array(
            imutils.resize(
                image=img.get_work_img_array(),
                width=self.get_option('width'),
                height=self.get_option('width'),
                inter=self.get_option('inter'),
            )
        )

        if self.get_option('resize_both'):
            img.set_orig_img_array(
                imutils.resize(
                    image=img.get_orig_img_array(),
                    width=self.get_option('width'),
                    height=self.get_option('width'),
                    inter=self.get_option('inter'),
                )
            )
        return img, ImageProcessorResult(self)