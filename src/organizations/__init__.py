import json
import requests

import config


def _get_data_from_spreadsheet():
    params = {
        'key': config.current_config.GOOGLE_API_KEY
    }
    spreadsheet_id = '1mcSKvl1-qND2Rfco6zUPzUZeMDkwQtToBV6jJQs1iwM'
    base = 'https://sheets.googleapis.com/v4/spreadsheets'
    sheet_range = 'companies!A1:X100'

    url = '{base}/{sid}/values/{range}'.format(
        base=base, sid=spreadsheet_id, range=sheet_range
    )

    response = requests.get(url, params=params)
    return json.loads(response.content)


def get_organizations():
    data = _get_data_from_spreadsheet()

    headers = data['values'][0]
    rows = data['values'][1:]

    return [dict(zip(headers, row)) for row in rows]


def get_organization(name):
    data = _get_data_from_spreadsheet()

    headers = data['values'][0]

    # Name if the first column
    for row in data['values']:
        if row[0] == name:
            return dict(zip(headers, row))

    return None
