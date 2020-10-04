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
import re

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.default_dirs import DEFAULT_LANDMARK_FILES, get_landmark_filename
from src.train_test.landmarks.sets import LANDMARKS_MODELS


def select_labels(type: str, model_name: str):
    # to easily parse out the eye locations from the XML file we can
    # utilize regular expressions to determine if there is a 'part'
    # element on any given line
    PART = re.compile("part name='[0-9]+'")

    # load the contents of the original XML file and open the output file
    # for writing
    rows = open(DEFAULT_LANDMARK_FILES[type]).read().strip().split("\n")
    output = open(get_landmark_filename(type, model_name), "w")

    # loop over the rows of the data split file
    for row in rows:
        # check to see if the current line has the (x, y)-coordinates for
        # the facial landmarks we are interested in
        parts = re.findall(PART, row)

        # if there is no information related to the (x, y)-coordinates of
        # the facial landmarks, we can write the current line out to disk
        # with no further modifications
        if len(parts) == 0:
            output.write("{}\n".format(row))

        # otherwise, there is annotation information that we must process
        else:
            # parse out the name of the attribute from the row
            attr = "name='"
            i = row.find(attr)
            j = row.find("'", i + len(attr) + 1)
            name = int(row[i + len(attr):j])

            # if the facial landmark name exists within the range of our
            # indexes, write it to our output file
            if name in LANDMARKS_MODELS[model_name]:
                output.write("{}\n".format(row))
    # close the output file
    output.close()

if __name__ == "__main__":

    print(os.path.basename(os.path.abspath(__file__)))
    for model_name, landmarks_set in LANDMARKS_MODELS.items():
        for type in ['test', 'train_test']:
            print(f'model:{model_name}, {type}')
            select_labels(type=type, model_name=model_name)
