#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Interface for parametr for image processor.

'''
import sys
import os
from enum import Enum, auto

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..', '..'))
sys.path.append(PROJECT_ROOT)


class ParameterType(Enum):
    '''
    Type of parametr.
    '''
    string = auto()
    integer = auto()
    boolean = auto()
    directory = auto()
    option = auto()
    group = auto()

class DictStorable:

    def get_module(self):
        module = self.__class__.__module__
        if module is None or module == str.__class__.__module__:
            return None
        else:
            return module



    @staticmethod
    def get(in_dict: dict, key: str, default=None):
        try:
            return in_dict[key]
        except KeyError:
            return default

    def __init__(
        self,
        full_package_class_name: str,
        markup_description: str = '',
        parameters: ['DictStorable'] = None
    ):
        self._full_package_class_name = full_package_class_name
        self._markup_description = markup_description
        self._parameters = parameters

    def to_dict(self, store_description: bool = True) -> dict:
        ret =  { 'class': self._full_package_class_name }
        if store_description:
            ret['description'] = self._markup_description
        if self._parameters:
            parameters = [p.to_dict() for p in self._params]
            if parameters:
                ret['params'] = ret['params']

    @classmethod
    def from_dict(cls, in_dict: dict, store_description: bool = True) -> 'ImgProcessorDescription':
        return DictStorable(
            full_package_class_name=DictStorable.get(in_dict, 'class'),
            markup_description=DictStorable.get(in_dict, 'description'),
            params=[p.read_from_dict() for p in DictStorable.get(in_dict, 'params')]
        )



class Param(DictStorable):
    '''
    Param object is used to say to GUI how to fill real values of the parameter for image processors.
    '''

    def __init__(self, name: str, markup_description: str = '', default=None):
        self._name = name
        self._markup_description = markup_description
        self._value = default

    def get_name(self) -> str:
        return self._name

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    def get_markup_description(self):
        return self._markup_description

    def is_valid(self, value) -> bool:
        return True

    def to_dict(self):
        return {
            'class': self.__class__.__name__,
            'name': self.get_name(),
            'markup_description': self.get_markup_description(),
            'value': self.get_value()
        }

    @classmethod
    def from_dict(cls, in_dict: dict, store_description: bool = True) -> 'Param':
        pass





# class ImgProcessorDescription(DictStorable):






if __name__ == "__main__":
    from src.img.processor.params.params import Param
    from src.img.processor.landmarks_detector.face_alignment_landmarks_detector import FaceAlignmentLandmarksDetector

    x = Param(
        name='root',
        markup_description='To je ##paramettr##'
    )
    from pprint import pprint

    pprint(x.to_dict(), indent=3)

    import jsonpickle
    print(jsonpickle.encode(x, indent=3))