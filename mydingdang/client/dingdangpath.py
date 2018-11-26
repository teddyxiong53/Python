import json, os, logging

APP_PATH= os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

DATA_PATH = os.path.join(APP_PATH, 'static')
LIB_PATH = os.path.join(APP_PATH, 'client')

CONFIG_PATH = os.path.join(APP_PATH, 'config')


