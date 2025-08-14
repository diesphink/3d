# %%
from ocp_vscode import *
from sphlib import align, Dimensions, distribute, rescale_chamfer
from enum import Enum

from build123d import *

# === Dimensions
X, Y, Z = 0, 1, 2

# %%
d = Dimensions()
d.external = [35, 60, 6]
d.external_fillet = 2.5
d.bump = [d.external[X] - 2 * d.external_fillet, 2.5, 1.95]
d.gap = 0.35
d.cylinder.radius = 2.35
d.gap_printinplace = 0.15
d.sphere_female = 1.5
d.sphere_male = 1.45
d.border = 1.2


# %%


def gen_base(length=d.external[X], width=d.external[Y], height=d.external[Z], border=d.border):
    base = Box(length=length, width=width, height=height)
    base = chamfer(objects=base.edges().filter_by(Axis.Z), length=d.external_fillet)

    innerbox = Box(length=length - border * 2, width=width - border * 2, height=0.6)
    innerbox = chamfer(objects=innerbox.edges().filter_by(Axis.Z), length=rescale_chamfer(d.external_fillet, border))

    base -= align(innerbox, ref=base, center="xy", end="z")

    return base


class HingeType(Enum):
    MALE = 1
    FEMALE = 2


def add_hinge(base, flip=True, type=HingeType.MALE):
    base = base.rotate(Axis.Y, 180) if flip else base
    length = base.bounding_box().size.X - 2 * d.external_fillet

    # Little bump over the edge of base, to limit the hinge movement
    d.bump = [length, 2.5, 1.95]
    bump = align(
        Box(length=d.bump[X], width=d.bump[Y], height=d.bump[Z]), ref=base, end="y", center="x", beginToEnd="z"
    )

    # Hinge
    d.hinge = [(length - 2 * d.gap) / 3, d.cylinder.radius * 2 + d.gap_printinplace, d.external[Z] + d.bump[Z]]
    # if type == HingeType.MALE:
    #     d.hinge[X] = d.hinge[X] * 2

    # Wedge under the hinge
    hinge = Wedge(
        xsize=d.hinge[X],
        ysize=d.hinge[Y],
        zsize=d.external[Z],
        xmin=0,
        xmax=d.hinge[X],
        zmin=d.external[Z],
        zmax=d.external[Z],
    )

    # Extra height for the wedge
    hinge += align(
        Box(length=d.hinge[X], width=d.hinge[Y], height=d.bump[Z]),
        ref=hinge,
        begin="z",
        center="x",
        beginToEnd="z",
    )

    hinge = align(hinge, ref=base, beginToEnd="y", begin="z")

    # Hinge cylinder
    hinge_cylinder = Cylinder(radius=d.cylinder.radius, height=d.hinge[X]).rotate(Axis.Y, 90)
    hinge_cylinder = align(hinge_cylinder, ref=hinge, end="y", center="x", centerToEnd="z")

    if type == HingeType.MALE:
        hinge_cylinder += align(Sphere(radius=d.sphere_male), ref=hinge_cylinder, center="yz", centerToBegin="x")
        hinge_cylinder += align(Sphere(radius=d.sphere_male), ref=hinge_cylinder, center="yz", centerToEnd="x")
        hinge += hinge_cylinder
    if type == HingeType.FEMALE:
        hinge = (
            hinge
            + hinge_cylinder
            - align(Sphere(radius=d.sphere_female), ref=hinge_cylinder, center="yz", centerToEnd="x")
        )
        hinge = align(hinge, bump, begin="x")
        hinge = hinge + align(mirror(hinge, Plane.YZ), bump, end="x")

    return base, bump, hinge


def position_bases(side1, side2):
    side1 = sum(side1, start=Part())
    side2 = sum(side2, start=Part())

    side2 = side2.rotate(Axis.Z, 180)
    side2 = align(side2, ref=side1, begin="z", center="x", beginToEnd="y", margins=[0, -d.cylinder.radius * 2, 0])

    return side1 + side2


def make_vertical_text(base, text, font_size=10, height=5, margin=3):
    letras = []
    for letra in text:
        letras.append(
            extrude(Text(letra, font="Cambria", font_style=FontStyle.BOLD, font_size=font_size), amount=height)
        )

    for i, letra in enumerate(letras):
        letras[i] = align(letra, ref=base, center="x", end="z")
    letras[0] = align(letras[0], ref=base, end="y", margins=[0, margin, 0])
    letras[2] = align(letras[2], ref=base, begin="y", end="z", margins=[0, margin, 0])
    letras = distribute(list(reversed(letras)), center="y")

    return letras


def make_field_icon(icon, field):
    return align(
        extrude(Text(icon, font="Ubuntu Nerd Font", font_size=5, font_style=FontStyle.BOLD), amount=5),
        ref=field,
        begin="x",
        center="y",
        end="z",
        margins=[d.border, 0, 0],
    )


def make_field(length=20, ratio=0.5):
    field = Box(length=length - 4 * d.border, width=(length - 4 * d.border) * ratio, height=5)
    field = chamfer(
        field.edges().filter_by(Axis.Z), length=rescale_chamfer(rescale_chamfer(d.external_fillet, d.border), d.border)
    )
    return field


def make_small_icon_field(icon, length=20, ratio=0.5):
    field = make_field(length, ratio)
    field -= make_field_icon(icon, field)
    return field


def make_pc_tracker(
    player_text,
    dm_text,
    player_size=20,
    dm_size=40,
    player_font_size=14,
    dm_font_size=10,
    length=20,
):

    base1 = gen_base(length=length, width=player_size)

    base1 += make_vertical_text(base1, player_text, font_size=player_font_size, height=5, margin=3)
    base1 = add_hinge(base1, type=HingeType.MALE)

    base2 = gen_base(length, dm_size)

    field1 = align(
        make_small_icon_field("\uf132"), ref=base2, end="z", center="x", begin="y", margins=[0, d.border * 2, 0]
    )
    field2 = align(
        make_small_icon_field("\uf004"), ref=field1, end="z", center="x", beginToEnd="y", margins=[0, d.border, 0]
    )
    field3 = align(
        make_small_icon_field("󰈈"), ref=field2, end="z", center="x", beginToEnd="y", margins=[0, d.border, 0]
    )

    text = align(
        extrude(Text(dm_text, font="Impact", font_size=dm_font_size, font_style=FontStyle.BOLD), amount=5),
        ref=base2,
        center="x",
        end="zy",
        margins=[0, d.border * 2, 0],
    )

    base2 = base2 + field1 + field2 + field3 + text

    base2 = add_hinge(base2, type=HingeType.FEMALE)

    tracker = position_bases(base1, base2)
    show(tracker)

    export_stl(Compound(tracker), f"library/trackers/{player_text}.stl")
    print(f"library/trackers/{player_text}.stl exported")
    return tracker


def make_dm_tracker(length=20, dm_size=32, player_size=33, icon="󰀦", player_icon_size=12, font="Ubuntu Nerd Font"):
    player_size = (length - d.border * 4) * 2 + d.border * 5

    base1 = gen_base(length=length, width=player_size)
    base1 += align(make_field(ratio=1), ref=base1, end="z", center="x", begin="y", margins=[0, d.border * 2, 0])
    ref = align(make_field(ratio=1), ref=base1, end="zy", center="x", margins=[0, d.border * 2, 0])
    # base1 += ref
    base1 += align(
        extrude(Text(icon, font=font, font_size=player_icon_size, font_style=FontStyle.BOLD), amount=5),
        ref=ref,
        center="xy",
        end="z",
        margins=[0, d.border * 2, 0],
    )

    base2 = add_hinge(base1, type=HingeType.FEMALE)
    base1 = add_hinge(base1, type=HingeType.MALE)

    tracker = position_bases(base1, base2)

    export_stl(Compound(tracker), f"library/trackers/{icon}.stl")
    print(f"library/trackers/{icon}.stl exported")
    return tracker


# icons = ["", "󱢾", "󰓥", "󰈈", "", "", "", "󰱩", "", "󰱯", "", "", "󰀦"]
# icons = ["󱢾"]
# for icon in icons:
#     show(make_dm_tracker(icon=icon)

# icons = ["1", "2", "3", "4", "5", "6"]
icons = ["A", "B", "C"]

for icon in icons:
    show(make_dm_tracker(icon=icon, font="Cambria"))


# show(make_pc_tracker("BUGUBI", "BGB", player_size=70))
# show(make_pc_tracker("FARPA", "FRP", player_size=60))
# show(make_pc_tracker("LANZARA", "LNZ", player_size=80))
# show(make_pc_tracker("PIP", "PIP", player_size=38))
show(make_pc_tracker("COXIBE", "CXB", player_size=70))
show(make_pc_tracker("KOSHIBE", "KSB", player_size=80))
# show(make_pc_tracker("GOODORIAN", "GOD", player_size=100))
