from nanohttp import RegexRouteController, json

from .helper import alfacoins_mockup_gateway


class Root(RegexRouteController):
    def __init__(self):
        super().__init__([
            ('/api/status', self.order_status),
        ])

    @json(verbs=['post'])
    def order_status(self):
        return ORDER_STATUS_RESPONSE


def test_order_status():
    with alfacoins_mockup_gateway(Root()) as gateway:
        order_status = gateway.order_status(1)
        assert order_status == ORDER_STATUS_RESPONSE


ORDER_STATUS_RESPONSE = {
      'status': 'paid',
      'deposit': {
          'address': 'rExZpwNwwrmFWbX81AqbKJYkq8W6ZoeWE6',
          'destination_tag': '1294967290',
      },
      'coin_requested_amount': '1.23',
      'requested_amount': '12.3',
      'amount': '1.2',
      'rate': '10',
      'coin_amount': '10',
      'currency': 'USD',
      'type': 'bitcoin',
      'date': '2018-11-11T13:54:06.127610',
      'url': 'test-url',
      'iframe': 'test-url'
}
