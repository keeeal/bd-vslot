from itertools import product
from typing import Optional, Union

from build123d import *
from build123d.build_common import LocationList
from build123d.topology import tuplify
from numpy.typing import NDArray

from bd_extrusions.utils.array import in_bounds


class SafeGridLocations(GridLocations):
    def __init__(
        self,
        x_spacing: float,
        y_spacing: float,
        x_count: int,
        y_count: int,
        align: Union[Align, tuple[Align, Align]] = Align.CENTER,
    ):
        super().__init__(
            x_spacing=x_spacing,
            y_spacing=y_spacing,
            x_count=max(x_count, 1),
            y_count=max(y_count, 1),
            align=align,
        )
        if x_count < 1 or y_count < 1:
            self.local_locations = []


class ArrayGridLocations(LocationList):
    def __init__(
        self,
        x_spacing: float,
        y_spacing: float,
        array: NDArray,
        align: Union[Align, tuple[Align, Align]] = Align.CENTER,
    ):
        align = tuplify(align, 2)
        x_count, y_count = array.shape
        size = [x_spacing * (x_count - 1), y_spacing * (y_count - 1)]

        offset = []
        for i in range(2):
            if align[i] == Align.MIN:
                offset.append(0.0)
            elif align[i] == Align.CENTER:
                offset.append(-size[i] / 2)
            elif align[i] == Align.MAX:
                offset.append(-size[i])

        local_locations = []
        for i, j in product(range(x_count), range(y_count)):
            if not array[i, j]:
                continue
            local_locations.append(
                Location(Vector(i * x_spacing + offset[0], j * y_spacing + offset[1]))
            )

        local_locations = Locations._move_to_existing(local_locations)
        super().__init__(local_locations)


class ArrayPolarLocations(LocationList):
    def __init__(
        self,
        x_spacing: float,
        y_spacing: float,
        a_array: NDArray,
        b_array: Optional[NDArray] = None,
        invert: bool = False,
        radius: float = 0,
        rotate: bool = True,
        align: Union[Align, tuple[Align, Align]] = Align.CENTER,
    ):
        if b_array is None:
            b_array = a_array
        assert a_array.shape == b_array.shape

        align = tuplify(align, 2)
        x_count, y_count = a_array.shape
        size = [x_spacing * (x_count - 1), y_spacing * (y_count - 1)]

        offset = []
        for i in range(2):
            if align[i] == Align.MIN:
                offset.append(0.0)
            elif align[i] == Align.CENTER:
                offset.append(-size[i] / 2)
            elif align[i] == Align.MAX:
                offset.append(-size[i])

        local_locations = []
        for i, j in product(range(x_count), range(y_count)):
            if not a_array[i, j]:
                continue
            for n, (di, dj) in enumerate(((1, 0), (0, 1), (-1, 0), (0, -1))):
                if (
                    in_bounds(b_array, i + di, j + dj) and b_array[i + di, j + dj]
                ) == invert:
                    continue
                local_locations.append(
                    Location(
                        Vector(i * x_spacing + offset[0], j * y_spacing + offset[1])
                        + Vector(radius, 0).rotate(Axis.Z, 90 * n),
                        rotate * (90 * n),
                    )
                )

        print(len(local_locations))

        self.local_locations = Locations._move_to_existing(local_locations)
        super().__init__(self.local_locations)
