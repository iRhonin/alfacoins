
from alfacoins import ALFACoins, APIException
from nanohttp import settings
import pytest

from .helper import alfacoins_mockup_server


def test_get_rates():
    alfacoins = ALFACoins()
    rates = alfacoins.get_rates()
    assert isinstance(rates, dict)
    assert isinstance(rates['BTC'], list)


def test_get_rate():
    alfacoins = ALFACoins()
    rates = alfacoins.get_rate('BTC_USD')
    assert isinstance(rates, float)

    with pytest.raises(APIException):
        alfacoins.get_rate('ABC_DEF')


def test_get_fees():
    alfacoins = ALFACoins()
    fees = alfacoins.get_fees()
    assert isinstance(fees, dict)

