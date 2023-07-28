# -*- coding: utf-8 -*-
import os,sys

def get_global_config_path():
    #获取当前文件所在目录的绝对路径
    json_path = os.path.dirname(__file__)
    config_file = os.path.join(json_path, './config.json')
    return config_file



def get_curr_path():
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))



