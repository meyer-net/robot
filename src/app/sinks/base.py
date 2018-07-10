# -- coding: UTF-8 

from common import SuperBase

from abc import ABCMeta, abstractmethod, abstractproperty

class Base(SuperBase):
    __metaclass__ = ABCMeta
    '''初始化构造函数'''
    def __init__(self, conf):
        super(Base, self).__init__()
        self._conf = conf
        self._args = self._conf

    def set_format_args(self, *args):
        '''
        设置settings.conf文件中format部分的格式化参数
        '''
        if len(args) == 0:
            args = ["notset"]

        # 获取settings.conf文件中format部分的格式化后的值
        if "format" in self._conf:
            _formated = self._conf["format"].format(*args)
            self._args = dict(self._conf, formated=_formated)

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
