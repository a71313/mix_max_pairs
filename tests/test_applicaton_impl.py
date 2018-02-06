import asyncio
from unittest import TestCase
from unittest.mock import MagicMock

import inject

from application.application_impl import ApplicationImpl
from application.currencies import currencies
from exchange_data_fetchers import ExchangeFetcher
from fetcher import Fetcher


class A(ExchangeFetcher):
    async def get_pair_value(self, cur1, cur2):
        return ('a', 1.1)


class B(ExchangeFetcher):
    async def get_pair_value(self, cur1, cur2):
        return ('b', 1.2)


class C(ExchangeFetcher):
    async def get_pair_value(self, cur1, cur2):
        return ('c', 1.3)


class D(ExchangeFetcher):
    async def get_pair_value(self, cur1, cur2):
        return ('d', 1.4)


def test_config(binder):
    binder.bind_to_constructor(Fetcher, lambda: MagicMock())


class TestApp(TestCase):
    def setUp(self):
        inject.clear_and_configure(test_config)
        self.app = ApplicationImpl(usable_exchange_fetchers=(A(), B(), C(), D()))
        self.loop = asyncio.new_event_loop()

    def test_make_futures(self):
        step = {'pair': (currencies.BTC, currencies.LTC), 'func': MagicMock(),
                'to_revert': (A,), 'calc_through': (B,), 'skip': (C,)}

        futures = self.app._make_futures(fetchers=(A(), B(), C(), D()), step=step)

        res = [self.loop.run_until_complete(f()) for f in futures]

        expected = [('a', 1.1), ('b', 1.0), ('d', 1.4)]

        self.assertEqual(res, expected)

    def test_min(self):
        step = {'pair': (currencies.BTC, currencies.LTC), 'func': min,
                'to_revert': tuple(), 'calc_through': tuple(), 'skip': tuple()}

        res = self.loop.run_until_complete(self.app.run_step(step))

        expected = ('a', 1.1)
        self.assertEqual(res, expected)

    def test_max(self):
        step = {'pair': (currencies.BTC, currencies.LTC), 'func': max,
                'to_revert': tuple(), 'calc_through': tuple(), 'skip': tuple()}

        res = self.loop.run_until_complete(self.app.run_step(step))

        expected = ('d', 1.4)
        self.assertEqual(res, expected)