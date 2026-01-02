from __future__ import annotations

from build123d import *

from bd_vslot.constants import HOLE_TOLERANCE, BoltSize
from bd_vslot.utils.typing import Align2D, Align3D


class VSlot2020EndCapProfile(BaseSketchObject):
    def __init__(
        self,
        num_x_holes: int,
        num_y_holes: int,
        hole_radius: BoltSize | float,
        corner_radius: float = 0,
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
    def __init__(
        self,
        thickness: float,
        num_x_holes: int,
        num_y_holes: int,
        hole_radius: BoltSize | float,
        corner_radius: float = 0,
        chamfer_size: float | None = None,
        rotation: RotationLike = (0, 0, 0),
        align: Align3D = None,
        mode: Mode = Mode.ADD,
    ):
        if chamfer_size is None:
            chamfer_size = min(thickness / 2, 1.0)

        with BuildPart() as plate:
            with BuildSketch():
                VSlot2020EndCapProfile(
                    num_x_holes,
                    num_y_holes,
                    hole_radius,
                    corner_radius,
                )
            extrude(amount=thickness)
            chamfer(
                plate.edges().filter_by(GeomType.LINE).group_by(Axis.Z)[-1],
                chamfer_size,
            )

        super().__init__(plate.part, rotation, align, mode)


class BuildPlateProfile(BaseSketchObject):
    def __init__(
        self,
        num_x_holes: int,
        num_y_holes: int,
        hole_radius: BoltSize | float,
        corner_radius: float = 0,
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
    def __init__(
        self,
        thickness: float,
        num_x_holes: int,
        num_y_holes: int,
        hole_radius: BoltSize | float,
        corner_radius: float = 0,
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

        super().__init__(plate.part, rotation, align, mode)


class LPlate(BasePartObject):
    def __init__(
        self,
        thickness: float,
        num_x_holes: int,
        num_y_holes: int,
        num_z_holes: int,
        hole_radius: BoltSize | float,
        corner_radius: float = 0,
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
