#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Shortcut for selecting storage for image
'''
import sys
import os

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '../..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.image import Image


# sources
from src.img.processor.storage.dir import ImgStorageDir
from src.img.processor.storage.video import ImgStorageVideo
from src.img.processor.storage.window import ImgStorageWindow

class ConfigurableImgStorage:

    def __init__(
        self,
        path_to_images: str = None,
        path_to_video: str = None,
        window_name: str = None,
        video_codec:str = 'mp4v',
        video_fps: int = 30
    ):
        self._storages = []
        self._video = None
        if path_to_images is not None:
            self._storages.append(ImgStorageDir(path=path_to_images))
        if path_to_video is not None:
            # It is important store ImgStorageVideo object, for callin its __del__() method
            self._video = ImgStorageVideo(path=path_to_video, codec=video_codec, fps=video_fps)
            self._storages.append(self._video)
        if window_name is not None:
            self._storages.append(ImgStorageWindow(name=window_name))
        if len(self._storages) <= 0:
            raise Warning('No storage was selected.')

    def process(self, img: Image = None) -> Image:
        '''
        Reimplements method from predcessor.
        Simple call selected source
        '''
        for storage in self._storages:
            img = storage.process(img)
        return img




