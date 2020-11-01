#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Images from video.
'''
import sys
import os
import cv2
import numpy as np

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '../..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.processor.source.base import ImgSourceBase
from src.img.container.image import Image
from src.img.processor.types import VideoFileType

class ImgSourceVideo(ImgSourceBase):
    """
    Images are frames from a video file.
    """

    def __init__(
        self,
        path: VideoFileType('The  path  to file with video', must_exists=True)
    ):
        super().__init__('video.' + path)
        self._capture = cv2.VideoCapture(path)
        self.add_not_none_option('video file', path)

    def _get_img(self) -> (np.ndarray, int):
        ret, img = self._capture.read()
        # Int id of image. In the case of camera it can be "Current position of the video file in microseconds".
        img_microseconds = int(1000 * self._capture.get(cv2.CAP_PROP_POS_MSEC))
        return img, img_microseconds

    def get_next_image(self) -> Image:
        '''
        @see from src.img.source.base.ImgSourceBase#get_next_image
        '''
        img, img_microseconds = self._get_img()
        return Image(array=img, id=img_microseconds)




