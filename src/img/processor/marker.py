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

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.image import Image
from src.img.container.result import ImageProcessorResult
from src.img.processor.processor import ImgProcessor
from src.img.processor.landmarks_detector.result import LandmarksDetectorResult, FaceLandmarsks
from src.img.processor.face_detector.result import FaceDetectorResult
from src.img.processor.reformat.squere_crop.result import SquereCropResult

class ImgMarkerProcessor(ImgProcessor):

    def __init__(self, resize_factor: (int, int) = (1,1)):
        super().__init__('marker')
        self._resize_factor = resize_factor
        self.add_not_none_option('resize_factor', self._resize_factor)

    def _process_body(self, img: Image = None) -> Image:
        '''
        Face coordinates an landmarks was found in orig_img_array.
        But work_img was created by resizing of work_img_array
        We want to mark found points in orig_img_array.
        '''
        orig_img_array = img.get_orig_img_array()
        work_img_array = img.get_work_img_array()

        orig_shape = orig_img_array.shape
        h_orig = orig_shape[0]
        w_orig = orig_shape[1]

        work_shape = work_img_array.shape
        h_work = work_shape[0]
        w_work = work_shape[1]

        reformat_result = img.get_results().get_results_for_processor_super_class(SquereCropResult)
        if reformat_result:
            img_scale = reformat_result[0].get_img_scale()
            mx, my = img_scale, img_scale
        else:
            mx, my = w_orig / w_work, h_orig / h_work

        def r_x(x: int) -> int:
            return int(round(mx * x, 0))

        def r_y(y: int) -> int:
            return int(round(my * y, 0))

        faces_results = img.get_results().get_results_for_processor_super_class(FaceDetectorResult)
        for face_result in faces_results:
            face_color = face_result.get_processor().get_option('color')
            for face_rectangle in face_result.get_rectangles():
                # draw face
                l_t = face_rectangle.left_top()
                x1 = l_t.x()
                y1 = l_t.y()
                r_b = face_rectangle.right_bottom()
                x2 = r_b.x()
                y2 = r_b.y()
                pt1 = (r_x(x1), r_y(y1))
                pt2 = (r_x(x2), r_y(y2))
                try:
                    cv2.rectangle(img=orig_img_array, pt1=pt1, pt2=pt2, color=face_color, thickness=2)
                except Exception as e:
                    print('!' * 5, e)


        landmark_results = img.get_results().get_results_for_processor_super_class(LandmarksDetectorResult)  # [FaceLandmarsks]
        for landmark_result in landmark_results: # FaceLandmarsks
            for face_landmarks in landmark_result.get_face_landmark_couples():
                landmarks = face_landmarks.get_landmarks()  # [Point]
                face_result =  face_landmarks.get_face_result()  # FaceDetectorResult
                landmarks_color = landmark_result.get_processor().get_option('color')
                face_color = face_result.get_processor().get_option('color')

                # draw landmarks
                for landmark_point in landmarks:
                    x, y = landmark_point.x(), landmark_point.y()
                    try:
                        cv2.circle(orig_img_array, (r_x(x), r_y(y)), 1, face_color, 2)
                        cv2.circle(orig_img_array, (r_x(x), r_y(y)), 2, landmarks_color, -1)
                    except Exception as e:
                        print('$' * 5, e)

        return img, ImageProcessorResult(self)
