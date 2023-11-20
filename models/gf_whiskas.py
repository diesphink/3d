from ocp_vscode import show
from gridfinity.gridfinity_scoops import GridfinityBox
from sphlib import align, Dimensions, Slot, SlotPosition, SlotType
import gridfinity as gf

from build123d import Axis, Box

# === Dimensions
X, Y, Z = 0, 1, 2
d = Dimensions()
d.sachet = [96, 150, 140]


base = gf.GridfinityFilled(x_grid_number=3, y_grid_number=4, unit_height=22, disable_mholes=True)
slot = Box(*d.sachet)
base -= align(slot, ref=base, center="x", begin="y", end="z")
# slot = Slot(slot, SlotPosition.Y_AXIS_MIN, 25, SlotType.SPHERE)
# base -= align(slot, ref=base, center="xy", end="z", margin=0)
show(base)
# base.export_stl("library/gridfinity/wallet.stl")
# base.export_step("library/gridfinity/wallet.step")
