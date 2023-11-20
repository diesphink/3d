from ocp_vscode import show

# from gridfinity.gridfinity_scoops import GridfinityBox
from cqgridfinity import GridfinityBox
from sphlib import align, Dimensions, Slot, SlotPosition, SlotType
import gridfinity as gf

from build123d import Axis, Box, Cylinder, fillet

# === Dimensions
X, Y, Z = 0, 1, 2
d = Dimensions()
d.humidifier = [104, 104, 220]

base = Box(1, 1, 1)
base.wrapped = GridfinityBox(length_u=3, width_u=3, height_u=10, holes=True, solid=True).render().objects[0].wrapped

slot = Box(*d.humidifier)
slot = fillet(slot.edges().filter_by(Axis.Z), 10)
base -= align(slot, ref=base, center="xy", begin="z", margin=7)
show(base)
base.export_stl("library/gridfinity/humidifier.stl")
base.export_step("library/gridfinity/humidifier.step")

# Compare this snippet from models/gf_pen2.py:
# from ocp_vscode import show
