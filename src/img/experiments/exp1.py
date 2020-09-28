#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Place for testing code.
'''
import sys
import os
from copy import copy

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

if __name__ == "__main__":
    # for tests only
    # sources
    from src.img.source.dir import ImgSourceDir
    from src.img.source.camera import Camera

    # storages
    from src.img.storage.dir import ImgStorageDir
    from src.img.storage.window import ImgStorageWindow

    # preprocessors
    from src.img.processor.resizer import ImgResizeProcessor
    from src.img.processor.decolorizer import ImgDecolorizeProcessor
    from src.img.processor.list import ImgListProcessor

    # face
    from src.img.processor.face_detector.dlib_frontal_face_detector import DlibFaceDetectorImgProcessor
    from src.img.processor.face_detector.cv2_dnn_caffe import Cv2Dnn_CafeeFaceDetectorImgProcessor

    # landmarks
    from src.img.processor.landmarks_detector.dlib_shape_predictor import DlibLandmarksDetectorImgProcessor

    # markers
    from src.img.processor.marker import ImgMarkerProcessor

    # statistics
    from src.utils.timeit_stats import TimeStatistics

    read_from_camera = True
    store_to_file = not read_from_camera
    show_in_window = True
    log_each_image = True
    log_gobal_statistics = True
    
    if read_from_camera:
        source = Camera()
    else:
        source = ImgSourceDir(path='/home/ivo/workspace/x_my_actual/quick_faces/nogit_data/from_herman/img')

    if store_to_file:
        storage = ImgStorageDir(path='/home/ivo/workspace/x_my_actual/quick_faces/nogit_data/from_herman/img.copy')
    resizer = ImgResizeProcessor(width=400)
    decolorizer = ImgDecolorizeProcessor()
    preprocessor = ImgListProcessor(name='preprocessor', processors=[resizer, decolorizer])
    face_detector_Dlib = DlibFaceDetectorImgProcessor(color=(0, 200, 50))
    face_detector_Cv2Dnn_CafeeFace = Cv2Dnn_CafeeFaceDetectorImgProcessor(color=(255, 10, 10))

    left_face_landmarks_predictor = DlibLandmarksDetectorImgProcessor('left_face', color=(10,10,255))
    right_face_landmarks_predictor = DlibLandmarksDetectorImgProcessor('right_face' , color=(100,100,255))


    marker = ImgMarkerProcessor()
    window = ImgStorageWindow('Faces')

    # loop
    stop = False
    i = 0
    while not stop:
        try:
            img = source.process(None)

            if img is None:
                raise StopIteration()

            orig_img = copy(img) # it is funny, it create new img array, but log inforamtions are shared
            #img = preprocessor.process(img)

            img = face_detector_Dlib.process(img)
            img = face_detector_Cv2Dnn_CafeeFace.process(img)
            print(img)
            print('='*50)
            print(img.get_results().get_results_with_given_result_name('faces'))
            continue

            img = left_face_landmarks_predictor.process(img)

            marker.set_resize_factor(orig_img, img)
            orig_img = marker.process(orig_img)

            if store_to_file:
                orig_img = storage.process(orig_img)

            if show_in_window:
                orig_img = window.process(orig_img)

            # log
            if log_each_image:
                print(orig_img)
            else:
                if i % 80 == 0:
                    sys.stdout.write('\n')
                sys.stdout.write('.')
                sys.stdout.flush()
            i += 1
        except StopIteration:
            stop = True
    if log_gobal_statistics:
        TimeStatistics.print_as_tsv(print_header=True)