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
import numpy as np

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '../../..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.image import Image
from src.img.container.result import ImageProcessorResult
from src.img.processor.processor import ImgProcessor
from src.img.processor.reformat.squere_crop.result import SquereCropResult
from src.img.processor.faces.evaluation.is_open import IsOpenResult

class IsOpenMarkerImgProcessor(ImgProcessor):

    FONT_SCALE = 0.6
    FONT = cv2.FONT_HERSHEY_SIMPLEX  # FONT_HERSHEY_PLAIN
    THICKNESS = 1
    DEFAULT_COLOR = (255, 255, 0)
    INDICATOR_WIDTH = 20
    INDICATOR_HEIGHT = 60

    def __init__(self, resize_factor: (int, int) = (1,1)):
        super().__init__('is_open.marker')
        self._resize_factor = resize_factor
        self.add_not_none_option('resize_factor', self._resize_factor)


    def _draw_indicator(self, start_y: int,  img: np.array, is_open_result: IsOpenResult, name: str) -> int:
        '''
        Draw rectangle with open result
        '''
        shift_x = 2

        # upper part
        if np.isnan(is_open_result.open_percents):
            # before calibration
            return start_y

        color = (10, 15, 20)
        (text_width, text_height) = cv2.getTextSize(name, fontFace=self.FONT, fontScale=self.FONT_SCALE, thickness=self.THICKNESS)[0]
        cv2.putText(
            img, name, (shift_x, start_y + text_height), self.FONT, fontScale=self.FONT_SCALE, color=color, thickness=self.THICKNESS
        )
        start_y += 5 + text_height

        color = (255, 255, 255)
        height = int((100 - is_open_result.open_percents) * self.INDICATOR_HEIGHT / 100)
        points = np.array( [[
            [shift_x, start_y],
            [shift_x + self.INDICATOR_WIDTH, start_y],
            [shift_x + self.INDICATOR_WIDTH, start_y + height],
            [shift_x, start_y + height],
        ]], dtype=np.int32 )
        cv2.fillPoly(img, points, color)

        # down parts
        start_y1 = start_y + height
        height1 = int(is_open_result.open_percents * self.INDICATOR_HEIGHT / 100)
        if is_open_result.is_open:
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)
        points = np.array([[
            [shift_x, start_y1],
            [shift_x + self.INDICATOR_WIDTH, start_y1],
            [shift_x + self.INDICATOR_WIDTH, start_y1 + height1],
            [shift_x, start_y1 + height1],
        ]], dtype=np.int32)
        cv2.fillPoly(img, points, color)

        # threshold
        y = start_y + int((100 - is_open_result.threshold_percents) * self.INDICATOR_HEIGHT / 100)
        cv2.line(img, (shift_x, y), (self.INDICATOR_WIDTH + 2 * shift_x, y), color=(0,0,0), thickness=1)

        cv2.rectangle(img, (shift_x, start_y), (shift_x + self.INDICATOR_WIDTH, start_y + self.INDICATOR_HEIGHT), color=(10,10,10), thickness=1)
        return start_y + self.INDICATOR_HEIGHT


    def _process_image(self, img: Image = None) -> (Image, ImageProcessorResult):
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


        is_open_results = img.get_results().get_results_for_processor_super_class(IsOpenResult)
        start_y = 0
        for i, is_open_result in enumerate(is_open_results):
            face_landmarks = is_open_result.face_landmarks  # FaceLandmarsks
            try:
                result_short_name = is_open_result.get_processor().get_name().split('.')[-2]
                lt = face_landmarks.get_actual_face().left_top()
                face_result = face_landmarks.get_face_result()  # FaceDetectorResult:
                face_processor = face_result.get_processor()
                face_color = face_processor.get_option('color')
                if not face_color:
                    face_color = self.DEFAULT_COLOR
                text = f'{result_short_name:15}: {round(is_open_result.rate, 2)}, {round(is_open_result.open_percents, 2)} %, open={is_open_result.is_open}'
                (text_width, text_height) = cv2.getTextSize(text,  fontFace=self.FONT, fontScale=self.FONT_SCALE, thickness=self.THICKNESS)[0]
                # set the text start position
                text_offset_x = int(max(0, r_x(lt.x())))
                text_offset_y = int(max(0, r_y(lt.y()) - ((i + 1) * (text_height + 5))))
                cv2.putText(
                    orig_img_array, text, (text_offset_x, text_offset_y), self.FONT, fontScale=self.FONT_SCALE,
                    color=face_color, thickness=self.THICKNESS
                )
                start_y = self._draw_indicator(
                    start_y=start_y, img=orig_img_array, is_open_result=is_open_result, name=result_short_name
                )

            except Exception as e:
                raise e
                print('$' * 5, e)

        return img, ImageProcessorResult(self)
