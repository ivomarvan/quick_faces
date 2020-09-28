#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Dlib face detector as img processor
'''
import sys
import os
import dlib


# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.image import Image

# @todo Refactor to predseccor of all face_detectors
class FaceDetectorDecorator:

    def _add_faces(self, img: Image, rectangles: dlib.rectangles):
        results = img.get_results()
        results.add(self._name, 'faces', rectangles)
        results.add(self._name, 'color', self._color)



