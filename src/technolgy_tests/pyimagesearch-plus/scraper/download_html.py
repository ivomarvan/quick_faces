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
def _read_and_save(url: str, out_dir:str):
    out_filename = os.path.join(out_dir, 'article.html')
    if os.path.isfile(out_filename):
        sys.stdout.write(' skipped (file exists aready)')
        sys.stdout.flush()
        return
    sleep(2)
    r = requests.get(url)
    with open(out_filename, 'w') as f:
        f.write(r.text)
    sys.stdout.write(' downloaded and saved')
    sys.stdout.flush()

def _read_html(row: pd.Series):
    sys.stdout.write(row.article_link)
    sys.stdout.flush()

    out_dir = os.path.join(OUT_DIR, f'{row.id:03d}')
    if not os.path.isdir(out_dir):
        sys.stdout.write(' skipped (dir do not exists yeat)\n')
        sys.stdout.flush()
    else:
        if row.article_link:
            try:
                _read_and_save(row.article_link, out_dir)
                sys.stdout.write(' OK\n')
            except Exception as e:
                sys.stdout.write(f' ERR: {e}\n')

        else:
            print(f'No article_link for id={row.id} "{row.title}"')
    sys.stdout.flush()


index_filename = os.path.join(OUT_DIR, 'links.tsv.gz')
df = pd.read_csv(index_filename, sep='\t', compression='gzip')
try:
    for i in range(len(df.index)):
        _read_html(df.iloc[i])
finally:
    TimeStatistics.print_as_tsv(print_header=True)


