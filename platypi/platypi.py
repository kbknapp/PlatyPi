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

VERSION = '0.2.1'
PPMOD_DIR = 'ppmodules'
ROCKER_RIGHT = 7
ROCKER_LEFT = 6
ROCKER_PUSH = 5


class PlatyPi(object):

    def __init__(self, cad, ppmod_dir, title):
        self.__cad = cad
        self.__options = deque()
        self.__dirs = []
        self.__commands = []
        self.__index = 0
        self.__is_root_dir = True
        self.__pp_dir = os.path.dirname(os.path.realpath(__file__))
        self.__mod_prefix = [PPMOD_DIR]
        self.__title = title

    def start(self):
        """Entry point for the platypi system
        Return: Status (0 or 1)
        """
        self.set_title(self.__title)
        print('Getting modules')
        self.__dirs, self.__commands = loader.find_ppmodules(os.path.join(self.__pp_dir, PPMOD_DIR))
        #self.__commands.append(self.__exit_mod)
        self.__commands.append('Exit')
        self.__is_root_dir = False
        self.__options.appendleft(self.make_options(self.__dirs,
                                                    self.__commands))
         # DEBUG
        print('Current options:')
        for opt in self.__options[0]:
            print('\tOption {}'.format(opt))
        # END DEBUG
        self.__index = len(self.__options[0]) - 1
        self.next_option()

    def next_option(self, event=None):
        print('Going to next option')
        if self.__index == len(self.__options[0]) - 1:
            self.__index = 0
        else:
            self.__index += 1
        self.update_display(os.path.basename(self.__options[0][self.__index]))

    def previous_option(self, event=None):
        print('Going to previous option')
        if self.__index == 0:
            self.__index = len(self.__options[0]) - 1
        else:
            self.__index -= 1
        self.update_display(os.path.basename(self.__options[0][self.__index]))

    def do_option(self, event=None):
        curr_option = self.__options[0][self.__index]
        print('Doing option {}'.format(curr_option))
        if os.path.isdir(os.path.join(self.__pp_dir, curr_option)):
            print('It is a directory')
            self.__mod_prefix.append(os.path.splitext(os.path.basename(curr_option))[0])
            self.__dirs, self.__commands = loader.find_ppmodules(curr_option)
            if self.__is_root_dir:
                self.__commands.append('Exit')
                self.__is_root_dir = False
            else:
                self.__commands.append('Back')
            self.__options.appendleft(self.make_options(self.__dirs, self.__commands))
            self.__index = 0
            self.set_title(self.__mod_prefix[-1])
            self.next_option()
        elif curr_option == 'Exit':
            print('It is the exit command')
            exit_barrier.wait()
        elif curr_option == 'Back':
            print('It is the back command')
            print('Popping options')
            self.__options.popleft()
            print('New options:')
            for opt in self.__options[0]:
                print('\tOption {}'.format(opt))
            print('Popping mod_prefix')
            self.__mod_prefix.pop()
            print('New mod_prefix: {}'.format(self.__mod_prefix.__str__()))
            self.__index = 0
            if len(self.__mod_prefix) == 1:
                self.set_title(self.__title)
            else:
                self.set_title(self.__mod_prefix[-1])
            self.next_option()
        else:
            print('It is a module to run')
            self.__mod_prefix.append(os.path.splitext(os.path.basename(curr_option))[0])
            pkg_name = '.'.join(self.__mod_prefix)
            print('{} is a package'.format(pkg_name))
            mod_name = self.__mod_prefix[-1]
            print('{} is the module'.format(mod_name))
            mod = __import__(pkg_name, fromlist=[self.__mod_prefix[:-1]])
            mod.run(cad=self.__cad)
            print('Done running module')

    def make_options(self, dirs, cmds):
        print('Making iterable options')
        return dirs + cmds

    def set_title(self, title):
        lcd = self.__cad.lcd
        print('Writing title: {}'.format(title))
        lcd.home()
        lcd.write(' ' * pifacecad.lcd.LCD_WIDTH)
        lcd.home()
        lcd.write(title)

    def update_display(self, line):
        print('Updating display')
        lcd = self.__cad.lcd
        lcd.set_cursor(0, 1)
        lcd.write(' ' * pifacecad.lcd.LCD_WIDTH)
        lcd.set_cursor(0, 1)
        print('Writing line: {}'.format(line))
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
    return cad


if __name__ == '__main__':
    cad = init_cad()
    pp = PlatyPi(cad, PPMOD_DIR, 'PlatyPi v{}'.format(VERSION))
    pp.start()

    global exit_barrier
    exit_barrier = Barrier(2)

    listener = register_buttons(cad, pp)

    listener.activate()
    print('1st wait()')
    exit_barrier.wait()

    pp.close()
    listener.deactivate()

    sys.exit(0)