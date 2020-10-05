#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Define default dirs, ...  
'''

import sys
import os.path
import gzip

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..'))
sys.path.append(PROJECT_ROOT)

NOGIT_DATA = os.path.join(PROJECT_ROOT, 'nogit_data')

# === for training ====================================================================
DEFAULT_LANDMARK_DIR = os.path.join(NOGIT_DATA, 'ibug_300W_large_face_landmark_dataset')
DEFAULT_LANDMARK_FILES = {
    'test': os.path.join(DEFAULT_LANDMARK_DIR, 'labels_ibug_300W_test.xml'),
    'train_test': os.path.join(DEFAULT_LANDMARK_DIR, 'labels_ibug_300W_train.xml'),
}

def get_landmark_filename(type: str,  model_name: str, out_dir: str = DEFAULT_LANDMARK_DIR) -> str:
    return os.path.join(out_dir, f'labels_ibug_300W_{type}_{model_name}.xml')

# =====================================================================================
class ModelsSource:
    # models in lfs (Versioning large files, https://docs.github.com/en/free-pro-team@latest/github/managing-large-files/versioning-large-files)
    MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')
    # cache for unzziped models in no-git directory
    MODELS_CACHE_DIR = os.path.join(NOGIT_DATA, 'models_cache')

    @classmethod
    def get_file_name(cls, relative_path:str) -> str:
        cached_filename = os.path.join(cls.MODELS_CACHE_DIR, relative_path)
        if os.path.isfile(cached_filename):
            return cached_filename
        not_zipped_filename = os.path.join(cls.MODELS_DIR, relative_path)
        if os.path.isfile(not_zipped_filename):
            return not_zipped_filename
        gzipped_filename = os.path.join(cls.MODELS_DIR, relative_path + '.gz')
        if os.path.isfile(gzipped_filename):
            cls.ungzip(gzipped_filename, cached_filename)
            return cached_filename
        raise FileNotFoundError(relative_path)

    @classmethod
    def ungzip(cls, source_filepath: str, dest_filepath: str, block_size: int=65536):
        os.makedirs(os.path.dirname(dest_filepath), exist_ok=True)
        with gzip.open(source_filepath, 'rb') as s_file, open(dest_filepath, 'wb') as d_file:
            while True:
                block = s_file.read(block_size)
                if not block:
                    break
                else:
                    d_file.write(block)

    @classmethod
    def get_model_dlib_shape_predictor_filename(cls, model_filename: str) -> str:
        return cls.get_file_name(os.path.join('dlib_shape_predictor', model_filename))

    @classmethod
    def get_model_cv2_dnn_cafee_filename(cls) -> (str, str):
        '''
        Model from From https://github.com/vardanagarwal/Proctoring-AI/blob/master/face_detection/models/res10_300x300_ssd_iter_140000.caffemodel
        '''
        filename1 = os.path.join('cv2_dnn_cafee', 'res10_300x300_ssd_iter_140000.caffemodel')
        filename2 = os.path.join('cv2_dnn_cafee', 'deploy.prototxt.txt')
        return cls.get_file_name(filename1), cls.get_file_name(filename2)

