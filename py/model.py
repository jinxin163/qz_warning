# -*- coding: utf-8 -*-
from dataIo import *
from dp import *
from logger import logger
from modelCalc import *


def GNSS(device_code):
    df = get_data_device(device_code, '3h')
    if df.empty:
        print('df.empty')
        return None
    indicators = calc_GNSS_S_past_time(df, '1h')
    result_df = generate_result_monitor_warning(device_code, indicators, df.index[-1])
    return result_df


def BMQX(device_code):
    df = get_data_device(device_code, '2h')
    if df.empty:
        print('df.empty')
        return None
    indicators = calc_diff_time_range(df, '1h')
    result_df = generate_result_monitor_warning(device_code, indicators, df.index[-1])
    return result_df


def DBLF(device_code):
    df = get_data_device(device_code, '2h')
    if df.empty:
        print('df.empty')
        return None
    indicators = calc_diff_time_range(df, '1h')
    result_df = generate_result_monitor_warning(device_code, indicators, df.index[-1])
    return result_df


def SWGD(device_code):
    df = get_data_device(device_code, '2h')
    if df.empty:
        print('df.empty')
        return None
    indicators = calc_diff_time_range(df, '1h')
    result_df = generate_result_monitor_warning(device_code, indicators, df.index[-1])
    return result_df


# -------------------------------------------
def SBQX(device_code):
    df = get_data_device(device_code, '2h')
    if df.empty:
        print('df.empty')
        return None
    indicators = calc_diff_time_range(df, '1h')
    result_df = generate_result_monitor_warning(device_code, indicators, df.index[-1])
    return result_df


def JSJC(device_code):
    df = get_data_device(device_code, '1h')
    if df.empty:
        print('df.empty')
        return None
    indicators = df.iloc[-1].to_dict()
    result_df = generate_result_monitor_warning(device_code, indicators, df.index[-1])
    return result_df


def BTJC(device_code):
    df = get_data_device(device_code, '1h')
    if df.empty:
        print('df.empty')
        return None
    indicators = df.iloc[-1].to_dict()
    result_df = generate_result_monitor_warning(device_code, indicators, df.index[-1])
    return result_df


def DXSW(device_code):
    df = get_data_device(device_code, '1h')
    if df.empty:
        print('df.empty')
        return None
    indicators = df.iloc[-1].to_dict()
    result_df = generate_result_monitor_warning(device_code, indicators, df.index[-1])
    return result_df


def THSL(device_code):
    df = get_data_device(device_code, '1h')
    if df.empty:
        print('df.empty')
        return None
    indicators = df.iloc[-1].to_dict()
    result_df = generate_result_monitor_warning(device_code, indicators, df.index[-1])
    return result_df


# -------------------------------------------


def QXJY(risk_zone_num):
    df = get_data_qx(risk_zone_num)
    if df.empty:
        print('df.empty')
        return None
    indicators = calc_sum_time_range(df, '24h')
    result_df = generate_result_zone_warning(risk_zone_num, indicators, df.index[-1])
    return result_df


def QXJY_report(risk_zone_num):
    df1 = get_data_qx(risk_zone_num)
    if df1.empty:
        print('df.empty')
        return None
    df2 = get_data_qx_report(risk_zone_num)
    if df1.empty:
        print('df.empty')
        return None

    indicators = calc_QXJY_report_12_24h(df1, df2)

    result_df = generate_result_zone_warning_report(risk_zone_num, indicators, df2.index[-1])
    return result_df


def switch_model(code, type=None):
    df = sourceCli.query_params(table='qz_warning_model_use_info',
                                items=['model_code'],
                                where={'obj_id': code})
    try:
        model_code = str(df['model_code'][0])
        model_code = model_code.split('-')
        model_code = model_code[0]
        if type == 'report':
            model_code = model_code + '_report'
        model_ = eval(model_code)
    except:
        logger.exception(msg='')
        return None
    return model_
