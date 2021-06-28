# -*- coding:utf-8 -*-
import datetime
import numpy as np
import pandas as pd

from config import sourceCli


def row_to_column(df):
    df.replace('', np.NAN, inplace=True)
    df['monitor_value'] = df['monitor_value'].astype('float')
    df['monitor_time'] = df['monitor_time'].apply(lambda x: str(x)[:17] + '00')
    df = df.drop_duplicates(subset=['data_type_code', 'monitor_time'])
    df = df.pivot(values='monitor_value', index='monitor_time', columns=['data_type_code'])
    df.index = pd.DatetimeIndex(df.index.tolist())
    df.columns = [i.upper() for i in df.columns]
    return df


def resample(df, period='1h', method='mean'):
    if method == 'mean':
        df = df.resample(period).mean()
    if method == 'mode':
        df = df.resample(period).mode()
    if method == 'median':
        df = df.resample(period).median()
    if method == 'min':
        df = df.resample(period).min()
    if method == 'median':
        df = df.resample(period).max()
    if method == 'sum':
        df = df.resample(period).sum()
    df = df.fillna(method='ffill')
    df = df.dropna()
    return df


def match_warning_level(indicators_dict, threshold_dict):
    warning_value, threshold_value, warning_level, gz_key_triggered = 0, 0, 0, 0
    level_keys = ['red', 'orange', 'yellow']
    gz_keys = list(set(threshold_dict.get('red').keys()) & set(indicators_dict.keys()))
    for level_key in level_keys:
        is_matched = False
        for gz_key in gz_keys:
            threshold_value = threshold_dict.get(level_key).get(gz_key)
            warning_value = indicators_dict.get(gz_key)
            gz_key_triggered = gz_key
            if warning_value > threshold_value:
                warning_level = 3 - level_keys.index(level_key)
                is_matched = True
                break
        if is_matched:
            break
    return warning_value, threshold_value, warning_level, gz_key_triggered


def generate_result_monitor_warning(code, indicators_dict, monitor_time):
    df = sourceCli.query_params(table='qz_warning_model_use_info',
                                items=['model_code', 'model_name', 'param_info', 'extra_param_info'],
                                where={"obj_id": code})
    info_dic = df.to_dict(orient='index')
    info_dic = info_dic.get(0)
    model_code = info_dic.get('model_code')
    model_name = info_dic.get('model_name')
    threshold_dict = eval(info_dic.get('param_info'))
    extra_param_info = eval(info_dic.get('extra_param_info'))

    warning_value, threshold_value, warning_level, gz_key_triggered = \
        match_warning_level(indicators_dict, threshold_dict)
    data_type_code = code[10:14]

    dic = sourceCli.query_params(table='qz_monitor_device',
                                 items=['station_code', 'name', 'monitor_type_id',
                                        'risk_zone_num', 'risk_zone_name'],
                                 where={"code": code},
                                 dt='dict')
    station_code = dic.get('station_code')
    station_name = dic.get('name')
    risk_zone_num = dic.get('risk_zone_num')
    risk_zone_name = dic.get('risk_zone_name')
    monitor_type_id = dic.get('monitor_type_id')
    warning_rule = extra_param_info.get(gz_key_triggered)

    if warning_level == 0:
        return None

    result_df = pd.DataFrame(data={"station_code": station_code,
                                   "station_name": station_name,
                                   "device_code": code,
                                   "monitor_type_id": monitor_type_id,
                                   "data_type_code": data_type_code,
                                   "model_code": model_code,
                                   "model_name": model_name,
                                   "risk_zone_num": risk_zone_num,
                                   "risk_zone_name": risk_zone_name,
                                   "threshold_value": threshold_value,
                                   "monitor_value": warning_value,
                                   "warning_level": warning_level,
                                   "warning_rule": warning_rule,
                                   "warning_time": monitor_time,
                                   "version": 1,
                                   "remark": '',
                                   "create_time": str(datetime.datetime.now())[:19],
                                   "update_time": str(datetime.datetime.now())[:19],
                                   "is_deleted": 0
                                   }, index=[0])
    return result_df


def generate_result_zone_warning(risk_zone_num, indicators_dict, monitor_time):
    df = sourceCli.query_params(table='qz_warning_model_use_info',
                                items=['model_code', 'model_name', 'param_info', 'extra_param_info'],
                                where={"obj_id": risk_zone_num})
    info_dic = df.to_dict(orient='index')
    info_dic = info_dic.get(0)
    model_code = info_dic.get('model_code')
    model_name = info_dic.get('model_name')
    threshold = eval(info_dic.get('param_info'))
    extra_param_info = eval(info_dic.get('extra_param_info'))

    warning_value, threshold_value, warning_level, gz_key_triggered = \
        match_warning_level(indicators_dict, threshold)

    df1 = sourceCli.query_params(table="qz_risk_zone",
                                 items=["risk_zone_name"],
                                 where={"risk_zone_num": risk_zone_num})
    risk_zone_name = df1.values[0]
    warning_rule = extra_param_info.get(gz_key_triggered)

    if warning_level == 0:
        return None

    result_df = pd.DataFrame(data={'model_code': model_code,
                                   'model_name': model_name,
                                   'risk_zone_num': risk_zone_num,
                                   'risk_zone_name': risk_zone_name,
                                   'threshold_value': threshold_value,
                                   'monitor_value': warning_value,
                                   'warning_rule': warning_rule,
                                   'warning_level': warning_level,
                                   'warning_time': monitor_time,
                                   "version": 1,
                                   "remark": '',
                                   "create_time": str(datetime.datetime.now())[:19],
                                   "update_time": str(datetime.datetime.now())[:19],
                                   "is_deleted": 0}, index=[0])
    return result_df


def generate_result_zone_warning_report(risk_zone_num, indicators_dict, monitor_time):
    df = sourceCli.query_params(table='qz_warning_model_use_info',
                                items=['model_code', 'model_name', 'param_info', 'extra_param_info'],
                                where={"obj_id": risk_zone_num})
    info_dic = df.to_dict(orient='index')
    info_dic = info_dic.get(0)
    model_code = info_dic.get('model_code')
    model_name = info_dic.get('model_name')
    threshold = eval(info_dic.get('param_info'))
    extra_param_info = eval(info_dic.get('extra_param_info'))
    threshold_new = {"red": {"QXJY_YB_12h": list(threshold.get('red').values())[0],
                             "QXJY_YB_24h": list(threshold.get('red').values())[0]},
                     "orange": {"QXJY_YB_12h": list(threshold.get('orange').values())[0],
                                "QXJY_YB_24h": list(threshold.get('orange').values())[0]},
                     "yellow": {"QXJY_YB_12h": list(threshold.get('yellow').values())[0],
                                "QXJY_YB_24h": list(threshold.get('yellow').values())[0]}}

    warning_value, threshold_value, warning_level, gz_key_triggered = \
        match_warning_level(indicators_dict, threshold_new)

    df1 = sourceCli.query_params(table="qz_risk_zone",
                                 items=["risk_zone_name"],
                                 where={"risk_zone_num": risk_zone_num})
    risk_zone_name = df1.values[0]
    warning_rule = extra_param_info.get(gz_key_triggered)
    map1 = {'QXJY_YB_12h': 1, 'QXJY_YB_24h': 2}
    forecast_time_type = map1.get(gz_key_triggered)

    if warning_level == 0:
        return None

    result_df = pd.DataFrame(data={'risk_zone_num': risk_zone_num,
                                   'risk_zone_name': risk_zone_name,
                                   'model_code': model_code,
                                   'model_name': model_name,
                                   'model_type': 1,
                                   'threshold_value': threshold_value,
                                   'monitor_value': warning_value,
                                   'warning_level': warning_level,
                                   'warning_rule': warning_rule,
                                   'warning_time': monitor_time,
                                   'forecast_time_type': forecast_time_type,
                                   "version": 1,
                                   "remark": '',
                                   "create_time": str(datetime.datetime.now())[:19],
                                   "update_time": str(datetime.datetime.now())[:19],
                                   "is_deleted": 0}, index=[0])
    return result_df
