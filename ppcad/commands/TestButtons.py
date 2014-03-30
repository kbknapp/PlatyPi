#!/usr/bin/python
#
# Python 3.x
#
# PlatyPiCTL_TestCAD.py
#
# Used to test various features of the PiFaceCAD
import pifacecad
import time		# Used for sleeping

__listener = None

def update_pin_text(event):
	event.chip.lcd.set_cursor(13, 0)
	event.chip.lcd.write(str(event.pin_num))

def quit_test(event):
	global __listener
	__listener.deactivate()
	event.chip.lcd.clear()
	event.chip.lcd.write("Quiting...")
	time.sleep(3)
	event.chip.lcd.clear()
	
cad = pifacecad.PiFaceCAD()
cad.lcd.write("You pressed: ")
global __listner
__listener = pifacecad.SwitchEventListener(chip=cad)
for i in range(4):
	__listener.register(i, pifacecad.IODIR_FALLING_EDGE, update_pin_text)
__listener.register(5, pifacecad.IODIR_FALLING_EDGE, quit_test)
cad.lcd.blink_off()
__listener.activate()
