import logging

from django.test import TestCase
from django.urls import reverse


class FilmsViewTest(TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def test_list(self):
        response = self.client.get(reverse('film-list'))
        self.assertEqual(response.status_code, 200)
