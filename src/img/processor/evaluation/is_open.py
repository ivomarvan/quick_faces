#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = """
    Img processor for decision if mouth is open or close
"""
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

class PointsPairs:
    """
    Corresponding points and conection to real values from landmarks
    """

    def __init__(self, points_pairs_id: [(int, int)]):
        """
        The points_pairs_id is list of pairs of id which are relevnt in the case.
        For task as "left eye" us importantn, that one ID can be used more times.
        """
        def add_id(d:dict, i:int, id:int):
            """
            Crete dictionary: id => list of position in values array.
            """
            if not id in d:
                d[id] = []
            d[id].append(i)

        self._id_to_positions1 = {}  # id1 => [position] for id1 in  [(id1, _)]
        self._id_to_positions2 = {}  # id2 => [position] for id1 in  [(_, id2)]

        for i, (id1,id2) in enumerate(points_pairs_id):
            add_id(self._id_to_positions1, i, id1)
            add_id(self._id_to_positions2, i, id2)

        # create placeholder for values of points
        self._xy_values_array1 = np.full(shape=(len(points_pairs_id), 2), fill_value=np.nan, dtype=np.float)
        self._xy_values_array2 = np.full(shape=(len(points_pairs_id), 2), fill_value=np.nan, dtype=np.float)

    def reset_values(self):
        self._xy_values_array1[:, :] = np.nan
        self._xy_values_array2[:, :] = np.nan

    def add(self, point_number, point: Point) -> bool:
        """
        Try to add real valuses (from piscture, i.e. point.x() and point.y()) to all corespondet places
        Return True just when point_numer/point are used.
        """
        def add_value(id: int, index_dict: dict, point: Point, values_array: np.ndarray) -> bool:
            if id in index_dict:
                for index in index_dict[id]:
                    values_array[index][0] = point.x()
                    values_array[index][1] = point.y()
                return True
            else:
                return False

        return add_value(point_number, self._id_to_positions1, point, self._xy_values_array1) \
            or add_value(point_number, self._id_to_positions2, point, self._xy_values_array2)
            
    def _get_distances(self) -> np.ndarray:
        """
        Returns array of distances of two corresponding points.
        """
        return np.linalg.norm(self._xy_values_array1 - self._xy_values_array2, axis=1)

    def get_mean_distances(self) -> float:
        """
        Returns mean of array of distances of two corresponding points
        """
        return self._get_distances().mean()

    def debug_print(self):
        print('id to positions 1', self._id_to_positions1)
        print('id to positions 2', self._id_to_positions2)
        print('xy_values_array 1', self._xy_values_array1.shape, "\n", self._xy_values_array1)
        print()
        print('xy_values_array 2', self._xy_values_array2.shape, "\n",  self._xy_values_array2)
        print()
        distances = self._get_distances()
        print('distances', distances.shape, distances)
        print('metrics', self.get_mean_distances())

class IsOpenManager:
    """
    Decide if mouth/eye/... is open or not
    """
    FOUND_MAX_RATE = -np.inf
    FOUND_MIN_RATE = np.inf
    THRESHOLD_PERCENTS = 25.5

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
        """
        Try to add point values (if point_number is acceptable)
        """
        self._mouth_like_pairs.add(point_number=point_number, point=point)
        self._reference_pairs.add(point_number=point_number, point=point)
    
    def get_rate_rate_percents_is_open(self) -> (float, float, bool):
        """
        Compare distances of pairs of points for mouth_like object with same disnces in comparation objects
        """
        # if self._reference_pairs.get_mean_distances() is 0, it is a error and raising exception is on the place
        rate = self._mouth_like_pairs.get_mean_distances() / self._reference_pairs.get_mean_distances()
        if self._calibration_mode:
            self._min_rate = min(self._min_rate, rate)
            self._max_rate = max(self._max_rate, rate)
        percents = 100 * (rate - self._min_rate) / (self._max_rate - self._min_rate)
        is_open = percents >= self._threshold_percents
        '''
        print(f'{self.name}, min:{self._min_rate:2.3f}, max:{self._max_rate:2.3f}')
        print(f'{self.name}, rate:{rate:2.3f}, ({percents:2.3f} %), open:{is_open}')
        print(f'{self.name}, in:{self._mouth_like_pairs.get_mean_distances():2.3f}, ref:{self._reference_pairs.get_mean_distances():2.3f}')
        '''
        return rate, percents, is_open

    def get_threshold_percents(self):
        return self._threshold_percents

# --- specific configurations for mouth --------------------------------------------------------------------------------
class InsightfaceMouthIsOpenManager(IsOpenManager):

    def __init__(
            self,
            calibration_mode: bool = True,
            threshold_percents: np.float = 25.0
    ):
        super().__init__(
            name = 'insightface.106.mouth',
            mouth_like_pairs = PointsPairs([
                (60, 71), (62, 53), (63, 56), (67, 59)
            ]),
            reference_pairs = PointsPairs([
                (72, 80), (1, 2), (25, 20)
            ]),
            calibration_mode = calibration_mode,
            threshold_percents=threshold_percents
        )


# --- specific configurations for left eye  ----------------------------------------------------------------------------
class InsightfaceLeftEyeIsOpenManager(IsOpenManager):

    def __init__(
            self,
            calibration_mode: bool = True,
            threshold_percents: np.float = 50.0
    ):
        center_of_left_eye = 92 # or 88
        obj_list = []
        for second in [87, 89, 90, 91] + list(range(93, 103)):
            obj_list.append((center_of_left_eye, second))
        super().__init__(
            name = 'insightface.106.left eye',
            mouth_like_pairs = PointsPairs(
                # [(95, 90), (94, 87), (96, 91)]
                # [(94, 87)]
                obj_list
            ),
            reference_pairs = PointsPairs([
                (72, 80), (1, 2), (25, 20)
            ]),
            calibration_mode = calibration_mode,
            threshold_percents = threshold_percents
        )

# --- specific configurations for right eye  ----------------------------------------------------------------------------
class InsightfaceRightEyeIsOpenManager(IsOpenManager):

    def __init__(
            self,
            calibration_mode: bool = True,
            threshold_percents: np.float = 50.0
    ):
        center_of_right_eye = 34 # or 38
        obj_list = []
        for second in [33, 35, 36, 37] + list(range(39, 52)):
            obj_list.append((center_of_right_eye, second))
        super().__init__(
            name = 'insightface.106.right eye',
            mouth_like_pairs = PointsPairs(
                # [(41, 36), (40, 33), (42, 37)]
                # [(41, 36), (40, 33), (42, 37)]
                obj_list
            ),
            reference_pairs = PointsPairs([
                (72, 80), (1, 2), (25, 20)
            ]),
            calibration_mode = calibration_mode,
            threshold_percents = threshold_percents
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
        """
        Face coordinates an landmarks was found in orig_img_array.
        Use landmarks for desicion if mouth/eye/... is open.
        """
        result = ImageProcessorResult(processor=self)
        landmark_results = img.get_results().get_results_for_processor_super_class(LandmarksDetectorResult)  # [FaceLandmarsks]
        for landmark_result in landmark_results: # FaceLandmarsks
            for face_landmarks in landmark_result.get_face_landmark_couples():
                landmarks = face_landmarks.get_landmarks()  # [Point]
                # registre landmarks
                for point_number, landmark_point in enumerate(landmarks):
                    self._is_open_manager.add(point_number=point_number, point=landmark_point)
                # calculate result
                rate, percents, is_open = self._is_open_manager.get_rate_rate_percents_is_open()
                result = IsOpenResult(
                    processor=self,
                    rate=rate,
                    open_percents=percents,
                    is_open=is_open,
                    face_landmarks=face_landmarks,
                    threshold_percents = self._is_open_manager.get_threshold_percents()
                )
                # print('XXX', result.rate, result.open_percents, result.is_open)

        return img, result


if __name__ == "__main__":
    # for testing
    def add_verbose(pp: PointsPairs, point_number: int, point: Point):
        success = pp.add(point_number=point_number, point=point)
        print(f'add({point_number}, {point}) -> {success}')
        
        
    coresponding_points_ids = [
        (64,55), (66,54), (71, 60)
    ]
    pp = PointsPairs(coresponding_points_ids)

    print('list of coresponding ids', coresponding_points_ids)
    # will be ignored, point_number=1 is not registred
    add_verbose(pp=pp, point_number=1, point=Point(1000, 2000))

    # will be added tu up
    add_verbose(pp=pp, point_number=64, point=Point(0, 1))
    add_verbose(pp=pp, point_number=66, point=Point(2, 2))
    add_verbose(pp=pp, point_number=71, point=Point(100, 100))

    # will be added to down
    add_verbose(pp=pp, point_number=55, point=Point(1, 1))
    add_verbose(pp=pp, point_number=54, point=Point(4, 4))
    add_verbose(pp=pp, point_number=60, point=Point(100, 105))

    pp.debug_print()


