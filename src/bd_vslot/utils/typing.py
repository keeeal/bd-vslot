from build123d.build_enums import Align

# Type aliases for the alignment options used to initialize Build123d's
# BaseSketchObject and BasePartObject classes.
Align2D = Align | tuple[Align, Align] | None
Align3D = Align | tuple[Align, Align, Align] | None
