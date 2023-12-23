from cadquery import Location
from ocp_vscode import show

from sphlib import Dimensions, align
import gridfinity as gf

from build123d import (
    Axis,
    Box,
    BuildPart,
    BuildSketch,
    Circle,
    Mode,
    Rectangle,
    chamfer,
    extrude,
    fillet,
)

from sphlib.slots import FingerSlot, Slot, SlotPosition, SlotType

# === Dimensions
X, Y, Z = 0, 1, 2
d = Dimensions()
d.fillet.big = 15
d.fillet.small = 3
d.fillet.top = 2
d.size = [190, 50, 22]
d.handle = [115, 60, 22]


base = gf.GridfinityFilled(x_grid_number=5, y_grid_number=2, unit_height=4, disable_mholes=True)
slot1 = Box(*d.size)
slot1 = fillet(slot1.edges().filter_by(Axis.Z), d.fillet.big)

slot2 = Box(*d.handle)
slot2 = fillet(slot2.edges().filter_by(Axis.Z), d.fillet.small)
slot2 = align(slot2, ref=slot1, center="y", end="xz", margin=0)

edges_base = base.edges()
# print(edges_base)

slot = Slot(slot1 + slot2, SlotPosition.Y_AXIS_MIN, 25, SlotType.SPHERE)
base -= align(slot, ref=base, center="xy", end="z", margins=[0, 0, 3.85])

new_edges = base.edges() - edges_base
new_edges = new_edges.group_by(Axis.Z)[-1]
print(new_edges)
base = chamfer(new_edges, length=d.fillet.top)

show(base)


# base = gf.GridfinityFilled(x_grid_number=7, y_grid_number=3, unit_height=5, disable_mholes=True)
# slot1 = Box(*d.size)
# slot1 = fillet(slot1.edges().filter_by(Axis.Z), d.fillet.big)

# slot2 = Box(*d.handle)
# slot2 = fillet(slot2.edges().filter_by(Axis.Z), d.fillet.small)
# slot2 = align(slot2, ref=slot1, center="y", end="xz", margin=0)

# slot = Slot(slot1 + slot2, SlotPosition.Y_AXIS_MIN, 25, SlotType.SPHERE)
# base -= align(slot, ref=base, begin="x", center="y", end="z", margins=[2, 0, 3.85])

# slot3 = Box(104, 107, 28)
# slot3 = fillet(slot3.edges().filter_by(Axis.Z), d.fillet.small)
# slot = Slot(slot3, SlotPosition.Y_AXIS_MIN, 25, SlotType.SPHERE)

# base -= align(slot, ref=base, center="y", end="xz", margins=[2, 0, 3.85])

# show(base)

base.export_stl("library/gridfinity/gf_rj45.stl")
base.export_step("library/gridfinity/gf_rj45.step")
