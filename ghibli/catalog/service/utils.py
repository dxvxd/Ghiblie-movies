import uuid
import logging

from data_fetcher.url_fetcher import UrlFetcher
from ..models import Film

logger = logging.getLogger(__name__)


def create_film_from_url(url):
    film_fetcher = UrlFetcher(url)
    data = film_fetcher.get_json()
    return Film.objects.create(
        id=uuid.UUID(data['id']),
        name=data['name']
    )
