# -- coding: UTF-8 

import os

from sources import SourceBase

from abc import ABCMeta, abstractmethod, abstractproperty

class Base(SourceBase):
    '''初始化构造函数'''
    __metaclass__ = ABCMeta
    def __init__(self, conf):
        super(Base, self).__init__(conf)

    def get_position_path(self):
        path = self._conf["path"]
        ref = self._conf["ref"]
        return "{}/{}.position".format(path, ref)

    def restore_hung_up(self, handler, ctx):
        '''IO流可以通过行号跟offset去定位最后读取的位置，所以不用实现'''
        pass