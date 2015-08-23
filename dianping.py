# -*- Encoding: utf-8 -*-
import os
from os.path import dirname, join, exists
import re
from crawler.request import request

cache_root = join(dirname(__file__), 'cache')

page_types = ['user_prof']
for t in page_types:
    if not exists(join(cache_root, t)):
        os.makedirs(join(cache_root, t))

uid_ptn = re.compile(r'href="/member/(\d+)(?:\?[^"]+)?"')


def grab_user_prof(key):
    url = 'http://www.dianping.com/member/{}'.format(key)
    fn = join(cache_root, 'user_prof', '{}_user.html'.format(key))
    c = request(url.format(key), filename=fn)
    return set(uid_ptn.findall(c)) - {key}


if __name__ == '__main__':
    ret = grab_user_prof('3601131')
    print ret
    print len(ret)
