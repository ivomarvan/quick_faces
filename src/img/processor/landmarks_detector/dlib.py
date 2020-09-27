#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Dlib lendmarks detector (redictor in some terminology) as img processor
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
from src.default_dirs import get_model_filename

class DlibLandmarksDetectorImgProcessor(ImgProcessorBase):

    def __init__(self, model_name:str):
        super().__init__(f'dlib_landmarks_predictor({model_name})')
        self._predictor = dlib.shape_predictor(get_model_filename(model_name))

    def _process_body(self, img: Image = None) -> Image:
        landmarks = []
        for face in img.get_params().get('faces'):
            # face_landmarks = face_utils.shape_to_np(self._predictor(img.get_array(), face))
            face_landmarks = self._predictor(img.get_array(), face)
            landmarks.append(face_landmarks)
        img.get_params().add('landmarks', landmarks)
        return img