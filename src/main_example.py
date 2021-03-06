#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Place for testing code.
'''
import sys
import os


# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, 'img', '..', '..'))
sys.path.append(PROJECT_ROOT)

if __name__ == "__main__":
    # --- sources ---
    from src.img.source.configurable import ConfigurableImgSource
    # Only one parametr can be set
    source = ConfigurableImgSource(
        range_of_camara_numbers=range(0,10),
        # path_to_images=os.path.join(PROJECT_ROOT, 'nogit_data/ivo_in'),  # 'nogit_data/from_herman/in_img'
        # path_to_video=os.path.join(PROJECT_ROOT, 'nogit_data/from_herman/in_video/IMG_8339.MOV')
    )

    # --- storages ---
    from src.img.storage.configurable import ConfigurableImgStorage
    # You can comment a parametr if you do not use a storage
    storage = ConfigurableImgStorage(
        # path_to_images=os.path.join(PROJECT_ROOT, 'nogit_data/from_herman/out_img'),
        # path_to_video=os.path.join(PROJECT_ROOT, 'nogit_data/from_herman/out_video/video.mp4'),
        window_name='Debug Window',
        video_fps=25  # parameter only for video, Frames Per Second
    )

    # --- processors ---
    processors = []

    # ------ preprocessors ---
    processors += [
        # ImgResizeProcessor(width=200),
        # ImgDecolorizeProcessor()
    ]

    device = 'cpu' # cuda / cpu

    # ------ face detectors ---
    from src.img.processor.face_detector.face_aligment import FaceAlignmentFaceDetector, FaceAlignmentFaceDetectorType
    from src.img.processor.face_detector.insightface_face_detector import InsightfaceFaceDetector
    processors += [
        FaceAlignmentFaceDetector(color=(0, 0, 255), detector_type=FaceAlignmentFaceDetectorType.blazeface, device=device, find_best=True),
        #InsightfaceFaceDetector(model_name='retinaface_mnet025_v2', color=(0, 200, 50)),
        # DlibFaceDetectorImgProcessor(color=(0, 200, 50)),
        # Cv2DnnCafeeFaceDetector(color=(255, 10, 10))
    ]

    # ------ landmarks ----
    #from src.img.processor.landmarks_detector.face_alignment_landmarks_detector import FaceAlignmentLandmarksDetector
    #from face_alignment.api import LandmarksType
    from src.img.processor.landmarks_detector.insightface_landmarks_detector import \
        InsightfaceLandmarksDetectorImgProcessor

    processors += [
        # DlibLandmarksDetectorImgProcessor('predictor_model_left_face.dat', color=(10,10,255)),
        #DlibLandmarksDetectorImgProcessor('predictor_model_left_face.precision.dat', color=(10, 10, 255)),
        #DlibLandmarksDetectorImgProcessor('predictor_model_right_face.dat', color=(255, 100, 100)),
        # DlibLandmarksDetectorImgProcessor('shape_predictor_68_face_landmarks.dat', color=(200, 200, 200)),
        # FaceAlignmentLandmarksDetector(landmarks_type=LandmarksType._2D, device=device, color=(0, 255, 0)),
        InsightfaceLandmarksDetectorImgProcessor(color=(255,255,255))
    ]

    # ------ evaluation ---
    from src.img.processor.evaluation.is_open import IsOpenImgProcessor, \
        InsightfaceMouthIsOpenManager, InsightfaceLeftEyeIsOpenManager, InsightfaceRightEyeIsOpenManager
    threshold_percents=25
    processors += [
        IsOpenImgProcessor(is_open_manager=InsightfaceMouthIsOpenManager(calibration_mode=True)),
        IsOpenImgProcessor(is_open_manager=InsightfaceLeftEyeIsOpenManager(calibration_mode=True, threshold_percents=threshold_percents)),
        IsOpenImgProcessor(is_open_manager=InsightfaceRightEyeIsOpenManager(calibration_mode=True, threshold_percents=threshold_percents)),
    ]

    # ------ markers ---
    from src.img.processor.marker.marker import ImgMarkerProcessor
    from src.img.processor.marker.add_landmarks_numbers import LandmarkNumbersImgProcessor
    from src.img.processor.marker.is_open_marker import IsOpenMarkerImgProcessor
    processors += [
        ImgMarkerProcessor(),
        # LandmarkNumbersImgProcessor(),
        IsOpenMarkerImgProcessor()
    ]

    # --- image process loop --
    from src.img.processor.loop import ImgLoop
    loop = ImgLoop(
        img_source=source,
        img_processors=processors,
        img_storage=storage
    )

    # --- run ---
    loop.run(log_each_image=False, log_gobal_statistics=True)
