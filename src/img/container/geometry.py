#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Basic containers for points, rectangles ...
    The goal is to unify results of different processors  
'''
import dlib
import numpy as np

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

    def as_tuple(self):
        return (self.x(), self.y())

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

    def as_bbox(self) -> np.ndarray:
        return np.array([
            self.left_top().x(), self.left_top().y(), self.right_bottom().x(), self.right_bottom().y()
        ])

    def __str__(self):
        right_bottom = self.right_bottom()
        return f'Rectangle(x={right_bottom.x()}, y={right_bottom.y()}, width={self.width()}, height={self.height()})'

    @classmethod
    def from_bbox(cls, bbox: np.ndarray) -> 'Rectangle':
        return Rectangle(
            left_top=Point(x=bbox[0], y=bbox[1]),
            right_bottom=Point(x=bbox[2], y=bbox[3])
        )

def landmarks_to_points(landmarks: np.ndarray)-> [Point]:
    in_list = list(landmarks[0])
    return [Point(x=p[0], y=p[1]) for p in in_list]