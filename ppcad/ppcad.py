#!/usr/bin/python
#
# Python 3.x
#
# ppcad.py
#
# v0.1
#	*
#
# Controls the PlatyPiCAD
#
import pifacecad
from threading import Barrier
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
	
	# Use barrier to wait for exit command before quitting
	global exit_barrier
	exit_barrier = Barrier(2)
	
	ppm = PPModule(cad, _TITLE, exit_barrier)
	ppm.start()
	
	exit_barrier.wait()		# Wait for exit
	
	cad.lcd.clear()
	cad.lcd.home()
	cad.lcd.write("Exiting...")
	sleep(3)
	cad.lcd.display_off()
