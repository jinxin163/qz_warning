# -*- coding: utf-8 -*-
from config import sourceCli
import time
import warnings
warnings.filterwarnings("ignore")

def monitor_binding():
    df1 = sourceCli.query_params(table='qz_warning_model', items=["*"])
    print(df1)
    df2 = sourceCli.query_params(table='qz_warning_model_use_info', items=["*"])

    df1.columns = ['id', 'model_code', 'model_name', 'disaster_type', 'monitor_type',
                   'param_info', 'extra_param_info', 'model_type', 'version', 'remark',
                   'create_time', 'update_time', 'is_deleted']

    df1.drop(columns=['id'], inplace=True)
    df2.drop(columns=['id'], inplace=True)
    cols = list(df2.columns)
    print(cols)

    df3 = sourceCli.query_params(table='qz_monitor_device',
                                 items=["code", "monitor_type_id"],
                                 distinct=True)

    for i in range(len(df3)):
        device_code = df3.iloc[i]['code']
        monitor_type_id = df3.iloc[i]['monitor_type_id']
        dfi = df1[df1['monitor_type'] == str(monitor_type_id)]
        dfi['obj_id'] = device_code
        dfi['attachment_url'] = ''
        dfi = dfi[cols]
        dfi.reset_index(inplace=True, drop=True)
        print(dfi)
        if dfi.empty:
            continue
        sourceCli.insert_df(table='qz_warning_model_use_info', df=dfi)


# ----------------------------------------------------------------------
def risk_zone_binding():
    df1 = sourceCli.query_params(table='qz_warning_model', items=["*"])
    print(df1)
    df2 = sourceCli.query_params(table='qz_warning_model_use_info', items=["*"])

    df1.columns = ['id', 'model_code', 'model_name', 'disaster_type', 'monitor_type',
                   'param_info', 'extra_param_info', 'model_type', 'version', 'remark',
                   'create_time', 'update_time', 'is_deleted']

    df1.drop(columns=['id'], inplace=True)
    df2.drop(columns=['id'], inplace=True)
    cols = list(df2.columns)
    print(cols)

    df3 = sourceCli.query_params(table='qz_risk_zone',
                                 items=["risk_zone_num"],
                                 distinct=True)

    for i in range(len(df3)):
        risk_zone_num = df3.iloc[i]['risk_zone_num']
        dfi = df1[df1['monitor_type'] == str(1)]
        dfi['obj_id'] = risk_zone_num
        dfi['attachment_url'] = ''
        dfi = dfi[cols]
        dfi.reset_index(inplace=True, drop=True)
        print(dfi)
        print(dfi['model_type'])
        if dfi.empty:
            continue
        sourceCli.insert_df(table='qz_warning_model_use_info', df=dfi)


if __name__ == '__main__':
    monitor_binding()
    risk_zone_binding()
