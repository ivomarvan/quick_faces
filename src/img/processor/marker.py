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
                print(face_rectangle, landmarks)
                exit()


        faces_results = img.get_results().get_results_for_processor_super_class(FaceDetectorResult)

        faces_dir = img.get_results().get('faces')
        landmarks_dir = img.get_results().get('landmarks')
        if faces_dir:
            for face_processor_name, faces_dir1 in faces_dir.items():
                for face in faces_dir1['rectangles']:
                    (x, y, w, h) = face_utils.rect_to_bb(face)
                    cv2.rectangle(img.get_array(), ( r_x(x),  r_y(y)), (r_x(x + w),  r_y(y + h)), faces_dir1['color'], 2)

                if landmarks_dir:
                    landmarks_dir1 = landmarks_dir[face_processor_name]
                    for landmarks in landmarks_dir1['landmarks']:
                        shape = face_utils.shape_to_np(landmarks)
                        for (sX, sY) in shape:
                            cv2.circle(img.get_array(), (r_x(sX), r_y(sY)), 3, faces_dir1['color'], 2)
                            cv2.circle(img.get_array(), (r_x(sX), r_y(sY)), 2 - 1, landmarks_dir1['color'], -1)

        return img