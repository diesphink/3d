# %%
from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults

set_port(3939)


from build123d import Cylinder, fillet, export_stl, Box, Axis
from ocp_vscode import show

import gridfinity as gf

# from gridfinity.gridfinity_scoops import GridfinityBox
from sphlib import Dimensions, Slot, SlotPosition, SlotType, align

# === Dimensions
X, Y, Z = 0, 1, 2
d = Dimensions()
d.cubo = [51, 51, 50]

# %%
base = gf.GridfinityFilled(x_grid_number=2, y_grid_number=2, unit_height=3, disable_mholes=True)
cubo = Box(*d.cubo)
cubo = fillet(cubo.edges(), 1)  # .rotate(axis=Axis.X, angle=45).rotate(axis=Axis.Y, angle=45)
base -= align(cubo, ref=base, center="xy", begin="z", margin=7)
show(base)


# %%
export_stl(base, "library/gridfinity/cubo.stl")
