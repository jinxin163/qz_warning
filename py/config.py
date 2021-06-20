# -*- coding:utf-8 -*-
import configparser
import os
import redis
from dbClient import mysqlClient

__projectName = 'qz_warning'
__curPath = os.getcwd()
rootPath = __curPath[:__curPath.find(__projectName) + len(__projectName)]

conf = configparser.ConfigParser()
conf.read(rootPath + r'/conf/conf.ini', encoding='utf-8')

_section1 = 'mysql_conn_zwy'
_section2 = 'mysql_conn_zwy'
_section3 = 'redis_conn_zwy'

# _section1 = 'source_conn'
# _section2 = 'result_conn'
# _section3 = 'redis_conn'

sourceCli = mysqlClient(host=conf.get(_section1, 'ip'), port=conf.getint(_section1, 'port'),
                        user=conf.get(_section1, 'user'), password=conf.get(_section1, 'pw'),
                        db=conf.get(_section1, 'db'))
resultCli = mysqlClient(host=conf.get(_section2, 'ip'), port=conf.getint(_section2, 'port'),
                        user=conf.get(_section2, 'user'), password=conf.get(_section2, 'pw'),
                        db=conf.get(_section2, 'db'))

pool = redis.ConnectionPool(host=conf.get(_section3, 'ip'), port=conf.get(_section3, 'port'),
                            password=conf.get(_section3, 'pw'),
                            decode_responses=True)

redisCli = redis.Redis(connection_pool=pool)
