# %%
from textwrap import fill
from build123d import *
from ocp_vscode import show

from sphlib import Dimensions, align, Slot
from sphlib.slots import SlotPosition, SlotType

from gfthings import Bin
from gflabel import cli


# %%
# Large bins for full keycap sets
big_bin = Bin.Bin(2, 3, 9, scoop_rad=0, divisions=1, label=True, magnets=False)
export_stl(big_bin, "library/gridfinity/keycaps_bigbin.stl")
show(big_bin)

# %%
# Two layer keycaps, extra keycaps for used ones
small_bin = Bin.Bin(2, 2, 7, scoop_rad=0, divisions=2, label=True, magnets=False)
export_stl(small_bin, "library/gridfinity/keycaps_smallbin.stl")
show(small_bin)

# %%
# Tools bin
tool_bin = Bin.Bin(1, 4, 2, scoop_rad=0, divisions=1, label=False, magnets=False)
export_stl(tool_bin, "library/gridfinity/keycaps_tool_bin.stl")
show(tool_bin)

# %%
tiny_bin = Bin.Bin(1, 1, 2, scoop_rad=0, divisions=1, label=False, magnets=False)
export_stl(tiny_bin, "library/gridfinity/keycaps_tiny_bin.stl")
show(tiny_bin)

# %%
bin3 = Bin.Bin(1, 2, 7, scoop_rad=0, divisions=1, label=True, magnets=False)
export_stl(bin3, "library/gridfinity/keycaps_bin3.stl")
show(bin3)

# %%
bin4 = Bin.Bin(1, 2, 7, scoop_rad=0, divisions=1, label=False, magnets=False)
export_stl(bin4, "library/gridfinity/keycaps_bin4.stl")
show(bin4)

# %%
# LABELS
# gflabel modern "KEYCAPS" -w 5 --vscode --font-size 7 --font-style bold -o library/gridfinity/keycaps_label.stl
# gflabel pred -w 2 --font-style bold "104 KEYS - ABNT2 - ABS" --vscode --font-size 5 -o "library/gridfinity/lbl_keycaps_104_abs.stl"
# gflabel pred -w 1 --font-style bold "118K - US - PBT" --vscode --font-size 4 -o "library/gridfinity/lbl_keycaps_118_lp_pbt.stl"
# gflabel pred -w 2 --font-style bold "104 KEYS - ABNT2 - ABS - SURARA" --vscode --font-size 4.2 -o "library/gridfinity/lbl_keycaps_104_abs_surara.stl"
# gflabel pred -w 2 --font-style bold "DOUBLE LAYERED\n FOR CUSTOMIZATION" --vscode --font-size 4.2 -o "library/gridfinity/lbl_keycaps_twolayers.stl"
