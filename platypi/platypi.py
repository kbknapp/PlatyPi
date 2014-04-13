#!/usr/bin/env python
"""
Python 3.x

platypi.py

Controls the platypi system
"""
import sys
import os
from collections import deque
from time import sleep
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


class PlatyPi(object):

    def __init__(self, cad, ppmod_dir):
        self.__cad = cad
        self.__options = deque()
        self.__dirs = []
        self.__commands = []
        self.__index = 0
        self.__is_root_dir = True
        self.__pp_dir = os.path.dirname(os.path.realpath(__file__))
        self.__exit_mod = os.path.join(self.__pp_dir, 'Exit.py')
        self.__back_mod = os.path.join(self.__pp_dir, 'Back.py')

    def start(self):
        """Entry point for the platypi system
        Return: Status (0 or 1)
        """
        print('Getting modules')
        self.__dirs, self.__commands = loader.find_ppmodules(
                                os.path.join(self.__pp_dir, PPMOD_DIR))
        self.__commands.append(self.__exit_mod)
        self.__is_root_dir = False
        self.__options.appendleft(self.make_options(self.__dirs, self.__commands))
         # DEBUG
        print('Current options:')
        for opt in self.__options[0]:
            print('\tOption {}'.format(opt))
        # END DEBUG
        self.next_option()

    def next_option(self, event=None):
        print('Going to next option')
        self.update_display(os.path.basename(self.__options[0][self.__index]))
        if self.__index == len(self.__options[0]) - 1:
            self.__index = 0
        else:
            self.__index += 1

    def previous_option(self, event=None):
        print('Going to previous option')
        self.update_display(os.path.basename(self.__options[0][self.__index]))
        if self.__index == 0:
            self.__index = len(self.__options[0]) - 1
        else:
            self.__index -= 1

    def do_option(self, event=None):
        curr_option = self.__options[0][self.__index - 1]
        print('Doing option {}'.format(curr_option))
        if os.path.isdir(curr_option):
            print('It is a directory')
            self.__dirs, self.__commands = loader.find_ppmodules(curr_option)
            if self.__is_root_dir:
                self.__commands.append(self.__exit_mod)
                self.__is_root_dir = False
            else:
                self.__commands.append(self.__back_mod)
            self.__options.appendleft(self.make_options(self.__dirs, self.__commands))
            self.next_option()
        else:
            print('It is a module')
            mod = __import__(curr_option)
            mod.run(self.__cad)

    def make_options(self, dirs, cmds):
        print('Making iterable options')
        return self.__dirs + self.__commands

    def update_display(self, line):
        print('Updating display')
        lcd = self.__cad.lcd
        lcd.set_cursor(0, 1)
        lcd.write(' ' * pifacecad.lcd.LCD_WIDTH)
        lcd.set_cursor(0, 1)
        print('Writing {}'.format(line))
        lcd.write(line)

    def close(self):
        print('Exiting...')
        self.update_display('Exiting...')
        sleep(2)
        self.__cad.lcd.clear()
        self.__cad.lcd.display_off()


def register_buttons(cad, platypi):
    listener = pifacecad.SwitchEventListener(chip=cad)
    listener.register(ROCKER_RIGHT, pifacecad.IODIR_ON, platypi.next_option)
    listener.register(ROCKER_LEFT, pifacecad.IODIR_ON, platypi.previous_option)
    listener.register(ROCKER_PUSH, pifacecad.IODIR_ON, platypi.do_option)
    return listener


def init_cad():
    print('Creating CAD')
    cad = pifacecad.PiFaceCAD()
    cad.lcd.blink_off()
    cad.lcd.cursor_off()
    cad.lcd.write('PlatyPi v{}'.format(VERSION))
    return cad


if __name__ == '__main__':
    cad = init_cad()
    pp = PlatyPi(cad, PPMOD_DIR)
    pp.start()

    global exit_barrier
    exit_barrier = Barrier(2)

    listener = register_buttons(cad, pp)

    listener.activate()

    exit_barrier.wait()

    pp.close()
    listener.deactivate()

    sys.exit(0)