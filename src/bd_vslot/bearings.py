from typing import Union

from build123d import *


class Bearing(BasePartObject):
    def __init__(
        self,
        outer_diameter: float,
        inner_diameter: float,
        thickness: float,
        rotation: RotationLike = (0, 0, 0),
        align: Union[Align, tuple[Align, Align, Align]] = Align.CENTER,
        mode: Mode = Mode.ADD,
    ):
        outer_radius = outer_diameter / 2
        inner_radius = inner_diameter / 2

        with BuildPart() as outer:
            Cylinder(outer_radius, thickness)
            chamfer(outer.edges(), 0.2)
            Hole(outer_radius - 1)
        with BuildPart() as seal:
            Cylinder(outer_radius - 1, thickness - 0.2)
            Hole(inner_radius + 1)
            chamfer(seal.edges(), 0.2)
        with BuildPart() as inner:
            Cylinder(inner_radius + 1, thickness)
            Hole(inner_radius)
            chamfer(inner.edges(select=Select.LAST), 0.2)
        with BuildPart() as bearing:
            add(outer)
            add(seal)
            add(inner)

        super().__init__(bearing.part, rotation, align, mode)


class Bearing625(Bearing):
    def __init__(
        self,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] = Align.CENTER,
        mode: Mode = Mode.ADD,
    ):
        super().__init__(16, 5, 5, rotation, align, mode)


class Bearing688(Bearing):
    def __init__(
        self,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] = Align.CENTER,
        mode: Mode = Mode.ADD,
    ):
        super().__init__(16, 8, 5, rotation, align, mode)


class Bearing105(Bearing):
    def __init__(
        self,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] = Align.CENTER,
        mode: Mode = Mode.ADD,
    ):
        super().__init__(10, 5, 4, rotation, align, mode)
