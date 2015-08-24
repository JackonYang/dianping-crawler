# -*- Encoding: utf-8 -*-
import re
import os
from os.path import join
import json


class Scanner:
    def __init__(self, cache_filename, ptn):
        self.cache_name = cache_filename
        self.ptn = ptn
        self.data = self.load()

    def scan(self, path, save_period=2000):
        total = {fn for fn in os.listdir(path)
                 if os.path.isfile(join(path, fn))}
        todo = total - set(self.data.keys())

        print 'scanning {}/{}'.format(len(todo), len(total))
        for i, filename in enumerate(todo):
            with open(join(path, filename), 'r') as f:
                c = ''.join(f.readlines())
            self.data[filename] = list(set(self.ptn.findall(c)))

            if i % save_period == 0:
                print '...saving. {} done.'.format(i+1)
                self.save()

        self.save()
        print 'scan finished. {} new files.'.format(len(todo))

    def load(self):
        data = dict()
        if os.path.exists(self.cache_name):
            with open(self.cache_name, 'r') as fr:
                data = json.load(fr)
        return data

    def save(self):
        with open(self.cache_name, 'wb') as fw:
            json.dump(self.data, fw, indent=4)


if __name__ == '__main__':
    fn = 'test.json'
    if os.path.exists(fn):
        os.remove(fn)

    ptn = re.compile(r'import (\w+)')
    s = Scanner(fn, ptn)

    s.scan('.', save_period=7)
    print '----------'
    s.scan('.', save_period=7)
    print '----------'
    s.scan('..', save_period=7)
