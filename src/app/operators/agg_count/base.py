# -- coding: UTF-8 

import time

from common import SuperBase
from operators import OperatorBase

from abc import ABCMeta, abstractmethod, abstractproperty

from org.apache.flink.streaming.api.functions.source import SourceFunction
from org.apache.flink.api.common.functions import FlatMapFunction, ReduceFunction
from org.apache.flink.api.java.functions import KeySelector
from org.apache.flink.streaming.util.serialization import SerializationSchema
from org.apache.flink.streaming.api.windowing.time.Time import milliseconds
from org.apache.flink.core.fs.FileSystem import WriteMode

class FlatMap(FlatMapFunction, SuperBase):
    def __init__(self, operator):
        super(FlatMap, self).__init__()
        self._operator = operator

    def flatMap(self, value, collector):
        try:
            # merge_list = [self._operator.get_agg_key()]
            value_list = value.lstrip('[').rstrip(']').lstrip('(').rstrip(')').split(",")
            time_stamp = float(value_list[2].strip())
            time_array = time.localtime(time_stamp)

            value_list[0] = int(value_list[0])
            value_list[1] = value_list[1].decode()
            value_list[2] = time.strftime("%Y-%m-%d", time_array)

            tuple_collect = tuple(value_list)
            collector.collect(tuple_collect)

        except ValueError as err:
            self.logger.error(err)

# KeyBy之后，实际上按照需要的维度进行分组了，不会出现重复维度的数据
class KeyBy(KeySelector):
    def getKey(self, input):
        return input[2]

# KeyBy之后，依据FlatMap返回的类型为Tuple的值后执行的运算
class Reduce(ReduceFunction):
    def reduce(self, prev, this):
        # 此处 prev_key = this_key
        prev_count, prev_key, prev_receive_time = prev
        this_count, this_key, this_receive_time = this
            
        reduce_count = prev_count + this_count
        
        return (reduce_count, this_key, this_receive_time)

class Base(OperatorBase):
    '''
    父类必须继承超类OperatorBase
    '''
    __metaclass__ = ABCMeta
    def __init__(self):
        super(Base, self).__init__()

    @abstractmethod
    def get_agg_key(self):
        '''
        分组依据KEY，子类必须实现
        '''
        raise NotImplementedError

    def get_stream(self, stream):
        '''
        流逻辑，必须实现
        '''
        return stream.flat_map(FlatMap(self)) \
            .key_by(KeyBy()) \
            .time_window(milliseconds(1000)) \
            .reduce(Reduce())

    def get_sink(self, sink):
        '''
        流逻辑，必须实现
        '''
        return sink
