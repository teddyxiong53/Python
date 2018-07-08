from __future__ import absolute_import, division, print_function, with_statement
import sys,os, logging, signal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))

from shadowsocks import shell

def main():
    shell.check_python()
    config = shell.get_config(True)
    print (config)

if __name__ == '__main__':
    main()