#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Wrapper for MediaPipe Hands solution.
'''
import sys
import os
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

mp_hands = mp.solutions.hands

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.processor.media_pipe.abstract import AbstractSolution


class HandsSolution(AbstractSolution):

    def __init__(
        self,
        max_num_hands: int = 6,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5
    ):
        super().__init__(
            solution=mp_hands.Hands(
                max_num_hands=max_num_hands,
                min_detection_confidence=min_detection_confidence, 
                min_tracking_confidence=min_tracking_confidence
            )
        )

    def draw(self, img: np.ndarray) -> np.ndarray:
        if self._results.multi_hand_landmarks:
            for hand_landmarks in self._results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    img,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )
        return img

