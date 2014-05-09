#!/usr/bin/env python
"""
Displays information about the PlatyPi tool
"""

import pifacecad

from .platypi import VERSION

def run(cad=None):
    if cad is None:
        cad = pifacecad.PiFaceCAD()
        cad.lcd.blink_off()
        cad.lcd.cursor_off()
    cad.lcd.write('PlatyPi v{}'.format(VERSION))
    cad.lcd.set_cursor(0, 1)
    cad.lcd.write('github.com/kbknapp/PlatyPi')
    cad.lcd.move_right()