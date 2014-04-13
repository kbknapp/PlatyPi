# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Python 3.x

loader.py
"""
import os


def find_ppmodules(path, custom_path=None):
    print('Finding modules from {}...'.format(path))
    for root, dirs, files in os.walk(path):
        pp_files = [os.path.realpath(file_name)
                    for file_name in files
                        if os.path.basename(file_name)[:2] != '__']
        pp_dirs = [os.path.realpath(dir_name)
                    for dir_name in dirs
                        if os.path.basename(dir_name)[:2] != '__']
        break
        if custom_path:
            print('Custom path is {}'.format(custom_path))
            if os.path.isdir(custom_path):
                pp_dirs.append(custom_path)
            else:
                pp_files.append(custom_path)
    return (pp_dirs, pp_files)