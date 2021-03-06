# -*- coding: utf-8 -*-
from utils import *


def calc_GNSS_S_past_time(df, time_range):
    x_col, y_col, z_col = 'GNSS01', 'GNSS02', 'GNSS03'

    df = df.resample('1' + time_range[-1]).last().ffill()
    df_new = df.tail(1)
    before_time = df.index[-1] - deltaTime(time_range)
    df_bt = df[df.index == before_time]

    if df_bt.empty:
        print('df_bt.empty')
        return {}

    delta_x = df_new[x_col][0] - df_bt[x_col][0]
    delta_y = df_new[y_col][0] - df_bt[y_col][0]
    delta_z = df_new[z_col][0] - df_bt[z_col][0]

    xy_s = pow(pow(delta_x, 2) + pow(delta_y, 2), 0.5)
    xyz_s = pow(pow(delta_x, 2) + pow(delta_y, 2) + pow(delta_z, 2), 0.5)

    dic = {f'XY_{time_range}': xy_s, f'Z_{time_range}': abs(delta_z), f'XYZ_{time_range}': xyz_s}
    return dic


def calc_sum_time_range(df, time_range):
    df = df.resample('1h').last().ffill()
    start_time = max(df.index) - deltaTime(time_range)
    df = df[df.index > start_time]
    df.columns = [f'{i}_{time_range}' for i in df.columns]
    dic = df.sum().to_dict()
    return dic


def calc_diff_time_range(df, time_range):
    df = df.resample('1' + time_range[-1]).last().ffill()

    start_time = df.index[-1] - deltaTime(time_range)
    df = df[df.index >= start_time]

    if len(df) < 2:
        print('len(df) < 2')
        return {}

    df = df.diff().dropna()
    df.columns = [col + '_' + time_range for col in df.columns]
    dic = df.to_dict('records')[0]
    return dic


def calc_QXJY_report_12_24h(df1, df2):
    df1 = df1.resample('1h').last().ffill()

    time_range = '12h'
    start_time = max(df1.index) - deltaTime(time_range)
    df1 = df1[df1.index > start_time]
    df1.columns = [f'{i}_{time_range}' for i in df1.columns]
    dic = df1.sum().to_dict()
    QXJY_PAST_12 = dic.get('QXJY_12h')

    QXJY_00_12 = df2['value_00_12'].values[0]
    QXJY_12_24 = df2['value_12_24'].values[0]

    QXJY_YB_12h = QXJY_PAST_12 + QXJY_00_12
    QXJY_YB_24h = QXJY_00_12 + QXJY_12_24

    dic1 = {'QXJY_YB_12h': QXJY_YB_12h, 'QXJY_YB_24h': QXJY_YB_24h}
    return dic1
