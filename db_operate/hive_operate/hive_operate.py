import math

import pandas as pd

from db_operate.shared_lib.get_config import *
from db_operate.shared_lib.hive_helper import HiveHelper
from db_operate.shared_lib.logger import Logger
from db_operate.shared_lib.tools import *

CONFIG = get_config(file=os.path.join(os.path.dirname(__file__), 'config.json'))
logger = Logger(__name__)


def get_all_tables(db_helper):
    """
    获取数据库内所有表名
    :param db_helper:
    :return:
    """
    sql = f"SHOW TABLES;"
    result = pd.DataFrame(db_helper.queryAll(sql), columns=['table_name'])
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


    # 2. 准备sql语句
    if need_type == 'str':
        result = ''
    else:
        result = []
    sql = 'INSERT INTO `{}`({}) ' \
          'VALUES {};'
    temp_columns = attr_dict.keys()
    temp_attr = ", ".join([f'`{key}`' for key in temp_columns])

    all_data = []
    if not datas.empty:
        # 简单处理datas内容
        datas = datas.where(datas.notnull(), None)
        # 开始插入
        j = 0
        for i, row in datas.iterrows():
            j += 1
            temp_data = ', '.join(
                ["NULL" if check_dataframe_value_null(row[key], attr_dict[key]) else format_dataframe_value(row[key], attr_dict[key]) for key in
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
    else:
        logger.info("  the data is empty!")
    return result


def demo1():
    """
    读取csv文件中的table表名
    :return:
    """
    logger.info("hive数据库操作")
    hive_helper = HiveHelper()

    # 读取excel文件
    data = pd.read_excel("./data/宁波-数据库表.xlsx", engine='openpyxl', skiprows=1)  # 导入excel表中的数据

    result = pd.DataFrame(columns=['table_name', 'column_name', 'column_type', 'column_describe'])

    # 获取表结构
    for table_name in set(data['表名']):
        table_struct = describe_table(hive_helper, table_name)
        result = result.append(table_struct)

    # 重新排序索引
    result = result.sort_index()

    # 预览数据类型种类
    column_types = set(result['column_type'])
    print(column_types)

    # 分组
    grouped = result.groupby(by='table_name')
    for group_label, group_data in grouped:
        attr_dict = group_data[['column_name', 'column_type']].set_index('column_name')['column_type'].to_dict()
        create_sql = get_create_table_sql(group_label, attr_dict)
        datas = hive_helper.pd_read_sql(f'SELECT * FROM {group_label};')
        insert_sql = get_insert_sql(group_label, attr_dict, datas)
        with open('./data/宁波-v2.sql', 'a') as f:
            f.write(create_sql)
            f.write('\n\n')
            f.write(insert_sql)
            f.write('\n\n')

    hive_helper.close()


if __name__ == '__main__':
    logger.info("hive数据库操作")
    # hive_helper = HiveHelper()
    out_hive_helper = HiveHelper(section="hive-sadan")
    in_hive_helper = HiveHelper(section="hive-fengqing_leaderwarehouse")

    # out_all_tables = get_all_tables(out_hive_helper)
    # in_all_tables = get_all_tables(in_hive_helper)
    #
    # # 筛选
    # out_all_tables = out_all_tables[out_all_tables["table_name"].apply(lambda x: x.startswith("rlt_"))]
    # # 获取重合表
    # common_elements = pd.Series(pd.np.intersect1d(out_all_tables["table_name"], in_all_tables["table_name"]))

    result = pd.DataFrame(columns=['table_name', 'column_name', 'column_type', 'column_describe'])
    out_all_tables = ['base_org_bak']
    # 获取表结构
    for table_name in set(out_all_tables):
        table_struct = describe_table(out_hive_helper, table_name)
        result = result.append(table_struct)

    # 预览数据类型种类
    column_types = set(result['column_type'])
    print(column_types)

    # 分组
    grouped = result.groupby(by='table_name')
    logger.info('共{}表, 需要处理, 开始:'.format(len(grouped)))
    for index, (group_label, group_data) in enumerate(grouped):
        logger.info('  第{}个,表名{}, 开始处理'.format(index+1, group_label))
        attr_dict = group_data[['column_name', 'column_type']].set_index('column_name')['column_type'].to_dict()
        create_sql = get_create_table_sql(group_label, attr_dict)
        datas = out_hive_helper.pd_read_sql(f'SELECT * FROM {group_label};')
        insert_sqls = get_insert_sql(group_label, attr_dict, datas, need_type='list')
        in_hive_helper.createTable(create_sql)
        logger.info('  第{}个,表名{}, 创建成功'.format(index + 1, group_label))
        for insert_sql in insert_sqls:
            in_hive_helper.insert(insert_sql)
        logger.info('  第{}个,表名{}, 数据插入成功'.format(index + 1, group_label))

    out_hive_helper.close()
    in_hive_helper.close()
