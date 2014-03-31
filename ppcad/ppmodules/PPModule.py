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
from collections import deque

class PPModule(object):
	_ppmodules = deque()			# A list of modules to display to the user
	_curr_index = 0			# The currently displayed module
	_cad = None				# The PiFaceCAD
	_exit_barrier = None	# The Exit Barrier
	_search_dir = deque()
	_title = 'Home Module v0.1'
	_first = True
	_listener = None
	_ROCKER_PUSH = 5
	_ROCKER_RIGHT = 7
	_ROCKER_LEFT = 6
	_quit_barrier = None
	
	def __init__(self, cad, title, exit_barrier):
		print("Making PPModule...")
		self._cad = cad
		self._exit_barrier = exit_barrier
		if title != '':
			self._title = title
		self._listener = pifacecad.SwitchEventListener(chip=cad)
		self._search_dir.append(os.path.dirname(os.path.abspath(__file__)))
	
	
	def previous_cmd(self, event=None):
		if len(self._ppmodules[0]) > 0:
			if self._curr_index == 0:
				self._curr_index = (len(self._ppmodules[0])-1)
			else:
				self._curr_index -= 1
			self.update_disp()
	
	
	def next_cmd(self, event=None):
		if len(self._ppmodules[0]) > 0:
			if self._curr_index == (len(self._ppmodules[0])-1):
				self._curr_index = 0
			else:
				self._curr_index += 1
			self.update_disp()
	
	
	def run_cmd(self, event=None):
		print("Running command...")
		curr_dict = self._ppmodules[0][self._curr_index]
		if curr_dict['type'] == 'directory':
			print("It was a dictionary")
			self._search_dir.appendleft(os.path.join(self._search_dir[0], curr_dict['name']))
			self.find_ppmodules()
			self._ppmodules[0].append({'name': "Back", 'compiled': False, 'type': 'function'})
		elif curr_dict['type'] == 'function':
			print("It was a function...")
			if curr_dict['name'] == "Back":
				print("Back called...")
				self._search_dir.popleft()
				self._ppmodules.popleft()
				self._curr_index = 0
			elif curr_dict['name'] == "Quit":
				print("Quit called...")
				self.close()
		else:
			print("It was a script...")
			pass
		self.update_disp()
	
	
	def load_ppmodule(self, index):
		module = __import__('%s.%s' % (self._pmod_dir, self._ppmodules[self._curr_index]['name']), fromlist=[])
		for cls in dir(module):
			cls = getattr(module, cls)
			if (inspect.isclass(cls) and inspect.getmodule(cls) == module and issubclass(cls,'PPModuleBase')):
				return cls
	
	def find_ppmodules(self):
		print("Looking for modules...")
		# PPModules are files, but folders are displayed to the user to
		# the interface clean and navigationally organized
		self._ppmodules.appendleft([])
		for root, dirs, files in os.walk(self._search_dir[0]):
			# Add all the directories
			for dir_name in dirs:
				print("Looking through directories of %s" % root)
				if dir_name[:2] == "__":
					print("Found something starting with __, skipping...")
					continue
				print("Found a directory named, %s" % dir_name)
				self._ppmodules[0].append({'name': dir_name, 'compiled': False, 'type': 'directory'})
			for file_name in files:
				print("Looking through files of %s" % root)
				# First check to make sure we're not adding ourself, or any __init__.py files
				if file_name[:2] == '__' or os.path.basename(__file__) == file_name:
					print("Found something starting with __, skipping...")
					continue
				if os.path.splitext(file_name)[1] == '.pyc':
					print("Found a compiled script %s" % file_name)
					self._ppmodules[0].append({'name': file_name, 'compiled': True, 'type': 's'})
				else:
					print("Found a script %s" % file_name)
					self._ppmodules[0].append({'name': file_name, 'compiled': False, 'type': 's'})
			self._ppmodules[0].append({'name': "Quit", 'compiled': False, 'type': 'function'})
			break		# Only doing one iteration (current dir only)
	
	
	
	def update_disp(self):
		print("Updating the display...")
		# Clear bottom row and reset cursor to bottom row
		if(self._first):
			print("First time!")
			self._cad.lcd.home()
			self._cad.lcd.write("%s\n%s" % (self._title, ' '*16))
			self._first = False
		else:
			print("Not the first time, clearing only the second row...")
			self._cad.lcd.set_cursor(0, 1)
			self._cad.lcd.write(' '*16)
		
		self._cad.lcd.set_cursor(0, 1)
		print("Writing a module name %s" % (self._ppmodules[0][self._curr_index]['name']))
		# write the current ppmodule name on the display
		self._cad.lcd.write(self._ppmodules[0][self._curr_index]['name'])
	
	
	def close(self):
		self._quit_barrier.wait()
	
	
	def start(self):
		print("Starting PPModule...")
		self.find_ppmodules()
		self.update_disp()
		print("Registering listner...")
		self._listener.register(self._ROCKER_PUSH, pifacecad.IODIR_ON, self.run_cmd)
		self._listener.register(self._ROCKER_LEFT, pifacecad.IODIR_ON, self.previous_cmd)
		self._listener.register(self._ROCKER_RIGHT, pifacecad.IODIR_ON, self.next_cmd)
		self._listener.activate()
		
		self._quit_barrier = Barrier(2)
		self._quit_barrier.wait()
		
		self._listener.deactivate()
		self._exit_barrier.wait()
