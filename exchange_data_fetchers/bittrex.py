from exchange_data_fetchers import ExchangeFetcher


class BittrexFetcher(ExchangeFetcher):
    url = 'https://bittrex.com/api/v1.1/public/getticker'
    name = 'bittrex'

    async def get_pair_value(self, cur1, cur2):
        pair = f'{cur1}-{cur2}'

        data = {'market': pair}

        res = await self.fetcher.fetch(self.url, data=data)

        return {self.name: res['result']['Last']}
