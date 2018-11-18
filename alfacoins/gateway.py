import json
from hashlib import md5
from urllib.parse import urljoin

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

    def _request(self, method, uri, params=None, json_data=None):
        url = urljoin(self.base_url, uri)
        response =  request(
            method=method,
            url=url,
            params=params,
            json=json_data
        )
        return json.loads(response.content if response.content else None), \
            response.status_code

    def request(self, method, uri, params=dict(), json_data=dict()):

        if self._is_authenticated:
            json_data.update(
                name=self.name,
                secret_key=self.secret_key,
                password=self.password
            )

        result, status_code = self._request(
            method=method,
            uri=uri,
            params=params,
            json_data=json_data,
        )

        if 500 <= status_code < 600:
            raise ServerException()

        if status_code != 200 or 'error' in result:
            raise APIException(
                result['error']
                if status_code == 200
                else result[0])

        return result

    def get_rates(self):
        return self.request('GET', 'rates')

    def get_rate(self, pair):
        return self.request('GET', f'rate/{pair}')[0]

    def get_fees(self):
        return self.request('GET', 'fees')

    def bitsend(self, type, options, recipient_email=None, amount=None,
            coin_amount=None, recipient_name=None, reference=None):

        if amount is None and coin_amount is None:
            raise TypeError('One of amount or coin_amount must be passed')

        data = dict(
            type=type,
            amount=amount,
            coin_amount=coin_amount,
            recipient_name=recipient_name,
            recipient_email=recipient_email,
            reference=reference
        )

        return int(self.request('POST', 'bitsend', json_data=data))

    def bitsend_status(self, bitsend_id):
        return self.request(
            'POST',
            'bitsend_status',
            json_data=dict(bitsend_id = bitsend_id),
        )

    def create_order(self, type, amount, order_id, options, currency=None,
            description=None):
        data = dict(
            type=type,
            amount=amount,
            order_id=order_id,
            options=options,
            currency=currency,
            description=description
        )
        return self.request('POST', 'create', json_data=data)

    def order_status(self, txn_id):
        return self.request('POST', 'status', json_data=dict(txn_id=txn_id))

    def statistics(self):
        return self.request('POST', 'stats')

    def refund(self, txn_id, options, amount=None, new_rate=False):
        data = dict(
            txn_id=txn_id,
            options=options,
            amount=amount,
            new_rate=new_rate
        )
        return self.request('POST', 'refund', json_data=data)

