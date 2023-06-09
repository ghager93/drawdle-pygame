import os
import json

from typing import List, Tuple

import numpy as np
import skimage

from PIL import Image

EXPORT_DIR = os.path.join(os.getcwd(), "out", "")


def to_bmp(filename: str, lines: List[List[Tuple[int, int]]], size: Tuple[int, int]) -> None:
    filename = str(filename)
    if not os.path.exists(EXPORT_DIR):
        os.mkdir(EXPORT_DIR)

    if not os.path.splitext(filename)[1]:
        filename += ".bmp"

    image = Image.fromarray(as_numpy(lines, size), mode="L").convert("1")
    image.save(os.path.join(EXPORT_DIR, filename))

    print("Image saved as", filename)


def to_json(filename: str, lines: List[List[Tuple[int, int]] | List[List[int]]]) -> None:
    filename = str(filename)
    if not os.path.exists(EXPORT_DIR):
        os.mkdir(EXPORT_DIR)

    if not os.path.splitext(filename)[1]:
        filename += ".json"

    with open(os.path.join(EXPORT_DIR, filename), 'w') as f:
        json.dump(lines, f)

    print("Lines saved as", filename)


def as_quickdraw(lines: List[List[Tuple[int, int]]]) -> List[List[List[int]]]:
    quickdraw_lines = []
    for line in lines:
        x_list = [p[0] for p in line]
        y_list = [p[1] for p in line]
        quickdraw_lines.append([x_list, y_list])

    return quickdraw_lines


def as_numpy(lines: List[List[Tuple[int, int]]], size: Tuple[int]) -> np.ndarray:
    matrix = np.zeros((size[0]+1, size[1]+1), dtype=np.dtype('uint8'))
    for line in lines:
        for i in range(len(line)-1):
            matrix[skimage.draw.line(*line[i], *line[i+1])] = 255

    return matrix.T
