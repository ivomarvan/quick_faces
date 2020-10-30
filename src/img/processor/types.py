#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = """
Meta Features for image processor.
Ability to simply store constructor parameters and create the object from the stored parameters.
Types for annotation of constructor parameters with human description.
"""

import sys
import os
import inspect

from typing import Any

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..', '..'))
sys.path.append(PROJECT_ROOT)


class AutomaticPropertiesFromConstructor:
    """
    Add all named parameters of constructor to object as property
    """
    MAX_NESTED = 100

    def __init__(self):
        for i in range(1, self.MAX_NESTED):
            #print(f'{i} {self.__class__.__name__} --- inicializace lokálních proměnných ---')
            try:
                f = sys._getframe(i) if hasattr(sys, "_getframe") else None  # inspect.currentframe()
            except Exception:
                return
            v = inspect.getargvalues(f)

            for arg in v.args:
                if arg != 'self':
                    var_value = v.locals[arg]
                    # print(arg, '=> ', var_value)
                    setattr(self, arg, var_value)


class DictStorable(AutomaticPropertiesFromConstructor):
    """
    Parameters of a constructor can be stored as dictionary (json) and restored back later.
    """

    @staticmethod
    def get_module(o):
        module = o.__class__.__module__
        if module is None or module == str.__class__.__module__:
            return o.__class__.__name__  # Avoid reporting __builtin__
        else:
            return module

    def to_dict(self, store_description: bool = True, use_system_types: bool = False) -> dict:
        ret = {}
        ret['module'] = self.get_module(self)
        ret['class'] = self.__class__.__name__
        if store_description:
            ret['description'] = inspect.getdoc(self)
        params = []
        for param in inspect.signature(self.__init__).parameters.values():
            param_dict = {}
            param_dict['1.name'] = param.name
            param_dict['2.value'] = getattr(self, param.name, None)
            if param.default != inspect._empty:
                param_dict['3.default'] = param.default
            if param.annotation != inspect._empty:
                if isinstance(param.annotation, Type):
                    param_dict['4.type'] = \
                        param.annotation.to_dict(store_description=store_description, use_system_types=use_system_types)
                elif use_system_types:
                    param_dict['4.annotation'] = param.annotation
            params.append(param_dict)
        ret['params'] = params
        return ret

    @classmethod
    def from_dict(cls, in_dict: dict) -> 'DictStorable':
        def get(key: str, default=None):
            try:
                return in_dict[key]
            except:
                return default

        module = get('module')
        the_class = get('class')
        the_class_from_module = getattr(__import__(module, fromlist=[the_class]), the_class)
        params_named = {}
        for p_dict in get('params'):
            params_named[p_dict['1.name']] = p_dict['2.value']


        return the_class_from_module(**params_named)


class Type(DictStorable):
    """ Base type with human description of parameter """
    def __init__(self, descr: str, base_type=None):
        super(Type, self).__init__()

    def is_valid(self, value) -> True|str:
        """
        Return True or error string.
        """
        if self.base_type is not None and not isinstance(value, self.base_type):
            return f'Value {value} is not type of {self.base_type}.'
        return True


class IntType(Type):
    """ Integer value """
    def __init__(self, descr: str):
        super(OptionType, self).__init__(descr=descr, base_type=int)


class StrType(Type):
    """String value"""
    def __init__(self, descr: str):
        super(OptionType, self).__init__(descr=descr, base_type=str)

class BoolType(Type):
    """Boolean value"""
    def __init__(self, descr: str):
        super(OptionType, self).__init__(descr=descr, base_type=bool)


class BGRColorType(Type):
    """Color BGR value"""
    def __init__(self, descr: str):
        super(OptionType, self).__init__(descr=descr, base_type=tuple)


class OptionType(Type):
    """Option from given values"""
    def __init__(self, descr: str, options: list):
        super(OptionType, self).__init__(descr=descr)

    def is_valid(self, value) -> True|str:
        """
        Return True or error string.
        """
        if not value in self.options:
            return f'The value "{value}" must one from "{self.options}".'
        return True


class DirectoryType(Type):
    """File storage directory value"""
    def __init__(self, descr: str, must_exists: bool = False):
        super(OptionType, self).__init__(descr=descr, base_type=str)

    def is_valid(self, value) -> True|str:
        """
        Return True or error string.
        """
        err_str = super(DirectoryType, self).is_valid()
        if isinstance(err_str, str):
            return err_str
        if self.must_exists and not os.path.isdir(value):
            return f'The directory "{value}" do not exists.'
        return True


class IntInRangeType(Type):
    """ Integer value from range. """
    def __init__(self, descr: str, min_val: int, max_val:int):
        super(OptionType, self).__init__(descr=descr, base_type=int)

    def is_valid(self, value) -> True|str:
        """
        Return True or error string.
        """
        err_str = super(DirectoryType, self).is_valid()
        if isinstance(err_str, str):
            return err_str
        if value < self.min_val or value > self.max_val:
            return f'The value "{value}" must be in range <{self.min_val}, {self.max_val}>.'
        return True

