# -- coding: UTF-8

import time

from operators.agg import OperatorAggBase

class Day(OperatorAggBase):
  '''初始化构造函数'''

  def __init__(self):
    super(Day, self).__init__()

  def get_group_key(self):
      return time.strftime("%Y-%m-%d", time.localtime())
