from __future__ import with_statement, print_function, division, absolute_import

import os, sys, time, socket, select, traceback, logging, errno
from collections import defaultdict

from shadowsocks import shell

__all__ = [
    'EventLoop',
    'POLL_NULL',
    'POLL_IN',
    'POLL_OUT',
    'POLL_ERR',
    'POLL_HUP',
    'POLL_NVAL',
    'EVENT_NAMES',
]

POLL_NUL = 0X00
POLL_IN = 0X01
POLL_OUT = 0X04
POLL_ERR = 0X08
POLL_HUP = 0X10
POLL_NVAL = 0X20

EVENT_NAMES = {
    PULL_NULL: 'POLL_NULL',
    POLL_IN: 'POLL_IN',
    POLL_OUT: 'POLL_OUT',
    POLL_ERR: 'POLL_ERR',
    POLL_HUP: 'POLL_HUP',
    POLL_NVAL: 'POLL_NVAL',
}

TIMEOUT_PRECISION = 10

class SelectLoop(object):
    def __init__(self):
        self._r_list = set()
        self._w_list = set()
        self._x_list = set()

    def poll(self, timeout):
        r,w,x = select.select(self._r_list, self._w_list, self._x_list, timeout )
        results = defaultdict(lambda : POLL_NULL)
        for p in [(r,POLL_IN), (w, POLL_OUT), (x, POLL_ERR)]:
            for fd in p[0]:
                results[fd] |= p[1]
        return  results.items()
    def regisger(self, fd, mode):
        if mode & POLL_IN:
            self._r_list.add(fd)
        if mode & POLL_OUT:
            self._w_list.add(fd)
        if mode & POLL_ERR:
            self._x_list.add(fd)

    def unregister(self, fd):
        if fd in self._r_list:
            self._r_list.remove(fd)
        if fd in self._w_list:
            self._w_list.remove(fd)
        if fd in self._x_list:
            self._x_list.remove(fd)

    def modify(self, fd, mode):
        self.unregister(fd)
        self.regisger(fd, mode)

    def close(self):
        pass

class EventLoop(object):
    def __init__(self):
        self._impl = SelectLoop()
        model = 'select'
        self._fdmap = {}
        self._last_time = time.time()
        self._periodic_callbacks = []
        self._stopping = False
    def poll(self, timeout=None):
        events = self._impl.poll(timeout)
        return [(self._fdmap[fd][0], fd, event) for fd, event in events]

    def add(self, f, mode, handler):
        fd = f.fileno()
        self._fdmap[fd] = (f, handler)
        self._impl.regisger(fd, mode)

    def remove(self, f):
        fd = f.fileno()
        del self._fdmap[fd]
        self._impl.unregister(fd)

    def add_periodic(self, callback):
        self._periodic_callbacks.append(callback)

    def remove_periodic(self, callback):
        self._periodic_callbacks.remove(callback)

    def modify(self, f, mode):
        fd = f.fileno()
        self._impl.modify(fd, mode)

    def stop(self):
        self._stopping = True

    def run(self):
        events = []
        while not self._stopping:
            asap = False # as soon as possible
            try:
                events = self.poll(TIMEOUT_PRECISION)
            except (OSError, IOError) as e:
                if errno_from_exception(e) in (errno.EPIPE, errno.EINTR):
                    asap = True
                    logging.debug('poll:%s', e)
                else:
                    logging.error('poll:%s', e)
                    traceback.print_exc()
                    continue
            for sock,fd, event in events:
                handler = self._fdmap.get(fd, None)
                if handler is not None:
                    handler = handler[1]
                    try:
                        handler.hanle_event(sock,fd, event)
                    except (OSError, IOError) as e:
                        shell.print_exception(e)
            now = time.time()
            if asap or now - self._last_time >= TIMEOUT_PRECISION:
                for callback in self._periodic_callbacks:
                    callback()
                self._last_time =now

    def __del__(self):
        self._impl.close()


def errno_from_exception(e):
    if hasattr(e, 'errno'):
        return e.errno
    elif e.args:
        return e.args[0]
    else:
        return None

