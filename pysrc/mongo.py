__author__  = 'Chris Joakim'
__email__   = 'chjoakim@microsoft.com'
__license__ = 'MIT'
__version__ = '2022/08/30'

import json
import os

from pymongo import MongoClient
from bson.objectid import ObjectId

# This class uses the pymongo library to access a CosmosDB Mongo API database.

class Mongo(object):

    def __init__(self, opts):
        self._opts = opts
        self._db = None
        self._coll = None
        print(self._opts)
        host = opts['host']
        port = opts['port']
        self._client = MongoClient(host, port)
        print(self._client)

    def list_databases(self):
        return self._client.list_database_names()

    def list_collections(self):
        return self._db.list_collection_names()

    def set_db(self, dbname):
        self._db = self._client[dbname]
        print(self._db)
        return self._db 

    def set_coll(self, collname):
        self._coll = self._db[collname]
        print(self._coll)
        return self._coll 

    def insert_doc(self, doc):
        return self._coll.insert_one(doc)

    def find_one(self, query_spec):
        return self._coll.find_one(query_spec)

    def find(self, query_spec):
        return self._coll.find(query_spec)

    def find_by_id(self, id):
        return self._coll.find_one({'_id': ObjectId(id)})

    def delete_by_id(self, id):
        return self._coll.delete_one({'_id': ObjectId(id)})

    def delete_one(self, query_spec):
        return self._coll.delete_one(query_spec)

    def delete_many(self, query_spec):
        return self._coll.delete_many(query_spec)

    def update_one(self, filter, update, upsert):
        # 'update only works with $ operators'
        return self._coll.update_one(filter, update, upsert)

    def update_many(self, filter, update, upsert):
        # 'update only works with $ operators'
        return self._coll.update_many(filter, update, upsert)

    def count_docs(self, query_spec):
        return self._coll.count_documents(query_spec)

    def client(self):
        return self._client
