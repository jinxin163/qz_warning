# -*- coding: utf-8 -*-
import time

from logger import logger
from process import *


def start():
    while True:
        device_codes = get_device_codes_updated()
        for device_code in device_codes:
            try:
                running_by_device_code(device_code)
            except:
                logger.exception(msg=device_code)

        # -----------------------------------------------------------------------------
        risk_zone_nums = get_risk_zone_nums_updated()
        for zone_num in risk_zone_nums:
            try:
                running_by_risk_zone_num(zone_num)
            except:
                logger.exception(msg=zone_num)

        time.sleep(10)


if __name__ == "__main__":
    start()
