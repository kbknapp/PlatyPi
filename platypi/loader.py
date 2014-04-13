# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Python 3.x

loader.py
"""
import os


def find_ppmodules(path):
    print('Finding modules from {}...'.format(path))
    for root, dirs, files in os.walk(path):
        print('Root: {}'.format(root))
        pp_files = [os.path.abspath(file_name)
                    for file_name in files
                        if os.path.basename(file_name)[:2] != '__']
        pp_dirs = [os.path.abspath(dir_name)
                    for dir_name in dirs
                        if os.path.basename(dir_name)[:2] != '__']
        break
    return (pp_dirs, pp_files)