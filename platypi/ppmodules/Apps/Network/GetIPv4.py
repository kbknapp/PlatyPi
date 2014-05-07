# -*- coding: utf-8 -*-
from .. import CADCommand

class GetIPv4(CADCommand):
	
	def __init__(self):
		super(GetIPv4, self).__init__()
		self._title = 'IPv4 Address:'
		self._name = 'IP Address'
	
	
	def execute(self):
		return self.get_ipv4_address()
	
	
	def get_ipv4_address(self):
		"""Returns a string of the Current IP address such as 192.168.0.1"""
		return '192.168.0.1'		# Testing ONLY