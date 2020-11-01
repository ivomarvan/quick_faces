#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = """
Meta Features for image processor.
Ability to simply store constructor parameters and create the object from the stored parameters.
Types for annotation of constructor parameters with human description.
"""

import os
import sys

import cv2

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.img.processor.magic import DictStorable


class Type(DictStorable):
    """ Base type with human description of parameter """

    def __init__(self, descr: str, base_type=None):
        super().__init__()

    def is_valid(self, value) -> 'True|str':
        """
        Return True or error string.
        """
        if self.base_type is not None and not isinstance(value, self.base_type):
            return f'Value {value} is not type of {self.base_type}.'
        return True


class IntType(Type):
    """ Integer value """

    def __init__(self, descr: str):
        super().__init__(descr=descr, base_type=int)


class StrType(Type):
    """String value"""

    def __init__(self, descr: str):
        super().__init__(descr=descr, base_type=str)


class BoolType(Type):
    """Boolean value"""

    def __init__(self, descr: str):
        super().__init__(descr=descr, base_type=bool)


class BGRColorType(Type):
    """Color BGR value"""

    def __init__(self, descr: str):
        super().__init__(descr=descr, base_type=tuple)


class OptionType(Type):
    """Option from given values"""

    def __init__(self, descr: str, options: list):
        super().__init__(descr=descr)

    def is_valid(self, value) -> 'True | str':
        """
        Return True or error string.
        """
        if not value in self.options:
            return f'The value "{value}" must one from "{self.options}".'
        return True


class DirectoryType(Type):
    """File storage directory value"""

    def __init__(self, descr: str, must_exists: bool = False):
        super().__init__(descr=descr, base_type=str)

    def is_valid(self, value) -> 'True | str':
        """
        Return True or error string.
        """
        err_str = super().is_valid()
        if isinstance(err_str, str):
            return err_str
        if self.must_exists and not os.path.isdir(value):
            return f'The directory "{value}" does not exist.'
        return True


class FileType(Type):
    """File path"""

    def __init__(self, descr: str, must_exists: bool = False):
        super().__init__(descr=descr, base_type=str)

    def is_valid(self, value) -> 'True | str':
        """
        Return True or error string.
        """
        err_str = super().is_valid()
        if isinstance(err_str, str):
            return err_str
        if self.must_exists and not os.path.isfile(value):
            return f'The file "{value}" does not exist.'
        return True


class VideoFileType(FileType):
    """ File wir video """

    def is_valid(self, value) -> 'True | str':
        """
        Return True or error string.
        """
        err_str = super().is_valid()
        if isinstance(err_str, str):
            return err_str
        try:
            cv2.VideoCapture(value)
        except Exception as e:
            return str(e)
        return True


class IntInRangeType(Type):
    """ Integer value from range. """

    def __init__(self, descr: str, min_val: int, max_val: int):
        super().__init__(descr=descr, base_type=int)

    def is_valid(self, value) -> 'True | str':
        """
        Return True or error string.
        """
        err_str = super().is_valid()
        if isinstance(err_str, str):
            return err_str
        if value < self.min_val or value > self.max_val:
            return f'The value "{value}" must be in range <{self.min_val}, {self.max_val}>.'
        return True
