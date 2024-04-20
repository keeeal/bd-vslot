from __future__ import annotations

from itertools import product
from typing import Union

import numpy as np
from build123d import *
from build123d.build_common import LocationList
from build123d.topology import tuplify
from numpy.typing import ArrayLike

from bd_vslot.utils.array import in_bounds


class VSlotProfile(BaseSketchObject):
    def __init__(
        self,
        array: ArrayLike,
        rotation: float = 0,
        align: Union[Align, tuple[Align, Align]] = Align.CENTER,
        mode: Mode = Mode.ADD,
    ):
        array = np.asarray(array, dtype=bool)
        x, y = array.shape
        size = 20 * x, 20 * y
        align = tuplify(align, 2)
        offset = []
        for i in range(2):
            if align[i] == Align.MIN:
                offset.append(0.0)
            elif align[i] == Align.CENTER:
                offset.append(-size[i] / 2)
            elif align[i] == Align.MAX:
                offset.append(-size[i])

        def _get(i: int, j: int) -> bool:
            return in_bounds(array, i, j) and array[i, j]

        squares: list[Location] = []
        slots: list[Location] = []
        center_cavities: list[Location] = []
        center_cavities_mirrored: list[Location] = []
        corner_cavities: list[Location] = []
        corner_cavities_mirrored: list[Location] = []
        edge_cavities: list[Location] = []
        edge_cavities_mirrored: list[Location] = []

        for i, j in product(range(x), range(y)):
            if not array[i, j]:
                continue
            if all(map(_get, (i + 1, i, i - 1, i), (j, j + 1, j, j - 1))):
                continue
            translation = Vector(20 * i + offset[0], 20 * j + offset[1])
            squares.append(Location(translation))
            for n, (di, dj) in enumerate(((1, 0), (0, 1), (-1, 0), (0, -1))):
                location = Location(translation, 90 * n)
                if _get(i + di, j + dj):
                    if di:
                        if _get(i, j + di):
                            if _get(i + di, j + di):
                                center_cavities.append(location)
                            else:
                                corner_cavities.append(location)
                        else:
                            edge_cavities.append(location)
                        if _get(i, j - di):
                            if _get(i + di, j - di):
                                center_cavities_mirrored.append(location)
                            else:
                                corner_cavities_mirrored.append(location)
                        else:
                            edge_cavities_mirrored.append(location)
                    else:
                        if _get(i + dj, j):
                            if _get(i + dj, j + dj):
                                center_cavities_mirrored.append(location)
                            else:
                                corner_cavities_mirrored.append(location)
                        else:
                            edge_cavities_mirrored.append(location)
                        if _get(i - dj, j):
                            if _get(i - dj, j + dj):
                                center_cavities.append(location)
                            else:
                                corner_cavities.append(location)
                        else:
                            edge_cavities.append(location)
                else:
                    slots.append(location)

        with BuildSketch() as slot:
            with BuildLine():
                Polyline(
                    (3.75, 0),
                    (3.9, 0.15),
                    (3.9, 2.84),
                    (6.56, 5.5),
                    (8.2, 5.5),
                    (8.2, 3.125),
                    (8.545, 3.125),
                    (10, 4.58),
                    (10, 0),
                )
                mirror(about=Plane.XZ)
            make_face()

        with BuildSketch() as edge_cavity:
            with BuildLine():
                Polyline(
                    (10, 0),
                    (3.9, 0),
                    (3.9, 3.16),
                    (7.3, 6.56),
                    (7.3, 8.2),
                    (10, 8.2),
                    (10, 0),
                )
            make_face()

        with BuildSketch() as corner_cavity:
            with BuildLine():
                Polyline(
                    (10, 0),
                    (3.9, 0),
                    (3.9, 2.84),
                    (9.26, 8.2),
                    (10, 8.2),
                    (10, 0),
                )
            make_face()

        with BuildSketch() as center_cavity:
            with BuildLine():
                Polyline(
                    (10, 0),
                    (3.9, 0),
                    (3.9, 2.84),
                    (3.37, 3.37),
                    (10, 10),
                    (10, 0),
                )
            make_face()

        with BuildSketch() as profile:
            with LocationList(squares):
                Rectangle(20, 20)
                Circle(2.1, mode=Mode.SUBTRACT)
            with LocationList(slots):
                add(slot.face(), mode=Mode.SUBTRACT)
            with LocationList(center_cavities):
                add(center_cavity.face(), mode=Mode.SUBTRACT)
            with LocationList(center_cavities_mirrored):
                add(center_cavity.face().mirror(Plane.XZ), mode=Mode.SUBTRACT)
            with LocationList(corner_cavities):
                add(corner_cavity.face(), mode=Mode.SUBTRACT)
            with LocationList(corner_cavities_mirrored):
                add(corner_cavity.face().mirror(Plane.XZ), mode=Mode.SUBTRACT)
            with LocationList(edge_cavities):
                add(edge_cavity.face(), mode=Mode.SUBTRACT)
            with LocationList(edge_cavities_mirrored):
                add(edge_cavity.face().mirror(Plane.XZ), mode=Mode.SUBTRACT)

        super().__init__(profile.sketch, rotation, align, mode)

    @classmethod
    def box(cls, num_x_rails: int = 1, num_y_rails: int = 1) -> VSlotProfile:
        array = np.ones((num_x_rails, num_y_rails), dtype=bool)
        return cls(array)

    @classmethod
    def c_beam(cls, num_x_rails: int = 4, num_y_rails: int = 2) -> VSlotProfile:
        array = np.ones((num_x_rails, num_y_rails), dtype=bool)
        array[1:-1, 1:] = False
        return cls(array)


class VSlotRail(BasePartObject):
    def __init__(
        self,
        length: float,
        num_x_rails: int = 1,
        num_y_rails: int = 1,
        c_beam: bool = False,
        rotation: RotationLike = (0, 0, 0),
        align: Union[Align, tuple[Align, Align, Align]] = Align.CENTER,
        mode: Mode = Mode.ADD,
    ):
        super().__init__(
            part=extrude(
                (
                    VSlotProfile.c_beam(num_x_rails, num_y_rails)
                    if c_beam
                    else VSlotProfile.box(num_x_rails, num_y_rails)
                ),
                amount=length,
                dir=(0, 0, 1),
            ),
            rotation=rotation,
            align=align,
            mode=mode,
        )
