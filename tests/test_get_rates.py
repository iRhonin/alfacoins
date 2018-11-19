from nanohttp import RegexRouteController, json

from tests.helper import alfacoins_mockup_gateway


class Root(RegexRouteController):
    def __init__(self):
        super().__init__([
            ('/api/rates', self.get_rates),
        ])

    @json(verbs=['get'])
    def get_rates(self):
        return GET_RATES_RESPONSE

def test_get_rates():
    with alfacoins_mockup_gateway(Root()) as gateway:
        rates = gateway.get_rates()
        assert rates == GET_RATES_RESPONSE


GET_RATES_RESPONSE = {'BTC':[{'code':'AED','rate':1.23}]}
