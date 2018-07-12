# -- coding: UTF-8

from operators.calc_count import OperatorCalcCountBase


class Ip(OperatorCalcCountBase):
    def __init__(self):
        super(Ip, self).__init__("Headers", "host")
