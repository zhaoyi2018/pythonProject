import math
from datetime import datetime

import numpy as np
import pandas as pd

from db_operate.shared_lib.hive_helper import HiveHelper
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
                ["NULL" if check_dataframe_value_null(row[key], table_attr[key]) else format_dataframe_value(row[key],
                                                                                                             table_attr[
                                                                                                                 key])
                 for key in
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
    elif dtype in ['int', 'date', 'bigint']:
        return pd.isna(value)
    else:
        logger.info("未设置NULL的数据类型:", dtype)
        return True


def format_dataframe_value(value, dtype):
    """
    格式化df数据, 转为insert into可接受格式
    :param value: 数值
    :param dtype: 类型
    :return:
    """
    if dtype == 'string':
        return "'{}'".format(value.replace("'", "\\'"))
    elif dtype in ['float', 'double', 'int', 'bigint']:
        return f"{value}"
    else:
        logger.info("未设置格式化的数据类型:", dtype)
        return f"{value}"


def check_hive_adapt_types(types):
    """
    检测数据类型是否支持
    :param types: 数据类型
    :return:
    """
    supported = {'string', 'float', 'double', 'int', 'bigint'}
    diff_types = types-supported
    if len(diff_types) == 0:
        return True
    else:
        logger.error("异常存在不支持数据类型: " + diff_types)
        return False


def get_create_table_sql(table_name, attr_dict):
    """
    获取创建sql语句
    :param table_name: 表名
    :param attr_dict: 字段字典 { key: key_type...}
    :return:
    """
    attr_sql = ''
    for key, value in attr_dict.items():
        if attr_sql == '':
            attr_sql += f"`{key}` {value}"
        else:
            attr_sql += f", `{key}` {value}"
    sql = f"CREATE TABLE IF NOT EXISTS `{table_name}` (" \
          f"{attr_sql}" \
          f");"
    return sql


def get_insert_sql(table_name, attr_dict, datas, max_nums=10000, need_type='str'):
    """
    获取插入语句
    :param table_name: 表名
    :param attr_dict: 字段字典
    :param datas: dataframe的数据
    :param max_nums: 最大插入行数
    :param need_type: 返回sqls格式类型（字符串，列表）
    :return:
    """
    # 0. 校验
    if need_type == 'str':
        result = ''
    else:
        result = []

    if datas.empty:
        logger.info("  the data is empty!")
        return result

    # 1. 修正数据格式
    datas_dtype_dict = datas.dtypes.to_dict()
    # 1.1. 首先判断表和df的相同字段数据类型是否相同
    for attr_name, table_attr_type in attr_dict.items():
        df_attr_dtype = datas_dtype_dict.get(attr_name)

        # 1.1.1 同则跳过
        if table_attr_type == 'string' and df_attr_dtype == 'object':
            continue
        elif table_attr_type in ['int', 'bool', 'float', 'double'] and table_attr_type == df_attr_dtype:
            continue
        # 1.1.2 异则修正， 由df现有类型->表指定类型。正常来说，从数据库读出来的数据一般不会发生太大的变异
        elif table_attr_type in ['int', 'bigint'] and df_attr_dtype == 'float':
            # 目前只见到因为np.nan将int转为float情况
            datas[attr_name] = datas[attr_name].apply(lambda x: pd.NA if math.isnan(x) else int(x))
        else:
            logger.info("未知变化，原始数据类型:", table_attr_type, ", 新数据类型:", df_attr_dtype)
            return None

    # 2. 准备sql语句
    sql = 'INSERT INTO `{}`({}) ' \
          'VALUES {};'
    temp_columns = attr_dict.keys()
    temp_attr = ", ".join([f'`{key}`' for key in temp_columns])

    all_data = []

    # 3. 简单处理datas内容
    datas = datas.where(datas.notnull(), None)
    # 开始插入
    j = 0
    for i, row in datas.iterrows():
        j += 1
        temp_data = ', '.join(
            ["NULL" if check_dataframe_value_null(row[key], attr_dict[key]) else format_dataframe_value(row[key],
                                                                                                        attr_dict[key])
             for key in
             temp_columns])
        all_data.append(f"({temp_data})")
        # 若插入数据行数过多，则提前插入
        if j > max_nums:
            logger.info(f'origin_nums: {datas.shape[0]},have saved nums :{i}')
            j = 0
            sql_insert = sql.format(table_name, temp_attr, ', \n'.join(all_data))
            if need_type == 'str':
                result += sql_insert
            else:
                result.append(sql_insert)
            all_data = list()
    if j > 0:
        sql_insert = sql.format(table_name, temp_attr, ', \n'.join(all_data))
        if need_type == 'str':
            result += sql_insert
        else:
            result.append(sql_insert)
        del all_data
        logger.info('  prepare the data success')
    return result


def describe_table(db_helper, table_name):
    """
    获取表结构
    :param db_helper:
    :param table_name:
    :return:
    """
    describe_sql = f"DESCRIBE {table_name};"
    result = pd.DataFrame(db_helper.queryAll(describe_sql), columns=['column_name', 'column_type', 'column_describe'])
    result.insert(0, 'table_name', table_name)
    return result


def insert_tables_to_hive_db(from_db, to_db, tables):
    """
    适用于hive到hive库的表移动（测试版）
    :param from_db 来源数据库
    :param to_db 目标数据库
    :param tables 指定表名(列表类型)
    :return:
    """
    if tables is None:
        return
    result = pd.DataFrame(columns=['table_name', 'column_name', 'column_type', 'column_describe'])
    #  获取表结构
    for table_name in set(tables):
        table_struct = describe_table(from_db, table_name)
        result = result.append(table_struct)

    #  预览数据类型种类
    column_types = set(result['column_type'])
    if not check_hive_adapt_types(column_types):
        return

    #  数据转移
    grouped = result.groupby(by='table_name')
    error_tables = []
    logger.info('共{}表, 需要处理, 开始:'.format(len(grouped)))
    for index, (group_label, group_data) in enumerate(grouped):
        logger.info('  第{}个,表名{}, 开始处理'.format(index + 1, group_label))
        attr_dict = group_data[['column_name', 'column_type']].set_index('column_name')['column_type'].to_dict()
        create_sql = get_create_table_sql(group_label, attr_dict)
        datas = from_db.pd_read_sql(f'SELECT * FROM {group_label};')
        insert_sqls = get_insert_sql(group_label, attr_dict, datas, need_type='list')
        if insert_sqls is None:
            error_tables.append(group_label)
            continue
        to_db.createTable(create_sql)
        logger.info('  第{}个,表名{}, 创建成功'.format(index + 1, group_label))
        for insert_sql in insert_sqls:
            to_db.insert(insert_sql)
        logger.info('  第{}个,表名{}, 数据插入成功'.format(index + 1, group_label))
    logger.info("导出失败表:" + str(error_tables))
    logger.info("结束转移")


def backup_db_to_sql(db_helper, file_path, tables=None):
    """
    备份hive数据库到指定sql文件
    :param db_helper: 数据库连接工具类
    :param file_path: sql文件保存路径
    :param tables: 指定表名(列表类型)
    :return:
    """
    # 检验参数
    if db_helper is None or file_path is None:
        logger.error("传入参数为None")
        return
    if not isinstance(db_helper, HiveHelper) or not isinstance(file_path, str):
        logger.error("传入参数类型异常")
        return
    if not file_path.endswith('.sql') or not len(file_path) >= 4:
        logger.error("文件路径异常")
        return
    if db_helper.showDatabases() is None:
        logger.error("数据库连接异常")
        return

    # 开始备份
    logger.info("开始备份")
    all_tables = pd.DataFrame(db_helper.showTables(), columns=["table_name"])
    if tables is not None:
        all_tables = pd.DataFrame({"table_name": tables}, columns=["table_name"])
    result = pd.DataFrame(columns=['table_name', 'column_name', 'column_type', 'column_describe'])
    #  获取表结构
    tables_num = len(set(all_tables['table_name']))
    for index, table_name in enumerate(set(all_tables['table_name'])):
        logger.info("获取表结构-共有{}表, 进行到第{}表:{}".format(tables_num, index + 1, table_name))
        table_struct = describe_table(db_helper, table_name)
        result = result.append(table_struct)
    #  数据类型种类检测
    column_types = set(result['column_type'])
    if not check_hive_adapt_types(column_types):
        return
    #  生成sql文件
    grouped = result.groupby(by='table_name')
    error_tables = []
    for index, (group_label, group_data) in enumerate(grouped):
        logger.info('生成sql文件-共有{}表, 处理第{}个,表名{}, 开始处理'.format(tables_num, index + 1, group_label))
        attr_dict = group_data[['column_name', 'column_type']].set_index('column_name')['column_type'].to_dict()
        create_sql = get_create_table_sql(group_label, attr_dict)
        datas = db_helper.pd_read_sql(f'SELECT * FROM {group_label};')
        insert_sql = get_insert_sql(group_label, attr_dict, datas)
        if insert_sql is None:
            error_tables.append(group_label)
            continue
        with open(file_path, 'w') as f:
            f.write(create_sql)
            f.write('\n\n')
            f.write(insert_sql)
            f.write('\n\n')

    # 结束备份
    logger.info("导出失败表:" + str(error_tables))
    logger.info("结束备份")
