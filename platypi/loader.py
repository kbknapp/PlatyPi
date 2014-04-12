# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Python 3.x

loader.py
"""
import os


def find_ppmodules(path):
    for root, dirs, files in os.walk(path):
        pp_files = [os.path.abspath(file_name)
                    for file_name in files if file_name[:2] is not '__']
        pp_dirs = [dir_name
                    for dir_name in dirs if dir_name[:2] is not '__']
        return (pp_dirs, pp_files)