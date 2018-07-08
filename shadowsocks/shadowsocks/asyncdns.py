from __future__ import print_function, division, with_statement, absolute_import

import os, sys, os.path, struct, re, logging, socket

from shadowsocks import common, lru_cache, eventloop, shell

CACHE_SWEEP_INTERVAL = 30
VALID_HOSTNAME = re.compile(br"(?!-)[A-Z\d\-_]{1,63}(?<!-)$", re.IGNORECASE)

common.patch_socket()

QTYPE_ANY = 255
QTYPE_A = 1
QTYPE_AAAA = 28
QTYPE_CNAME = 5
QTYPE_NS = 2
QCLASS_IN = 1

class DNSResolver(object):
    def __init__(self, server_list=None, prefer_ipv6=False):
        self._loop = None
        self._hosts = {}
        self._hostname_status = {}
        self._hostname_to_cb = {}
        self._cb_to_hostname = {}
        self._cache = lru_cache.LRUCache(timeout=300)
        self._sock = None
        if server_list is  None:
            self._servers = None
            self._parse_resolv()
        else:
            self._servers = server_list
        if prefer_ipv6:
            self._QTYPES = [QTYPE_AAAA, QTYPE_A]
        else:
            self._QTYPES = [QTYPE_A, QTYPE_AAAA]
        self._parse_resolv()

    def _parse_resolv(self):
        self._servers = []
        try:
            with open('/etc/resolv.conf', 'rb') as f:
                content = f.readlines()
                for line in content:
                    line = line.strip()
                    if not (line and line.startswith(b'nameserver')):
                        continue
                    parts = line.split()
                    if len(parts) < 2:
                        continue
                    server = parts[1]
                    if common.is_ip(server) == socket.AF_INET:
                        if type(server) != str:
                            server = server.decode('utf8')
                        self._servers.append(server)
        except IOError:
            pass
        if not self._servers:
            self._servers = ['8.8.4.4', '8.8.8.8']
