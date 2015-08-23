# -*- Encoding: utf-8 -*-
import redis

from os.path import dirname, join
from log4f import debug_logger

BASE_DIR = dirname(__file__)
log = debug_logger(join(BASE_DIR, 'log/download'), 'root.download')


class JobPool:
    def __init__(self, job_name, total, done,
                 host='localhost', port=6379, db=0,
                 timeout=10):
        self.timeout = timeout
        self.db = redis.StrictRedis(host, port, db)
        self.total_tbl = '{}:total'.format(job_name)
        self.todo_tbl = '{}:todo'.format(job_name)
        self.name = job_name

        self.init_data(total, done)

    def init_data(self, total, done):
        self.db.delete(self.total_tbl)
        self.db.delete(self.todo_tbl)

        todo = set(total) - set(done)

        self.db.sadd(self.total_tbl, *total)
        self.db.rpush(self.todo_tbl, *todo)

    def count_todo(self):
        return self.db.llen(self.todo_tbl)

    def count_total(self):
        return self.db.scard(self.total_tbl)

    def run(self, callback, recursive=False):
        print '{} start.TODO/Total: {}/{}'.\
            format(self.name, self.count_todo(), self.count_total())
        key = self._next()
        while key:
            log.info('downloading {}-{}'.format(self.name, key))
            try:
                items = callback(key)
                log.info(
                    '{} items in {}-{}'.format(
                        len(items), self.name, key))
                if recursive:
                    self._add(*items)
            except Exception as e:
                log.error('{}. ID={}'.format(e, key))
                self.db.rpush(self.todo_tbl, key)
            key = self._next()

        info = '{} done. {} got'.format(self.name, self.count_total())
        print(info)
        log.warning(info)

    def _next(self):
        key = self.db.blpop(self.todo_tbl, self.timeout)
        return key and key[1]

    def _add(self, *keys):
        for item in keys:
            if self.db.sadd(self.total_tbl, item):
                self.db.rpush(self.todo_tbl, item)


if __name__ == '__main__':
    job_name = 'job_test'
    total = [str(i) for i in range(1, 9)]
    done = [str(i) for i in range(3, 9, 2)]

    job = JobPool(job_name, total, done, db=9, timeout=2)

    job.run(lambda key: [11, 12])

    job.init_data(total, done)
    job.run(lambda key: [11, 12], recursive=True)
