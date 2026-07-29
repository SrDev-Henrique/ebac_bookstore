from django.db import IntegrityError
from django.test import TestCase

from order.models import Order
from order.tests.factories import OrderFactory, UserFactory
from product.tests.factories import ProductFactory


class OrderModelTest(TestCase):
    def test_create_order(self):
        user = UserFactory()
        product = ProductFactory()
        order = OrderFactory(user=user, product=[product])

        self.assertEqual(order.user, user)
        self.assertEqual(order.product.count(), 1)
        self.assertIn(product, order.product.all())

    def test_order_requires_user(self):
        with self.assertRaises(IntegrityError):
            Order.objects.create()

    def test_order_can_have_multiple_products(self):
        products = ProductFactory.create_batch(3)
        order = OrderFactory(product=products)

        self.assertEqual(order.product.count(), 3)

    def test_deleting_user_deletes_order(self):
        user = UserFactory()
        order = OrderFactory(user=user)
        order_id = order.id

        user.delete()

        self.assertFalse(Order.objects.filter(id=order_id).exists())
