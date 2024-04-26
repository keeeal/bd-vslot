from typing import Union

from build123d import *

from bd_vslot.constants import BoltSize


class SlidingTNut(BasePartObject):
    def __init__(
        self,
        hole_radius: Union[BoltSize, float],
        rotation: RotationLike = (0, 0, 0),
        align: Union[Align, tuple[Align, Align, Align]] = Align.CENTER,
        mode: Mode = Mode.ADD,
    ):
        if isinstance(hole_radius, BoltSize):
            hole_radius = hole_radius.value + 0.05

        with BuildPart() as nut:
            with BuildSketch(Plane.YZ):
                with BuildLine():
                    Polyline(
                        (0, 4.5),
                        (3.1, 4.5),
                        (3.1, 3),
                        (4.75, 3),
                        (4.75, 2),
                        (2.75, 0),
                        (0, 0),
                    )
                    mirror(about=Plane.YZ)
                make_face()
            extrude(amount=4.75, both=True)
            Hole(hole_radius)

        super().__init__(nut.part, rotation, align, mode)
