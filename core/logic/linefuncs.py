from typing import List, Tuple
from functools import lru_cache
from collections import namedtuple

import pygame as pg


HashableRect = namedtuple("HashableRect", "left top width height")


def normalise_lines(lines: List[List[Tuple[int, int]]], rect: pg.Rect) -> List[List[Tuple[float, float]]]:
    """
    Normalise points of lines relative to a rectangle. 
    A point on the left side of the rectangle will have x-value = 0.
    A point on the right side of the rectangle will have x-value = 1.
    Likewise for y-value (top = 0, bottom = 1).
    """
    return [[normalise_point(p, HashableRect(*tuple(rect))) for p in line] for line in lines]


@lru_cache
def normalise_point(point: Tuple[int, int], rect: HashableRect) -> Tuple[float, float]:
    """
    Normalise a point relative to a rectangle. 
    A point on the left side of the rectangle will have x-value = 0.
    A point on the right side of the rectangle will have x-value = 1.
    Likewise for y-value (top = 0, bottom = 1).
    """
    return (point[0] - rect.left) / rect.width, (point[1] - rect.top) / rect.height   


def scale_lines(lines: List[List[Tuple[float, float]]], rect: pg.Rect) -> List[List[Tuple[float, float]]]:
    """
    Scale points of lines by the dimensions of a rectangle, such that a normalised set of points will shifted and scaled to within the rectangle.
    Inverse function of normalise_lines (except returns float not int).
    """
    return [[scale_point(p, HashableRect(*tuple(rect))) for p in line] for line in lines]


@lru_cache
def scale_point(point: Tuple[float, float], rect: HashableRect) -> Tuple[float, float]:
    """
    Scale a pointby the dimensions of a rectangle, such that a normalised set of points will shifted and scaled to within the rectangle.
    Inverse function of normalise_point (except returns float not int).
    """
    return point[0]*rect.width + rect.left, point[1]*rect.height + rect.top    

