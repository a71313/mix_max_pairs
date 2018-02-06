from exchange_data_fetchers import ExchangeFetcher


class PoloniexFetcher(ExchangeFetcher):
    url = 'https://poloniex.com/public?command=returnTicker'
    name = 'poloniex'

    async def get_pair_value(self, cur1, cur2):
        pair = f'{cur1}_{cur2}'
        res = await self.fetcher.fetch(self.url)
        return {self.name: res[pair]['last']}
