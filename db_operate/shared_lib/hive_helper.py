# -*- coding: utf-8 -*-
# @Time    : 1/17/21 7:32 PM
# @Author  : Bian Binbin
# @FileName: hive_helper.py


import sys
sys.path.append('.')

from impala.dbapi import connect
# import Config as Config
# from base_people_preprocess.preschoolers_analysis.conf.config import getConfig
# from conf.config import read_config
from db_operate.shared_lib.get_config import *
from db_operate.config.get_config_path import *

import pandas as pd
import traceback

from db_operate.shared_lib.logger import Logger
logger = Logger(__name__)


class HiveHelper(object):
    def __init__(self, file_path=None):
        if file_path is None:
            self.db_config = get_config(file=get_global_config_path(),section='hive')
        else:
            self.db_config = get_config(file=file_path, section='hive')
        self.init()

    def init(self):
        """
        init database connection
        :param dbconfig:
        :return: True/False
        """
        try:
            self.connection = connect(**self.db_config)
            # self.connection.autocommit(True)
            self.cursor = self.connection.cursor()
            logger.info(f"Connected to Hive database [ {self.db_config['database']} ]")
            return True
        except Exception as e:
            logger.error(f"Connect Hive exception : \n{str(e)}\n")
            return False


    def queryAll(self, sql):
        try:
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
            self.cursor.execute(sql, param)
            if size:
                rows = self.cursor.fetchmany(size)
            else:
                rows = self.cursor.fetchall()
        except Exception as e:
            self.connection.rollback()
            logger.error(traceback.format_exc())
            logger.error("[sql]:{} [param]:{}".format(sql, param))
        # finally:
        #     self.close()
        return rows

    def pd_read_sql(self, sql):
        try:
            data = pd.read_sql(sql, self.connection)
            return data
        except Exception as e:
            logger.error("Pandas read_sql error: " + str(e))
            return None
        # finally:
        #     self.close()



    def _operate(self, sql, params=None, DML=True):
        """
        exec DML: INSERT/UPDATE/DELETE
        exec DDL: CREATE TABLE/VIEW/INDEX/SYN/CLUSTER
        :param sql: dml sql
        :param param: string|list
        :return: Number of rows affected
        """
        count = 0
        try:
            count = self.cursor.execute(sql, params)
            self.commit()
        except Exception as e:
            if DML:
                self.rollback()
            logger.error("Operate error:" + str(e))
        # finally:
        #     self.close()
        return count

    def invalidate_metadata(self, tablename=None):
        # self.cursor.execute(f"invalidate metadata")
        self.cursor.execute(f"invalidate metadata {tablename}")

    def commit(self, ):
        self.connection.commit()

    def rollback(self, ):
        self.connection.rollback()

    def close(self):
    # def __del__(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None
            logger.info(f"Close Hive database [ {self.db_config['database']} ]")
        if self.connection:
            self.connection.close()
            self.connection = None

    def insert(self, sql):
        return self._operate(sql)

    def update(self, sql):
        return self._operate(sql)

    def delete(self, sql):
        return self._operate(sql)

    def createTable(self, sql):
        return self._operate(sql, DML=False)

    def dropTable(self, tablename):
        sql = f"DROP TABLE IF EXISTS {tablename}"
        self._operate(sql, DML=False)

    def truncateTable(self, tablename):
        sql = f"TRUNCATE TABLE IF EXISTS {tablename}"
        self._operate(sql, DML=False)

    def table_exists(self, tablename):
        return self.cursor.table_exists(tablename)


    def showTables(self):
        res = None
        try:
            self.cursor.execute('SHOW Tables')
            tables = self.cursor.fetchall()
            logger.info(f'SHOW Tables:')
            for t in tables:
                logger.info(f"     {t[0]}")
            return tables
        except Exception as e:
            logger.error("SHOW Tables error: " + str(e))
        # finally:
        #     self.close()

    def showDatabases(self):
        res = None
        try:
            self.cursor.execute('SHOW DATABASES')
            databases = self.cursor.fetchall()
            logger.info(f'SHOW DATABASES:')
            for db in databases:
                logger.info(f"     {db[0]}")
            return databases
        except Exception as e:
            logger.error("SHOW DATABASES error: " + str(e))
        # finally:
        #     self.close()

    def showCreateTable(self,tablename):
        try:
            self.cursor.execute(f'SHOW CREATE TABLE {tablename}')
            res = self.cursor.fetchall()
            logger.info(f'SHOW  CREATE TABLE [ {tablename} ]:')
            logger.info(f'     {res[0][0]}')
            return res
        except Exception as e:
            logger.error("SHOW CREATE TABLE error: " + str(e))
        # finally:
        #     self.close()


#
# h = HiveHelper(json_file='../config.json')
# h.pd_read_sql()