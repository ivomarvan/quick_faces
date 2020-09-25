#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''

    K libovolnému řetězci (který obvykle popisuje nějakou konfiguraci) přiřadí křestní jméno ze seznamu.
    Použije se pro mnemotechnické pojmenování variant.


    Vstupy:
        * řetězec

    Výstup:
        * jedno jméno ze seznamu

'''

import sys
import os.path
import argparse
import hashlib

# root of lib repository
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.realpath(THIS_DIR + '/../../')
sys.path.append(PROJECT_ROOT)

class StrToName:

    def __init__(self, namesFile=os.path.join(THIS_DIR, 'names.txt')):
        self.namesFile = namesFile
        self.__namesList = None

    def getNamesList(self):
        '''
        Vrátí seznam jmen jako list.
        Líně ho načítá ze souboru
        '''
        if self.__namesList is None:
            if isinstance(self.namesFile, str):
                with  open(self.namesFile, 'r') as f:
                    self.__namesList = f.readlines()
            else:
                self.__namesList = self.namesFile.readlines()
        return self.__namesList


    def getName(self, inputString: str):
        '''
        K řetězci vrátí jméno.
        '''
        names = self.getNamesList()
        l = len(names)
        index = int(hashlib.sha1(inputString.encode('utf8')).hexdigest(), 16) % l
        return sorted(names)[index].strip('\n')

# --- Spustitelná část programu ----------------------------------------------------------------------------------------

if __name__ == '__main__':
    from src.ext_lib.py.cmdLine.processor import Processor
    from src.ext_lib.py.cmdLine.cmdLineParser import CmdLineParser


    class Program(Processor, CmdLineParser):
        '''
        Spouštěcí část skriptu. Command line, Exceptions, ...
        '''

        def __init__(self):
            # zpracuje příkazovou řádku
            CmdLineParser.__init__(self, description=__description__)

            # spustí program, zachytí výjimky
            Processor.__init__(self)


        def _addArgsToCmdLineParser(self, parser):
            '''
            Definice příkazové řádky
            '''
            default = os.path.join(THIS_DIR, 'names.txt')
            parser.add_argument(
                '-n', '--names-file',
                dest='namesFile',
                metavar='<namesFile>',
                type=argparse.FileType('r'),
                required=False,
                help='Soubor se seznamem jmen. (default: ' + str(default) + ')',
                default=default
            )

            parser.add_argument(
                dest='inputString',
                help='Řetězec, který se má převést na jméno.',
                type=str
            )


        def run(self):
            strToName = StrToName(self.cmdLineParams.namesFile)
            print(strToName.getName(self.cmdLineParams.inputString))

    Program()