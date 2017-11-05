import datetime
import requests

import pandas as pd
import inflection


class InvalidRequest(Exception):
    """ Exception for invalid request"""
    pass


def _make_request(market: str, symbol: str, start_date: str, end_date: str):
    """ Make request to Google """
    params = {
        'q': '{market}:{symbol}'.format(market=market, symbol=symbol),
        'startdate': start_date,
        'enddate': end_date,
        'output': 'csv'
    }

    url = 'http://finance.google.com/finance/historical'
    response = requests.get(url, params=params)

    if response.ok is False:
        raise InvalidRequest(response.text)

    return response


def _format_response_string(response_string: str):
    """
    Format CSV-like response-string to an array

    :param response_string:
    :return:
    """

    # Split on new lines ('\n') and commas
    rows = filter(lambda row: row and row != '', response_string.split('\n'))
    resp_data = [str(row).split(',') for row in rows]
    return resp_data


def _convert_to_date(date_string):
    date_format = '%d-%b-%y'
    dt = datetime.datetime.strptime(date_string, date_format)
    date = datetime.date(dt.year, dt.month, dt.day)
    return date


def _is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        # Not possible
        return False


def _build_data_frame(data: list):
    """
    Build data frame from the response

    :param data:
    :return:
    """
    # The first row is the column names, the rest is the body
    headers, body = data[0], data[1:]
    df = pd.DataFrame(body, columns=headers)

    # Format the dates to python date-objects.
    date_column_name = 'Date'
    dates = df[date_column_name].map(lambda x: _convert_to_date(x))

    # Set the date as index and drop date-column
    # https://stackoverflow.com/questions/17328655/pandas-set-datetimeindex
    df.set_index(pd.DatetimeIndex(dates), inplace=True)
    df.drop(date_column_name, axis=1, inplace=True)

    # All other columns should be numeric values
    for column in df.columns:
        # Clean out invalid rows.
        # Feels sub-optimal but might be necessary to actually check all columns.
        df = df[df[column].apply(lambda value: _is_numeric(value))]
        df[column] = df[column].map(lambda value: float(value))

    return df


def _format_date(date_or_datetime):
    if isinstance(date_or_datetime, (datetime.datetime, datetime.date)):
        return date_or_datetime.strftime('%Y-%m-%d')
    return date_or_datetime


def get_data(market='NASDAQ', symbol='AAPL', start_date=None, end_date=None) -> pd.DataFrame:
    """
    Get historical Stock prices

    :param market:
    :param symbol:
    :param start_date:
    :param end_date:
    :return: DataFrame
    """

    start_date = _format_date(start_date) if start_date else datetime.date(2017, 1, 1)
    end_date = _format_date(end_date) if end_date else datetime.date(2017, 5, 1)

    response = _make_request(market, symbol, start_date, end_date)

    data = _format_response_string(response.text)
    df = _build_data_frame(data)

    # Set attributes on columns
    df['market'] = market
    df['symbol'] = symbol

    # Make sure columns are camel_case
    df.rename_axis(lambda column_name: inflection.underscore(column_name), axis=1, inplace=True)

    # The index of the dataframe is the date, set as a column.
    df['date'] = df.index
    return df
