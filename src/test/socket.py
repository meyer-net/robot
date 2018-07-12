# -- coding: UTF-8

import os
import socket
import threading
import time


class SocketStringReader(threading.Thread):
    def __init__(self, host, port, expected_num_values):
        threading.Thread.__init__(self)
        self._host = host
        self._port = port
        self._expected_num_values = expected_num_values

    def run(self):
        serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((self._host, self._port))
        serversocket.listen(5)
        (clientsocket, address) = serversocket.accept()

        try:
            all_data = []
            while True:
                data = clientsocket.recv(1024)
                if not data:
                    break

                all_data.append(data)
                print(bytes.decode(data))
                # for v in msg.split('|')[:-1]:
                #     print(v)

                #     try:
                #         file.seek(0)
                #         file.write(v)
                #         file.flush()
                #     except Exception as err:
                #         print(err)
        except Exception as err:
            print(err)

        print("*** Done receiving ***")
        clientsocket.close()
        serversocket.close()

if __name__ == '__main__':
        SocketStringReader('127.0.0.1', 54321, 100).start()
