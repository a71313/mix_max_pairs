from abc import ABCMeta, abstractmethod


class Fetcher(metaclass=ABCMeta):
    @abstractmethod
    def fetch(self, url, data=None):
        pass


