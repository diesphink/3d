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

# %%
base = gf.GridfinityFilled(x_grid_number=1, y_grid_number=1, unit_height=4, disable_mholes=True)

d = Dimensions()
d.cubo = [50, 32, 25]
d.base = [25.5, 25.5, 3]
d.hook = [4, 50, 2]

cubo = Box(*d.cubo)
cubo += align(
    Box(d.base[X] - d.hook[X], d.hook[Y], d.bahookse[Z]), ref=cubo, center="x", begin="z", endToBegin="y", margin=0
)

# cubo = fillet(cubo.edges(), 1)  # .rotate(axis=Axis.X, angle=45).rotate(axis=Axis.Y, angle=45)
base -= align(cubo, ref=base, end="xyz", margin=0)

show(base)


# %%
export_stl(base, "library/gridfinity/cubo.stl")
