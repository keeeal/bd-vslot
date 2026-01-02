from build123d import *

from bd_vslot.constants import HOLE_TOLERANCE, BoltSize
from bd_vslot.utils.typing import Align3D


class VSlot2020SlidingTNut(BasePartObject):
    """
    Sliding T-nut compatible with 2020 V-Slot rails.

    Args:
        hole_radius (BoltSize | float): The radius of the hole for the bolt.
    """

    def __init__(
        self,
        hole_radius: BoltSize | float,
        *,
        rotation: RotationLike = (0, 0, 0),
        align: Align3D = None,
        mode: Mode = Mode.ADD,
    ):
        if isinstance(hole_radius, BoltSize):
            hole_radius = hole_radius.value + HOLE_TOLERANCE

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
