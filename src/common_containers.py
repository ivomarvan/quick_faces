#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Různé variace na kontainery, uspořádané slovníky a pod.
'''

import os
import sys

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..'))
sys.path.append(PROJECT_ROOT)

class SortedContainer:

    def __init__(self, reverse:bool=False):
        self._data = {}
        self._reverse = reverse

    def add(self, key:int, data ):
        try:
           list_with_same_key = self._data[key]
           list_with_same_key.append(data)
        except KeyError:
            self._data[key] = [data]

    def gen_sorted(self, reverse:bool=None) -> 'generator':
        if reverse is None:
            reverse = self._reverse
        for key in sorted(self._data.keys(), reverse=reverse):
            for item in self._data[key]:
                yield item


