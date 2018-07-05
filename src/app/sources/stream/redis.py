# -- coding: UTF-8 

from sources import SourceBase
from store.cache import StoreCacheRedis

class Redis(SourceBase):
    '''初始化构造函数'''
    def __init__(self, conf):
        super(Redis, self).__init__(conf)

    def get_handler(self):
        try:
            return self._adapter
        except AttributeError as err:
            self._adapter = StoreCacheRedis(host=self._conf["host"], port=self._conf["port"])

        return self._adapter

    def get_position_key(self):
        return "{}_position".format(self._conf["key"])

    def set_position(self, handler, position):
        handler.set(self.get_position_key(), position)
        
    def get_position(self, handler):
        return handler.get(self.get_position_key())

    def restore_hung_up(self, handler, ctx):
        position = self.get_position(handler)
        return self.collect_from_adapter(handler, ctx, position)
        
    '''
    将缓冲区的内容装载至指定位置
    外围项目启动通过当前环境的解释器去运行脚本程式，否则会出现找不到现有项目模块的问题
    '''
    def mount(self, handler, ctx):
        return self.collect_from_adapter(handler, ctx, self._conf["key"])

    '''
    内部函数，用于收集来自于适配器中的数据
    '''
    def collect_from_adapter(self, handler, ctx, buffer_key):        
        mq_key, mq_elements = handler.read_buffer(buffer_key)

        if mq_key == None:
            self.logger.error("{} -> None key named '{}'".format(buffer_key, mq_key))
            return
        else:
            self.logger.debug("Collect key '{}'".format(mq_key))
        
        for element in mq_elements:
            self.logger.debug("Collect element '{}'".format(element))
            ctx.collect(element)

        return mq_key
