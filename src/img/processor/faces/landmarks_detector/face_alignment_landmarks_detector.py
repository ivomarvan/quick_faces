#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Landmarks detector from face_alignment library.
    @credit https://github.com/1adrianb/face-alignment
'''
import sys
import os
import numpy as np
import torch

from face_alignment.api import LandmarksType, NetworkSize, models_urls
from face_alignment.models import FAN, ResNetDepth
from face_alignment.utils import crop, flip, get_preds_fromhm, draw_gaussian
from torch.utils.model_zoo import load_url

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '../..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)
NOGIT_DATA = os.path.join(PROJECT_ROOT, 'nogit_data')


from src.img.container.geometry import landmarks_to_points
from src.img.container.image import Image
from src.img.processor.processor import ImgProcessor
from src.img.processor.faces.landmarks_detector.result import LandmarksDetectorResult, FaceLandmarsks
from src.img.processor.faces.face_detector.result import FaceDetectorResult

class FaceAlignmentLandmarksDetector(ImgProcessor):

    def __init__(
        self,
        landmarks_type: LandmarksType,
        network_size: int = NetworkSize.LARGE.value,
        device: str = 'cpu',
        flip_input: bool = False,
        color: tuple = (0, 0, 255)
    ):
        super().__init__(f'face_alignment.landmarks.{landmarks_type.name}')
        self._landmarks_type = landmarks_type
        self._flip_input = flip_input
        self._color = color
        self._device = device
        self.add_not_none_option('color', color)
        self.add_not_none_option('device', device)

        # @todo Consider not use constant value
        self._face_detector_reference_scale = 195
        # Initialise the face alignemnt networks
        self.face_alignment_net = FAN(network_size)
        if landmarks_type == LandmarksType._2D:
            network_name = '2DFAN-' + str(network_size)
        else:
            network_name = '3DFAN-' + str(network_size)

        fan_weights = load_url(models_urls[network_name], map_location=lambda storage, loc: storage)
        self.face_alignment_net.load_state_dict(fan_weights)

        self.face_alignment_net.to(device)
        self.face_alignment_net.eval()

        # Initialiase the depth prediciton network
        if landmarks_type == LandmarksType._3D:
            self.depth_prediciton_net = ResNetDepth()

            depth_weights = load_url(models_urls['depth'], map_location=lambda storage, loc: storage)
            depth_dict = {
                k.replace('module.', ''): v for k, v in depth_weights['state_dict'].items()
            }
            self.depth_prediciton_net.load_state_dict(depth_dict)

            self.depth_prediciton_net.to(device)
            self.depth_prediciton_net.eval()

    def _run(self, image: np.ndarray, face_boxess) -> list:
        landmarks = []
        for i, d in enumerate(face_boxess):
            center = torch.FloatTensor(
                [d[2] - (d[2] - d[0]) / 2.0, d[3] - (d[3] - d[1]) / 2.0])
            center[1] = center[1] - (d[3] - d[1]) * 0.12
            scale = (d[2] - d[0] + d[3] - d[1]) / self._face_detector_reference_scale

            try:
                inp = crop(image, center, scale)
                inp = torch.from_numpy(inp.transpose(
                    (2, 0, 1))).float()

                inp = inp.to(self._device)
                inp.div_(255.0).unsqueeze_(0)

                out = self.face_alignment_net(inp)[-1].detach()
                if self._flip_input:
                    out += flip(self.face_alignment_net(flip(inp))
                                [-1].detach(), is_label=True)
                out = out.cpu()

                pts, pts_img = get_preds_fromhm(out, center, scale)
                pts, pts_img = pts.view(68, 2) * 4, pts_img.view(68, 2)

                if self._landmarks_type == LandmarksType._3D:
                    heatmaps = np.zeros((68, 256, 256), dtype=np.float32)
                    for i in range(68):
                        if pts[i, 0] > 0:
                            heatmaps[i] = draw_gaussian(
                                heatmaps[i], pts[i], 2)
                    heatmaps = torch.from_numpy(
                        heatmaps).unsqueeze_(0)

                    heatmaps = heatmaps.to(self._device)
                    depth_pred = self.depth_prediciton_net(
                        torch.cat((inp, heatmaps), 1)).data.cpu().view(68, 1)
                    pts_img = torch.cat(
                        (pts_img, depth_pred * (1.0 / (256.0 / (200.0 * scale)))), 1)

                landmarks.append(pts_img.numpy())
            except Exception:
                continue
        return landmarks


    def _process_image(self, img: Image = None) -> (Image, LandmarksDetectorResult):
        # all faces, potentially from different face detectors
        faces_results = img.get_results().get_results_for_processor_super_class(FaceDetectorResult)
        face_landmark_couples = []
        for face_result in faces_results:
            faces = face_result.get_rectangles()  # [Rectangle]
            for face_index, face_rectangle in enumerate(faces):
                landmarks__from_detector = self._run(img.get_work_img_array(), np.array([face_rectangle.as_bbox()]))
                if not landmarks__from_detector:
                    continue
                landmarks_points = landmarks_to_points(landmarks__from_detector)
                face_landmark_couples.append(
                    FaceLandmarsks(face_result=face_result, landmarks=landmarks_points, face_index=face_index))
        return img, LandmarksDetectorResult(self, face_landmark_couples=face_landmark_couples)

