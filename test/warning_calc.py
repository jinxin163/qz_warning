# -*- coding: utf-8 -*-
import datetime

import numpy as np
import pandas as pd
import scipy.stats as st

from config import sourceCli, weightingFactorJson
from dp import row_to_column, calc_displacement


def calculate_threshold(station_code, data_type_code):
    geo_score_sql = "SELECT * FROM ms_station_slope_score WHERE station_code=%s" % station_code
    geo_score_df = sourceCli.query_df(geo_score_sql)
    geo_score_df = geo_score_df.drop(columns=['id', 'station_code'])

    geo_weight_sql = "SELECT * FROM ms_station_slope_weight WHERE station_code=%s" % station_code
    geo_weight_df = sourceCli.query_df(geo_weight_sql)
    geo_weight_df = geo_weight_df.drop(columns=['id', 'station_code'])

    default_threshold_sql = 'SELECT model_code, rule_code, red_threshold, orange_threshold, yellow_threshold, ' \
                            'rule FROM ms_model_rule WHERE rule_code LIKE "%s" AND is_active=1' \
                            % ('%' + data_type_code + '%')
    default_threshold_df = sourceCli.query_df(default_threshold_sql)
    if default_threshold_df.empty:
        print('default_threshold_df.empty')
        return None, None, None
    model_code = default_threshold_df['model_code'][0]
    rule_code = default_threshold_df['rule_code'][0]
    M0 = 14.8
    geo_score_arr = np.array(geo_score_df.values.ravel())
    geo_weight_arr = np.array(geo_weight_df.values.ravel())
    if len(geo_score_arr) != 0 and len(geo_weight_arr) != 0:
        M = sum(geo_score_arr * geo_weight_arr)
    else:
        M = M0

    default_threshold_df = default_threshold_df.drop(columns=['model_code', 'rule_code'])
    threshold_dict = default_threshold_df.set_index('rule').to_dict()
    for key in threshold_dict.keys():
        for i in range(1, len(threshold_dict.get(key)) + 1):
            threshold_dict[key][i] = round(threshold_dict[key][i] * M / M0, 2)
    return model_code, rule_code, threshold_dict


def device_warning_calculate(df, device_code):
    station_code = device_code[:10]
    data_type = device_code[10:14]
    df = df.sort_values(by='monitor_time', ignore_index=True)
    model_code, rule_code, threshold_dict = calculate_threshold(station_code, data_type)
    if rule_code is None:
        return None
    level = 0
    threshold_value = 0
    warning_value = 0

    if data_type == 'GNSS':
        if len(df) < 24 * 3:
            print('数据不足')
            return None
        df = calc_displacement(df, station_code)
        s1 = df['S'].iloc[-24 * 2] - df['S'].iloc[-24 * 3]
        s2 = df['S'].iloc[-24] - df['S'].iloc[-24 * 2]
        s3 = df['S'].iloc[-1] - df['S'].iloc[-24]

        y1 = df['S'].iloc[-24 * 2: -24 * 1].tolist()
        y2 = df['S'].iloc[-24 * 1:].tolist()
        x = np.linspace(0, 1, num=len(y1))
        k1 = st.linregress(x, y1)[0]
        k2 = st.linregress(x, y2)[0]
        acce = k2 - k1

        if min([s1, s2, s3]) > threshold_dict.get('red_threshold').get(1):
            threshold_value = threshold_dict.get('red_threshold').get(1)
            warning_value = min([s1, s2, s3])
            level = 3
        elif s3 > threshold_dict.get('red_threshold').get(2):
            threshold_value = threshold_dict.get('red_threshold').get(2)
            warning_value = s3
            level = 3
        elif acce > threshold_dict.get('red_threshold').get(3):
            threshold_value = threshold_dict.get('red_threshold').get(3)
            warning_value = acce
            level = 3
        elif min([s1, s2, s3]) > threshold_dict.get('orange_threshold').get(1):
            threshold_value = threshold_dict.get('orange_threshold').get(1)
            warning_value = min([s1, s2, s3])
            level = 2
        elif s3 > threshold_dict.get('orange_threshold').get(2):
            threshold_value = threshold_dict.get('orange_threshold').get(2)
            warning_value = s3
            level = 2
        elif acce > threshold_dict.get('orange_threshold').get(3):
            threshold_value = threshold_dict.get('orange_threshold').get(3)
            warning_value = acce
            level = 2
        elif min([s1, s2, s3]) > threshold_dict.get('yellow_threshold').get(1):
            threshold_value = threshold_dict.get('yellow_threshold').get(1)
            warning_value = min([s1, s2, s3])
            level = 1
        elif s3 > threshold_dict.get('yellow_threshold').get(2):
            threshold_value = threshold_dict.get('yellow_threshold').get(2)
            warning_value = s3
            level = 1
        elif acce > threshold_dict.get('yellow_threshold').get(3):
            threshold_value = threshold_dict.get('yellow_threshold').get(3)
            warning_value = acce
            level = 1

    elif data_type in ['THSL', 'JSJC']:
        index = str(list(df.columns)).find(data_type)
        data_type_code = str(list(df.columns))[index:index+6]

        warning_value = df[data_type_code].tail(1).values[0]
        if warning_value > threshold_dict.get('red_threshold').get(1):
            threshold_value = threshold_dict.get('red_threshold').get(1)
            level = 3
        elif warning_value > threshold_dict.get('orange_threshold').get(1):
            threshold_value = threshold_dict.get('orange_threshold').get(1)
            level = 2
        elif warning_value > threshold_dict.get('yellow_threshold').get(1):
            threshold_value = threshold_dict.get('yellow_threshold').get(1)
            level = 1

    if level != 0:
        result_df = pd.DataFrame(data={"device_code": device_code,
                                       "data_type_code": data_type,
                                       "threshold_value": threshold_value,
                                       "warning_value": warning_value,
                                       "warning_level": level,
                                       "monitor_time": df['monitor_time'].tail(1).values,
                                       "import_time": str(datetime.datetime.now())[:19],
                                       "station_code": station_code,
                                       "rule_code": rule_code,
                                       "model_code": model_code})
    else:
        result_df = None

    return result_df


def comprehensive_warning_calculate(df, station_code):
    start = str(datetime.datetime.now())[:14] + '00:00'
    end = str(datetime.datetime.now())
    df = df[(df['monitor_time'] >= start) & (df['monitor_time'] < end)]
    if df.empty:
        return None
    df = df.groupby(['data_type_code'])['monitor_value'].mean()
    if 'GNSS01' in list(df.index):
        df = calc_displacement(df, station_code)
    factor = weightingFactorJson.get(station_code).keys()
    missing_data_type = [i for i in factor if i not in list(df.index)]
    if len(missing_data_type) > 0:
        print('缺少%s数据' % missing_data_type)
        return None

    model_code, rule_code, threshold_dict = calculate_threshold(station_code, 'ZH')
    if rule_code is None:
        return None
    level = 0
    threshold_value = 0
    warning_value = 0

    factor = weightingFactorJson.get(station_code)
    for key in factor.keys():
        warning_value = warning_value + factor.get(key) * df[key]

    if warning_value > threshold_dict.get('red_threshold').get(1):
        threshold_value = threshold_dict.get('red_threshold').get(1)
        level = 3
    elif warning_value > threshold_dict.get('orange_threshold').get(1):
        threshold_value = threshold_dict.get('orange_threshold').get(1)
        level = 2
    elif warning_value > threshold_dict.get('yellow_threshold').get(1):
        threshold_value = threshold_dict.get('yellow_threshold').get(1)
        level = 1

    if level != 0:
        result_df = pd.DataFrame(data={"device_code": df['device_code'].unique(),
                                       "data_type_code": 'comprehensive',
                                       "threshold_value": threshold_value,
                                       "warning_value": warning_value,
                                       "warning_level": level,
                                       "monitor_time": df['monitor_time'].tail(1).values,
                                       "import_time": str(datetime.datetime.now())[:19],
                                       "station_code": station_code,
                                       "rule_code": rule_code,
                                       "model_code": model_code})
    else:
        result_df = None

    return result_df


def warning_calculate_by_station(df, station_code):
    if df.empty:
        return None
    df['monitor_value'] = df['monitor_value'].astype('float')
    df['data_type_code'] = df['data_type_code'].apply(lambda x: x.upper())

    device_codes = df['device_code'].unique()
    warning_df = pd.DataFrame()
    for device_code in device_codes:
        print(device_code)
        dfi = df[df['device_code'] == device_code]
        dfi = dfi.drop(columns=['device_code'])
        dfi = row_to_column(dfi)
        warning_dfi = device_warning_calculate(dfi, device_code)
        if warning_dfi is not None:
            warning_df = warning_df.append(warning_dfi, ignore_index=True)
    comprehensive_warning_df = comprehensive_warning_calculate(df, station_code)
    if comprehensive_warning_df is not None:
        warning_df = warning_df.append(comprehensive_warning_df, ignore_index=True)

    if warning_df.empty:
        warning_df = None
    return warning_df

