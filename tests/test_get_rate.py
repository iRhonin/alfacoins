import pytest
from alfacoins import APIException
from nanohttp import RegexRouteController, json

from .helper import unauthorized_alfacoins_mockup_gateway


class Root(RegexRouteController):
    def __init__(self):
        super().__init__([
            ('/api/rate/BTC_USD', self.get_rate),
            ('/api/rate/invalid-pair', self.get_invalid_rate),
        ])

    @json(verbs=['get'])
    def get_rate(self):
        return GET_BTC_USD_RATE_RESPONSE

    @json(verbs=['get'])
    def get_invalid_rate(self):
        return {'error': 'Invalid currency'}


def test_get_rates():
    with unauthorized_alfacoins_mockup_gateway(Root()) as gateway:
        rates = gateway.get_rate('BTC_USD')
        assert rates == GET_BTC_USD_RATE_RESPONSE[0]

        with pytest.raises(APIException):
            gateway.get_rate('invalid-pair')


GET_BTC_USD_RATE_RESPONSE = ['628.51000000']
