#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    List of img processors.
    It is a img processor also.
'''
import sys
import os
import time

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.processor.base import ImgProcessorBase
from src.img.container.image import Image
from src.img.container.history import ImageHistory

class ImgListProcessor(ImgProcessorBase):
    '''
    List of processors. Process sequentaly image with all subrocessors int the list.
    '''
    def __init__(self, name: str, processors: [ImgProcessorBase], options: dict = {}, level: int = 0):
        super().__init__('list.' + name, options)
        self._processors = processors
        self._level = level

    def _process_body(self, img:Image = None) -> Image:
        '''
        @see src.img.processor.base.ImgProcessorBase._process_body
        '''
        img = img
        for processor in self._processors:
            img = processor.process(img)
        return img

    def process(self, img: Image) -> Image:
        '''
        Runs _process_body and store item to image history
        '''
        old_history_before_list = img.history
        img.history = ImageHistory(self._level + 1)  # new for list
        out_image = self._process_body(img)
        if not out_image is None:
            subprocesses_history = out_image.history
            out_image.history = old_history_before_list
            out_image.history.add_history(processor_name=self._name, subprocesses_history=subprocesses_history)
        return out_image