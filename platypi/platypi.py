#!/usr/bin/env python
"""
Python 3.x

platypi.py

Controls the platypi system
"""
import sys
import os
import itertools
from threading import Barrier        # Python 3

try:
    import pifacecad
except ImportError:
    print("'pifacecad'' module not installed, using console exclusivly.")

import loader

PY3 = sys.version_info[0] >= 3
if not PY3:
    print('Requires Python 3.x\n\nExiting...')
    sys.exit(1)

VERSION = 0.1
PPMOD_DIR = 'ppmodules'
ROCKER_RIGHT = 7
ROCKER_LEFT = 6
ROCKER_PUSH = 5

__cad = None
__options = None
__dirs = []
__commands = []


def main():
    """Entry point for the platypi system
    Return: Status (0 or 1)
    """
    global __cad
    __cad = pifacecad.PiFaceCAD()
    __cad.lcd.blink_off()
    __cad.lcd.cursor_off()
    __cad.lcd.write('PlatyPi v{}'.format(VERSION))

    global __dirs
    global __commands
    (__dirs, __commands) = loader.find_ppmodules(os.path.join(
                                            os.path.abspath(__file__),
                                            PPMOD_DIR
                                            ))
    global __options
    __options = make_options(__dirs, __commands)

    global __exit_barrier
    __exit_barrier = Barrier(2)

    listener = pifacecad.SwitchEventListener(chip=__cad)
    listener.register(pifacecad.IODIR_ON, ROCKER_RIGHT, next_option)
    listener.register(pifacecad.IODIR_ON, ROCKER_LEFT, previous_option)
    listener.register(pifacecad.IODIR_ON, ROCKER_PUSH, do_option)
    listener.activate()

    __exit_barrier.wait()
    close()
    listener.deactivate()

    return 0


def next_option(event=None):
    update_display(next(__options))


def previous_option(event=None):
    to_advance = (len(__dirs) + len(__commands)) - 2
    update_display(next(itertools.islice(__options, to_advance, to_advance),
                        None))


def do_option(event=None):
    pass


def make_options(dirs, cmds):
    return itertools.cycle(itertools.chain(__dirs, __commands))


def update_display(line):
    lcd = __cad.lcd
    lcd.set_cursor(0, 1)
    lcd.write(' ' * pifacecad.LCD_WIDTH)
    lcd.set_cursor(0, 1)
    lcd.write(line)


def close():
    __cad.lcd.clear()
    __cad.lcd.disp_off()

if __name__ == '__main__':
    sys.exit(main())