from collections import namedtuple

Currencies = namedtuple('Currencies', (
    'ETH', 'LTC', 'BTC'
))

currencies = Currencies('ETH', 'LTC', 'BTC')
