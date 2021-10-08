#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Tests Media Play library.
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
        path_to_images=os.path.join(PROJECT_ROOT, 'nogit_data/media_pipe'),
        # path_to_video=os.path.join(PROJECT_ROOT, 'nogit_data/from_herman/out_video/video.mp4'),
        window_name='Media Pipe',
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
    from src.img.processor.media_pipe.faces import FaceMeshSolution
    from src.img.processor.media_pipe.hands import HandsSolution
    from src.img.processor.media_pipe.pose import PoseSolutions
    from src.img.processor.media_pipe.holistic import HolisticSolutions
    from src.img.processor.media_pipe.selfie_segmentation import SelfieSegmentationSolution

    from src.img.processor.media_pipe.media_pipe_processor import MediaPipeProcessor, MediaPipeMarker

    face_solution = FaceMeshSolution()
    hands_solution = HandsSolution()

    processors += [
        MediaPipeProcessor(face_solution),
        MediaPipeProcessor(hands_solution)
    ]


    # ------ markers ---
    processors += [
        MediaPipeMarker(face_solution),
        MediaPipeMarker(hands_solution)
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
