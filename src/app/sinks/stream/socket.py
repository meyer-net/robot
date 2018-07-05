# -- coding: UTF-8 

from sinks import SinkBase

class Socket(SinkBase):
    '''初始化构造函数'''
    def __init__(self, conf):
        super(Socket, self).__init__(conf)

    def write_by_stream(self, data_stream):
        '''
        该函数指示将指定数据流写入至目标处
        '''
        data_stream.write_to_socket(self._conf["host"], self._conf["port"])