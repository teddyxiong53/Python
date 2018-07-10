from __future__ import print_function, division, with_statement, absolute_import


import sys,os,os.path
import logging
import getopt
import json

sys.path.append("./")


from common import to_str, to_bytes, IPNetwork

VERBOSE_LEVEL = 5
verbose = 0

def check_python():
    info = sys.version_info
    print(info)

def find_config():
    config_path = 'config.json'
    if os.path.exists(config_path):
        return config_path
    config_path = os.path.join(os.path.dirname(__file__), config_path)
    if os.path.exists(config_path):
        return config_path
    return None

def _decode_list(data):
    rv = []
    for item in data:
        if hasattr(item, 'encode'):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)

    return rv

def _decode_dict(data):
    rv = {}
    for key,value in data.items():
        if hasattr(value, 'encode'):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

def parse_json_in_str(data):
    return json.loads(data, object_hook=_decode_dict)

def print_local_help():
    print("""
    usage: sslocal [options] ...

    """
    )
def print_server_help():
    print("""
    usage: ssserer [options] ...
    """
    )
def print_shadowsocks():
    print("1.0")

def print_help(is_local):
    if is_local:
        print_local_help()
    else:
        print_server_help()


def check_config(config, is_local):
    if config.get('daemon', None) == 'stop':
        return
    if is_local:
        if config.get('server', None) is None:
            logging.error('server addr not specified')
            print_local_help()
            sys.exit(2)
        else:
            config['server'] = to_str(config['server'])
    else:
        config['server'] = to_str(config.get(['server'], "0.0.0.0"))
        try:
            config['forbidden_ip'] = IPNetwork(config.get('forbidden_ip', '127.0.0.0/8'))
        except Exception as e:
            logging.error(e)
            sys.exit(2)
    if is_local and not config.get('password', None):
        logging.error('password not specified')
        sys.exit(2)

    if not is_local and not config.get('password', None) \
            and not config.get('port_password', None) \
            and not config.get('manager_address'):
        logging.error('password or port_password not specified')
        print_help(is_local)
        sys.exit(2)

    # TODO



def get_config(is_local):
    global verbose
    logging.basicConfig(level=logging.INFO, format='%(levelname)-s: %(message)s')
    if is_local:
        shortopts = 'hd:s:b:p:k:l:m:c:t:vqa'
        longopts = ['help', 'fast-open', 'pid-file=', 'log-file=', 'user=', 'version']
    else:
        shortopts = 'hd:s:p:k:m:c:t:vqa'
        longopts = ['help', 'fast-open', 'pid-file=', 'log-file=', 'workers=',
                    'forbidden-ip=', 'user=', 'manager-address=', 'version', 'prefer-ipv6']
    try:
        config_path = find_config()
        optlist, args = getopt.getopt(sys.argv[1:], shortopts, longopts)
        for key,value in optlist:
            if key == '-c':
                config_path = value
        if config_path:
            logging.info('loading config from %s' % config_path)
            with open(config_path, 'rb') as f:
                try:
                    config = parse_json_in_str(f.read().decode('utf8'))
                except ValueError as e:
                    logging.error('found an error in config.json')
                    sys.exit(1)
        else:
            config = {}
        v_count = 0
        for key,value in optlist:
            if key == '-p':
                config['server_port'] = int(value)
            elif key == '-k':
                config['password'] = to_bytes(value)
            elif key == '-l':
                config['local_port'] = int(value)
            elif key == '-s':
                config['server'] = to_str(value)
            elif key == '-m':
                config['method'] = to_str(value)
            elif key == '-b':
                config['local_address'] = to_str(value)
            elif key == '-v':
                v_count += 1
                config['verbose'] = v_count
            elif key == '-a':
                config['one_time_auth'] = True
            elif key == '-t':
                config['timeout'] = int(value)
            elif key == '--fast-open':
                config['fast_open'] = True
            elif key == '--workers':
                config['workers'] = int(value)
            elif key == '--manager-address':
                config['manager_address'] = value
            elif key == '--user':
                config['user'] = to_str(value)
            elif key in ('-h', '--help'):
                if is_local:
                    print_local_help()
                else:
                    print_server_help()
                sys.exit(0)
            elif key == '--version':
                print_shadowsocks()
            elif key == '-d':
                config['daemon'] = to_str(value)
            elif key == '--log-file':
                config['log-file'] = to_str(value)
            elif key == '--pid-file':
                config['pid-file'] = to_str(value)
            elif key == '-q':
                v_count -= 1
                config['verbose'] = v_count
            elif key == '--prefer-ipv6':
                config['prefer_ipv6'] = True

    except getopt.GetoptError as e:
        print(e, file=sys.stderr)
        print_help(is_local)
        sys.exit(2)

    if not config:
        logging.error("config not specified")
        print_help(is_local)
        sys.exit(2)

    config['password'] = to_bytes(config.get('password', ""))
    config['method'] = to_str(config.get('method', 'aes-256-cfb'))
    config['port_password'] = config.get('port_password',None )
    config['timeout'] = int(config.get('timeout', 300))
    config['fast_open'] = config.get('fast_open', False)
    config['workers'] = config.get('workers', 1)
    config['pid-file'] = config.get('pid-file', '/var/run/shadowsocks.pid')
    config['log-file'] = config.get('log-file', '/var/log/shadowsocks.log')
    config['verbose'] = config.get('verbose', False)
    config['local_address'] = to_str(config.get('local_address', '127.0.0.1'))
    config['local_port'] = config.get('local_port', 1080)
    config['one_time_auth'] = config.get('one_time_auth', False)
    config['prefer_ipv6'] = config.get('prefer_ipv6', False)
    config['server_port'] = config.get('server_port', 8388)

    logging.getLogger('').handlers = []
    logging.addLevelName(VERBOSE_LEVEL, "VERBOSE")
    if config['verbose'] >= 2:
        level = VERBOSE_LEVEL
    elif config['verbose'] == 1:
        level = logging.DEBUG
    elif config['verbose'] == -1:
        level = logging.WARN
    elif config['verbose'] <= -2:
        level = logging.ERROR
    else:
        level = logging.INFO
    verbose = config['verbose']
    logging.basicConfig(level=level, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    check_config(config, is_local)
    return config

def print_exception(e):
    global verbose
    logging.error(e)
    if verbose > 0:
        import traceback
        traceback.print_exc()
