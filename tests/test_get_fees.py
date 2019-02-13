from nanohttp import RegexRouteController, json

from .helper import unauthorized_alfacoins_mockup_gateway


class Root(RegexRouteController):
    def __init__(self):
        super().__init__([
            ('/api/fees', self.get_fees),
        ])

    @json(verbs=['get'])
    def get_fees(self):
        return GET_FEES_RESPONSE


def test_get_fees():
    with unauthorized_alfacoins_mockup_gateway(Root()) as gateway:
        fees = gateway.get_fees()
        assert fees == GET_FEES_RESPONSE


GET_FEES_RESPONSE = {
    'bitcoin': {'deposit':{'commission':'0.99%','network_fee':'0 BTC'}}
}
