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
import numpy as np

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.geometry import Point
from src.img.container.image import Image
from src.img.processor.processor import ImgProcessor
from src.default_dirs import ModelsSource
from src.img.processor.landmarks_detector.result import LandmarksDetectorResult, FaceLandmarsks
from src.img.processor.face_detector.result import FaceDetectorResult


def landmarks_to_points(dlib_landmarks, dtype="int") -> [Point]:
	# initialize the list of (x, y)-coordinates
	coords = np.zeros((dlib_landmarks.num_parts, 2), dtype=dtype)

	# loop over all facial landmarks and convert them
	# to a 2-tuple of (x, y)-coordinates
	for i in range(0, dlib_landmarks.num_parts):
		coords[i] = dlib_landmarks.part(i).x, dlib_landmarks.part(i).y


	# return the list of (x, y)-coordinates
	return [Point(c[0], c[1]) for c in coords]


class DlibLandmarksDetectorImgProcessor(ImgProcessor):

    def __init__(self, model_filename:str, color: tuple = (0, 0, 255)):
        super().__init__(f'dlib.shape_predictor({model_filename})')
        self._color = color
        self.add_not_none_option('color', color)
        self._predictor = dlib.shape_predictor(ModelsSource.get_model_dlib_shape_predictor_filename(model_filename))


    def _process_body(self, img: Image = None) -> (Image, LandmarksDetectorResult):

        # all faces, potentially from different face detectors
        faces_results = img.get_results().get_results_for_processor_super_class(FaceDetectorResult)
        face_landmark_couples = []
        for face_result in faces_results:
            faces = face_result.get_rectangles()  # [Rectangle]
            for face_index, face_rectangle in enumerate(faces):
                landmarks = landmarks_to_points(self._predictor(img.get_work_img_array(), face_rectangle.as_dlib_rectangle()))
                face_landmark_couples.append(FaceLandmarsks(face_result=face_result, landmarks=landmarks, face_index=face_index))
        return img, LandmarksDetectorResult(self, face_landmark_couples=face_landmark_couples)

