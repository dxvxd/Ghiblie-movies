import requests
import hashlib


class UrlFetcherException(Exception):
    pass


class NoDataError(UrlFetcherException):
    pass


class ApiServiceError(UrlFetcherException):
    pass


def get_signature(input_string, encoding='utf-8'):
    md5 = hashlib.md5()
    md5.update(input_string.encode(encoding))
    return md5.hexdigest()


class UrlFetcher:

    def __init__(self, url):
        self.url = url
        self.response = self._get_response()
        self.data = self.response.text
        self.signature = get_signature(self.data)

    def _get_response(self):

        response = requests.get(
            self.url,
            stream=False,
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'close'
            }
        )

        if response.status_code == 404:
            raise NoDataError('No data for url')

        if response.status_code != 200:
            raise ApiServiceError(
                f'API status code: {response.status_code}'
            )

        return response

    def get_json(self):
        return self.response.json()
