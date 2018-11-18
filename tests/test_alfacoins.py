
from alfacoins import ALFACoins, APIException
from nanohttp import settings
import pytest

from .helper import alfacoins_mockup_server



class TestALFACoins:

    @property
    def alfacoins(self):
        if not hasattr(self, '_gateway'):
            self._gateway = ALFACoins(
                name='alpha-test',
                password='abcdefgh',
                secret_key='d53974471e9b555554f5c318e07e9f23',
            )
        return self._gateway

    def test_get_rates(self):
        rates = self.alfacoins.get_rates()
        assert isinstance(rates, dict)
        assert isinstance(rates['BTC'], list)

    def test_get_rate(self):
        rate = self.alfacoins.get_rate('BTC_USD')
        assert isinstance(rate, str)

        with pytest.raises(APIException):
            self.alfacoins.get_rate('ABC_DEF')

    def test_get_fees(self):
        fees = self.alfacoins.get_fees()
        assert isinstance(fees, dict)

    def test_bitsend(self):
        bitsend_id = self.alfacoins.bitsend(
            type='litecointestnet',
            amount=10,
            options={'address': '3P3QsMVK89JBNqZQv5zMAKG8FK3kJM4rjt'},
            recipient_name='test_client',
            recipient_email='abc@abc.com',
            reference=1,
        )
        assert bitsend_id is not None

    def test_bitsend_status(self):
        bitsend_status = self.alfacoins.bitsend_status(34516)
        assert isinstance(bitsend_status, dict)

    def test_create_order(self):
        order = self.alfacoins.create_order(
            type='litecointestnet',
            amount=1.2345,
            currency='USD',
            order_id=1,
            options={
                'notificationURL': 'http://abc.com/notify',
                'redirectURL': 'http://abc.com/succeed',
                'payerName': 'Bob',
                'payerEmail': 'no_reply@alfacoins.com'
            },
            description='This is a test order',
        )
        assert order['id'] is not None

    def test_order_status(self):
        order = self.alfacoins.order_status(1)
        assert 'status' in order

    def test_statistics(self):
        statistics = self.alfacoins.statistics()
        assert 'balances' in statistics

    def test_refund(self):
        result = self.alfacoins.refund(
            1,
            options={'address': '1FE7bSYsXSMrdXTCdRUWUB6jGFFba74fzm'}
        )
