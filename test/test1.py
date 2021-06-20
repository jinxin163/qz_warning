from config import sourceCli
from dp import row_to_column
import pandas as pd

code = '3308240102BMQX01021'
df = sourceCli.query_params(table='qz_warning_model', distinct=True,
                            items=['*'],
                            limit=18,
                            dt='df')
# df = row_to_column(df)
print(df)
a = df['param_info'][5]
print(a)
a = eval(a)
print(a)
c = a.get('red').get('JSJC01_1h')
print(c)
