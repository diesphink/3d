# from attrdict import AttrDict
from math import sqrt
from ocp_vscode import show
from sphlib import Dimensions

from build123d import (
    Axis,
    BasePartObject,
    Locations,
    Part,
    Pos,
    RegularPolygon,
    chamfer,
    extrude,
)


d = Dimensions()
d.pin.top.side = 7.5
d.pin.top.height = 10
d.pin.top.chamfer = 0.5

d.pin.bottom.side = 9.815
d.pin.bottom.height = 2

d.distance_between = 23.6

d.space_x = d.distance_between
d.space_y = d.distance_between * sqrt(3) / 2
d.space_offset = d.distance_between / 2


def _location_grid(pins_per_row=[1]):
    loc = []
    for row, pins in enumerate(pins_per_row):
        for pin in range(pins):
            loc.append((pin * d.space_x - (d.space_offset if row % 2 == 0 else 0), row * d.space_y))
    return Locations(*loc)


class HoneycombPin(BasePartObject):
    def __init__(self, **kwargs):
        bottom_hexa = RegularPolygon(radius=d.pin.bottom.side, side_count=6, rotation=90)
        pin = extrude(bottom_hexa, amount=d.pin.bottom.height)

        top_hexa = RegularPolygon(radius=d.pin.top.side, side_count=6, rotation=90)
        pin += extrude(Pos(0, 0, d.pin.bottom.height) * top_hexa, amount=d.pin.top.height)
        pin = chamfer(pin.edges().group_by(Axis.Z)[-1], length=d.pin.top.chamfer)

        super().__init__(part=pin, **kwargs)


class HoneycombGrid(BasePartObject):
    def __init__(self, pins_per_row=[1], **kwargs):
        grid = sum(_location_grid(pins_per_row) * HoneycombPin(), Part())
        super().__init__(part=grid, **kwargs)


# show(HoneycombGrid([6, 4, 0, 2]), alphas=[0.5])
