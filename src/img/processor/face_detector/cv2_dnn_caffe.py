#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Dlib face detector as img processor
'''
import sys
import os
import numpy as np
import cv2, cv2.dnn as dnn

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.image import Image
from src.default_dirs import get_model_cv2_dnn_cafee_filename
from src.img.processor.face_detector.face_detector import FaceDetector
from src.img.processor.face_detector.result import FaceDetectorResult
from src.img.container.geometry import Point, Rectangle

class Cv2DnnCafeeFaceDetector(FaceDetector):

    def __init__(self, name: str='dnn.readNetFromCaffe', find_best: bool = True, color: tuple = (0, 255, 0)):
        super().__init__(name=name, find_best=find_best, color=color)
        model_filename, config_filename = get_model_cv2_dnn_cafee_filename()
        self._net = dnn.readNetFromCaffe(config_filename, model_filename)
        self.add_not_none_option('config', config_filename)
        self.add_not_none_option('model', model_filename)

    def _process_body(self, img: Image = None) -> (Image, FaceDetectorResult):
        img_array = img.get_array()
        h, w = img.get_heigth(), img.get_width()
        blob = dnn.blobFromImage(cv2.resize(img_array, (300, 300)), 1.0, (300, 300), (104.0, 117.0, 123.0))
        self._net.setInput(blob)
        faces_coffee = self._net.forward()
        faces_rectangles = []
        faces_dictionary = {}

        for i in range(faces_coffee.shape[2]):
            confidence = faces_coffee[0, 0, i, 2]
            if confidence > 0.5:
                box = faces_coffee[0, 0, i, 3:7] * np.array([w, h, w, h])
                if self._find_best:
                    faces_dictionary[confidence] = box.astype("int")
                else:
                    (x, y, x1, y1) = box.astype("int")
                    faces_rectangles.append(Rectangle(Point(x, y), Point(x1, y1)))

        if self._find_best and faces_dictionary:
            key = max(faces_dictionary.keys())
            (x, y, x1, y1) = faces_dictionary[key] # best item
            faces_rectangles.append(Rectangle(Point(x, y), Point(x1, y1)))

        return img, FaceDetectorResult(self, rectangles=faces_rectangles)

