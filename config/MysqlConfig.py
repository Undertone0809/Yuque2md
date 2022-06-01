# -*- coding: utf-8 -*-
# @Time    : 2022/5/12 21:15
# @Author  : Zeeland
# @File    : MysqlConfig.py
# @Software: PyCharm
import MySQLdb
import pymysql
from dbutils.pooled_db import PooledDB

"""
@description: MysqlConfig,其他数据库对象可以继承该类用作model service,定制化CRUD,
              具体实现参考epi_province_service.py和epi_area_service.py
@param      : 可以引入pool线程池,也可不引入
"""
class MysqlConfig:
    def __init__(self,pool=None):
        self.conn = None
        self.cursor = None
        self.pool = pool

        self.host = 'localhost'
        self.user = 'root'
        self.password = 'xxx'
        self.db = 'xxx'
        self.port = 3306

        self.get_db_conn()

    def get_db_conn(self):
        try:
            if self.pool is not None:
                self.conn = self.pool.connection()
                print('[info] connect mysql successfully(by pool)')
            else:
                self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db,
                                            port=self.port)
                print('[info] connect mysql successfully(by connector)')
            self.cursor = self.conn.cursor()
        except Exception as e:
            print('[error] get_db_conn error:',e)

