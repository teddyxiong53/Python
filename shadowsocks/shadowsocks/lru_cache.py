from __future__ import absolute_import, division, print_function, with_statement

import os, sys, os.path, re, logging, time, collections

class LRUCache(collections.MutableMapping):
    """
    This class is not thread safe
    """
    def __init__(self, timeout=60, close_callback=None, *args, **kwargs):
        self.timeout = timeout
        self.close_callback = close_callback
        self._store = {}
        self._time_to_keys = collections.defaultdict(list)
        self._keys_to_last_time = {}
        self._last_visits = collections.deque()
        self._closed_values = set()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        t = time.time()
        self._keys_to_last_time[key] = t
        self._time_to_keys[t].append(key)
        self._last_visits.append(t)
        return self._store[key]

    def __setitem__(self, key, value):
        t = time.time()
        self._keys_to_last_time[key] = t
        self._store[key] = value
        self._time_to_keys[t].append(key)
        self._last_visits.append(t)

    def __delitem__(self, key):
        del self._store[key]
        del self._keys_to_last_time[key]

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def sweep(self):
        now = time.time()
        c = 0
        while len(self._last_visits) > 0:
            least = self._last_visits[0]
            if now - least <= self.timeout:
                break
            if self.close_callback is not None:
                # todo
                pass
            self._last_visits.popleft()
            for key in self._time_to_keys[least]:
                if key in self._store:
                    if now - self._keys_to_last_time[key] > self.timeout:
                        del self._store[key]
                        del self._keys_to_last_time[key]
                        c += 1
        if c:
            self._closed_values.clear()
            logging.debug('%d keys swept ' % c)