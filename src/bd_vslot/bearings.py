from build123d import *

from bd_vslot.utils.typing import Align3D


class Bearing(BasePartObject):
    """
    Base class for creating bearings with specified dimensions.

    Args:
        outer_diameter (float): The outer diameter of the bearing.
        inner_diameter (float): The diameter of the center hole.
        thickness (float): Thickness in the axial direction.
    """

    def __init__(
        self,
        outer_diameter: float,
        inner_diameter: float,
        thickness: float,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align3D = None,
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
    """
    625 bearing (OD: 16mm, ID: 5mm, T: 5mm).

    Used with 2020 V-Slot wheels.
    """

    def __init__(
        self,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align3D = None,
        mode: Mode = Mode.ADD,
    ):
        super().__init__(
            outer_diameter=16,
            inner_diameter=5,
            thickness=5,
            rotation=rotation,
            align=align,
            mode=mode,
        )


class Bearing688(Bearing):
    """
    688 bearing (OD: 16mm, ID: 8mm, T: 5mm).

    Used with 2020 V-Slot wheels.
    """

    def __init__(
        self,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align3D = None,
        mode: Mode = Mode.ADD,
    ):
        super().__init__(
            outer_diameter=16,
            inner_diameter=8,
            thickness=5,
            rotation=rotation,
            align=align,
            mode=mode,
        )


class Bearing105(Bearing):
    """
    105 bearing (OD: 10mm, ID: 5mm, T: 4mm).

    Used with 2020 V-Slot mini wheels.
    """

    def __init__(
        self,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align3D = None,
        mode: Mode = Mode.ADD,
    ):
        super().__init__(
            outer_diameter=10,
            inner_diameter=5,
            thickness=4,
            rotation=rotation,
            align=align,
            mode=mode,
        )
