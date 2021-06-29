# -*- coding: utf-8 -*-
import pandas as pd
import time
from config import resultCli

df = pd.read_csv(r"qz_risk_zone_rain.csv", sep=',')
df.drop(columns=['id'], inplace=True)
df = df.tail(4000)
print(df)

# df1 = resultCli.query_params(table='sqxj_hj_biz_067_qx_skmyl_valid_old111', items=["*"])
# print(df1)
# cols = list(df1.columns)
# cols.remove("id")
# df.columns = cols
#
# df = df[df['city'] == "衢州"]


code_list = df['hash_unique'].drop_duplicates().to_list()
print(code_list)
for code in code_list:
    dfi = df[df['hash_unique'] == code]
    dfi = dfi.reset_index(drop=True)
    dfi = dfi.head(1)
    print(dfi)
    resultCli.insert_df(table='qz_risk_zone_rain', df=dfi)
    time.sleep(2)
