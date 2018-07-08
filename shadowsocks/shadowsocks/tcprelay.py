from __future__ import with_statement, print_function, division, absolute_import

import os,sys,os.path, logging, socket
import socket

from shadowsocks import eventloop, common, shell


class TCPRelay(object):

    def __init__(self, config, dns_resolver, is_local, stat_callback=None):
        self._config = config
        self._is_local = is_local
        self._dns_resolver = dns_resolver
        self._closed = False
        self._eventloop = None
        self._fd_to_handlers = {}

        self._timeout = config['timeout']
        self._timeouts = []
        self._timeout_offset = 0
        self._handler_to_timeouts = {}

        if is_local:
            listen_addr = config['local_address']
            listen_port = config['local_port']
        else:
            listen_addr = config['server']
            listen_port = config['server_port']

        self._listen_port = listen_port
        addrs = socket.getaddrinfo(listen_addr, listen_port, 0, socket.SOCK_STREAM, socket.SOL_TCP)

        if len(addrs) == 0:
            raise Exception("cannot get addrinfo for %s:%d" % (listen_addr, listen_port))

        af, socktype, proto, canonname, sa = addrs[0]
        server_socket = socket.socket(af, socktype, proto)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(sa)
        server_socket.setblocking(False)

        if config['fast_open']:
            try:
                server_socket.setsockopt(socket.SOL_TCP, 23, 5)
            except socket.error:
                logging.error('warning: fast open is not available')
                self._config['fast_open'] = False
        server_socket.listen(1024)
        self._server_socket = server_socket
        self._stat_callback = stat_callback

