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

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.image import Image
from src.img.processor.processor import ImgProcessor
from src.default_dirs import get_model_dlib_shape_predictor_filename
from src.img.processor.landmarks_detector.result import LandmarksDetectorResult, FaceLandmarsks
from src.img.processor.face_detector.result import FaceDetectorResult

class DlibLandmarksDetectorImgProcessor(ImgProcessor):

    def __init__(self, model_name:str, color: tuple = (0, 0, 255)):
        super().__init__(f'dlib_shape_predictor({model_name})')
        self._color = color
        self.add_not_none_option('color', color)
        self._predictor = dlib.shape_predictor(get_model_dlib_shape_predictor_filename(model_name))


    def _process_body(self, img: Image = None) -> (Image, LandmarksDetectorResult):

        # all faces, potentially from different face detectors
        faces_results = img.get_results().get_results_for_processor_super_class(FaceDetectorResult)
        face_landmark_couples = []
        for face_result in faces_results:
            faces = face_result.get_rectangles()  # [Rectangle]
            for face_rectangle in faces:
                landmarks = self._predictor(img.get_array(), face_rectangle.as_dlib_rectangle())
                face_landmark_couples.append(FaceLandmarsks(face_result=face_result, landmarks=landmarks))
        return img, LandmarksDetectorResult(self, face_landmark_couples=face_landmark_couples)

        '''
        img_results = img.get_results()
        # for all faces from all face_processors
        faces_results = img_results.get_results_with_given_result_name('faces')
        if faces_results:
            for face_processor_name, face_processor_results in faces_results.items():
                # for one face processor
                landmarks = []
                for face in face_processor_results['face']:
                    face_landmarks = self._predictor(img.get_array(), face)
                    landmarks.append(face_landmarks)

                img_results.add(self.name, 'landmarks', landmarks)




                landmarks_dir[face_processor_name] = {
                    'landmarks': landmarks,
                    'color': self._color
                }
                for face in faces_dir1['rectangles']:
                    pass

            img.get_results().add('landmarks', landmarks_dir)
        return img
        '''