import asyncio
# from pool import Pool
#
from functools import partial

from application import Application
from application.currencies import currencies
from exchange_data_fetchers.bitfinex import BitfinexFetcher
from exchange_data_fetchers.bittrex import BittrexFetcher
from exchange_data_fetchers.livecoin import LivecoinFetcher
from exchange_data_fetchers.poloniex import PoloniexFetcher
from pool import Pool


class ApplicationImpl(Application):
    loop = asyncio.get_event_loop()
    difference = 0.01

    strategy = (
        # {'pair': (currencies.BTC, currencies.LTC), 'func': min,
        #  'to_revert': (LivecoinFetcher, BitfinexFetcher), 'calc_through': tuple(), 'skip': tuple()},
        {'pair': (currencies.LTC, currencies.ETH), 'func': min,
         'to_revert': tuple(),
         'calc_through': (BitfinexFetcher, LivecoinFetcher),
         'skip': (PoloniexFetcher, BittrexFetcher)
         },
        {'pair': (currencies.ETH, currencies.BTC), 'func': max,
         'to_revert': (PoloniexFetcher, BittrexFetcher),
         'calc_through': tuple(),
         'skip': tuple()
         },
    )

    def __init__(self, usable_exchange_fetchers=None):
        super().__init__()
        self._usable_exchange_fetchers = usable_exchange_fetchers

    @property
    def usable_exchange_fetchers(self):
        if not self._usable_exchange_fetchers:
            self._usable_exchange_fetchers = (LivecoinFetcher(), BittrexFetcher(), BitfinexFetcher(), PoloniexFetcher())
        return self._usable_exchange_fetchers

    def _make_futures(self, fetchers, step):
        futures = []
        for fetcher in self.usable_exchange_fetchers:
            if isinstance(fetcher, step['to_revert']):
                futures.append(partial(self.reverted, **dict(fetcher=fetcher,
                                                             cur1=step['pair'][0], cur2=step['pair'][1])))
            elif isinstance(fetcher, step['calc_through']):
                futures.append(partial(self.calc_through_usd, **dict(fetcher=fetcher,
                                                                     cur1=step['pair'][0], cur2=step['pair'][1])))
            elif isinstance(fetcher, step['skip']):
                pass
            else:
                futures.append(partial(fetcher.get_pair_value, *(step['pair'][0], step['pair'][1])))
        return futures

    async def calc_through_usd(self, fetcher, cur1, cur2):
        res1 = await fetcher.get_pair_value(cur1, currencies.USD)
        res2 = await fetcher.get_pair_value(cur2, currencies.USD)
        return (res1[0], res1[1] / res2[1])

    async def reverted(self, fetcher, cur1, cur2):
        res = await fetcher.get_pair_value(cur2, cur1)
        # return (res[0], 1 / res[1])
        return res

    async def get_min_max(self):
        for step in self.strategy:
            print(f'Finding {step["func"].__name__} for pair {step["pair"][0]}/{step["pair"][1]}')
            futures = self._make_futures(self.usable_exchange_fetchers, step)
            pool = Pool(futures)
            res = await pool.run()
            print(res)
            res = filter(None, res)
            func = step['func']
            gotten_func_res = func(res, key=lambda x: x[1])
            print(f'Found {step["func"].__name__}. It is {gotten_func_res[0]} exchange with value {gotten_func_res[1]}')

    def run(self):
        self.loop.run_until_complete(self.get_min_max())
        # self.loop.run_forever()
