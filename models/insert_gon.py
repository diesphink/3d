# %%
from textwrap import fill
from build123d import (
    Axis,
    Box,
    BuildPart,
    BuildSketch,
    Circle,
    Cylinder,
    FontStyle,
    GridLocations,
    Mode,
    Plane,
    Rectangle,
    Rot,
    Sketch,
    Text,
    extrude,
    fillet,
    loft,
    export_stl,
)
from ocp_vscode import show


from sphlib import Dimensions, align, Slot
from sphlib.slots import SlotPosition, SlotType

# === Dimensions
X, Y, Z = 0, 1, 2
d = Dimensions()
d.geral = [89, 89, 25]
d.minicarta = [66, 45]
d.carta_grande = [68, 89, 3]

d.mini.total = [67, 40, 25]  # Tamanho do bloco que vai segurar a mini
d.mini.base.diameter = 25.4  # Diâmetro da base da mini
d.mini.base.height = 3.2  # Altura apenas da base da mini
d.mini.angle = 4  # Ângulo de inclinação da base da mini ao colocar no suporte
d.mini.margin = 2.2  # Distância entre os limites da base e os limites da miniatura
d.mini.paredes = 2  # Tamanho das paredes ao redor da mini


# === Suporte Mini
suporte_mini = Box(*d.mini.total)
suporte_mini = fillet(suporte_mini.edges().filter_by(Axis.Z), 1)
mini = Cylinder(d.mini.base.diameter / 2, d.mini.base.height)
mini += align(Box(d.mini.base.diameter, d.mini.base.diameter / 2, d.mini.base.height), ref=mini, begin="xyz")
mini += align(Cylinder(d.mini.base.diameter / 2 - d.mini.margin, 80), ref=mini, beginToEnd="z")
mini += align(
    Box(d.mini.base.diameter - 2 * d.mini.margin, d.mini.base.diameter / 2, 80),
    ref=mini,
    begin="y",
    center="x",
    end="z",
)
mini = mini.rotate(Axis.X, -90 + d.mini.angle).rotate(Axis.Z, -90)
suporte_mini -= align(mini, ref=suporte_mini, center="y", begin="xz", margins=[d.mini.paredes, 0, 0]).translate(
    [0, 2, -0.4]
)
suporte_mini -= align(
    Box(d.mini.total[X] - d.mini.base.height - 2 * d.mini.paredes, d.mini.total[Y] - d.mini.paredes, d.mini.total[Z]),
    ref=suporte_mini,
    begin="y",
    end="xz",
)


# === Suporte Cartas

d.small.total = [67, 49, 25]
d.small.floor = 0.6

suporte_cartas = Box(*d.small.total)
suporte_cartas = fillet(suporte_cartas.edges().filter_by(Axis.Z), 1)
slot = Slot(
    Box(d.minicarta[X], d.minicarta[Y], d.small.total[Z] - d.small.floor),
    SlotPosition.Y_AXIS_MAX,
    (d.small.total[Z] - d.small.floor) * 2,
    SlotType.SPHERE,
)
suporte_cartas -= align(slot, ref=suporte_cartas, begin="xy", end="z", margins=[0, 2, 0])
suporte_cartas = align(suporte_cartas, ref=suporte_mini, begin="xz", endToBegin="y")

# === Empty

d.empty = [22, 89, 25]
empty = Box(*d.empty)
empty = fillet(empty.edges().filter_by(Axis.Z), 1)
empty = align(empty, ref=suporte_cartas, begin="yz", beginToEnd="x")


# === Buraco das cartas grandes

cartas_grandes = align(Box(*d.carta_grande), ref=empty, end="xyz")

suporte_cartas -= cartas_grandes
suporte_mini -= cartas_grandes
empty -= cartas_grandes


# show(suporte_mini)

all = suporte_mini + suporte_cartas + empty


# === Token

d.token.total = [22, 89, 25 - 2]  # z minus 2mm for felt
d.token.hole = [4, 4, 4]
d.token.pin.bottom = [3.7, 3.7, 4]
d.token.pin.top.radius = 2.5
d.token.pin.top.height = 4

token = Box(d.token.total[X], d.token.total[Y], d.token.total[Z] - d.token.pin.top.height)
token = fillet(token.edges(), 1)

token_holes = None
for loc in GridLocations(x_spacing=7, y_spacing=10, x_count=3, y_count=9):
    if token_holes == None:
        token_holes = Plane.XY * loc * Box(*d.token.hole)
    else:
        token_holes += Plane.XY * loc * Box(*d.token.hole)

token -= align(token_holes, ref=token, center="xy", end="z")

# show(token)

# === Pin

pin = Box(*d.token.pin.bottom)
# pin = fillet(pin.edges().filter_by(Axis.Z), 0.5)
pin_bottom = fillet(pin.edges().group_by(Axis.Z)[:-1], 0.5)


pin_top = align(
    Cylinder(d.token.pin.top.radius, d.token.pin.top.height * 4 / 5),
    ref=pin,
    center="xy",
    beginToEnd="z",
    margins=[0, 0, d.token.pin.top.height / 5],
)

# faces = Sketch() + [
# pin_top.faces().sort_by(Axis.Z).first() * Circle(d.token.pin.top.radius),
# pin_.offset(length / 2) * Rectangle(length / 6, width / 6),
# ]

pin_loft = loft([pin_top.faces().sort_by(Axis.Z).first, pin_bottom.faces().sort_by(Axis.Z).last])
pin = pin_bottom + pin_top + pin_loft
pin = pin.rotate(Axis.X, 180)


# === Pin Label

d.token.label.total = [22, 7, 1]
d.token.label.texts = ["INSPIR", "1ST LVL", "2ND LVL", "WLD SHP", "HIT DIE", "3RD LVL", "4TH LVL"]
d.token.label.font_sizes = [5, 5, 5, 4.3, 5, 5, 5]
d.token.label.font_height = 0.4
d.token.label.border = 0.8

for i in range(len(d.token.label.texts)):

    token_label = Box(*d.token.label.total)
    token_label = fillet(token_label.edges().filter_by(Axis.Z), 0.4)
    token_label -= align(
        Box(
            d.token.label.total[X] - 2 * d.token.label.border,
            d.token.label.total[Y] - 2 * d.token.label.border,
            d.token.label.font_height,
        ),
        ref=token_label,
        center="xy",
        end="z",
    )

    text = d.token.label.texts[i]
    font_size = d.token.label.font_sizes[i]
    token_label += align(
        extrude(
            Text(text, font_size=font_size, font_style=FontStyle.BOLD),
            amount=d.token.label.font_height,
        ),
        ref=token_label,
        center="xy",
        end="z",
    )

    token_label_pins = None
    for loc in GridLocations(x_spacing=7, y_spacing=7, x_count=3, y_count=1):
        if token_label_pins == None:
            token_label_pins = Plane.XY * loc * pin_bottom
        else:
            token_label_pins += Plane.XY * loc * pin_bottom

    token_label += align(token_label_pins, ref=token_label, center="xy", endToBegin="z", margins=[0, 0, -0.5])

    show(token_label)
    token_label = token_label.rotate(Axis.X, 180)
    # token_label.export_stl(f"library/insert_bugubi.token_label.{text}.stl")
    export_stl(token_label, f"library/insert_gon.token_label.{text}.stl")


# Text("Hello", font_size=fontsz, align=(Align.CENTER, Align.MIN)


suporte_mini.export_stl("library/insert_bugubi.mini.stl")
suporte_cartas.export_stl("library/insert_bugubi.cartas.stl")
empty.export_stl("library/insert_bugubi.empty.stl")
pin.export_stl("library/insert_bugubi.pin.stl")
token.export_stl("library/insert_bugubi.token.stl")


# with BuildPart() as insert:
# with BuildSketch() as sk:
#     Circle(d.geral[0] / 2)
# extrude(amount=d.geral[2])

# with BuildSketch(insert.faces().sort_by(Axis.Z)[-1]) as sk2:
#     Circle(d.geral[0] / 2 - 1.2)

# extrude(amount=-d.geral[2], mode=Mode.SUBTRACT)

# show(insert)
