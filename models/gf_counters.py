# %%
from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)


from build123d import Box
from ocp_vscode import show

import gridfinity as gf

# from gridfinity.gridfinity_scoops import GridfinityBox
from sphlib import Dimensions, Slot, SlotPosition, SlotType, align

# === Dimensions
X, Y, Z = 0, 1, 2
d = Dimensions()
d.charger = [65, 95, 28]

# %%
# base = gf.GridfinityFilled(x_grid_number=1, y_grid_number=2, unit_height=3, disable_mholes=True)
# slot = Slot(Box(*d.charger), SlotPosition.Y_AXIS, 30, SlotType.SPHERE)
# base -= align(slot, ref=base, center="xy", end="z", margin=3.85)
show(Box(1,1,1))
# %%
# base.export_stl("library/gridfinity/battery/charger.stl")
# base.export_step("library/gridfinity/battery/charger.step")
