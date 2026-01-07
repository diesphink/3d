# %%
from textwrap import fill
from build123d import *
from ocp_vscode import show

from sphlib import Dimensions, align, Slot
from sphlib.slots import SlotPosition, SlotType

from gfthings import Bin
from gflabel import cli

# Caixa 1: LEDs, botões, resistores, potenciômetros, outros pequenos componentes
# Caixa 2: Sensores, comunicação, displays, câmeras
# Caixa 3: Fios, jumper cables, conectores, bornes, terminais, pinos dc12v, relays, motores
# Caixa 4: Placas arduino, esp, raspberry,  attiny85, shields, protoboards


# %%
# leds
leds = Bin.Bin(3, 1, 3, scoop_rad=0, divisions=6, label=True, magnets=False)
export_stl(leds, "library/gridfinity/electronics_leds.stl")
show(leds)

# %%
# Resistors
res4 = Bin.Bin(2, 2, 2, scoop_rad=0, divisions=4, label=True, magnets=False)
export_stl(res4, "library/gridfinity/electronics_res_4.stl")
show(res4)

res5 = Bin.Bin(2, 2, 2, scoop_rad=0, divisions=5, label=True, magnets=False)
export_stl(res5, "library/gridfinity/electronics_res_5.stl")
show(res5)

res6 = Bin.Bin(2, 2, 3, scoop_rad=0, divisions=6, label=True, magnets=False)
export_stl(res6, "library/gridfinity/electronics_res_6.stl")
show(res6)

# %%
# Buttons
# big push buttons (4) x1
buttons = Bin.Bin(2, 1, 3, scoop_rad=0, divisions=3, label=False, magnets=False)
export_stl(buttons, "library/gridfinity/buttons1.stl")
show(buttons)

# small push buttons (12) x2
buttons = Bin.Bin(2, 1, 2, scoop_rad=0, divisions=6, label=False, magnets=False)
export_stl(buttons, "library/gridfinity/buttons2.stl")
show(buttons)


# buttons = Bin.Bin(2, 1, 1, scoop_rad=0, divisions=6, label=False, magnets=False, lip=False)
# export_stl(buttons, "library/gridfinity/buttons3.stl")
# show(buttons)

# Surface push buttons (12) x1 + extra bin x1
buttons = Bin.Bin(2, 1, 2, scoop_rad=0, divisions=1, label=False, magnets=False)
export_stl(buttons, "library/gridfinity/buttons3.stl")
show(buttons)

# Rocker btns (9) x1
buttons = Bin.Bin(2, 1, 3, scoop_rad=0, divisions=1, label=False, magnets=False)
export_stl(buttons, "library/gridfinity/buttons4.stl")
show(buttons)

# Other state buttons x1
buttons = Bin.Bin(2, 1, 4, scoop_rad=0, divisions=3, label=False, magnets=False)
export_stl(buttons, "library/gridfinity/buttons5.stl")
show(buttons)

# potentiometers (5), encoders (2), joystick x1
buttons = Bin.Bin(3, 1, 6, scoop_rad=0, divisions=3, label=False, magnets=False)
export_stl(buttons, "library/gridfinity/buttons6.stl")
show(buttons)

# Extras
buttons = Bin.Bin(3, 3, 3, scoop_rad=0, divisions=1, label=False, magnets=False)
export_stl(buttons, "library/gridfinity/buttons7.stl")
show(buttons)

# %%
# DISPLAYS
# big eink
display = Bin.Bin(3, 4, 2, scoop_rad=0, divisions=1, label=False, magnets=False)
export_stl(display, "library/gridfinity/eink.stl")
show(display)

# lcd, segment display
display = Bin.Bin(2, 3, 7, scoop_rad=0, divisions=1, label=False, magnets=False)
export_stl(display, "library/gridfinity/lcd.stl")
show(display)


# small eink
display = Bin.Bin(2, 3, 4, scoop_rad=0, divisions=1, label=False, magnets=False)
export_stl(display, "library/gridfinity/small_eink.stl")
show(display)

# %%
# attiny85
chips = Bin.Bin(1, 1, 8, scoop_rad=0, divisions=1, label=False, magnets=False)
export_stl(chips, "library/gridfinity/attiny85.stl")
show(chips)

# %%
# pins
pins = Bin.Bin(1, 5, 2, scoop_rad=0, divisions=2, label=False, magnets=False)
export_stl(pins, "library/gridfinity/pins.stl")
show(pins)

# %%
# shields
shields = Bin.Bin(1, 3, 9, scoop_rad=0, divisions=1, label=False, magnets=False)
export_stl(shields, "library/gridfinity/shields.stl")
show(shields)

# %%
# nodemcu
nodemcu = Bin.Bin(2, 1, 7, scoop_rad=0, divisions=1, label=False, magnets=False)
export_stl(nodemcu, "library/gridfinity/nodemcu.stl")
show(nodemcu)

# nodemcu2
nodemcu = Bin.Bin(2, 1, 2, scoop_rad=0, divisions=1, label=False, magnets=False)
export_stl(nodemcu, "library/gridfinity/nodemcu2.stl")
show(nodemcu)

# small pcbs
smallpcbs = Bin.Bin(2, 1, 5, scoop_rad=0, divisions=1, label=False, magnets=False)
export_stl(smallpcbs, "library/gridfinity/smallpcbs.stl")
show(smallpcbs)

# %%
# arduino
arduino = Bin.Bin(2, 2, 3, scoop_rad=0, divisions=1, label=False, magnets=False)
export_stl(arduino, "library/gridfinity/arduino.stl")
show(arduino)

# %%
# 12v, bornes
connectors = Bin.Bin(4, 2, 3, scoop_rad=0, divisions=4, label=False, magnets=False)
export_stl(connectors, "library/gridfinity/connectors.stl")
show(connectors)

# 12v cable conns
connectors = Bin.Bin(1, 2, 6, scoop_rad=0, divisions=1, label=False, magnets=False)
export_stl(connectors, "library/gridfinity/connectors2.stl")
show(connectors)

# breadboards
breadboards = Bin.Bin(5, 1, 9, scoop_rad=0, divisions=1, label=False, magnets=False, lip=False)
export_stl(breadboards, "library/gridfinity/breadboards.stl")
show(breadboards)

# comps
comps = Bin.Bin(5, 1, 3, scoop_rad=0, divisions=5, label=True, magnets=False)
export_stl(comps, "library/gridfinity/comps.stl")
show(comps)

# comps
comps = Bin.Bin(4, 1, 3, scoop_rad=0, divisions=3, label=True, magnets=False)
export_stl(comps, "library/gridfinity/comps2.stl")
show(comps)

# comps
comps = Bin.Bin(1, 1, 3, scoop_rad=0, divisions=2, label=True, magnets=False)
export_stl(comps, "library/gridfinity/comps3.stl")
show(comps)

# comps
comps = Bin.Bin(1, 2, 9, scoop_rad=0, divisions=1, label=False, magnets=False)
export_stl(comps, "library/gridfinity/comps4.stl")
show(comps)

# comps
comps = Bin.Bin(1, 2, 9, scoop_rad=0, divisions=1, label=False, magnets=False, lip=False)
export_stl(comps, "library/gridfinity/comps5.stl")
show(comps)

# comps
comps = Bin.Bin(1, 1, 9, scoop_rad=0, divisions=1, label=False, magnets=False, lip=False)
export_stl(comps, "library/gridfinity/comps6.stl")
show(comps)

# comps
comps = Bin.Bin(3, 1, 3, scoop_rad=0, divisions=1, label=False, magnets=False)
export_stl(comps, "library/gridfinity/comps7.stl")
show(comps)

# %%

# comps
comps = Bin.Bin(2, 2, 4, scoop_rad=0, divisions=1, label=False, magnets=False, lip=False)
export_stl(comps, "library/gridfinity/comps8.stl")
show(comps)

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

# gflabel pred -w 2 -d 6 --font-style bold "10\nΩ" "100\nΩ" "1\nKΩ" "10\nKΩ" "100\nKΩ" "1\nMΩ" --vscode --font-size 5 -o "library/gridfinity/electronics_lbl_res10.stl"
# gflabel pred -w 2 -d 5 --font-style bold "22\nΩ" "220\nΩ" "2.2\nKΩ" "22\nKΩ" "220\nKΩ" --vscode --font-size 5 -o "library/gridfinity/electronics_lbl_res22.stl"
# gflabel pred -w 2 -d 5 --font-style bold "47\nΩ" "470\nΩ" "4.7\nKΩ" "47\nKΩ" "470\nKΩ" --vscode --font-size 5 -o "library/gridfinity/electronics_lbl_res47.stl"
# gflabel pred -w 2 -d 5 --font-style bold "680\nΩ" "6.8\nKΩ" "68\nKΩ" "680\nKΩ" "OUTROS" --vscode --font-size 5 -o "library/gridfinity/electronics_lbl_res68.stl"
# gflabel pred -w 3 -d 6 --font-style bold "L7805CV\nV Regul 5V" "CAPACIT\n1µF 50V" "2N3904\nNPN Trans" "PS1420P02\nBuzzer 5V" "" "" --vscode --font-size 3.2 -o "library/gridfinity/electronics_lbl_assort1.stl"

# gflabel modern "Microcontrollers\nDisplays" -w 5 --vscode --font-size 7 --font-style bold -o library/gridfinity/lbl_microcontrollers_displays.stl
# gflabel modern "Screwdriver\nDeburr, Knife" -w 5 --vscode --font-size 7 --font-style bold -o library/gridfinity/lbl_tools_screwdriver.stl

# gflabel pred -w 5 -d 5 --font-style bold "DHT22" "DHT11" "MICROSD" "RASP CAMERA" "LM393 OPTIC" --vscode --font-size 5 -o "library/gridfinity/electronics_lbl_comp.stl"
# gflabel pred -w 4 -d 3 --font-style bold "RF SC2272" "LM393 SOUND" "BT JY-MCU" --vscode --font-size 5 -o "library/gridfinity/electronics_lbl_comp2.stl"
# gflabel pred -w 1 -d 2 --font-style bold "BMP\n085" "IR - VS\n1838B" --vscode --font-size 3.7 -o "library/gridfinity/electronics_lbl_comp3.stl"
