# -*- coding: utf-8 -*-
import pandas as pd

from config import resultCli

df = pd.read_csv("C:\\Users\\X1\\Desktop\\skmyl.csv", sep='\t', header=None)
print(df)
print(df.columns)

df1 = resultCli.query_params(table='sqxj_hj_biz_067_qx_skmyl_valid_old', items=["*"])
cols = list(df1.columns)

df.columns = cols
print(df)

resultCli.insert_df(table='sqxj_hj_biz_067_qx_skmyl_valid_old', df=df.head(1))