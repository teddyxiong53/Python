#!/usr/bin/env python

from __future__ import with_statement, print_function

import sys
import ctypes.util
import ctypes

def check_python():
    info = sys.version_info
    #print info
    #if info > (2,0):
    #    print "yes, newer than 2.0"
    #print type(info)
    #print (info.minor)
    #print info[0]
    if info.major ==2 and not info.minor >= 6:
        print ("python 2.6+ is required")
    elif info.major == 3 and not info.minor >= 3:
        print("python 3.3+ is required")
    elif info.major not in [2, 3]:
        print("python version not supported")
    else:
        print("your python version is ok")

def find_library(possible_lib_names, search_symbol, library_name):
    if not type(possible_lib_names) in (tuple, list):
        possible_lib_names = [possible_lib_names]

    lib_names = []
    paths = []
    for lib_name in possible_lib_names:
        lib_names.append(lib_name)
        lib_names.append("lib" + lib_name)

    for name in lib_names:
        path = ctypes.util.find_library(name)
        if path:
            paths.append(path)

    for path in paths:
        try:
            lib = ctypes.CDLL(path)
            if hasattr(lib, search_symbol):
                return lib
        except:
            pass
    return None
if __name__ == "__main__":
    check_python()
    print( find_library(['c'], 'strcpy', 'libc'))
