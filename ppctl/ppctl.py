#!/usr/bin/python
#
# Python 3.x
#
# PlatyPiCTL.py
#
# v0.1
#	* Displays a welcom to the User
#
# Controls the PlatyPi
#
import pifacecad
from pifacecad.tools.question import LCDQuestion

VERSION = "v0.1"
welcome_msg = "PlatyPi %s" % VERSION
options = ["Commands", "About"]

# > char
#quaver = pifacecad.LCDBitmap([0x0, 0x8, 0xc, 0xe, 0xc, 0x8, 0x0, 0x0])

cad = pifacecad.PiFaceCAD()
#cad.lcd.store_custom_bitmap(0, quaver)
#cad.lcd.clear()
#cad.lcd.blink_off()
#cad.lcd.cursor_off()
#cad.lcd.write(welcome_msg)
question = LCDQuestion(welcome_msg, options)
answer_index = question.ask()


