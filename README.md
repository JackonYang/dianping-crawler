大众点评爬虫
============

抓取页面:

1. shop profile
2. shop review
3. user profile


## 用法

#### Scanner

以 shop review 为例, 下载的数据保存在
`/home/jackon/media/dianping/reviews` 目录下.
希望从 reviews 页面中找出所有的 user-id

```python
import re
from scanner import Scanner

uid_ptn = re.compile(r'href="/member/(\d+)(?:\?[^"]+)?"')
json_name = 'uid.json'

s = Scanner(json_name, uid_ptn)
s.scan('/home/jackon/media/dianping/reviews')

for k, v in s.data.items():
    print '{} items in {}'.format(len(v), k)
```

扫描完成后输出如下格式:
```shell
20 items in 6845514_1.html
20 items in 550426_18.html
0 items in 3926803_2.html
20 items in 4550817_72.html
0 items in 6006104_3.html
0 items in 22281825_3.html
20 items in 2817364_18.html
20 items in 18221165_1.html
20 items in 550099_10.html
20 items in 21293756_2.html
20 items in 586687_31.html
20 items in 20815806_10.html
```


#### 压缩 / 解压数据的 shell 命令

```shell
$ time 7z x shop_prof_20150821.7z
# Folders: 1
# Files: 164805
# Size:       18068875270
# Compressed: 359098116

# real    164m37.408s
# user    18m2.913s
# sys 39m50.784s
$ ls shop_prof | wc -l
# 164805
7z l shop_prof_20150821.7z | grep '.html' | wc -l
# 164805
```
