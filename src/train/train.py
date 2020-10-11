#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Selet landmarks for given landmaarks set. Read xml file, where imagges are tagged. Write it to new xml file.
    
    @credit https://www.pyimagesearch.com/2019/12/16/training-a-custom-dlib-shape-predictor/   
'''

import sys
import os.path
import multiprocessing
import dlib

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.train_test.landmarks.sets import LANDMARKS_MODELS
from src.models.source import get_model_dlib_shape_predictor_filename, get_landmark_filename

DEFAULT_SHAPE_PREDICTOR_OPTIONS = dlib.shape_predictor_training_options()

# define the depth of each regression tree -- there will be a total
# of 2^tree_depth leaves in each tree; small values of tree_depth
# will be *faster* but *less accurate* while larger values will
# generate trees that are *deeper*, *more accurate*, but will run
# *far slower* when making predictions
DEFAULT_SHAPE_PREDICTOR_OPTIONS.tree_depth = 4

# regularization parameter in the range [0, 1] that is used to help
# our model generalize -- values closer to 1 will make our model fit
# the training data better, but could cause overfitting; values closer
# to 0 will help our model generalize but will require us to have
# training data in the order of 1000s of data points
DEFAULT_SHAPE_PREDICTOR_OPTIONS.nu = 0.1

# the number of cascades used to train_test the shape predictor -- this
# parameter has a *dramtic* impact on both the *accuracy* and *output
# size* of your model; the more cascades you have, the more accurate
# your model can potentially be, but also the *larger* the output size
DEFAULT_SHAPE_PREDICTOR_OPTIONS.cascade_depth = 15

# number of pixels used to generate features for the random trees at
# each cascade -- larger pixel values will make your shape predictor
# more accurate, but slower; use large values if speed is not a
# problem, otherwise smaller values for resource constrained/embedded
# devices
DEFAULT_SHAPE_PREDICTOR_OPTIONS.feature_pool_size = 400

# selects best features at each cascade when training -- the larger
# this value is, the *longer* it will take to train_test but (potentially)
# the more *accurate* your model will be
DEFAULT_SHAPE_PREDICTOR_OPTIONS.num_test_splits = 50

# controls amount of "jitter" (i.e., data augmentation) when training
# the shape predictor -- applies the supplied number of random
# deformations, thereby performing regularization and increasing the
# ability of our model to generalize
DEFAULT_SHAPE_PREDICTOR_OPTIONS.oversampling_amount = 5

# amount of translation jitter to apply -- the dlib docs recommend
# values in the range [0, 0.5]
DEFAULT_SHAPE_PREDICTOR_OPTIONS.oversampling_translation_jitter = 0.1

# tell the dlib shape predictor to be verbose and print out status
# messages our model trains
DEFAULT_SHAPE_PREDICTOR_OPTIONS.be_verbose = True

# number of threads/CPU cores to be used when training -- we default
# this value to the number of available cores on the system, but you
# can supply an integer value here if you would like
DEFAULT_SHAPE_PREDICTOR_OPTIONS.num_threads = multiprocessing.cpu_count() - 1

class TrainProcess:

    def __init__(self, options: dlib.shape_predictor_training_options = DEFAULT_SHAPE_PREDICTOR_OPTIONS):
        self._options = options

    def run(self, model_name):
        model_filename = get_model_dlib_shape_predictor_filename(model_name)
        landmark_filename = get_landmark_filename(type='train', model_name=model_name)
        os.makedirs(os.path.dirname(model_filename), exist_ok=True)
        
        # log our training options to the terminal
        print(f'''
            landmark_filename={landmark_filename}, 
            predictor_output_filename={model_filename}, 
            options={self._options}'''
        )

        # train_test the shape predictor
        dlib.train_shape_predictor(
            dataset_filename=landmark_filename,
            predictor_output_filename=model_filename,
            options=self._options
        )

if __name__ == "__main__":

    print(os.path.basename(os.path.abspath(__file__)))
    train_process = TrainProcess()
    for model_name, landmarks_set in LANDMARKS_MODELS.items():
        train_process.run(model_name=model_name)

