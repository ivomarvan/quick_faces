#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Container for results of all img.processors.
    When a processor processes an image, it adds found results like faces, landmarks etc.
'''

import sys
import os

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..'))
sys.path.append(PROJECT_ROOT)


from src.img.container.result import ImageProcessorResult


class ImageProcessorResults:

    def __init__(self):
        self._results_by_history = []
        self._total_time_ms = 0

    def add(self, result: ImageProcessorResult):
        self._results_by_history.append(result)
        self._total_time_ms += result.get_time_ms()

    def get_results_for_processor_super_class(self, superclass) -> [ImageProcessorResult]:
        return [result for result in self._results_by_history if isinstance(result, superclass)]

    def __str__(self):
        s = f'\nresults:'
        for i, result in enumerate(self._results_by_history):
            s += f'\n\t{i:3d}.: \t{result}'
        s += f'\n\ttotal time: {self._total_time_ms} ms'
        return s
