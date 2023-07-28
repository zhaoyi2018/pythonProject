# -*- coding: utf-8 -*-
# @Time    : 1/17/21 7:32 PM
# @Author  : Bian Binbin
# @FileName: mysql_helper.py

# import os, sys
# current_dir = os.path.abspath(os.path.dirname(__file__))
# sys.path.append(current_dir)

import pymysql
# from business_environment.large_enterprises.conf.conf import read_config
# from conf.config import *
from db_operate.shared_lib.get_config import *
from db_operate.config.get_config_path import *
import pandas as pd
import traceback
from db_operate.shared_lib.logger import Logger
logger = Logger(__name__)


class MysqlHelper(object):
    def __init__(self,file_path=None,section='mysql'):

        if file_path is None:
            self.db_config = get_config(file=get_global_config_path(),section=section)
        else:
            self.db_config = get_config(file=file_path, section=section)
        self.init()

    def init(self):
        """
        init database connection
        :param dbconfig:
        :return: True/False
        """
        try:
            self.connection = pymysql.connect(**self.db_config)
            self.connection.autocommit(True)
            self.cursor = self.connection.cursor()
            logger.info(f"Connected to Mysql database [ {self.db_config['database']} ]")
            return True
        except Exception as e:
            logger.error(f"Connect Mysql exception : \n{str(e)}\n")
            return False

    def reConnect(self):
        try:
            self.connection.ping()
        except:
            self.connection()

    def close(self):
    # def __del__(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None
            logger.info(f"Close Mysql database [ {self.db_config['database']} ]")
        if self.connection:
            self.connection.close()
            self.connection = None

    def queryAll(self, sql):
        try:
            self.reConnect()
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            return res
        except Exception as e:
            logger.error("queryAll error: " + str(e))
            return None
        # finally:
        #     self.close()

    def queryMany(self, sql, n):
        try:
            self.reConnect()
            self.cursor.execute(sql)
            res = self.cursor.fetchmany(n)
            return res
        except Exception as e:
            logger.error("queryMany error: " + str(e))
            return None
        # finally:
        #     self.close()

    def queryOne(self, sql):
        try:
            self.reConnect()
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            return res
        except Exception as e:
            logger.error("queryOne error: " + str(e))
            return None
        # finally:
        #     self.close()

    def select(self, sql, param=None, size=None):
        """
        Query data
        :param sql:
        :param param:
        :param size: Number of rows of data you want to return
        :return:
        """
        rows = None
        try:
            self.reConnect()
            self.cursor.execute(sql, param)
            if size:
                rows = self.cursor.fetchmany(size)
            else:
                rows = self.cursor.fetchall()
        except Exception as e:
            self.connect.rollback()
            logger.error(traceback.format_exc())
            logger.error("[sql]:{} [param]:{}".format(sql, param))
        # finally:
        #     self.close()
        return rows
    def query_dataframe(self,query,param=None):
        '''
        :param query:your sql string
        :param kwargs:
        :return: multi rows with dataframe format
        '''
        self.select(query,param)
        table_keys = [keys[0] for keys in self.cursor.description]
        table_vales = [value for value in self.cursor]
        # table_keys, table_vales = self.raw_query(query=query,**kwargs)
        table_keys = [col.split(".")[1:][0] for col in table_keys]
        df = pd.DataFrame.from_records(data=table_vales,columns=table_keys)
        return df

    def pd_read_sql(self, sql):
        try:
            self.reConnect()
            data = pd.read_sql(sql, self.connection)
            return data
        except Exception as e:
            logger.error("pandas read_sql error: " + str(e))
            return None
        # finally:
        #     self.close()

    def showTables(self):
        res = None
        try:
            self.reConnect()
            self.cursor.execute('SHOW Tables')
            tables = self.cursor.fetchall()
            # logger.info(f'SHOW Tables:{tables}')
            return tables
        except Exception as e:
            logger.error("SHOW Tables error: " + str(e))
        # finally:
        #     self.close()

    def showDatabases(self):
        res = None
        try:
            self.reConnect()
            self.cursor.execute('SHOW DATABASES')
            databases = self.cursor.fetchall()
            logger.info(f'SHOW DATABASES:{databases}')
            return databases
        except Exception as e:
            logger.error("SHOW DATABASES error: " + str(e))
        # finally:
        #     self.close()

    def operate(self, sql, params=None, DML=True):
        """
        exec DML: INSERT/UPDATE/DELETE
        exec DDL: CREATE TABLE/VIEW/INDEX/SYN/CLUSTER
        :param sql: dml sql
        :param param: string|list
        :return: Number of rows affected
        """
        count = 0
        try:
            self.reConnect()
            count = self.cursor.execute(sql, params)
            self.connection.commit()
        except Exception as e:
            if DML:
                self.connection.rollback()
            logger.error("operate error:" + str(e))
        # finally:
        #     self.close()
        return count

    def insert(self, sql):
        return self.operate(sql)

    def update(self, sql):
        return self.operate(sql)

    def delete(self, sql):
        return self.operate(sql)

    def createTable(self, sql):
        return self.operate(sql, DML=False)

    def dropTable(self, tablename):
        sql = f"DROP TABLE IF EXISTS {tablename}"
        self.operate(sql, DML=False)

    def table_exists(self, tablename):
        tables = self.showTables()
        if (tablename, )  in tables:
            return True
        else:
            return False
        # sql = f"select * from information_schema.TABLES where TABLE_NAME = '{}'".format(tablename)
        # try:
        #     self.reConnect()
        #     self.cursor.execute('SHOW Tables')
        #     tables = self.cursor.fetchall()
        #     logger.info(f'SHOW Tables:{tables}')
        #     return tables
        # except Exception as e:
        #     logger.error("SHOW Tables error: " + str(e))