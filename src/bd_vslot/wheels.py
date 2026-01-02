from build123d import *

from bd_vslot.utils.typing import Align3D


class Wheel(BasePartObject):
    def __init__(
        self,
        outer_diameter: float,
        inner_diameter: float,
        outer_thickness: float,
        inner_thickness: float,
        rotation: RotationLike = (0, 0, 0),
        align: Align3D = None,
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


class VSlot2020Wheel(Wheel):
    def __init__(
        self,
        rotation: RotationLike = (0, 0, 0),
        align: Align3D = None,
        mode: Mode = Mode.ADD,
    ):
        super().__init__(23.9, 16, 10.2, 5.9, rotation, align, mode)


class VSlot2020MiniWheel(Wheel):
    def __init__(
        self,
        rotation: RotationLike = (0, 0, 0),
        align: Align3D = None,
        mode: Mode = Mode.ADD,
    ):
        super().__init__(15.2, 10, 8.8, 5.8, rotation, align, mode)
