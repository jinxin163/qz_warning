# -*- coding: utf-8 -*-
from config import conf, resultCli
from dbClient import mysqlClient
from utils import switch_source_table
import time

_section1 = 'source_conn54'

sourceCli = mysqlClient(host=conf.get(_section1, 'ip'), port=conf.getint(_section1, 'port'),
                        user=conf.get(_section1, 'user'), password=conf.get(_section1, 'pw'),
                        db=conf.get(_section1, 'db'))


code = '3308240700BMQX0401'
table = switch_source_table(code)
print(table)
df = sourceCli.query_params(table=table,
                            items=['device_code', 'data_type_code', 'monitor_value', 'monitor_time', 'import_time'],
                            where={'device_code': code,
                                   'monitor_time': ['2021-05-23 00:00:00', None]})
# df = row_to_column(df)
# print(df)
# print(table)

time_list = df['monitor_time'].drop_duplicates().to_list()
print(time_list)

for t in time_list:
    print(t)
    dfi = df[df['monitor_time'] == t]
    dfi = dfi.reset_index(drop=True)
    print(dfi)
    resultCli.insert_df('qz_device_data', dfi)
    time.sleep(5)
