#!/usr/bin/python
#
# Python 3.x
#
# platypi.py
#
# v0.1
#	*
#
# Controls the PlatyPi
#
import pifacecad
from time import sleep
from ppmodules import PPModule

_TITLE = "PlatyPi v0.1"

if __name__ == "__main__":
	# Set up CAD
	cad = pifacecad.PiFaceCAD()
	cad.lcd.blink_off()
	cad.lcd.cursor_off()
	cad.lcd.backlight_off()
	cad.lcd.clear()
	cad.lcd.write(_TITLE)
	
	ppm = PPModule(cad, _TITLE)
	ppm.start()
	
	
	cad.lcd.clear()
	cad.lcd.home()
	cad.lcd.write("Exiting...")
	sleep(3)
	cad.lcd.display_off()
