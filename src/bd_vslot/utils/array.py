import numpy as np
from numpy.typing import ArrayLike


def in_bounds(array: ArrayLike, *indices: int) -> bool:
    """Check if the given indices are within the bounds of the array."""
    return all(
        0 <= index < shape
        for index, shape in zip(indices, np.asarray(array).shape, strict=True)
    )
