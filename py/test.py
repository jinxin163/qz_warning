# -*- coding: utf-8 -*-
import pandas as pd
from config import sourceCli

df = sourceCli.query_params(table='qz_risk_zone_warning', items=["*"])

print(df)
print(df.columns)

