from aiohttp import ClientSession

from fetcher import Fetcher


class AsyncFetcher(Fetcher):
    async def fetch(self, url, method="get", data=None):
        if not data:
            data = {}

        async with ClientSession() as session:
            if method == "get":
                request_run = session.get(url, timeout=15, params=data)
            else:
                raise NotImplemented(f"Method {method} is no supported")
            async with request_run as response:
                return await response.json()
