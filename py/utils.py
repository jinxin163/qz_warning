# -*- coding:utf-8 -*-
import datetime


def deltaTime(s):
    b = int(s[:-1])
    timedelta = None
    if s.find('s') != -1:
        timedelta = datetime.timedelta(seconds=b)
    if s.find('m') != -1:
        timedelta = datetime.timedelta(minutes=b)
    if s.find('h') != -1:
        timedelta = datetime.timedelta(hours=b)
    if s.find('d') != -1:
        timedelta = datetime.timedelta(days=b)
    return timedelta


def check_whether_data_updated(latest_time_dict_old, latest_time_dict):
    is_continue = False
    if len(latest_time_dict) == 0:
        return False
    if len(latest_time_dict_old) == 0:
        return True
    else:
        keys = latest_time_dict.keys()
        true_count = 0
        for key in keys:
            if latest_time_dict_old.get(key) is not None:
                if latest_time_dict.get(key) > latest_time_dict_old.get(key):
                    true_count += 1
        if true_count > 0:
            is_continue = True
    return is_continue


def switch_source_table(code):
    code = int(code[1: 6])
    mod = (code % 8)
    table = 'monitor_device_data' + str(mod + 1)
    return table

