from nanohttp import RegexRouteController, json

from .helper import alfacoins_mockup_gateway


class Root(RegexRouteController):
    def __init__(self):
        super().__init__([
            ('/api/stats', self.stats),
        ])

    @json(verbs=['post'])
    def stats(self):
        return STATISTICS_RESPONSE


def test_statistics():
    with alfacoins_mockup_gateway(Root()) as gateway:
        statistics = gateway.statistics()
        assert statistics == STATISTICS_RESPONSE


STATISTICS_RESPONSE = {
    'balances':{
        'BCH':'0.00000000',
        'BTC':'0.00000000',
        'DASH':'0.00000000',
        'ETH':'0.00000000',
        'LTC':'0.00000000',
        'LTCT':'0.00001188',
        'XRP':'0.00000000'
    },
    'volume':1.2,
    'pending':0
}
