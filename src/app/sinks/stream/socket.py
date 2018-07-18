# -- coding: UTF-8 

import time
import utils

from sinks import SinkBase
from drivers import SocketDriver

class Socket(SinkBase):
    '''初始化构造函数'''
    def __init__(self, conf):
        super(Socket, self).__init__(conf)

    def write_by_stream(self, data_stream, **kvs):
        '''
        该函数指示将指定数据流写入至目标处
        '''
        args = self._args
        host = str(args["host"])
        port = int(utils.gen_free_port(args["port"]))

        socket = SocketDriver.socket(
            SocketDriver.AF_INET, SocketDriver.SOCK_STREAM)

        # 等待时间
        wait_secs = 5

        while True:
            try:
                self.logger.info("Attempting to connect to '{}:{}'".format(host, port))
                socket.connect((host, port))
                socket.close()
                self.logger.info(
                    "Socket connect to '{}:{}' success".format(host, port))
                break
            except SocketDriver.error, e:
                self.logger.error(
                    "Socket connect to '{}:{}' failed, wait for {}s then retry".format(host, port, wait_secs))
                time.sleep(wait_secs)
        
        data_stream.write_to_socket(host, port, self._kvs["schema"])
