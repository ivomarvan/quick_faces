#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Images from directory.
'''
import sys
import os
import cv2

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.source.base import ImgSourceBase
from src.utils.common import fwalk
from src.img.container.image import Image
from src.img.processor.types import IntType, DirectoryType, BoolType


class ImgSourceDir(ImgSourceBase):
    """
    Source of images.
    All images from the directory.
    """
    def __init__(
        self,
        path: DirectoryType(descr='path for seacrhing of images', must_exists=True),
        recursively: BoolType(descr='search recursively?') = True,
        color_flag: IntType(descr='opencv2.imread parameter') = cv2.IMREAD_UNCHANGED
    ):
        super().__init__('dir.' + path)
        self._path = path
        self._len_path1 = len(path) + 1
        self._recursively = recursively
        self._color_flag = color_flag
        self._files = None

    def _get_file_id(self, path:str):
        return path[self._len_path1:]

    def _get_files(self):
        # lean inicialisation
        if self._files is None:
            self._files = ((self._get_file_id(f),f) for f in fwalk(top=self._path, predicates=[Image.acceptable_file], recursively=self._recursively))
        return self._files

    def get_next_image(self) -> Image:
        '''
        @see from src.img.source.base.ImgSourceBase#get_next_image
        '''
        try:
            id, path = next(self._get_files())
            img = Image.read_from_file(path=path, color_flag=self._color_flag, img_id = id)
            self.add_not_none_option('extension', Image.get_extension(path))
            return img
        except StopIteration:
            return None

