from textwrap import fill
from ocp_vscode import show

# from gridfinity.gridfinity_scoops import GridfinityBox
from cqgridfinity import GridfinityBox
from sphlib import align, Dimensions, Slot, SlotPosition, SlotType
import gridfinity as gf

from build123d import Axis, Box, Cylinder, fillet

# === Dimensions
X, Y, Z = 0, 1, 2
d = Dimensions()
d.base = [130, 130, 90]
d.depakene = [49, 49, 74]
d.cerazette = [25, 60, 120]
d.venlift = [90, 60, 144]
d.outros = [65, 55, 144]

d.outer_margin = 6


base = fillet(Box(*d.base).edges(), 4)

depakene = Cylinder(radius=d.depakene[X] / 2, height=d.depakene[Z])
depakene = align(
    depakene, ref=base, begin="xy", end="z", margins=[d.outer_margin, d.outer_margin + 3, -d.depakene[Z] / 2]
)

venlift = Box(*d.venlift)
venlift = fillet(venlift.edges().filter_by(Axis.Z), 4)
venlift = align(venlift, ref=base, begin="xz", end="y", margins=[d.outer_margin, d.outer_margin, 1])

cerazette = Box(*d.cerazette)
cerazette = fillet(cerazette.edges().filter_by(Axis.Z), 4)
cerazette = align(cerazette, ref=base, end="xyz", margins=[d.outer_margin, d.outer_margin, -d.cerazette[Z] / 2])

outros = Box(*d.outros)
outros = fillet(outros.edges().filter_by(Axis.Z), 4)
outros = align(outros, ref=base, begin="zy", end="x", margins=[d.outer_margin, d.outer_margin, 1])

base -= depakene
base -= venlift
base -= cerazette
base -= outros

# slot = Box(*d.humidifier)
# slot = fillet(slot.edges().filter_by(Axis.Z), 10)
# base -= align(slot, ref=base, center="xy", begin="z", margin=7)
show(base)
base.export_stl("library/caixa_remedios.stl")
base.export_step("library/caixa_remedios.step")

# Compare this snippet from models/gf_pen2.py:
# from ocp_vscode import show
