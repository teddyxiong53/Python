from __future__ import with_statement, print_function, division, absolute_import

import os, sys, time, socket, select, traceback, logging, errno
from collections import defaultdict

from shadowsocks import shell

class SelectLoop(object):
    def __init__(self):
        self._r_list = set()
        self._w_list = set()
        self._x_list = set()

    def poll(self, timeout):
        r,w,x = select.select(self._r_list, self._w_list, self._x_list, timeout )
        results = defaultdict(lambda : POLL_NULL)

class EventLoop(object):
    def __init__(self):
        self._impl = SelectLoop()
        model = 'select'
