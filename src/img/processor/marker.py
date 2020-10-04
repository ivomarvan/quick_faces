#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Img processor for writing tags to image.
'''
import sys
import os
import cv2
from imutils import face_utils


# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.image import Image
from src.img.container.result import ImageProcessorResult
from src.img.processor.processor import ImgProcessor
from src.img.processor.landmarks_detector.result import LandmarksDetectorResult, FaceLandmarsks

class ImgMarkerProcessor(ImgProcessor):

    def __init__(self, resize_factor: (int, int) = (1,1)):
        super().__init__('marker')
        self._resize_factor = resize_factor
        self.add_not_none_option('resize_factor', self._resize_factor)

    def set_resize_factor(self, orig_img:Image, work_img:Image):
        '''
        Face coordinates an landmarks was found in work_img.
        But work_img was created by resizing of orig_img image
        We want to mark found points in orig_img.
        '''
        orig_shape = orig_img.get_shape()
        h_orig = orig_shape[0]
        w_orig = orig_shape[1]
        
        work_shape = work_img.get_shape()
        h_work = work_shape[0]
        w_work = work_shape[1]

        self._resize_factor = w_orig / w_work, h_orig / h_work

    def _process_body(self, img: Image = None) -> Image:

        mx, my = self._resize_factor

        def r_x(x: int) -> int:
            return int(round(mx * x, 0))

        def r_y(y: int) -> int:
            return int(round(my * y, 0))

        landmark_results = img.get_results().get_results_for_processor_super_class(LandmarksDetectorResult)  # [FaceLandmarsks]
        for landmark_result in landmark_results: # FaceLandmarsks
            for face_landmarks in landmark_result.get_face_landmark_couples():
                landmarks = face_landmarks.get_landmarks()  # [Point]
                face_result =  face_landmarks.get_face_result()  # FaceDetectorResult
                face_rectangle = face_landmarks.get_actual_face()
                landmarks_color = landmark_result.get_processor().get_option('color')
                face_color = face_result.get_processor().get_option('color')

                # draw face
                l_t = face_rectangle.left_top()
                x1 = l_t.x()
                y1 = l_t.y()
                r_b = face_rectangle.right_bottom()
                x2 = r_b.x()
                y2 = r_b.y()
                cv2.rectangle(
                    img.get_array(),
                    (r_x(x1), r_y(y1)), (r_x(x2), r_y(y2)), face_color, 2)

                # draw landmarks
                for landmark_point in landmarks:
                    x, y = landmark_point.x(), landmark_point.y()
                    cv2.circle(img.get_array(), (r_x(x), r_y(y)), 1, face_color, 2)
                    cv2.circle(img.get_array(), (r_x(x), r_y(y)), 2, landmarks_color, -1)

        return img, ImageProcessorResult(self)