#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import re
from pprint import pprint
import pandas as pd


# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)
NOGIT_DATA = os.path.join(PROJECT_ROOT, 'nogit_data')
OUT_DIR = os.path.join(NOGIT_DATA, 'pyimagesearch', 'tutorials')

HREF_REG_1 = re.compile(r'"https://www.pyimagesearch.com/20[^"]*')
HREF_REG_2 = re.compile(r'"(http[s]?://(s3-us-west-2.amazonaws.com/static.pyimagesearch.com/|pyimg.co/)[^"]*)')
TITLE_REG = re.compile(r'class="html-attribute-value">_blank</span>"&gt;</span>([^👉\s][^>]+)<span')

SEPARATOR = '''class="html-tag">&lt;/strong&gt;</span><span class="html-tag">&lt;/li&gt;</span>
        </td>'''

data_dict = []

filename = os.path.join(THE_FILE_DIR, '..', 'doc', 'index.html')
with open(filename, 'r') as f:
    html_str = f.read()

rows = []
for i, text in enumerate(html_str.split(SEPARATOR)):

    # find article link
    matches = HREF_REG_1.findall(text)
    if not matches:
        continue
    article_link = matches[0].strip('"/')

    # find zip_file
    matches = HREF_REG_2.findall(text)
    zip_link = matches[0][0].strip('"/') if matches else ''

    # find title
    matches = TITLE_REG.findall(text)
    title = ''
    titles = [m for m in matches if m[0].isupper()]
    if titles:
        title = titles[0]
        title = ' '.join([m.strip(' ') for m in title.split('\n')])
    #pprint(matches, indent=3)

    rows.append([i, article_link, zip_link, title])

# pprint(rows)
df = pd.DataFrame(data=rows, columns=['id', 'article_link', 'zip_link', 'title'])
os.makedirs(OUT_DIR, exist_ok=True)
out_filename = os.path.join(OUT_DIR, 'links.tsv.gz')
print(out_filename)
df.to_csv(out_filename, sep='\t', compression='gzip')
