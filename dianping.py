# -*- Encoding: utf-8 -*-
import os
from os.path import join, exists
import re
from crawler.request import request
from settings import cache_root

page_types = ['user_prof', 'shop_prof', 'review']
for t in page_types:
    if not exists(join(cache_root, t)):
        os.makedirs(join(cache_root, t))

uid_ptn = re.compile(r'href="/member/(\d+)(?:\?[^"]+)?"')
sid_ptn = re.compile(r'href="/shop/(\d+)(?:\?[^"]+)?"')
rev_ptn = re.compile(r'<li[^>]+id="rev_(\d+)"')


def grab_user_prof(key):
    url = 'http://www.dianping.com/member/{}'.format(key)
    fn = join(cache_root, 'user_prof', '{}_user.html'.format(key))
    c = request(url.format(key), filename=fn)
    return set(uid_ptn.findall(c)) - {key}


def grab_shop_prof(key):
    url = 'http://www.dianping.com/shop/{}'.format(key)
    fn = join(cache_root, 'shop_prof', '{}_shop.html'.format(key))
    c = request(url.format(key), filename=fn)
    return set(sid_ptn.findall(c)) - {key}


if __name__ == '__main__':
    # from test_tools import request

    uid = '3601131'
    print grab_user_prof(uid)

    sid = '5195730'  # 45 reviews on 2015.8.3
    print grab_shop_prof(sid)
