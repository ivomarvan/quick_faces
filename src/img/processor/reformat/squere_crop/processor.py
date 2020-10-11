#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Img processor for squere crop
'''
import sys
import os
import cv2
import numpy as np


# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '../../..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.image import Image
from src.img.processor.processor import ImgProcessor
from src.img.container.result import ImageProcessorResult
from src.img.processor.reformat.squere_crop.result import SquereCropResult

class SquereCropImgProcessor(ImgProcessor):

    def __init__(self, crop_size: int = 640):
        super().__init__('squre_crop')
        self._crop_size = crop_size
        self.add_not_none_option('crop_size', crop_size)

    def _square_crop(self, img: np.ndarray) -> (np.ndarray, float):
        if img.shape[0] > img.shape[1]:
            height = self._crop_size
            width = int(float(img.shape[1]) / img.shape[0] * self._crop_size)
            scale = float(self._crop_size) / img.shape[0]
        else:
            width = self._crop_size
            height = int(float(img.shape[0]) / img.shape[1] * self._crop_size)
            scale = float(self._crop_size) / img.shape[1]
        resized_im = cv2.resize(img, (width, height))
        det_im = np.zeros((self._crop_size, self._crop_size, 3), dtype=np.uint8)
        det_im[:resized_im.shape[0], :resized_im.shape[1], :] = resized_im
        return det_im, scale

    def _process_body(self, img: Image = None) -> Image:
        new_work_array, img_scale = self._square_crop(img.get_work_img_array())
        img.set_orig_img_array(new_work_array)
        return img, SquereCropResult(processor=self, img_scale=img_scale)