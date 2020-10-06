#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Shortcut for selecting source of image
'''
import sys
import os

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.image import Image
from src.img.processor.processor import ImgProcessor
# sources
from src.img.source.dir import ImgSourceDir
from src.img.source.camera import Camera
from src.img.source.video import ImgSourceVideo

class ConfigurableImgSource(ImgProcessor):

    def __init__(
        self,
        path_to_images: str = None,
        path_to_video: str = None,
        range_of_camara_numbers: 'int|[int]|range' = None
    ):
        super().__init__(name=self.__class__.__name__)
        numer_of_none = 0
        params = [path_to_images, path_to_video, range_of_camara_numbers]
        for param in params:
            if param is None:
                numer_of_none += 1
        if len(params) - numer_of_none != 1:
            raise Exception(f'Exactly one parameter must be set for {self.__class__.__name__}.')
        if path_to_images is not None:
            self._source = ImgSourceDir(path=path_to_images)
        elif path_to_video is not None:
            self._source = ImgSourceVideo(path=path_to_video)
        elif range_of_camara_numbers is not None:
            if isinstance(range_of_camara_numbers, int):
                range_of_camara_numbers = [range_of_camara_numbers]
            self._source = Camera(range_of_camara_numbers=range_of_camara_numbers)
        else:
            raise Exception('Uknown img source')

    def process(self, img: Image = None) -> Image:
        '''
        Reimplements method from predcessor.
        Simple call selected source
        '''
        return self._source.process(img)





