# -- coding: UTF-8 

import json
import backports.configparser

class Config(object):
    '''日志操作'''
    def __init__(self, env_root):
        super(Config, self).__init__()
        self._env_root = env_root

    '''
    加载配置文件
    '''
    def _load_from(self, conf_path):
        conf = backports.configparser.RawConfigParser()
        conf.read(conf_path)

        return conf
            
    '''
    加载文件
    '''
    def _load_file(self, file_path):
        with open(file_path) as file:
            content = file.read()
            file.close()
            return content

    '''
    将配置文件转换成对象
    '''
    def _conf_to_obj(self, conf):
        obj = {}
        for section in conf.sections():
            obj[section] = {}
            for key, value in conf.items(section):
                obj[section][key] = value
                
        return obj

    def load_settings(self):
        settings_conf = self._load_from("{}/conf/settings.conf".format(self._env_root))
        return self._conf_to_obj(settings_conf)

    def load_boot(self):
        boot_json = self._load_file("{}/conf/boot.json".format(self._env_root))
        return json.loads(boot_json)