#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Predcessor for all image processors.
    The processors must satisfy the ImgProcessorInterface. 
'''
import sys
import os
import time
from typing import Any

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.image import Image
from src.utils.timeit_stats import TimeStatistics
from src.img.processor.interface import ImgProcessorInterface
from src.img.container.result import ImageProcessorResult
from src.img.processor.types import DictStorable

class ImgProcessor(DictStorable):

    def __init__(self, name: str):
        super(ImgProcessor, self).__init__()
        self._name = name
        self._options = {}
        
    def _process_image(self, img: Image = None) -> (Image, ImageProcessorResult):
        '''
        Proces image. Image is container which contain image as np.array and other
        parameters as history o processing and so.
        Returns processed image and some result (like face boxess, landmarks and so.).
        Result is a successor of ImageProcessorResult.
        '''
        raise NotImplementedError(f'Do not use instance of interface: "{self.__class__.__name__}"')

    def get_name(self):
        return self._name

    def add_not_none_option(self, key: str, value):
        if value is not None:
            self._options[key] = value

    def get_option(self,  key: str) -> Any:
        try:
            return self._options[key]
        except KeyError:
            return None

    def get_options(self) -> dict:
        return self._options

    def process(self, img: Image) -> Image:
        '''
        Runs _process_image and store item to image history
        '''
        ts = time.time()
        out_image, processor_result = self._process_image(img)
        te = time.time()
        time_ms = int((te - ts) * 1000)

        TimeStatistics.logTimeDiff(name=self._name, timeDiff=time_ms, result=out_image)

        if not out_image is None:
            processor_result.set_time_ms(time_ms)
            out_image.get_results().add(processor_result)

        return out_image


