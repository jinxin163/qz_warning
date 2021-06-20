# -*- coding: utf-8 -*-
import gc
import warnings

from config import resultCli
from model import *

warnings.filterwarnings('ignore')


def running_by_device_code(device_code):
    print(device_code)
    source_table = 'qz_device_data'
    result_table = 'qz_monitor_warning'

    lt = sourceCli.query_latest_time(source_table, device_code)
    save_latest_time(device_code, lt)

    model_ = switch_model(device_code)
    if model_ is None:
        print('model is None')
        return

    result_df = model_(device_code)

    if result_df is not None:
        print(result_df)
        resultCli.insert_df(result_table, result_df)

    for x in locals().keys():
        del locals()[x]
    gc.collect()


def running_by_risk_zone_num(risk_zone_num):
    print(risk_zone_num)
    result_table = 'qz_risk_zone_warning'
    model_ = switch_model(risk_zone_num)
    if model_ is None:
        print('model is None')
        return

    result_df = model_(risk_zone_num)

    if result_df is not None:
        print(result_df)
        resultCli.insert_df(result_table, result_df)

    for x in locals().keys():
        del locals()[x]
    gc.collect()
