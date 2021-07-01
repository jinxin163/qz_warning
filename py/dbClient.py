# -*- coding: utf-8 -*-
import pymysql
import pandas as pd


class mysqlClient:
    def __init__(self, host, port, user, password, db):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db

    def _get_connect(self):
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db)
        return conn

    def query(self, sql, dt='ori'):
        conn = self._get_connect()
        cur = conn.cursor()
        try:
            cur.execute(sql)
            results = cur.fetchall()
            cols = []
            for field in cur.description:
                cols.append(field[0])
            results = pd.DataFrame(data=results, columns=cols)
            if dt == 'df':
                pass
            if dt == 'list':
                results = list(results.values.ravel())
            if dt == 'dict':
                results = results.to_dict(orient='index')
                if len(results) == 1:
                    results = results.get(0)
            if dt == 'value_one':
                results = results.values.ravel()[0]

        except Exception as e:
            raise e
        finally:
            conn.close()
        return results

    def insert(self, sql):
        conn = self._get_connect()
        cur = conn.cursor()
        try:
            cur.execute(sql)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def insert_batch(self, sql, values):
        conn = self._get_connect()
        cur = conn.cursor()
        try:
            cur.executemany(sql, values)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def update(self, sql):
        conn = self._get_connect()
        cur = conn.cursor()
        try:
            cur.execute(sql)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def delete(self, sql):
        conn = self._get_connect()
        cur = conn.cursor()
        try:
            cur.execute(sql)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def insert_df(self, table, df):
        df = df.reset_index(drop=True)
        cols = list(df.columns)
        values = []
        for i in range(len(df)):
            value = []
            for col in cols:
                value.append(str(df[col][i]))
            values.append(tuple(value))
        sql = f'INSERT INTO {table} {tuple(cols)} VALUES {tuple(["%s"]*(len(cols)))}'.replace('\'', '')
        self.insert_batch(sql, values)

    def query_params(self, table, items, where=None, order_by=None, sort='ASC', limit=None, distinct=False, dt='df'):
        sql = 'SELECT '
        if distinct:
            sql = f'{sql} DISTINCT '
        for item in items:
            sql = sql + item
            if item != items[-1]:
                sql = sql + ', '
        sql = f'{sql} FROM {table}'

        if where is not None:
            sql = f'{sql} WHERE'
            keys = list(where.keys())
            for key in keys:
                value = where.get(key)
                if isinstance(value, list):

                    for i in range(len(value)):
                        if isinstance(value[i], str):
                            value[i] = f'"{value[i]}"'

                    if value.count(None) == 0:
                        sql = f'{sql} {key} > {value[0]} AND {key} < {value[1]}'
                    elif value[0] is not None:
                        sql = f'{sql} {key} > {value[0]}'
                    elif value[1] is not None:
                        sql = f'{sql} {key} < {value[1]}'
                else:
                    if isinstance(value, str):
                        if value.find('%') != -1:
                            sql = f'{sql} {key} LIKE "{value}"'
                        else:
                            sql = f'{sql} {key} = "{value}"'
                    else:
                        sql = f'{sql} {key} = {value}'
                if key != keys[-1]:
                    sql = sql + ' AND '

        if order_by is not None:
            sql = f'{sql} ORDER BY {order_by} {sort.upper()}'
        if limit is not None:
            sql = f'{sql} LIMIT {limit}'
        results = self.query(sql=sql, dt=dt)
        return results

    def query_latest_time(self, table, device_code):
        df = self.query_params(table=table,
                               items=['device_code', 'monitor_time'],
                               distinct=True,
                               where={"device_code": device_code},
                               order_by='monitor_time', sort='DESC', limit=10)
        df = df.drop_duplicates(subset=['device_code'])
        df = df.reset_index()
        dic = {}
        for i in range(len(df)):
            dic[df['device_code'][i]] = str(df['monitor_time'][i])
        return dic

