# pyright: reportUnannotatedClassAttribute=false, reportUnknownMemberType=false, reportUninitializedInstanceVariable=false, reportAny=false

from typing import override

from rest_framework import status
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

    def test_list_allows_anonymous(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_allows_anonymous(self):
        response = self.client.get(self._detail_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_allows_anonymous(self):
        payload = {
            'title': 'Anonymous Category',
            'slug': 'anonymous-category',
            'description': 'Should be created',
            'active': True,
        }

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Category.objects.filter(title='Anonymous Category').exists()
        )

    def test_update_allows_anonymous(self):
        response = self.client.patch(
            self._detail_url(), {'title': 'Updated Anon'}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.title, 'Updated Anon')

    def test_delete_allows_anonymous(self):
        response = self.client.delete(self._detail_url())

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(pk=self.category.pk).exists())
