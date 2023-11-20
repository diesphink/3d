from ocp_vscode import show

# from gridfinity.gridfinity_scoops import GridfinityBox
from cqgridfinity import GridfinitySolidBox
from sphlib import align, Dimensions, Slot, SlotPosition, SlotType
import gridfinity as gf

from build123d import Axis, Box, Cylinder

# === Dimensions
X, Y, Z = 0, 1, 2
d = Dimensions()
d.pen_radius = 5.5
d.pen_height = 58

base = gf.GridfinityFilled(x_grid_number=1, y_grid_number=1, unit_height=8)
slot = Cylinder(radius=d.pen_radius, height=d.pen_height)
base -= align(slot, ref=base, center="xy", end="z", margin=0)
show(base)
base.export_stl("library/gridfinity/single_pen.stl")
base.export_step("library/gridfinity/single_pen.step")
