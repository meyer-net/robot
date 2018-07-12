# -- coding: UTF-8 

from common import FlowBase

from abc import ABCMeta, abstractmethod, abstractproperty

class Base(FlowBase):
    __metaclass__ = ABCMeta
    '''初始化构造函数'''
    def __init__(self, conf):
        super(Base, self).__init__(conf)

    def set_stream_args(self, **kvs):
        '''
        设置write_by_stream下调用时参数
        '''
        self._kvs = dict(kvs)
        
    @abstractmethod
    def write_by_stream(self, data_stream):
        '''
        该函数指示将指定数据流写入至目标处
        '''
        raise NotImplementedError
