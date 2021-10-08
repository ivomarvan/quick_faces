#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Wrapper for all MediaPipe solutions.
'''

import mediapipe as mp
import sys
import os
import numpy as np

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.processor.processor import ImgProcessor
from src.img.container.result import ImageProcessorResult
from src.img.processor.media_pipe.abstract import AbstractSolution
from src.img.container.image import Image


class MediaPipeResult(ImageProcessorResult):

    def __init__(
            self,
            processor: ImgProcessor,
            time_ms: int = None,
            data = None
    ):
        super().__init__(processor=processor, time_ms=time_ms)
        self._data = data

    def get_data(self):
        return self._data


class MediaPipeProcessor(ImgProcessor):

    def __init__(
        self,
        solution: AbstractSolution
    ):
        super().__init__(name=solution.__class__.__name__)
        self._solution = solution

    def _process_image(self, img: Image = None) -> (Image, ImageProcessorResult):
        img_array = img.get_work_img_array()
        results_data = self._solution.process(img_array)
        return img, MediaPipeResult(self, data=results_data)


class MediaPipeMarker(MediaPipeProcessor):

    def _process_image(self, img: Image = None) -> (Image, ImageProcessorResult):
        img_array = img.get_orig_img_array()
        self._solution.draw(img_array)
        return img, ImageProcessorResult(self)
