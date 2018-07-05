# -- coding: UTF-8 
# expamples: https://github.com/wdm0006/flink-python-examples, below flink 1.5

import os
import time
import json

from common import SuperBase
from operators import OperatorBase

from org.apache.flink.streaming.api.functions.source import SourceFunction
from org.apache.flink.api.common.functions import FlatMapFunction, ReduceFunction
from org.apache.flink.api.java.functions import KeySelector
# from org.apache.flink.streaming.api.collector.selector import OutputSelector;
from org.apache.flink.streaming.api.windowing.time.Time import milliseconds
from org.apache.flink.core.fs.FileSystem import WriteMode

class FlatMap(FlatMapFunction, SuperBase):
    def __init__(self, *depth_params):
        super(FlatMap, self).__init__()
        self.current_time = time.time()
        self.depth_params = depth_params

    def flatMap(self, value, collector):
        try:
            jsv = json.loads(value, "UTF-8")
            receive_time = jsv["ReceiveTime"]
            group_key = self.read_from_jsonobj(jsv)

            # 获取统计的延迟时间
            # receive_time = int(jsv["ReceiveTime"])
            # delayTime = current_time - receive_time
            
            #collect参数中的*tuple为数组类型，按参数的位置，提供给下游keyby、sum等函数运算
            collector.collect((1, group_key, receive_time)) 
        except ValueError as err:
            self.logger.error(err)

    # 根据初始化深度获取JSON内值
    def read_from_jsonobj(self, jsonobj):
        val = jsonobj
        for item in self.depth_params:
            val = val[item]
        
        return val

# KeyBy之后，实际上按照需要的维度进行分组了，不会出现重复维度的数据
class KeyBy(KeySelector):
    def getKey(self, input):
        return input[1]

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
    def __init__(self, *depth_params):
        '''
        参数1：深度参数，表示按深度取json值，位置所在参数表示作为后续计算依据。例如("Headers", "host")
        '''
        super(Base, self).__init__()
        self.flat_map = FlatMap(*depth_params)

    def get_stream(self, stream):
        '''
        流逻辑，必须实现
        '''
        return stream.flat_map(self.flat_map) \
            .key_by(KeyBy()) \
            .time_window(milliseconds(50)) \
            .reduce(Reduce())

    def get_sink(self, sink):
        '''
        流逻辑，必须实现
        '''
        sink.set_format_args(["{}_{}".format(self.__module__, self.__class__.__name__)])
        return sink