# -- coding: UTF-8 

from common import SuperBase

from abc import ABCMeta, abstractmethod, abstractproperty

class Base(SuperBase):
    __metaclass__ = ABCMeta
    '''初始化构造函数'''
    def __init__(self, conf):
        super(Base, self).__init__()
        self._conf = conf
        self._args = []

    def set_format_args(self, *args):
        '''
        设置settings.conf文件中format部分的格式化参数
        '''
        if len(args) == 0:
            args = ["notset"]

        self._args = list(*args)

    def get_format_val(self):
        '''
        获取settings.conf文件中format部分的格式化后的值
        '''
        args = self._args
        return self._conf["format"].format(*args)

    @abstractmethod
    def write_by_stream(self, data_stream):
        '''
        该函数指示将指定数据流写入至目标处
        '''
        raise NotImplementedError