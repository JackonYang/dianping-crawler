# -*- Encoding: utf-8 -*-
import os
from os.path import join, exists
import re

from crawler.request import request, request_pages
from crawler.scanner import Scanner
from crawler.job_engine import JobPool

from settings import cache_root, db

page_types = ['user_prof', 'shop_prof', 'reviews']
page_path = {name: join(cache_root, name) for name in page_types}
for path in page_path.values():
    if not exists(path):
        os.makedirs(path)

uid_ptn = re.compile(r'href="/member/(\d+)(?:\?[^"]+)?"')
sid_ptn = re.compile(r'href="/shop/(\d+)(?:\?[^"]+)?"')
rev_ptn = re.compile(r'<li[^>]+id="rev_(\d+)"')
find_rev = lambda c, key: set(rev_ptn.findall(c))


def grab_user_prof(key):
    url = 'http://www.dianping.com/member/{}'.format(key)
    fn = join(page_path['user_prof'], '{}_user.html'.format(key))
    c = request(url.format(key), filename=fn)
    return set(uid_ptn.findall(c))


def grab_shop_prof(key):
    url = 'http://www.dianping.com/shop/{}'.format(key)
    fn = join(page_path['shop_prof'], '{}_shop.html'.format(key))
    c = request(url.format(key), filename=fn)
    return set(sid_ptn.findall(c)) - {key}


def grab_reviews(key, max_page=100):
    url = 'http://www.dianping.com/shop/{key}/review_more?pageno={page}'

    filename_ptn = join(page_path['reviews'], '{}_{}.html')  # key, page
    return request_pages(key, range(1, max_page), url, find_rev,
                         filename_ptn=filename_ptn)


def init_user_prof(host, job_name='user_prof'):
    s = Scanner(join(cache_root, 'uid.json'), uid_ptn)
    s.scan(page_path['reviews'])
    total = {v for vs in s.data.values() for v in vs}
    done = {fn[:fn.find('_')]
            for fn in os.listdir(page_path[job_name])}
    job = JobPool(job_name, host, db=db)
    job.init(total, done)


if __name__ == '__main__':
    """
    from test.test_tools import request, request_pages

    uid = '3601131'
    print grab_user_prof(uid)

    sid = '5195730'  # 45 reviews on 2015.8.3
    print grab_shop_prof(sid)
    print grab_reviews(sid)
    """

    job = JobPool('user_prof', 'jackon.me', db=db)
    job.run(grab_user_prof)
