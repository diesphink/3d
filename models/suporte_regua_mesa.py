# %%
from textwrap import fill
from build123d import *
from ocp_vscode import show


from sphlib import Dimensions, align, Slot
from sphlib.slots import SlotPosition, SlotType

# === Dimensions
X, Y, Z = 0, 1, 2
d = Dimensions()
d.bloco1 = [23, 38, 55]
d.bloco2 = [23, 85, 35]
d.extra_margins_y = 5
d.bloco1[Y] += 2 * d.extra_margins_y
d.vao = [12, 4.3, d.bloco1[Z]]
d.vao_margem = [5.5, 3, 0]

d.distancia_entre_m3 = 28.7  # Com base nos centros


d.parafuso_m3 = 3.3 / 2
d.nut_m3 = 6 / 2
d.parafuso_madeira = 5.5 / 2


bloco1 = Box(*d.bloco1)
# parafuso =

bloco1 = fillet(bloco1.edges(), 1)
show(bloco1)

bloco2 = Box(*d.bloco2)
# parafuso =

bloco2 -= align(
    Cylinder(radius=d.parafuso_madeira, height=d.bloco2[Z]),
    ref=bloco2,
    center="xz",
    centerToEnd="y",
    margins=[0, d.vao_margem[Y] + d.parafuso_madeira + d.extra_margins_y, 0],
)
bloco2 -= align(
    Cylinder(radius=d.parafuso_madeira, height=d.bloco2[Z]),
    ref=bloco2,
    center="xz",
    centerToBegin="y",
    margins=[0, d.vao_margem[Y] + d.parafuso_madeira + d.extra_margins_y, 0],
)
bloco2 = chamfer(bloco2.edges().filter_by(GeomType.CIRCLE).group_by(Axis.Z)[-1], 3)
show(bloco2)

bloco2 = align(bloco2, ref=bloco1, center="yx", begin="z")

bloco = bloco1 + bloco2

m3 = Cylinder(radius=d.parafuso_m3, height=bloco.size().Z + 2)


show(bloco)

export_stl(bloco, f"library/suporte_regua_mesa.stl")
