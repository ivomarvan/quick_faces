#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Basic containers for points, rectangles ...
    The goal is to unify results of different processors  
'''
import dlib

class Point:

    def __init__(self, x: int = None, y: float = int):
        self.__x = x
        self.__y = y


    def x(self):
        return self.__x

    def y(self):
        return self.__y

    def __str__(self):
        return f'Point(x={self.x()}, y={self.y()})'

class Rectangle:

    def __init__(self, left_top: Point, right_bottom:Point):
        self.__left_top  = left_top
        self.__right_bottom = right_bottom

    def right_bottom(self) -> Point :
        return self.__right_bottom

    def left_top(self) -> Point :
        return self.__left_top

    '''
    def left_bottom(self) -> Point :
        return Point(self.left_bottom().x(), self._right_bottom().y())

    def right_top(self) -> Point :
        return Point(self.right_bottom().x(), self.left_top().y())
    '''

    def width(self) -> int :
        return self.right_bottom().x() - self.left_top().x() + 1

    def height(self) -> int :
        return self.right_bottom().y() - self.left_top().y() + 1

    def center(self) -> Point:
        return Point(
            x=int(round((self.right_bottom().x() + self.left_top().x() / 2), 0)),
            y=int(round((self.right_bottom().y() + self.left_top().y() / 2), 0))
        )

    def __str__(self):
        return f'Rectangle(left_top=({self.left_top()}), width={self.width()}, height={self.height()})'

    @classmethod
    def crate_from_dlib_rectangle(cls, dlib_rect: dlib.rectangle) -> 'Rectangle':
        return Rectangle(
            left_top=Point(x=dlib_rect.left(), y=dlib_rect.top()),
            right_bottom=Point(x=dlib_rect.right(), y=dlib_rect.bottom())
        )

    def as_dlib_rectangle(self) -> dlib.rectangle:
        return dlib.rectangle(
            left=self.left_top().x(),
            top=self.left_top().y(),
            right=self.right_bottom().x(),
            bottom=self.right_bottom().y()
        )

    def __str__(self):
        right_bottom = self.right_bottom()
        return f'Rectangle(x={right_bottom.x()}, y={right_bottom.y()}, width={self.width()}, height={self.height()})'