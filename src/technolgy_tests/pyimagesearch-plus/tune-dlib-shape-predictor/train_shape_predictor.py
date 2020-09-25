# USAGE
# python train_shape_predictor.py --training ibug_300W_large_face_landmark_dataset/labels_ibug_300W_train_eyes.xml --model optimal_eye_predictor.dat

# import the necessary packages
import multiprocessing
import argparse
import dlib

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--training", required=True,
	help="path to input training XML file")
ap.add_argument("-m", "--model", required=True,
	help="path serialized dlib shape predictor model")
args = vars(ap.parse_args())

# grab the default options for dlib's shape predictor
print("[INFO] setting shape predictor options...")
options = dlib.shape_predictor_training_options()

# update our hyperparameters
options.tree_depth = 2
options.nu = 0.25
options.cascade_depth = 12
options.feature_pool_size = 500
options.num_test_splits = 20
options.oversampling_amount = 20
options.oversampling_translation_jitter = 0

# tell the dlib shape predictor to be verbose and print out status
# messages our model trains
options.be_verbose = True

# number of threads/CPU cores to be used when training -- we default
# this value to the number of available cores on the system, but you
# can supply an integer value here if you would like
options.num_threads = multiprocessing.cpu_count()

# log our training options to the terminal
print("[INFO] shape predictor options:")
print(options)

# train the shape predictor
print("[INFO] training shape predictor...")
dlib.train_shape_predictor(args["training"], args["model"], options)