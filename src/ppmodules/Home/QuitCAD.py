#!/usr/bin/python
#
# Python 3.x
#
# PlatyPiCTL_ClearCAD
#
# Turns off and clears the PiFaceCAD

import pifacecad
cad = pifacecad.PiFaceCAD()

cad.lcd.clear()
cad.lcd.backlight_off()
cad.lcd.display_off()
