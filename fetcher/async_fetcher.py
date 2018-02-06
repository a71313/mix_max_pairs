from aiohttp import ClientSession

from fetcher import Fetcher


class AsyncFetcher(Fetcher):
    async def fetch(self, url, method="get", data=None):
        if not data:
            data = {}

        async with ClientSession() as session:
            if method == "get":
                request_run = session.get(url, timeout=10, params=data)
            elif method == "post":
                request_run = session.post(url, data, timeout=10)
            else:
                raise NotImplemented(f"Method {method} is no supported")
            async with request_run as response:
                return await response.json()
