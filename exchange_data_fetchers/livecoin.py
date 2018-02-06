from exchange_data_fetchers import ExchangeFetcher


class LivecoinFetcher(ExchangeFetcher):
    url = 'https://api.livecoin.net/exchange/ticker'
    name = 'livecoin'

    async def get_pair_value(self, cur1, cur2):
        pair = f'{cur1}/{cur2}'

        data = {'currencyPair': pair}

        res = await self.fetcher.fetch(self.url, data=data)

        return (self.name, res['last'])
