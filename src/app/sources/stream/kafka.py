# -- coding: UTF-8 

from sources import SourceBase
# from store.cache import StoreCacheKafka

class Kafka(SourceBase):
    '''初始化构造函数'''
    def __init__(self, conf):
        super(Kafka, self).__init__(conf)
        
    def get_position_key(self):
        pass

    def set_position(self, handler, position):
        pass
        
    def get_position(self, handler):
        pass
        
    def get_handler(self):
        pass

    def restore_hung_up(self, handler, ctx):
        pass
        
    def mount(self, handler, ctx):
        pass
