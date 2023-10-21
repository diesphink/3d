from ocp_vscode import show
from gridfinity.gridfinity_scoops import GridfinityBox
from sphlib import align, Dimensions, Slot, SlotPosition, SlotType
import gridfinity as gf

from build123d import Box

# === Dimensions
X, Y, Z = 0, 1, 2
d = Dimensions()
d.charger = [65, 95, 28]


base = gf.GridfinityFilled(x_grid_number=2, y_grid_number=3, unit_height=5, disable_mholes=True)
slot = Slot(Box(*d.charger), SlotPosition.Y_AXIS, 30, SlotType.SPHERE)
base -= align(slot, ref=base, center="xy", end="z", margin=3.85)
# show(base)

show(
    GridfinityBox(
        x_grid_number=3,
        y_grid_number=3,
        y_divider_number=2,
        x_divider_number=2,
        unit_height=5,
        disable_mholes=True,
        disable_scoops=True,
    )
)

base.export_stl("library/gridfinity/battery/charger.stl")
