#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Abstract class for MediaPipe solutions wrapers.
'''

import numpy as np


class AbstractSolution:

    def __init__(self, solution: 'mp.SolutionBase'):
        self._solution = solution
        self._results = None

    def process(self, img: np.ndarray):
        self._results = self._solution.process(img)
        return self._results

    def draw(self, img: np.ndarray) -> np.ndarray:
        raise NotImplementedError(f'Do not use object of abstract class "{self.__class__.__name__}"!')