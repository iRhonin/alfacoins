from contextlib import contextmanager

from nanohttp import RegexRouteController, json, settings, context, \
    HTTPStatus, Application, configure
from restfulpy.mockup import mockup_http_server


test_server_url = None


@contextmanager
def alfacoins_mockup_server():
    class Root(RegexRouteController):

        def __init__(self):
            super().__init__([
                ('/api/rates', self.get_rates),
            ])

        @json(verbs=['get'])
        def get_rates(self):
            return GET_RATES_RESPONSE

    app = Application(Root())
    with mockup_http_server(app) as (server, url):
        global test_server_url
        test_server_url = url
        yield app
