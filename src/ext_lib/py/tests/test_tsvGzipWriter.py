#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Testy pro třídu TsvGzipWriter
"""

__author__ = "Ivo Marvan"
__email__ = "ivo@wikidi.com"

import sys
import os.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from tsvGzipWriter import TsvGzipWriter
from tsvFileReader import TsvFileReader
import unittest



class TestTsvGzipWriter(unittest.TestCase):

    _rows =  [
        ['ahoj', 'příliš žluťoučký kůň pěl dábelské ódy'],
        ['1', '"2"'],
        ['(60° C)', 'Kärcher', 'Pro² 7001'],
        ['ě', 'š', 'č', 'ř', 'ž', 'ý', 'á', 'í', 'é', 'ů', 'ú']
    ]

    def writeReadRows(self, outputFilenameRelativePtah):
        '''
        Ulozi radky do souboru a nasledne je zase nacte
        '''
        outputFilename = os.path.dirname(os.path.abspath(__file__)) + '/data/' + outputFilenameRelativePtah
        writer = TsvGzipWriter(outputFilename)
        for row in self._rows:
            writer.writerow(row)

        writer.close()
        reader = TsvFileReader(outputFilename)
        for row in self._rows:
            rowFromFile = reader.getRow()
            self.assertListEqual(row, rowFromFile)

    def test_UnicodeZipped(self):
        self.writeReadRows('unicodeTsvGzipWriterTest.tsv.gz')

    def test_UnicodeNoZipped(self):
        self.writeReadRows('unicodeTsvGzipWriterTest.tsv')


if __name__ == "__main__":
    unittest.main()
