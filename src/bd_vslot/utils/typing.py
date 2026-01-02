from build123d.build_enums import Align

Align2D = Align | tuple[Align, Align] | None
Align3D = Align | tuple[Align, Align, Align] | None
