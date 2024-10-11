# %%
# %cd /home/sphink/devel/3d
from ocp_vscode import *
from sphlib import align, Dimensions, Slot, SlotPosition, SlotType
import gridfinity as gf
import math

from build123d import *

# === Dimensions
X, Y, Z = 0, 1, 2

# %%
d = Dimensions()
d.diametro = 23
d.wall = 3

base = Cylinder(d.diametro, d.wall)



show(ex8)

export_stl(ex8, "library/vassoura.stl")
