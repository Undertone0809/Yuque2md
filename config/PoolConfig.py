# -*- coding: utf-8 -*-
# @Time    : 2022/5/13 12:43
# @Author  : Zeeland
# @File    : PoolConfig.py
# @Software: PyCharm

from dbutils.pooled_db import PooledDB
import MySQLdb

class PoolConfig:
    def __init__(self):
        self.pool = None
        self.host = 'localhost'
        self.user = 'xxx'
        self.password = 'xxx'
        self.db = 'xxx'
        self.port = 3306
        self.pool_init()

    def pool_init(self):
        try:
            self.pool = PooledDB(MySQLdb, 5, host=self.host, user=self.user, passwd=self.password,
                                 db=self.db,port=self.port)
            print('[info] pool init')
        except Exception as e:
            print('[error]',e)

