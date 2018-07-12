# -- coding: UTF-8 
################################################################################
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

import chardet
# from bs4 import BeautifulSoup
from abc import ABCMeta, abstractmethod, abstractproperty

from org.apache.flink.api.common.functions import MapFunction
from org.apache.flink.core.fs.FileSystem import WriteMode

from common import SuperBase

class CharsetEncodeMapFunction(MapFunction):
    def __init__(self, charset):
        self._charset = charset

    def map(self, value):
        value_str = value.encode("raw_unicode_escape")
        encode_info = chardet.detect(value_str)
        value_encode_type = encode_info.get("encoding")

        # GBK 是 GB2312 的超集，当字符在 GBK 集合中，但不在 GB2312 时，就会乱码。
        if value_encode_type == "gb2312":
            value_encode_type = "gbk"
        
        if value_encode_type == self._charset:
            return value

        return value_str.decode(value_encode_type).encode(self._charset) #BeautifulSoup(value, fromEncoding=encode_info.encoding)

class GBKEncodeMapFunction(CharsetEncodeMapFunction):
    def __init__(self):
        super(GBKEncodeMapFunction, self).__init__("gbk")

class Base(SuperBase):
    '''
    父类必须继承超类object
    '''
    __metaclass__ = ABCMeta
    def __init__(self):
        super(Base, self).__init__()

    @abstractmethod
    def get_stream(self, stream):
        '''
        流逻辑，子类必须实现
        '''
        raise NotImplementedError  

    @abstractmethod
    def get_sink(self, sink):
        '''
        流逻辑，子类必须实现
        '''
        raise NotImplementedError  

    def main(self, job_name, env_parallelism, env, source, sinks):
        '''
        主运行函数，分析入口，*不可缺失
        '''
        #1：设置并发度等运行参数（TaskManager * TaskSlots = Max Parallelism）
        env.set_parallelism(env_parallelism)

        #env对象可以完成流式计算的功能。包括
        #2：接入逻辑流
        stream = env.create_python_source(source)
        stream = self.get_stream(stream)
        
        if sinks == None:
            stream.output()
        else:
            sink = sinks[0]
            sink.set_stream_args(mode=WriteMode.OVERWRITE)
            sink = self.get_sink(sink)
            sink.write_by_stream(stream)

            for sink in sinks[1:]:
                stream.add_sink(sink)
            
        #3：启动任务
        env.execute("Py-Module '{}'".format(job_name))
