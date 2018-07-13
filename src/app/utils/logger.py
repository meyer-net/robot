# -- coding: UTF-8

import os

#http://logbook.readthedocs.io/en/stable/api/index.html
import logbook
from logbook import Logger as LoggerDriver, TimedRotatingFileHandler
from logbook.more import ColorizedStderrHandler

from runtime import LOGGER_CONF

class Printer(object):
    def __init__(self):
        super(Printer, self).__init__()
    
    def empty(self, msg):
        print("{}".format(msg))
        
    def critical(self, msg):
        print("[CRITICAL]{}".format(msg))
    
    def error(self, msg):
        print("[ERROR]{}".format(msg))
        
    def info(self, msg):
        print("[INFO]{}".format(msg))
        
    def debug(self, msg):
        print("[DEBUG]{}".format(msg))
        
    def warning(self, msg):
        print("[WARNING]{}".format(msg))

class Logger(object):
    '''日志操作'''
    def __init__(self, log_name="default"):
        super(Logger, self).__init__()
        self._pid = os.getpid()
        self._ppid = os.getppid()

        self._loggers = {}
        self._logger_handlers = self.get_handlers(log_name)

    def get_logger(self, channel="default"):
        if channel in self._loggers:
            return self._loggers[channel]

        logger = LoggerDriver(channel)
        logger.handlers = self._logger_handlers
        self._loggers[channel] = logger

        return logger

    '''只能提取到外部去调用，不然定位不到写日志的地方'''
    def get_handlers(self, log_name):
        logger_dir = LOGGER_CONF["path"]
        logger_fmt = LOGGER_CONF["format"]
        # logger_size = int(LOGGER_CONF["size"])
        logger_level = LOGGER_CONF["level"].upper()

        if not os.path.exists(logger_dir):
            os.makedirs(logger_dir)

        def log_type(record, handler):
            log = logger_fmt.format(
                date = record.time,                              # 日志时间
                level = record.level_name,                       # 日志等级
                filename = os.path.split(record.filename)[-1],   # 文件名
                func_name = record.func_name,                    # 函数名
                lineno = record.lineno,                          # 行号
                msg = record.message,                            # 日志内容
                channel = record.channel,                        # 通道
                pid = self._pid,
                ppid = self._ppid
            )

            return log

        # 日志打印到屏幕
        log_std = ColorizedStderrHandler(bubble=True, level=logger_level)
        log_std.formatter = log_type

        # 日志打印到文件
        log_file = TimedRotatingFileHandler(os.path.join(logger_dir, '{}.log'.format(log_name)), date_format='%Y-%m-%d', rollover_format='{basename}_{timestamp}{ext}', bubble=True, level=logger_level, encoding='utf-8')
        log_file.formatter = log_type

        logbook.set_datetime_format("local")

        return [log_std, log_file]
