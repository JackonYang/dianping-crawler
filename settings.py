#-*- coding:utf-8 -*-
from os.path import join, dirname

cache_root = join(dirname(__file__), 'cache')

db = 8

try:
    from local_settings import *
except Exception as e:
    pass

