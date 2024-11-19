# %%
"""
(c) 2020 diesphink
This code is licensed under MIT license (see LICENSE for details)
"""

from build123d import Vector
from enum import Enum
from functools import reduce

BEGIN = 0
CENTER = 1
END = 2
GAP = 3

AXES = ["x", "y", "z"]


def _vector_to_array(vector):
    return [vector.X, vector.Y, vector.Z]


def min_value(bounding_box, axis, current=None):
    if current is None:
        return _vector_to_array(bounding_box.min)[axis]
    else:
        return min(_vector_to_array(bounding_box.min)[axis], current)


def max_value(bounding_box, axis, current=None):
    if current is None:
        return _vector_to_array(bounding_box.max)[axis]
    else:
        return max(_vector_to_array(bounding_box.max)[axis], current)


def distribute(
    objs, begin="", center="", end="", gap="", rangeX=None, rangeY=None, rangeZ=None, outerGap=False, indexOrder=True
):
    """
    Distribute in the specifide mode the objects on an axis, returning the
    repositionated objects.

    The objects can be distributed in the following modes:

        begin:      Distribute the objects making their beginnings equidistant
        center:     Distribute the objects making their centers equidistant
        end:        Distribute the objects making their endings equidistant
        gap:        Distribute the objects making the distance between the objects
                    equidistant

    On each parameter of mode above, it can receive any combination of axes (x,
    y or z)

    For the distribution, the objects will use the minimum and maximum value on
    the specified axis. To specify one specific range for the distribution, use
    the range parameter for the correct axis (rangeX, rangeY or rangeZ).

    When the ditribution is using the gap mode, it's possible to add a gap on the
    beginning and end of the distribution with the parameter outerGap. If passed
    true, it will add a space before and after the objects with the same distance
    as the inner gaps. If a numeric value is passed, it will add that specific gap
    before and after the objects.

    Parameter
    objs:       Array of objects to be distributed
    begin:      Axes to distribute the object's begin
    center:     Axes to distribute the object's center
    end:        Axes to distribute the object's end
    gap:        Axes to distribute the distance between the objects
    rangeX:     Array with [min, max] to use on the X axis distribution
    rangeY:     Array with [min, max] to use on the Y axis distribution
    rangeZ:     Array with [min, max] to use on the Z axis distribution
    outerGap:   Only when using gap, indicates if should add a gap before and after
                the objects. If passed true, will add a gap with the same size as
                the inner gaps, if a number is passed, will add a gap with that
                size

    Retorns:
    New object array with the repositionated objects

    Example:

        // Creates 10 cubes with random positions and sizes
        let cubes = []
        for (let i = 1; i <= 10; i++)
            cubes.push(translate([Math.random() * 20, 0, 0],cube({ size: 0.2 + Math.random() * 2 })))

        // Distributes the cubes on the X axis to keep the same distance between them
        cubes = distribute(cubes,  {gap: "x"})
    """

    # If objs is None or is not an array
    if objs == None or not hasattr(objs, "__iter__"):
        raise ValueError("objs must be an array of objects")

    ret = []

    deltas = []

    for axis, axisName in enumerate(AXES):
        if axisName in begin:
            mode = BEGIN
        elif axisName in center:
            mode = CENTER
        elif axisName in end:
            mode = END
        elif axisName in gap:
            mode = GAP
        else:
            continue

        # Order objects in the array based on the order on the current axis
        if not indexOrder:
            objs = sorted(objs, key=lambda obj: min_value(obj.bounding_box(), axis))

        # Gather each relevant metric
        def gather_metrics(obj):
            bounds = obj.bounding_box()
            min = _vector_to_array(bounds.min)
            max = _vector_to_array(bounds.max)
            rt = [None] * 4
            rt[BEGIN] = min[axis]
            rt[CENTER] = (min[axis] + max[axis]) / 2
            rt[END] = max[axis]
            rt[GAP] = max[axis] - min[axis]
            return rt

        metrics = [*map(gather_metrics, objs)]

        # Ranges contains min/max values for the axis
        # It's a bidimensional array with the first indicating0: mins, 1: maxes
        # and the index holds the actual min or max value for each distribution mode
        ranges = None

        if (
            (axisName == "x" and rangeX is not None)
            or (axisName == "y" and rangeY is not None)
            or (axisName == "z" and rangeZ is not None)
        ):
            ranges = [[None] * 4, [None] * 4]
            for distmode in [BEGIN, CENTER, END, GAP]:
                ranges[0][distmode] = rangeX[0] if axisName == "x" else rangeY[0] if axisName == "y" else rangeZ[0]
                ranges[1][distmode] = rangeX[1] if axisName == "x" else rangeY[1] if axisName == "y" else rangeZ[1]
        else:

            def reduce_metrics(acc, m):
                for distmode in [BEGIN, CENTER, END, GAP]:
                    if acc[0][distmode] is None or m[distmode] < acc[0][distmode]:
                        acc[0][distmode] = m[distmode]
                    if acc[1][distmode] is None or m[distmode] > acc[1][distmode]:
                        acc[1][distmode] = m[distmode]
                return acc

            ranges = reduce(reduce_metrics, metrics, [[None] * 4, [None] * 4])

        if mode == GAP:
            # Move objects considering only the empty space between them
            total_range = ranges[1][END] - ranges[0][BEGIN]
            total_size = reduce(lambda total_size, m: total_size + m[GAP], metrics, 0)

            space_between = None
            if isinstance(outerGap, (int, float)):
                space_between = (total_range - total_size - 2 * outerGap) / (len(objs) - 1)
            elif outerGap:
                space_between = (total_range - total_size) / (len(objs) + 1)
            else:
                space_between = (total_range - total_size) / (len(objs) - 1)

            acc = ranges[0][BEGIN]
            if isinstance(outerGap, (int, float)):
                acc += outerGap
            elif outerGap:
                acc += space_between

            for i, obj in enumerate(objs):
                if len(deltas) <= i:
                    deltas.append([0, 0, 0])
                deltas[i][axis] = acc - metrics[i][mode]
                acc += metrics[i][GAP] + space_between
                # deltas[i][axis] = ranges[0][mode] + i * space_between - metrics[i][mode]

        else:
            space_between = (ranges[1][mode] - ranges[0][mode]) / (len(objs) - 1)
            for i, obj in enumerate(objs):
                if len(deltas) <= i:
                    deltas.append([0, 0, 0])
                deltas[i][axis] = ranges[0][mode] + i * space_between - metrics[i][mode]

    for i, obj in enumerate(objs):
        ret.append(obj.translate(deltas[i]))
    return ret
