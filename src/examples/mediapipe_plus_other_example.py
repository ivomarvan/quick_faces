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
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..'))
sys.path.append(PROJECT_ROOT)

if __name__ == "__main__":
    # --- sources ---
    # Only one parametr can be set
    from src.img.processor.source.camera import Camera
    from src.img.processor.source.video import ImgSourceVideo
    from src.img.processor.source.dir import ImgSourceDir

    # Only one parametr can be set
    source = Camera(range_of_camera_ids=range(0,10))
    #source = ImgSourceDir(path=os.path.join(PROJECT_ROOT, 'nogit_data/from_herman/in_img'))
    #source = ImgSourceVideo(path=os.path.join(PROJECT_ROOT, 'nogit_data/from_herman/in_video/IMG_8339.MOV'))

    # --- storages ---
    from src.img.processor.storage.configurable import ConfigurableImgStorage
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
    from src.img.processor.faces.face_detector.face_aligment import FaceAlignmentFaceDetector, \
        FaceAlignmentFaceDetectorType

    processors += [
        FaceAlignmentFaceDetector(color=(0, 0, 255), detector_type=FaceAlignmentFaceDetectorType.blazeface,
                                  device=device, find_best=True),
        # InsightfaceFaceDetector(model_name='retinaface_mnet025_v2', color=(0, 200, 50)),
        # DlibFaceDetectorImgProcessor(color=(0, 200, 50)),
        # Cv2DnnCafeeFaceDetector(color=(255, 10, 10))
    ]

    # ------ landmarks ----
    from src.img.processor.faces.landmarks_detector.insightface_landmarks_detector import \
        InsightfaceLandmarksDetectorImgProcessor
    from src.img.processor.faces.landmarks_detector.mediapipe_landmarks_detector import MediapipeLandmarksDetectorImgProcessor

    processors += [
        InsightfaceLandmarksDetectorImgProcessor(color=(0, 255, 255)),
        MediapipeLandmarksDetectorImgProcessor(quick_faces_color=(255,0,0))  # quick_faces_color=(255,0,0)
    ]

    # ------ evaluation ---

    # ------ markers ---
    from src.img.processor.faces.marker.marker import ImgMarkerProcessor
    from src.img.processor.faces.marker.is_open_marker import IsOpenMarkerImgProcessor

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
