import json

from django.conf import settings
from django.core.management import call_command
from django.db import connection
from django.test import TestCase
# from django_tenants.test.cases import TenantTestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from tenant_schemas.utils import get_public_schema_name, get_tenant_model

from backend.tenant.models import Client

ALLOWED_TEST_DOMAIN = '.localhost'

# class UrlTest(TestCase):

#     def setUp(self) -> None:
#         self.payload = {
#             "name": "James Stewart"
#         }

#     def test_create_customer(self):
#         response = self.client.post(
#             '/crm/api/customers/',
#             data=self.payload,
#             content_type='application/json'
#         )
#         resultado = json.loads(response.content)
#         esperado = {
#             "name": "James Stewart"
#         }

#         self.assertEqual(esperado, resultado)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


class UrlTest(TestCase):

    def setUp(self) -> None:
        super().setUp()
        Client.objects.create(
            domain_url='localhost',
            schema_name='public',
            name='public'
        )
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


# class TenantTestCase(APITestCase):
#     public_tenant = None
#     test_tenant = None
#     test2_tenant = None

#     @classmethod
#     def setUpClass(cls):
#         # cls.add_allowed_test_domain()
#         # cls.setUpTestData()
#         super(TenantTestCase, cls).setUpClass()

#     @classmethod
#     def setUpTestData(cls):
#         print('run setUpTestData')

#         cls.public_tenant = Client.create_tenant('Public')
#         cls.test_tenant = Client.create_tenant('stark')

#         connection.set_tenant(cls.public_tenant)


# class TenantModelTests(TenantTestCase):

#     def setUp(self):
#         self.client = APIClient()
#         super(TenantModelTests, self).setUp()

#     def test_check_public_tenant(self):
#         self.assertIsInstance(self.public_tenant, Client)

#         self.assertEqual(self.public_tenant.name, 'Public', 'Public tenant name is not "Public".')
#         self.assertEqual(self.public_tenant.subdomain, '', 'Public tenant subdomain is not blank.')
#         self.assertEqual(self.public_tenant.schema_name, 'public', 'Public tenant schema_name is not "public".')

#     def test_check_private_tenants(self):
#         self.assertIsInstance(self.test_tenant, Client)

#         self.assertEqual(self.test_tenant.name, 'Test', 'Test tenant name is not "Test".')
#         self.assertEqual(self.test_tenant.subdomain, 'test', 'Test tenant subdomain is not "test".')
#         self.assertEqual(self.test_tenant.schema_name, 'test', 'Test tenant schema_name is not "test".')


# class PublicTenantTestCase(TenantTestCase):
#     @staticmethod
#     def get_test_tenant_domain():
#         return 'localhost'

#     @staticmethod
#     def get_test_schema_name():
#         return 'public'


# class TenantModelTests(PublicTenantTestCase):

#     def setUp(self):
#         self.client = APIClient()
#         super(TenantModelTests, self).setUp()

#     def test_check_public_tenant(self):
#         self.assertIsInstance(self.public_tenant, Client)

#         self.assertEqual(self.public_tenant.name, 'Public', 'Public tenant name is not "Public".')
#         self.assertEqual(self.public_tenant.subdomain, '', 'Public tenant subdomain is not blank.')
#         self.assertEqual(self.public_tenant.schema_name, 'public', 'Public tenant schema_name is not "public".')

#     def test_check_private_tenants(self):
#         self.assertIsInstance(self.test_tenant, Client)

#         self.assertEqual(self.test_tenant.name, 'Test', 'Test tenant name is not "Test".')
#         self.assertEqual(self.test_tenant.subdomain, 'test', 'Test tenant subdomain is not "test".')
#         self.assertEqual(self.test_tenant.schema_name, 'test', 'Test tenant schema_name is not "test".')


class TenantTestCase(TestCase):
    @classmethod
    def add_allowed_test_domain(cls):
        # ALLOWED_HOSTS is a special setting of Django setup_test_environment so we can't modify it with helpers
        if ALLOWED_TEST_DOMAIN not in settings.ALLOWED_HOSTS:
            settings.ALLOWED_HOSTS += [ALLOWED_TEST_DOMAIN]

    @classmethod
    def remove_allowed_test_domain(cls):
        if ALLOWED_TEST_DOMAIN in settings.ALLOWED_HOSTS:
            settings.ALLOWED_HOSTS.remove(ALLOWED_TEST_DOMAIN)

    @classmethod
    def setUpClass(cls):
        cls.sync_shared()
        cls.add_allowed_test_domain()
        tenant_domain = 'stark.localhost'
        cls.tenant = get_tenant_model()(domain_url=tenant_domain, schema_name='stark')
        cls.tenant.save(verbosity=0)  # todo: is there any way to get the verbosity from the test command here?

        connection.set_tenant(cls.tenant)

    @classmethod
    def tearDownClass(cls):
        connection.set_schema_to_public()
        cls.tenant.delete()

        cls.remove_allowed_test_domain()
        cursor = connection.cursor()
        cursor.execute('DROP SCHEMA IF EXISTS stark CASCADE')

    @classmethod
    def sync_shared(cls):
        call_command('migrate_schemas',
                     schema_name=get_public_schema_name(),
                     interactive=False,
                     verbosity=0)


class FastTenantTestCase(TenantTestCase):
    @classmethod
    def setUpClass(cls):
        cls.sync_shared()
        cls.add_allowed_test_domain()
        tenant_domain = 'stark.localhost'

        TenantModel = get_tenant_model()
        try:
            cls.tenant = TenantModel.objects.get(domain_url=tenant_domain, schema_name='stark')
        except:
            cls.tenant = TenantModel(domain_url=tenant_domain, schema_name='stark')
            cls.tenant.save(verbosity=0)

        connection.set_tenant(cls.tenant)

    @classmethod
    def tearDownClass(cls):
        connection.set_schema_to_public()
        cls.remove_allowed_test_domain()
