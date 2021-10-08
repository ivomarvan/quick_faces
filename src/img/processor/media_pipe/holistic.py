#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Wrapper for MediaPipe Holistic solution.
'''
import sys
import os
import mediapipe as mp
import numpy as np

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

mp_holistic = mp.solutions.holistic

from src.img.processor.media_pipe.abstract import AbstractSolution


class HolisticSolutions(AbstractSolution):
    mp_pose = mp.solutions.pose

    def __init__(self, min_detection_confidence: float = 0.5, min_tracking_confidence: float = 0.5):
        super().__init__(
            solution=mp_holistic.Holistic(
                min_detection_confidence=min_detection_confidence,
                min_tracking_confidence=min_tracking_confidence
            )
        )

    def draw(self, img: np.ndarray) -> np.ndarray:
        mp_drawing.draw_landmarks(
            img,
            self._results.face_landmarks,
            mp_holistic.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
                .get_default_face_mesh_contours_style()
        )
        mp_drawing.draw_landmarks(
            img,
            self._results.pose_landmarks,
            mp_holistic.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles
                .get_default_pose_landmarks_style()
        )
        return img
