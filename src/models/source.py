#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Source fo models (data fo processors, neural nets, ....). 
    Files are in some place on the internet and are stored localy outside git directory.
    File is loaded if it is needt only.
'''

import sys
import os.path
import gzip
import json
import requests
import re
import html
import user_agent

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..'))
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
    MODELS_DIR = os.path.join(PROJECT_ROOT, '')
    MODELS_JSON_DIR = os.path.join(PROJECT_ROOT, 'models.json')
    # cache for unzziped models in no-git directory
    MODELS_CACHE_DIR = os.path.join(NOGIT_DATA, 'models_cache')

    HEADERS = {
        'User-Agent': user_agent.generate_user_agent()
    }


    @classmethod
    def get_file_name(cls, relative_json_path:str) -> str:
        json_filename = os.path.join(cls.MODELS_JSON_DIR, relative_json_path + '.json')
        with open(json_filename, 'r') as f:
            json_dict = json.load(f)
        cached_path = os.path.join(cls.MODELS_CACHE_DIR, json_dict['path'])
        os.makedirs(cached_path, exist_ok=True)
        cache_gzipped_filename = os.path.join(cached_path, json_dict['filename'])
        gz = False
        if cache_gzipped_filename.endswith('.gz'):
            gz = True
            cache_ungzipped_filename = cache_gzipped_filename[:-3]
        else:
            cache_ungzipped_filename = cache_gzipped_filename
        if os.path.isfile(cache_ungzipped_filename):
            # file exists in cache alredy
            return cache_ungzipped_filename
        # download file
        cls.download_binary(
            url_descr=json_dict['url'],
            out_filename=cache_gzipped_filename,
            cache_ungzipped_filename=cache_ungzipped_filename
        )
        if gz:
            cls.ungzip(cache_gzipped_filename, cache_ungzipped_filename)
            os.remove(cache_gzipped_filename)
        return cache_ungzipped_filename


    @classmethod
    def download_binary(cls, url_descr, out_filename: str, cache_ungzipped_filename: str):
        with open(out_filename, 'wb') as fd:
            if isinstance(url_descr, str):
                urls = [url_descr]
            elif isinstance(url_descr, dict):
                urls = [os.path.join(url_descr['dir_url'], chunk) for chunk in url_descr['chunks']]
            else:
                raise Exception(f'Unsuported type of url ({type}) in {cache_ungzipped_filename}')
            for url in urls:
                r = requests.get(url, headers=cls.HEADERS)
                print(f'downloading {url} -> {out_filename}')
                for chunk in r.iter_content(chunk_size=128):
                    fd.write(chunk)

    @classmethod
    def ungzip(cls, source_filepath: str, dest_filepath: str, block_size: int=65536):
        print(f'unziping {source_filepath} -> {dest_filepath}')
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

