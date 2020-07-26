import logging
from unittest import mock

from django.test import TestCase

from catalog.service.data_fetcher import (
    DataFetcher,
    FilmsFetcher,
    PeopleFetcher
)


class DataFetcherBaseTest(TestCase):

    def setUp(self) -> None:
        logging.disable(logging.CRITICAL)
        self.data_url = mock.Mock()
        self.url_fetcher = mock.Mock()


class DataFetcherTest(DataFetcherBaseTest):

    def setUp(self) -> None:
        super().setUp()
        self.data_url.data_hash = 'a'
        self.url_fetcher.signature = 'a'

    def test_refresh_hash_without_changes(self):

        data_fetcher = DataFetcher(self.data_url, self.url_fetcher)

        data_fetcher.refresh()
        self.data_url.update_hash.assert_not_called()

    def test_refresh_hash_with_changes(self):
        data_fetcher = DataFetcher(self.data_url, self.url_fetcher)

        self.url_fetcher.signature = ''

        with mock.patch.object(
                data_fetcher, 'refresh_objects'
        ) as mock_refresh_objects:
            data_fetcher.refresh()

        self.data_url.update_hash.assert_called_once()
        mock_refresh_objects.assert_called_once()


class FilmsFetcherTest(DataFetcherBaseTest):

    @mock.patch('catalog.service.data_fetcher.uuid')
    @mock.patch('catalog.service.data_fetcher.Film')
    def test_refresh_object(self, mock_film, mock_uuid):
        films_fetcher = FilmsFetcher(self.data_url, self.url_fetcher)
        film_obj = mock.Mock()
        mock_film.objects.get_or_create.side_effect = [(film_obj, False)]
        result = films_fetcher.refresh_object(
            {'id': 0, 'title': 'a'}
        )
        self.assertIs(result, film_obj)
        mock_film.objects.get_or_create.assert_called_once()
        mock_uuid.UUID.assert_called_once()


class PeopleFetcherTest(DataFetcherBaseTest):

    @mock.patch('catalog.service.data_fetcher.uuid')
    @mock.patch('catalog.service.data_fetcher.Film')
    @mock.patch('catalog.service.data_fetcher.Character')
    def test_refresh_object(self, mock_character, mock_film, mock_uuid):
        people_fetcher = PeopleFetcher(self.data_url, self.url_fetcher)
        character_obj = mock.Mock()
        mock_character.objects.get_or_create.side_effect = [
            (character_obj, False)
        ]
        result = people_fetcher.refresh_object(
            {'id': 0, 'name': 'a', 'films': ['a/b']}
        )
        self.assertIs(result, character_obj)
        mock_character.objects.get_or_create.assert_called_once()
        mock_film.objects.get.assert_called_once()
        mock_uuid.UUID.has_calls([mock.call(0), mock.call('b')])
