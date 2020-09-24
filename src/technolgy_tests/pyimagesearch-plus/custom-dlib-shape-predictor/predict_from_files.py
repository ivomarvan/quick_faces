#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    V zadaném adresáři a podadresáří označí všechny obrázky podle daného modelu.
    
    vstupy: dir, 
    výstup: viz výstupy jednotlivých skriptů 
 
    
    @see dir
'''

import os
import sys

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

