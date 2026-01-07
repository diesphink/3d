# %%
from textwrap import fill
from build123d import *
from ocp_vscode import show

from sphlib import Dimensions, align, Slot
from sphlib.slots import SlotPosition, SlotType

from gfthings import Bin
from gflabel import cli


# %%
# nozzles
nozzles = Bin.Bin(1, 1, 2, scoop_rad=0, divisions=2, label=True, magnets=False)
export_stl(nozzles, "library/gridfinity/slarti_nozzles.stl")
show(nozzles)

# %%
tools = Bin.Bin(4, 1, 6, scoop_rad=0, divisions=1, label=False, magnets=False)
export_stl(tools, "library/gridfinity/slarti_tools.stl")
show(tools)

# %%
small = Bin.Bin(2, 1, 6, scoop_rad=0, divisions=1, label=False, magnets=False)
export_stl(small, "library/gridfinity/slarti_small.stl")
show(small)


# %%
printed_partes = Bin.Bin(5, 1, 6, scoop_rad=0, divisions=1, label=False, magnets=False)
export_stl(printed_partes, "library/gridfinity/slarti_printed_partes.stl")
show(printed_partes)

# %%
# LABELS
# gflabel modern "KEYCAPS" -w 5 --vscode --font-size 7 --font-style bold -o library/gridfinity/keycaps_label.stl
# gflabel pred -w 2 --font-style bold "104 KEYS - ABNT2 - ABS" --vscode --font-size 5 -o "library/gridfinity/lbl_keycaps_104_abs.stl"
# gflabel pred -w 1 --font-style bold "118K - US - PBT" --vscode --font-size 4 -o "library/gridfinity/lbl_keycaps_118_lp_pbt.stl"
# gflabel pred -w 2 --font-style bold "104 KEYS - ABNT2 - ABS - SURARA" --vscode --font-size 4.2 -o "library/gridfinity/lbl_keycaps_104_abs_surara.stl"
# gflabel pred -w 2 --font-style bold "DOUBLE LAYERED\n FOR CUSTOMIZATION" --vscode --font-size 4.2 -o "library/gridfinity/lbl_keycaps_twolayers.stl"

# gflabel modern "SLARTIBARTFAST\nTools and Spares" -w 5 --vscode --font-size 7 --font-style bold -o library/gridfinity/slarti_tools.stl
# gflabel pred -w 1 -d 2 --font-style bold ".2" ".25" --vscode --font-size 5 -o "library/gridfinity/slarti_0.2-0.25.stl"
# gflabel pred -w 1 -d 2 --font-style bold ".6" "" --vscode --font-size 5 -o "library/gridfinity/slarti_0.6.stl"
# gflabel pred -w 1 -d 1 --font-style bold ".6" --vscode --font-size 5 -o "library/gridfinity/slarti_0.6.stl"
