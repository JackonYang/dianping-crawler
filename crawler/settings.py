# -*- coding:utf-8 -*-
REDIS_CONN = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': 8,
}

WECHAT_CONN = {
    'username': '',
    'password': '',
}

DELAY_BOTTOM = 5
DELAY_TOP = 10

NOTIFY_IDS = [
    '2271762240',  # k
    '98160640',  # v
]

MSG_SIGNATURE = 'AutoSend by Dianping Crawler'


try:
    from local_settings import *
except Exception as e:
    pass
