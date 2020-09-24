#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Testy pro třídu TsvFileReader
"""

__author__ = "Ivo Marvan"
__email__ = "ivo@wikidi.com"

import sys
import os.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from sortedFileReader import SortedFileReader, OrderError
import unittest



class TestSortedFileReader(unittest.TestCase):

    def goodOrder(self, filename):
        reader = SortedFileReader(filename, 1)
        self.assertListEqual(reader.getRowForId('0', False), ['5.', '0','60°'], '1.klic 0')
        self.assertListEqual(reader.getRowForId('0', False), ['6.', '0','Pro²'], '2.klic 0')
        self.assertIsNone(reader.getRowForId('0', False),  'klic 0 tam uz neni')
        self.assertListEqual(reader.getRowForId('klíček', False), ['druhý', 'klíček','b'], 'najdi vybraný radek')
        self.assertListEqual(reader.getRowForId('žäž', False), ['10.', 'žäž','ž1'], 'posledni zdojeny klic')

    def test_goodOrderTsv(self):
        self.goodOrder(os.path.dirname(os.path.abspath(__file__)) + '/data/sorted.LC_ALL=C.tsv')

    def test_goodOrderGz(self):
        self.goodOrder(os.path.dirname(os.path.abspath(__file__)) + '/data/sorted.LC_ALL=C.tsv.gz')

    def test_badOrder(self):
        reader = SortedFileReader(os.path.dirname(os.path.abspath(__file__)) + '/data/unsorted.tsv', 1)
        self.assertRaises(OrderError, reader.getRowForId('0'), 'spatne usporadany soubor' )

    def test_goodOrderTsvWithSkipiingSameRows(self):
        reader = SortedFileReader(os.path.dirname(os.path.abspath(__file__)) + '/data/sorted.LC_ALL=C.tsv', 1)
        self.assertListEqual(reader.getRowForId('0', True), ['5.', '0','60°'], '1.klic 0')
        self.assertIsNone(reader.getRowForId('0', True),  'klic 0 tam uz neni')
        self.assertListEqual(reader.getRowForId('klíček', True), ['druhý', 'klíček','b'], 'najdi vybraný radek')
        self.assertListEqual(reader.getRowForId('žäž', True), ['10.', 'žäž','ž1'], 'posledni zdojeny klic')
        self.assertIsNone(reader.getRowForId('žäž', True),  'klic žžž tam uz neni')

if __name__ == "__main__":
    unittest.main()
