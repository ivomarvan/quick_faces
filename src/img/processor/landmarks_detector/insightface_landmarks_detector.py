#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    InsightfaceFace lendmarks detector (predictor in some terminology) as img processor.
    @credit https://github.com/deepinsight/insightface/tree/master/alignment/coordinateReg
'''
import sys
import os
import numpy as np
import cv2
import mxnet as mx
from skimage import transform as trans

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)
NOGIT_DATA = os.path.join(PROJECT_ROOT, 'nogit_data')

from src.img.container.geometry import Point, Rectangle
from src.img.container.image import Image
from src.img.processor.processor import ImgProcessor
from src.default_dirs import ModelsSource
from src.img.processor.landmarks_detector.result import LandmarksDetectorResult, FaceLandmarsks
from src.img.processor.face_detector.result import FaceDetectorResult

class InsightfaceLandmarksDetectorImgProcessor(ImgProcessor):

    def __init__(
        self,
        # @todo It is hack when online storage is not implemented yet
        # see https://github.com/deepinsight/insightface/tree/master/alignment/coordinateReg for downloading the model
        model_prefix:str = os.path.join(NOGIT_DATA, 'models_cache', '2d106det', '2d106det'),
        epoch: int = 0,
        im_size: int = 192,
        ctx_id: int = -1,
        color: tuple = (0, 0, 255)
    ):
        super().__init__(f'insightface.landmarks_predictor({model_prefix})')
        self._color = color
        self.add_not_none_option('im_size', im_size)
        self.add_not_none_option('color', color)

        if ctx_id >= 0:
            ctx = mx.gpu(ctx_id)
        else:
            ctx = mx.cpu()
        self._image_size = (im_size, im_size)
        sym, arg_params, aux_params = mx.model.load_checkpoint(model_prefix, epoch)
        all_layers = sym.get_internals()
        sym = all_layers['fc1_output']
        self._model = mx.mod.Module(symbol=sym, context=ctx, label_names=None)
        self._model.bind(for_training=False, data_shapes=[('data', (1, 3, self._image_size[0], self._image_size[1]))])
        self._model.set_params(arg_params, aux_params)

    def transform(self, data, center, output_size, scale, rotation):
        scale_ratio = scale
        rot = float(rotation) * np.pi / 180.0
        # translation = (output_size/2-center[0]*scale_ratio, output_size/2-center[1]*scale_ratio)
        t1 = trans.SimilarityTransform(scale=scale_ratio)
        cx = center[0] * scale_ratio
        cy = center[1] * scale_ratio
        t2 = trans.SimilarityTransform(translation=(-1 * cx, -1 * cy))
        t3 = trans.SimilarityTransform(rotation=rot)
        t4 = trans.SimilarityTransform(translation=(output_size / 2, output_size / 2))
        t = t1 + t2 + t3 + t4
        M = t.params[0:2]
        cropped = cv2.warpAffine(data, M, (output_size, output_size), borderValue=0.0)
        return cropped, M

    #----
    def trans_points2d(self, pts, M):
        new_pts = np.zeros(shape=pts.shape, dtype=np.float32)
        for i in range(pts.shape[0]):
            pt = pts[i]
            new_pt = np.array([pt[0], pt[1], 1.], dtype=np.float32)
            new_pt = np.dot(M, new_pt)
            # print('new_pt', new_pt.shape, new_pt)
            new_pts[i] = new_pt[0:2]

        return new_pts

    def trans_points3d(self, pts, M):
        scale = np.sqrt(M[0][0] * M[0][0] + M[0][1] * M[0][1])
        # print(scale)
        new_pts = np.zeros(shape=pts.shape, dtype=np.float32)
        for i in range(pts.shape[0]):
            pt = pts[i]
            new_pt = np.array([pt[0], pt[1], 1.], dtype=np.float32)
            new_pt = np.dot(M, new_pt)
            # print('new_pt', new_pt.shape, new_pt)
            new_pts[i][0:2] = new_pt[0:2]
            new_pts[i][2] = pts[i][2] * scale

        return new_pts

    def trans_points(self,pts, M):
        if pts.shape[1] == 2:
            return self.trans_points2d(pts, M)
        else:
            return self.trans_points3d(pts, M)

    def _run(self, im: np.ndarray, face_boxess) -> list:
        out = []
        for i in range(face_boxess.shape[0]):
            bbox = face_boxess[i]
            input_blob = np.zeros((1, 3) + self._image_size, dtype=np.float32)
            w, h = (bbox[2] - bbox[0]), (bbox[3] - bbox[1])
            center = (bbox[2] + bbox[0]) / 2, (bbox[3] + bbox[1]) / 2
            rotate = 0
            _scale = self._image_size[0] * 2 / 3.0 / max(w, h)
            rimg, M = self.transform(im, center, self._image_size[0], _scale, rotate)
            rimg = cv2.cvtColor(rimg, cv2.COLOR_BGR2RGB)
            rimg = np.transpose(rimg, (2, 0, 1))  # 3*112*112, RGB
            input_blob[0] = rimg
            data = mx.nd.array(input_blob)
            db = mx.io.DataBatch(data=(data,))
            self._model.forward(db, is_train=False)
            pred = self._model.get_outputs()[-1].asnumpy()[0]
            if pred.shape[0] >= 3000:
                pred = pred.reshape((-1, 3))
            else:
                pred = pred.reshape((-1, 2))
            pred[:, 0:2] += 1
            pred[:, 0:2] *= (self._image_size[0] // 2)
            if pred.shape[1] == 3:
                pred[:, 2] *= (self._image_size[0] // 2)

            IM = cv2.invertAffineTransform(M)
            pred = self.trans_points(pred, IM)
            out.append(pred)
        if out:
            out = np.round(out).astype(np.int)
        return out

    def _rescangles_to_bbboxes(self, rectangles:[Rectangle]):
        ret_list =[rect.as_bbox() for rect in rectangles]
        return np.ndarray(ret_list)

    def _landmarks_to_points(self, insightface_landmarks: np.ndarray)-> [Point]:
        in_list = list(insightface_landmarks[0])
        return [Point(x=p[0], y=p[1]) for p in in_list]

    def _process_body(self, img: Image = None) -> (Image, LandmarksDetectorResult):
        # all faces, potentially from different face detectors
        faces_results = img.get_results().get_results_for_processor_super_class(FaceDetectorResult)
        face_landmark_couples = []
        for face_result in faces_results:
            faces = face_result.get_rectangles()  # [Rectangle]
            for face_index, face_rectangle in enumerate(faces):
                landmarks__from_detector = self._run(img.get_work_img_array(), np.array([face_rectangle.as_bbox()]))
                landmarks_points = self._landmarks_to_points(landmarks__from_detector)
                face_landmark_couples.append(
                    FaceLandmarsks(face_result=face_result, landmarks=landmarks_points, face_index=face_index))
        return img, LandmarksDetectorResult(self, face_landmark_couples=face_landmark_couples)
