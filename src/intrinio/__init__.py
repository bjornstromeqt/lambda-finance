import json

import requests
from requests.auth import HTTPBasicAuth

import config


class IntrionioClient(object):
    SCHEME = 'https'
    NETLOC = 'api.intrinio.com'

    def __init__(self):
        username = config.current_config.INTRINIO_USERNAME
        password = config.current_config.INTRINIO_PASSWORD
        self.auth = HTTPBasicAuth(username, password)

    def make_request(self, method, endpoint, **kwargs):
        url = '{scheme}://{netloc}/{endpoint}'.format(
            scheme=self.SCHEME,
            netloc=self.NETLOC,
            endpoint=endpoint
        )

        response = requests.request(method, url, auth=self.auth, **kwargs)
        envelope = json.loads(response.text)
        return envelope
