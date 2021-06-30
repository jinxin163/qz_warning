# -*- coding: utf-8 -*-
import pandas as pd
import time
from config import resultCli

df = pd.read_csv(r"qz_risk_zone_rain_report.csv")
df.drop(columns=['id'], inplace=True)
df = df[df['city'] == '衢州市']
print(df)
print(df.columns)

code_list = df['hash_unique'].drop_duplicates().to_list()
print(code_list)
for code in code_list:
    dfi = df[df['hash_unique'] == code]
    dfi = dfi.reset_index(drop=True)
    print(dfi)
    resultCli.insert_df(table='qz_risk_zone_rain_report', df=dfi)
    time.sleep(5)
