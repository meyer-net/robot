# -- coding: UTF-8 
# https://pypi.python.org/pypi/redis
# https://www.cnblogs.com/wang-yc/p/5693288.html

import json

from drivers import RedisDriver

from store.cache import StoreCacheBase

class Redis(StoreCacheBase):
  '''初始化构造函数'''
  def __init__(self, host, port):
    super(Redis, self).__init__()
    self.host = host
    self.port = port
    self.pool = RedisDriver.ConnectionPool(host=host, port=port)
    self.connect = RedisDriver.StrictRedis(connection_pool=self.pool, socket_timeout=None, charset='utf-8', errors='strict', unix_socket_path=None)

  '''将数据读取成列表 print(json.loads(val)["Uri"])'''
  def read_buffer(self, mq_key):
    mq_list=[]
    mq_key = self._read_buffer(mq_key, lambda val: mq_list.append(val))
    return mq_key, mq_list

  '''将数据读取成实体列表'''
  def read_buffer_to_obj(self, mq_key):
    mq_list=[]
    mq_key = self._read_buffer(mq_key, lambda val: mq_list.append(json.loads(val)))
    return mq_key, mq_list

  '''读取数据函数基础调用'''
  def _read_buffer(self, mq_key, while_action):
    inner_mq_key = self._pop(mq_key)    
    while True:
      val = self._pop(inner_mq_key)
      if val == None:
        break

      while_action(val)
    
    return inner_mq_key
  
  '''出栈'''
  def _pop(self, mq_key):
    return self.connect.rpop(mq_key)

  def get(self, key):
    return self.connect.get(key)

  def set(self, key, value):
    return self.connect.set(key, value)
        

    