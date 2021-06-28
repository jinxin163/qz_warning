# -*- coding: utf-8 -*-
import pandas as pd
import time
from config import resultCli

df = pd.read_csv(r"24xsljmyl.csv", header=None)
print(df)

df1 = resultCli.query_params(table='qz_risk_zone_rain_report', items=["*"])
print(df1)
cols = list(df1.columns)
cols.remove("id")
df.columns = cols
print(df)
df = df[df['city'] == "衢州市"]
print(df)

code_list = df['hash_unique'].drop_duplicates().to_list()
print(code_list)
for code in code_list:
    dfi = df[df['hash_unique'] == code]
    dfi = dfi.reset_index(drop=True)
    dfi = dfi.head(1)
    print(dfi)
    resultCli.insert_df(table='qz_risk_zone_rain_report', df=dfi)
    time.sleep(5)
