import socket
import struct

def to_bytes(s):
    if bytes != str:
        if type(s) == str:
            return s.encode('utf-8')
    return s

def to_str(s):
    if bytes != str:
        if type(s) == bytes:
            return s.decode('utf-8')
    return s

def inet_pton(family, addr):
    addr = to_str(addr)
    if family == socket.AF_INET:
        return socket.inet_aton(addr)
    elif family == socket.AF_INET6:
        pass
    else:
        raise RuntimeError('what family?')

def is_ip(address):
    for family in (socket.AF_INET, socket.AF_INET6):
        try:
            if type(address) != str:
                address = address.decode('utf8')
            inet_pton(family, address)
            return  family
        except (TypeError, ValueError, OSError, IOError):
            pass
    return False

class IPNetwork(object):
    ADDRLENGTH = {socket.AF_INET:32, socket.AF_INET6: 128, False:0}
    def __init__(self, addrs):
        self._network_list_v4 = []
        self._network_list_v6 = []
        if type(addrs) == str:
            addrs = addrs.split(',')
        list(map(self.add_network, addrs))

    def add_network(self, addr):
        if addr is "":
            return
        block = addr.split('/')
        addr_family = is_ip(block[0])
        addr_len = IPNetwork.ADDRLENGTH[addr_family]
        if addr_family is  socket.AF_INET:
            ip, = struct.unpack("!I", socket.inet_aton(block[0]))
        elif addr_family is socket.AF_INET6:
            pass
        else:
            raise Exception('not a valid CIDR notation: %s' % addr)

        if len(block) is 1:
            prefix_size = 0
            while (ip & 1)== 0 and ip is not 0:
                ip >>= 1
                prefix_size += 1
        elif block[1].isdigit() and int(block[1]) <= addr_len:
            prefix_size = addr_len - int(block[1])
            ip >>= prefix_size
        else :
            raise Exception("not a valid CIDR notation")
        if addr_family is socket.AF_INET:
            self._network_list_v4.append((ip, prefix_size))
        else:
            self._network_list_v6.append((ip, prefix_size))

    def __contains__(self, addr):
        addr_family = is_ip(addr)
        if addr_family is socket.AF_INET:
            ip, = struct.unpack('!I', socket.inet_aton(addr))
            return any(map(lambda n_ps: n_ps[0] == ip>>n_ps[1], self._network_list_v4))
        elif addr_family is socket.AF_INET6:
            return False
        else:
            return False


