# -- coding: UTF-8 

from common import SuperBase

from abc import ABCMeta, abstractmethod, abstractproperty

class Base(SuperBase):
    __metaclass__ = ABCMeta
    '''初始化构造函数'''
    def __init__(self, conf):
        super(Base, self).__init__()
        self._conf = conf

    '''读取配置文件内容'''
    def get_conf(self, key):
        if key in self._conf:
            return self._conf[key]
        return None

    '''设置配置文件内容'''
    def set_conf(self, key, value):
        self._conf[key] = value

    '''
    用于标记最后信息的读取位置
    '''
    @abstractmethod
    def set_position(self, handler, position):
        raise NotImplementedError

    '''
    用于获取最后信息的读取位置
    '''
    @abstractmethod
    def get_position(self, handler):
        raise NotImplementedError

    '''恢复上次中断时异常挂起的作业'''
    @abstractmethod
    def restore_hung_up(self, handler, ctx):
        raise NotImplementedError

    '''获取处理源数据的句柄对象，避免重复创建上引起的性能消耗'''
    @abstractmethod
    def get_handler(self):
        raise NotImplementedError
        
    '''
    将缓冲区的内容装载至指定位置
    外围项目启动通过当前环境的解释器去运行脚本程式，否则会出现找不到现有项目模块的问题
    '''
    @abstractmethod
    def mount(self, handler, ctx):
        raise NotImplementedError