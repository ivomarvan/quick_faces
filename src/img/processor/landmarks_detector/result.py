#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Normalized result for landmarks detector (prediktor)
'''

import sys
import os

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.result import ImageProcessorResult
from src.img.container.geometry import Point, Rectangle
from src.img.processor.processor import ImgProcessor
from src.img.processor.face_detector.result import FaceDetectorResult

class FaceLandmarsks:

    def __init__(self, face_result: FaceDetectorResult, landmarks: [Point], face_index:int):
        self._face_result = face_result
        self._landmarks = landmarks
        self._face_index = face_index

    def get_face_result(self) -> FaceDetectorResult:
        return self._face_result

    def get_landmarks(self) -> [Point]:
        return self._landmarks

    def get_face_index(self) -> int:
        return self._face_index

    def get_actual_face(self) -> Rectangle:
        return self.get_face_result().get_rectangles()[self.get_face_index()]

    def __str__(self):
        s = f'\n\t\tlandmarks: {self.get_landmarks()}'
        s += f'\n\t\t\tfor face: {self.get_face_index()}:{self.get_actual_face()} - {self.get_face_result().get_processor().get_name()}'
        return s

class LandmarksDetectorResult(ImageProcessorResult):

    def __init__(self, processor: ImgProcessor, time_ms: int = None, face_landmark_couples: [FaceLandmarsks] = []):
        super().__init__(processor=processor, time_ms=time_ms)
        self._face_landmark_couples = face_landmark_couples

    def get_face_landmark_couples(self) -> [FaceLandmarsks]:
        return self._face_landmark_couples

    def __str__(self):
        s = super().__str__()
        for face_landmark_cuple in self.get_face_landmark_couples():
            s += f'{face_landmark_cuple}'
        return s