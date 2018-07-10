# -- coding: UTF-8

from sources import SourceBase
from drivers import SocketDriver

class Socket(SourceBase):
    '''初始化构造函数'''

    def __init__(self, conf):
        super(Socket, self).__init__(conf)

    def set_position(self, handler, position):
        pass

    def get_position(self, handler):
        pass

    def get_handler(self):
        server_socket = SocketDriver.socket(SocketDriver.AF_INET, SocketDriver.SOCK_STREAM)
        server_socket.bind((self._conf["host"], self._conf["port"]))
        server_socket.listen(5)
        (client_socket, address) = server_socket.accept()

        return client_socket

    def restore_hung_up(self, handler, ctx):
        pass

    def mount(self, handler, ctx):
        while True:
            data = handler.recv(1024)
            if not data:
                break

            element = bytes.decode(data)
            self.logger.debug("Collect element '{}'".format(element))
            ctx.collect(element)
