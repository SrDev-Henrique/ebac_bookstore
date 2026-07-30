from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from product.factories import CategoryFactory, ProductFactory
from product.models import Product


class ProductViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.categories = CategoryFactory.create_batch(2)
        self.product = ProductFactory(category=self.categories)
        self.url = '/bookstore/v1/products/'

    def test_list_products(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_product(self):
        response = self.client.get(f'{self.url}{self.product.pk}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.product.title)
        self.assertEqual(response.data['price'], self.product.price)
        self.assertEqual(len(response.data['category']), 2)

    def test_create_product(self):
        new_categories = CategoryFactory.create_batch(2)
        payload = {
            'title': 'New Book',
            'description': 'A new book',
            'price': 5000,
            'active': True,
            'categories_id': [category.pk for category in new_categories],
        }

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Book')
        self.assertEqual(response.data['price'], 5000)
        self.assertEqual(len(response.data['category']), 2)

    def test_delete_product(self):
        response = self.client.delete(f'{self.url}{self.product.pk}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_update_product(self):
        new_categories = CategoryFactory.create_batch(2)
        payload = {
            'title': 'Updated Book',
            'description': 'Updated description',
            'price': 7500,
            'active': False,
            'categories_id': [category.pk for category in new_categories],
        }

        response = self.client.put(
            f'{self.url}{self.product.pk}/', payload, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Book')
        self.assertEqual(response.data['price'], 7500)
        self.assertEqual(response.data['active'], False)
        self.assertEqual(len(response.data['category']), 2)

    def test_partial_update_product(self):
        payload = {'title': 'Partially Updated Book', 'price': 3000}

        response = self.client.patch(
            f'{self.url}{self.product.pk}/', payload, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Partially Updated Book')
        self.assertEqual(response.data['price'], 3000)
        self.assertEqual(len(response.data['category']), 2)

