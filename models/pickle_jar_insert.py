from cadquery import Location
from ocp_vscode import show

from sphlib import Dimensions
import gridfinity as gf

from build123d import (
    Axis,
    BuildPart,
    BuildSketch,
    Circle,
    Mode,
    extrude,
)

# === Dimensions
X, Y, Z = 0, 1, 2
d = Dimensions()
d.jar_radius = 86 / 2
d.wall_size = 1.2
d.wall_height = 10

with BuildPart() as insert:
    with BuildSketch() as sk:
        Circle(d.jar_radius)
    extrude(amount=d.wall_size + d.wall_height)

    with BuildSketch(insert.faces().sort_by(Axis.Z)[-1]) as sk2:
        Circle(d.jar_radius - d.wall_size)

    extrude(amount=-d.wall_height, mode=Mode.SUBTRACT)

    show(insert)


insert.part.export_stl("library/picke_jar_insert.stl")
insert.part.export_step("library/picke_jar_insert.step")
