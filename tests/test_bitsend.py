from nanohttp import RegexRouteController, json
import pytest

from .helper import alfacoins_mockup_gateway


class Root(RegexRouteController):
    def __init__(self):
        super().__init__([
            ('/api/bitsend', self.bitsend),
        ])

    @json(verbs=['post'])
    def bitsend(self):
        return BITSEND_RESPONSE


def test_bitsend():
    with alfacoins_mockup_gateway(Root()) as gateway:
        bitsend_id = gateway.bitsend(
            type='bitcoin',
            amount=10,
            options={'address': '3P3QsMVK89JBNqZQv5zMAKG8FK3kJM4rjt'},
            recipient_name='test_client',
            recipient_email='abc@abc.com',
            reference=1,
        )
        assert bitsend_id == 1

        with pytest.raises(TypeError):
            gateway.bitsend(
                type='bitcoin',
                recipient_name='test_client',
                options={'address': '3P3QsMVK89JBNqZQv5zMAKG8FK3kJM4rjt'},
                recipient_email='abc@abc.com',
                reference=1,
            )


BITSEND_RESPONSE = {'id': '1'}
