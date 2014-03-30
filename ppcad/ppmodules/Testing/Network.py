# -*- coding: utf-8 -*-
#!/usr/bin/python
#
# Python 3.x
#
# ppctl_cadnetwork v0.1
#	* Displays information about the network setup to the PiFaceCAD
#	* Requires:
#		* ifconfig (for subnet mask)
#		* grep (for subnet mask)
#		* awk (for subnet mask)
#		* ip (for default gw)
#
# Changelog
#	* v0.1
#		* Initial Release
#
import pifacecad
import socket			# For: IP, Hostname
import subprocess		# For: Default GW, Subnet Mask

_ROCKER_RIGHT = 7
_ROCKER_LEFT = 6
_ROCKER_PUSH = 5

_curr_index = 0

_cad = None
_listener = None
_orig_listener = None
_orig_screen = ""

_screens = [["IP:", ""],
	["Subnet Mask:", ""],
	["Default GW:", ""],
	["Hostname", ""],
	["Quit?", ""]]


def _write_screen():
	_cad.lcd.clear()
	if _screens[_curr_index][1] == "":
		_do_action(_curr_index)
	_cad.lcd.write("%s\n%s" % (_screens[_curr_index][0], _screens[_curr_index][1]))


def _next():
	global _curr_index
	if _curr_index == len(_screens):
		_curr_index = 0
	else:
		_curr_index += 1
	_write_screen()


def _previous():
	global _curr_index
	if _curr_index == 0:
		_curr_index = len(_screens)
	else:
		_curr_index -= 1
	_write_screen()


def _do_action():
	if _curr_index == 0:
		# Get IP
		_screens[0][1] = socket.gethostbyname(socket.gethostname())
	elif _curr_index == 1:
		# Get Subnet Mask
		_screens[1][1] = subprocess.check_output("ifconfig eth0 | grep netmask | awk '{print $4}'", shell=True).decode("utf-8")
	elif _curr_index == 2:
		# Get Default GW
		_screens[2][1] = subprocess.check_output("ip route show | grep via | awk '{print $3}'", shell=True).decode("utf-8")
	elif _curr_index == 3:
		# Get hostname
		_screens[3][1] = socket.gethostname()
	else:
		# Quit
		_listener.deactivate()
		_cad.lcd.clear()
		if _orig_screen != "" and _orig_listener is not None:
			_cad.lcd.write(_orig_screen)
			_orig_listener.activate()


def _register_buttons():
	_listener = pifacecad.SwitchEventListener(chip=_cad)
	# Add rocker->right (switch 7) to 'next'
	_listener.register(_ROCKER_RIGHT, pifacecad.IODIR_FALLING_EDGE, _next)
	# Add rocker->left (switch 6) to 'previous'
	_listener.register(_ROCKER_LEFT, pifacecad.IODIR_FALLING_EDGE, _previous)
	# Add rocker->down (push) (switch 8) to 'do action'
	_listener.register(_ROCKER_PUSH, pifacecad.IODIR_FALLING_EDGE, _do_action)
	_listener.activate()


def start_module(cad, listener, screen):
	global _cad
	global _orig_listener
	global _orig_screen
	_cad = cad
	_orig_listener = listener
	_orig_screen = screen
	_cad.lcd.clear()
	_cad.lcd.blink_off()
	_cad.lcd.cursor_off()
	if _screens[0][1] == "":
		_do_action(0)
	_cad.lcd.write("%s\n%s" % (_screens[0][0], _screens[0][1]))
	_register_buttons()


if __name__ == "__main__":
	# Called directly, must initialize CAD
	_cad = pifacecad.PiFaceCAD()
	_cad.lcd.blink_off()
	_cad.lcd.cursor_off()
	_cad.lcd.backlight_off()
	if _screens[0][1] == "":
		_do_action(0)
	_cad.lcd.write("%s\n%s" % (_screens[0][0], _screens[0][1]))
	_register_buttons()