#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Img processor for writing numbers of landmarks.
'''
import sys
import os
import cv2

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '../../..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.image import Image
from src.img.container.result import ImageProcessorResult
from src.img.processor.processor import ImgProcessor
from src.img.processor.landmarks_detector.result import LandmarksDetectorResult, FaceLandmarsks
from src.img.processor.face_detector.result import FaceDetectorResult
from src.img.processor.reformat.squere_crop.result import SquereCropResult

class LandmarkNumbersImgProcessor(ImgProcessor):

    FONT_SCALE = 0.4
    FONT = cv2.FONT_HERSHEY_SIMPLEX  # FONT_HERSHEY_PLAIN
    THICKNESS = 1

    def __init__(self, resize_factor: (int, int) = (1,1)):
        super().__init__('add_numers_for_landmarks')
        self._resize_factor = resize_factor
        self.add_not_none_option('resize_factor', self._resize_factor)

    def _process_image(self, img: Image = None) -> (Image, FaceDetectorResult):
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

            # get the width and height of the text box



        landmark_results = img.get_results().get_results_for_processor_super_class(LandmarksDetectorResult)  # [FaceLandmarsks]
        for landmark_result in landmark_results: # FaceLandmarsks
            for face_landmarks in landmark_result.get_face_landmark_couples():
                landmarks = face_landmarks.get_landmarks()  # [Point]
                face_result =  face_landmarks.get_face_result()  # FaceDetectorResult
                landmarks_color = landmark_result.get_processor().get_option('color')
                face_color = face_result.get_processor().get_option('color')

                # draw landmarks
                print('*******', len(landmarks))
                for i, landmark_point in enumerate(landmarks):
                    '''
                    if i % 2 == 0: 
                        continue
                    '''
                    x, y = landmark_point.x(), landmark_point.y()
                    try:
                        text = str(i)
                        # cv2.getTextSize(text, self.FONT, fontScale=self.FONT_SCALE, thickness=self.THICKNESS)[0]
                        (text_width, text_height) = cv2.getTextSize(text,  fontFace=self.FONT, fontScale=self.FONT_SCALE, thickness=self.THICKNESS)[0]
                        #                         # set the text start position
                        text_offset_x = max(0, r_x(x))
                        text_offset_y = r_y(y) - int(text_height / 2)
                        cv2.putText(
                            orig_img_array, text, (text_offset_x, text_offset_y), self.FONT, fontScale=self.FONT_SCALE,
                            color=landmarks_color, thickness=self.THICKNESS
                        )

                    except Exception as e:
                        raise e
                        print('$' * 5, e)

        return img, ImageProcessorResult(self)
