# %%
from ocp_vscode import show
from sphlib import Dimensions, align

from build123d import *
from bd_warehouse.fastener import *

# === Dimensions
X, Y, Z = 0, 1, 2

d = Dimensions()
d.bg = 0.8
d.txt = 1.2


print(import_svg("models/fadamachado/fada-txt.svg"))
fada_bg = extrude(import_svg("models/fadamachado/fada-bg.svg"), d.bg)
# show( )
fada_txt = extrude(import_svg("models/fadamachado/fada-txt.svg"), d.txt)
# show(fada_txt)

# %%

d.sup = [51, 51, 72]
d.wall = 3
d.parafuso.corpo = [3.7, 3.7, d.wall * 3 + 0.5]
d.parafuso.cab = [7.5, 7.5, 2.5]

base = Cylinder(radius=d.sup[X] / 2 + d.wall, height=d.sup[Z] + d.wall)
hole = align(Cylinder(radius=d.sup[X] / 2, height=d.sup[Z]), ref=base, center="xy", end="z")
base -= align(Box(d.sup[X] + 2 * d.wall, d.sup[Y] / 2 + d.wall, d.sup[Z] - d.wall), ref=base, center="x", end="yz")
base += align(
    Box(d.sup[X] + 2 * d.wall, d.sup[Y] / 2 + d.wall * 3, d.sup[Z] + d.wall),
    ref=base,
    center="x",
    begin="zy",
    margins=[0, -d.wall * 2, 0],
)
base -= hole

parafuso = Cylinder(radius=d.parafuso.corpo[X] / 2, height=d.parafuso.corpo[Z])
parafuso += align(
    Cylinder(radius=d.parafuso.cab[X] / 2, height=d.parafuso.cab[Z]),
    ref=parafuso,
    center="xy",
    begin="z",
)
base -= align(parafuso.rotate(Axis.X, 90), ref=base, center="x", begin="y", end="z", margins=[0, 0, d.wall])
base -= align(
    parafuso.rotate(Axis.X, 90),
    ref=base,
    center="x",
    begin="y",
    end="z",
    margins=[0, 0, d.wall * 2 + d.parafuso.cab[X]],
)
# show(parafuso)
show(base)
# base.export_stl("library/lavanderia/suporte.stl")
export_stl(base, "library/lavanderia/suporte.stl")
# %%

# === Base via sketch
side = Plane.ZY * Polygon([(d.base_frente, 0), (0, 0), (0, d.base[Y]), (d.base[Z], d.base[Y])])
base = extrude(side, d.base[X])

snapshot = base.edges()

base -= align(Cylinder(radius=d.jarro, height=d.base[Z]), ref=base, center="x", begin="yz", margins=[0, 25, 0])

# plane = Plane(base.faces().filter_by(Axis.Z).sort_by(Axis.X).last)
# base -= extrude(plane * Location(d.translate_jarro) * Circle(d.jarro), amount=-d.base[Z])
base = fillet(base.edges() - snapshot, 8)


screw = ClearanceHole(fastener=CounterSunkScrew(fastener_type="iso7046", size="M4-0.7", length=40 * MM), depth=60 * MM)

# base -= align(screw, ref=base, centerToBegin="xy", endToBegin="z", margins=[10, 10, -15])
# base -= align(Cylinder(radius=5, height=d.base[Z]), ref=base, centerToBegin="xy", begin="z", margins=[10, 10, 15])

# base -= align(screw, ref=base, centerToBegin="y", centerToEnd="x", endToBegin="z", margins=[10, 10, -15])
# base -= align(
#     Cylinder(radius=5, height=d.base[Z]), ref=base, centerToBegin="y", centerToEnd="x", begin="z", margins=[10, 10, 15]
# )

base -= align(screw, ref=base, centerToBegin="x", centerToEnd="y", endToBegin="z", margins=[10, 10, -15])
base -= align(
    Cylinder(radius=5, height=d.base[Z]), ref=base, centerToBegin="x", centerToEnd="y", begin="z", margins=[10, 10, 15]
)


base -= align(screw, ref=base, centerToEnd="xy", endToBegin="z", margins=[10, 10, -15])
base -= align(Cylinder(radius=5, height=d.base[Z]), ref=base, centerToEnd="xy", begin="z", margins=[10, 10, 15])

base -= align(screw, ref=base, centerToBegin="y", center="x", endToBegin="z", margins=[0, 10, -15])
base -= align(
    Cylinder(radius=5, height=d.base[Z]), ref=base, centerToBegin="y", center="x", begin="z", margins=[0, 10, 15]
)


show(base)


# plane = plane * Location((-d.base[Y] / 2, -d.base[X] / 2))

# base =

# suporte_beckerg = base - extrude(plane * Circle(d.beckerg), amount=-d.base[Z])

becker_g = Cylinder(radius=d.beckerg, height=d.base[Z])
becker_p = Cylinder(radius=d.beckerp, height=d.base[Z])


base_g = base - align(becker_g, ref=base, begin="yz", centerToEnd="x", margins=[0, 5, 2])
# base_g = fillet(base_g.edges().filter_by(GeomType.ELLIPSE) + base_g.edges().filter_by(GeomType.CIRCLE), 5)

base_gp = base - align(becker_g, ref=base, begin="yz", centerToBegin="x", margins=[0, 5, 2])
base_gp = base_gp - align(becker_p, ref=base, begin="yz", end="x", margins=[5, 5, 2])
edges = base_gp.edges().filter_by(GeomType.ELLIPSE) + base_gp.edges().filter_by(GeomType.CIRCLE)
# base_gp = fillet(edges, 3)

base_gg = base - align(becker_g, ref=base, begin="yz", centerToEnd="x", margins=[0, 5, 2])
base_gg = base_gg - align(becker_g, ref=base, begin="yz", centerToBegin="x", margins=[0, 5, 2])
# base_gg = fillet(base_gg.edges().filter_by(GeomType.ELLIPSE) + base_gg.edges().filter_by(GeomType.CIRCLE), 5)


base_p = base - align(becker_p, ref=base, begin="yz", end="x", margins=[5, 5, 2])
edges = base_p.edges().filter_by(GeomType.ELLIPSE) + base_p.edges().filter_by(GeomType.CIRCLE)
# base_p = fillet(edges, 3)

# extrude(base.faces().sort_by(Axis.Z).first.make_plane() * Circle(d.jarro / 2), d.base[Z], mode=Mode.SUBTRACT)

mirror_base_p = base_p.mirror(Plane.ZY.offset(d.base[X] / 2))
mirror_base_g = base_g.mirror(Plane.ZY.offset(d.base[X] / 2))
mirror_base_gp = base_gp.mirror(Plane.ZY.offset(d.base[X] / 2))

show(base_gp)

# print(Screw)

# screw = ClearanceHole(fastener=CounterSunkScrew(fastener_type="iso7046", size="M4-0.7", length=40 * MM), depth=60 * MM)

# screw = align(Box(13, 13, 8), ref=screw, center="xy", end="z") - screw

# show(screw)


base_g.export_stl("library/lavanderia/base_g.stl")
base_gp.export_stl("library/lavanderia/base_gp.stl")
base_p.export_stl("library/lavanderia/base_p.stl")
base_gg.export_stl("library/lavanderia/base_gg.stl")
mirror_base_g.export_stl("library/lavanderia/mirror_base_g.stl")
mirror_base_gp.export_stl("library/lavanderia/mirror_base_gp.stl")
mirror_base_p.export_stl("library/lavanderia/mirror_base_p.stl")

screw.export_stl("library/lavanderia/screw.stl")
