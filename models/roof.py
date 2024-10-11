# %%
%cd /home/sphink/devel/3d
from ocp_vscode import *
from sphlib import align, Dimensions, Slot, SlotPosition, SlotType
import gridfinity as gf

from build123d import *

# === Dimensions
X, Y, Z = 0, 1, 2
d = Dimensions()
d.charger = [65, 95, 28]

# %%

triangle = Triangle(a = 72.179, B=57.8, C=57.8)
square = align(Rectangle(width=triangle.a, height=10), ref=triangle, endToBegin="y")
shape1 = triangle + square
shape2 = offset(shape1, 5.27, kind=Kind.INTERSECTION).translate([0, 0, 8])
base = loft(sections=[shape1, shape2])
cut_tool = align(Box(100, 100, 10), ref=base, begin="zy", margins=[0, 5.3, 0]) - base
show(cut_tool)
# show(triangle, triangle2, base)



# %%

# %%
cut_tool.export_stl("library/roof_45_cut_tool.stl")
