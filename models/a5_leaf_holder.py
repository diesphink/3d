from ocp_vscode import show

# from gridfinity.gridfinity_scoops import GridfinityBox
from cqgridfinity import GridfinityBox
from sphlib import align, Dimensions, Slot, SlotPosition, SlotType
import gridfinity as gf

from build123d import (
    Axis,
    Bezier,
    Box,
    BuildLine,
    BuildPart,
    BuildSketch,
    Circle,
    Cylinder,
    Line,
    Locations,
    Mode,
    SlotCenterToCenter,
    Spline,
    extrude,
    make_face,
    offset,
)

# === Dimensions
X, Y, Z = 0, 1, 2
d = Dimensions()
d.a5 = [210, 148]
d.box = [220, 160, 16]
d.spline.width = 120
d.spline.smaller_width = 80
d.spline.deep = 30
d.walls = 1.6
d.slots = d.box[X] - 20, 5
d.tolerance = 0.6

slot_locations = [(0, -d.a5[Y] / 3), (0, d.a5[Y] / 3), (0, 0)]
# slot_locations = [(0, 0)]

# Test
# d.box[X] = 40
# d.box[Y] = 30
# d.slots = 20, 5
# d.spline.width = 5
# d.spline.smaller_width = 3
# slot_locations = (0, 0)
# d.spline.deep = 10


sPnts = [
    ((d.box[X] - d.spline.width) / 2, d.box[Y]),
    ((d.box[X] - d.spline.smaller_width) / 2, d.box[Y]),
    ((d.box[X] - d.spline.smaller_width) / 2, d.box[Y] - d.spline.deep),
    ((d.box[X] + d.spline.smaller_width) / 2, d.box[Y] - d.spline.deep),
    ((d.box[X] + d.spline.smaller_width) / 2, d.box[Y]),
    ((d.box[X] + d.spline.width) / 2, d.box[Y]),
]

with BuildPart() as ex12:
    with BuildSketch() as ex12_sk:
        with BuildLine() as ex12_ln:
            l1 = Line((0, d.box[Y]), sPnts[0])
            l1 = Bezier(*sPnts)

            l2 = Line(sPnts[-1], (d.box[X], d.box[Y]))

            l2 = Line((d.box[X], d.box[Y]), (d.box[X], 0))
            l3 = Line((d.box[X], 0), (0, 0))
            l4 = Line((0, 0), (0, d.box[Y]))
            # show(l1, l2, l3, l4)
            show(ex12_ln)
        make_face()

    extrude(amount=d.box[Z])
    faces = [ex12.faces()[0], ex12.faces()[1], ex12.faces()[2]]
    offset(amount=-d.walls, openings=faces)

    with BuildSketch(ex12.faces().sort_by(Axis.Z).last) as sk2:
        with Locations(*slot_locations):
            SlotCenterToCenter(*d.slots)

    extrude(amount=-d.walls / 2, mode=Mode.SUBTRACT)

    with BuildSketch(ex12.faces().sort_by(Axis.Z).first) as sk3:
        with Locations(*slot_locations):
            SlotCenterToCenter(*d.slots)
        offset(amount=-0.6)
    extrude(amount=d.walls / 2, mode=Mode.ADD)

    # show(ex12)


show(ex12)
ex12.part.export_stl("library/a5_leaf_holder.stl")
ex12.part.export_step("library/a5_leaf_holder.step")

# Compare this snippet from models/gf_pen2.py:
# from ocp_vscode import show
