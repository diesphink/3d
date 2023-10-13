"""
(c) 2020 diesphink
This code is licensed under MIT license (see LICENSE for details)
"""

from build123d import Vector


def _vector_to_array(vector):
    return [vector.X, vector.Y, vector.Z]


class Dimensions(object):
    def __getattr__(self, attr):
        setattr(self, attr, Dimensions())
        return getattr(self, attr)


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
    """

    Aligns an object (obj) considering a reference (ref) on begin/center/end,
    returning the traslated object.

    There are nine possible alignment options, based on which part of the object
    will be used for calculations (begin, center or end), for each object (obj or
    reference):

    +-------------------+-----------------+-----------------+--------------+
    |                   |                 Anchor on reference              |
    | Anchor on object  | begin             center            end          |
    +-------------------+-----------------+-----------------+--------------+
    | begin             | begin           | beginToCenter   | beginToEnd   |
    | center            | centerToBegin   | center          | centerToEnd  |
    | end               | endToBegin      | endToCenter     | end          |
    +-------------------+-----------------+-----------------+--------------+

    For the alignment, begin means the minimum value of this object on the axis,
    end means the maximum value of this object on the axis, and center means the
    mean value in the axis ((min+max)/2).

    On each of these 9 options, any of the 3 (x, y, z) axes can be passed, as
    string. You may pass any number of axes/alignment options. E.g. to center the
    obj to the reference in all axes, you may call:
        align(obj, {ref, center: "xyz"})

    Ref may be an object (in this case, the reference will be the bounding box
    around the object) or an array of coordinates ([x, y, z]). If no ref is
    passed, the origin is used ([0, 0, 0]).

    Parameters

    obj:            Object to be aligned/translated
    ref:            Reference object or reference array ([x, y, z]). If
                    omitted, will use origins: ([0, 0, 0])
    begin:          Axes to align the object's begin to the reference begin
    beginToCenter:  Axes to align the object's begin to the reference center
    beginToEnd:     Axes to align the object's begin to the reference end
    centerToBegin:  Axes to align the object's center to the reference begin
    center:         Axes to align the object's center to the reference center
    centerToEnd:    Axes to align the object's center to the reference end
    endToBegin:     Axes to align the object's end to the reference begin
    endToCenter:    Axes to align the object's end to the reference center
    end:            Axes to align the object's end to the reference end

    Returns
    obj translated according to the parameters

    Example:

        # Creates a 2³ translated cube @ (4,2,9)
        cube1 = Pos(4, 2, 9) * Box(2, 2, 2)

        # Creates a 1³ cube directly above (z axis) the first cube,
        # centered on the x and y axes
        cube2 = align(Box(1, 1, 1), ref=cube1, center="xy", beginToEnd="z")

        show(cube1, cube2)


    """

    # pontos do objeto (begin, end e center)
    bObj = _vector_to_array(object.bounding_box().min)
    eObj = _vector_to_array(object.bounding_box().max)
    cObj = _vector_to_array((object.bounding_box().min + object.bounding_box().max) / 2)

    # Pontos do ref (begin, end e center)
    if ref is None:
        bRef = eRef = cRef = [0, 0, 0]
    elif type(ref) is list:
        bRef = eRef = cRef = ref
    else:
        bRef = _vector_to_array(ref.bounding_box().min)
        eRef = _vector_to_array(ref.bounding_box().max)
        cRef = _vector_to_array((ref.bounding_box().min + ref.bounding_box().max) / 2)

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
            from_ = bObj[i]
            deltas[i] = margins[i] + margin

        if axis in centerToBegin or axis in center or axis in centerToEnd:
            from_ = cObj[i]
            if axis in centerToBegin:
                deltas[i] = margins[i] + margin
            elif axis in centerToEnd:
                deltas[i] = -margins[i] - margin

        if axis in endToBegin or axis in endToCenter or axis in end:
            from_ = eObj[i]
            deltas[i] = -margins[i] - margin

        # ...is aligned to which part of the ref
        if axis in begin or axis in centerToBegin or axis in endToBegin:
            to_ = bRef[i]
        if axis in beginToCenter or axis in center or axis in endToCenter:
            to_ = cRef[i]
        if axis in beginToEnd or axis in centerToEnd or axis in end:
            to_ = eRef[i]

        if from_ is not None and to_ is not None:
            deltas[i] = deltas[i] + to_ - from_

    return object.translate(Vector(deltas[0], deltas[1], deltas[2]))
