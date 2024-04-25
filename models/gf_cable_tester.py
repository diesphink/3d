from cadquery import Location
from ocp_vscode import show

from sphlib import Dimensions, align
import gridfinity as gf

from build123d import (
    Axis,
    Box,
    BuildPart,
    BuildSketch,
    Circle,
    ExportSVG,
    Mode,
    Rectangle,
    Shape,
    chamfer,
    extrude,
    fillet,
)

from sphlib.slots import Slot, SlotPosition, SlotType

# === Dimensions
X, Y, Z = 0, 1, 2
d = Dimensions()
d.size = [68, 107, 28]
d.fillet = 2


base = gf.GridfinityFilled(x_grid_number=2, y_grid_number=3, unit_height=5, disable_mholes=True)
slot1 = Box(*d.size)
# slot1 = fillet(slot1.edges().filter_by(Axis.Z), d.fillet)

slot = Slot(slot1, SlotPosition.Y_AXIS, 12, SlotType.SPHERE)
edges1 = base.edges()
base -= align(slot, ref=base, center="xy", end="z", margins=[0, 0, 3.85])
delta = base.edges() - edges1
base = fillet(delta.group_by(Axis.Z)[-1], 3)


show(base)


# base = gf.GridfinityFilled(x_grid_number=7, y_grid_number=3, unit_height=5, disable_mholes=True)
# slot1 = Box(*d.size)
# slot1 = fillet(slot1.edges().filter_by(Axis.Z), d.fillet.big)

# slot2 = Box(*d.handle)
# slot2 = fillet(slot2.edges().filter_by(Axis.Z), d.fillet.small)
# slot2 = align(slot2, ref=slot1, center="y", end="xz", margin=0)

# slot = Slot(slot1 + slot2, SlotPosition.Y_AXIS_MIN, 25, SlotType.SPHERE)
# base -= align(slot, ref=base, begin="x", center="y", end="z", margins=[2, 0, 3.85])

# slot3 = Box(104, 107, 28)
# slot3 = fillet(slot3.edges().filter_by(Axis.Z), d.fillet.small)
# slot = Slot(slot3, SlotPosition.Y_AXIS_MIN, 25, SlotType.SPHERE)

# base -= align(slot, ref=base, center="y", end="xz", margins=[2, 0, 3.85])

# show(base)

base.export_stl("library/gridfinity/gf_cable_tester1.stl")
base.export_step("library/gridfinity/gf_cable_tester1.step")


# logo.export_step("logo.step")
def add_svg_shape(svg: ExportSVG, shape: Shape, color: tuple[float, float, float]):
    global counter
    try:
        counter += 1
    except:
        counter = 1

    visible, _hidden = shape.project_to_viewport((-5, 1, 10), viewport_up=(0, 1, 0), look_at=(0, 0, 0))
    if color is not None:
        svg.add_layer(str(counter), fill_color=color, line_weight=1)
    else:
        svg.add_layer(str(counter), line_weight=1)
    svg.add_shape(visible, layer=str(counter))


svg = ExportSVG(scale=1)
# add_svg_shape(svg, base, None)
svg.add_layer("1", fill_color=(255, 255, 255), line_weight=0.1)
visible, hidden = base.project_to_viewport((0, 20, 20))
svg.add_shape(visible, layer="1")
# add_svg_shape(svg, Compound(children=[one.line, extension_lines.line]), None)
# add_svg_shape(svg, Compound(children=[two.sketch, build.sketch]), (170, 204, 255))
# add_svg_shape(svg, three_d.part, (85, 153, 255))
svg.write("teste.svg")
