# pyright: reportUnannotatedClassAttribute=false, reportUnknownMemberType=false, reportUninitializedInstanceVariable=false, reportAny=false

from typing import override

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase

from order.factories import OrderFactory, UserFactory
from order.models import Order
from product.factories import ProductFactory
from product.models.product import Product


class OrderViewSetSecurityTest(APITestCase):
    client: APIClient
    user: User
    products: list[Product]
    order: Order
    url: str

    @override
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = UserFactory()
        self.products = ProductFactory.create_batch(2)
        self.order = OrderFactory(user=self.user, product=self.products)
        self.url = '/bookstore/v1/orders/'

    def _detail_url(self) -> str:
        return f'{self.url}{self.order.pk}/'

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
        new_user = UserFactory()
        new_products = ProductFactory.create_batch(2)
        payload = {
            'user': new_user.pk,
            'products_id': [product.pk for product in new_products],
        }

        response = self.client.post(self.url, payload, format='json')

        self.assertDenied(response)
        self.assertFalse(Order.objects.filter(user=new_user).exists())

    def test_update_requires_authentication(self):
        new_user = UserFactory()
        payload = {'user': new_user.pk}

        response = self.client.patch(self._detail_url(), payload, format='json')

        self.assertDenied(response)
        self.order.refresh_from_db()
        self.assertEqual(self.order.user.pk, self.user.pk)

    def test_delete_requires_authentication(self):
        response = self.client.delete(self._detail_url())

        self.assertDenied(response)
        self.assertTrue(Order.objects.filter(pk=self.order.pk).exists())
