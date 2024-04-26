from __future__ import annotations

from typing import Union

from build123d import *

from bd_vslot.constants import BoltSize


class BuildPlateProfile(BaseSketchObject):
    def __init__(
        self,
        num_x_holes: int,
        num_y_holes: int,
        hole_radius: Union[BoltSize, float],
        corner_radius: float = 0,
        rotation: float = 0,
        align: Union[Align, tuple[Align, Align]] = Align.CENTER,
        mode: Mode = Mode.ADD,
    ):
        if isinstance(hole_radius, BoltSize):
            hole_radius = hole_radius.value + 0.05

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
        hole_radius: Union[BoltSize, float],
        corner_radius: float = 3,
        rotation: RotationLike = (0, 0, 0),
        align: Union[Align, tuple[Align, Align, Align]] = Align.CENTER,
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
        hole_radius: Union[BoltSize, float],
        corner_radius: float = 0,
        rotation: RotationLike = (0, 0, 0),
        align: Union[Align, tuple[Align, Align, Align]] = (
            Align.CENTER,
            Align.MIN,
            Align.MIN,
        ),
        mode: Mode = Mode.ADD,
    ):
        if isinstance(hole_radius, BoltSize):
            hole_radius = hole_radius.value + 0.05

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
