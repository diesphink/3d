from cadquery import Location
from ocp_vscode import show

# from gridfinity.gridfinity_scoops import GridfinityBox
from cqgridfinity import GridfinityBox
from sphlib import align, Dimensions, Slot, SlotPosition, SlotType
import gridfinity as gf

from build123d import (
    Align,
    Axis,
    Box,
    BuildPart,
    BuildSketch,
    Circle,
    Cylinder,
    Keep,
    Locations,
    Mode,
    Plane,
    Rectangle,
    Select,
    add,
    chamfer,
    extrude,
    fillet,
    loft,
    split,
)

# === Dimensions
X, Y, Z = 0, 1, 2
d = Dimensions()
d.clock = [35, 42, 11.45]
d.clock_fillet = 10
d.clock_bracelets = [25, 50]

d.clock_holder = [42, 50, 14]
d.clock_holder_fillet = 2

d.totem.bottom = [8, 18]
d.totem.margin_right = 3
d.totem.margin_cable = 6
d.totem.top = [8, 50]
d.totem.fillet.big = 2
d.totem.fillet.small = 1.5
d.totem.cable_radius = 3
d.totem.height = 70
d.totem.top_rotation = 35

with BuildPart() as clock:
    with BuildSketch() as sk:
        Rectangle(d.clock_holder[X], d.clock_holder[Y])
        fillet(sk.vertices(), radius=d.clock_holder_fillet)
    extrude(amount=d.clock_holder[Z])

    with BuildSketch(clock.faces().sort_by(Axis.Z)[-1]) as sk2:
        Rectangle(d.clock[X], d.clock[Y])
        fillet(sk2.vertices(), radius=d.clock_fillet)
        Rectangle(*d.clock_bracelets)
    extrude(amount=-d.clock[Z], mode=Mode.SUBTRACT)

    show(clock)

with BuildPart() as base:
    # gridfinity base
    gf = Box(1, 1, 1)
    gf.wrapped = (
        GridfinityBox(length_u=1, width_u=1, height_u=2, holes=True, solid=True, no_lip=True)
        .render()
        .objects[0]
        .wrapped
    )
    add(gf)

    top_face = gf.faces().group_by(Axis.Z)[-3][0]

    top_plane = Plane(top_face, x_dir=(1, 0, 0))

    # pos_x é metade da largura, tira meio retângulo, tira margem direita
    pos_x = base.part.bounding_box().size.X / 2 - d.totem.margin_right - d.totem.bottom[X] / 2

    # Sketch do retângulo inferior
    with BuildSketch(top_plane) as sk:
        with Locations((pos_x, 0)):
            Rectangle(*d.totem.bottom)
            fillet(sk.vertices(), radius=d.totem.fillet.big)
            with Locations((d.totem.bottom[X] / 2, -d.totem.bottom[Y] / 2 + d.totem.margin_cable)):
                Circle(d.totem.cable_radius, mode=Mode.SUBTRACT)

    # Sketch do retângulo superior, com rotação de 35º
    with BuildSketch(top_plane.offset(d.totem.height).rotated((d.totem.top_rotation, 0, 0))) as sk2:
        with Locations((pos_x, 0)):
            Rectangle(*d.totem.top)
            fillet(sk2.vertices(), radius=d.totem.fillet.big)
            with Locations((d.totem.top[X] / 2, -d.totem.top[Y] / 2 + d.totem.margin_cable)):
                Circle(d.totem.cable_radius, mode=Mode.SUBTRACT)

    # LOFT!
    loft()

    small_fillet_edges = (base.edges(Select.LAST)).group_by(Axis.Z)[0]
    fillet(small_fillet_edges, radius=d.totem.fillet.small)

    snap_edges = base.edges()
    # Buraco pro parafuso
    with BuildSketch(
        Plane(
            base.faces().group_by(Axis.Z)[-1][0].bounding_box().center(),
            z_dir=base.faces().group_by(Axis.Z)[-1][0].normal_at(),
        )
    ) as sk:
        Circle(1.6)
    extrude(amount=-10, mode=Mode.SUBTRACT)
    chamfer(base.edges(Select.LAST).group_by(Axis.Z)[-1], length=0.5)
    # show(part, part.edges(Select.LAST).group_by(Axis.Z)[-2])

    # show(base)

base.part.export_stl("library/gridfinity/banglejs2_base.stl")
base.part.export_step("library/gridfinity/banglejs2_base.step")


# Compare this snippet from models/gf_pen2.py:
# from ocp_vscode import show
