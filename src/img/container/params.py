#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Container for the params of image.
    When a processor processes an image, it adds found params like faces, landmarks etc. 
'''
from typing import Any



class ImageParams:

    def __init__(self, print_separator: str = '\n\t'):
        self._data = {}
        self._print_separator = print_separator


    def add(self, key: str, value: Any):
        self._data[key] = value

    def get(self, key: str):
        try:
            return self._data[key]
        except KeyError:
            return None

    def copy(self, other_params: 'ImageParams', keys_to_copy: [str]):
        for key in keys_to_copy:
            value = other_params.get(key)
            self.add(key, value)


    def __str__(self):
        s = f'{self._print_separator}params:'
        for name, value in self._data.items():
            s += f'{self._print_separator} {name} => "{value}"'
        return s