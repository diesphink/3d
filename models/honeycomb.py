# from attrdict import AttrDict
from math import sqrt
from ocp_vscode import show

from build123d import (
    Axis,
    BuildPart,
    Box,  # noqa: F401, E501
    BuildSketch,
    Locations,  # noqa: F401, E501
    Mode,  # noqa: F401, E501
    RegularPolygon,
    chamfer,
    extrude,
    fillet,  # noqa: F401, E501
    offset,  # noqa: F401, E501
)

d = {
    "pin": {
        "top": {
            "side": 7.5,
            "height": 10,
            "chamfer": 0.5,
        },
        "bottom": {
            "side": 9.815,
            "height": 2,
        },
    },
    "distance_between": 23.6,
}

space_x = d['distance_between']
space_y = d['distance_between'] * sqrt(3)/2
space_offset = d['distance_between']/2

def location_grid(pins_per_row = [1]):
    loc = []
    for row, pins in enumerate(pins_per_row):
        for pin in range(pins):
            print(row, pin)
            loc.append((pin * space_x - (space_offset if row % 2 == 0 else 0), row * space_y))
    return Locations(*loc)


# locations = Locations(
#     (0, 0),
#     (0, d["distance_between"]),
#     (d["distance_between"] * sqrt(3)/ 2,  d["distance_between"]/2),
#     (d["distance_between"] * sqrt(3)/ 2,  d["distance_between"]/2),
# )

with BuildPart() as pin:
    with BuildSketch() as sketch:
        with location_grid([6, 4, 0, 2]) as locations:
            RegularPolygon(radius=d["pin"]["bottom"]["side"], side_count=6, rotation=90)
    extrude(amount=d["pin"]["bottom"]["height"])
    with BuildSketch(*pin.faces().group_by(Axis.Z)[-1]) as sketch:
        RegularPolygon(radius=d["pin"]["top"]["side"], side_count=6, rotation=90)
    extrude(amount=d["pin"]["top"]["height"])
    chamfer(pin.edges().group_by(Axis.Z)[-1], length=d["pin"]["top"]["chamfer"])

show(pin)
