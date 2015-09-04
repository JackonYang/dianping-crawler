# -*- Encoding: utf-8 -*-
import re
import socket
from httplib2 import Http

import time
import random

from os.path import dirname, join
from log4f import debug_logger

BASE_DIR = dirname(__file__)
log = debug_logger(join(BASE_DIR, 'log/request'), 'root.request')
_last_req = None


def delay(bottom=5, top=20):
    global _last_req
    if _last_req is None:
        _last_req = time.time()
        return 0

    period = max(0,
                 _last_req+random.uniform(bottom, top)-time.time())
    log.debug('...wait {:.2f} sec'.format(period))
    time.sleep(period)
    _last_req = time.time()
    return period


def wait(f):
    def _wrap_func(*args, **kwargs):
        delay()
        return f(*args, **kwargs)
    return _wrap_func

headers_templates = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
    'Content-type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Host': 'www.dianping.com',
    'Referer': 'http://www.dianping.com/',
    'DNT': '1',
    'Cookie': '_hc.v="\"34c79447-2d40-484c-b3a8-111ed94f15c6.1441030730\""; PHOENIX_ID=0a010439-14f86a71577-18284d; __utma=205923334.1131356186.1441030729.1441075605.1441099049.5; __utmb=205923334.25.10.1441099049; __utmc=205923334; __utmz=205923334.1441030729.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); JSESSIONID=A3752DEEAE18623895C02473CF612F4E; aburl=1; cy=1; cye=shanghai',
}


@wait
def request(url, timeout=2, method='GET', filename=None):
    """return None if timeout"""
    h = Http(timeout=timeout)
    try:
        log.debug('request {}'.format(url))
        rsp, content = h.request(url, method, headers=headers_templates)
    except socket.timeout:
        return None

    if filename:
        with open(filename, 'w') as f:
            f.write(content)
        log.debug('response saved. filename={}'.format(filename))

    return content


def request_pages(key, page_range, url_ptn, find_items, resend=3,
                  min_num=0, max_failed=5, filename_ptn=None):
    """request a list of pages in page_range

    """
    items_total = set()  # items will be out of order if some pages failed
    failed = set()

    for page in page_range:

        filename = filename_ptn and filename_ptn.format(key, page)
        page_url = url_ptn.format(key=key, page=page)
        content = request(page_url, filename=filename)

        if content is not None:
            items_page = find_items(content, key)
            if items_page and len(items_page) > min_num:
                items_total.update(items_page)
            else:
                log.debug('nothing in page {} of {}'.format(page, key))
                break
        else:
            log.warning('failed to request page {} of {}'.format(page, key))
            failed.add(page)
            if len(failed) > max_failed:
                log.error('more timeout than {}'.format(max_failed))
                return

    if failed:
        if not resend:
            return None
        log.debug('resend failed pages of {}'.format(key))
        items_more = request_pages(key, failed, url_ptn, find_items,
                                   resend-1, min_num, filename_ptn)
        if items_more is None:
            return None
        items_total.update(items_more)
    return items_total


if __name__ == '__main__':

    url = 'http://www.dianping.com/shop/{key}/review_more?pageno={page}'
    find_uid = lambda content, key: \
        re.compile(r'href="/member/(\d+)">(.+?)</a>').findall(content)

    uid = '5195730'  # 45 reviews on 2015.8.3
    pages = range(1, 9)

    ret = request_pages(uid, pages, url, find_uid, resend=3,
                        min_num=0, max_failed=5, filename_ptn=None)
    for user, name in ret:
        print user, name
    print len(ret)
