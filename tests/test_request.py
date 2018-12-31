from alfacoins import ServerException, APIException
from nanohttp import RegexRouteController, json, context
import pytest

from .helper import alfacoins_mockup_gateway


class Root(RegexRouteController):
    def __init__(self):
        super().__init__([
            ('/api/GET-test', self.get_test),
            ('/api/POST-test', self.post_test),
        ])

    @json(verbs=['get'])
    def get_test(self):
        return dict(get='GET')

    @json(verbs=['post'])
    def post_test(self):
        if context.form['a'] == 'a':
            return dict(a='a')
        elif context.form['a'] == 'server error':
            return 1/0
        elif context.form['a'] == 'api error':
            return dict(error='error')


class TestRequest:

    def test_request(self):
        with alfacoins_mockup_gateway(Root()) as gateway:
            result = gateway._request('GET', 'GET-test')
            assert result == dict(get='GET')

            result = gateway._request('POST', 'POST-test', json_data=dict(a='a'))
            assert result['a'] == 'a'

            with pytest.raises(ServerException):
                gateway._request(
                    'POST',
                    'POST-test',
                    json_data=dict(a='server error')
                )

            with pytest.raises(APIException):
                gateway._request(
                    'POST',
                    'POST-test',
                    json_data=dict(a='api error')
                )
