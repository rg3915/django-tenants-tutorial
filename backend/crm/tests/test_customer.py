import json

from django.test import TestCase
from rest_framework import status


class UrlTest(TestCase):

    def setUp(self) -> None:
        self.payload = {
            "name": "James Stewart"
        }

    def test_create_customer(self):
        response = self.client.post(
            '/crm/api/customers/',
            data=self.payload,
            content_type='application/json'
        )
        resultado = json.loads(response.content)
        esperado = {
            "name": "James Stewart"
        }

        self.assertEqual(esperado, resultado)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
