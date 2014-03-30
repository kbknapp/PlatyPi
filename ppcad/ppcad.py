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
import os
from time import sleep

ROCKER_LEFT = 6
ROCKER_RIGHT = 7
ROCKER_PUSH = 5

_WELCOME = "PlatyPi v0.1"
_CMD_DIR = "ppmodules"

class ppcad:
	def __init__(self, cad, title, cmd_dir):
		self._title = title
		self._cmds = []
		self._curr_index = 0
		self._cad = cad
		self._self_dir = os.path.realpath(__file__)[:-8]
		self._cmd_dir = cmd_dir
		self.update_disp()
	
	def previous_cmd(self, event=None):
		if len(self._cmds) > 0:
			if self._curr_index == 0:
				self._curr_index = (len(self._cmds)-1)
			else:
				self._curr_index -= 1
			self.update_disp()
	
	
	def next_cmd(self, event=None):
		if len(self._cmds) > 0:
			if self._curr_index == (len(self._cmds)-1):
				self._curr_index = 0
			else:
				self._curr_index += 1
			self.update_disp()
	
	
	def run_cmd(self, event=None):
		pass
	
	
	def load_cmds(self):
		# Get all files in the 'commands' directory as possible commands
		pcmds = os.listdir(os.path.join(self._self_dir, self._cmd_dir))
		# Loop over them all, adding them to the _cmds list as sets
		i = 0
		for pcmd in pcmds:
			# Check if the file is __init__.py or __init__.pyc to skip
			# Also check for directories...skip those too
			if pcmd[:8] == "__init__" or os.path.isdir(os.path.join(self._self_dir, pcmd)):
				continue
			# Add to _cmds
			self._cmds.append({'name': '', 'compiled': False})
			# Check if it's a .py or .pyc'
			if pcmd[-1:] == 'c':
				self._cmds[i]['compiled'] = True
				self._cmds[i]['name'] = pcmd[:-4]
			else:
				self._cmds[i]['compiled'] = False
				self._cmds[i]['name'] = pcmd[:-3]
			i += 1
	
	def update_disp(self):
		self._cad.lcd.home()
		if len(self._cmds) > 0:
			self._cad.lcd.set_cursor(0,1)
			self._cad.lcd.write(' '*16)
			self._cad.lcd.set_cursor(0,1)
			self._cad.lcd.write("%s" % (self._cmds[self._curr_index]['name']))
		else:
			self._cad.lcd.clear()
			self._cad.lcd.write(self._title)
	
	
	def close(self):
		self._cad.lcd.write("Exiting...\n")
		sleep(3)
		self._cad.lcd.clear()
		self._cad.lcd.backlight_off()
		self._cad.lcd.display_off()

if __name__ == "__main__":
	# Set up CAD
	cad = pifacecad.PiFaceCAD()
	cad.lcd.blink_off()
	cad.lcd.cursor_off()
	cad.lcd.backlight_off()
	cad.lcd.clear()
	my_cad = ppcad(cad, _WELCOME, _CMD_DIR)
	
	# Load and display commands
	my_cad.load_cmds()
	my_cad.update_disp()
	
	# Use barrier to wait for exit command before quitting
	global exit_barrier
	exit_barrier = Barrier(2)
	
	# Set up buttons
	listener = pifacecad.SwitchEventListener(chip=cad)
	listener.register(ROCKER_LEFT, pifacecad.IODIR_ON, my_cad.previous_cmd)
	listener.register(ROCKER_RIGHT, pifacecad.IODIR_ON, my_cad.next_cmd)
	listener.register(ROCKER_PUSH, pifacecad.IODIR_ON, my_cad.run_cmd)
	listener.activate()
	
	exit_barrier.wait()		# Wait for exit
	
	my_cad.close()
	listener.deactivate()