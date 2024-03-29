#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = """
Meta Features for image processor.
Ability to simply store constructor parameters and create the object from the stored parameters.
"""

import sys
import inspect


def get_module(o):
    module = o.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return o.__class__.__name__  # Avoid reporting __builtin__
    else:
        return module

def is_builtin_class_instance(obj):
    '''
    @credit https://stackoverflow.com/questions/1322068/determine-if-python-variable-is-an-instance-of-a-built-in-type
    '''
    BUILTS_FOR_DIFFERENT_PY_VERSIONS = ['__builtin__', '__builtins__', 'builtins']
    return obj.__class__.__module__ in  BUILTS_FOR_DIFFERENT_PY_VERSIONS


class AutomaticPropertiesFromConstructor:
    """
    Add all named parameters of constructor to object as property
    """
    MAX_NESTED = 100

    def __init__(self):
        for i in range(1, self.MAX_NESTED):
            # print(f'{i} {self.__class__.__name__} --- inicializace lokálních proměnných ---')
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

    

    def to_dict(self, store_description: bool = True, use_system_types: bool = False) -> dict:
        ret = {}
        ret['module'] = get_module(self)
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
                if not is_builtin_class_instance(param.annotation):
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
