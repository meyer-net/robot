# -- coding: UTF-8 

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
    def __init__(self, func_get_group_key):
        super(FlatMap, self).__init__()
        self._func_get_group_key = func_get_group_key

    def flatMap(self, value, collector):
        try:
            count_key = tuple(value.lstrip('(').rstrip(')').split(","))
            collector.collect((count_key[0], self._func_get_group_key()))
        except ValueError as err:
            self.logger.error(err)

# KeyBy之后，实际上按照需要的维度进行分组了，不会出现重复维度的数据
class KeyBy(KeySelector):
    def getKey(self, input):
        return input[1]

# KeyBy之后，依据FlatMap返回的类型为Tuple的值后执行的运算
class Reduce(ReduceFunction):
    def reduce(self, prev, this):
        # 此处 prev_key = this_key
        prev_count, prev_key = prev
        this_count, this_key = this
            
        reduce_count = prev_count + this_count
        
        return (reduce_count, this_key)

class Base(OperatorBase):
    '''
    父类必须继承超类OperatorBase
    '''
    __metaclass__ = ABCMeta
    def __init__(self):
        super(Base, self).__init__()

    @abstractmethod
    def get_group_key(self):
        '''
        分组依据KEY，子类必须实现
        '''
        raise NotImplementedError

    def get_stream(self, stream):
        '''
        流逻辑，必须实现
        '''
        return stream.flat_map(FlatMap(self.get_group_key)) \
            .key_by(KeyBy()) \
            .time_window(milliseconds(50)) \
            .reduce(Reduce())

    def get_sink(self, sink):
        '''
        流逻辑，必须实现
        '''
        sink.set_format_args(["{}_{}".format(self.__module__, self.__class__.__name__)])
        sink.set_stream_args(mode=WriteMode.OVERWRITE)
        return sink
