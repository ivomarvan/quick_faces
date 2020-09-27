#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Common functions.
'''
import os


def fwalk(top: str, predicates: list = [], recursively: bool = True):
    """
    Generator that filters results of os.walk using a set of predicate functions
    @credithttps://blog.anvetsu.com/posts/general-purpose-directory-iterator-python-os-walk/
    """
    for root, dirs, files in os.walk(os.path.expanduser(os.path.expandvars(top))):
        for f in files:
            cond = all(pred(root, f) for pred in predicates)
            if cond:
                yield os.path.join(root, f)
        if not recursively:
            break