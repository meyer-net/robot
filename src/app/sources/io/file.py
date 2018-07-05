# -- coding: UTF-8 

import os

from sources.io import SourceIOBase

class File(SourceIOBase):
    '''初始化构造函数'''
    def __init__(self, conf):
        super(File, self).__init__(conf)

    def set_position(self, handler, position):
        with closing(open(self.get_position_path(), "w+")) as write_open:
            try:
                write_open.seek(0)
                write_open.truncate()
                write_open.write(str(position))
                write_open.flush()
            except Exception as err:
                self.logger.error("Record position to file '{}' error -> {}".format(self.get_position_path(), err))
        
    def get_position(self, handler):
        position = 0
        with closing(open(self.get_position_path(), "r")) as read_open:
            try:
                read_open.seek(0)
                line_text = read_open.readline().strip()
                position = int(line_text or 0)
            except IOError as err:
                self.set_position(0)
            except Exception as err:
                self.logger.error("Read position from file '{}' error -> {}".format(self.get_position_path(), err))

        return position
        
    def restore_hung_up(self, handler, ctx):
        pass

    def mount(self, handler, ctx):
        '''
        该函数指示将指定数据流写入至目标处
        '''
        # 获取配置信息
        read_name = self._conf["key"]
        path = self._conf["path"]
        ref = self._conf["ref"]
        
        # 读路径
        read_file = self._conf["format"].format(read_name)
        read_path = "{}/{}".format(path, read_file)
        if not os.access(read_path, os.F_OK):
            return

        # 获取最后读取的位置
        line_index = self.get_position(handler)

        # 打开文件
        with closing(open(read_path, "r")) as read_open:
            try:
                lines = read_open.readlines()
                lines_len = len(lines)
                if line_index >= lines_len:
                    self.logger.info("Ref operator of '{}' raise err(line index {} greater than total line {} from file '{}'), read break".format(ref, line_index, lines_len, read_file))
                    return

                self.logger.debug("Ref operator of '{}'(Read start {}/{} from file '{}')".format(ref, line_index, lines_len, read_file))
                for line in lines[line_index:]:                     # 依次读取每行  
                    line = line.strip()                             # 去掉每行头尾空白  
                    ctx.collect(line)
                    line_index += 1
                    self.logger.debug("Ref operator of '{}'(Reading file {}/{} from file '{}')".format(ref, line_index, lines_len, read_file))

            except Exception as err:  
                self.logger.error("Ref operator of '{}' raise err({}) from file '{}', read break".format(ref, err, read_file))

        self.logger.info("Ref operator of '{}'(Read over from file '{}')".format(ref, read_file))
        
        return line_index
        # ctx.collect(element)
        # ctx.read_text("file://{}/{}".format(self._conf["path"], self.get_format_val()), WriteMode.OVERWRITE)