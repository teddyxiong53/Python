from __future__ import absolute_import, division, print_function, with_statement
import sys,os, logging, signal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))

from shadowsocks import shell, daemon, eventloop, tcprelay, udprelay, asyncdns

def main():
    shell.check_python()
    config = shell.get_config(True)
    print (config)
    daemon.daemon_exec(config)
    logging.info('starting local at %s:%d' % (config['local_address'], config['local_port']))
    dns_resolver = asyncdns.DNSResolver()
    tcp_server = tcp_relay.TCPRelay(config, dns_resolver, True)
    udp_server = udp_relay.UDPRelay(config, dns_resolver, True)
    loop = eventloop.EventLoop()
    dns_resolver.add_to_loop()
    tcp_server.add_to_loop()
    udp_server.add_to_loop()

if __name__ == '__main__':
    main()