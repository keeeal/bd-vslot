from typing import Union

from build123d import *


class Wheel(BasePartObject):
    def __init__(
        self,
        outer_diameter: float = 23.9,
        inner_diameter: float = 5,
        outer_thickness: float = 10.25,
        inner_thickness: float = 10.25,
        rotation: RotationLike = (0, 0, 0),
        align: Union[Align, tuple[Align, Align, Align]] = Align.CENTER,
        mode: Mode = Mode.ADD,
    ):
        outer_radius = outer_diameter / 2
        inner_radius = inner_diameter / 2

        with BuildPart() as wheel:
            Cylinder(outer_radius, outer_thickness)
            chamfer(wheel.edges(), (outer_thickness - inner_thickness) / 2)
            Hole(inner_radius)
            chamfer(wheel.edges(select=Select.LAST), 0.3)

        super().__init__(wheel.part, rotation, align, mode)


class VWheel(Wheel):
    def __init__(
        self,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] = Align.CENTER,
        mode: Mode = Mode.ADD,
    ):
        super().__init__(23.9, 16, 10.2, 5.9, rotation, align, mode)


class MiniVWheel(Wheel):
    def __init__(
        self,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] = Align.CENTER,
        mode: Mode = Mode.ADD,
    ):
        super().__init__(15.2, 10, 8.8, 5.8, rotation, align, mode)
