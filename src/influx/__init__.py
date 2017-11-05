
from typing import List

from influxdb import DataFrameClient
import pandas as pd

import config


class InfluxClient(object):

    def __init__(self):
        host = config.current_config.INFLUX_HOST
        port = config.current_config.INFLUX_PORT
        user = config.current_config.INFLUX_USER
        password = config.current_config.INFLUX_PASSWORD
        db_name = config.current_config.INFLUX_DB

        self.client = self._create_data_frame_client(host, port, user, password, db_name)

    @staticmethod
    def _create_data_frame_client(host, port, user, password, db_name):
        _client = DataFrameClient(host, port, user, password, db_name)
        _client.create_database(db_name)
        _client.switch_database(db_name)
        return _client

    def write_to_db(self, data: pd.DataFrame, measurement: str, tag_columns: List[str]):
        return self.client.write_points(data, measurement=measurement, tag_columns=tag_columns, protocol='json')

    def query(self, query_string):
        return self.client.query(query_string)


def _build_query(symbol: str, start_date: str, end_date: str, order_by: str):
    """
    Build query from arguments

    :param symbol:
    :param start_date:
    :param end_date:
    :param order_by:
    :return:
    """
    query = "select * from stock_price where symbol = '{symbol}'".format(symbol=symbol)
    if start_date:
        query += " and time >= '{}'".format(start_date)
    if end_date:
        query += " and time <= '{}'".format(end_date)

    if order_by == 'ASC':
        # Default
        pass
    elif order_by == 'DESC':
        query += ' order by time desc'

    return query


def get_stock_prices(symbol, start_date=None, end_date=None, order_by='DESC'):
    """
    Get stock prices from database
    :param symbol:
    :param start_date:
    :param end_date:
    :param order_by:
    :return:
    """

    query = _build_query(symbol, start_date, end_date, order_by)
    client = InfluxClient()
    result = client.query(query)
    data_frame = result['stock_price']
    return data_frame


def write_stock_prices_to_db(df):
    client = InfluxClient()
    measurement = 'stock_price'
    return client.write_to_db(df, measurement=measurement, tag_columns=['symbol', 'market'])

