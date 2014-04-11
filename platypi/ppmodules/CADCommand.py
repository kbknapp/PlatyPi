# -*- coding: utf-8 -*-
import abc

class CADCommand(object):
	"""The command interface"""
	
	__metaclass__ = abc.ABCMeta
	
	_title = ''
	_name = ''
	
	def __init__(self):
		
		
	
	
	@abc.abstractmethod
	def execute(self):
		"""Performs some action"""
		pass
	
	
	def get_name(self):
		"""Returns the name of the command"""
		return self._name
	
	
	def get_title(self):
		"""Returns the title that will be displayed on the top line of the CAD"""
		return self._title
	
	