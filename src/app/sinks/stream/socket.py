# -- coding: UTF-8 

import utils
from sinks import SinkBase

class Socket(SinkBase):
    '''初始化构造函数'''
    def __init__(self, conf):
        super(Socket, self).__init__(conf)

    def write_by_stream(self, data_stream, **kvs):
        '''
        该函数指示将指定数据流写入至目标处
        '''
        args = self._args
        host = args["host"]
        port = utils.gen_free_port(args["port"])
        
        data_stream.write_to_socket(host, port, self._kvs["schema"])
