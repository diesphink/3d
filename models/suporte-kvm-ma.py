# %%
from textwrap import fill
from build123d import *
from ocp_vscode import show


from sphlib import Dimensions, align, Slot
from sphlib.slots import SlotPosition, SlotType

# === Dimensions
X, Y, Z = 0, 1, 2
d = Dimensions()

d.kvm = [61.53, 96, 25.14]
d.folga = 0.5

d.margem_suporte = 8

d.parafuso = 4.5 / 2
d.cabeca_parafuso = 9 / 2

parafuso = Cylinder(radius=d.parafuso, height=20)
parafuso += align(
    Cone(bottom_radius=d.cabeca_parafuso, top_radius=d.parafuso, height=5),
    ref=parafuso,
    center="xy",
    begin="z",
)

# show(parafuso)

suporte = Box(d.kvm[X] + d.margem_suporte * 2, d.margem_suporte * 2, d.kvm[Z] + d.margem_suporte)
suporte = fillet(suporte.edges(), 1)
kvm = Box(d.kvm[X] + d.folga, d.kvm[Y] + d.folga, d.kvm[Z] + d.folga)
suporte -= align(kvm, ref=suporte, center="x", begin="z", end="y", margins=[0, d.margem_suporte, 0])

done_edges = suporte.edges()

show(suporte)

export_stl(suporte, f"library/suporte_kvm_ma.stl")
