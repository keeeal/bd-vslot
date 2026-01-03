from build123d import *

from bd_vslot.utils.typing import Align3D


class Wheel(BasePartObject):
    """
    Base class for creating wheels with specified dimensions.

    :param outer_diameter: The outer diameter of the wheel.
    :param inner_diameter: The diameter of the center hole.
    :param outer_thickness: Thickness (axially) at the outer edge.
    :param inner_thickness: Thickness (axially) at the inner edge.
    """

    def __init__(
        self,
        outer_diameter: float,
        inner_diameter: float,
        outer_thickness: float,
        inner_thickness: float,
        *,
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
    """
    A common wheel used with 2020 V-Slot rails.

    The axle should be positioned ~20 mm from the center of the V-Slot rail.
    """

    def __init__(
        self,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align3D = None,
        mode: Mode = Mode.ADD,
    ):
        super().__init__(
            outer_diameter=23.9,
            inner_diameter=16,
            outer_thickness=10.2,
            inner_thickness=5.9,
            rotation=rotation,
            align=align,
            mode=mode,
        )


class VSlot2020MiniWheel(Wheel):
    """
    A smaller wheel used with 2020 V-Slot rails.

    The axle should be positioned ~15 mm from the center of the V-Slot rail.
    """

    def __init__(
        self,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align3D = None,
        mode: Mode = Mode.ADD,
    ):
        super().__init__(
            outer_diameter=15.2,
            inner_diameter=10,
            outer_thickness=8.8,
            inner_thickness=5.8,
            rotation=rotation,
            align=align,
            mode=mode,
        )
