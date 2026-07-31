from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from order.factories import OrderFactory, UserFactory
from order.models import Order
from product.factories import ProductFactory


class OrderViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.products = ProductFactory.create_batch(2)
        self.order = OrderFactory(user=self.user, product=self.products)
        self.url = '/bookstore/v1/orders/'

    def test_list_orders(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_order(self):
        response = self.client.get(f'{self.url}{self.order.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(len(response.data['product']), 2)
        self.assertEqual(
            response.data['total'],
            sum(product.price for product in self.products),
        )

    def test_create_order(self):
        new_user = UserFactory()
        new_products = ProductFactory.create_batch(2)
        payload = {
            'user': new_user.id,
            'products_id': [product.pk for product in new_products],
        }

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['product']), 2)
        self.assertEqual(
            response.data['total'],
            sum(product.price for product in new_products),
        )

    def test_delete_order(self):
        response = self.client.delete(f'{self.url}{self.order.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())

    def test_update_order(self):
        new_user = UserFactory()
        new_products = ProductFactory.create_batch(2)
        payload = {
            'user': new_user.id,
            'products_id': [product.pk for product in new_products],
        }

        response = self.client.put(
            f'{self.url}{self.order.id}/', payload, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], new_user.id)
        self.assertEqual(len(response.data['product']), 2)
        self.assertEqual(
            response.data['total'],
            sum(product.price for product in new_products),
        )

    def test_partial_update_order(self):
        new_products = ProductFactory.create_batch(3)
        payload = {
            'products_id': [product.pk for product in new_products],
        }

        response = self.client.patch(
            f'{self.url}{self.order.id}/', payload, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(len(response.data['product']), 3)
        self.assertEqual(
            response.data['total'],
            sum(product.price for product in new_products),
        )

