import logging

from data_fetcher.models import DataURL
from data_fetcher.url_fetcher import UrlFetcher
from .data_fetcher import FilmsFetcher, PeopleFetcher

__all__ = ['refresh_data']

logger = logging.getLogger(__name__)


def refresh_data():
    logger.info('Refreshing data.')
    try:
        films_data_url = DataURL.objects.get(name='films')
        films_url_fetcher = UrlFetcher(films_data_url.url)
        FilmsFetcher(films_data_url, films_url_fetcher).refresh()
    except DataURL.DoesNotExist:
        logger.error('No defined DataURL with name: films')

    try:
        people_data_url = DataURL.objects.get(name='people')
        people_url_fetcher = UrlFetcher(people_data_url.url)
        PeopleFetcher(people_data_url, people_url_fetcher).refresh()
    except DataURL.DoesNotExist:
        logger.error('No defined DataURL with name: people')
