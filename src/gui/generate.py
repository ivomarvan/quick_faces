#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Generate d GUI from constructors of image processors.
'''
import sys
import os
import inspect
from copy import deepcopy
from pprint import pprint

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.utils.common import fwalk
from src.img.processor.processor import ImgProcessor
from src.img.processor.magic import get_module

class GuiGenerator:
    '''
    Generate GUI from constructors of image processors.
    '''
    OUT_DIR = os.path.join(THE_FILE_DIR, 'generated')
    PROCESSORS_DIR = os.path.join(PROJECT_ROOT, 'src', 'img', 'processor')

    def __init__(
        self,
        out_filename = os.path.join(OUT_DIR, 'gui.generated.py')
    ):
        self._classes = {}

    def run(self):
        self._store_clases_from_root(root=self.PROCESSORS_DIR, starts_from = ['source', 'storage'])
        pprint(self._classes)

    def _store_clases_from_root(self, root: str = PROCESSORS_DIR, starts_from: [str] = [] ):
        for path in fwalk(top=root, predicates=[lambda root, file: file.endswith('.py')], recursively=True):
            long_module_name = path[len(PROJECT_ROOT) + 1:].replace(os.path.sep, '.')[:-3]
            long_module_list = long_module_name.split('.')[1:]
            category = long_module_list[-2]
            if starts_from != []:
                if not category in starts_from:
                    continue
            if not category in self._classes:
                self._classes[category] = {}
            module_object = __import__(long_module_name)
            self._store_classes(
                module_object=module_object,
                long_module_list=long_module_list,
                to_dict=self._classes[category]
            )

    def _store_classes(self, module_object: 'module', long_module_list: list, to_dict:dict):
        '''
        Colect all image processors
        '''
        mod_list = deepcopy(long_module_list)
        # find last level of module
        module_type = type(module_object)
        while mod_list:
            first = mod_list.pop(0)
            for name, cls in module_object.__dict__.items():
                if name == first and isinstance(cls, module_type):
                    module_object=cls
                    break
        # find Image Processors
        for name, cls in module_object.__dict__.items():
            if inspect.isclass(cls) and issubclass(cls, ImgProcessor):
                if not 'Base' in name:  # @todo Hack
                    key = cls.__module__ + '.' +name
                    to_dict[key] = cls


if __name__ == "__main__":
    g = GuiGenerator()
    g.run()