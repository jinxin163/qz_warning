# -*- coding: utf-8 -*-

from dp import *

from utils import switch_source_table

code = '3303270729GNSS0401'
# table = switch_source_table(code)
# table = switch_source_table(code)
# start = str(datetime.datetime.now() - deltaTime('5d'))
df = sourceCli.query_params(table='qz_monitor_device',
                            items=['code'])
codes = df['code'].to_list()

data_types = [str(i).upper()[10:14] for i in codes]
data_types = set(data_types)
print(data_types)
print(len(data_types))
