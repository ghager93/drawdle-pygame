import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from typing import List, Dict, Tuple

import numpy as np
import tensorflow as tf


RES_DIR = os.path.join(os.getcwd(), "res", "")
MODEL_PATH = os.path.join(RES_DIR, "keras.h5")
CAT_PATH = os.path.join(RES_DIR, "cats.txt")


model = tf.keras.models.load_model(MODEL_PATH)
print(model.summary())


def predict(matrix: np.ndarray) -> Dict[str, float]:
    tensor = _preprocess(matrix)
    categories = get_categories()
    predictions =  model.predict(tensor)
    return {categories[i]: p for i, p in enumerate(predictions)}


def get_categories() -> List[str]:
    with open(CAT_PATH) as f:
        cats = f.read().splitlines()

    return cats


def sort_predictions(predictions: Dict[str, float]) -> List[Tuple[str, float]]:
    sorted_keys = sorted(predictions.keys(), key=lambda x: predictions[x])
    return [(k, predictions[k]) for k in sorted_keys]


def _preprocess(matrix: np.ndarray) -> tf.Tensor:
    matrix = np.rot90(matrix, k=2)
    tensor = tf.convert_to_tensor(matrix, dtype=float)
    tensor = tf.reshape(tensor, [1, 28, 28]) / 255
    return tensor

