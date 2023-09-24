from build123d import Vector


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
