from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from product.factories import CategoryFactory
from product.models import Category


class CategoryViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = CategoryFactory(title='books')
        self.url = '/bookstore/v1/categories/'

    def test_list_categories(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_category(self):
        response = self.client.get(f'{self.url}{self.category.pk}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.category.title)
        self.assertEqual(response.data['slug'], self.category.slug)
        self.assertEqual(response.data['description'], self.category.description)
        self.assertEqual(response.data['active'], self.category.active)

    def test_create_category(self):
        payload = {
            'title': 'Fiction',
            'slug': 'fiction',
            'description': 'Fiction books',
            'active': True,
        }

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Fiction')
        self.assertEqual(response.data['slug'], 'fiction')
        self.assertEqual(response.data['active'], True)

    def test_delete_category(self):
        response = self.client.delete(f'{self.url}{self.category.pk}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(pk=self.category.pk).exists())

    def test_update_category(self):
        payload = {
            'title': 'Updated Category',
            'slug': 'updated-category',
            'description': 'Updated description',
            'active': False,
        }

        response = self.client.put(
            f'{self.url}{self.category.pk}/', payload, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Category')
        self.assertEqual(response.data['slug'], 'updated-category')
        self.assertEqual(response.data['active'], False)

    def test_partial_update_category(self):
        payload = {'title': 'Partially Updated'}

        response = self.client.patch(
            f'{self.url}{self.category.pk}/', payload, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Partially Updated')
        self.assertEqual(response.data['slug'], self.category.slug)

