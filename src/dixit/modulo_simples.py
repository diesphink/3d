# from attrdict import AttrDict
from ocp_vscode import show

from build123d import (
    Axis,
    Box,  # noqa: F401, E501
    Vector,
    chamfer,
    fillet,  # noqa: F401, E501
)


def vector_to_array(vector):
    return [vector.X, vector.Y, vector.Z]


def align(
    object,
    ref=None,
    begin="",
    center="",
    end="",
    beginToCenter="",
    beginToEnd="",
    centerToBegin="",
    centerToEnd="",
    endToBegin="",
    endToCenter="",
    margins=[0, 0, 0],
    margin=0,
):
    # pontos do objeto (begin, end e center)
    bObj = vector_to_array(object.bounding_box().min)
    eObj = vector_to_array(object.bounding_box().max)
    cObj = vector_to_array((object.bounding_box().min + object.bounding_box().max) / 2)

    print(bObj, eObj, cObj)

    # Pontos do ref (begin, end e center)
    if ref is None:
        bRef = eRef = cRef = [0, 0, 0]
    else:
        bRef = vector_to_array(ref.bounding_box().min)
        eRef = vector_to_array(ref.bounding_box().max)
        cRef = vector_to_array((ref.bounding_box().min + ref.bounding_box().max) / 2)
    # TODO: Adicionar opção para array
    # else:
    #     bRef = eRef = cRef = ref

    deltas = [0, 0, 0]

    begin = begin.lower()
    center = center.lower()
    end = end.lower()
    beginToCenter = beginToCenter.lower()
    beginToEnd = beginToEnd.lower()
    centerToBegin = centerToBegin.lower()
    centerToEnd = centerToEnd.lower()
    endToBegin = endToBegin.lower()
    endToCenter = endToCenter.lower()

    axes = ["x", "y", "z"]
    for i, axis in enumerate(axes):
        from_ = None
        to_ = None

        # Which part of the object...
        if axis in begin or axis in beginToCenter or axis in beginToEnd:
            print("from begin: " + axis)
            from_ = bObj[i]
            deltas[i] = margins[i] + margin

        if axis in centerToBegin or axis in center or axis in centerToEnd:
            print("from center: " + axis)
            from_ = cObj[i]

        if axis in endToBegin or axis in endToCenter or axis in end:
            print("from end: " + axis)
            from_ = eObj[i]
            deltas[i] = -margins[i] - margin

        # ...is aligned to which part of the ref
        if axis in begin or axis in centerToBegin or axis in endToBegin:
            print("to begin: " + axis)
            to_ = bRef[i]
        if axis in beginToCenter or axis in center or axis in endToCenter:
            print("to center: " + axis)
            to_ = cRef[i]
        if axis in beginToEnd or axis in centerToEnd or axis in end:
            print("to end: " + axis)
            to_ = eRef[i]

        if from_ is not None and to_ is not None:
            deltas[i] = deltas[i] + to_ - from_

    return object.translate(Vector(deltas[0], deltas[1], deltas[2]))


X, Y, Z = 0, 1, 2

d = {
    "module": [135, 90, 54],
    "wall": 3,
    "floor": 0.4,
    "card": [126, 84, 36 / 100],
    "score": [118, 250, 6],
    "guess": [118, 76, 22],
    "token": [50, 64, 24],
}

module = Box(*d["module"])

cards_slot = Box(d["card"][X], d["card"][Y], d["module"][Z] - d["floor"])
finger_slot = Box(25, 25, d["module"][Z] - d["floor"])
score_slot = Box(*d["score"])
guess_slot = Box(*d["guess"])
token_slot = Box(*d["token"])

module -= align(cards_slot, module, begin="x", end="z", margins=[d["wall"], 0, 0])
module -= align(finger_slot, module, center="y", end="xz")

module2 = module.copy()
module2 -= align(score_slot, module2, center="xy", end="z")
module2 = align(module2, module, beginToEnd="y", margin=2)

module3 = Box(*d["module"])
module3 = align(module3, module2, beginToEnd="y", margin=2)
module3 -= align(score_slot, module3, center="xy", end="z")
guess_slot = align(guess_slot, module3, center="xy", end="z", margins=[0, 0, d["score"][Z]])
module3 -= guess_slot
module3 -= align(finger_slot, guess_slot, begin="z", beginToEnd="x", center="y")
module3 -= align(token_slot, guess_slot, endToBegin="z", begin="x", center="y", margins=[6, 0, 0])
module3 -= align(token_slot, guess_slot, endToBegin="z", end="x", center="y", margins=[6, 0, 0])

module = chamfer(module.edges().group_by(Axis.Z)[-1], 1)
module = fillet(module.edges().group_by(Axis.Z)[1].group_by(Axis.X)[3], 10)

module2 = chamfer(module2.edges().group_by(Axis.Z)[-1], 1)
module2 = fillet(module2.edges().group_by(Axis.Z)[1].group_by(Axis.X)[3], 10)

fillet_edges = module3.edges().group_by(Axis.Z)[1]
fillet_edges += module3.edges().group_by(Axis.Z)[3].group_by(Axis.X)[-2]

module3 = fillet(fillet_edges, 10)

chamfer_edges = module3.edges().group_by(Axis.Z)[-1]
chamfer_edges += module3.edges().group_by(Axis.Z)[-3].group_by(Axis.Y)[2]
chamfer_edges += module3.edges().group_by(Axis.Z)[-3].group_by(Axis.Y)[3]

# show(module3, module3.edges().group_by(Axis.Z)[-9])

chamfer_edges += module3.edges().group_by(Axis.Z)[-9].group_by(Axis.X)[1]
chamfer_edges += module3.edges().group_by(Axis.Z)[-9].group_by(Axis.X)[2]
chamfer_edges += module3.edges().group_by(Axis.Z)[-9].group_by(Axis.X)[3]
# chamfer_edges += module3.edges().group_by(Axis.Z)[-9].group_by(Axis.X)[4]
chamfer_edges += module3.edges().group_by(Axis.Z)[-9].group_by(Axis.X)[5]
chamfer_edges += module3.edges().group_by(Axis.Z)[-9].group_by(Axis.X)[6]
chamfer_edges += module3.edges().group_by(Axis.Z)[-9].group_by(Axis.X)[7]

module3 = chamfer(chamfer_edges, 1)


show(module, module2, module3)

module.export_stl("library/dixit/module1.stl")
module2.export_stl("library/dixit/module2.stl")
module3.export_stl("library/dixit/module3.stl")
