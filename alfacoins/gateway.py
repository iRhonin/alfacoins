import json
from hashlib import md5
from urllib.parse import urljoin

from requests import request

from .exceptions import APIException, ServerException


class ALFACoins:
    """
    Gateway class

    """
    def __init__(self, name: str = '', secret_key: str = '', password: str = '',
                 base_url: str = 'https://www.alfacoins.com/api/'):
        """
        :param name: Shop Name of API which you assigned when you create the
            API
        :param password: Password that you assigned when you create the API,
            the upper case MD5 hash of it will be stored
        :param secret_key: Secret key which is given after API was created
        :param base_url: Base url of APIs, Change it when you want to use a
            custom server like in tests
        """

        self.base_url = base_url
        self.name = name
        self.secret_key = secret_key
        self.password = password

    @property
    def password(self):
        return self._encoded_password

    @password.setter
    def password(self, raw_password: str):
        self._encoded_password = md5(raw_password.encode('utf-8')) \
            .hexdigest() \
            .upper()

    @property
    def is_authenticated(self):
        return bool(self.name and self.password and self.secret_key)

    def _http_requste(self, method: str, uri: str, params: dict = dict(), json_data: dict = dict()):
        url = urljoin(self.base_url, uri)
        response = request(
            method=method,
            url=url,
            params=params,
            json=json_data
        )
        return response.content.decode('utf-8'), response.status_code

    def _request(self, method: str, uri: str, params: dict = dict(), json_data: dict = dict()):
        if self.is_authenticated:
            json_data.update(
                name=self.name,
                secret_key=self.secret_key,
                password=self.password
            )

        result, status_code = self._http_requste(
            method=method,
            uri=uri,
            params=params,
            json_data=json_data,
        )

        if 500 <= status_code < 600:
            raise ServerException(result)

        if status_code == 200:
            result = json.loads(result)

        if status_code != 200 or 'error' in result:
            raise APIException(
                result['error']
                if status_code == 200
                else result)

        return result

    def get_rates(self):
        """
        Get rate for all available pairs

        :raises ServerException: Internal server error
        """
        return self._request('GET', 'rates.dict')

    def get_rate(self, pair: str):
        """
        Get rate for pair

        :param pair: Cryptocurrency and fiat Pair

        :raises ServerException: Internal server error
        :raises APIException: Invalid pair

        """
        return self._request('GET', f'rate/{pair}')[0]

    def get_fees(self):
        """
        Get all gate fees for deposit and withdrawal

        :raises ServerException: Internal server error
        """
        return self._request('GET', 'fees')

    def bitsend(self, type: str, options: dict, recipient_email: str = None, 
                amount: str = None, coin_amount: str = None, 
                recipient_name: str = None, reference: str = None):
        """
        BitSend primary use to payout salaries for staff or making direct
            deposits to different cryptocurrency addresses


        :param type: Cryptocurrency to pay with
        :param options: (array) Client cryptocurrency address for deposit,
            and additional tags i.e.
            {"address": "1FE7bSYsXSMrdXTCdRUWUB6jGFFba74fzm"} for Bitcoin,
            Litecoin, Ethereum, Dash
            {
                "address": "qFE7bSYsXSMrdXTCdRUWUB6jGFFba74fzm",
                "legacy_address": "1FE7bSYsXSMrdXTCdRUWUB6jGFFba74fzm"
            }
            for Bitcoin Cash {
                "address": "rExZpwNwwrmFWbX81AqbKJYkq8W6ZoeWE6",
                "destination_tag": "1294967290"
            } for XRP
        :param amount: Deposit amount in merchant's fiat currency (optional)
        :param coin_amount: Deposit amount in selected cryptocurrency
            (optional)
        :param recipient_name: Client Name (for email notification)
        :param recipient_email: Client email (for email notification)
        :param reference: Deposit description (for client notification)

        :raises ServerException: Internal server error
        :raises APIException: Related error message

        """
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

        return int(self._request('POST', 'bitsend', json_data=data)['id'])

    def bitsend_status(self, bitsend_id: int):
        """
        BitSend status primary use to get information of bitsend payout

        :params bitsend_id: (int) Bitsend ID

        :raises ServerException: Internal server error
        :raises APIException: Related error message
        """
        return self._request(
            'POST',
            'bitsend_status',
            json_data=dict(bitsend_id=bitsend_id),
        )

    def create_order(self, type: str, amount, order_id: float, options: dict, description: str,
                     currency: str = None):
        """
        Create order for payment

        :param order_id: Merchant's Order ID
        :param description: Description for order
        :param options: (Optional) Array {
                "notificationURL": "[custom Merchant's URL for paymentnotification]
                ",
                "redirectURL": "[Merchant's page which is shown after
                     payment is made by a customer]",
                "payerName": "[Customer's name for notification]",
                "payerEmail": "[Customer's email for notification]"
            }

        :raises ServerException: Internal server error
        :raises APIException: Related error message
        """
        data = dict(
            type=type,
            amount=amount,
            order_id=order_id,
            options=options,
            currency=currency,
            description=description
        )
        return self._request('POST', 'create', json_data=data)

    def order_status(self, txn_id: int):
        """
        Get status of created Order

        :param txn_id: ALFAcoins TXN ID

        :raises ServerException: Internal server error
        :raises APIException: Related error message
        """
        return self._request('POST', 'status', json_data=dict(txn_id=txn_id))

    def statistics(self):
        """Merchant's volume and balance statistics

        :raises ServerException: Internal server error
        :raises APIException: Related error message
        """

        return self._request('POST', 'stats')

    def refund(self, txn_id: int, options: dict = dict(), address: str = '', 
               amount: float = None, new_rate: bool = False):
        """
        Refund completed order

        :param txn_id: ALFAcoins TXN ID
        :param options: (array) Client cryptocurrency address for deposit,
            and additional tags i.e.
                {"address": "1FE7bSYsXSMrdXTCdRUWUB6jGFFba74fzm"}
                    for Bitcoin, Litecoin, Ethereum, Dash
                {
                    "address": "qFE7bSYsXSMrdXTCdRUWUB6jGFFba74fzm",
                    "legacy_address": "1FE7bSYsXSMrdXTCdRUWUB6jGFFba74fzm"
                } for Bitcoin Cash
                {
                    "address": "rExZpwNwwrmFWbX81AqbKJYkq8W6ZoeWE6",
                    "destination_tag": "1294967290"
                } for XRP
        :param amount: (Optional) Amount to refund, must be
            less Order amount, If omitted full amount will be refunded
        :param new_rate: (Optional) Use current time rates for fiat to
            cryptocurrency conversion or use order's rate

        :raises ServerException: Internal server error
        :raises APIException: Related error message
        """
        if not address and not options:
            raise KeyError('One of options or address is requierd')

        data = dict(
            txn_id=txn_id,
            options=options,
            amount=amount,
            new_rate=new_rate
        )
        return self._request('POST', 'refund', json_data=data)
