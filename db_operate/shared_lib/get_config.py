import configparser
import json
import os

#
cur_path = os.path.dirname(os.path.realpath(__file__))

conf = configparser.ConfigParser()

def getMysqlConfig(section):
    config = configparser.ConfigParser()
    config_path = os.path.join(cur_path, 'conf.ini')
    config.read(config_path)
    for kv in config['mysql']:
        print(kv)
    con = {}
    # for item in conf.items(section):
    #     print(item)
    #     con[item[0]] = item[1]
    con['host'] = config.get(section, 'host')
    con['port'] = int(config.get(section, 'port'))
    con['user'] = config.get(section, 'user')
    con['password'] = config.get(section, 'password')
    con['database'] = config.get(section, 'database')
    con['charset'] = config.get(section, 'charset')

    return con
    # return conf.get(section, key)


def getHiveConfig(section):
    config = configparser.ConfigParser()
    config_path = os.path.join(cur_path, 'conf.ini')
    config.read(config_path)
    con = {}
    # for item in conf.items(section):
    #     print(item)
    #     con[item[0]] = item[1]
    con['host'] = config.get(section, 'host')
    con['port'] = int(config.get(section, 'port'))
    con['user'] = config.get(section, 'user')
    con['password'] = config.get(section, 'password')
    con['database'] = config.get(section, 'database')
    con['auth_mechanism'] = config.get(section, 'auth_mechanism')
    return con

def getConfig(section):
    if section=='mysql':
        return getMysqlConfig(section)
    elif section =='hive':
        return getHiveConfig(section)


def get_config(file="config.json", section=None):
    with open(file,encoding='UTF-8') as json_file:
        config = json.load(json_file,encoding='UTF-8')
    if section is None:
        return config
    else:
        return config[section]
