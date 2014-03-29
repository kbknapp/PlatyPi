#!/usr/bin/python
#
# Python 3.x
#
# PlatyPiCTL_TestCAD.py
#
# Used to test various features of the PiFaceCAD
import pifacecad
def update_pin_text(event):
	event.chip.lcd.set_cursor(13, 0)
	event.chip.lcd.write(str(event.pin_num))

cad = pifacecad.PiFaceCAD()
cad.lcd.write("You pressed: ")
listener = pifacecad.SwitchEventListener(chip=cad)
for i in range(8):
	listener.register(i, pifacecad.IODIR_FALLING_EDGE, update_pin_text)
cad.lcd.blink_off()
listener.activate()
