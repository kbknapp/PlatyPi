# -*- coding: utf-8 -*-
#!/usr/bin/python
#
# Python 3.x
#
# PlatyPiCtl.py v0.1
#
import pifacecad
from pifacecad.tools.question import LCDQuestion

VERSION_STR = "v0.1"

initial_q = "PlatyPi %s" % VERSION_STR
options = ["Cmds", "About"]

cad = pifacecad.PiFaceCAD()
qestion = LCDQuestion(initial_q, options)
answer_index = question.ask()