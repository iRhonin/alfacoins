Python ALFACoins

A Python3.6 wapper aournd the [ALFACoins](https://www.alfacoins.com/) [APIs](https://www.alfacoins.com/developers).
 
by [Carrene](https://github.com/Carrene).

[![Build Status](https://travis-ci.com/ArashFatahzade/alfacoins.svg?branch=master)](https://travis-ci.com/ArashFatahzade/alfacoins)
[![Coverage Status](https://coveralls.io/repos/github/ArashFatahzade/alfacoins/badge.svg?branch=master)](https://coveralls.io/github/ArashFatahzade/alfacoins?branch=master)

## Description

**alfacoins** is a Python3.6 Library for interacting with [ALFAcoins API](https://www.alfacoins.com/developers).

**alfacoins** provides cryptocurrency payment integration on your website via [ALFAcoins](https://www.alfacoins.com).

**alfacoins** allows you to integrate payments with the following cryptocurrencies:
* Bitcoin (BTC)
* Ethereum (ETH)
* XRP (XRP)
* Bitcoin Cash (BCH)
* Litecoin (LTC)
* Dash (DASH)

## APIs
* get_fees
* get_rate
* get_rates
* create_order*
* order_status*
* bitsend*
* bitsend_status*
* refund*
* statistics*

*: Private API

## Installation

```bash
pip3.6 install alfacoins
```

## Getting Started

### Gateway

You can get an instance of `ALFACoins` class like this:

#### For public APIs

```python
from alfacoins import ALFACoins


alfacoins = ALFACoins()
```

#### For private APIs

```python3
from alfacoins import ALFACoins


alfacoins = ALFACoins(
  name='shop-name',
  password='password',
  secret_key='07fc884cf02af307400a9df4f2d15490'
)
```

### Create order

```python3
result = alfacoins.create_order(
    type='litecointestnet',
    amount=1.2345,
    currency='USD',
    order_id=1,
    options={
        'notificationURL': 'https://example.io/notify',
        'redirectURL': 'https://example.io/redirect',
        'payerName': 'Bob',
        'payerEmail': 'no_reply@alfacoins.com',
        },
    description='This is for test!',
)
```

Additional information and API documentation is here: [ALFAcoins API Reference](https://www.alfacoins.com/developers).
