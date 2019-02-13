from contextlib import contextmanager
from urllib.parse import urljoin

from alfacoins import ALFACoins
from nanohttp import Application
from restfulpy.mockup import mockup_http_server


@contextmanager
def alfacoins_mockup_gateway(root_controller):
    app = Application(root_controller)
    with mockup_http_server(app) as (server, url):
        yield ALFACoins(
            name='test-shop',
            password='abcdefgh',
            secret_key='d53974471e9b555554f5c318e07e9f23',
            base_url=urljoin(url, '/api/'),
        )


@contextmanager
def unauthorized_alfacoins_mockup_gateway(root_controller):
    app = Application(root_controller)
    with mockup_http_server(app) as (server, url):
        yield ALFACoins(
            base_url=urljoin(url, '/api/'),
        )
