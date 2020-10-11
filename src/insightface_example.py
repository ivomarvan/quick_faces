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
        #range_of_camara_numbers=range(0,10),
        path_to_images=os.path.join(PROJECT_ROOT, 'nogit_data/from_herman/in_img'),
        # path_to_video=os.path.join(PROJECT_ROOT, 'nogit_data/from_herman/in_video/IMG_8339.MOV')
    )

    # --- storages ---
    from src.img.storage.configurable import ConfigurableImgStorage
    # You can comment a parametr if you do not use a storage
    storage = ConfigurableImgStorage(
        path_to_images=os.path.join(PROJECT_ROOT, 'nogit_data/from_herman/out_img'),
        # path_to_video=os.path.join(PROJECT_ROOT, 'nogit_data/from_herman/out_video/video.mp4'),
        window_name='Debug Window',
        video_fps=2  # parameter only for video, Frames Per Second
    )

    # --- processors ---
    processors = []

    # ------ preprocessors ---
    from src.img.processor.reformat.squere_crop.processor import SquereCropImgProcessor
    processors += [
        SquereCropImgProcessor(crop_size=640)
    ]

    # ------ face detectors ---
    from src.img.processor.face_detector.insightface_face_detector import InsightfaceFaceDetector

    processors += [
        InsightfaceFaceDetector(model_name='retinaface_mnet025_v2', color=(0, 200, 50)),
    ]

    # ------ landmarks ----
    processors += [
    ]

    # ------ markers ---
    from src.img.processor.marker import ImgMarkerProcessor
    processors += [
        ImgMarkerProcessor()
    ]

    # --- image process loop --
    from src.img.processor.loop import ImgLoop
    loop = ImgLoop(
        img_source=source,
        img_processors=processors,
        img_storage=storage
    )

    # --- run ---
    loop.run(log_each_image=True, log_gobal_statistics=True)
