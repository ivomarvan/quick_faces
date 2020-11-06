#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Img processor for decision if mouth is open or close
'''
import sys
import os
import cv2
import numpy as np
from pprint import pprint

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '../..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.image import Image
from src.img.container.result import ImageProcessorResult
from src.img.processor.processor import ImgProcessor
from src.img.processor.landmarks_detector.result import LandmarksDetectorResult, FaceLandmarsks
from src.img.processor.reformat.squere_crop.result import SquereCropResult
from src.img.container.geometry import Point
from src.img.processor.face_detector.result import FaceDetectorResult

class Points:
    '''
    Store selected points of landmarks-
    '''

    def __init__(self, point_numbers: [int]):
        # create placeholder for values of points
        self._values = np.full(shape=(len(point_numbers), 2), fill_value=np.nan, dtype=np.float)
        # create reverse index for lanmarks number
        #   point_number => index in numpy array
        self._reverse_index = {}
        for i, x in enumerate(point_numbers):
            self._reverse_index[x] = i

    def add(self, point_number: int, point: Point):
        if point_number in self._reverse_index:
            index = self._reverse_index[point_number]
            self._values[index][0] = point.x()
            self._values[index][1] = point.y()
            return True
        else:
            return False

    def get_values(self) -> np.ndarray:
        return self._values

    
class PointsPairs:
    '''
    Corresponding points. 
    '''

    def __init__(self, points_pairs: [(int, int)]):
        self._up = Points([x for x,_ in points_pairs])
        self._down = Points([y for y, y in points_pairs])


    def add(self, point_number, point: Point) -> bool:
        '''
        Try to add point values (if point_number is acceptable)
        '''
        return self._up.add(point_number=point_number, point=point) or self._down.add(point_number=point_number, point=point)
            
    def get_distances(self) -> np.ndarray:
        '''
        Returns array of distances of two corresponding points.
        '''
        return np.linalg.norm(self._up.get_values() - self._down.get_values(), axis=1)

    def get_mean_distances(self) -> float:
        '''
        Returns mean of array of distances of two corresponding points
        '''
        return self.get_distances().mean()


class IsOpenManager:
    '''
    Decide if mouth/eye/... is open or not
    '''
    FOUND_MAX_RATE = -np.inf
    FOUND_MIN_RATE = np.inf
    THRESHOLD_PERCENTS  = 25.5

    def __init__(
        self,
        name : str,
        mouth_like_pairs: PointsPairs,
        reference_pairs: PointsPairs,
        max_rate: np.float = FOUND_MAX_RATE,
        min_rate: np.float = FOUND_MIN_RATE,
        threshold_percents: np.float = THRESHOLD_PERCENTS,
        calibration_mode: bool = True
    ):
        self.name = name
        self._mouth_like_pairs = mouth_like_pairs
        self._reference_pairs = reference_pairs
        self._threshold_percents = threshold_percents
        self._max_rate = max_rate
        self._min_rate = min_rate
        self._calibration_mode = calibration_mode
        

    def add(self, point_number, point: Point):
        '''
        Try to add point values (if point_number is acceptable)
        '''
        self._mouth_like_pairs.add(point_number=point_number, point=point)
        self._reference_pairs.add(point_number=point_number, point=point)
    
    def get_rate(self):
        '''
        Compare distances of pairs of points for mouth_like object with same disnces in comparation objects
        '''
        # if self._reference_pairs.get_mean_distances() is 0, it is a error and raising exception is on the place
        rate = self._mouth_like_pairs.get_mean_distances() / self._reference_pairs.get_mean_distances()
        if self._calibration_mode:
            self._min_rate = min(self._min_rate, rate)
            self._max_rate = max(self._max_rate, rate)
        return rate
            
    def open_percents(self) -> float:
        #print(f'min:{self._min_rate}, max:{self._max_rate}' )
        return 100 * (self.get_rate() - self._min_rate) / (self._max_rate - self._min_rate)

    def is_open(self) -> bool:
        return self.open_percents() >= self._threshold_percents

    def get_threshold_percents(self):
        return self._threshold_percents

# --- specific configurations ------------------------------------------------------------------------------------------
class InsightfaceMouthIsOpenManager(IsOpenManager):

    def __init__(
            self,
            calibration_mode: bool = True
    ):
        super().__init__(
            name = 'insightface.106.mouth',
            mouth_like_pairs = PointsPairs([
                (60, 71), (62, 53), (63, 56), (67, 59)
            ]),
            reference_pairs = PointsPairs([
                (72, 80), (1, 2), (25, 24)
            ]),
            calibration_mode = calibration_mode
        )


class IsOpenResult(ImageProcessorResult):

    def __init__(
        self, 
        processor: ImgProcessor,
        time_ms: int = None,
        rate: float = np.nan,
        open_percents: float = np.nan,
        is_open: bool = False,
        face_landmarks: FaceDetectorResult = None,
        threshold_percents: int = None
    ):
        super().__init__(processor=processor, time_ms=time_ms)
        self.rate = rate
        self.open_percents = open_percents
        self.is_open = is_open
        self.face_landmarks = face_landmarks
        self.threshold_percents = threshold_percents


class IsOpenImgProcessor(ImgProcessor):

    def __init__(self, is_open_manager: IsOpenManager):
        super().__init__(name=is_open_manager.name + '.is_open')
        self._is_open_manager = is_open_manager

    def _process_body(self, img: Image = None) -> Image:
        '''
        Face coordinates an landmarks was found in orig_img_array.
        Use landmarks for desicion if mouth/eye/... is open.
        '''
        landmark_results = img.get_results().get_results_for_processor_super_class(LandmarksDetectorResult)  # [FaceLandmarsks]
        for landmark_result in landmark_results: # FaceLandmarsks
            for face_landmarks in landmark_result.get_face_landmark_couples():
                landmarks = face_landmarks.get_landmarks()  # [Point]
                # registre landmarks
                for point_number, landmark_point in enumerate(landmarks):
                    self._is_open_manager.add(point_number=point_number, point=landmark_point)
                # calculate result
                result = IsOpenResult(
                    processor=self,
                    rate=self._is_open_manager.get_rate(),
                    open_percents=self._is_open_manager.open_percents(),
                    is_open=self._is_open_manager.is_open(),
                    face_landmarks=face_landmarks,
                    threshold_percents = self._is_open_manager.get_threshold_percents()
                )
                # print('XXX', result.rate, result.open_percents, result.is_open)

        return img, result


if __name__ == "__main__":
    # for testing
    pp = PointsPairs([
        (64,55), (66,54), (71, 60)
    ])

    # will be ignored, point_number=1 is not registred
    pp.add(point_number=1, point=Point(1000, 2000))

    # will be added tu up
    pp.add(point_number=64, point=Point(0, 1))
    pp.add(point_number=66, point=Point(2, 2))
    pp.add(point_number=71, point=Point(100, 100))

    # will be added to down
    pp.add(point_number=55, point=Point(1, 1))
    pp.add(point_number=54, point=Point(4, 4))
    pp.add(point_number=60, point=Point(100, 105))

    print('up')
    pprint(pp._up.get_values())
    print('down')
    pprint(pp._down.get_values())
    print('distances', pp.get_distances())
    print('metrics', pp.get_mean_distances())

