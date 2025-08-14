# %%
from ocp_vscode import *
from sphlib import align, Dimensions, distribute, rescale_chamfer
from enum import Enum

from build123d import *

# === Dimensions
X, Y, Z = 0, 1, 2

d = Dimensions()
d.base_radius = 14 / 2
d.base_height = 3.3
d.pin_ext_radius = [9.6 / 2, 8.5 / 2]
d.pin_int_radius = [7.2 / 2, 6.2 / 2]
d.pin_height = 12
d.furo_radius = 1.5 / 2

base = Cylinder(radius=d.base_radius, height=d.base_height)
base = fillet(base.edges().sort_by(Axis.Z)[0], radius=0.5)

ellipse = Ellipse(x_radius=d.pin_ext_radius[X], y_radius=d.pin_ext_radius[Y])

pino = extrude(ellipse, amount=d.pin_height) - extrude(
    Ellipse(x_radius=d.pin_int_radius[X], y_radius=d.pin_int_radius[Y]), amount=d.pin_height
)

furo = Cylinder(radius=d.furo_radius, height=d.base_radius * 2).rotate(Axis.X, 90)
for i in range(3):
    pino = pino - align(furo, ref=pino, center="xy", centerToEnd="z", margins=[0, 0, (i + 1) * d.pin_height / 4])
# pino = pino - align(furo, ref=pino, center="xy", end="z", margins=[0, 0, d.base_height/4])


chinelo = base + align(pino, ref=base, center="xy", beginToEnd="z")
show(chinelo)

# d.bd = [59.3, 31.3, 6]
# d.folga = 0.2
# d.walls = 0.4
# d.cx = [dim + d.walls * 2 + d.folga for dim in d.bd[0:2]] + [d.bd[Z] + d.walls]

# print(d.cx)
# cx = Box(length=d.cx[X], width=d.cx[Y], height=d.cx[Z])
# cx -= align(Box(length=d.bd[X], width=d.bd[Y], height=d.bd[Z]), ref=cx, center="xy", end="z")
# show(cx)


export_stl(chinelo, "library/chinelo.stl")

# %%
