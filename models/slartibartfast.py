from ocp_vscode import show
from honeycomb import HoneycombGrid
from sphlib import Dimensions, align

from build123d import Box, Cylinder, Part, Plane, Rot, chamfer, fillet


d = Dimensions()
d.base = [159, 97, 2]
d.radius_screw = 3.5 / 2
d.margins1 = [4.5, 97 - 7 - 84.5, 0]
d.margins2 = [3, 7, 0]

base = Box(*d.base)
base += align(Plane.XY * Rot(0, 180, 90) * HoneycombGrid([3, 3, 3, 3, 3, 3, 3]), ref=base, center="xy", endToBegin="z")
base -= align(Cylinder(radius=d.radius_screw, height=20), ref=base, centerToBegin="xy", center="z", margins=d.margins1)
base -= align(Cylinder(radius=d.radius_screw, height=20), ref=base, centerToEnd="xy", center="z", margins=d.margins2)
show(base)


(Rot(180, 0, 0) * base).export_stl("library/slartibartfast/fonte.stl")
