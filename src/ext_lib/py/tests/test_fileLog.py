#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Testy pro třídu FileLog
"""

__author__ = "Ivo Marvan"
__email__ = "ivo@wikidi.com"

import sys
import os.path
import unittest
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import fileLock



class TestSortedFileReader(unittest.TestCase):

    def test_Basic(self):
        filename = os.path.dirname(os.path.abspath(__file__)) + '/data/logTest.txt'
        with fileLock.FileLock(filename, timeout=60) as lock:
            try:
                with fileLock.FileLock(filename, timeout=0.1, delay=.05) as lock:
                    pass
                self.assertTrue(False, "Nemelo by jit otevrit zamknuty soubor")
            except fileLock.FileLockException:
                self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
