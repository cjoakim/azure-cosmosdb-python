"""
Usage:
  python main.py <func>
  python main.py env         <-- displays necessary environment variables
  python main.py cosmos_sql  <-- executes a suite of CosmosDB SQL API operations
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

__author__  = 'Chris Joakim'
__email__   = 'chjoakim@microsoft.com'
__license__ = 'MIT'
__version__ = '2022/08/30'

import base64
import json
import sys
import time
import os

from docopt import docopt

from pysrc.cosmos import Cosmos
from pysrc.env import Env
from pysrc.fs import FS
from pysrc.mongo import Mongo


def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version=__version__)
    print(arguments)

def check_env():
    print('AZURE_COSMOSDB_SQL_URI:     {}'.format(Env.var('AZURE_COSMOSDB_SQL_URI')))
    print('AZURE_COSMOSDB_SQL_RW_KEY1: {}'.format(Env.var('AZURE_COSMOSDB_SQL_RW_KEY1')))
    print('AZURE_COSMOSDB_SQL_DB:      {}'.format(Env.var('AZURE_COSMOSDB_SQL_DB')))

def check_fs():
    pwd = FS.pwd()
    print('pwd: {}'.format(pwd))
    files = FS.walk(pwd)
    for file in files:
        if 'cj-py/pysrc' in file['dir']:
            if file['base'].endswith('.py'):
                print(file['full'])
    print('count: {}'.format(len(files)))

    infile = 'data/postal_codes_nc.csv'
    rows = FS.read_csvfile_into_rows(infile, delim=',')
    for idx, row in enumerate(rows):
        if idx < 5:
            print(row)

    objects = FS.read_csvfile_into_objects(infile, delim=',')
    for idx, obj in enumerate(objects):
        if idx < 5:
            print(obj)

def check_cosmos_mongo():
    opts = dict()
    opts['host'] = 'localhost'
    opts['port'] = 27017
    m = Mongo(opts)
    db = m.set_db('dev')
    coll = m.set_coll('movies')
    movies = FS.read_json('data/movies.json')
    keys = sorted(movies.keys())
    for idx, key in enumerate(keys):
        if idx < 100:
            data = dict()
            data['title_id'] = key
            data['title'] = movies[key]
            data['doctype'] = 'movie'
            if idx < 12:
                data['top10'] = True
            else:
                data['top10'] = False
            result = m.insert_doc(data)
            #print('{} -> {}'.format(str(result.inserted_id), str(data)))
            print(data)
    print(m.list_collections())
    print(m.list_databases())
    print(m.find_one({"title": 'Footloose'}))
    print(m.find_one({"title": 'Not There'}))
    print(m.find_by_id('5ea575f08bd3a96405ea6366'))

    um = m.update_many({"top10": True}, {'$set': {"rating": 100, "bacon": False}}, False)
    print(um)
    fl2 = m.update_one({"title": 'Footloose'}, {'$set': {"rating": 100, "bacon": True}}, False) # update_one(filter, update, upsert)
    print(fl2)
    fl3 = m.find_one({"title": 'Footloose'})
    print(fl3)
    cursor = m.find({"top10": True})
    for doc in cursor:
        print(doc)

    print(m.count_docs({}))
    print(m.count_docs({"title": 'Footloose'}))
    print(m.delete_by_id('5ea575f08bd3a96405ea6366'))
    print(m.count_docs({}))
    print(m.delete_one({"title": 'The Money Pit'}))
    print(m.count_docs({}))
    print(m.delete_many({"doctype": 'movie'}))
    print(m.count_docs({}))

def check_cosmos_sql():
    opts = dict()
    opts['url'] = Env.var('AZURE_COSMOSDB_SQL_URI')
    opts['key'] = Env.var('AZURE_COSMOSDB_SQL_RW_KEY1')
    dbname = Env.var('AZURE_COSMOSDB_SQL_DB')
    cname  = 'testing'  # cname is container name

    c = Cosmos(opts)    # see file pysrc/cosmos.py in this repo for my Cosmos wrapper class

    print('disable/enable metrics, print_record_diagnostics:')
    c.disable_query_metrics()
    c.enable_query_metrics()
    c.reset_record_diagnostics()
    c.print_record_diagnostics()
    c.print_last_request_charge()

    print('list_databases:')
    for db in c.list_databases():
        print('database: {}'.format(db['id']))   
    c.print_last_request_charge()

    print('set_db:')
    dbproxy = c.set_db(dbname)
    c.print_last_request_charge()

    print('list_containers:')
    for con in c.list_containers():
        print('container: {}'.format(con['id']))    
    c.print_last_request_charge()

    print('delete_container:')
    c.delete_container(cname)
    c.print_last_request_charge()

    print('create_container:')
    ctrproxy = c.create_container(cname, '/pk', 500)
    c.print_last_request_charge()

    print('create_container:')
    ctrproxy = c.create_container(cname, '/pk', 500)
    c.print_last_request_charge()

    print('set_container:')
    ctrproxy = c.set_container(cname)
    c.print_last_request_charge()
    
    print('update_container_throughput:')
    offer = c.update_container_throughput(cname, 600)
    c.print_last_request_charge()

    print('get_container_offer:')
    offer = c.get_container_offer(cname)
    c.print_last_request_charge()

    infile = 'data/postal_codes_nc.csv'
    objects = FS.read_csvfile_into_objects(infile, delim=',')
    documents = list()
    ctrproxy = c.set_container(cname)

    print('upsert_docs:')
    for idx, obj in enumerate(objects):
        del obj['id']
        if idx < 10:
            obj['pk'] = obj['postal_cd']
            print(obj)
            result = c.upsert_doc(obj)
            documents.append(result)
            c.print_last_request_charge()

    for idx, doc in enumerate(documents):
        if idx < 3:
            result = c.delete_doc(doc, doc['pk'])
            print('delete result: {}'.format(result))
            c.print_last_request_charge()
        else:
            doc['updated'] = True
            result = c.upsert_doc(doc)
            print('update result: {}'.format(result))
            c.print_last_request_charge()

    sql = "select * from c where c.state_abbrv = 'NC'"
    print('query; sql: {}'.format(sql))
    items = c.query_container(cname, sql, True, 1000)
    c.print_last_request_charge()
    last_id, last_pk = None, None
    for item in items:
        last_id = item['id']
        last_pk = item['pk']
        print(json.dumps(item, sort_keys=False, indent=2))

    print('read_doc; id: {} pk: {}'.format(last_id, last_pk))
    doc = c.read_doc(cname, last_id, last_pk)
    print(doc)
    c.print_record_diagnostics()
    c.print_last_request_charge()

    print('record_diagnostics_headers_dict:')
    print(json.dumps(c.record_diagnostics_headers_dict(), sort_keys=True, indent=2))
    
    print('reset and print diagnostics')
    c.reset_record_diagnostics()
    c.print_record_diagnostics()

    # Delete documents that are the results of a query
    sql = "select * from c where c.pk in ('27013', '27016')"
    print('query; sql: {}'.format(sql))
    items = c.query_container(cname, sql, True, 1000)
    c.print_last_request_charge()
    last_id, last_pk = None, None
    for item in items:
        print('deleting document:')
        print(json.dumps(item, sort_keys=False, indent=2))
        c.delete_doc(item, item['pk'])

    # print('delete container: {}'.format(cname))
    # c.delete_container(cname)
    # c.print_last_request_charge()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli_func = sys.argv[1].lower()

        if cli_func == 'env':
            check_env()
        elif cli_func == 'cosmos_sql':
            check_cosmos_sql()
        elif cli_func == 'fs':
            check_fs()
        elif cli_func == 'check_cosmos_mongo':
            check_cosmos_mongo()
        else:
            print_options('Error: invalid command-line function: {}'.format(cli_func))
    else:
        print_options('Error: no command-line args provided') 
