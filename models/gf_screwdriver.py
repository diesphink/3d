# %%
from textwrap import fill
from build123d import *
from ocp_vscode import show

from sphlib import Dimensions, align, Slot
from sphlib.slots import SlotPosition, SlotType

from gfthings import Bin


# === Dimensions
X, Y, Z = 0, 1, 2
d = Dimensions()

d.screwdriver = [184, 16.6, 16.4]
d.tolerance = 0.2
d.screwdriver[X] += d.tolerance
d.screwdriver[Y] += d.tolerance
d.lip_height = 4.45  # - 0.35

# show(BaseEqual(grid_x=3, grid_y=1))

part = Bin.Bin(5, 1, 3, scoop_rad=0, divisions=1, label=False, solid=True, magnets=False)
# show(part)

screwdriver = Slot(
    Box(d.screwdriver[X], d.screwdriver[Y], d.screwdriver[Z]),
    positions=SlotPosition.Y_AXIS,
    slot_size=24,
    slot_type=SlotType.SPHERE,
)
screwdriver = fillet(screwdriver.edges().filter_by(Axis.Z), 3)
part = part - align(screwdriver, ref=part, center="xy", end="z", margins=[0, 0, d.lip_height - 0.35])

show(part)

export_stl(part, "library/gf_screwdriver.stl")

# %%
# Bin under screwdriver for plastic parts
bin2 = Bin.Bin(4, 1, 3, scoop_rad=0, divisions=1, label=False, magnets=False)
export_stl(bin2, "library/gf_screwdriver_bin2.stl")
show(bin2)

# %%
# Bin under bits for spare bins
bin3 = Bin.Bin(5, 1, 2, scoop_rad=0, divisions=5, label=False, magnets=False, lip=False)
export_stl(bin3, "library/gf_screwdriver_bin3.stl")
show(bin3)

# %%
# magnetizer/demagneitizer
bin4 = Bin.Bin(1, 1, 3, scoop_rad=0, divisions=1, label=False, magnets=False)
export_stl(bin4, "library/gf_screwdriver_bin4.stl")
show(bin4)
# %%
# Laminas
bin5 = Bin.Bin(
    1, 0.5, 5, scoop_rad=0, divisions=3, label=False, magnets=False, lip=False, half_grid=True, wall_thickness=0.8
)
export_stl(bin5, "library/gf_screwdriver_bin5.stl")
show(bin5)


# %%
# Hobby knife + Deburring tool
bin6 = Bin.Bin(4, 1, 4, scoop_rad=0, divisions=1, label=False, magnets=False, lip=False)
show(bin6)
export_stl(bin6, "library/gf_screwdriver_bin6.stl")
# %%
# Other backup tools
bin7 = Bin.Bin(5, 1, 4, scoop_rad=0, divisions=1, label=False, magnets=False)
show(bin7)
export_stl(bin7, "library/gf_screwdriver_bin7.stl")

# %%
# Small extra tools
bin8 = Bin.Bin(5, 1, 2, scoop_rad=0, divisions=1, label=False, magnets=False)
show(bin8)
export_stl(bin8, "library/gf_screwdriver_bin8.stl")

# %%
# Extra deburring knifes
bin9 = Bin.Bin(4, 1, 2, scoop_rad=0, divisions=1, label=False, magnets=False)
show(bin9)
export_stl(bin9, "library/gf_screwdriver_bin9.stl")

# %%

d.bit = [5 / 2, 5 / 2, 15.4]
bit = Cylinder(d.bit[0], d.bit[2])

for i in range(29):
    for j in range(5):
        x = i * (d.bit[0] * 2 + 2.2)
        y = j * (d.bit[1] * 2 + 2.2)
        positioned_bit = bit.translate((x, y, 0))
        if i == 0 and j == 0:
            bits = positioned_bit
        else:
            bits += positioned_bit

bits_bin = Bin.Bin(5, 1, 3, scoop_rad=0, divisions=1, label=False, solid=True, magnets=False, lip=False)
bits_bin -= align(bits, ref=bits_bin, center="xy", end="z")

export_stl(bits_bin, "library/gf_screwdriver_bits.stl")

show(bits_bin)
