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
from imutils import face_utils


# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.image import Image
from src.img.processor.base import ImgProcessorBase
from src.img.processor.face_detector.decorator import FaceDetectorDecorator

class DlibFaceDetectorImgProcessor(ImgProcessorBase, FaceDetectorDecorator):

    def __init__(self, color: tuple = (0, 255, 0)):
        super().__init__('dlib_frontal_face_detector')
        self._color = color
        self.add_not_none_option('color', color)
        self._detector = dlib.get_frontal_face_detector()


    def _process_body(self, img: Image = None) -> Image:
        faces = self._detector(img.get_array(), 0)
        self._add_faces(img, faces)
        return img