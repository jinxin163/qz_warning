# -*- coding: utf-8 -*-
import gc
import warnings

from config import resultCli
from model import *

warnings.filterwarnings('ignore')


def running_monitor_warning(device_code):
    print(device_code)
    source_table = 'qz_device_data'
    result_table = 'qz_monitor_warning'

    lt = sourceCli.query_latest_time(source_table, device_code)
    save_latest_time(device_code, lt)

    model_ = switch_model(device_code, modelType=1)
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


def running_risk_zone_warning(risk_zone_num):
    print(risk_zone_num)
    result_table = 'qz_risk_zone_warning'
    model_ = switch_model(risk_zone_num, modelType=2)
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


def running_risk_zone_report(risk_zone_num):
    print('report ' + risk_zone_num)
    result_table = 'qz_warning_forecast'
    model_ = switch_model(risk_zone_num, modelType=3)
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
