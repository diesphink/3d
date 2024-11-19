# %%
from ocp_vscode import *
from sphlib import align, Dimensions, distribute, rescale_chamfer
from enum import Enum

from build123d import *

# === Dimensions
X, Y, Z = 0, 1, 2

# ==== caches
cache_lofteds = []

d = Dimensions()

d.caixa = [285, 285, 73]
d.tabuleiro = [281, 281, 12]
d.manual = [220, 281, 3]

d.dado = [14.5, 14.5, 14.5]

d.construcao.total = [d.caixa[X] - d.manual[X], 281, 32]
d.construcao.target = [d.caixa[X] - d.manual[X], 297, 32]
d.construcao.delta = (d.construcao.target[Y] - d.construcao.total[Y]) / 4

d.construcao.tile = [49, 49, 2]
d.construcao.lado_tile = 20

d.fillet = 1
d.wall = 0.8


d.cidadaos = [57, 57, 18]
d.cidadaos_grip = [-25, 10, 10]


# %%


def gen_cidadaos(qtd=1):
    cidadaos = Box(length=d.cidadaos[X], width=d.cidadaos[Y] * qtd, height=d.cidadaos[Z])

    top_face = cidadaos.faces().group_by(Axis.Z)[-1][0]
    cidadaos = fillet(cidadaos.edges() - top_face.edges(), radius=d.fillet)

    plane = Plane(top_face)

    upper_rec = Rectangle(
        d.cidadaos[X] - d.wall * 2 - d.cidadaos_grip[X], d.cidadaos[Y] - d.wall * 2 - d.cidadaos_grip[Y]
    )
    upper_rec = fillet(upper_rec.vertices(), d.fillet * 10)

    middle_rec = Rectangle(d.cidadaos[X] - d.wall * 2, d.cidadaos[Y] - d.wall * 2)
    middle_rec = fillet(middle_rec.vertices(), d.fillet * 10)

    faces = Sketch() + [
        plane * upper_rec,
        plane.offset(-d.cidadaos_grip[Z]) * middle_rec,
        plane.offset(-d.dado[Z]) * Rectangle(d.dado[X] * 3, d.dado[Y] * 3),
    ]

    lofted = loft(faces)

    for i in range(qtd):
        # cidadaos += lofted.translate([0, d.cidadaos[Y] * i, 0])
        if len(cache_lofteds) <= i:
            cache_lofteds.append(lofted.translate([0, d.cidadaos[Y] * i, 0]) + cache_lofteds)

    return cidadaos - align(cache_lofteds[qtd - 1], ref=cidadaos, center="xy", end="z")


show(gen_cidadaos(1))

export_stl(gen_cidadaos(1), f"library/origin/cidadaos_1.stl")
export_stl(gen_cidadaos(2), f"library/origin/cidadaos_2.stl")
export_stl(gen_cidadaos(3), f"library/origin/cidadaos_3.stl")
export_stl(gen_cidadaos(4), f"library/origin/cidadaos_4.stl")
export_stl(gen_cidadaos(5), f"library/origin/cidadaos_5.stl")

# %%

d.recursos = [57 * 1.5, 57 * 1, 18]
d.recurso_diam = 23
d.recursos_grip = d.recurso_diam / 2
d.recursos_deepness = 15
d.recursos_5 = [23, 23, 2.05]


recursos = Box(length=d.recursos[X], width=d.recursos[Y], height=d.recursos[Z])

top_face = recursos.faces().group_by(Axis.Z)[-1][0]
recursos = fillet(recursos.edges() - top_face.edges(), radius=d.fillet)

plane = Plane(top_face)

upper_rec = Rectangle(
    d.recursos[X] - d.wall * 2 - d.recurso_diam / 2 - d.recursos_grip, d.recursos[Y] - d.wall * 2 - d.recurso_diam / 2
).translate([-d.recurso_diam / 4 + d.recursos_grip / 2, -d.recurso_diam / 4, 0])
upper_rec = fillet(upper_rec.vertices(), d.fillet * 10)

lower_rec = Rectangle(d.recursos[X] - d.wall * 2 - d.recurso_diam / 2, d.recursos[Y] * 0.5).translate(
    [-d.recurso_diam / 4, d.recursos[Y] * 0.5 / 2, 0]
)
lower_rec = align(lower_rec, ref=upper_rec, end="xy")
lower_rec = fillet(lower_rec.vertices(), d.fillet * 5)


faces = Sketch() + [
    plane * upper_rec,
    plane.offset(-d.recursos_deepness) * lower_rec,
]

# lofted = loft(faces)
recursos -= loft(faces)

recursos -= align(
    Cylinder(radius=d.recurso_diam / 2, height=d.recursos_5[Z] * 5),
    ref=recursos,
    end="xyz",
    margins=[d.wall, d.wall, 0],
)

show(recursos)
export_stl(recursos, f"library/origin/recursos.stl")

# %%

d.recursos = [57 * 1.5, 57 * 1, 18]
d.recurso_diam = 23
d.recursos_grip = d.recurso_diam / 2
d.recursos_deepness = 15
d.recursos_5 = [23, 23, 2.05]


recursos = Box(length=d.recursos[X] * 2, width=d.recursos[Y] * 2, height=d.recursos[Z])

top_face = recursos.faces().group_by(Axis.Z)[-1][0]
recursos = fillet(recursos.edges() - top_face.edges(), radius=d.fillet)

plane = Plane(top_face)
upper_rec = Rectangle(
    d.recursos[X] - d.wall * 2 - d.recurso_diam / 2 - d.recursos_grip, d.recursos[Y] - d.wall * 2 - d.recurso_diam / 2
)
upper_rec = fillet(upper_rec.vertices(), d.fillet * 10)

lower_rec = Rectangle(d.recursos[X] - d.wall * 2 - d.recurso_diam / 2, d.recursos[Y] * 0.5)
lower_rec = align(lower_rec, ref=upper_rec, end="xy")
lower_rec = fillet(lower_rec.vertices(), d.fillet * 5)


faces = Sketch() + [
    plane * upper_rec,
    plane.offset(-d.recursos_deepness) * lower_rec,
]

lofted = loft(faces)
lofted += align(Cylinder(radius=d.recurso_diam / 2, height=d.recursos_5[Z] * 4), ref=lofted, end="z", centerToEnd="xy")

recursos -= align(lofted, ref=recursos, begin="xy", margins=[d.wall, d.wall, 0])
lofted = mirror(lofted, about=Plane.XZ)
recursos -= align(lofted, ref=recursos, begin="x", end="y", margins=[d.wall, d.wall, 0])
lofted = mirror(lofted, about=Plane.YZ)
recursos -= align(lofted, ref=recursos, begin="", end="xy", margins=[d.wall, d.wall, 0])
lofted = mirror(lofted, about=Plane.XZ)
recursos -= align(lofted, ref=recursos, begin="y", end="x", margins=[d.wall, d.wall, 0])

show(recursos)
# recursos -= loft(faces)

# recursos -= align(lofted, ref=recursos, end="xyz")

# recursos -= align(
#     Cylinder(radius=d.recurso_diam / 2, height=d.recursos_5[Z] * 5),
#     ref=recursos,
#     end="xyz",
#     margins=[d.wall, d.wall, 0],
# )

# show(recursos)
export_stl(recursos, f"library/origin/recursos.stl")

# %%
d.superioridade.box = [3 * 57, 57, 18]
d.superioridade.token = [31, 31, 2.05]

d.superioridade.side_space = 13

d.m100.token = [21, 39, 2.05]


def gen_box(**kwargs):
    box = Box(**kwargs)
    top_face = box.faces().group_by(Axis.Z)[-1][0]
    box = fillet(box.edges() - top_face.edges(), radius=d.fillet)
    return box


box_superioridade = gen_box(width=d.superioridade.box[Y], length=d.superioridade.box[X], height=d.superioridade.box[Z])

token_superioridade = Box(
    length=d.superioridade.token[X], width=d.superioridade.token[Y], height=d.superioridade.token[Z] * 7
).rotate(Axis.Z, 45)

tokens = Part() + distribute([token_superioridade] * 3, gap="x", rangeX=[0, 144])

box_superioridade -= align(tokens, ref=box_superioridade, begin="x", center="y", end="z", margins=[d.wall, 0, 0])

# side_space = Box(length=d.superioridade.box[X] - 2*d.wall - d.m100.token[X], width=d.superioridade.side_space, height=d.superioridade.token[Z] * 5)
side_space = Box(length=d.superioridade.box[X], width=d.superioridade.side_space, height=d.superioridade.token[Z] * 7)

box_superioridade -= align(side_space, ref=box_superioridade, begin="x", end="yz")
box_superioridade -= align(side_space, ref=box_superioridade, begin="xy", end="z")


m100 = extrude(SlotOverall(width=d.m100.token[Y], height=d.m100.token[X]), d.m100.token[Z] * 7).rotate(Axis.Z, 90)

box_superioridade -= align(m100, ref=box_superioridade, center="y", end="xz", margins=[d.wall, 0, 0])


show(box_superioridade)
export_stl(box_superioridade, f"library/origin/superioridade.stl")

# # %%
# d.superioridade.box = [3 * 57, 57, 18]
# d.superioridade.tokens = [112, 31, 16]

# d.superioridade.side_space = (d.superioridade.box[Y] - d.superioridade.tokens[Y]) / 2

# d.m100.token = [21, 39, 2.05]
# d.superioridade.wedge = [18, 31, 16]


# def gen_box(**kwargs):
#     box = Box(**kwargs)
#     top_face = box.faces().group_by(Axis.Z)[-1][0]
#     box = fillet(box.edges() - top_face.edges(), radius=d.fillet)
#     return box


# box_superioridade = gen_box(width=d.superioridade.box[Y], length=d.superioridade.box[X], height=d.superioridade.box[Z])

# tokens = Box(length=d.superioridade.tokens[X], width=d.superioridade.tokens[Y], height=d.superioridade.tokens[Z])
# tokens -= align(
#     Wedge(ysize=18, xsize=31, zsize=16, xmin=0, xmax=31, zmin=0, zmax=0).rotate(Axis.Z, -90),
#     ref=tokens,
#     begin="x",
#     center="y",
#     end="z",
# )

# m100 = extrude(SlotOverall(width=d.m100.token[Y], height=d.m100.token[X]), d.m100.token[Z] * 4).rotate(Axis.Z, 90)


# side_space = Box(length=d.superioridade.box[X], width=d.superioridade.side_space, height=d.superioridade.tokens[Z] / 2)

# box_superioridade -= align(side_space, ref=box_superioridade, begin="xy", end="z")

# box_superioridade -= align(tokens, ref=box_superioridade, begin="x", center="y", end="z", margins=[10, 0, 0])
# box_superioridade -= align(m100, ref=box_superioridade, center="y", end="xz", margins=[10, 0, 0])


# show(box_superioridade)
# export_stl(box_superioridade, f"library/origin/superioridade.stl")

# %%
import math

d.construcoes.tile = [49, 49, 2.05]
d.construcoes.box = [57, 57, 38]
d.construcoes.rotation = 45 / 2


def gen_construcoes(qtd):
    box = gen_box(length=d.construcoes.box[X], width=d.construcoes.box[Y] * qtd, height=d.construcoes.box[Z])
    octagon = extrude(
        RegularPolygon(radius=d.construcoes.tile[X] / 2, major_radius=False, side_count=8), d.construcoes.tile[Z] * 15
    )
    octagon = octagon.rotate(Axis.Z, d.construcoes.rotation)
    extraslot = Box(length=57, width=d.construcoes.tile[X] / 2, height=d.construcoes.tile[Z] * 15)

    slot = align(octagon, ref=box, center="xy", end="z") + align(extraslot, ref=box, center="xy", end="z")

    if qtd > 1:
        slots = distribute(qtd * [slot], gap="y", rangeY=[0, 57 * qtd - d.fillet * 2])
    else:
        slots = slot

    edges_before = box.edges()
    box -= align(Part() + slots, ref=box, center="xy", end="z")
    box -= align(
        Box(length=d.construcoes.tile[X] / 2, width=57 * qtd, height=d.construcoes.tile[Z] * 15),
        ref=box,
        center="xy",
        end="z",
    )

    box = fillet(box.edges().filter_by(Axis.Z) - edges_before, radius=d.fillet * 2)

    return box


show(gen_construcoes(3))

export_stl(gen_construcoes(1), f"library/origin/construcoes_1.stl")
export_stl(gen_construcoes(2), f"library/origin/construcoes_2.stl")
export_stl(gen_construcoes(3), f"library/origin/construcoes_3.stl")
export_stl(gen_construcoes(4), f"library/origin/construcoes_4.stl")
export_stl(gen_construcoes(5), f"library/origin/construcoes_5.stl")

# %%
d.jogador.box = [57, 57 * 1.5, 50]
d.jogador.arconte = 21
d.jogador.arconte_z = 40
d.jogador.wall = 2
d.jogador.side_space = [d.jogador.box[X], 2 * d.jogador.wall + d.jogador.arconte, d.jogador.box[Z] / 2]
d.jogador.slot = [5, 65, d.construcoes.tile[X]]
d.jogador.token = [
    d.jogador.box[X] - d.jogador.wall * 3 - d.jogador.slot[X],
    d.jogador.box[Y] - d.jogador.arconte - d.jogador.wall * 4,
    20,
]
d.jogador.grip = 15


box = gen_box(length=d.jogador.box[X], width=d.jogador.box[Y], height=d.jogador.box[Z])
tokens = gen_box(length=d.jogador.token[X], width=d.jogador.token[Y], height=d.jogador.token[Z])
arconte = Cylinder(radius=d.jogador.arconte / 2, height=d.jogador.arconte_z)
side_space = Box(length=d.jogador.side_space[X], width=d.jogador.side_space[Y], height=d.jogador.side_space[Z])
side2 = Box(
    length=d.jogador.slot[X] + d.jogador.wall, width=d.jogador.slot[Y] + d.jogador.wall, height=d.jogador.side_space[Z]
)
slot = Box(length=d.jogador.slot[X], width=d.jogador.slot[Y], height=d.jogador.slot[Z])
grip = Cone(d.jogador.wall / 2, top_radius=d.jogador.grip / 2, height=d.jogador.grip / 2)

box -= align(tokens, ref=box, begin="xy", end="z", margins=[d.jogador.wall, d.jogador.wall, 0])
box -= align(arconte, ref=box, end="yz", begin="x", margins=[d.jogador.wall, d.jogador.wall, 0])
box -= align(side_space, ref=box, end="xyz")
box -= align(side2, ref=box, end="xyz")
box -= align(slot, ref=box, end="yxz", margins=[d.jogador.wall, d.jogador.wall, 0])
box += align(
    grip, ref=box, center="x", end="z", centerToEnd="y", margins=[0, d.jogador.wall * 2.5 + d.jogador.arconte, 0]
)

box = fillet(box.edges().filter_by(Axis.Z).group_by(Axis.Z)[-2], radius=d.fillet - 0.01)

show(box)
# show(box, box.edges().filter_by(Axis.Z).group_by(Axis.Z)[-2])

# show(box)
export_stl(box, f"library/origin/jogador.stl")

# %%
d.navemae.box = [57 * 1.5, 57 * 1.5, 40]
d.navemae.naves = [61, 61, 36]

d.long_token = [15.5, 45.5, 2.05]
gap = (d.navemae.box[X] - d.long_token[X] - d.navemae.naves[X]) / 3

box = gen_box(length=d.navemae.box[X], width=d.navemae.box[Y], height=d.navemae.box[Z])

naves = Cylinder(radius=d.navemae.naves[X] / 2, height=d.navemae.naves[Z])
naves += Box(length=d.navemae.naves[X] / 2, width=d.navemae.box[Y], height=d.navemae.naves[Z])


tokens = Box(length=d.long_token[X], width=d.long_token[Y], height=d.long_token[Z] * 5)
tokens = fillet(tokens.edges().filter_by(Axis.Z), radius=d.fillet)
tokens += align(
    Box(length=d.navemae.box[X] / 2, width=d.navemae.naves[X] / 2, height=d.long_token[Z] * 5),
    ref=tokens,
    end="zx",
    center="y",
    margins=[-gap, 0, 0],
)

gap = (d.navemae.box[X] - d.long_token[X] - d.navemae.naves[X]) / 3

box -= align(naves, ref=box, begin="x", center="y", end="z", margins=[gap, 0, 0])
box -= align(tokens, ref=box, begin="", center="y", end="xz")

show(box)
export_stl(box, f"library/origin/navemae.stl")

# %%
d.distrito.box = [57 * 1.5, 57 * 1.5, 40]
d.distrito.cartas = [42, 64, 18]
d.distrito.wall = 2
d.distrito.tokens = [
    d.distrito.box[X] - d.distrito.cartas[X] - d.distrito.wall * 3,
    d.distrito.box[Y] - d.distrito.wall * 2,
    d.distrito.cartas[Z],
]

box = gen_box(length=d.distrito.box[X], width=d.distrito.box[Y], height=d.distrito.box[Z])

cartas = Box(length=d.distrito.cartas[X], width=d.distrito.cartas[Y], height=d.distrito.cartas[Z])
# cartas = fillet(cartas.edges().filter_by(Axis.Z), radius=d.fillet)
cartas += align(
    Box(length=d.distrito.cartas[X] / 2, width=d.distrito.box[Y], height=d.distrito.cartas[Z]),
    ref=cartas,
    end="z",
    center="xy",
)

tokens = Box(length=d.distrito.tokens[X], width=d.distrito.tokens[Y], height=d.distrito.tokens[Z])
# tokens = fillet(tokens.edges().filter_by(Axis.Z), radius=d.fillet)

box -= align(cartas, ref=box, center="y", end="xz", margins=[d.distrito.wall, 0, 0])
box -= align(tokens, ref=box, begin="x", center="y", end="z", margins=[d.distrito.wall, 0, 0])

box = fillet(box.edges().filter_by(Axis.Z).group_by(Axis.Z)[-1], radius=d.fillet)


show(box)
export_stl(box, f"library/origin/distrito.stl")

# %%

d.oradores.box = [57, 57, 40]

box = gen_box(length=d.oradores.box[X], width=d.oradores.box[Y], height=d.oradores.box[Z])

bottom_rec = Rectangle(d.dado[X] * 2 + 3, d.dado[Y] * 2 + 3)
upper_rec = Rectangle(d.oradores.box[X] - d.wall * 2, d.oradores.box[Y] - d.wall * 2).translate([0, 0, d.dado[Z]])

lofted = loft([bottom_rec, upper_rec])

box -= align(lofted, ref=box, center="xy", end="z")
box = fillet(box.edges().group_by(Axis.Z)[-2], radius=5)

show(box)
export_stl(box, f"library/origin/oradores.stl")


# %%
d.tab_jogador.box = [57 * 4, 57 * 1.5, 40]
d.tab_jogador.wall = 2
d.tab_jogador.tile = [220, 80, 2.05]

box = gen_box(length=d.tab_jogador.box[X], width=d.tab_jogador.box[Y], height=d.tab_jogador.box[Z])

slot = gen_box(
    length=d.tab_jogador.box[X] - d.tab_jogador.wall * 2,
    width=d.tab_jogador.box[Y] - d.tab_jogador.wall * 2,
    height=d.tab_jogador.tile[Z] * 4,
)

box -= align(slot, ref=box, center="xy", end="z")

show(box)
export_stl(box, f"library/origin/tab_jogador.stl")

# %%
d.zod_cartas.box = [57, 57 * 1.5, 20]
d.zod_cartas.cartas = [42, 64, 9]
d.zod_cartas.wall = 2

box = gen_box(length=d.zod_cartas.box[X], width=d.zod_cartas.box[Y], height=d.zod_cartas.box[Z])

cartas = Box(length=d.zod_cartas.cartas[X], width=d.zod_cartas.cartas[Y], height=d.zod_cartas.cartas[Z])
# cartas = fillet(cartas.edges().filter_by(Axis.Z), radius=d.fillet)
cartas += align(
    Box(length=d.zod_cartas.cartas[X] / 2, width=d.zod_cartas.box[Y], height=d.zod_cartas.cartas[Z]),
    ref=cartas,
    end="z",
    center="xy",
)

# tokens = Box(length=d.distrito.tokens[X], width=d.distrito.tokens[Y], height=d.distrito.tokens[Z])
# tokens = fillet(tokens.edges().filter_by(Axis.Z), radius=d.fillet)

box -= align(cartas, ref=box, center="yx", end="z", margins=[d.distrito.wall, 0, 0])
# box -= align(tokens, ref=box, begin="x", center="y", end="z", margins=[d.distrito.wall, 0, 0])

box = fillet(box.edges().filter_by(Axis.Z).group_by(Axis.Z)[-1], radius=d.fillet)


show(box)
export_stl(box, f"library/origin/zod_cartas.stl")
