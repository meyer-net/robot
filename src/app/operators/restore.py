# -- coding: UTF-8 

from operators import OperatorBase, GBKEncodeMapFunction

class Restore(OperatorBase):
    '''
    还原原始数据流到本地
    '''
    def __init__(self):
        super(Restore, self).__init__()
        
    def get_stream(self, stream):
        '''
        原封不动
        '''
        return stream.map(GBKEncodeMapFunction())

    def get_sink(self, sink):
        '''
        流逻辑，必须实现
        '''
        sink.set_format_args(["{}_{}".format(self.__module__, self.__class__.__name__)])
        return sink