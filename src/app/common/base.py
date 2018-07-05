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
        