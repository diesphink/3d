# %%
from ocp_vscode import *
from sphlib import align, Dimensions, distribute, rescale_chamfer
from enum import Enum

from build123d import *

# === Dimensions
X, Y, Z = 0, 1, 2

# d = Dimensions()
# d.bd = [59.3, 31.3, 6]
# d.folga = 0.2
# d.walls = 0.4
# d.cx = [dim + d.walls * 2 + d.folga for dim in d.bd[0:2]] + [d.bd[Z] + d.walls]

# print(d.cx)
# cx = Box(length=d.cx[X], width=d.cx[Y], height=d.cx[Z])
# cx -= align(Box(length=d.bd[X], width=d.bd[Y], height=d.bd[Z]), ref=cx, center="xy", end="z")
# show(cx)


tubo = Cylinder(radius=17.5 / 2, height=200)
tubo = tubo.rotate(Axis.X, 90)
tubo = split(tubo, bisect_by=Plane.XY.offset(-7), keep=Keep.TOP)

show(tubo)

# export_stl(tubo, "library/tubo.stl")

# %%
importer = Mesher()
a = importer.read("/home/sphink/Downloads/RR-933-Level Grid 3X3.stl")
show(a)
