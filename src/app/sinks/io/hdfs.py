# -- coding: UTF-8 

from sinks import SinkBase

class Hdfs(SinkBase):
    '''初始化构造函数'''
    def __init__(self, conf):
        super(Hdfs, self).__init__(conf)

    def write_by_stream(self, data_stream):
        '''
        该函数指示将指定数据流写入至目标处
        '''
        args = self._args
        hdfs_path = "hdfs://{host}:{wport}{path}/{formated}".format(**args)

        data_stream.write_as_text(hdfs_path, self._kvs["mode"])
