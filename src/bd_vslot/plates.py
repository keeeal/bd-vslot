from __future__ import annotations

from build123d import *

from bd_vslot.constants import HOLE_TOLERANCE, BoltSize
from bd_vslot.utils.typing import Align2D, Align3D


class VSlot2020EndCapProfile(BaseSketchObject):
    """
    An end cap profile for 2020 V-Slot rails.

    Holes are spaced 20 mm apart to align with tapped holes in the ends of
    the rails. The width and height are determined by the number of holes
    specified along each axis.

    :param num_x_holes: Number of holes (rails) along the X-axis.
    :param num_y_holes: Number of holes (rails) along the Y-axis.
    :param hole_radius: The radius of the holes for the bolts.
    :param corner_radius: Filet radius for the corners of the end cap.
    """

    def __init__(
        self,
        num_x_holes: int,
        num_y_holes: int,
        hole_radius: BoltSize | float,
        corner_radius: float = 0,
        *,
        rotation: float = 0,
        align: Align2D = None,
        mode: Mode = Mode.ADD,
    ):
        if isinstance(hole_radius, BoltSize):
            hole_radius = hole_radius.value + HOLE_TOLERANCE

        width = 20 * num_x_holes
        height = 20 * num_y_holes

        with BuildSketch() as profile:
            (
                RectangleRounded(width, height, corner_radius)
                if corner_radius
                else Rectangle(width, height)
            )
            with GridLocations(20, 20, num_x_holes, num_y_holes):
                Circle(hole_radius, mode=Mode.SUBTRACT)

        super().__init__(profile.sketch, rotation, align, mode)


class VSlot2020EndCap(BasePartObject):
    """
    An end cap for 2020 V-Slot rails.

    Holes are spaced 20 mm apart to align with tapped holes in the ends of
    the rails. The width and height are determined by the number of holes
    specified along each axis.

    :param thickness: Thickness of the end cap.
    :param num_x_holes: Number of holes (rails) along the X-axis.
    :param num_y_holes: Number of holes (rails) along the Y-axis.
    :param hole_radius: The radius of the holes for the bolts.
    :param corner_radius: Filet radius for the corners of the end cap.
    :param chamfer_size: Size of chamfer on top edges of the end cap.
    """

    def __init__(
        self,
        thickness: float,
        num_x_holes: int,
        num_y_holes: int,
        hole_radius: BoltSize | float,
        corner_radius: float = 0,
        chamfer_size: float = 0,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align3D = None,
        mode: Mode = Mode.ADD,
    ):
        with BuildPart() as plate:
            with BuildSketch():
                VSlot2020EndCapProfile(
                    num_x_holes,
                    num_y_holes,
                    hole_radius,
                    corner_radius,
                )
            extrude(amount=thickness)

            if chamfer_size > 0:
                chamfer(
                    plate.edges().filter_by(GeomType.LINE).group_by(Axis.Z)[-1],
                    chamfer_size,
                )

        super().__init__(plate.part, rotation, align, mode)


class BuildPlateProfile(BaseSketchObject):
    """
    A common build plate profile with a grid of mounting holes.

    Holes are spaced 10 mm apart. The width and height are determined by the
    number of holes specified along each axis. There is a 10 mm margin around
    the holes.

    :param num_x_holes: Number of holes along the X-axis.
    :param num_y_holes: Number of holes along the Y-axis.
    :param hole_radius: The radius of the holes for the bolts.
    :param corner_radius: Filet radius for the corners of the plate.
    """

    def __init__(
        self,
        num_x_holes: int,
        num_y_holes: int,
        hole_radius: BoltSize | float,
        corner_radius: float = 0,
        *,
        rotation: float = 0,
        align: Align2D = None,
        mode: Mode = Mode.ADD,
    ):
        if isinstance(hole_radius, BoltSize):
            hole_radius = hole_radius.value + HOLE_TOLERANCE

        width = 10 * (num_x_holes + 1)
        height = 10 * (num_y_holes + 1)

        with BuildSketch() as profile:
            (
                RectangleRounded(width, height, corner_radius)
                if corner_radius
                else Rectangle(width, height)
            )
            with GridLocations(10, 10, num_x_holes, num_y_holes):
                Circle(hole_radius, mode=Mode.SUBTRACT)

        super().__init__(profile.sketch, rotation, align, mode)


class BuildPlate(BasePartObject):
    """
    A common build plate with a grid of mounting holes.

    Holes are spaced 10 mm apart. The width and height are determined by the
    number of holes specified along each axis. There is a 10 mm margin around
    the holes.

    :param thickness: Thickness of the plate.
    :param num_x_holes: Number of holes along the X-axis.
    :param num_y_holes: Number of holes along the Y-axis.
    :param hole_radius: The radius of the holes for the bolts.
    :param corner_radius: Filet radius for the corners of the plate.
    """

    def __init__(
        self,
        thickness: float,
        num_x_holes: int,
        num_y_holes: int,
        hole_radius: BoltSize | float,
        corner_radius: float = 0,
        chamfer_size: float = 0,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align3D = None,
        mode: Mode = Mode.ADD,
    ):
        with BuildPart() as plate:
            with BuildSketch():
                BuildPlateProfile(
                    num_x_holes,
                    num_y_holes,
                    hole_radius,
                    corner_radius,
                )
            extrude(amount=thickness)

            if chamfer_size > 0:
                chamfer(
                    plate.edges().filter_by(GeomType.LINE).group_by(Axis.Z)[-1],
                    chamfer_size,
                )

        super().__init__(plate.part, rotation, align, mode)


class LPlate(BasePartObject):
    """
    An L-shaped plate (bracket) with a grid of mounting holes on each face.

    Holes are spaced 10 mm apart. The width and height are determined by the
    number of holes specified along each axis. There is a 10 mm margin around
    the holes.

    :param thickness: Thickness of the plate.
    :param num_x_holes: Number of holes along the X-axis.
    :param num_y_holes: Number of holes along the Y-axis.
    :param num_z_holes: Number of holes along the Z-axis.
    :param hole_radius: The radius of the holes for the bolts.
    :param corner_radius: Filet radius for the corners of the plate.
    """

    def __init__(
        self,
        thickness: float,
        num_x_holes: int,
        num_y_holes: int,
        num_z_holes: int,
        hole_radius: BoltSize | float,
        corner_radius: float = 0,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align3D = None,
        mode: Mode = Mode.ADD,
    ):
        if isinstance(hole_radius, BoltSize):
            hole_radius = hole_radius.value + HOLE_TOLERANCE

        with BuildPart() as plate:
            with BuildSketch(Plane.XY):
                BuildPlateProfile(
                    num_x_holes,
                    num_y_holes,
                    hole_radius,
                    corner_radius=0,
                    align=(Align.CENTER, Align.MIN),
                )
            with BuildSketch(Plane.XZ):
                BuildPlateProfile(
                    num_x_holes,
                    num_z_holes,
                    hole_radius,
                    corner_radius=0,
                    align=(Align.CENTER, Align.MIN),
                )
            extrude(amount=thickness)

            if corner_radius:
                fillet(
                    plate.edges().group_by(Axis.Z)[-1].filter_by(Axis.Y)
                    + plate.edges().group_by(Axis.Y)[-1].filter_by(Axis.Z),
                    corner_radius,
                )

        super().__init__(plate.part, rotation, align, mode)
