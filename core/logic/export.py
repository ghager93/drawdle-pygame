import os

from typing import List, Tuple

import numpy as np
import skimage

from PIL import Image

EXPORT_DIR = os.path.join(os.getcwd(), "out", "")


def to_bmp(filename: str, size: Tuple[int, int], lines: List[List[Tuple[int, int]]]) -> None:
    filename = str(filename)
    if not os.path.exists(EXPORT_DIR):
        os.mkdir(EXPORT_DIR)

    if not os.path.splitext(filename)[1]:
        filename += ".bmp"

    image = Image.fromarray(to_numpy(lines, size), mode="L").convert("1")
    image.save(os.path.join(EXPORT_DIR, filename))


def to_quickdraw_format(lines: List[List[Tuple[int | float, int | float]]]) -> List[List[List[int]]]:
    ...


def to_json(filename: str, lines: List[List[Tuple[int | float, int | float]]]) -> None:
    ...


def to_numpy(lines: List[List[Tuple[int, int]]], size: Tuple[int]) -> np.ndarray:
    matrix = np.zeros((size[0]+1, size[1]+1), dtype=np.dtype('uint8'))
    for line in lines:
        for i in range(len(line)-1):
            matrix[skimage.draw.line(*line[i], *line[i+1])] = 255

    return matrix.T