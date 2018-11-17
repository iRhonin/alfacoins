from hashlib import md5
from urllib.parse import urljoin
import json

from requests import request

from .exceptions import APIException, ServerException


class ALFACoins:

    def __init__(self, name=None, secret_key=None, password=None,
                 base_url='https://www.alfacoins.com/api/'):
        self.base_url = base_url
        self._is_authenticated = False

        if name and secret_key and password:
            self._is_authenticated = True
            self.name = name
            self.secret_key = secret_key
            self.password = password

    @property
    def password(self):
        return self._encoded_password

    @password.setter
    def password(self, raw_password):
        self._encoded_password = md5(raw_password.encode('utf-8')) \
            .hexdigest() \
            .upper()

    def _request(self, method, uri, params=None, data=None):
        url = urljoin(self.base_url, uri)
        return request(method=method, url=url, params=params, data=data)


    def request(self, method, uri, params=None, data=None):
        if self._is_authenticated:
            data.update(
                name=self.name,
                secret_key=self.secret_key,
                password=self.password
            )

        response = self._request(
            method=method,
            uri=uri,
            params=params,
            data=data
        )

        if 500 <= response.status_code < 600:
            raise ServerException()

        json_response = json.loads(response.content)

        if response.status_code == 200 and 'error' in json_response:
            raise APIException(json_response['error'])

        return json_response

    def get_rates(self):
        return self.request('GET', 'rates')

    def get_rate(self, pair):
        return float(self.request('GET', f'rate/{pair}')[0])

    def get_fees(self):
        return self.request('GET', 'fees')
