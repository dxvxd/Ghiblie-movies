import uuid
import logging


from ..models import Film, Character
from .utils import create_film_from_url

logger = logging.getLogger(__name__)


class DataFetcher:

    def __init__(self, data_url, url_fetcher):
        self.data_url = data_url
        self.fetcher = url_fetcher

    def refresh_objects(self):
        for data in self.fetcher.get_json():
            self.refresh_object(data)

    def refresh_object(self, data):
        raise NotImplementedError()

    def refresh(self):
        if self.data_url.data_hash != self.fetcher.signature:
            logger.info(
                f'URL {self.data_url.name} contains fresh data.'
            )
            self.data_url.update_hash(self.fetcher.signature)
            self.refresh_objects()
        else:
            logger.info(
                f'URL {self.data_url.name} does not contain fresh data.'
            )


class FilmsFetcher(DataFetcher):

    def refresh_object(self, data):
        obj, _ = Film.objects.get_or_create(
            id=uuid.UUID(data['id']),
            title=data['title']
        )
        return obj


class PeopleFetcher(DataFetcher):

    def refresh_object(self, data):
        obj, _ = Character.objects.get_or_create(
            id=uuid.UUID(data['id']),
            name=data['name']
        )

        for film_url in data['films']:
            film_id = film_url.split('/')[-1]
            try:
                film = Film.objects.get(id=uuid.UUID(film_id))
            except Film.DoesNotExist:
                # in a case film is not included in regular film list,
                # but appears in character films list
                film = create_film_from_url(film_url)
            obj.films.add(film)

        return obj
