from ocp_vscode import show
from build123d import Box, Plane, Pos, Text

from sphlib import align

axes = ["x", "y", "z"]
centeredAxis = ["y", "x", "y"]
hoverAxis = ["z", "z", "x"]

labels = [
    "endToBegin",
    "centerToBegin",
    "begin",
    "endToCenter",
    "center",
    "beginToCenter",
    "end",
    "centerToEnd",
    "beginToEnd",
]

cubes1 = []
cubes2 = []
texts = []
for i in range(3):
    axis = axes[i]
    for anchor in range(9):
        pos = Pos(
            70 * (anchor + 1) if axis == "x" else 0,
            50 * (anchor + 1) if axis == "y" else 0,
            50 * (anchor + 1) if axis == "z" else 0,
        )

        box1 = pos * Box(50, 30, 30)
        box2 = align(Box(10, 10, 10), ref=box1, beginToEnd=hoverAxis[i], center=centeredAxis[i])
        if anchor == 0:
            box2 = align(box2, ref=box1, endToBegin=axis)
        if anchor == 1:
            box2 = align(box2, ref=box1, centerToBegin=axis)
        if anchor == 2:
            box2 = align(box2, ref=box1, begin=axis)
        if anchor == 3:
            box2 = align(box2, ref=box1, endToCenter=axis)
        if anchor == 4:
            box2 = align(box2, ref=box1, center=axis)
        if anchor == 5:
            box2 = align(box2, ref=box1, beginToCenter=axis)
        if anchor == 6:
            box2 = align(box2, ref=box1, end=axis)
        if anchor == 7:
            box2 = align(box2, ref=box1, centerToEnd=axis)
        if anchor == 8:
            box2 = align(box2, ref=box1, beginToEnd=axis)

        text = Plane.XZ * Text(labels[anchor], font_size=7)

        cubes1.append(box1)
        cubes2.append(box2)
        texts.append(align(text, ref=box1, center="xz", endToBegin="y"))

show(cubes1, cubes2, texts, colors=["coral", "darkseagreen", "black"])
