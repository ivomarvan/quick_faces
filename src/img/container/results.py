#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Container for results of img.processor.
    When a processor processes an image, it adds found results like faces, landmarks etc.
'''

from typing import Any
from collections import OrderedDict


class ImageProcessorResults:

    def __init__(self):
        self._data = OrderedDict()

    def add(self, processor_name: str, param_name: str, value: Any):
        try:
            processor_results = self._data[processor_name]
        except KeyError:
            processor_results = self._data[processor_name] = OrderedDict()
        processor_results[param_name] = {param_name: value}


    def get_results_with_given_result_name(self, param_name: str):
        ret = OrderedDict()
        for processor_name, processor_results in self._data.items():
            if param_name in processor_results:
                ret[processor_name] = processor_results
        return ret

    def __str__(self):
        s = f'\n\tparams:'
        for processor_name, results_dir in self._data.items():
            s += f'\n\tprocessor:{processor_name} => '
            for parametr_name, results in results_dir.items():
                s += f'\n\t\t{parametr_name} : {results}'
        return s
