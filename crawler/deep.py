# -*- Encoding: utf-8 -*-
import os
import re
import json

path = 'D:/github/data/shop_review'
info_ptn = re.compile(ur'href="/member/(\d*)">.*?title="(.*?)"',re.DOTALL)  # 匹配用户id 和他的贡献值

err = []
id_sc = {}
re_id = {}

for f in os.listdir(path):  # 进入一个店铺的一页评论。
    filename = path + '/'+f
    ids = []
    try:
        with open(filename,'r') as fp:
            content = ''.join(fp.readlines())
    except:
        err.append(filename)     # 若打不开文件，将其放入 err 中
    else:
        info_ret = info_ptn.findall(content)
        for id,sc in info_ret:  # 找出没有分数的用户，并放入到list,ids中
            id_sc[id] = sc
            if len(sc) == 0:
                ids.append(id)
    re_id[f] = ids  # 店铺id为key, 最终所求（需要爬主页）的用户id为 values.


with open('err.json','w') as fe:    # 打不开的文件
    json.dump(err,fe,indent=4)
with open('id_sc.json','w') as fi:  # 用户及他的贡献值
    json.dump(id_sc,fi,indent=4)
with open('re_id.json','w') as fd:  # 没有贡献值的用户
    json.dump(re_id,fd,indent=4)
