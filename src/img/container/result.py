#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Container for one result of  one img.processor.
'''

import sys
import os

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

# from src.img.processor.processor import ImgProcessor

class ImageProcessorResult:
    '''
    Result of image processor.
    '''

    def __init__(
        self,
        processor: 'ImgProcessor',
        time_ms: int = None
    ):
        self._processor = processor  # reference to processor object
        self._time_ms = time_ms  # the time required to obtain the result [ms]

    def get_processor(self) -> 'ImgProcessor':
        return self._processor

    def get_time_ms(self):
        return self._time_ms

    def set_time_ms(self, time_ms:int):
        self._time_ms = time_ms

    def __str__(self):
        s = f'\n\t\tprocessor:{self.get_processor().get_name()} => {self.get_time_ms()} [ms]'
        s += f'\n\t\toptions: {self.get_processor().get_options()}'
        return s