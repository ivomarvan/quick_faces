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
from src.img.processor.face_detector.face_detector import FaceDetector
from src.img.processor.face_detector.result import FaceDetectorResult
from src.img.container.geometry import Rectangle


class DlibFaceDetectorImgProcessor(FaceDetector):

    def __init__(self, name: str='dlib_frontal_face_detector', find_best: bool = True, color: tuple = (0, 255, 0)):
        super().__init__(name=name, find_best=find_best, color=color)
        self._detector = dlib.get_frontal_face_detector()

    def _process_body(self, img: Image = None) -> (Image, FaceDetectorResult):
        faces = self._detector(img.get_array(), 0)
        rectangles = [Rectangle.crate_from_dlib_rectangle(dlib_rect) for dlib_rect in faces]
        return img, FaceDetectorResult(self, rectangles=rectangles)