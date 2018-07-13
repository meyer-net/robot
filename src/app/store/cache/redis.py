# -- coding: UTF-8
# https://pypi.python.org/pypi/redis
# https://www.cnblogs.com/wang-yc/p/5693288.html

import json

from drivers import RedisDriver

from store.cache import StoreCacheBase

# netstat -an | grep 6379 |wc -l
class Redis(StoreCacheBase):
    def __init__(self, host, port):
        '''初始化构造函数'''
        super(Redis, self).__init__()
        self.host = host
        self.port = port
        self.pool = RedisDriver.ConnectionPool(host=host, port=port)

        connect_args = {
            "connection_pool": self.pool,
            "socket_timeout": None,
            "charset": "utf-8",
            "errors": "strict",
            "unix_socket_path": None
        }
        self.connect = RedisDriver.StrictRedis(**connect_args)

    def get(self, key):
        '''获取'''
        return self.connect.get(key)

    def set(self, key, value):
        '''设置'''
        return self.connect.set(key, value)

    def read_buffer(self, buffer_key):
        '''将数据读取成列表 print(json.loads(val)["Uri"])'''
        mq_list = []
        mq_key = self._read_buffer_action(
            buffer_key, lambda val: mq_list.append(val))
        return mq_key, mq_list

    def read_buffer_to_obj(self, buffer_key):
        '''将数据读取成实体列表'''
        mq_list = []
        mq_key = self._read_buffer_action(
            buffer_key, lambda val: mq_list.append(json.loads(val)))
        return mq_key, mq_list

    def read_list(self, mq_key):
        mq_list = []
        self._pop_action(mq_key, lambda val: mq_list.append(val))
        return mq_list

    def _read_buffer_action(self, buffer_key, while_action):
        '''读取数据函数基础调用'''
        mq_key = self._pop(buffer_key)
        self._pop_action(mq_key, while_action)
        return mq_key

    def _pop_action(self, mq_key, while_action):
        while True:
            val = self._pop(mq_key)
            if val == None:
                break

            while_action(val)

    def _pop(self, mq_key):
        '''出栈'''
        return self.connect.rpop(mq_key)
