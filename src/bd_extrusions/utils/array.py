import numpy as np
from numpy.typing import ArrayLike


def in_bounds(array: ArrayLike, *indices: int) -> bool:
    for i, shape in zip(indices, np.asarray(array).shape, strict=True):
        if not 0 <= i < shape:
            return False
    return True
