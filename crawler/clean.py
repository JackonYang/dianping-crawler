# -*- Encoding: utf-8 -*-
__author__ = 'vivian'
import re
import json

from scanner import Scanner

uid_ptn = re.compile(r'href="/member/(\d+)(?:\?[^"]+)?"')
rid_ptn = re.compile(r'shop_review\\(\d*)')
filename = 'uid.json'

s = Scanner(filename, uid_ptn)

s.scan('D:\github\data\shop_review', save_period=500)

count = 0
for k, v in  s.data.items():
    if len(v) == 0 and k.endswith('_1.html'):
        count += 1
        rid_ret = rid_ptn.findall(k)
        with open("rid.json",'a') as fp:
            json.dump(rid_ret,  fp)

        print rid_ret

print count
