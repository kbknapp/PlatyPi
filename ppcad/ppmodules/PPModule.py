# -*- coding: utf-8 -*-
#!/usr/bin/python
#
# Python 3.x
#
# PPModule.py
#
# Provides a base class for all platypi modules
#
import pifacecad
from threading import Barrier
import os
import inspect

class PPModule(object):
	_ppmodules = []			# A list of modules to display to the user
	_curr_index = 0			# The currently displayed module
	_cad = None				# The PiFaceCAD
	_exit_barrier = None	# The Exit Barrier
	_search_dir = '.'		# Where to search for platypi modules
	_title = ''
	_first = True
	
	def __init__(self, cad, title='Home Module v0.1', exit_barrier):
		self._cad = cad
		self._exit_barrier = exit_barrier
		self._title = title
	
	
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
		# PPModules are files, but folders are displayed to the user to
		# the interface clean and navigationally organized
		for root, dirs, files in os.walk(self._search_dir):
			# Add all the directories
			for dir_name in dirs:
				if dir_name.starts_with('__'):
					continue
				self._ppmodules.append({'name': dir_name, 'compiled': False, 'type': 'directory'})
			for file_name in files:
				# First check to make sure we're not adding ourself, or any __init__.py files
				if file_name.starts_with('__') or os.path.basename(__file__) == file_name:
					continue
				if os.path.splitext(file_name)[1] == '.pyc':
					self._ppmodules.append({'name': file_name, 'compiled': True, 'type': 's'})
				else:
					self._ppmodules.append({'name': file_name, 'compiled': False, 'type': 's'})
			break		# Only doing one iteration (current dir only)
	
	
	
	def update_disp(self):
		# Clear bottom row and reset cursor to bottom row
		if(self._first):
			self._cad.lcd.home()
			self._cad.lcd.write("%s\n%s" % (self._title, ' '*16))
			self._first = False
		else:
			self._cad.lcd.set_cursor(0, 1)
			self._cad.lcd.write(' '*16)
			self._cad.lcd.set_cursor(0, 1)
		
		# write the current ppmodule name on the display
		self._cad.lcd.write(self._ppmodules[self._curr_index]['name'])
	
	
	def close(self):
		self._exit_barrier.wait()
	
	
	def start(self):
		self.find_ppmodules()
		self.update_disp()