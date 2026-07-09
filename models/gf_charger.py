# %%
from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults

set_port(3939)


from build123d import Box, fillet, export_stl
from ocp_vscode import show

import gridfinity as gf

# from gridfinity.gridfinity_scoops import GridfinityBox
from sphlib import Dimensions, Slot, SlotPosition, SlotType, align

# === Dimensions
X, Y, Z = 0, 1, 2
d = Dimensions()
d.charger = [102, 72.5, 35]
d.abert1 = 25
d.abert2 = 63

# %%
base = gf.GridfinityFilled(x_grid_number=3, y_grid_number=2, unit_height=6, disable_mholes=True)
charger = Box(*d.charger)
charger = align(charger, ref=base, center="xy", end="z", margin=3.85)
charger += align(Box(122, d.abert1, 30), ref=charger, center="y", end="xz")
charger += align(Box(122, d.abert2, 30), ref=charger, center="y", begin="x", end="z", margins=[20, 0, 0])
charger = fillet(charger.edges(), 1)
show(charger)
slot = Slot(charger, SlotPosition.Y_AXIS, 30, SlotType.SPHERE)
base -= align(slot, ref=base, center="xy", end="z")
show(base)


# %%
export_stl(base, "library/gridfinity/charger.stl")
