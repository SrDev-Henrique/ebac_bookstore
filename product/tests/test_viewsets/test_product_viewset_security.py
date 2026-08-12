# pyright: reportUnannotatedClassAttribute=false, reportUnknownMemberType=false, reportUninitializedInstanceVariable=false, reportAny=false

import base64
from typing import override

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase

from product.factories import CategoryFactory, ProductFactory
from product.models import Category, Product


class ProductViewSetSecurityTest(APITestCase):
    client: APIClient
    user: User
    username: str
    password: str
    categories: list[Category]
    product: Product
    url: str

    @override
    def setUp(self) -> None:
        self.client = APIClient()
        self.username = 'security-user'
        self.password = 'a-very-secret-password'
        self.user = User.objects.create_user(
            username=self.username,
            email='security@example.com',
            password=self.password,
        )
        self.categories = CategoryFactory.create_batch(2)
        self.product = ProductFactory(category=self.categories)
        self.url = '/bookstore/v1/products/'

    def _detail_url(self) -> str:
        return f'{self.url}{self.product.pk}/'

    def assertDenied(self, response: Response) -> None:
        # DRF answers 401 or 403 depending on which authenticator is listed
        # first (SessionAuthentication provides no WWW-Authenticate header).
        # Either way the request must not be served.
        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )

    # --- anonymous access is allowed on every action ---

    def test_list_allows_anonymous(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_allows_anonymous(self):
        response = self.client.get(self._detail_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_allows_anonymous(self):
        payload = {
            'title': 'Anonymous Book',
            'description': 'Should be created',
            'price': 100,
            'active': True,
            'categories_id': [category.pk for category in self.categories],
        }

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.filter(title='Anonymous Book').exists())

    def test_update_allows_anonymous(self):
        response = self.client.patch(
            self._detail_url(), {'title': 'Updated Anon'}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.title, 'Updated Anon')

    def test_delete_allows_anonymous(self):
        response = self.client.delete(self._detail_url())

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    # --- token authentication (optional; invalid credentials still fail) ---

    def test_valid_token_grants_access(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_token_is_rejected(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token 0000000000invalid')

        response = self.client.get(self.url)

        self.assertDenied(response)

    def test_unrecognized_auth_scheme_falls_back_to_anonymous(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer not-a-drf-scheme')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_of_deleted_user_is_rejected(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        _ = self.user.delete()

        response = self.client.get(self.url)

        self.assertDenied(response)

    def test_inactive_user_token_is_rejected(self):
        token = Token.objects.create(user=self.user)
        self.user.is_active = False
        self.user.save()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = self.client.get(self.url)

        self.assertDenied(response)

    # --- basic authentication ---

    def _basic_header(self, username: str, password: str) -> str:
        raw = f'{username}:{password}'.encode()
        return f'Basic {base64.b64encode(raw).decode()}'

    def test_valid_basic_credentials_grant_access(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=self._basic_header(self.username, self.password)
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wrong_basic_password_is_rejected(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=self._basic_header(self.username, 'wrong')
        )

        response = self.client.get(self.url)

        self.assertDenied(response)

    # --- injection / payload handling ---

    def test_sql_injection_in_query_string_is_not_executed(self):
        response = self.client.get(f"{self.url}?search=1');DROP TABLE product_product;--")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())

    def test_sql_injection_in_detail_lookup_is_not_executed(self):
        response = self.client.get(f"{self.url}1 OR 1=1/")

        self.assertIn(
            response.status_code,
            (status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST),
        )
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())

    def test_script_payload_is_stored_verbatim_and_served_as_json(self):
        payload = {
            'title': '<script>alert(1)</script>',
            'description': 'xss attempt',
            'price': 100,
            'active': True,
            'categories_id': [category.pk for category in self.categories],
        }

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.data['title'], '<script>alert(1)</script>')
        # Served as JSON, never as HTML, so the payload cannot execute.
        self.assertNotIn('text/html', response['Content-Type'])

    def test_read_only_fields_cannot_be_overridden(self):
        response = self.client.patch(
            self._detail_url(), {'id': 9999}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())
        self.assertFalse(Product.objects.filter(pk=9999).exists())
