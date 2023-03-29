from typing import List, Tuple
from functools import lru_cache

import pygame as pg


def normalise_lines(lines: List[List[Tuple[int, int]]], rect: pg.Rect) -> List[List[Tuple[float, float]]]:
    """
    Normalise points of lines relative to a rectangle. 
    A point on the left side of the rectangle will have x-value = 0.
    A point on the right side of the rectangle will have x-value = 1.
    Likewise for y-value (top = 0, bottom = 1).
    """
    return [[normalise_point(p, rect) for p in line] for line in lines]


@lru_cache
def normalise_point(point: Tuple[int, int], rect: pg.Rect) -> Tuple[float, float]:
    """
    Normalise a point relative to a rectangle. 
    A point on the left side of the rectangle will have x-value = 0.
    A point on the right side of the rectangle will have x-value = 1.
    Likewise for y-value (top = 0, bottom = 1).
    """
    return (point[0] - rect.left) / rect.width, (point[1] - rect.top) / rect.height   

