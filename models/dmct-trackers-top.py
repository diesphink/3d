# %%
from ocp_vscode import *
from sphlib import align, Dimensions, Slot, SlotPosition, SlotType
import gridfinity as gf
import math

from build123d import *

# === Dimensions
X, Y, Z = 0, 1, 2

# %%
d = Dimensions()
d.slot.width = 16.5
d.slot.cap.height = 6.59
d.slot.cap.slope_width = 8
d.slot.cap.over_height = 7
d.wall.thickness = 2
d.degrees = 39.421

d.thickness = 15

pts = []
x, y = 0, 0
pts.append((x, y))

x += d.wall.thickness
pts.append((x, y))

y += d.slot.cap.over_height
pts.append((x, y))

x += d.slot.cap.slope_width
y += math.tan(math.radians(d.degrees)) * d.slot.cap.slope_width
pts.append((x, y))

x += d.slot.width - (d.slot.cap.slope_width * 2)
pts.append((x, y))


x += d.slot.cap.slope_width
y -= math.tan(math.radians(d.degrees)) * d.slot.cap.slope_width
pts.append((x, y))

y -= d.slot.cap.over_height
pts.append((x, y))

x += d.wall.thickness
pts.append((x, y))

y += d.slot.cap.over_height
pts.append((x, y))

y += math.tan(math.radians(d.degrees)) * (d.slot.cap.slope_width + d.wall.thickness)
x -= d.wall.thickness + d.slot.cap.slope_width
pts.append((x, y))

x -= d.slot.width - (d.slot.cap.slope_width * 2)
pts.append((x, y))

x -= d.wall.thickness + d.slot.cap.slope_width
y -= math.tan(math.radians(d.degrees)) * (d.slot.cap.slope_width + d.wall.thickness)
pts.append((x, y))

y -= d.slot.cap.over_height
pts.append((x, y))

# pts = [
#     (0,0),
#     (d.wall.thickness, 0),
#     (d.)
# ]

# (L, H, W, t) = (100.0, 20.0, 20.0, 1.0)
# pts = [
#     (0, H / 2.0),
#     (W / 2.0, H / 2.0),
#     (W / 2.0, (H / 2.0 - t)),
#     (t / 2.0, (H / 2.0 - t)),
#     (t / 2.0, (t - H / 2.0)),
#     (W / 2.0, (t - H / 2.0)),
#     (W / 2.0, H / -2.0),
#     (0, H / -2.0),
# ]


ln = Polyline(*pts)
# ln += mirror(ln, Plane.YZ)

sk8 = make_face(Plane.YZ * ln)
# show(sk8)
ex8 = extrude(sk8, d.thickness).clean()

show(ex8)

export_stl(ex8, "library/dmct-trackers-top.stl")
