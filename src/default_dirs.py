#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Define default dirs, ...  
'''

import sys
import os.path

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..'))
sys.path.append(PROJECT_ROOT)

NOGIT_DATA = os.path.join(PROJECT_ROOT, 'nogit_data')
DEFAULT_LANDMARK_DIR = os.path.join(NOGIT_DATA, 'ibug_300W_large_face_landmark_dataset')
DEFAULT_LANDMARK_FILES = {
    'test': os.path.join(DEFAULT_LANDMARK_DIR, 'labels_ibug_300W_test.xml'),
    'train_test': os.path.join(DEFAULT_LANDMARK_DIR, 'labels_ibug_300W_train.xml'),
}

DEFAULT_MODEL_DIR = os.path.join(NOGIT_DATA, 'models')

def get_landmark_filename(type: str,  model_name: str, out_dir: str = DEFAULT_LANDMARK_DIR) -> str:
    return os.path.join(out_dir, f'labels_ibug_300W_{type}_{model_name}.xml')

def get_model_filename(model_name: str) -> str:
    return os.path.join(DEFAULT_MODEL_DIR, f'predictor_model_{model_name}.dat')