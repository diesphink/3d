# pylint: disable=invalid-name
# Originally from
# https://github.com/Ruudjhuu/gridfinity_build123d

"""Gridfinity standard constants."""


from dataclasses import dataclass


@dataclass
class gridfinity_standard:
    """Gridfinity standard constants."""

    @dataclass
    class stacking_lip:
        """Stacking lip constants."""

        height_1 = 0.7
        height_2 = 1.8
        height_3 = 1.9
        offset = 0.25

    @dataclass
    class grid:
        """Grid constants."""

        size = 42
        radius = 7.5
        tollerance = 0.5

    @dataclass
    class bottom:
        """Bottom constants."""

        platform_height = 2.8
        hole_from_side = 4.8

    @dataclass
    class magnet:
        """Magnet constants."""

        size = 6.5
        thickness = 2.4

    @dataclass
    class screw:
        """Screw constants."""

        size = 3
        depth = 6
