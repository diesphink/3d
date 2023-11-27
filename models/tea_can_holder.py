from ocp_vscode import show

from sphlib import Dimensions

from build123d import (
    Axis,
    Box,
    BuildPart,
    BuildSketch,
    Circle,
    Ellipse,
    Locations,
    Mode,
    Plane,
    Rectangle,
    SlotCenterToCenter,
    extrude,
    fillet,
)

# === Dimensions
X, Y, Z = 0, 1, 2
d = Dimensions()
d.box = [72, 92, 102.5]
d.bottom = 2
d.walls = 3
d.floors = 2
d.border_radius = 2.5

d.magnets.radius = 5.125
d.magnets.height = 2.2
d.magnets.padding = [19.25, 23.1535]
d.magnets.space = [33.5, 56.193]

d.side_slot.radius = 15.956
d.side_slot.height = 44.127

with BuildPart() as tea_can_holder:
    # === Base
    Box(*d.box)
    fillet(tea_can_holder.edges().filter_by(Axis.Z), radius=d.border_radius)

    # === Magnets
    with BuildSketch(Plane(tea_can_holder.faces().sort_by(Axis.Y)[-1], x_dir=(1, 0, 0))) as sk:
        with Locations((-d.magnets.space[X] / 2, -d.magnets.space[Y] / 2)):
            with Locations(
                (0, 0), (0, d.magnets.space[Y]), (d.magnets.space[X], 0), (d.magnets.space[X], d.magnets.space[Y])
            ):
                Circle(d.magnets.radius)
    extrude(amount=-d.magnets.height, mode=Mode.SUBTRACT)

    # === Shelves
    with BuildSketch(tea_can_holder.faces().sort_by(Axis.Y)[0]) as sk:
        Rectangle(d.box[Z] - 2 * d.floors, d.box[X] - 2 * d.walls)
        Rectangle(d.floors, d.box[X], mode=Mode.SUBTRACT)
    extrude(amount=-d.box[Y] + d.walls, mode=Mode.SUBTRACT)

    # Ellipse holes in front
    with BuildSketch(Plane(tea_can_holder.faces().sort_by(Axis.Z)[0], x_dir=(0, 1, 0))) as sk:
        with Locations((-d.box[Y] / 2, 0)):
            Ellipse(y_radius=d.box[X] / 2 - d.walls, x_radius=20)
    extrude(amount=-d.box[Z] + d.walls, mode=Mode.SUBTRACT)

    # Side slots
    planes = (
        Plane(tea_can_holder.faces().sort_by(Axis.X)[0], x_dir=(0, 0, 1)),
        Plane(tea_can_holder.faces().sort_by(Axis.X)[-1], x_dir=(0, 0, 1)),
    )
    for plane in planes:
        with BuildSketch(plane) as sk:
            SlotCenterToCenter(d.side_slot.height, d.side_slot.radius * 2)
        extrude(amount=-d.walls, mode=Mode.SUBTRACT)

show(tea_can_holder)
tea_can_holder.part.export_stl("library/tea_can_holder.stl")
tea_can_holder.part.export_step("library/tea_can_holder.step")
