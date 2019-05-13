# -*- coding:utf-8 -*-
"""
Author:zsprout
date:2019-04-26 13:11
desc:
"""
import pymysql


class Save_To_Mysql():
    _db_message = {
        'host': '3.112.113.214',
        'port': 3306,
        'user': 'root',
        'passwd': 'zsprout',
        'charset': 'utf8'
    }
    def __init__(self, **config):
        self.db_name = config.get('db', 'test')
        self.table_name= config.get('table', )

        self.connect = pymysql.connect(**self._db_message)
        db_sql = "CREATE DATABASE If Not Exists {} CHARACTER SET UTF8;".format(self.db_name)
        tb_sql = '''CREATE TABLE If Not Exists {}.{}(
                        rid bigint(8) not null Primary key,
                        uname varchar(200),
                        title varchar(500),
                        po_count int(9) not null,
                        time timestamp);'''.format(self.db_name, self.table_name)
        self.cursor = self.connect.cursor()
        try:
            try:
                self.cursor.execute("use %s;"%self.db_name)
            except Exception:
                self.cursor.execute(db_sql)
                self.execute("use %s;"%self.db_name)
            self.execute(tb_sql)
        except:
            pass

    def execute(self, sql, data=[]):
        try:
            self.cursor.execute(sql, data)
            self.connect.commit()
        except:
            self.connect.rollback()
    def insert(self, data):
        insert_sql = "INSERT INTO {}(%s) values(%s);".format(self.table_name)
        select_sql = "SELECT * FROM {} WHERE rid = %s;".format(self.table_name)
        col = ", ".join("{}".format(k) for k in data.keys())
        val = ", ".join("%({})s".format(k) for k in data.keys())
        try:
            sql = insert_sql % (col, val)
            self.execute(sql, data)
        except:
            pass
    def close(self):
        self.connect.close()

