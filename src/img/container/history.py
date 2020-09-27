#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Container for the history of image.
    When a processor processes an image, it adds its name and processing time to the history. 
'''
from collections import OrderedDict

class ImageHistory:

    def __init__(self, level: int=0, print_separator: str = '\n\t'):
        self._data = OrderedDict()
        self._print_separator = print_separator + '\t' * level
        self._total_time_ms = 0
        self._level = level

    def add(self, processor_name: str, time_ms: int):
        self._data[processor_name] = time_ms
        self._total_time_ms += time_ms

    def add_history(self, processor_name: str, subprocesses_history: 'ImageHistory'):
        self._data[processor_name] = subprocesses_history
        self._total_time_ms += subprocesses_history._total_time_ms

    def __str__(self):
        if self._level <= 0:
            s = f'{self._print_separator}history:'
        else:
            s = ''
        for i, (processor_name, value) in enumerate(self._data.items()):
            if isinstance(value, int):
                s += f'{self._print_separator}{i:3d}. {processor_name} => {value} ms'
            else:
                s += f'{self._print_separator}{i:3d}. {processor_name} => {value}'
        s += f'{self._print_separator}sum: {self._total_time_ms} ms'
        return s