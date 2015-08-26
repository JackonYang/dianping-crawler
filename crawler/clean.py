# -*- Encoding: utf-8 -*-
__author__ = 'vivian'
import re
import os
import json

from scanner import Scanner
 
revp_ptn = re.compile(r'(\d+)_(\d+)')
revp_list = {}
data = {}
ret_ex = []
ret_vac = []
path = 'D:\github\data\shop_review'

uid_ptn = re.compile(r'href="/member/(\d+)(?:\?[^"]+)?"')
filename = 'uid.json'
s = Scanner(filename, uid_ptn)  # 找到每个店铺的评价页面的用户id，输出在uid.json中，key为店铺评价页面，values为对应页面的
                                # 评价的用户id
s.scan(path, save_period=500)

count = 0
rid = []
for k, v in  s.data.items():  # 店铺评价页面的首页没有评价的店铺。输出在 rid.json中。
    if len(v) == 0 and k.endswith('_1.html'):
        count += 1
        rid.append(k)
print count  # 输出符合条件的店铺总数
with open("rid.json",'w ') as fp:
    json.dump(rid, fp)


for f in os.listdir(path):  # 搜索目标文件夹中的文件名（店铺及评价页面），输出在revp.json中

    # key为店铺id，对应的values为爬取到的店铺评价页
    revp_ret = revp_ptn.findall(f)
    for k,v in revp_ret:
        if k in revp_list:
            revp_list[k].append(v)
        else:
            revp_list[k] = [v]

with open("revp.json",'w') as fp:
    json.dump(revp_list,fp)

with open("uid.json",'r') as fd:
    data = json.load(fd)

for k,v in revp_list.items():  # 找到每个店铺相应的评价最后一页的评价用户id，输出目标文件不存在（ret_ex）和有用户评价的
    file = k+'_'+str(len(v))+'.html'  # 文件（ret_vac),最终输出保存在result.json中
    if file not in data.keys():
        ret_ex.append(file)
    elif data[file]!=[]:
        ret_vac.append(file)
    else:
        pass

js_dic = {'these are not exist!':ret_ex,'these are not empty!':ret_vac}
with open("result.json",'w') as fr:
    json.dump(js_dic,fr, indent=4)