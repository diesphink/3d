# %%
from ocp_vscode import *
from sphlib import align, Dimensions, distribute, rescale_chamfer
from enum import Enum

from build123d import *

# === Dimensions
X, Y, Z = 0, 1, 2

d = Dimensions()
d.abertura = [77, 90, 80]

d.madeira = 16

d.fillet_radius = 50
d.wall = 3
d.furo = 1.5  # radius

d.lid = [10, 10, 3]

abertura = Box(d.abertura[X], d.abertura[Y], d.abertura[Z] + d.madeira + d.lid[Z])
abertura = fillet(abertura.edges().group_by(Axis.Z)[-1].sort_by(Axis.Y)[0], d.fillet_radius)

lid = Box(d.abertura[X] + 2 * d.lid[X], d.abertura[Y] + d.lid[Y], d.lid[Z])
lid = align(lid, ref=abertura, center="x", begin="z", end="y")
lid = lid - abertura

furo = Cylinder(radius=d.furo, height=d.lid[Z])
lid -= align(furo, ref=lid, centerToEnd="xy", begin="z", margins=[5, 5, 0])
lid -= align(furo, ref=lid, centerToEnd="y", centerToBegin="x", begin="z", margins=[5, 5, 0])
lid -= align(furo, ref=lid, centerToEnd="x", centerToBegin="y", begin="z", margins=[5, 5, 0])
lid -= align(furo, ref=lid, centerToBegin="xy", begin="z", margins=[5, 5, 0])

bottom_face = abertura.faces().filter_by(Axis.Z, 0)[0]
back_face = abertura.faces().filter_by(Axis.Y, 0)[-1]

abertura = offset(abertura, amount=-d.wall, openings=(bottom_face, back_face))
# show(lid, abertura)

export_stl(lid + abertura, "library/pia_abertura.stl")
