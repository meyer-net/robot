# -- coding: UTF-8 

import os
import sys
import json

from contextlib import closing

ENV_ROOT = str(os.path.dirname(os.path.abspath(__file__)))
APP_ROOT = "{}/app".format(ENV_ROOT)
sys.path.append(ENV_ROOT)

from utils import Printer, Config

logger = Printer()

'''
加载环境包
'''
def load_packages():
    # 只导入存在的包
    # for package in sys.path:
    #     if not os.path.exists(package):
    #         logger.warning("Package not found, then environment remove it '{}'".format(package))
    #         sys.path.remove(package)
    #     else:
    #         logger.info("Checking '{}'".format(package))
            
    # 如果是模块目录的话，需要进一步导入
    # ??? 避免导入多余包，参照package时的操作，做一次转换
    packages = [APP_ROOT]        
    def convert_then_fill_packages(package):
        ignore_module_list = ['configparser', 'beautifulsoup4']
        for (root, dirs, files) in os.walk(package, topdown=True):
            for folder in dirs:
                # 限制只加入根下的模块
                new_package = "{}/{}".format(root, folder)
                if folder != "__pycache__" and root == package and os.path.exists("{}/__init__.py".format(new_package)):
                    # 为EGG时限制只与包名匹配
                    parent = root.split('/')[-1]
                    is_egg = parent.split('.')[-1] == "egg"
                    module = folder
                    if is_egg:
                        module = parent.split('-')[0].lower()

                    # 有些模块不一定包名下包含的是一样的，例如 configparser 
                    if module == folder or (module in ignore_module_list):
                        packages.append(new_package)

    for package in PACKAGES:
        convert_then_fill_packages(package)
                
    # debug
    logger.empty('+--------------------------------------------------------------------------------------------------------+')
    for package in packages:
        logger.info("PyFlink.OSTeam of sandbox loaded package '{}'".format(package))
    logger.empty('+--------------------------------------------------------------------------------------------------------+')

    return " ".join(packages)
        
'''
通过FLINK自带的shell脚本提交计算程式
'''
def join_job(settings, boot_operator, packages):
    main_path = "{}{}main.py".format(APP_ROOT, os.sep)
    params = "--settings '{}' --env_root '{}' --module '{}' --script '{}'".format(settings, APP_ROOT, "operators", boot_operator)
    cmd = "nohup {} {} {} - {} &".format(PY_FLINK, main_path, packages, params)
    
    os.system(cmd)

'''
动态控制运行时部分变量
'''
def configure_runtime():
    runtime_file_path = "{}/runtime/environment.py".format(APP_ROOT)

    with closing(open(runtime_file_path, "w")) as write_open:
        write_open.write("# -- coding: UTF-8\n")
        write_open.write("ENV_ROOT = '{}'\n".format(ENV_ROOT))
        write_open.write("LOGGER_CONF = {}\n".format(
            json.dumps(settings_conf["logger"])))
        write_open.flush()

if __name__ == '__main__':
    PY_FLINK = sys.argv[1]
    PACKAGES = sys.argv[2]
    logger.empty("#############################################################")
    logger.info("RUNNING 'PYFLINK-FRAMEWORK.OSTEAM.BASE' BY OSTEAM.MEYER")
    logger.empty("#############################################################")
    #加载初级配置
    conf = Config(ENV_ROOT)
    settings_conf = conf.load_settings()

    #加载启动器信息
    boot_conf = conf.load_boot()
    
    # 配置runtime运行时数据
    configure_runtime()
    
    packages = load_packages()
    for opr_boot_conf in boot_conf:
        name = opr_boot_conf["name"].strip()
        module = opr_boot_conf["module"].strip()
        logger.info("CHECKING FOR OPERATOR-MODULE '{}'".format(module))
        settings_conf["boot_conf"] = opr_boot_conf
        settings_conf_json = json.dumps(settings_conf)
        join_job(settings_conf_json, module, packages)
        logger.info(
            "BOOTER '{}' USE MODULE '{}' ALREADY SUBMIT, AFTER A MOMENT WILL START".format(name, module))
        logger.empty('+--------------------------------------------------------------------------------------------------------+')

#类似 { python3 -m venv pyenv3 && source $PYENV3_DIR/bin/activate } 这种创建一个python3名为pyenv3的虚拟环境也可以完成该功能，但管理相对比较分散。
#启动命令：bin/sandbox src/boot.py '/usr/local/opt/flink/bin/pyflink-stream.sh'
