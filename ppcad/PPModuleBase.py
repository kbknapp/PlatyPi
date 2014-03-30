# -*- coding: utf-8 -*-
#!/usr/bin/python
#
# Python 3.x
#
# PPModuleBase.py
#
# Provides a base class for all platypi modules
#
import pifacecad
from threading import Barrier
import os
import inspect

class PPModuleBase(object):
	def __init__(self, cad, pmod_dir, exit_barrier):
		self._ppmodules = []
		self._curr_index = 0
		self._cad = cad
		self._self_dir = os.path.basename(os.path.realpath(__file__))
		self._pmod_dir = pmod_dir
		self._exit_barrier = exit_barrier
	
	
	def previous_cmd(self, event=None):
		if len(self._ppmodules) > 0:
			if self._curr_index == 0:
				self._curr_index = (len(self._ppmodules)-1)
			else:
				self._curr_index -= 1
			self.update_disp()
	
	
	def next_cmd(self, event=None):
		if len(self._ppmodules) > 0:
			if self._curr_index == (len(self._ppmodules)-1):
				self._curr_index = 0
			else:
				self._curr_index += 1
			self.update_disp()
	
	
	def run_cmd(self, event=None):
		ppm = self.load_ppmodule(self._curr_index)
		exit_barrier = Barrier(2)
		ppm(self._cad, '', exit_barrier).start()
		exit_barrier.wait()
	
	
	def load_ppmodule(self, index):
		module = __import__('%s.%s' % (self._pmod_dir, self._ppmodules[self._curr_index]['name']), fromlist=[])
		for cls in dir(module):
			cls = getattr(module, cls)
			if (inspect.isclass(cls) and inspect.getmodule(cls) == module and issubclass(cls,'PPModuleBase')):
				return cls
	
	def find_ppmodules(self):
		# Get all files in the 'commands' directory as possible modules
		full_pmod_dir = os.path.join(self._self_dir, self._pmod_dir)
		pmods = os.listdir(full_pmod_dir)
		# Loop over them all, adding them to the _ppmodules list as sets
		i = 0
		for pmod in pmods:
			# Check if the file is __init__.py or __init__.pyc to skip
			# Also check for directories...skip those too
			if pmod[:8] == "__init__" or os.path.isdir(os.path.join(full_pmod_dir, pmod)):
				continue
			# Add to _ppmodules
			self._ppmodules.append({'name': '', 'compiled': False})
			# Check if it's a .py or .pyc'
			pmod_split = os.path.splitext(pmod)
			if pmod_split[1] == '.pyc':
				self._ppmodules[i]['compiled'] = True
				self._ppmodules[i]['name'] = pmod_split[0]
			else:
				self._ppmodules[i]['compiled'] = False
				self._ppmodules[i]['name'] = pmod_split[0]
			i += 1
	
	
	def update_disp(self):
		# Clear bottom row and reset cursor to bottom row
		self._cad.lcd.set_cursor(0,1)
		self._cad.lcd.write(' '*16)
		self._cad.lcd.set_cursor(0,1)
		
		# write the current ppmodule name on the display
		self._cad.lcd.write(self._ppmodules[self._curr_index]['name'])
	
	
	def close(self):
		self._exit_barrier.wait()
	
	
	def start(self):
		self.find_ppmodules()
		self.update_disp()