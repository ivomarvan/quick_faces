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

class DlibFaceDetectorImgProcessor(ImgProcessorBase):

    def __init__(self):
        super().__init__('dlib_face_detector')
        self._detector = dlib.get_frontal_face_detector()


    def _process_body(self, img: Image = None) -> Image:
        faces = self._detector(img.get_array(), 0)
        img.get_params().add('faces', faces)
        return img