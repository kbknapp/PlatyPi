# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Get's the local IPv4 address and displays to the user
Requires:
    * ifconfig
    * grep
    * awk
"""
import subprocess

import pifacecad

MOD_VERSION = '0.1'

def get_ipv4():
    return subprocess.check_output('ifconfig | grep broadcast | awk "{print $2}"', shell=True).decode('utf-8')

def run(cad=None):
    if cad is None:
        cad = pifacecad.PiFaceCad()
        cad.lcd.blink_off()
        cad.lcd.cursor_off()
    cad.lcd.write('IPv4 Address:')
    ip = get_ipv4()
    cad.lcd.set_cursor(0, 1)
    cad.lcd.write(' ' * pifacecad.lcd.LCD_WIDTH)
    cad.lcd.set_cursor(0, 1)
    cad.lcd.write(ip)