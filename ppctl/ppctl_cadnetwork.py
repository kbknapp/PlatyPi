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
import socket
import subprocess

__ROCKER_RIGHT = 7
__ROCKER_LEFT = 6
__ROCKER_PUSH = 8

__curr_index = 0

__cad = None
__listener = None

__screens = [["IP:", ""],
			 ["Subnet Mask:", ""],
			 ["Default GW:", ""],
			 ["Hostname", ""],
			 ["Quit?", ""]]

def __write_screen():
	__cad.lcd.clear()
	if __screens[__curr_index][1] == "":
		__do_action(__curr_index)
	__cad.lcd.write("%s\n%s" % (__screens[__curr_index][0], __screens[__curr_index][1]))

def __next():
	global __curr_index
	if __curr_index == len(__screens):
		__curr_index = 0
	else:
		__curr_index += 1
	__write_screen()

def __previous():
	global __curr_index
	if __curr_index == 0:
		__curr_index = len(__screens)
	else:
		__curr_index -= 1
	__write_screen()

def __do_action():
	if __curr_index == 0:
		# Get IP
		__screens[0][1] = socket.gethostbyname(socket.gethostname())
	elif __curr_index == 1:
		# Get Subnet Mask
		__screens[1][1] = subprocess.check_output("ifconfig eth0 | grep netmask | awk '{print $4}'", shell=True).decode("utf-8")
	elif __curr_index == 2:
		# Get Default GW
		__screens[2][1] = subprocess.check_output("ip route show | grep via | awk '{print $3}'", shell=True).decode("utf-8")
	elif __curr_index == 3:
		# Get hostname
		__screens[3][1] = socket.gethostname()
	else:
		# Quit
		__listener.deactivate()
		__cad.lcd.clear()

def __register_buttons():
	__listener = pifacecad.SwitchEventListener(chip=__cad)
	# Add rocker->right (switch 7) to 'next'
	__listener.register(__ROCKER_RIGHT, pifacecad.IODIR_FALLING_EDGE, __next)
	# Add rocker->left (switch 6) to 'previous'
	__listener.register(__ROCKER_LEFT, pifacecad.IODIR_FALLING_EDGE, __previous)
	# Add rocker->down (push) (switch 8) to 'do action'
	__listener.register(__ROCKER_PUSH, pifacecad.IODIR_FALLING_EDGE, __do_action)
	__listener.activate()

if __name__ == "__main__":
	# Called directly, must initialize CAD
	__cad = pifacecad.PiFaceCAD()
	__cad.lcd.blink_off()
	__cad.lcd.cursor_off()
	__cad.lcd.backlight_off()
	if __screens[0][1] == "":
		__do_action(__curr_index)
	__cad.lcd.write("%s\n%s" % (__screens[0][0], __screens[0][1]))
	__register_buttons()