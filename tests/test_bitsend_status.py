from nanohttp import RegexRouteController, json

from .helper import alfacoins_mockup_gateway


class Root(RegexRouteController):
    def __init__(self):
        super().__init__([
            ('/api/bitsend_status', self.bitsend_status),
        ])

    @json(verbs=['post'])
    def bitsend_status(self):
        return BITSEND_STATUS_RESPONSE


def test_statistics():
    with alfacoins_mockup_gateway(Root()) as gateway:
        bitsend_status = gateway.bitsend_status(1)
        assert bitsend_status == BITSEND_STATUS_RESPONSE


BITSEND_STATUS_RESPONSE = {
    'status': 'paid',
    'coin_amount': '1.23456789',
    'rate': '1.2',
    'type': 'bitcoin',
    'txid': '1',
}