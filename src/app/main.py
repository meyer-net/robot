# -- coding: UTF-8 

# API文档：https://ci.apache.org/projects/flink/flink-docs-release-1.5/dev/stream/python.html#data-sinks

import sys
import os
import time
import json
import argparse

from common import SuperBase
from utils import String, Printer

from org.apache.flink.streaming.api.functions.source import SourceFunction
from org.apache.flink.streaming.api.functions.sink import DiscardingSink

# '''
# 判断派生关系
# '''
# def is_sub_class_of(obj, cls):
#     try:
#         for i in obj.__bases__:
#             if i is cls or isinstance(i, cls):
#                 return True

#         for i in obj.__bases__:
#             if is_sub_class_of(i, cls):
#                 return True

#     except AttributeError:
#         return is_sub_class_of(obj.__class__, cls)

#     return False


'''
动态导入类
'''
def import_class(module_base_name, script_name):
    """
    导入指定模块的脚本，并返回
    # from sys import stdin
    # sys = __import__('sys', fromlist = ['stdin'])
    :return: 所需模块
    """
    module_levels = script_name.split(".")
    
    file_module_name = module_levels[-1]
    class_name = String().class_name_normalize(file_module_name)
    fromlist = [class_name]
    
    module = __import__("{}.{}".format(module_base_name, script_name), fromlist = fromlist)
    
    script_module = getattr(module, class_name)

    # 如果不是模块，直接返回
    if script_module.__class__.__name__ != "module":
        return script_module
        
    script_class = getattr(script_module, class_name)
    
    return script_class

'''
数据源
'''
class Generator(SourceFunction, SuperBase):
    def __init__(self, operator_name, data_source):
        self._running = True
        self._operator_name = operator_name
        self._data_source = data_source

    def get_data_source(self):
        return self._data_source

    def run(self, ctx):
        try:
            # 还原上次挂起
            data_source = self.get_data_source()
            data_source_handler = data_source.get_handler()
            restore_ok = data_source.restore_hung_up(data_source_handler, ctx)
            if restore_ok:
                self.logger.info("Restore source from '{}' OK".format(restore_ok))

            # 自动数秒
            wait_seconds_default = 1
            wait_seconds = wait_seconds_default
            while self._running:
                position = data_source.mount(data_source_handler, ctx)
                if position != None:
                    wait_seconds = wait_seconds_default
                    data_source.set_position(data_source_handler, position)
                else:
                    self.logger.info("Module '{}' Ends by current mount, worker will delay for '{}s'".format(self._operator_name, wait_seconds))
                    time.sleep(wait_seconds)
                    wait_seconds = wait_seconds * 2

        except Exception as err:  
            self.logger.error("Generator raise error: '{}', job exited".format(err))
        finally:
            self.logger.info("Job finished")

    def cancel(self):
        self._running = False

'''
标记处理Sink
??? 试图在此解决数据position mark的问题，从而精确调用原source中的set_position
此处并未找到合适重写java接口的方法，需要在编译时，重新新增一个实现了SinkFunction接口的抽象类
'''
class MarkProcess(DiscardingSink, SuperBase):
    def __init__(self, source):
        self._source = source

        # setattr(self.__class__, "invoke", self._invoke)
        # self.invoke = self._invoke
        
    def _invoke(self, value, context):
        print("--------------- invoke it")
        
'''
所有操作器执行的入口
'''
class OperatorEntry(SuperBase):
    logger = Printer()

    '''初始化构造函数'''
    def __init__(self, name):
        pass

    """
    用于启动子类算子
    接收参数：
    参数1：环境根目录
    参数2：模块
    参数3：执行脚本
    参数4：队列文件
    """
    def run_main(self, factory, args):
        # 创建算子
        operator = import_class(args.module, args.script)()
        
        # 创建执行环境
        env = factory.get_execution_environment()

        # 创建数据源抓取对象
        settings_conf = json.loads(args.settings)
        boot_conf = settings_conf["boot_conf"]

        # 合并 boot_conf 内容
        boot_name = boot_conf.get("name", None)
        source_key = boot_conf.get("source_key")
        env_parallelism = boot_conf.get("parallelism")

        # 主要用于像sink为socket时，对应的source为socket且并未优先启动的情况。
        # 端口没有提前开启写入，则会报错。泛指调整启动优先级的情况。
        if "boot_delay" in boot_conf:
            boot_delay = int(boot_conf.get("boot_delay"))
            self.logger.warning("Operator of '{}' delay for {} seconds".format(operator.__module__, boot_delay))
            time.sleep(boot_delay)
        
        # 依据环境变化计算出来的配置
        dynamic_conf = {
            "source_key": source_key,
            "ref": operator.__module__
        }

        # 内部函数
        def load_flow_class(load_type):
            load_type_name = boot_conf.get("{}_type".format(load_type))
            load_type_driver_name = boot_conf.get("{}_driver".format(load_type))
            load_type_conf_name = boot_conf.get("{}_conf".format(load_type))
            load_type_conf = settings_conf.get(load_type_conf_name)

            if load_type_conf == None:
                raise Exception("Cannot find section of '{}' from the settings.conf case when load the type of '{}'".format(load_type_conf_name, load_type))

            load_type_conf = dict(dynamic_conf, **load_type_conf)
            instance = import_class("{}s".format(load_type), "{}.{}".format(load_type_name, load_type_driver_name))(load_type_conf)
            self.logger.info("Operator [{}] -> [{}] = '{}' & [config] = '{}'".format(operator.__module__, load_type, instance.__module__, load_type_conf))
            return instance

        # 创建数据源适配
        data_source = load_flow_class("source")
        data_source.set_format_args(source_key)
        
        # 将动态部分依据KEY提前格式化
        # 注意：同一个模块运算会出现相同运算的SINK，这时候就得显示什么sink_key
        sink = load_flow_class("sink")
        sink.set_format_args(boot_conf.get("sink_key", "{}_{}".format(
            operator.__module__, operator.__class__.__name__)))


        # 数据源包裹器
        data_generator = Generator(operator.__module__, data_source)

        # 创建输出适配
        data_sinks = [sink, MarkProcess(data_source)]

        # 打印日志
        self.logger.info("Worker running local at '{}'".format(str(os.path.dirname(os.path.abspath(__file__)))))
        self.logger.info("Worker commited to job '{}' by '{}'".format(boot_name, operator.__module__))

        # 动态运行算子
        operator.main(boot_name, env_parallelism,
                      env, data_generator, data_sinks)

'''
Flink 主运行函数
'''
def main(factory):
    charset = "utf-8"
    if sys.getdefaultencoding() != charset:
        reload(sys)
        sys.setdefaultencoding(charset)

    parser = argparse.ArgumentParser(description='OSTeam PyFlink-Framework.')
    parser.add_argument('--settings', metavar='IN', help='json config')
    parser.add_argument('--env_root', metavar='IN', help='env path')
    parser.add_argument('--module', metavar='IN', help='module path')
    parser.add_argument('--script', metavar='IN', help='script file path')
    
    args = parser.parse_args()

    # 操作器驱动入口
    OperatorEntry(args.script).run_main(factory, args)
