# -- coding: UTF-8

from sources import SourceBase
from store.cache import StoreCacheRedis


class Redis(SourceBase):
    def __init__(self, conf):
        '''初始化构造函数'''
        super(Redis, self).__init__(conf)

    def get_handler(self):
        return StoreCacheRedis(host=self._conf["host"], port=self._conf["port"])

    def get_position_key(self):
        return "{}_position".format(self._conf["key"])

    def set_position(self, handler, position):
        handler.set(self.get_position_key(), position)

    def get_position(self, handler):
        return handler.get(self.get_position_key())

    def restore_hung_up(self, handler, ctx):
        mq_key = self.get_position(handler)
        mq_elements = handler.read_list(mq_key)
        return self._collect_from_adapter(ctx, mq_key, mq_elements)

    def mount(self, handler, ctx):
        '''
        将缓冲区的内容装载至指定位置
        外围项目启动通过当前环境的解释器去运行脚本程式，否则会出现找不到现有项目模块的问题
        '''
        mq_key, mq_elements = handler.read_buffer(self._conf["key"])
        return self._collect_from_adapter(ctx, mq_key, mq_elements)

    def _collect_from_adapter(self, ctx, mq_key, mq_elements):
        '''
        内部函数，用于收集来自于适配器中的数据
        '''
        if mq_key != None:
            self.logger.debug("Collect key '{}'".format(mq_key))

            for element in mq_elements:
                self.logger.debug("Collect element '{}'".format(element))
                ctx.collect(element)

        return mq_key
