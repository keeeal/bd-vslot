from enum import Enum

HOLE_TOLERANCE = 0.05


class BoltSize(Enum):
    """Standard bolt sizes and their radii in millimeters."""

    M3 = 1.5
    M4 = 2.0
    M5 = 2.5
    M6 = 3.0
