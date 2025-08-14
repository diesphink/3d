# %%
from ocp_vscode import *
from sphlib import align, Dimensions, distribute, rescale_chamfer
from enum import Enum

from build123d import *

# === Dimensions
X, Y, Z = 0, 1, 2

d = Dimensions()

d.gaveta = [325, 215, 30]
d.paredes = 2
d.radius = 2
d.corner = 20
d.slot1 = d.slot2 = [90, 170, 30]
d.slot3 = [64, 170, 30]
d.slot4 = [80, 215, 30]
d.slot5 = [241, 45, 15]

d.slot6 = [95, 150, 30]
d.slot7 = [120, 150, 30]
d.slot8 = [100, 215, 30]
d.slot9 = [224, 65, 15]

corner = extrude(make_face(Plane.XY * Polyline([(0, 0), (d.corner, 0), (0, d.corner), (0, 0)])), amount=d.gaveta[Z])

slot1 = Box(length=d.slot1[X], width=d.slot1[Y], height=d.slot1[Z])
slot1 = fillet(slot1.edges().group_by(Axis.Z)[0:2], radius=d.radius)
slot1 = slot1 - align(
    fillet(
        Box(length=d.slot1[X] - 2 * d.paredes, width=d.slot1[Y] - d.paredes + d.radius, height=d.slot1[Z] - d.paredes)
        .edges()
        .group_by(Axis.Z)[0:2],
        radius=d.radius,
    ),
    ref=slot1,
    center="x",
    end="zy",
    margins=[0, d.radius, 0],
)

slot1 = slot1 - align(
    corner.rotate(Axis.Z, -90),
    ref=slot1,
    begin="x",
    end="yz",
)

# show(slot1)

export_stl(slot1, "library/slot1.stl")

slot2 = Box(length=d.slot2[X], width=d.slot2[Y], height=d.slot2[Z])
slot2 = fillet(slot2.edges().group_by(Axis.Z)[0:2], radius=d.radius)
slot2 = slot2 - align(
    fillet(
        Box(length=d.slot2[X] - 2 * d.paredes, width=d.slot2[Y] - d.paredes + d.radius, height=d.slot2[Z] - d.paredes)
        .edges()
        .group_by(Axis.Z)[0:2],
        radius=d.radius,
    ),
    ref=slot2,
    center="x",
    end="zy",
    margins=[0, d.radius, 0],
)

# show(slot2)

export_stl(slot2, "library/slot2.stl")

slot3 = Box(length=d.slot3[X], width=d.slot3[Y], height=d.slot3[Z])
slot3 = fillet(slot3.edges().group_by(Axis.Z)[0:2], radius=d.radius)
slot3 = slot3 - align(
    fillet(
        Box(length=d.slot3[X] - 2 * d.paredes, width=d.slot3[Y] - d.paredes + d.radius, height=d.slot3[Z] - d.paredes)
        .edges()
        .group_by(Axis.Z)[0:2],
        radius=d.radius,
    ),
    ref=slot3,
    center="x",
    end="zy",
    margins=[0, d.radius, 0],
)

# show(slot3)

export_stl(slot3, "library/slot3.stl")


slot4 = Box(length=d.slot4[X], width=d.slot4[Y], height=d.slot4[Z])
slot4 = fillet(slot4.edges().group_by(Axis.Z)[0:2], radius=d.radius)
slot4 = slot4 - align(
    fillet(
        Box(length=d.slot4[X] - 2 * d.paredes, width=d.slot4[Y] - 2 * d.paredes, height=d.slot4[Z] - d.paredes)
        .edges()
        .group_by(Axis.Z)[0:2],
        radius=d.radius,
    ),
    ref=slot4,
    center="xy",
    end="z",
)

slot4 = slot4 - align(
    corner.rotate(Axis.Z, -180),
    ref=slot4,
    begin="",
    end="xyz",
)

slot4 = slot4 - align(
    corner.rotate(Axis.Z, 90),
    ref=slot4,
    begin="y",
    end="xz",
)

# show(slot4)

export_stl(slot4, "library/slot4.stl")


slot5 = Box(length=d.slot5[X], width=d.slot5[Y], height=d.slot5[Z])
slot5 = fillet(slot5.edges().group_by(Axis.Z)[0:2], radius=d.radius)
slot5 = slot5 - align(
    fillet(
        Box(length=d.slot5[X] - 2 * d.paredes, width=d.slot5[Y] - 2 * d.paredes, height=d.slot5[Z] - d.paredes)
        .edges()
        .group_by(Axis.Z)[0:2],
        radius=d.slot5[Z] - d.paredes - 0.1,
    ),
    ref=slot5,
    center="xy",
    end="z",
)

slot5 = slot5 - align(
    corner.rotate(Axis.Z, 0),
    ref=slot5,
    begin="xyz",
)


# show(slot5)

export_stl(slot5, "library/slot5.stl")


slot6 = Box(length=d.slot6[X], width=d.slot6[Y], height=d.slot6[Z])
slot6 = fillet(slot6.edges().group_by(Axis.Z)[0:2], radius=d.radius)
slot6 = slot6 - align(
    fillet(
        Box(length=d.slot6[X] - 2 * d.paredes, width=d.slot6[Y] - d.paredes + d.radius, height=d.slot6[Z] - d.paredes)
        .edges()
        .group_by(Axis.Z)[0:2],
        radius=d.radius,
    ),
    ref=slot6,
    center="x",
    end="zy",
    margins=[0, d.radius, 0],
)

slot6 = slot6 - align(
    corner.rotate(Axis.Z, -90),
    ref=slot6,
    begin="x",
    end="yz",
)

# show(slot6)

export_stl(slot6, "library/slot6.stl")


slot7 = Box(length=d.slot7[X], width=d.slot7[Y], height=d.slot7[Z])
slot7 = fillet(slot7.edges().group_by(Axis.Z)[0:2], radius=d.radius)
slot7 = slot7 - align(
    fillet(
        Box(length=d.slot7[X] - 2 * d.paredes, width=d.slot7[Y] - d.paredes + d.radius, height=d.slot7[Z] - d.paredes)
        .edges()
        .group_by(Axis.Z)[0:2],
        radius=d.radius,
    ),
    ref=slot7,
    center="x",
    end="zy",
    margins=[0, d.radius, 0],
)

# show(slot7)

export_stl(slot7, "library/slot7.stl")


slot8 = Box(length=d.slot8[X], width=d.slot8[Y], height=d.slot8[Z])
slot8 = fillet(slot8.edges().group_by(Axis.Z)[0:2], radius=d.radius)
slot8 = slot8 - align(
    fillet(
        Box(length=d.slot8[X] - 2 * d.paredes, width=d.slot8[Y] - 2 * d.paredes, height=d.slot8[Z] - d.paredes)
        .edges()
        .group_by(Axis.Z)[0:2],
        radius=d.radius,
    ),
    ref=slot8,
    center="xy",
    end="z",
)

slot8 = slot8 - align(
    corner.rotate(Axis.Z, -180),
    ref=slot8,
    begin="",
    end="xyz",
)

slot8 = slot8 - align(
    corner.rotate(Axis.Z, 90),
    ref=slot8,
    begin="y",
    end="xz",
)

# show(slot8)

export_stl(slot8, "library/slot8.stl")


slot9 = Box(length=d.slot9[X], width=d.slot9[Y], height=d.slot9[Z])
slot9 = fillet(slot9.edges().group_by(Axis.Z)[0:2], radius=d.radius)
slot9 = slot9 - align(
    fillet(
        Box(length=d.slot9[X] - 2 * d.paredes, width=d.slot9[Y] - 2 * d.paredes, height=d.slot9[Z] - d.paredes)
        .edges()
        .group_by(Axis.Z)[0:2],
        radius=d.slot9[Z] - d.paredes - 0.1,
    ),
    ref=slot9,
    center="xy",
    end="z",
)

slot9 = slot9 - align(
    corner.rotate(Axis.Z, 0),
    ref=slot9,
    begin="xyz",
)


show(slot9)

export_stl(slot9, "library/slot9.stl")
