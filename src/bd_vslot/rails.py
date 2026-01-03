from itertools import product
from typing import Self

import numpy as np
from build123d import *
from build123d.build_common import LocationList
from numpy.typing import ArrayLike

from bd_vslot.utils.array import in_bounds
from bd_vslot.utils.typing import Align2D, Align3D


class VSlot2020RailProfile(BaseSketchObject):
    """
    Used to generate arbitrary shaped profiles for 2020 V-Slot rails.

    The profile is generated based on a 2D array where a True-like value
    represents the presence of a rail at that grid position. For example,
    it is possible to create a C-beam profile using the following array:

    .. code-block:: python

        [[ 1,  1 ],
         [ 1,  0 ],
         [ 1,  0 ],
         [ 1,  1 ]]

    Any array position that is True-like and adjacent to a False-like position
    will have the appropriate slot and cavity features subtracted to create
    the correct V-Slot profile. True-like positions that are adjacent to other
    True-like positions will be joined without slots.

    :param array: 2D boolean array representing the rail layout.
    """

    def __init__(
        self,
        array: ArrayLike,
        *,
        rotation: float = 0,
        align: Align2D = None,
        mode: Mode = Mode.ADD,
    ):
        array = np.asarray(array, dtype=bool)
        x, y = array.shape

        def _get(i: int, j: int) -> bool:
            """Get the value at the given indices or False if out of bounds."""
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

            translation = Vector(20 * i, 20 * j)
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
    def box(cls, num_x_rails: int = 1, num_y_rails: int = 1) -> Self:
        """
        Create a box-like V-Slot 2020 rail profile of the given dimensions.
        """
        array = np.ones((num_x_rails, num_y_rails), dtype=bool)
        return cls(array)

    @classmethod
    def c_beam(cls, num_x_rails: int = 4, num_y_rails: int = 2) -> Self:
        """
        Create a C-beam V-Slot 2020 rail profile of the given dimensions.
        """
        array = np.ones((num_x_rails, num_y_rails), dtype=bool)
        array[1:-1, 1:] = False
        return cls(array)


class VSlot2020Rail(BasePartObject):
    """
    A 2020 V-Slot rail.

    :param length: Length of the rail.
    :param num_x_rails: Number of rails along the X-axis.
    :param num_y_rails: Number of rails along the Y-axis.
    :param c_beam: Whether to create a C-beam profile. If False,
        a box-like profile will be created. Default: False.
    """

    def __init__(
        self,
        length: float,
        num_x_rails: int = 1,
        num_y_rails: int = 1,
        c_beam: bool = False,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align3D = None,
        mode: Mode = Mode.ADD,
    ):
        with BuildPart() as rail:
            with BuildSketch():
                if c_beam:
                    VSlot2020RailProfile.c_beam(num_x_rails, num_y_rails)
                else:
                    VSlot2020RailProfile.box(num_x_rails, num_y_rails)
            extrude(amount=length)

            RigidJoint("A", joint_location=Location((0, 0, length), (0, 0, 0)))
            RigidJoint("B", joint_location=Location((0, 0, 0), (180, 0, 0)))

        super().__init__(rail.part, rotation, align, mode)
