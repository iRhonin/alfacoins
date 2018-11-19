from nanohttp import RegexRouteController, json

from .helper import alfacoins_mockup_gateway


class Root(RegexRouteController):
    def __init__(self):
        super().__init__([
            ('/api/create', self.create_order),
        ])

    @json(verbs=['post'])
    def create_order(self):
        return CREATE_ORDER_RESPONSE


def test_create_order():
    with alfacoins_mockup_gateway(Root()) as gateway:
        order = gateway.create_order(
            type='litecointestnet',
            amount=1.2345,
            currency='USD',
            order_id=1,
            options={
                'notificationURL': 'http://abc.com/notify',
                'redirectURL': 'http://abc.com/redirect',
                'payerName': 'Bob',
                'payerEmail': 'no_reply@alfacoins.com'
            },
            description='This is a test order',
     )
        assert order == CREATE_ORDER_RESPONSE


CREATE_ORDER_RESPONSE = {
      'id': '1',
      'address': 'rExZpwNwwrmFWbX81AqbKJYkq8W6ZoeWE6',
      'deposit': {
          'address': 'rExZpwNwwrmFWbX81AqbKJYkq8W6ZoeWE6',
          'destination_tag': '1294967290',
      },
      'coin_amount': '1.234',
      'url': 'test-url',
      'iframe': 'test-url'
}

