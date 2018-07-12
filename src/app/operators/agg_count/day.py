# -- coding: UTF-8

import time

from operators.agg_count import OperatorAggCountBase


class Day(OperatorAggCountBase):
    def __init__(self):
        super(Day, self).__init__()

    def get_agg_key(self):
        return time.strftime("%Y-%m-%d", time.localtime())
