#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Base img processor.
    Interface.
'''
import sys
import os
import time


# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.image import Image


class ImgProcessorBase:

    def __init__(self, name: str, options: dict = {}):
        self._name = name
        self._options = options

    def process(self, in_img: Image) -> Image:
        '''
        Runs _process_body and store item to image history
        '''
        ts = time.time()
        out_image = self._process_body(in_img)
        te = time.time()
        time_ms = int((te - ts) * 1000)
        if not out_image is None:
            out_image.history.add(processor_name=self._name, time_ms=time_ms)
        return out_image

    def _process_body(self, in_img: Image = None) -> Image:
        raise NotImplemented(f'Do not use instance of interface: "{self.__class__.__name__}"')