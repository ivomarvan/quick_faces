#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Normalized result for face detectors   
'''

import sys
import os

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.result import ImageProcessorResult
from src.img.container.geometry import Rectangle
from src.img.processor.processor import ImgProcessor

class FaceDetectorResult(ImageProcessorResult):

    def __init__(self, processor: ImgProcessor, time_ms: int = None, rectangles:[Rectangle] = []):
        super().__init__(processor=processor, time_ms=time_ms)
        self._rectangles = rectangles

    def get_rectangles(self) -> [Rectangle]:
        return self._rectangles

    def get_rectangle(self, index:int) -> Rectangle:
        try:
            return self._rectangles[index]
        except IndexError:
            return None

    def __str__(self):
        s = super(FaceDetectorResult, self).__str__()
        s += f'\n\t\tfaces: {[str(r) for r in self.get_rectangles()]}'
        return s

