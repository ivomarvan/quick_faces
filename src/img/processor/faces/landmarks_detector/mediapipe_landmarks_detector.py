#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Mediapip landmarks detector (predictor in some terminology) as img processor.
    @credit https://mediapipe.dev/
    @credit https://techtutorialsx.com/2021/05/19/mediapipe-face-landmarks-estimation/
    
'''
import sys
import os
import numpy as np
import cv2
import mediapipe
from mediapipe.framework.formats import landmark_pb2
from mediapipe.python.solutions.drawing_utils import VISIBILITY_THRESHOLD, PRESENCE_THRESHOLD, _normalized_to_pixel_coordinates

drawingModule = mediapipe.solutions.drawing_utils
faceModule = mediapipe.solutions.face_mesh


# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '../..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)
NOGIT_DATA = os.path.join(PROJECT_ROOT, 'nogit_data')

from src.img.container.geometry import Point, Rectangle
from src.img.container.image import Image
from src.img.processor.processor import ImgProcessor
from src.img.processor.faces.landmarks_detector.result import LandmarksDetectorResult, FaceLandmarsks
from src.img.processor.faces.face_detector.result import FaceDetectorResult

COLOR = (255, 100, 100)

class MediapipeLandmarksDetectorImgProcessor(ImgProcessor):

    def __init__(
        self,
        quick_faces_color: tuple = COLOR,
        static_image_mode: bool = True,
        draw_mediapipe_way_color: tuple = COLOR  # or None for no drawing
    ):
        super().__init__(f'Mediapipe.landmarks_predictor')

        self._color = quick_faces_color
        self.add_not_none_option('color', quick_faces_color)
        self._draw_mediapipe_way_color = draw_mediapipe_way_color
        if draw_mediapipe_way_color is not None:
            self._circleDrawingSpec = drawingModule.DrawingSpec(thickness=1, circle_radius=1, color=draw_mediapipe_way_color)
            self._lineDrawingSpec = drawingModule.DrawingSpec(thickness=1, color=draw_mediapipe_way_color)

        self._detector = faceModule.FaceMesh(static_image_mode=static_image_mode)

    def _landmarks_to_points(self, landmarks: dict) -> [Point]:
        return [Point(x=l[0], y=l[1]) for key, l in landmarks.items()]

    def _tranform_mediapipe_landmarks(self,  landmark_list: landmark_pb2.NormalizedLandmarkList, image:np.ndarray):
        image_rows, image_cols, _ = image.shape
        idx_to_coordinates = {}
        for idx, landmark in enumerate(landmark_list.landmark):
            if ((landmark.HasField('visibility') and
                 landmark.visibility < VISIBILITY_THRESHOLD) or
                    (landmark.HasField('presence') and
                     landmark.presence < PRESENCE_THRESHOLD)):
                continue
            landmark_px = _normalized_to_pixel_coordinates(landmark.x, landmark.y,
                                                           image_cols, image_rows)
            if landmark_px:
                idx_to_coordinates[idx] = landmark_px
        return idx_to_coordinates

    def _process_image(self, img: Image = None) -> (Image, LandmarksDetectorResult):
        work_img = img.get_work_img_array()
        face_landmark_couples = []
        results = self._detector.process(cv2.cvtColor(work_img, cv2.COLOR_BGR2RGB))

        rectangles = []
        landmarks_in_good_format = []
        if results.multi_face_landmarks != None:
            for face_index, faceLandmarks in enumerate(results.multi_face_landmarks):
                transformed_landmarks = self._tranform_mediapipe_landmarks(landmark_list=faceLandmarks, image=work_img)
                landmarks_list_of_Points = self._landmarks_to_points(transformed_landmarks)
                xs = [l.x() for l in landmarks_list_of_Points]
                ys = [l.y() for l in landmarks_list_of_Points]
                rectangles.append(
                    Rectangle(
                        left_top=Point(x=min(xs), y=min(ys)),
                        right_bottom=Point(x=max(xs), y=max(ys))
                    )
                )
                landmarks_in_good_format.append(landmarks_list_of_Points)

                # drow like mesiapipe
                if self._draw_mediapipe_way_color is not None:

                    drawingModule.draw_landmarks(
                        work_img, faceLandmarks, faceModule.FACE_CONNECTIONS,
                        self._circleDrawingSpec, self._lineDrawingSpec
                    )
                    cv2.imshow('mediapipe_debug', work_img)
        else:
            # drow like mesiapipe
            if self._draw_mediapipe_way_color is not None:
                cv2.imshow('mediapipe_debug', work_img)

        # print('-' * 80)
        # print(rectangles)
        # print(landmarks_in_good_format)
        # print('='*80)
        face_detector_result = FaceDetectorResult(processor=self, time_ms=0, rectangles=rectangles)
        for face_index, landmarks_for_one_face in enumerate(landmarks_in_good_format):
            if self._color is None:
                landmarks_for_one_face = []
            face_landmark_couples.append(
                FaceLandmarsks(face_result=face_detector_result, landmarks=landmarks_for_one_face, face_index=face_index))



        return img,  LandmarksDetectorResult(self, face_landmark_couples=face_landmark_couples)
