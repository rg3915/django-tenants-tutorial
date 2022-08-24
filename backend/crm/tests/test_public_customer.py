import json
from django.test import TestCase

from rest_framework import status

from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient


class BaseSetup(TestCase):
    def setUp(self):
        self.payload = {
            "name": "James Stewart"
        }

    def test_create_customer(self):
        response = self.client.post(
            '/crm/api/customers/',
            data=self.payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_customer(self):
        self.client.post(
            '/crm/api/customers/',
            data=self.payload,
            content_type='application/json'
        )
        response = self.client.get('/crm/api/customers/')
        resultado = json.loads(response.content)
        esperado = [{"id": 2, "name": "James Stewart"}]

        self.assertEqual(esperado, resultado)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
