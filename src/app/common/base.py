# -- coding: UTF-8 
# 所有类的基类

from abc import ABCMeta, abstractmethod, abstractproperty

from utils import Logger

class Base(object):
    __metaclass__ = ABCMeta
    '''初始化构造函数'''
    def __init__(self):
        super(Base, self).__init__()
        
    @property
    def logger(self): 
        if not hasattr(self, "_logger"):
            self._logger = Logger().get_logger("{}@{}".format(self.__module__, self.__class__.__name__))
        
        return self._logger


class FlowBase(Base):
    __metaclass__ = ABCMeta
    '''初始化构造函数'''
    def __init__(self, conf):
        super(FlowBase, self).__init__()
        self._conf = conf
        self._args = self._conf

    def set_format_args(self, *args):
        '''
        设置settings.conf文件中format部分的格式化参数
        '''
        if len(args) == 0:
            args = ["notset"]

        # 获取settings.conf文件中format部分的格式化后的值
        _formated = "{}".format(*args)
        if "format" in self._conf:
            _formated = self._conf["format"].format(_formated)

        self._args = dict(self._conf, formated=_formated)
        
