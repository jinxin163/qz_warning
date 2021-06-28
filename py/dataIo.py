# -*- coding: utf-8 -*-
import datetime
import dp
import pandas as pd
from config import redisCli, sourceCli
from utils import deltaTime, switch_source_table


def save_latest_time(key, lt_dict):
    redisCli.set(key + '_st_warning_lt', str(lt_dict))


def get_latest_time(key):
    lt_dict = redisCli.get(key + '_st_warning_lt')
    if lt_dict is None:
        return {}
    lt_dict = eval(lt_dict)
    return lt_dict


def save_latest_id(key, latest_id_dict):
    redisCli.set(key + '_st_warning_li', str(latest_id_dict))


def get_latest_id(key):
    latest_id = redisCli.get(key + '_st_warning_li')
    if latest_id is not None:
        latest_id = int(latest_id)
    return latest_id


def get_device_codes_updated():
    table = 'qz_device_data'
    old_id = get_latest_id(table)
    if old_id is None:
        lasted_id = sourceCli.query_params(table,
                                           items=['id'],
                                           order_by='id',
                                           sort='DESC',
                                           limit=1,
                                           dt='list')[0]
        save_latest_id(table, lasted_id)
        return []

    df = sourceCli.query_params(table,
                                items=['id', 'device_code'],
                                where={'id': [old_id, None]})

    id_list = df['id'].to_list()
    if len(id_list) > 0:
        lasted_id = max(id_list)
        save_latest_id(table, lasted_id)

    device_codes = df['device_code'].drop_duplicates().to_list()
    data_types = ["GNSS", "BMQX", "DBLF", "SWGD", "JSJC", "BTJC", "THSL", "SBQX"]
    device_codes = list(filter(lambda s: s.upper()[10:14] in data_types, device_codes))
    return device_codes


def get_risk_zone_nums_updated():
    table = 'sqxj_hj_biz_067_qx_skmyl_valid_old'
    old_id = get_latest_id(table)
    if old_id is None:
        lasted_id = sourceCli.query_params(table,
                                           items=['id'],
                                           order_by='id',
                                           sort='DESC',
                                           limit=1,
                                           dt='list')[0]
        save_latest_id(table, lasted_id)
        return []

    df = sourceCli.query_params(table,
                                items=['id', 'county'],
                                where={'id': [old_id, None]})

    id_list = df['id'].to_list()
    if len(id_list) > 0:
        lasted_id = max(id_list)
        save_latest_id(table, lasted_id)

    counties = df['county'].drop_duplicates().to_list()
    risk_zone_nums = []
    for county in counties:
        zone_nums = sourceCli.query_params('qz_risk_zone',
                                           items=['risk_zone_num'],
                                           where={'district_name': "%" + str(county)[0:2] + "%"},
                                           dt="list")
        for num in zone_nums:
            risk_zone_nums.append(num)
    return risk_zone_nums


def get_risk_zone_nums_updated_forecast():
    table = 'sqxj_hj_biz_067_qx_24xsljmyl_valid_old_copy'
    old_id = get_latest_id(table)
    if old_id is None:
        lasted_id = sourceCli.query_params(table,
                                           items=['id'],
                                           order_by='id',
                                           sort='DESC',
                                           limit=1,
                                           dt='list')[0]
        save_latest_id(table, lasted_id)
        return []

    df = sourceCli.query_params(table,
                                items=['id', 'county'],
                                where={'id': [old_id, None]})

    id_list = df['id'].to_list()
    if len(id_list) > 0:
        lasted_id = max(id_list)
        save_latest_id(table, lasted_id)

    counties = df['county'].drop_duplicates().to_list()
    risk_zone_nums = []
    for county in counties:
        zone_nums = sourceCli.query_params('qz_risk_zone',
                                           items=['risk_zone_num'],
                                           where={'district_name': "%" + str(county)[0:2] + "%"},
                                           dt="list")
        for num in zone_nums:
            risk_zone_nums.append(num)
    return risk_zone_nums


def get_data_device(device_code, time_range):
    lt = get_latest_time(device_code)
    lt = datetime.datetime.strptime(list(lt.values())[0], "%Y-%m-%d %H:%M:%S")
    start = str(lt - deltaTime(time_range))
    start = start[:14] + '00:00'
    end = str(lt + deltaTime('1d'))
    table = 'qz_device_data'

    df = sourceCli.query_params(table=table,
                                items=['data_type_code', 'monitor_value', 'monitor_time'],
                                where={'device_code': device_code, 'monitor_time': [start, end]})
    df = dp.row_to_column(df)
    return df


def get_data_qx(risk_zone_num):
    district_name = sourceCli.query_params(table='qz_risk_zone',
                                           items=["district_name"],
                                           where={"risk_zone_num": risk_zone_num}, dt='list')
    district_name = district_name[0][0:2]
    df = sourceCli.query_params(table='sqxj_hj_biz_067_qx_skmyl_valid_old',
                                items=['observtimes', 'value'],
                                where={'county': "%" + district_name + "%"},
                                order_by="observtimes",
                                sort="DESC",
                                limit=30,
                                distinct=True)
    df.index = pd.DatetimeIndex(df['observtimes'].tolist())
    df.drop(columns=['observtimes'], inplace=True)
    df.columns = ['QXJY']
    return df


def get_data_qx_report(risk_zone_num):
    district_name = sourceCli.query_params(table='qz_risk_zone',
                                           items=["district_name"],
                                           where={"risk_zone_num": risk_zone_num}, dt='list')
    district_name = district_name[0][0:2]
    df = sourceCli.query_params(table='sqxj_hj_biz_067_qx_24xsljmyl_valid_old',
                                items=['reporttimes', 'value_00_12', 'value_12_24'],
                                where={'county': "%" + district_name + "%"},
                                order_by="reporttimes",
                                sort="DESC",
                                limit=1,
                                distinct=True)

    df.index = pd.DatetimeIndex(df['reporttimes'].tolist())
    df.drop(columns=['reporttimes'], inplace=True)
    return df
