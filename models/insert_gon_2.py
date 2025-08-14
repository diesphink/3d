# %%
from textwrap import fill
from build123d import *
from ocp_vscode import show


from sphlib import Dimensions, align, Slot
from sphlib.slots import SlotPosition, SlotType

# === Dimensions
X, Y, Z = 0, 1, 2
d = Dimensions()
d.espaco = [93, 143, 36]
d.placa = [93, 143, d.espaco[Z] - 20]
d.conectores.largura = 1.927
d.conectores.comprimento = 1.5

d.aranha.base = [51, 51, 2.5]
d.aranha.full = [54, 54, 33]

d.lobo.base = [51, 51, 2.5]
d.lobo.full = [54, 54, 33]

d.aranha_p.base = [26, 26, 2]
d.aranha_p.full = [26, 26, 10]

d.gon.base = [25.5, 25.5, 5]
d.gon.full = [37, 37, 30.8]

d.tigre.base = [51, 51, 2.5]
d.tigre.full = [54, 54, 33]


placa = Box(*d.placa)
placa = fillet(placa.edges().filter_by(Axis.Z), 5)

aranha = Cylinder(d.aranha.full[X] / 2, d.aranha.full[Z])
aranha += align(Cylinder(d.aranha.base[X] / 2, d.aranha.base[Z]), ref=aranha, center="xy", endToBegin="z")
aranha = align(aranha, ref=placa, begin="xy", end="z", margins=[1, 1, d.placa[Z] - d.espaco[Z]])

# lobo = Box(*d.lobo.full)
lobo = Cylinder(d.lobo.full[X] / 2, d.lobo.full[Z])
lobo_canto = Box(d.lobo.full[X] / 2, d.lobo.full[X] / 2, d.lobo.full[Z])
lobo_canto = fillet(lobo_canto.edges().filter_by(Axis.Z), 4)
lobo += align(lobo_canto, ref=lobo, end="y", begin="xz")
# lobo = fillet(lobo.edges().filter_by(Axis.Z), 5)
lobo += align(
    Cylinder(d.lobo.base[X] / 2, d.lobo.base[Z]), ref=lobo, end="y", center="x", endToBegin="z", margins=[0, 0.5, 0]
)

lobo = align(lobo, ref=placa, begin="x", end="yz", margins=[1, 1, d.placa[Z] - d.espaco[Z]])

aranha_p = Cylinder(d.aranha_p.full[X] / 2, d.aranha_p.full[Z])
aranha_p += align(Cylinder(d.aranha_p.base[X] / 2, d.aranha_p.base[Z]), ref=aranha_p, center="xy", endToBegin="z")
aranha_p = align(aranha_p, ref=placa, center="y", begin="x", end="z", margins=[3, 1, d.placa[Z] - d.espaco[Z]])

gon = Cylinder(d.gon.full[X] / 2, d.gon.full[Z])
gon += align(Cylinder(d.gon.base[X] / 2, d.gon.base[Z]), ref=gon, center="xy", endToBegin="z")
gon = align(gon, ref=placa, end="xyz", margins=[1, 1, d.placa[Z] - d.espaco[Z]])

tigre = Cylinder(d.tigre.full[X] / 2, d.tigre.full[Z])
tigre += align(Cylinder(d.tigre.base[X] / 2, d.tigre.base[Z]), ref=tigre, center="xy", endToBegin="z")
tigre = align(tigre, ref=placa, center="y", end="zx", margins=[1, 1, d.placa[Z] - d.espaco[Z]])


# extraheight = Box(30, 40, 12)
# extraheight = fillet(extraheight.edges().filter_by(Axis.Z), 5)
extraheight = Cylinder(16, 12)
extraheight = align(extraheight, ref=aranha_p, center="xy")
extraheight = align(extraheight, ref=placa, beginToEnd="z")

placa = placa + extraheight - aranha - lobo - aranha_p - gon - tigre

# export_stl(placa, "library/insert_gon.placa.stl")
# show(placa)

# === Token

d.token.total = [22, 143, 7]  # 13 (z) minus 4mm for pin, 2mm for felt
d.token.hole = [4, 4, 4]
d.token.pin.bottom = [3.7, 3.7, 4]
d.token.pin.top.radius = 2.5
d.token.pin.top.height = 4
d.lip = [1.9, 146, 7]

token = Box(d.token.total[X], d.token.total[Y], d.token.total[Z])
token = fillet(token.edges(), 1)
token += align(Box(*d.lip), ref=token, center="y", begin="xz")

token_holes = None
for loc in GridLocations(x_spacing=7, y_spacing=7, x_count=3, y_count=20):
    if token_holes == None:
        token_holes = Plane.XY * loc * Box(*d.token.hole)
    else:
        token_holes += Plane.XY * loc * Box(*d.token.hole)

token -= align(token_holes, ref=token, center="xy", end="z")

show(token)
export_stl(token, "library/insert_gon.token2.stl")

# %%
# Spell Markers
d.spell = [50, 50, 1]
spell = Cylinder(d.spell[X] / 2, d.spell[Z])

moonbeam = spell - align(
    extrude(Text("MOONBEAM", font_size=7, font_style=FontStyle.BOLD), 0.6), ref=spell, center="xy", end="z"
)
show(moonbeam)

conj = spell - align(
    extrude(Text("CONJURE\nANIMALS", font_size=8, font_style=FontStyle.BOLD), 0.6), ref=spell, center="xy", end="z"
)
show(conj)

export_stl(moonbeam, "library/insert_gon.spell.moonbeam.stl")
export_stl(conj, "library/insert_gon.spell.conjure_animals.stl")

# show(placa)
# placa = fillet(placa.edges().group_by(Axis.Z)[-1], 1.5)


# d.mini.total = [67, 40, 25]  # Tamanho do bloco que vai segurar a mini
# d.mini.base.diameter = 25.4  # Diâmetro da base da mini
# d.mini.base.height = 3.2  # Altura apenas da base da mini
# d.mini.angle = 4  # Ângulo de inclinação da base da mini ao colocar no suporte
# d.mini.margin = 2.2  # Distância entre os limites da base e os limites da miniatura
# d.mini.paredes = 2  # Tamanho das paredes ao redor da mini


# # === Suporte Mini
# suporte_mini = Box(*d.mini.total)
# suporte_mini = fillet(suporte_mini.edges().filter_by(Axis.Z), 1)
# mini = Cylinder(d.mini.base.diameter / 2, d.mini.base.height)
# mini += align(Box(d.mini.base.diameter, d.mini.base.diameter / 2, d.mini.base.height), ref=mini, begin="xyz")
# mini += align(Cylinder(d.mini.base.diameter / 2 - d.mini.margin, 80), ref=mini, beginToEnd="z")
# mini += align(
#     Box(d.mini.base.diameter - 2 * d.mini.margin, d.mini.base.diameter / 2, 80),
#     ref=mini,
#     begin="y",
#     center="x",
#     end="z",
# )
# mini = mini.rotate(Axis.X, -90 + d.mini.angle).rotate(Axis.Z, -90)
# suporte_mini -= align(mini, ref=suporte_mini, center="y", begin="xz", margins=[d.mini.paredes, 0, 0]).translate(
#     [0, 2, -0.4]
# )
# suporte_mini -= align(
#     Box(d.mini.total[X] - d.mini.base.height - 2 * d.mini.paredes, d.mini.total[Y] - d.mini.paredes, d.mini.total[Z]),
#     ref=suporte_mini,
#     begin="y",
#     end="xz",
# )


# # === Suporte Cartas

# d.small.total = [67, 49, 25]
# d.small.floor = 0.6

# suporte_cartas = Box(*d.small.total)
# suporte_cartas = fillet(suporte_cartas.edges().filter_by(Axis.Z), 1)
# slot = Slot(
#     Box(d.minicarta[X], d.minicarta[Y], d.small.total[Z] - d.small.floor),
#     SlotPosition.Y_AXIS_MAX,
#     (d.small.total[Z] - d.small.floor) * 2,
#     SlotType.SPHERE,
# )
# suporte_cartas -= align(slot, ref=suporte_cartas, begin="xy", end="z", margins=[0, 2, 0])
# suporte_cartas = align(suporte_cartas, ref=suporte_mini, begin="xz", endToBegin="y")

# # === Empty

# d.empty = [22, 89, 25]
# empty = Box(*d.empty)
# empty = fillet(empty.edges().filter_by(Axis.Z), 1)
# empty = align(empty, ref=suporte_cartas, begin="yz", beginToEnd="x")


# # === Buraco das cartas grandes

# cartas_grandes = align(Box(*d.carta_grande), ref=empty, end="xyz")

# suporte_cartas -= cartas_grandes
# suporte_mini -= cartas_grandes
# empty -= cartas_grandes


# # show(suporte_mini)

# all = suporte_mini + suporte_cartas + empty


# # === Token

# d.token.total = [22, 89, 25 - 2]  # z minus 2mm for felt
# d.token.hole = [4, 4, 4]
# d.token.pin.bottom = [3.7, 3.7, 4]
# d.token.pin.top.radius = 2.5
# d.token.pin.top.height = 4

# token = Box(d.token.total[X], d.token.total[Y], d.token.total[Z] - d.token.pin.top.height)
# token = fillet(token.edges(), 1)

# token_holes = None
# for loc in GridLocations(x_spacing=7, y_spacing=10, x_count=3, y_count=9):
#     if token_holes == None:
#         token_holes = Plane.XY * loc * Box(*d.token.hole)
#     else:
#         token_holes += Plane.XY * loc * Box(*d.token.hole)

# token -= align(token_holes, ref=token, center="xy", end="z")

# # show(token)

# # === Pin

# pin = Box(*d.token.pin.bottom)
# # pin = fillet(pin.edges().filter_by(Axis.Z), 0.5)
# pin_bottom = fillet(pin.edges().group_by(Axis.Z)[:-1], 0.5)


# pin_top = align(
#     Cylinder(d.token.pin.top.radius, d.token.pin.top.height * 4 / 5),
#     ref=pin,
#     center="xy",
#     beginToEnd="z",
#     margins=[0, 0, d.token.pin.top.height / 5],
# )

# # faces = Sketch() + [
# # pin_top.faces().sort_by(Axis.Z).first() * Circle(d.token.pin.top.radius),
# # pin_.offset(length / 2) * Rectangle(length / 6, width / 6),
# # ]

# pin_loft = loft([pin_top.faces().sort_by(Axis.Z).first, pin_bottom.faces().sort_by(Axis.Z).last])
# pin = pin_bottom + pin_top + pin_loft
# pin = pin.rotate(Axis.X, 180)


# # === Pin Label

# d.token.label.total = [22, 7, 1]
# d.token.label.texts = ["INSPIR", "1ST LVL", "2ND LVL", "WLD SHP", "HIT DIE"]
# d.token.label.font_sizes = [5, 5, 5, 4.3, 5]
# d.token.label.font_height = 0.4
# d.token.label.border = 0.8

# for i in range(len(d.token.label.texts)):

#     token_label = Box(*d.token.label.total)
#     token_label = fillet(token_label.edges().filter_by(Axis.Z), 0.4)
#     token_label -= align(
#         Box(
#             d.token.label.total[X] - 2 * d.token.label.border,
#             d.token.label.total[Y] - 2 * d.token.label.border,
#             d.token.label.font_height,
#         ),
#         ref=token_label,
#         center="xy",
#         end="z",
#     )

#     text = d.token.label.texts[i]
#     font_size = d.token.label.font_sizes[i]
#     token_label += align(
#         extrude(
#             Text(text, font_size=font_size, font_style=FontStyle.BOLD),
#             amount=d.token.label.font_height,
#         ),
#         ref=token_label,
#         center="xy",
#         end="z",
#     )

#     token_label_pins = None
#     for loc in GridLocations(x_spacing=7, y_spacing=7, x_count=3, y_count=1):
#         if token_label_pins == None:
#             token_label_pins = Plane.XY * loc * pin_bottom
#         else:
#             token_label_pins += Plane.XY * loc * pin_bottom

#     token_label += align(token_label_pins, ref=token_label, center="xy", endToBegin="z", margins=[0, 0, -0.5])

#     show(token_label)
#     token_label = token_label.rotate(Axis.X, 180)
#     # token_label.export_stl(f"library/insert_bugubi.token_label.{text}.stl")
#     export_stl(token_label, f"library/insert_gon.token_label.{text}.stl")


# # Text("Hello", font_size=fontsz, align=(Align.CENTER, Align.MIN)


# suporte_mini.export_stl("library/insert_bugubi.mini.stl")
# suporte_cartas.export_stl("library/insert_bugubi.cartas.stl")
# empty.export_stl("library/insert_bugubi.empty.stl")
# pin.export_stl("library/insert_bugubi.pin.stl")
# token.export_stl("library/insert_bugubi.token.stl")


# # with BuildPart() as insert:
# # with BuildSketch() as sk:
# #     Circle(d.geral[0] / 2)
# # extrude(amount=d.geral[2])

# # with BuildSketch(insert.faces().sort_by(Axis.Z)[-1]) as sk2:
# #     Circle(d.geral[0] / 2 - 1.2)

# # extrude(amount=-d.geral[2], mode=Mode.SUBTRACT)

# # show(insert)
