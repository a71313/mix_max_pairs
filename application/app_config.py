import inject


def main_configuration(binder):
    from application import Application
    from application.application_impl import ApplicationImpl
    from fetcher import Fetcher
    from fetcher.async_fetcher import AsyncFetcher

    binder.bind_to_constructor(Fetcher, lambda: AsyncFetcher())

    binder.bind(Application, ApplicationImpl())


def configurate():
    inject.configure_once(main_configuration)
