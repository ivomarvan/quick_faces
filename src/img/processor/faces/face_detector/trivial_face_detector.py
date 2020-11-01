#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Dlib face detector as img processor
'''
import sys
import os

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '../..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.image import Image
from src.img.processor.faces.face_detector.face_detector import FaceDetector
from src.img.processor.faces.face_detector.result import FaceDetectorResult
from src.img.container.geometry import Point, Rectangle


class TrivialFaceDetector(FaceDetector):
    '''
    Whole image is detected as a face.
    '''

    def __init__(self, name: str='trivial_face_detector', find_best: bool = True, color: tuple = (100, 255, 40)):
        super().__init__(name=name, find_best=find_best, color=color)

    def _process_image(self, img: Image = None) -> (Image, FaceDetectorResult):
        work_img_shape = img.get_work_img_array().shape
        rectangles = [Rectangle(left_top=Point(x=1, y=1), right_bottom=Point(x=work_img_shape[1] - 1, y=work_img_shape[0] - 1 ))]
        return img, FaceDetectorResult(self, rectangles=rectangles)