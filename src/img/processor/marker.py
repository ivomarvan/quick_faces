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
from src.img.processor.base import ImgProcessorBase

class ImgMarkerProcessor(ImgProcessorBase):

    def __init__(self, faces_color=(0, 255, 0), landmarks_color=(0, 0, 255), resize_factor: (int, int) = (1,1)):
        super().__init__('marker')
        self.faces_color = faces_color
        self._landmarks_color = landmarks_color
        self._resize_factor = resize_factor
        # colors are not important params for log
        # self.add_not_none_option('faces_color', faces_color)
        # self.add_not_none_option('landmarks_color', landmarks_color)

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
        faces = img.get_params().get('faces')
        mx, my = self._resize_factor

        def r_x(x: int) -> int:
            return int(round(mx * x, 0))

        def r_y(y: int) -> int:
            return int(round(my * y, 0))

        if faces:
            for rect in faces:
                (x, y, w, h) = face_utils.rect_to_bb(rect)
                cv2.rectangle(img.get_array(), ( r_x(x),  r_y(y)), (r_x(x + w),  r_y(y + h)), self.faces_color, 2)
        faces_landmarks = img.get_params().get('landmarks')
        if faces_landmarks:
            for landmarks in faces_landmarks:
                shape = face_utils.shape_to_np(landmarks)
                for (sX, sY) in shape:
                    cv2.circle(img.get_array(), (r_x(sX), r_y(sY)), 1, self._landmarks_color, -1)

        return img