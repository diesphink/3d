# %%
from textwrap import fill
from build123d import *
from ocp_vscode import show


from sphlib import Dimensions, align, Slot
from sphlib.slots import SlotPosition, SlotType

# === Dimensions
X, Y, Z = 0, 1, 2
d = Dimensions()
d.bloco1 = [30.2, 37.7, 56]  # 56
d.m3_bolt = [3.5 / 2, 2.5 / 2, 20]
d.m3_bolt_margins = [11, 5.7, 0]

d.m3_nut_slot = [5.75, 5.75 / 2 + d.m3_bolt_margins[Y], 3]
d.m3_nut_margins = [11, 0, 10]

d.parafuso = 5.5 / 2

d.bloco2 = [11, d.bloco1[Y], 20]

bloco1 = Box(*d.bloco1)
bloco1 -= align(
    Cylinder(radius=d.m3_bolt[X], height=d.m3_bolt[Z]),
    ref=bloco1,
    centerToBegin="xy",
    centerToEnd="",
    end="z",
    margins=d.m3_bolt_margins,
)
bloco1 -= align(
    Cylinder(radius=d.m3_bolt[X], height=d.m3_bolt[Z]),
    ref=bloco1,
    centerToBegin="y",
    centerToEnd="x",
    end="z",
    margins=d.m3_bolt_margins,
)
bloco1 -= align(
    Cylinder(radius=d.m3_bolt[X], height=d.m3_bolt[Z]),
    ref=bloco1,
    centerToBegin="x",
    centerToEnd="y",
    end="z",
    margins=d.m3_bolt_margins,
)
bloco1 -= align(
    Cylinder(radius=d.m3_bolt[X], height=d.m3_bolt[Z]),
    ref=bloco1,
    centerToBegin="",
    centerToEnd="xy",
    end="z",
    margins=d.m3_bolt_margins,
)

# Nut slots

bloco1 -= align(
    Box(*d.m3_nut_slot),
    ref=bloco1,
    begin="y",
    centerToBegin="x",
    end="z",
    margins=d.m3_nut_margins,
)
bloco1 -= align(
    Box(*d.m3_nut_slot),
    ref=bloco1,
    begin="y",
    centerToEnd="x",
    end="z",
    margins=d.m3_nut_margins,
)
bloco1 -= align(
    Box(*d.m3_nut_slot),
    ref=bloco1,
    end="yz",
    centerToBegin="x",
    margins=d.m3_nut_margins,
)
bloco1 -= align(
    Box(*d.m3_nut_slot),
    ref=bloco1,
    end="yz",
    centerToEnd="x",
    margins=d.m3_nut_margins,
)

parafuso_madeira = Cylinder(radius=5.5 / 2, height=d.bloco1[Y])
parafuso_madeira += align(
    Cone(bottom_radius=10 / 2, top_radius=5.5 / 2, height=5),
    ref=parafuso_madeira,
    center="xy",
    begin="z",
)
# show(parafuso_madeira)

bloco1 -= align(parafuso_madeira.rotate(Axis.X, angle=270), ref=bloco1, begin="y", center="xz")

bloco2 = Box(*d.bloco2)
bloco2 -= align(parafuso_madeira.rotate(Axis.X, angle=270), ref=bloco1, begin="y", center="xz")

bloco = bloco1 + align(bloco2, ref=bloco1, begin="yz", endToBegin="x")


show(bloco)
export_stl(bloco, f"library/suporte_regua_mesa.stl")
