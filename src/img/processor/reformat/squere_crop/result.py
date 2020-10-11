#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Normalized result for landmarks detector (prediktor)
'''

import sys
import os

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.result import ImageProcessorResult
from src.img.processor.processor import ImgProcessor

class SquereCropResult(ImageProcessorResult):

    def __init__(self, processor: ImgProcessor, time_ms: int = None, img_scale: float = 1.0):
        super().__init__(processor=processor, time_ms=time_ms)
        self._img_scale = img_scale

    def get_img_scale(self) -> float:
        return self._img_scale

    def __str__(self):
        s = super().__str__()
        s += f'(scale:{self.get_img_scale()})'
        return s