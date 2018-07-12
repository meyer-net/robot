# -- coding: UTF-8 
# https://blog.csdn.net/gamer_gyt/article/details/52446757
# import smart_open
# http://pyhdfs.readthedocs.io/en/latest/pyhdfs.html#pyhdfs.HdfsClient.open

from sources.io import SourceIOBase
from drivers import HdfsDriver
from contextlib import closing

class Hdfs(SourceIOBase):
    '''初始化构造函数'''
    def __init__(self, conf):
        super(Hdfs, self).__init__(conf)

    def set_position(self, handler, position):
        self.logger.debug("set position {}".format(str(position)))
        args = {
            "path": self.get_position_path(),
            "data": str(position),
            "overwrite": True
        }

        handler.create(**args)
        
    def get_position(self, handler):
        position = 0
        position_path = self.get_position_path()

        try:
            with closing(handler.open(position_path)) as resp:
                position = long(resp.read())
        except HdfsDriver.HdfsFileNotFoundException as err:
            self.set_position(handler, position)
        except Exception as err:
            self.logger.error("Read position from file '{}' error -> {}".format(position_path, err))

        return position

    def get_handler(self):
        args = self._args 
        return HdfsDriver.HdfsClient(hosts='{host}:{rport}'.format(**args), user_name='pyflink')

    def mount(self, handler, ctx):
        '''
        该函数指示将指定数据流写入至目标处
        '''
        args = self._args
        read_file = args["formated"]
        ref = args["ref"]
        
        # HDFS库
        # client = Client("http://{host}:{port}".format(**args), root=None, proxy=None, timeout=None, session=None) 
        # with client.read(filename, encoding='utf-8', delimiter='\n') as reader:
        #     for line in reader:
        #         print(line.strip())
        offset = self.get_position(handler)
        
        #93412555
        try:
            with closing(handler.open('{path}/{formated}'.format(**args), offset=offset)) as resp:
                lines = resp.read().split('\n')
                
                # 多余的一行是换行符，固然 -1
                lines_len = len(lines) - 1
                for index in range(lines_len):
                    line = lines[index]                        # 依次读取每行  
                    line_strip = line.strip()
                    ctx.collect(line_strip)                    # 去掉每行头尾空白  
                    offset += len(line+'\n')
                        
                    self.logger.debug("Ref operator of '{}'(Reading io '{}/{}' from file '{}', offset='{}')".format(ref, index+1, lines_len, read_file, offset))
                                
        except HdfsDriver.HdfsIOException as err:  
            self.logger.info("Ref operator of '{}' raise err({}), read break".format(ref, err, read_file))
            return

        except Exception as err:  
            self.logger.error("Ref operator of '{}' raise err({}) from file '{}', read break".format(ref, err, read_file))
        
        return offset
