#!/usr/bin/env python
"""
Displays information about the PlatyPi tool
"""
from time import sleep

import pifacecad

def run(cad=None):
    if cad is None:
        cad = pifacecad.PiFaceCAD()
        cad.lcd.blink_off()
        cad.lcd.cursor_off()
    title = 'PlatyPi Toolkit'
    cad.lcd.write(title)
    cad.lcd.set_cursor(0, 1)
    line = 'github.com/kbknapp/PlatyPi'
    cad.lcd.write(line)
    for _ in enumerate(range(len(line)%16)):
        cad.lcd.move_left()
        cad.lcd.home()
        cad.lcd.write(title)
        sleep(1)