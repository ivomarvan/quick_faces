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
from tsvFileReader import TsvFileReader
import unittest



class TestTsvFileReader(unittest.TestCase):

    def rowsTest(self, filename, skipEmptyRows):
        reader = TsvFileReader(filename)
        self.assertListEqual(reader.getRow(skipEmptyRows), ['ahoj', 'příliš žluťoučký kůň pěl dábelské ódy konec',
                                                            '(60° C)', 'Kärcher', 'Pro² 7001'], '1. řádek')
        self.assertListEqual(reader.getRow(skipEmptyRows), ['1', '2'], '2. řádek')
        if not skipEmptyRows:
            self.assertListEqual(reader.getRow(skipEmptyRows), [], '3. řádek, prázdný')
        self.assertListEqual(reader.getRow(skipEmptyRows), ['', ''], '4. řádek')
        self.assertListEqual(reader.getRow(skipEmptyRows), ['poslední'], '5. řádek')
        self.assertIsNone(reader.getRow(skipEmptyRows), '6. řádek - tam už není')


    def test_tsvNoSkip(self):
        """Testuje čtení z nezazipovaného souboru bez přeskakování prázdných řádků."""
        self.rowsTest(os.path.dirname(os.path.abspath(__file__)) + '/data/simple.tsv', False)

    def test_tsvGzNoSkip(self):
        """Testuje čtení z zazipovaného souboru bez přeskakování prázdných řádků."""
        self.rowsTest(os.path.dirname(os.path.abspath(__file__)) + '/data/simple.tsv.gz', False)

    def test_tsvSkip(self):
        """Testuje čtení z nezazipovaného souboru s přeskakováním prázdných řádků."""
        self.rowsTest(os.path.dirname(os.path.abspath(__file__)) + '/data/simple.tsv', True)

    def test_tsvGzSkip(self):
        """Testuje čtení z zazipovaného souboru s přeskakováním prázdných řádků."""
        self.rowsTest(os.path.dirname(os.path.abspath(__file__)) + '/data/simple.tsv.gz', True)



if __name__ == "__main__":
    unittest.main()
