#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Storage for images to video file.
    (Implements ImgProcessor, ImgStorageBase interfaces.)
'''

import sys
import os
import cv2
import numpy as np

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.storage.base import ImgStorageBase
from src.img.container.image import Image
from moviepy.editor import VideoFileClip, concatenate_videoclips
from src.img.processor.types import FileType, StrType, IntType


class ImgStorageVideo(ImgStorageBase):
    """Store result of image processing to video file"""

    max_images_in_one_part_descr = '''
    Maximal count of images in one video.
    (Because storege know nothing about source [sizes of individual images] 
    it store it in memory and calculate size of video-frame from it.
    And memory is limited.)
    When the limit is reached, the results are saved in a new video file. 
    '''

    def __init__(
            self,
            path: FileType(descr='Path to new file. (Directory will be create authomaticaly if it does not exist.)'),
            codec: StrType(
                descr='Video codec. Change if you know what you are duing. See https://www.fourcc.org/codecs.php fo codecs.') = 'mp4v',
            fps: IntType(descr='Count of frames per second (1-very slow, 25-normal, ....)') = 30,
            max_images_in_one_part: IntType(descr=max_images_in_one_part_descr) = 60 * 30
    ):
        super().__init__('dir.' + path)
        self.add_not_none_option('out', path)
        self.add_not_none_option('fps', fps)
        self._path = path
        self._codec = codec
        self._fps = fps
        self._images = []  # [Image]
        self._path = path
        self._max_images_in_one_part = max_images_in_one_part
        self._video_parts = []
        self._fourcc = cv2.VideoWriter_fourcc(*self._codec)

    def __del__(self):
        '''
        Store all temporally stored images images
        '''
        if self._images:
            self._store_one_part()
        return
        videos = [VideoFileClip(path) for path in self._video_parts]
        final_clip = concatenate_videoclips(videos)
        final_clip.write_videofile(self._path)
        for path in self._video_parts:
            os.remove(path)

    def _get_tmp_filename(self):
        name_parts = self._path.split('.')
        new_patrs = name_parts[:-1] + [f'{len(self._video_parts):03}'] + [name_parts[-1]]
        return '.'.join(new_patrs)

    def _store_one_part(self):
        tmp_wideo_path = self._get_tmp_filename()
        # find width and height for output
        widths = []
        heights = []
        for img in self._images:
            widths.append(img.get_width())
            heights.append(img.get_height())
        max_width = max(widths)
        max_height = max(heights)
        os.makedirs(os.path.dirname(tmp_wideo_path), exist_ok=True)
        out = cv2.VideoWriter(tmp_wideo_path, self._fourcc, self._fps, (max_width, max_height))
        for img in self._images:
            w, h = img.get_width(), img.get_height()
            if w != max_width or h != max_height:
                # put small image to big one (with maximal size in dataset)
                big_image = np.zeros((max_height, max_width, 3), np.uint8)
                big_image[0:h, 0:w, :] = img.get_orig_img_array()
                out.write(big_image)
            else:
                out.write(img.get_orig_img_array())
        out.release()
        # clean
        self._images = []
        self._video_parts.append(tmp_wideo_path)

    def store(self, img: Image) -> Image:
        '''
        @see src.img.storage.base.ImgStorageBase.store
        '''
        self._images.append(img)
        if len(self._images) >= self._max_images_in_one_part:
            self._store_one_part()
        return img
