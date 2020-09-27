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
import dlib



# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.image import Image
from src.img.processor.base import ImgProcessorBase
from src.default_dirs import get_model_cv2_dnn_cafee_filename
from src.img.processor.face_detector.decorator import FaceDetectorDecorator

class Cv2Dnn_CafeeFaceDetectorImgProcessor(ImgProcessorBase, FaceDetectorDecorator):

    def __init__(self, find_best: bool = True, color: tuple = (0, 255, 0)):
        super().__init__('face_detector(cv2_dnn_caffee_res10_300x300_ssd_iter_140000)')
        self._find_best = find_best
        model_filename, config_filename = get_model_cv2_dnn_cafee_filename()
        self._net = dnn.readNetFromCaffe(config_filename, model_filename)
        self._color = color
        self.add_not_none_option('color', color)
        self.add_not_none_option('find_best', find_best)

    def _process_body(self, img: Image = None) -> Image:
        img_array = img.get_array()
        h, w = img.get_heigth(), img.get_width()
        blob = dnn.blobFromImage(cv2.resize(img_array, (300, 300)), 1.0, (300, 300), (104.0, 117.0, 123.0))
        self._net.setInput(blob)
        faces_coffee = self._net.forward()
        faces_rectangles = dlib.rectangles()
        faces_dictionary = {}

        for i in range(faces_coffee.shape[2]):
            confidence = faces_coffee[0, 0, i, 2]
            if confidence > 0.5:
                box = faces_coffee[0, 0, i, 3:7] * np.array([w, h, w, h])
                if self._find_best:
                    faces_dictionary[confidence] = box.astype("int")
                else:
                    (x, y, x1, y1) = box.astype("int")
                    faces_rectangles.append(dlib.rectangle(x, y, x1, y1))

        if self._find_best and faces_dictionary:
            key = max(faces_dictionary.keys())
            (x, y, x1, y1) = faces_dictionary[key] # best item
            faces_rectangles.append(dlib.rectangle(x, y, x1, y1))

        self._add_faces(img, faces_rectangles)

        return img

