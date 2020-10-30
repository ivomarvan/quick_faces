#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Interface for image processor.

'''
import sys
import os
import time
from typing import Any

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.processor.params.params import Param
from src.img.container.image import Image
from src.img.container.result import ImageProcessorResult


class ImgProcessorInterface:

    @classmethod
    def get_parameters(cls) -> [Param]:
        '''
        Return all required parameter.
        The parameters will be fulfilled by values (potentially by GUI) and used to setup img. processor.
        '''
        raise NotImplemented(f'Do not use instance of interface: "{cls.__class__.__name__}"')

    def _process_image(self, img: Image = None) -> (Image, ImageProcessorResult):
        '''
        Proces image. Image is container which contain image as np.array and other
        parameters as history o processing and so.
        Returns processed image and some result (like face boxess, landmarks and so.).
        Result is a successor of ImageProcessorResult.
        '''
        raise NotImplemented(f'Do not use instance of interface: "{self.__class__.__name__}"')


    def get_markup_description(self) -> str:
        '''
        Returns descripton of rocessor in markup language (plain text with som formatting possibilities).
        '''
        raise NotImplemented(f'Do not use instance of interface: "{self.__class__.__name__}"')
