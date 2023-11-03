from ocp_vscode import show
from gridfinity.gridfinity_scoops import GridfinityBox
from sphlib import align, Dimensions, Slot, SlotPosition, SlotType
import gridfinity as gf

from build123d import (
    Box,
    Circle,
    Locations,
    Rectangle,
    Sketch,
    extrude,
    make_hull,
)

# === Dimensions
X, Y, Z = 0, 1, 2
d = Dimensions()
d.magnet.diameter = 10.25
d.magnet.deep = 2.2
d.magnet.distance = [33.5, 56.236]
d.magnet.separation = 0.7

d.box = [72, 92, 102.5]

d.border = 3

d.tape = [13, d.magnet.diameter + d.magnet.distance[Y], 1.2]

d.strip = [
    d.tape[X] + d.border * 2,
    d.tape[Y] + d.border * 2,
    d.magnet.separation + d.magnet.deep,
]


magnet_locations = Locations(
    (0, 0), (0, d.magnet.distance[Y]), (d.magnet.distance[X], 0), (d.magnet.distance[X], d.magnet.distance[Y])
)

sketch = [loc * Circle((d.magnet.diameter / 2) + d.border) for loc in magnet_locations]
sketch = make_hull(sketch[0].edges() + sketch[2].edges()) + make_hull(sketch[1].edges() + sketch[3].edges())
sketch += align(Rectangle(d.strip[X], d.strip[Y]), ref=sketch, center="xy")

base = extrude(sketch, d.strip[Z])

sketch = Sketch()
sketch += [loc * Circle((d.magnet.diameter / 2)) for loc in magnet_locations]
base -= align(extrude(sketch, d.magnet.deep), ref=base, end="z", center="xy")

base -= align(Box(*d.tape), ref=base, end="z", center="xy")

show(base)
