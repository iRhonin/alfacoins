
from nanohttp import RegexRouteController, json

from .helper import unauthorized_alfacoins_mockup_gateway


class Root(RegexRouteController):
    def __init__(self):
        super().__init__([
            ('/api/rates.dict', self.get_rates),
        ])

    @json(verbs=['get'])
    def get_rates(self):
        return GET_RATES_RESPONSE


def test_get_rates():
    with unauthorized_alfacoins_mockup_gateway(Root()) as gateway:
        rates = gateway.get_rates()
        assert rates == GET_RATES_RESPONSE
        assert rates['BTC'] == GET_RATES_RESPONSE['BTC']
        assert rates['BTC']['USD'] == GET_RATES_RESPONSE['BTC']['USD']


GET_RATES_RESPONSE = {
  'BTC': {'USD': 628.54, 'EUR': 579.940948},
  'LTC':  {'USD': 3.76613, 'EUR': 3.474931}
}
