import math
from datetime import datetime

import numpy as np
import pandas as pd

from db_operate.shared_lib.logger import Logger

logger = Logger(__name__)


def fast_save_to_db(db_helper, table_name, table_attr, result, config, drop=True, must_attr=True):
    """
    将指定数据，存入数据库的指定表名内
    :param db_helper:
    :param table_name: sql表名
    :param table_attr: 字典{sql列名：sql类型,,,}
    :param result: dataframe类型数据
    :param config: 配置文件
    :param drop: 是否删除表后，重建表结构
    :param must_attr: 必带属性，是否需要
    :return:
    """
    if must_attr:
        # 添加必带属性
        table_attr["orgid"] = "string"
        table_attr["orgname"] = "string"
        table_attr["insert_time"] = "string"
    # 获取sql列名语句
    temp_attr = ", ".join([f"{key} {value}" for key, value in table_attr.items()])
    temp_columns = table_attr.keys()

    # 判断表是否存在
    if not db_helper.table_exists(table_name):
        sql_create = f"CREATE TABLE  IF NOT EXISTS {table_name}({temp_attr});"
        db_helper.createTable(sql_create)
    else:
        if drop:
            db_helper.dropTable(table_name)
            sql_create = f"CREATE TABLE  IF NOT EXISTS {table_name}({temp_attr});"
            db_helper.createTable(sql_create)
        else:
            db_helper.truncateTable(table_name)

    # 准备插入数据
    all_data = []
    if not result.empty:
        # 简单处理result内容
        result = result.where(result.notnull(), None)
        if must_attr:
            # 必带属性-添加
            result["orgid"] = config["orgid"]
            result["orgname"] = config["orgname"]
            result["insert_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 开始插入
        j = 0
        for i, row in result.iterrows():
            j += 1
            temp_data = ', '.join(
                ["NULL" if check_dataframe_value_null(row[key], table_attr[key]) else format_dataframe_value(row[key], table_attr[key]) for key in
                 temp_columns])
            all_data.append(f"({temp_data})")
            # 若插入数据行数过多，则提前插入
            if j > config["max_insert_rows"]:
                logger.info(f'origin_nums: {result.shape[0]},have saved nums :{i}')
                j = 0
                sql_insert = f"insert into {table_name}({', '.join([key for key in temp_columns])}) " \
                             f"values {', '.join(all_data)};"
                db_helper.insert(sql_insert)
                all_data = list()
        if j > 0:
            sql_insert = f"insert into {table_name}({', '.join([key for key in temp_columns])}) " \
                         f"values {', '.join(all_data)};"
            db_helper.insert(sql_insert)
            del all_data
            logger.info('Save the data success')
    else:
        logger.info("the data is empty!")


def check_dataframe_value_null(value, dtype):
    """
    判断df中value是否为空值
    :param value: 数值
    :param dtype: 类型
    :return:
    """
    if dtype == 'string':
        return value is None
    elif dtype in ['float', 'double']:
        return value is None or math.isnan(value)
    elif dtype in ['int', 'date']:
        return pd.isna(value)
    else:
        logger.info("为设置NULL的数据类型:", dtype)
        return True


def format_dataframe_value(value, dtype):
    """
    格式化df数据, 转为insert into可接受格式
    :param value:
    :param dtype:
    :return:
    """
    if dtype == 'string':
        return f"'{value}'"
    elif dtype in ['float', 'double', 'int']:
        return f"{value}"
    else:
        logger.info("未设置格式化的数据类型:", dtype)
        return f"{value}"