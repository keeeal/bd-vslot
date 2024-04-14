from cadquery import Sketch, Workplane
from cadquery.types import Real


def _vslot(sketch: Sketch, a: Real = 0) -> Sketch:
    return (
        sketch.parray(5.23, a, 0, 1)
        .trapezoid(11, 2.66, 45, angle=90, mode="s")
        .parray(2.15, a, 0, 1, rotate=False)
        .rect(11, 1.64, angle=90, mode="s")
        .rect(6.25, 6, angle=90, mode="s")
        .parray(1.8925, a, 0, 1, rotate=False)
        .trapezoid(9.16, 1.455, 45, angle=90, mode="s")
    )


def profile(n: int = 1) -> Sketch:
    sketch = Sketch().rect(20 * n, 20).vertices().fillet(0.5)
    sketch = _vslot(sketch.reset().parray(10 * (n - 1), 0, 0, 1), a=0)
    sketch = _vslot(sketch.reset().parray(10 * (1 - n), 0, 0, 1), a=180)
    sketch = sketch.reset().rarray(20, 20, n, 1).circle(2.1, mode="s")
    sketch = _vslot(sketch.reset().rarray(20, 20, n, 1), a=90)
    sketch = _vslot(sketch.reset().rarray(20, 20, n, 1), a=270)

    if n > 1:
        sketch = (
            sketch.reset()
            .rarray(20, 20, n - 1, 1)
            .rect(5.4, 16.4, mode="s")
            .parray(10 - 7.8 / 2 - 2, 0, 180, 2)
            .trapezoid(13.68, 4, 45, angle=270, mode="s")
        )

    return sketch


def extrusion(length: Real, n: int = 1) -> Workplane:
    return Workplane().placeSketch(profile(n)).extrude(length)
