import traceback
from logging import getLogger

import asyncio


class Pool:

    def __init__(self, coroutines, size=10, ignore_errors=False):
        self.semaphore = asyncio.Semaphore(size)
        self.tasks = [asyncio.ensure_future(self.sub(f)) for f in coroutines]
        self.ignore_errors = ignore_errors

    async def sub(self, func):
        async with self.semaphore:
            return await func()

    async def run(self):
        exc = None
        results = []
        for a in asyncio.as_completed(self.tasks, loop=asyncio.get_event_loop()):
            try:
                result = await a
                results.append(result)
            except asyncio.CancelledError as e:
                exc = e
            except Exception as e:
                traceback.print_exc()
                for t in self.tasks:
                    t.cancel()
                exc = e
        if exc:
            if not self.ignore_errors:
                raise exc

        return results