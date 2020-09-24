#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@wikidi.com"

description = '''
    Vypíše moduly, které potřebuje daný skript.
'''

import sys
import os
import argparse
from modulefinder import ModuleFinder
from collections import OrderedDict

# root of lib repository
__PROJECT_ROOT__ = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../../../')
sys.path.append(__PROJECT_ROOT__)

from lib.py.cmdLine.processor import Processor
from lib.py.cmdLine.cmdLineParser import CmdLineParser

class Program(Processor, CmdLineParser):
    '''
    Viz parametr description.
    '''

    def __init__(self):

        # zpracuje příkazovou řádku
        CmdLineParser.__init__(self, description=description,)

        # spustí program, zachytí výjimky
        Processor.__init__(self)


    def _addArgsToCmdLineParser(self, parser):

        default = sys.stdin
        parser.add_argument(
            dest='infile',
            metavar='<pythonScriptFileName>',
            type=argparse.FileType('r'),
            help='vstupní soubor s pytoním skriptem',
            nargs='?'
        )

        dafault = False
        parser.add_argument(
            '-r', '--restrict-to-project-dir-only',
            dest='restrictToProject',
            action='store_true',
            default=dafault,
            help='Prohledává jen adresářích projektu. (default:{})'.format(dafault)
        )


    def run(self):
        p = self.cmdLineParams


        finder = ModuleFinder()
        finder.run_script(p.infile.name)

        modDict = {}
        for name, mod in finder.modules.items():
            if mod.__file__ is None:
                key = str(mod.__file__)
            else:
                key = os.path.abspath(mod.__file__)
            if not key in modDict:
                modDict[key] = []
            modDict[key].append(name)
        # sort
        for key in sorted(modDict):
            if p.restrictToProject and not key.startswith(__PROJECT_ROOT__):
                continue
            modules = modDict[key]
            sys.stdout.write(key)
            for moduleName in modules:
                sys.stdout.write('\t')
                sys.stdout.write(moduleName)
            sys.stdout.write('\n')




if __name__ == '__main__':
    # vytvoří objekt programu a spustí ho
    Program()