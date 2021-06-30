# -*- coding: utf-8 -*-
import time
from process import *
from multiprocessing import Process


def monitor_warning():
    print('monitor_warning', flush=True)
    print(datetime.datetime.now())
    device_codes = []
    try:
        device_codes = get_device_codes_updated()
    except:
        logger.exception(msg='')

    for device_code in device_codes:
        try:
            running_monitor_warning(device_code)
        except:
            logger.exception(msg=device_code)


def risk_zone_warning():
    print('risk_zone_warning', flush=True)
    print(datetime.datetime.now())
    risk_zone_nums = []
    try:
        risk_zone_nums = get_risk_zone_nums_updated()
    except:
        logger.exception(msg='')

    for zone_num in risk_zone_nums:
        try:
            running_risk_zone_warning(zone_num)
        except:
            logger.exception(msg=zone_num)


def risk_zone_warning_report():
    print('risk_zone_warning_report', flush=True)
    print(datetime.datetime.now())
    risk_zone_nums_report = []
    try:
        risk_zone_nums_report = get_risk_zone_nums_updated_report()
    except:
        logger.exception(msg='')

    for zone_num in risk_zone_nums_report:
        try:
            running_risk_zone_report(zone_num)
        except:
            logger.exception(msg=zone_num)


if __name__ == "__main__":
    while True:
        # monitor_warning()
        # risk_zone_warning()
        # risk_zone_warning_report()
        # time.sleep(30)

        process = [Process(target=monitor_warning, args=()),  # 方法名不能带括号
                   Process(target=risk_zone_warning, args=()),
                   Process(target=risk_zone_warning_report, args=())]
        [p.start() for p in process]  # 开启了3个进程
        [p.join() for p in process]  # 等待进程依次结束
        time.sleep(60)
