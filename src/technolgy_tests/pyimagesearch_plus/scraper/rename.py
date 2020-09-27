#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from pprint import pprint
import pandas as pd
import requests
import zipfile
import io

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)
NOGIT_DATA = os.path.join(PROJECT_ROOT, 'nogit_data')
OUT_DIR = os.path.join(NOGIT_DATA, 'pyimagesearch', 'tutorials')

from src.technolgy_tests.pyimagesearch_plus.scraper.download_zip import out_dir_name

def rename(row: pd.Series):
    old_dir = out_dir_name(row, new_format=False)
    new_dir = out_dir_name(row, new_format=True)
    if os.path.isdir(old_dir):
        print(old_dir, '=>', new_dir)
        os.rename(old_dir, new_dir)

if __name__ == "__main__":
    index_filename = os.path.join(OUT_DIR, 'links.tsv.gz')
    df = pd.read_csv(index_filename, sep='\t', compression='gzip')
    for i in range(len(df.index)):
        rename(df.iloc[i])


