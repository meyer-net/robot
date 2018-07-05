# -- coding: UTF-8

import time
import os
import shutil

from sinks import SinkBase

from org.apache.flink.core.fs.FileSystem import WriteMode

class File(SinkBase):
    '''初始化构造函数'''
    def __init__(self, conf):
        super(File, self).__init__(conf)

    def write_by_stream(self, data_stream):
        '''
        该函数指示将指定数据流写入至目标处
        '''
        # 文件备份，因为每次进程起来，文件都会被重新写入
        file_path = "{}/{}".format(self._conf["path"], self.get_format_val())

        if os.path.exists(file_path):
            bak_path = "{}.{}".format(file_path, int(round(time.time() * 1000)))
            shutil.move(file_path, bak_path)

        data_stream.write_as_text("file://{}".format(file_path), WriteMode.OVERWRITE)