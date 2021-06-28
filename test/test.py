# -*- coding: utf-8 -*-

import pandas as pd
from config import sourceCli

# df = sourceCli.query_params(table='qz_risk_zone_warning', items=["*"])
#
# print(df)
# print(df.columns)

df = pd.read_csv(r"C:\Users\X1\Desktop\qzdata\qz_warning_model.csv")
print(df)
sourceCli.insert_df(table='qz_warning_model', df=df)
