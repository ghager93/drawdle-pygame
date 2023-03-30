from typing import List, Tuple
from functools import lru_cache
from collections import namedtuple

import pygame as pg

from rdp import rdp


HashableRect = namedtuple("HashableRect", "left top width height")


def normalise_line(
    line: List[Tuple[int, int]], rect: pg.Rect
) -> List[Tuple[float, float]]:
    """
    Normalise points of a line relative to a rectangle.
    A point on the left side of the rectangle will have x-value = 0.
    A point on the right side of the rectangle will have x-value = 1.
    Likewise for y-value (top = 0, bottom = 1).
    """
    return [normalise_point(p, HashableRect(*tuple(rect))) for p in line]


@lru_cache
def normalise_point(point: Tuple[int, int], rect: HashableRect) -> Tuple[float, float]:
    """
    Normalise a point relative to a rectangle.
    A point on the left side of the rectangle will have x-value = 0.
    A point on the right side of the rectangle will have x-value = 1.
    Likewise for y-value (top = 0, bottom = 1).
    """
    return (point[0] - rect.left) / rect.width, (point[1] - rect.top) / rect.height


def scale_line(
    line: List[Tuple[float, float]], rect: pg.Rect
) -> List[Tuple[float, float]]:
    """
    Scale points of a line by the dimensions of a rectangle, such that a normalised set of points will shifted and scaled to within the rectangle.
    Inverse function of normalise_lines (except returns float not int).
    """
    return [scale_point(p, HashableRect(*tuple(rect))) for p in line]


@lru_cache
def scale_point(point: Tuple[float, float], rect: HashableRect) -> Tuple[float, float]:
    """
    Scale a pointby the dimensions of a rectangle, such that a normalised set of points will shifted and scaled to within the rectangle.
    Inverse function of normalise_point (except returns float not int).
    """
    return point[0] * rect.width + rect.left, point[1] * rect.height + rect.top


def decimate_line(
    line: List[Tuple[int | float, int | float]], epsilon: float = 1
) -> List[Tuple[float, float]]:
    """
    Reduces number of points in the line by reducing the resolution of curves.
    Higher epsilon means more reduction.
    """
    dec_line = rdp(line, epsilon)
    return [tuple(p) for p in dec_line]


def calculate_line_bounds(
    line: List[Tuple[int | float, int | float]]
) -> Tuple[float, float, float, float]:
    """
    Returns the min and max width and height of line.
    """
    x_min = min([p[0] for p in line])
    x_max = max([p[0] for p in line])
    y_min = min([p[1] for p in line])
    y_max = max([p[1] for p in line])

    return x_min, x_max, y_min, y_max
