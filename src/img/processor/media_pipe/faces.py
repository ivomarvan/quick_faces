#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Wrapper for MediaPipe FaceMesh solution.
'''

import mediapipe as mp
import sys
import os
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

mp_face_mesh = mp.solutions.face_mesh


# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.processor.media_pipe.abstract import AbstractSolution

class FaceMeshSolution(AbstractSolution):

    def __init__(
        self,
        max_num_faces: int = 5,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5
    ):
        super().__init__(
            solution=mp_face_mesh.FaceMesh(
                max_num_faces = max_num_faces,
                min_detection_confidence=min_detection_confidence,
                min_tracking_confidence=min_tracking_confidence
            )
        )

    def draw(self, img: np.ndarray) -> np.ndarray:
        if self._results.multi_face_landmarks:
            for face_landmarks in self._results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=img,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                        .get_default_face_mesh_tesselation_style()
                )
                mp_drawing.draw_landmarks(
                    image=img,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                        .get_default_face_mesh_contours_style()
                )
        return img

