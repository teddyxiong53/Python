import sys,os,os.path
import logging
import getopt
import json

from .common import to_bytes, to_str

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

        return config
    except getopt.GetoptError as e:
        pass
