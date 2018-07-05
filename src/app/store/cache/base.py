# -- coding: UTF-8 

from common import SuperBase

from abc import ABCMeta, abstractmethod, abstractproperty

class Base(SuperBase):
  __metaclass__ = ABCMeta
  def __init__(self):
    pass

  @abstractmethod
  def read_buffer(self, key):
    raise NotImplementedError  