from collections import namedtuple

Currencies = namedtuple('Currencies', (
    'ETH', 'LTC', 'BTC', 'USD'
))

currencies = Currencies('ETH', 'LTC', 'BTC', 'USD')
