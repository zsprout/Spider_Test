# -*- coding:utf-8 -*-
"""
Author:zsprout
date:2019-04-26 13:19
desc:
"""
import pymongo

class Save_To_Mongodb():

    _uri = "mongodb://root:zsprout@13.114.32.216"

    def __init__(self, **config):
        self.db_name = config.get('db', 'test')
        self.collection_name = config.get('table', 'test')

        self.client = pymongo.MongoClient(self._uri)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def insert(self, data):
        self.collection.update({'rid': data['rid']}, {'$set': data}, True)

    def close(self):
        self.client.close()

