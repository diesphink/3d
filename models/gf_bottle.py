from ocp_vscode import show

# from gridfinity.gridfinity_scoops import GridfinityBox
from cqgridfinity import GridfinityBox
from sphlib import align, Dimensions, Slot, SlotPosition, SlotType
import gridfinity as gf

from build123d import Axis, Box, Cylinder

# === Dimensions
X, Y, Z = 0, 1, 2
d = Dimensions()
d.bottle_radius = 70 / 2
d.bottle_height = 60

base = Box(1, 1, 1)
base.wrapped = GridfinityBox(length_u=2, width_u=2, height_u=8, holes=True, solid=True).render().objects[0].wrapped


slot = Cylinder(radius=d.bottle_radius, height=d.bottle_height)
base -= align(slot, ref=base, center="xy", begin="z", margin=7)
show(base)
base.export_stl("library/gridfinity/bottle.stl")
base.export_step("library/gridfinity/bottle.step")

# Compare this snippet from models/gf_pen2.py:
# from ocp_vscode import show
