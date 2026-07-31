# pyright: reportUnannotatedClassAttribute=false, reportUnknownMemberType=false, reportUninitializedInstanceVariable=false, reportAny=false

from typing import override

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase

from product.factories import CategoryFactory
from product.models import Category


class CategoryViewSetSecurityTest(APITestCase):
    client: APIClient
    category: Category
    url: str

    @override
    def setUp(self) -> None:
        self.client = APIClient()
        self.category = CategoryFactory(title='books')
        self.url = '/bookstore/v1/categories/'

    def _detail_url(self) -> str:
        return f'{self.url}{self.category.pk}/'

    def assertDenied(self, response: Response) -> None:
        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )

    def test_list_requires_authentication(self):
        response = self.client.get(self.url)

        self.assertDenied(response)

    def test_retrieve_requires_authentication(self):
        response = self.client.get(self._detail_url())

        self.assertDenied(response)

    def test_create_requires_authentication(self):
        payload = {
            'title': 'Anonymous Category',
            'slug': 'anonymous-category',
            'description': 'Should not be created',
            'active': True,
        }

        response = self.client.post(self.url, payload, format='json')

        self.assertDenied(response)
        self.assertFalse(
            Category.objects.filter(title='Anonymous Category').exists()
        )

    def test_update_requires_authentication(self):
        response = self.client.patch(
            self._detail_url(), {'title': 'Hacked'}, format='json'
        )

        self.assertDenied(response)
        self.category.refresh_from_db()
        self.assertNotEqual(self.category.title, 'Hacked')

    def test_delete_requires_authentication(self):
        response = self.client.delete(self._detail_url())

        self.assertDenied(response)
        self.assertTrue(Category.objects.filter(pk=self.category.pk).exists())
