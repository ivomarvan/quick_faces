#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Face detector from face_alignment library.
    @credit https://github.com/1adrianb/face-alignment
'''
import sys
import os
import numpy as np
from skimage import color
from enum import Enum, auto

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '../..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.container.image import Image
from src.img.processor.faces.face_detector.face_detector import FaceDetector
from src.img.processor.faces.face_detector.result import FaceDetectorResult
from src.img.container.geometry import Rectangle
from face_alignment.detection.core import FaceDetector as FaceAlignmentFaceDetector

class FaceAlignmentFaceDetectorType(Enum):
    sfd = auto()
    dlib = auto()
    blazeface = auto()
    folder = auto()

class FaceAlignmentFaceDetectorFactory:
    @classmethod
    def get_detector(
        cls,
        detector_type: FaceAlignmentFaceDetectorType = FaceAlignmentFaceDetectorType.sfd,
        device: str = 'cpu',
        verbose: bool = False
    ) -> FaceAlignmentFaceDetector:
        if detector_type == FaceAlignmentFaceDetectorType.sfd:
            from face_alignment.detection.sfd import FaceDetector
        elif detector_type == FaceAlignmentFaceDetectorType.dlib:
            from face_alignment.detection.dlib import FaceDetector
        elif detector_type == FaceAlignmentFaceDetectorType.blazeface:
            from face_alignment.detection.blazeface import FaceDetector
        elif detector_type == FaceAlignmentFaceDetectorType.folder:
            from face_alignment.detection.folder import FaceDetector
        else:
            raise Exception(f'Uknown type of face detector: {detector_type}.')
        return FaceDetector(device=device, verbose=verbose)


class FaceAlignmentFaceDetector(FaceDetector):

    def __init__(
        self,
        detector_type: FaceAlignmentFaceDetectorType = FaceAlignmentFaceDetectorType.sfd,
        find_best: bool = False,
        color: tuple = (45, 127, 200),
        device: str = 'cpu',
        verbose: bool = False
    ):        
        super().__init__(name='face_alignment.face_detector.' + detector_type.name, find_best=find_best, color=color)
        self._get_all = not find_best
        # Get the face detector
        self._face_detector = FaceAlignmentFaceDetectorFactory.get_detector(detector_type=detector_type, device=device, verbose=verbose)
        self.add_not_none_option('type',  detector_type.name)

    def _process_image(self, img: Image = None) -> (Image, FaceDetectorResult):
        img_array = img.get_work_img_array()
        if img_array.ndim == 2:
            img_array = color.gray2rgb(img_array.copy())
        elif img_array.ndim == 4:
            img_array = img_array.copy()[..., :3]
        bboxes = self._face_detector.detect_from_image(img_array[..., ::-1])
        if (not self._get_all) and (bboxes.shape[0] != 0):
            # select one with max trust
            bboxes = [bboxes[np.argmax(np.array(bboxes)[:,4])]]
        faces_rectangles = [Rectangle.from_bbox(bbox) for bbox in bboxes]

        #print(f'{faces_rectangles}')
        return img, FaceDetectorResult(self, rectangles=faces_rectangles)

