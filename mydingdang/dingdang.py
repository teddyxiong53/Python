#!/usr/bin/env python

import argparse
import os, sys
import os.path
import logging
from client import dingdangpath
from client import config

print dingdangpath.APP_PATH
parser = argparse.ArgumentParser(description="this is my dingdang speaker")
parser.add_argument("--local", action="store_true", help="use stdin to input rather than mic ")
parser.add_argument("--diagnose", action="store_true", help="to diagnose the network")
parser.add_argument("--verbose", action="store_true", help="verbose mode")


args = parser.parse_args()

#print args.local

class Dingdang(object):
	def __init__(self):
		self._logger = logging.getLogger(__name__)
		config.init()
		stt_engine_slug = config.get('stt_engine', 'sphinx')
		stt_engine_class = stt.get_engine_by_slug(stt_engine_slug)
		
		slug = config.get('stt_passive_engine', stt_engine_slug)
		stt_passive_engine_class = stt.get_engine_by_slug(slug)
		
		
if __name__ == '__main__':
	logging.basicConfig(
		format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s",
		level=logging.INFO
	)
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)
	try :
		app = Dingdang()
	except Exception:
		logger.exception("error occured")
		sys.exit(1)
		
	try:
		app.run()
	except KeyboardInterrupt:
		logger.info("dingdang get keyboard interrupt")
		sys.exit(0)
	except Exception:
		logger.info("dingdang run error")
		sys.exit(1)
		
		