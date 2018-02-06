from abc import ABCMeta, abstractmethod

import inject

from fetcher import Fetcher


class ExchangeFetcher(metaclass=ABCMeta):
    @inject.params(fetcher=Fetcher)
    def __init__(self, fetcher):
        self.fetcher = fetcher

    @abstractmethod
    def get_pair_value(self) -> dict:
        pass
