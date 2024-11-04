# %%
from ocp_vscode import *
from sphlib import align, Dimensions, distribute, rescale_chamfer
from enum import Enum

from build123d import *

# === Dimensions
X, Y, Z = 0, 1, 2

d = Dimensions()
d.nicho = [280, 400, 280]
d.coluna = [10, 10, 139]

d.rib = 30
d.bolt = 3

d.u = 44.45  # 1.75"
d.space = 15.875  # 0.625"
d.margins = 6.35  # 0.25"

d.placa = [140, d.u, 3]
d.placa_maior = [150, d.u, 3]


# %%

pts = []

x = 0
y = 0
pts.append((x, y))

x += d.nicho[Y] / 2
pts.append((x, y))

y += d.coluna[Z]
pts.append((x, y))

x -= d.coluna[Y]
pts.append((x, y))

y -= d.coluna[Z] - d.coluna[X] - d.rib
pts.append((x, y))

y -= d.rib
x -= d.rib
pts.append((x, y))

x -= d.nicho[Y] / 2 - 2 * d.rib - 2 * d.coluna[X]
pts.append((x, y))

y += d.rib
x -= d.rib
pts.append((x, y))

y += d.coluna[Z] - d.coluna[X] - d.rib
pts.append((x, y))

x -= d.coluna[Y]
pts.append((x, y))

y -= d.coluna[Z]
pts.append((x, y))


ln = Polyline(pts)

sketch = make_face(Plane.YZ * ln)
suporte = extrude(sketch, d.coluna[X]).clean()

furo = Cylinder(radius=d.bolt / 2, height=d.nicho[Y] / 2).rotate(angle=90, axis=Axis.X)

furos = []
cur_z = 0
for i in range(3):
    cur_z += d.margins
    furos.append(cur_z)
    cur_z += d.space
    furos.append(cur_z)
    cur_z += d.space
    furos.append(cur_z)
    cur_z += d.margins

for pos_z in furos:
    suporte -= align(furo, ref=suporte, center="xy", centerToEnd="z", margins=[0, 0, pos_z])

# show(suporte)

export_stl(suporte, f"library/heartofgold/suporte.stl")

duplo = suporte + align(suporte, ref=suporte, beginToEnd="x")
# show(duplo)

export_stl(duplo, f"library/heartofgold/suporte-duplo.stl")

shorter = split(suporte, Plane(suporte.faces().sort_by(Axis.Z).first).offset(-5), keep=Keep.BOTTOM)
export_stl(shorter, f"library/heartofgold/suporte-shorter.stl")

# show(shorter)


# %%


def gen_placa():
    # placa simples
    placa = Box(length=d.placa[X], width=d.placa[Y], height=d.placa[Z])

    pos_furos = [d.margins, d.margins + d.space, d.margins + 2 * d.space]
    furo = Cylinder(radius=d.bolt / 2, height=d.placa[Z])

    for pos_furo in pos_furos:
        placa -= align(
            furo, ref=placa, centerToBegin="x", center="z", centerToEnd="y", margins=[d.coluna[X] / 2, pos_furo, 0]
        )

    for pos_furo in pos_furos:
        placa -= align(furo, ref=placa, centerToEnd="yx", center="z", margins=[d.coluna[X] / 2, pos_furo, 0])

    return placa


placa = gen_placa()

marvin = split(placa, Plane(placa.faces().sort_by(Axis.Y).first).offset(-1 * (d.margins * 2 + d.space)), keep=Keep.TOP)
export_stl(marvin, f"library/heartofgold/marvin.stl")


show(marvin)

# %%
placa = gen_placa().rotate(angle=90, axis=Axis.X)

d.folga_prateleira = 2

prateleira = Box(length=d.placa[X] - 2 * d.coluna[X] - d.folga_prateleira, width=d.nicho[Y] / 2, height=d.placa[Z])
prateleira += align(placa, ref=prateleira, endToBegin="y", begin="z", center="x")
prateleira += align(placa, ref=prateleira, end="y", begin="z", center="x", margins=[0, d.coluna[Y], 0])

box_hole = Box(length=d.placa[X] - 2 * d.coluna[X] - d.folga_prateleira, width=d.nicho[Y] / 2 + d.placa[Z], height=200)
box_hole = fillet(box_hole.edges().filter_by(Axis.Y).group_by(Axis.Z)[0], 25)
prateleira -= align(box_hole, ref=prateleira, center="xy", begin="z", margins=[0, 0, d.placa[Z]])

show(prateleira)
export_stl(prateleira, f"library/heartofgold/prateleira.stl")

# %%

# Joiner
joiner = Box(length=d.coluna[X], width=4 * d.margins + 2 * d.space, height=d.placa[Z])
pos_furos = [d.margins, d.margins + d.space, 3 * d.margins + d.space, 3 * d.margins + 2 * d.space]
furo = Cylinder(radius=d.bolt / 2, height=d.placa[Z])

for pos_furo in pos_furos:
    joiner -= align(furo, ref=joiner, center="xz", centerToEnd="y", margins=[0, pos_furo, 0])


show(joiner)
export_stl(joiner, f"library/heartofgold/joiner.stl")

joinerduplo = joiner + align(joiner, ref=joiner, beginToEnd="x")
show(joinerduplo)
export_stl(joinerduplo, f"library/heartofgold/joinerduplo.stl")

# %%
# Shelf
