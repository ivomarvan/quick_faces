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

from src.utils.timeit_stats import TimeStatistics, timeit
from time import sleep

@timeit
def _read_and_unzip(url: str, out_dir:str):
    sleep(2)
    r = requests.get(url)
    sys.stdout.write(' downloaded')
    sys.stdout.flush()
    z = zipfile.ZipFile(io.BytesIO(r.content))
    os.makedirs(out_dir, exist_ok=True)
    z.extractall(out_dir)
    sys.stdout.write(' extracted')
    sys.stdout.flush()

def read_and_unzip(row: pd.Series):
    sys.stdout.write(row.zip_link)
    sys.stdout.flush()

    out_dir = os.path.join(OUT_DIR, f'{row.id:03d}')
    if os.path.isdir(out_dir):
        sys.stdout.write(' skipped\n')
        sys.stdout.flush()
    else:
        if row.zip_link:
            try:
                _read_and_unzip(row.zip_link, out_dir)
                sys.stdout.write(' OK\n')
            except Exception as e:
                sys.stdout.write(f' ERR: {e}\n')

        else:
            print(f'No zip_link for id={row.id} "{row.title}"')
    sys.stdout.flush()


index_filename = os.path.join(OUT_DIR, 'links.tsv.gz')
df = pd.read_csv(index_filename, sep='\t', compression='gzip')
try:
    for i in range(len(df.index)):
        read_and_unzip(df.iloc[i])
finally:
    TimeStatistics.print_as_tsv(print_header=True)


