#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Insightface face detector as img processor.
    @credit https://github.com/deepinsight/insightface
'''
import sys
import os
import numpy as np
import insightface

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.image import Image
from src.img.processor.face_detector.face_detector import FaceDetector
from src.img.processor.face_detector.result import FaceDetectorResult
from src.img.container.geometry import Point, Rectangle


class InsightfaceFaceDetector(FaceDetector):

    def __init__(
        self,
        model_name: str = 'retinaface_mnet025_v2',
        find_best: bool = False,
        ctx_id: int =-1,
        color: tuple = (123, 41, 87)
    ):
        '''
        You can replace 'retinaface_mnet025_v2' with your own face detector,  for example'retinaface_r50_v1'
        '''
        super().__init__(name='insightface.' + model_name, find_best=find_best, color=color)
        self._get_all = not find_best
        self._detector = insightface.model_zoo.get_model(model_name)
        self._detector.prepare(ctx_id=ctx_id)
        self.add_not_none_option('model', model_name)

    def _process_body(self, img: Image = None) -> (Image, FaceDetectorResult):
        img_array = img.get_work_img_array()
        bboxes, _ = self._detector.detect(img_array)
        if bboxes.shape[0] == 0:
            return np.ndarray([])
        if not self._get_all:
            areas = []
            for i in range(bboxes.shape[0]):
                x = bboxes[i]
                area = (x[2] - x[0]) * (x[3] - x[1])
                areas.append(area)
            m = np.argsort(areas)[-1]
            bboxes = bboxes[m:m + 1]
        faces_rectangles = []
        for bbox in bboxes:
            # w, h = (bbox[2] - bbox[0]), (bbox[3] - bbox[1])
            faces_rectangles.append(
                Rectangle(
                    left_top=Point(x=bbox[0], y=bbox[1]),
                    right_bottom=Point(x=bbox[2], y=bbox[3])
                )
            )
        print(f'{faces_rectangles}')
        return img, FaceDetectorResult(self, rectangles=faces_rectangles)

