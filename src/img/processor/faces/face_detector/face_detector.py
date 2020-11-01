#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Base class for all face detectors
'''
import sys
import os

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '../..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.processor.processor import ImgProcessor


class FaceDetector(ImgProcessor):

    def __init__(self, name: str, find_best: bool = True, color: tuple = (0, 255, 0)):
        super().__init__(name=name)
        self.add_not_none_option('color', color)
        self.add_not_none_option('find_best', find_best)
        self._color = color
        self._find_best = find_best

