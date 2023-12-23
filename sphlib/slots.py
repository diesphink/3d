import enum
from typing import Union

from build123d import Align, BasePartObject, Box, Mode, RotationLike, Sphere
import sphlib as sph


class SlotType(enum.Enum):
    SPHERE = 0


class SlotPosition(enum.Enum):
    X_AXIS = 0
    Y_AXIS = 1
    X_AXIS_MIN = 2
    X_AXIS_MAX = 3
    Y_AXIS_MIN = 4
    Y_AXIS_MAX = 5


class FingerSlot(BasePartObject):
    def __init__(
        self,
        type: SlotType,
        size: float,
        rotation: RotationLike = (0, 0, 0),
        align: Union[Align, tuple[Align, Align, Align]] = None,
        mode: Mode = Mode.ADD,
    ):
        self.type = type
        self.size = size

        if type == SlotType.SPHERE:
            part = Sphere(size / 2, arc_size3=180, rotation=(-90, 0, 0))

        super().__init__(part=part, rotation=rotation, align=align, mode=mode)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value


class Slot(BasePartObject):
    def __init__(
        self,
        shape,
        positions: SlotPosition,
        slot_size: float,
        slot_type: SlotType,
        rotation: RotationLike = (0, 0, 0),
        align: Union[Align, tuple[Align, Align, Align]] = None,
        mode: Mode = Mode.ADD,
    ):
        slot = FingerSlot(slot_type, slot_size)
        slots = list()
        if positions == SlotPosition.X_AXIS or positions == SlotPosition.X_AXIS_MIN:
            slots.append(sph.align(slot, ref=shape, centerToBegin="x", end="z"))
        if positions == SlotPosition.X_AXIS or positions == SlotPosition.X_AXIS_MAX:
            slots.append(sph.align(slot, ref=shape, centerToEnd="x", end="z"))
        if positions == SlotPosition.Y_AXIS or positions == SlotPosition.Y_AXIS_MIN:
            slots.append(sph.align(slot, ref=shape, centerToBegin="y", end="z"))
        if positions == SlotPosition.Y_AXIS or positions == SlotPosition.Y_AXIS_MAX:
            slots.append(sph.align(slot, ref=shape, centerToEnd="y", end="z"))

        super().__init__(part=shape + slots, rotation=rotation, align=align, mode=mode)
