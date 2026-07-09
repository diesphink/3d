# %%
from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults

set_port(3939)


from build123d import Cylinder, fillet, export_stl
from ocp_vscode import show

import gridfinity as gf

# from gridfinity.gridfinity_scoops import GridfinityBox
from sphlib import Dimensions, Slot, SlotPosition, SlotType, align

# === Dimensions
X, Y, Z = 0, 1, 2
d = Dimensions()
# d.vitaminas = 56

# %%
base = gf.GridfinityFilled(x_grid_number=3, y_grid_number=2, unit_height=2, disable_mholes=True)


# base -= align(Cylinder(radius=d.vitaminas / 2, height=25), ref=base, center="xy", end="z")
show(base)


# %%
export_stl(base, "library/gridfinity/cabos.stl")
