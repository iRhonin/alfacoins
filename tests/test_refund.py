import pytest
from nanohttp import RegexRouteController, json, context

from .helper import alfacoins_mockup_gateway


class Root(RegexRouteController):
    def __init__(self):
        super().__init__([
            ('/api/refund', self.refund),
        ])

    @json(verbs=['post'])
    def refund(self):
        return REFUND_RESPONSE


def test_refund():
    with alfacoins_mockup_gateway(Root()) as gateway:
        refund = gateway.refund(
            txn_id=1,
            address='rExZpwNwwrmFWbX81AqbKJYkq8W6ZoeWE6',
            amount=2,
        )
        assert refund == REFUND_RESPONSE

        refund = gateway.refund(
            txn_id=1,
            options={
                'address': 'rExZpwNwwrmFWbX81AqbKJYkq8W6ZoeWE6',
                'destination_tag': '1294967290'
            },
            amount=2,
        )
        assert refund == REFUND_RESPONSE

        with pytest.raises(KeyError):
            gateway.refund(txn_id=1, amount=2)


REFUND_RESPONSE = {'result': 'Refund is pending'}