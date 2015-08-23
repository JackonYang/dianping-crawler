# -*- Encoding: utf-8 -*-
import os
from os.path import join, exists
import re
from crawler.request import request, request_pages
from settings import cache_root

page_types = ['user_prof', 'shop_prof', 'reviews']
for t in page_types:
    if not exists(join(cache_root, t)):
        os.makedirs(join(cache_root, t))

uid_ptn = re.compile(r'href="/member/(\d+)(?:\?[^"]+)?"')
sid_ptn = re.compile(r'href="/shop/(\d+)(?:\?[^"]+)?"')
rev_ptn = re.compile(r'<li[^>]+id="rev_(\d+)"')
find_rev = lambda c, key: set(rev_ptn.findall(c))


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


def grab_reviews(key, max_page=100):
    url = 'http://www.dianping.com/shop/{key}/review_more?pageno={page}'

    filename_ptn = join(cache_root, 'reviews', '{}_{}.html')  # key, page
    return request_pages(key, range(1, max_page), url, find_rev,
                         filename_ptn=filename_ptn)


if __name__ == '__main__':
    # from test_tools import request, request_pages

    uid = '3601131'
    print grab_user_prof(uid)

    sid = '5195730'  # 45 reviews on 2015.8.3
    print grab_shop_prof(sid)
    print grab_reviews(sid)
