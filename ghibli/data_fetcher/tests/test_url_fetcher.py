from unittest import mock

from django.test import TestCase

from data_fetcher.url_fetcher import (
    get_signature,
    UrlFetcher,
    ApiServiceError,
    NoDataError
)


class SignatureTest(TestCase):

    def test_signature_length(self):
        signature_string = get_signature('a')
        self.assertEqual(32, len(signature_string))


class UrlFetcherErrorsTest(TestCase):

    def setUp(self):
        self.response = mock.MagicMock()

    @mock.patch('data_fetcher.url_fetcher.requests')
    def test_get_response_404(self, mock_requests):
        self.response.status_code = 404
        mock_requests.get.return_value = self.response

        with self.assertRaises(NoDataError):
            UrlFetcher('url')

    @mock.patch('data_fetcher.url_fetcher.requests')
    def test_get_response_401(self, mock_requests):
        self.response.status_code = 401
        mock_requests.get.return_value = self.response

        with self.assertRaises(ApiServiceError):
            UrlFetcher('url')


class UrlFetcherTest(TestCase):

    def setUp(self):
        self.response = mock.MagicMock()
        self.response.status_code = 200
        self.response.text = 'data_value'

    @mock.patch('data_fetcher.url_fetcher.requests')
    def test_fetcher_has_data(self, mock_requests):
        mock_requests.get.return_value = self.response

        url_fetcher = UrlFetcher('url')
        self.assertTrue(hasattr(url_fetcher, 'data'))

    @mock.patch('data_fetcher.url_fetcher.requests')
    def test_fetcher_signature(self, mock_requests):
        mock_requests.get.return_value = self.response

        url_fetcher = UrlFetcher('url')
        self.assertEqual(
            get_signature(self.response.text), url_fetcher.signature
        )

    @mock.patch('data_fetcher.url_fetcher.requests')
    def test_fetcher_get_json(self, mock_requests):
        mock_requests.get.return_value = self.response

        url_fetcher = UrlFetcher('url')
        url_fetcher.response.json = mock.MagicMock()
        url_fetcher.get_json()
        url_fetcher.response.json.assert_called_once()
