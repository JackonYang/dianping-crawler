# -*- Encoding: utf-8 -*-
__author__ = 'vivian'
import re
import os
import json

from scanner import Scanner

revp_ptn = re.compile(r'(\d+)_(\d+)')
revp_list = {}
for f in os.listdir('D:\github\data\shop_review'):
    revp_ret = revp_ptn.findall(f)
    for k,v in revp_ret:
        if k in revp_list:
            revp_list[k].append(v)
        else:
            revp_list[k] = [v]
with open("revp.json",'a') as fp:
    json.dump(revp_list,fp)




#sid_ptn = re.compile('')