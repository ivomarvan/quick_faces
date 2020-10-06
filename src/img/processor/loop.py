#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Default loop for process images by list of processor.
'''
import sys
import os

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.source.base import ImgSourceBase
from src.img.storage.base import ImgStorageBase
from src.img.processor.processor import ImgProcessor
from src.utils.timeit_stats import TimeStatistics

class ImgLoop:

    def __init__(
        self,
        img_source: ImgSourceBase,
        img_storage: ImgStorageBase,
        img_processors: [ImgProcessor]
    ):
        self._img_source = img_source
        self._img_storage = img_storage
        self._img_processors = img_processors

    def run(self, log_each_image: bool = True, log_gobal_statistics: bool=True):
        stop = False
        i = 0
        while not stop:
            try:
                # source
                img = self._img_source.process()

                if img is None:
                    raise StopIteration()

                # processors
                for processor in self._img_processors:
                    img = processor.process(img)

                # storage(s)
                img = self._img_storage.process(img)

                # log
                if log_each_image:
                    print(img)
                else:
                    if i % 80 == 0:
                        sys.stdout.write('\n')
                    sys.stdout.write('img/experiments')
                    sys.stdout.flush()
                i += 1
            except StopIteration:
                stop = True
        if log_gobal_statistics:
            print()
            print('===', 'Statistics', '=' * 60)
            TimeStatistics.print_as_tsv(print_header=True)
            print('=' * 80)