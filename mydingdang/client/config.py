import json, os, logging, os.path
from . import dingdangpath

CONFIG_FILE=os.path.join(dingdangpath.CONFIG_PATH, 'profile.json')
#print CONFIG_FILE

_logger = logging.getLogger(__name__)
_config = {}

def init():
	global _config
	
	try:
		with open(CONFIG_FILE, "r") as f:
			_config = json.loads(f.read())
			#print _config['name'], _config['age']
	except Exception:
		_logger.critical("can not open profile.json")
		
def get(item='', default=None):
	if not item :
		return _config
	try:
		return _config[item]
	except KeyError:
		logger.warning("%s not found in config file, default to %s", item, default)
		return default
		