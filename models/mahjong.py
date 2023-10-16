from ocp_vscode import show
from sphlib import Dimensions, align

from build123d import (
    Align,
    Axis,
    Box,
    Circle,
    Location,
    Locations,
    Plane,
    Rectangle,
    Sketch,
    Sphere,
    chamfer,
    extrude,
    fillet,
)

# === Dimensions
X, Y, Z = 0, 1, 2

d = Dimensions()

d.tile = [38, 28, 20]
d.qtd_tiles = [5, 6, 5]

d.spacer.size = [20, 167.51, 98]
d.spacer.corner_diam = 7.5
d.spacer.finger_well = 20
d.spacer.tile_space = d.spacer.size[Y] / d.qtd_tiles[Y]

d.slots.size.upper = [d.tile[X] + d.spacer.size[X], d.tile[Y] * 4, d.tile[Z]]
d.slots.fillet_radius = 2
d.slots.size.lower = [d.tile[X] + d.spacer.size[X], d.tile[Y] * 2 - d.slots.fillet_radius, d.tile[Z]]

d.dice.big = [24, 24, 24]
d.dice.small = [31, 16, 16]

# === Spacer
spacer = Plane.XY * Rectangle(*d.spacer.size[0:2], align=Align.MIN)

finger_well = Circle(d.spacer.finger_well / 2)
finger_well += Location((-d.spacer.finger_well / 2, 0)) * Rectangle(d.spacer.finger_well, d.spacer.finger_well)

for i in range(6):
    spacer -= Locations((8, d.spacer.tile_space * i + d.spacer.tile_space / 2)) * finger_well

spacer = fillet(spacer.vertices().group_by(Axis.X)[2], d.spacer.corner_diam / 2)
spacer = fillet(spacer.vertices().group_by(Axis.X)[0][1:13], 3)

spacer = extrude(spacer, d.spacer.size[Z])

slots = Box(*d.slots.size.upper)
slots += align(Box(*d.slots.size.lower), ref=slots, endToBegin="z")

spacer -= align(slots, ref=spacer, center="xy", end="z")

show(spacer)

spacer.export_stl("library/mahjong/spacer.stl")

# === Slots
slots = Box(*d.slots.size.upper)
slots += align(Box(*d.slots.size.lower), ref=slots, endToBegin="z")
slots = fillet(slots.edges(), d.slots.fillet_radius)


def make_slot(dim) -> Box:
    tolerance = 1
    slot = Box(dim[0] + tolerance, dim[1] + tolerance, dim[2] + tolerance)
    slot += align(
        Sphere((dim[Y] + tolerance) / 2),
        ref=slot,
        centerToBegin="x",
        center="y",
        centerToEnd="z",
        margins=[0, 0, tolerance],
    ) + align(
        Sphere((dim[Y] + tolerance) / 2),
        ref=slot,
        centerToEnd="xz",
        center="y",
        margins=[0, 0, tolerance],
    )
    return slot


# big_die_slot = Box(*d.dice.big)

# big_die_slot += align(
# Sphere(d.dice.big[0] / 2), ref=big_die_slot, centerToBegin="x", center="y", centerToEnd="z"
# ) + align(Sphere(d.dice.big[0] / 2), ref=big_die_slot, centerToEnd="xz", center="y")
# big_die = Box(*d.dice.big, rotation=(0, 45, 45))


slots -= align(make_slot(d.dice.big), ref=slots, center="xy", end="z", margins=[0, 0, -d.dice.big[Y] / 2 - 1])
slots -= align(
    make_slot(d.dice.small),
    ref=slots,
    begin="y",
    center="x",
    end="z",
    margins=[0, 10, -d.dice.small[Y] / 2 - 1],
)
slots -= align(make_slot(d.tile), ref=slots, center="x", end="zy", margins=[0, 10, -d.tile[Y] / 2 - 1])
slots.export_stl("library/mahjong/slots.stl")
